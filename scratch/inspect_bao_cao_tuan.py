import sys, json
sys.stdout.reconfigure(encoding='utf-8')
from google.oauth2.credentials import Credentials
import gspread
import pandas as pd

creds = Credentials.from_authorized_user_file('authorized_user.json')
gc = gspread.authorize(creds)
sh = gc.open_by_key('1rfoi8QaZSZNiYf8IyKNN4QLrjAVxCCGrX9Yli0D8T84')

ws = sh.worksheet('Bao cao Tuan')
data = ws.get_all_values()
print(f"=== Bao cao Tuan (rows: {len(data)}) ===")
for i in range(min(45, len(data))):
    row_str = [str(x) for x in data[i] if str(x).strip() != '']
    if row_str:
        print(f"R{i+1}: {row_str[:12]}")

print("\n=== Tuan 35 ===")
ws35 = sh.worksheet('Tuan 35')
data35 = ws35.get_all_values()
print(f"rows: {len(data35)}")
for i in range(min(25, len(data35))):
    row_str = [str(x) for x in data35[i] if str(x).strip() != '']
    if row_str:
        print(f"R{i+1}: {row_str[:12]}")
