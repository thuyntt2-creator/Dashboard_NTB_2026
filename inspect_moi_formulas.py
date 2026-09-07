import gspread
from google.oauth2.service_account import Credentials
import sys

sys.stdout.reconfigure(encoding='utf-8')

JSON_FILE = r'C:\Users\lap4all\Desktop\Backlog_Automation\credentials.json'
SHEET_ID = '1sTJEt8meKwVicbJAa8d7ml48yVoa_yD2_LAEbZ1ebGs'

creds = Credentials.from_service_account_file(
    JSON_FILE, 
    scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
)
gc = gspread.authorize(creds)
sh = gc.open_by_key(SHEET_ID)

ws = sh.worksheet('data mới')
# Get Q2:R10 cell formulas
formulas = ws.get_values('P1:R10', value_render_option='FORMULA')
for r_idx, row in enumerate(formulas):
    print(f"Row {r_idx+1}: {row}")
