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

# Print columns S to AA (index 18 to 26)
print("Summary 2 (Tỉnh W24 stats) in Phân tích AM-Tỉnh:")
for i, r in enumerate(data[:15]):
    print(f"Row {i:02d}: {r[18:27]}")
