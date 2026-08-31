import os, sys
import pandas as pd
sys.path.insert(0, os.path.abspath('.'))
sys.stdout.reconfigure(encoding='utf-8')

import app

# 1. Read the newly downloaded raw sheets
df_sl = pd.read_csv("scratch/sheet_sl_10kg_raw.csv")
df_tren = pd.read_csv("scratch/sheet_tren10kg_raw.csv")

print(f"SL > 10kg shape: {df_sl.shape}")
print(f"tren10kg shape: {df_tren.shape}")

# 2. Save to ops_heavy_10kg.csv and ops_tao_don_10kg.csv
df_sl.to_csv("ops_heavy_10kg.csv", index=False, encoding='utf-8-sig')
df_tren.to_csv("ops_tao_don_10kg.csv", index=False, encoding='utf-8-sig')

# Save to DB as well
app.save_df_to_db(df_sl, "ops_heavy_10kg.csv")
app.save_df_to_db(df_tren, "ops_tao_don_10kg.csv")

print("Successfully updated root CSV files and DB.")
