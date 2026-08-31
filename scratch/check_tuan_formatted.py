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

# Read formatted data
print("Reading Theo Tuần formatted...")
ws_week = ss.worksheet("Theo Tuần")
data_fmt = ws_week.get_all_values()
df_fmt = pd.DataFrame(data_fmt[1:], columns=data_fmt[0])

print("Unique values of Tuan (formatted):")
print(df_fmt['Tuan'].unique())

# Let's see some rows where they were numeric in the unformatted data
# e.g. row index 27 (which is index 28 in sheet, 26 in python dataframe)
print("\nRow 27 formatted:")
print(df_fmt.iloc[26])
print("\nRow 40 formatted:")
print(df_fmt.iloc[39])
