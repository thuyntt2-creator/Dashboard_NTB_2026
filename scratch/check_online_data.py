import os
import sys
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')
load_dotenv()

JSON_FILE = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS') or r'C:\Users\lap4all\Desktop\Backlog_Automation\credentials.json'
if not os.path.exists(JSON_FILE):
    JSON_FILE = 'credentials.json'

sheet_id = "12VsqpIx1vLOqk6-JKHwgRmdrgu6fxSNPQcpyO0wpvdQ"
creds = Credentials.from_service_account_file(
    JSON_FILE, 
    scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
)
gc = gspread.authorize(creds)
sh = gc.open_by_key(sheet_id)

ws = sh.worksheet('khách hàng mơi')

# Find the row for Mã KH 5099749
all_vals = ws.get_all_values()
for r_idx, row in enumerate(all_vals):
    if '5099749' in row:
        print(f"Row {r_idx+1} in 'khách hàng mơi': {row}")
        # Let's get the formatted value and formula for the Volume column (column I / 9)
        cell_val = ws.cell(r_idx+1, 9).value
        print(f"Volume cell value (raw): {cell_val}")
        break
