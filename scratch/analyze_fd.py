import pandas as pd
import os

path = "ops_fd.csv"
out_path = "scratch/analyze_fd_out.txt"

with open(out_path, "w", encoding="utf-8") as f:
    f.write("=== FD ANALYSIS ===\n")
    if os.path.exists(path):
        df = pd.read_csv(path)
        f.write(f"Columns: {df.columns.tolist()}\n")
        f.write("\n--- Header rows (first 15) ---\n")
        for idx, row in df.head(15).iterrows():
            f.write(f"Row {idx}: {row.tolist()}\n")
            
        f.write("\n--- High %FD post offices ---\n")
        df_clean = df.copy()
        df_clean.columns = df.iloc[1]
        df_clean = df_clean.iloc[2:].reset_index(drop=True)
        df_clean.columns = [str(c).strip() for c in df_clean.columns]
        f.write(f"Cleaned Columns: {df_clean.columns.tolist()}\n")
        f.write(df_clean.head(30).to_string() + "\n")
    else:
        f.write("ops_fd.csv not found\n")

print("Done writing FD analysis!")
