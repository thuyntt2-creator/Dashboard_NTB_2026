import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

CREDENTIALS_PATH = r'C:\Users\lap4all\Desktop\Backlog_Automation\credentials.json'
SPREADSHEET_ID   = '12VsqpIx1vLOqk6-JKHwgRmdrgu6fxSNPQcpyO0wpvdQ'
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
ss = gspread.authorize(creds).open_by_key(SPREADSHEET_ID)

ws = ss.worksheet("Theo Tuần")

print("Fetching both versions...")
data_fmt = ws.get_all_values()
data_raw = ws.get_all_values(value_render_option='UNFORMATTED_VALUE')

df_fmt = pd.DataFrame(data_fmt[1:], columns=data_fmt[0])
df_raw = pd.DataFrame(data_raw[1:], columns=data_raw[0])

# Find rows where Tuan is numeric in df_raw
differences = []
for idx in range(len(df_raw)):
    val_raw = df_raw.iloc[idx]['Tuan']
    val_fmt = df_fmt.iloc[idx]['Tuan']
    if isinstance(val_raw, (int, float)):
        differences.append((idx, val_raw, val_fmt))

print(f"Total numeric Tuan rows: {len(differences)}")
print("Sample mappings (idx, raw/unformatted, formatted):")
for item in differences[:30]:
    print(f"Row {item[0]+2}: Raw={item[1]} -> Formatted={item[2]}")
