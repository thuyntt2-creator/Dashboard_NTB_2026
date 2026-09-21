import pandas as pd
import json
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

for fn in ['sheet_cocau.csv', 'co_cau_ntb.csv']:
    if os.path.exists(fn):
        print(f"Found {fn}")
        df = pd.read_csv(fn)
        print(df.head(2))

with open('data.json', encoding='utf-8') as f:
    d = json.load(f)

print("data.json keys:", list(d.keys())[:15])
if 'cocau' in d:
    print("cocau in d:", len(d['cocau']))
