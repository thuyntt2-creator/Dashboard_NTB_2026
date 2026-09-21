import sys, json
sys.stdout.reconfigure(encoding='utf-8')
from google.oauth2.credentials import Credentials
import gspread

creds = Credentials.from_authorized_user_file('authorized_user.json')
gc = gspread.authorize(creds)
sh = gc.open_by_key('1rfoi8QaZSZNiYf8IyKNN4QLrjAVxCCGrX9Yli0D8T84')
ws = sh.worksheet('Bao cao Tuan')
values = ws.get_all_values()

print(f"Bao cao Tuan has {len(values)} rows")
for r_idx in range(min(45, len(values))):
    row = values[r_idx]
    if any(cell.strip() for cell in row):
        print(f"Row {r_idx+1:2d}: {row[:12]}")
