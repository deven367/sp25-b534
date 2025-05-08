import os
import time
import torch
import numpy as np
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


class DatasetWithStride(Dataset):
    """Dataset that returns overlapping chunks of data with a specified stride.

    Args:
        Dataset: PyTorch Dataset base class
    """

    def __init__(self, data, block_size, stride):
        self.data = data
        self.block_size = block_size
        self.stride = stride
        self.num_samples = (len(data) - block_size) // stride

    def __len__(self):
        return self.num_samples

    def __getitem__(self, idx):
        start_idx = idx * self.stride
        chunk = self.data[start_idx : start_idx + self.block_size + 1]
        x = torch.tensor(chunk[:-1], dtype=torch.long)
        y = torch.tensor(chunk[1:], dtype=torch.long)
        return x, y


# ===== Model =====
class SimpleTransformer(nn.Module):
    def __init__(self, vocab_size=512, seq_len=128, dim=300, depth=5, heads=5, mlp_dim=2048):
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
    def __init__(self, model, dataloader, optimizer, conf_name):
        self.conf_name = conf_name
        self.rank = int(os.environ["LOCAL_RANK"])
        self.device = torch.device(f"cuda:{self.rank}")
        self.model = DDP(model.to(self.device), device_ids=[self.rank])
        self.dataloader = dataloader
        self.optimizer = optimizer

        # Create CSV files with headers if they don't exist
        if self.rank == 0:
            # For epoch-level logging
            if not os.path.exists(f"{self.conf_name}_epochs.csv"):
                with open(f"{self.conf_name}_epochs.csv", "w") as f:
                    f.write("rank,epoch,loss,perplexity,time\n")

            # For step-level logging
            if not os.path.exists(f"{self.conf_name}_steps.csv"):
                with open(f"{self.conf_name}_steps.csv", "w") as f:
                    f.write("rank,epoch,step,loss,perplexity,time\n")

    def train(self, epochs):
        step = 0
        log_steps = 100  # Log every 100 steps

        for epoch in range(epochs):
            self.dataloader.sampler.set_epoch(epoch)
            start_time = time.time()
            epoch_start_time = time.time()
            total_loss = 0
            ppl = 0
            batch_count = 0
            step_loss = 0
            step_ppl = 0
            step_count = 0

            for batch_idx, (x, y) in enumerate(self.dataloader):
                step += 1
                step_count += 1

                x, y = x.long(), y.long()
                x, y = x.to(self.device), y.to(self.device)
                self.optimizer.zero_grad()

                # Handle potential dimension issues with the positional embeddings
                seq_len = x.size(1)
                if seq_len > self.model.module.pos_embed.size(1):
                    print(f"Warning: Input sequence length {seq_len} exceeds model's position embedding size {self.model.module.pos_embed.size(1)}")
                    x = x[:, :self.model.module.pos_embed.size(1)]
                    y = y[:, :self.model.module.pos_embed.size(1)]

                out = self.model(x)
                loss = F.cross_entropy(out.view(-1, out.size(-1)), y.view(-1))
                loss.backward()
                self.optimizer.step()

                current_loss = loss.item()
                current_ppl = torch.exp(loss).item()
                total_loss += current_loss
                ppl += current_ppl
                batch_count += 1

                step_loss += current_loss
                step_ppl += current_ppl

                # Log every log_steps steps
                if step % log_steps == 0:
                    avg_step_loss = step_loss / step_count
                    avg_step_ppl = step_ppl / step_count
                    elapsed = time.time() - start_time
                    tokens_per_sec = (x.size(0) * x.size(1) * step_count) / elapsed

                    print(f"[GPU {self.rank}] Epoch {epoch+1} | Step {step} | "
                          f"Loss: {avg_step_loss:.4f} | Perplexity: {avg_step_ppl:.4f} | "
                          f"Tokens/sec: {tokens_per_sec:.2f}")

                    # Log to CSV
                    with open(f"{self.conf_name}_steps.csv", "a") as f:
                        f.write(f"{self.rank},{epoch+1},{step},{avg_step_loss:.4f},{avg_step_ppl:.4f},{elapsed:.4f}\n")

                    # Reset step counters
                    step_loss = 0
                    step_ppl = 0
                    step_count = 0
                    start_time = time.time()

            torch.cuda.synchronize()
            epoch_elapsed = time.time() - epoch_start_time

            avg_loss = total_loss / batch_count if batch_count > 0 else 0
            avg_ppl = ppl / batch_count if batch_count > 0 else 0

            # Log epoch results
            with open(f"{self.conf_name}_epochs.csv", "a") as f:
                f.write(f"{self.rank},{epoch+1},{avg_loss:.4f},{avg_ppl:.4f},{epoch_elapsed:.4f}\n")

            print(f"[GPU {self.rank}] Epoch {epoch+1} Complete | "
                  f"Loss: {avg_loss:.4f} | Perplexity: {avg_ppl:.4f} | "
                  f"Time: {epoch_elapsed:.2f}s")


# ===== Main =====
def main(batch_size, epochs, seq_len, data_path=None):
    ddp_setup()

    vocab_size = 50257

    # Use the appropriate dataset based on data_path
    if data_path and os.path.exists(data_path):
        try:
            data = np.memmap(data_path, dtype=np.uint16, mode='r')
            dataset = DatasetWithStride(data, block_size=seq_len, stride=seq_len // 2)
        except Exception as e:
            print(f"Error loading memmap data: {e}")
            print("Falling back to random dataset")
            dataset = RandomTokenDataset(size=50000, seq_len=seq_len, vocab_size=vocab_size)
    else:
        dataset = RandomTokenDataset(size=50000, seq_len=seq_len, vocab_size=vocab_size)

    sampler = DistributedSampler(dataset)
    dataloader = DataLoader(dataset, batch_size=batch_size, sampler=sampler, pin_memory=True)

    model = SimpleTransformer(vocab_size=vocab_size, seq_len=seq_len)

    if int(os.environ["LOCAL_RANK"]) == 0:
        num_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
        print(f"Model Parameters: {num_params / 1e6:.2f}M")
        print(f"Batch Size: {batch_size}, Epochs: {epochs}, Sequence Length: {seq_len}")
        print(f"Num of batches: {len(dataloader)}")
        print(f"Dataset type: {type(dataset).__name__}")

    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)

    conf_name = f"benchmarks_{batch_size}_{epochs}_{seq_len}"

    trainer = Trainer(model, dataloader, optimizer, conf_name)
    trainer.train(epochs)

    destroy_process_group()


# ===== Entry Point =====
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=5)
    parser.add_argument("--batch_size", type=int, default=8)
    parser.add_argument("--seq_len", type=int, default=128)
    parser.add_argument("--data_path", type=str, default=None,
                        help="Path to memmap data file. If not provided, random data will be used.")
    args = parser.parse_args()

    main(
        batch_size=args.batch_size,
        epochs=args.epochs,
        seq_len=args.seq_len,
        data_path=args.data_path
    )