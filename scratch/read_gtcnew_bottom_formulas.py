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

print("gtcnew rows 25 to 50:")
for i in range(24, min(50, len(data))):
    r = data[i]
    # Filter empty elements at the end
    while r and r[-1] == "":
        r = r[:-1]
    print(f"Row {i+1:02d}: {r[:15]}")
