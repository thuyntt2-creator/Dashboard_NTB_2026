import os, sys
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

df_ops = pd.read_csv("scratch/sheet_sl_10kg_raw.csv")
df_tao = pd.read_csv("scratch/sheet_tren10kg_raw.csv")

print("=== DF OPS (SL > 10kg) ===")
print("Columns:", df_ops.columns.tolist())
print("Dates in Time:\n", df_ops['Time'].value_counts())
print("\nUnique Loại Hàng:\n", df_ops['Loại Hàng'].value_counts() if 'Loại Hàng' in df_ops else "N/A")
print("\nUnique Loại Khối Lượng:\n", df_ops['Loại Khối Lượng'].value_counts() if 'Loại Khối Lượng' in df_ops else "N/A")

print("\n=== DF TAO (treen10kg) ===")
print("Columns:", df_tao.columns.tolist())
print("Dates in ngay_tao_don:\n", df_tao['ngay_tao_don'].value_counts())
print("\nUnique nhom_kh:\n", df_tao['nhom_kh'].value_counts() if 'nhom_kh' in df_tao else "N/A")
print("\nUnique nhom_kl:\n", df_tao['nhom_kl'].value_counts() if 'nhom_kl' in df_tao else "N/A")

# Let's see daily volume per PO in df_ops vs df_tao
print("\n--- Summary by Date in df_ops ---")
df_ops['vol_num'] = pd.to_numeric(df_ops['Volume'], errors='coerce').fillna(0)
print(df_ops.groupby('Time')['vol_num'].agg(['sum', 'count', 'mean', 'max']))

print("\n--- Summary by Date in df_tao ---")
df_tao['vol_num'] = pd.to_numeric(df_tao['so_don'], errors='coerce').fillna(0)
print(df_tao.groupby('ngay_tao_don')['vol_num'].agg(['sum', 'count', 'mean', 'max']))

