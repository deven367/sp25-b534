#!/bin/bash
#SBATCH -p general
#SBATCH --job-name=b534
#SBATCH --account=cogneuroai
#SBATCH --output=./logs/%j.txt
#SBATCH --error=./logs/%j.err
#SBATCH --mem=64G
#SBATCH --tasks-per-node=10
#SBATCH --gres=gpu:L40S:2
#SBATCH --time=1:00:00


set -e
source /u/demistry/.venv/bin/activate
echo running with batch size $1 and context length $2
torchrun --nproc_per_node=2 nt3.py --batch_size $1 --seq_len $2 --epochs 10 --data_path train.bin

echo "**************************************"
