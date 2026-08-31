import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
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

ws = sh.worksheet('Phân tích AM W24 vs W23')
data = ws.get_all_values()
df = pd.DataFrame(data[1:], columns=data[0])

ndl_row = df[df.iloc[:, 0] == 'Nguyễn Duy Long']
print("Nguyễn Duy Long row details:")
for col in df.columns:
    print(f"  {col}: {ndl_row[col].values[0]}")
