# Distributed Training in PyTorch

Running this entire project has a lot of steps. This project was run on the Quartz cluster of IU's HPC. These experiments were done with 4 NVIDIA H100s and took about an hour to run in total.

## setup

1. request resources on Quartz using the Slurm command
   ```sh
   salloc -p hopper -A r00286 --nodes=1 --tasks-per-node=10 --gpus-per-node=4 --mem=64G --time=3:00:00
   ```
2. create a virtual env and install the requirements
   ```sh
   module load python/gpu/3.10.10
   python -m venv .venv
   source activate .venv/bin/activate
   pip install torch numpy pandas seaborn
   ```
3. once the dependencies are installed
   ```sh
   git clone https://github.com/deven367/sp25-b534
   cd sp25-b534/project/src
   bash loop.sh
   ```

The command will run all the configs and create a bunch of csv files in the `bench` folder.

Once the files benchmarks are in, I compile them into a master file, using the `process.py` file.

```sh
cd bench
python process.py
```

Once the master csv files for epochs and steps are ready, the plots can be generated. The plots are generated using the `plot.ipynb`.

Finally, the expected report is available in the `project` folder, as `report.pdf`.

I personally really enjoyed working on this project, as I love working with such systems and training models, overall this was a wonderful course :smile:
