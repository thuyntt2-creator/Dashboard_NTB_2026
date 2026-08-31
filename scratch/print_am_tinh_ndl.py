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

ws = sh.worksheet('Phân tích AM-Tỉnh')
data = ws.get_all_values()
headers = data[0]

# Find rows for Nguyễn Duy Long
print("Nguyễn Duy Long rows in Phân tích AM-Tỉnh:")
for i, r in enumerate(data[1:]):
    if r[0] == 'Nguyễn Duy Long':
        print(f"Row {i+2}:")
        for col_name, val in zip(headers[:11], r[:11]):
            print(f"  {col_name}: {val}")
