import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

JSON_FILE = r'C:\Users\lap4all\Desktop\Backlog_Automation\credentials.json'
SHEET_ID = '1j6Xm7JRemUGRSfbL-wc8DMwt7qfR7j79w9q79_snVnU'

print("Connecting to Google Sheets...")
creds = Credentials.from_service_account_file(JSON_FILE, scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
gc = gspread.authorize(creds)
sh = gc.open_by_key(SHEET_ID)

sheets_to_check = [
    'dataGTC gốc full hàng',
    'dataLTC full hàng',
    'dataODRfull hàng ',
    'cocau'
]

for name in sheets_to_check:
    print(f"\n--- Checking worksheet: {name} ---")
    ws = sh.worksheet(name)
    data = ws.get_all_values(value_render_option='UNFORMATTED_VALUE')
    if len(data) > 0:
        headers = data[0]
        df = pd.DataFrame(data[1:], columns=headers)
        print(f"Shape: {df.shape}")
        print(f"Columns: {df.columns.tolist()}")
        print("First row values preview:")
        print(df.iloc[0].to_dict())
    else:
        print("Empty worksheet!")
