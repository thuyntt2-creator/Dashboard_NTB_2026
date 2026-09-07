import sys, json
sys.stdout.reconfigure(encoding='utf-8')
from google.oauth2.credentials import Credentials
import gspread
import pandas as pd

creds = Credentials.from_authorized_user_file('authorized_user.json')
gc = gspread.authorize(creds)
sh = gc.open_by_key('1rfoi8QaZSZNiYf8IyKNN4QLrjAVxCCGrX9Yli0D8T84')

for ws_name in ['DATA XỬ LÝ', 'DATA GỐC', 'Tong quan L3D']:
    ws = sh.worksheet(ws_name)
    rows = ws.get_all_values()
    print(f"=== {ws_name} (rows: {len(rows)}) ===")
    if len(rows) > 0:
        print("Header:", rows[0][:15])
        # Find unique dates in date column
        # Let's inspect rows 1 to 5
        for r in range(1, min(5, len(rows))):
            print(f"R{r}:", rows[r][:10])
