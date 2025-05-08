import numpy as np
import sys

file = sys.argv[1]

print(np.memmap(file, dtype='int16', mode='r').shape)