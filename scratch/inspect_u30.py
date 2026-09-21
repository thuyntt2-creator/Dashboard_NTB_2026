import sys, json
sys.stdout.reconfigure(encoding='utf-8')
from google.oauth2.credentials import Credentials
import gspread

creds = Credentials.from_authorized_user_file('authorized_user.json')
gc = gspread.authorize(creds)
sh = gc.open_by_key('1rfoi8QaZSZNiYf8IyKNN4QLrjAVxCCGrX9Yli0D8T84')
ws_u30 = sh.worksheet('Duoi 30% (giai trinh)')
vals = ws_u30.get_all_values()
print(f"Duoi 30% has {len(vals)} rows")
for r in vals[:10]:
    print(r[:8])
