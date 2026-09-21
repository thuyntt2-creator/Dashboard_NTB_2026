import sys, json
sys.stdout.reconfigure(encoding='utf-8')
from google.oauth2.credentials import Credentials
import gspread

creds = Credentials.from_authorized_user_file('authorized_user.json')
gc = gspread.authorize(creds)
sh = gc.open_by_key('1rfoi8QaZSZNiYf8IyKNN4QLrjAVxCCGrX9Yli0D8T84')
ws = sh.worksheet('Bao cao Tuan')
all_vals = ws.get_all_values()

non_empty = [(i+1, r) for i, r in enumerate(all_vals) if any(c.strip() for c in r)]
print(f"Total non empty rows: {len(non_empty)}")
for line_no, r in non_empty[:35]:
    print(f"Line {line_no:3d}: {r[:8]}")
