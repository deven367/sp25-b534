import torch
from torch.utils.data import Dataset


class MyTrainDataset(Dataset):
    def __init__(self, size):
        self.size = size
        self.data = [(torch.rand(20), torch.rand(1)) for _ in range(size)]

    def __len__(self):
        return self.size

    def __getitem__(self, index):
        return self.data[index]

class DatasetWithStride(Dataset):
    """_summary_

    Args:
        Dataset (_type_): _description_
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
        x = chunk[:-1]
        y = chunk[1:]
        # print(idx, chunk.shape, x.shape, y.shape)
        return x, y