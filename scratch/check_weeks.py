import pandas as pd
import os

out_path = "scratch/check_weeks_out.txt"
with open(out_path, "w", encoding="utf-8") as f:
    for fname in ['ops_gtc.csv', 'ops_ltc.csv', 'ODR TTS.csv']:
        if os.path.exists(fname):
            df = pd.read_csv(fname, nrows=5)
            f.write(f"\n--- {fname} columns ---\n")
            f.write(str(df.columns.tolist()) + "\n")
            df_full = pd.read_csv(fname)
            week_cols = [c for c in df_full.columns if 'week' in c.lower() or 'tuan' in c.lower() or 'tuần' in c.lower()]
            f.write(f"Week columns: {week_cols}\n")
            if week_cols:
                for wc in week_cols:
                    f.write(f"{wc} unique values: {df_full[wc].dropna().unique().tolist()[:10]}\n")

print("Done writing check_weeks!")
