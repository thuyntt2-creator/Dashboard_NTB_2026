import pandas as pd
import os
import glob

csv_files = glob.glob("*.csv")
print("CSV files:", csv_files)

out_path = "scratch/analyze_csvs_out.txt"
with open(out_path, "w", encoding="utf-8") as f:
    f.write("=== ANALYSIS OF CSV FILES ===\n")
    for csv_file in csv_files:
        f.write(f"\n--- File: {csv_file} ---\n")
        try:
            df = pd.read_csv(csv_file, nrows=5)
            f.write(f"Shape: {pd.read_csv(csv_file).shape}\n")
            f.write(f"Columns: {df.columns.tolist()}\n")
            f.write(f"Head:\n{df.to_string()}\n")
        except Exception as e:
            f.write(f"Error reading: {e}\n")
            
print("Done inspecting CSVs!")
