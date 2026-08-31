import pandas as pd
import io
import urllib.request
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ss_id = '1DAwY-46twFrHIs77R4p4IMuIZ6JTE-e58Aj-9Kcr5Jk'
url = f"https://docs.google.com/spreadsheets/d/{ss_id}/export?format=csv&gid=910119805"

df = pd.read_csv(url)
print("=== SHEET 'raw' DATA SUMMARY ===")
print("Columns:", list(df.columns))
print(df.groupby('Loại Hàng')['Volume'].describe())
