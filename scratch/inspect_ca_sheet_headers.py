import urllib.request
import pandas as pd
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

url = 'https://docs.google.com/spreadsheets/d/1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ/export?format=csv&gid=260711009'
df_raw = pd.read_csv(url, header=None)

print("=== ROW 0 (GROUP HEADERS) ===")
for i, v in enumerate(df_raw.iloc[0]):
    if pd.notna(v):
        print(f"Col {i}: {v}")

print("\n=== ROW 1 (COLUMN NAMES) ===")
for i, v in enumerate(df_raw.iloc[1]):
    print(f"Col {i}: {v}")
