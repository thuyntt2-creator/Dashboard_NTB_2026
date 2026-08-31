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

ws = sh.worksheet('gtcnew')
data = ws.get_all_values()

# Print Row 24 (index 23)
row_idx = 23
r = data[row_idx]
print(f"Row {row_idx+1}:")
for col_idx in range(len(r)):
    h0 = data[0][col_idx]
    h1 = data[1][col_idx]
    h2 = data[2][col_idx]
    print(f"  Col {col_idx+1} ({h0} | {h1} | {h2}): {r[col_idx]}")
