import gspread
from google.oauth2.service_account import Credentials
import sys
sys.stdout.reconfigure(encoding='utf-8')

JSON_FILE = r'C:\Users\lap4all\Desktop\Backlog_Automation\credentials.json'
SHEET_ID = '1LEmer5MUw2iC40NXOsFI4BHJ0WHLdkxn8FSKG7cZLsc'

creds = Credentials.from_service_account_file(
    JSON_FILE, 
    scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
)
gc = gspread.authorize(creds)
sh = gc.open_by_key(SHEET_ID)

ws = sh.worksheet('LTC')
data = ws.get_all_values()
print(f"{'Row':<4} | {'Col A (LTC Tổng)':<25} | {'Col L (LTC TTS)':<25}")
print("-" * 60)
for i, r in enumerate(data[3:23]):
    row_num = i + 4
    col_a = r[0] if len(r) > 0 else ""
    col_l = r[11] if len(r) > 11 else ""
    print(f"{row_num:<4} | {col_a:<25} | {col_l:<25}")
