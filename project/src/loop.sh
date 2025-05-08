#!/bin/bash
set -e

source /u/demistry/.venv/bin/activate

for bsz in 64 128; do
  for ctx in 512 1024 2048; do
    # echo torchrun --nproc_per_node=2 ddp_train.py --batch_size $bsz --seq_len $ctx --epochs 1
    # torchrun --nproc_per_node=2 newtrainer.py --batch_size $bsz --seq_len $ctx --epochs 10
    sbatch run.sh $bsz $ctx
    echo "**************************************"
  done
done
