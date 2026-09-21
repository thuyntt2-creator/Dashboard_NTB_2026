import sys, json
sys.stdout.reconfigure(encoding='utf-8')
from google.oauth2.credentials import Credentials
import gspread

creds = Credentials.from_authorized_user_file('authorized_user.json')
gc = gspread.authorize(creds)
sh = gc.open_by_key('1rfoi8QaZSZNiYf8IyKNN4QLrjAVxCCGrX9Yli0D8T84')
ws = sh.worksheet('Bao cao Tuan')
all_vals = ws.get_all_values()

print(f"Total rows in Bao cao Tuan: {len(all_vals)}")
for idx in range(min(50, len(all_vals))):
    r = all_vals[idx]
    if any(c.strip() for c in r):
        print(f"R{idx+1:3d}: {r[:10]}")
