import os
import time
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from torch.utils.data.distributed import DistributedSampler
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.distributed import init_process_group, destroy_process_group


# ===== Dataset =====
class RandomTokenDataset(Dataset):
    def __init__(self, size, seq_len, vocab_size):
        self.data = torch.randint(0, vocab_size, (size, seq_len))
        self.labels = torch.randint(0, vocab_size, (size, seq_len))

    def __len__(self):
        return self.data.size(0)

    def __getitem__(self, idx):
        return self.data[idx], self.labels[idx]


# ===== Model =====
class SimpleTransformer(nn.Module):
    def __init__(self, vocab_size=512, seq_len=128, dim=768, depth=12, heads=12, mlp_dim=2048):
        super().__init__()
        self.token_embed = nn.Embedding(vocab_size, dim)
        self.pos_embed = nn.Parameter(torch.zeros(1, seq_len, dim))
        self.layers = nn.ModuleList([
            nn.TransformerEncoderLayer(d_model=dim, nhead=heads, dim_feedforward=mlp_dim, batch_first=True)
            for _ in range(depth)
        ])
        self.norm = nn.LayerNorm(dim)
        self.output = nn.Linear(dim, vocab_size)

    def forward(self, x):
        x = self.token_embed(x) + self.pos_embed
        for layer in self.layers:
            x = layer(x)
        x = self.norm(x)
        return self.output(x)


# ===== DDP Setup =====
def ddp_setup():
    torch.cuda.set_device(int(os.environ["LOCAL_RANK"]))
    init_process_group(backend="nccl")


# ===== Trainer =====
class Trainer:
    def __init__(self, model, dataloader, optimizer):
        self.rank = int(os.environ["LOCAL_RANK"])
        self.device = torch.device(f"cuda:{self.rank}")
        self.model = DDP(model.to(self.device), device_ids=[self.rank])
        self.dataloader = dataloader
        self.optimizer = optimizer

    def train(self, epochs):
        for epoch in range(epochs):
            self.dataloader.sampler.set_epoch(epoch)
            start_time = time.time()
            total_loss = 0

            for x, y in self.dataloader:
                x, y = x.to(self.device), y.to(self.device)
                self.optimizer.zero_grad()
                out = self.model(x)
                loss = F.cross_entropy(out.view(-1, out.size(-1)), y.view(-1))
                loss.backward()
                self.optimizer.step()
                total_loss += loss.item()

            torch.cuda.synchronize()
            elapsed = time.time() - start_time
            print(f"[GPU {self.rank}] Epoch {epoch+1} | Loss: {total_loss:.2f} | Time: {elapsed:.2f}s")


# ===== Main =====
def main(batch_size, epochs):
    ddp_setup()

    vocab_size = 512
    seq_len = 128
    dataset = RandomTokenDataset(size=50000, seq_len=seq_len, vocab_size=vocab_size)
    sampler = DistributedSampler(dataset)
    dataloader = DataLoader(dataset, batch_size=batch_size, sampler=sampler, pin_memory=True)

    model = SimpleTransformer(vocab_size=vocab_size, seq_len=seq_len)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)

    trainer = Trainer(model, dataloader, optimizer)
    trainer.train(epochs)

    destroy_process_group()


# ===== Entry Point =====
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=5)
    parser.add_argument("--batch_size", type=int, default=8)
    args = parser.parse_args()
    main(batch_size=args.batch_size, epochs=args.epochs)
