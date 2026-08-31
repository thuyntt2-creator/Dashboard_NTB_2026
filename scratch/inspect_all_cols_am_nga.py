import urllib.request
import pandas as pd
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

url = 'https://docs.google.com/spreadsheets/d/1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ/export?format=csv&gid=260711009'
df = pd.read_csv(url, header=1)

bcs = ['(LDO) 1 Bảo Lộc', "(LDO) B'Lao", '(LDO) Bảo Lâm 1', '(LDO) Bảo Lâm 3']
sub = df[(df.iloc[:, 1].isin(bcs)) & (df.iloc[:, 3] == '2026-07-23 - Thứ 5')]

print("=== ALL COLUMNS AND VALUES FOR AM NGA (2026-07-23) ===")
for col_idx, col_name in enumerate(df.columns):
    print(f"\n--- Col {col_idx}: '{col_name}' ---")
    for row_idx, r in sub.iterrows():
        print(f"  Row {row_idx} ({r.iloc[1]}): {r.iloc[col_idx]}")
