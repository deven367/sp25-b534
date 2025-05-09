import pandas as pd
import glob
import os

# Define patterns for epoch and step files
epoch_files = glob.glob("benchmarks_*_epochs.csv")
step_files = glob.glob("benchmarks_*_steps.csv")

def parse_filename(filename):
    # Extract batch_size, total_epochs, seq_len from filename
    basename = os.path.basename(filename)
    parts = basename.replace(".csv", "").split("_")
    return int(parts[1]), int(parts[2]), int(parts[3])  # batch_size, total_epochs, seq_len

def concat_files(file_list, output_filename):
    all_dfs = []
    for file in file_list:
        batch_size, total_epochs, seq_len = parse_filename(file)
        df = pd.read_csv(file)
        df["batch_size"] = batch_size
        df["total_epochs"] = total_epochs
        df["seq_len"] = seq_len
        all_dfs.append(df)

    master_df = pd.concat(all_dfs, ignore_index=True)
    master_df.to_csv(output_filename, index=False)
    print(f"Saved {output_filename} with {len(master_df)} rows.")

# Create master benchmark files
concat_files(epoch_files, "master_benchmark_epochs.csv")
concat_files(step_files, "master_benchmark_steps.csv")
