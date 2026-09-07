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

def get_df(name):
    ws = sh.worksheet(name)
    data = ws.get_all_values()
    headers = data[0]
    # pad headers if data has more columns than headers
    max_cols = max(len(row) for row in data)
    if len(headers) < max_cols:
        headers += [f"Unnamed_{i}" for i in range(len(headers)+1, max_cols+1)]
    return pd.DataFrame(data[1:], columns=headers)

df_cu = get_df('data cũ')
df_moi = get_df('data mới')

print("data cũ columns:", list(df_cu.columns))
print("data mới columns:", list(df_moi.columns))

# Let's print unique values for columns beyond 15
print("\nUnique values in data cũ extra columns:")
for col in df_cu.columns[15:]:
    print(f"\nColumn: '{col}'")
    print(df_cu[col].value_counts().head(10))

print("\nUnique values in data mới extra columns:")
for col in df_moi.columns[15:]:
    print(f"\nColumn: '{col}'")
    print(df_moi[col].value_counts().head(10))
