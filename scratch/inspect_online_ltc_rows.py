import urllib.request, io, sys
import pandas as pd
sys.stdout.reconfigure(encoding='utf-8')

url_ltc = 'https://docs.google.com/spreadsheets/d/1DAwY-46twFrHIs77R4p4IMuIZ6JTE-e58Aj-9Kcr5Jk/export?format=csv&gid=1365110988'
req = urllib.request.Request(url_ltc, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=30) as resp:
    content = resp.read()

df = pd.read_csv(io.BytesIO(content))
for i in range(min(5, len(df))):
    print(f"--- ROW {i} ---")
    for col in df.columns:
        print(f"  {col}: {df.iloc[i][col]}")
