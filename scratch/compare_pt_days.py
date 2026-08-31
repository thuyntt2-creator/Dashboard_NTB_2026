import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_csv("vols_tao_don.csv")
df.columns = [str(c).strip() for c in df.columns]
df['Date'] = pd.to_datetime(df['Date'])

df_pt = df[df['Bưu cục'] == '(BTH) Phú Thủy'].copy()

# Date: 2026-07-08 vs 2026-07-01
df_08 = df_pt[df_pt['Date'] == '2026-07-08']
df_01 = df_pt[df_pt['Date'] == '2026-07-01']

print("=== 2026-07-08 ===")
print("Number of rows:", len(df_08))
print("Volume sum:", df_08['Volume'].sum())
print("By bat_on category:")
print(df_08.groupby('bat_on')['Volume'].sum())

print("\n=== 2026-07-01 ===")
print("Number of rows:", len(df_01))
print("Volume sum:", df_01['Volume'].sum())
print("By bat_on category:")
print(df_01.groupby('bat_on')['Volume'].sum())
