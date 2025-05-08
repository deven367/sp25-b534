#!/bin/bash
#SBATCH -J smoothing
#SBATCH -p gpu
#SBATCH -A r00286
#SBATCH -o ./logs/%j.txt
#SBATCH -e ./logs/%j.err
#SBATCH --mail-type=ALL
#SBATCH --mail-user=demistry@iu.edu
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=10
#SBATCH --gpus-per-node=4
#SBATCH --time=1:00:00
#SBATCH --mem=64G

set -e
source /N/slate/demistry/.qvenv/bin/activate
echo running with batch size $1 and context length $2
torchrun --nproc_per_node=4 nt3.py --batch_size $1 --seq_len $2 --epochs 10 --data_path train.bin

echo "**************************************"
