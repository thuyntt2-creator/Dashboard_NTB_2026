import sys, requests, io
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_csv("scratch/raw_tren10kg.csv", header=None)

# Section A:U
df_ops_10kg = df.iloc[:, 0:21].copy()
df_ops_10kg.columns = [str(c).strip() for c in df_ops_10kg.iloc[0]]
df_ops_10kg = df_ops_10kg.iloc[1:].dropna(how='all')

print("--- Section A:U (Vận Hành >10kg) ---")
print(f"Row count: {len(df_ops_10kg)}")
print("Columns:", list(df_ops_10kg.columns))
print("Unique dates in Time:", df_ops_10kg['Time'].dropna().unique()[:5])
print("Unique Loai Hang:", df_ops_10kg['Loại Hàng'].dropna().unique())
print("Unique Tinh:", df_ops_10kg['Tỉnh'].dropna().unique())

# Section W:AD
df_tao_10kg = df.iloc[:, 22:30].copy()
df_tao_10kg.columns = [str(c).strip() for c in df_tao_10kg.iloc[0]]
df_tao_10kg = df_tao_10kg.iloc[1:].dropna(how='all')

print("\n--- Section W:AD (Tạo Đơn >10kg) ---")
print(f"Row count: {len(df_tao_10kg)}")
print("Columns:", list(df_tao_10kg.columns))
print("Unique dates in hen_lay:", df_tao_10kg['hen_lay'].dropna().unique()[:5])
print("Unique nhom_kg:", df_tao_10kg['nhom_kg'].dropna().unique())
print("Unique nhom_kh:", df_tao_10kg['nhom_kh'].dropna().unique()[:5])
print("Sample rows W:AD:")
print(df_tao_10kg.head(5))
