import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')
df = pd.read_csv('co_cau_ntb.csv')

print(f"{'STT':<4} | {'Họ Tên AM':<25} | {'Tỉnh Phụ Trách':<25} | {'Số BC':<6} | Danh Sách Bưu Cục")
print("-" * 120)

i = 1
for am, g in df.groupby('AM'):
    tinhs = ", ".join(sorted(g['Tỉnh'].unique()))
    bcs = ", ".join(g['Bưu cục'].tolist())
    print(f"{i:<4} | {am:<25} | {tinhs:<25} | {len(g):<6} | {bcs}")
    i += 1
