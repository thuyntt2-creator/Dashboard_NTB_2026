import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
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

ws = sh.worksheet('nd cần báo cáo')
data = ws.get_all_values()

print(f"Total rows in 'nd cần báo cáo': {len(data)}")
for r_idx, row in enumerate(data):
    # check if row has any non-empty cell
    non_empty = [f"Col {c_idx+1}: {cell}" for c_idx, cell in enumerate(row) if cell.strip() != ""]
    if non_empty:
        print(f"Row {r_idx+1}: " + " | ".join(non_empty))
