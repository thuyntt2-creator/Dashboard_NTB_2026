import pandas as pd
import io
import urllib.request
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ss_id = '1DAwY-46twFrHIs77R4p4IMuIZ6JTE-e58Aj-9Kcr5Jk'
url = f'https://docs.google.com/spreadsheets/d/{ss_id}/gviz/tq?tqx=out:csv&sheet=Data'

df = pd.read_csv(url)
print("=== SHEET DATA ANALYSIS ===")
print(f"Total Rows: {len(df)}")
print("Columns:", list(df.columns))

print("\n--- Unique values in 'Loại Hàng' ---")
print(df['Loại Hàng'].value_counts(dropna=False))

print("\n--- Unique values in 'Cấp Quản Lý' ---")
print(df['Cấp Quản Lý'].value_counts(dropna=False).head(10))

print("\n--- First 10 rows of 'Data' ---")
print(df[['Cấp Quản Lý', 'Chi tiết', 'Loại Hàng', 'Time', 'Volume', '% Gán', '% GTC']].head(10))
