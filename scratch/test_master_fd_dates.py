import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import pandas as pd
from datetime import datetime, timedelta

creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=creds)

source_sheet_id = "1odUPX5mWpUYUUQOrhX_k8kXWV7drMUdQ58DRwgSQNS8"

# Let's inspect the dates available in Master FD
res = service.spreadsheets().values().get(
    spreadsheetId=source_sheet_id,
    range="'FD'!A1:G50"
).execute()

rows = res.get('values', [])
print("Master FD first 10 rows:")
for r in rows[:10]:
    print(r)

# Let's check how many total rows in Master FD and what delivery_dates exist
res_dates = service.spreadsheets().values().get(
    spreadsheetId=source_sheet_id,
    range="'FD'!A1:B1000"
).execute()
dates_data = res_dates.get('values', [])
df_dates = pd.DataFrame(dates_data[1:], columns=['delivery_date', 'region'])
print("\nUnique regions:", df_dates['region'].unique() if 'region' in df_dates else "None")
print("Unique dates in first 1000:", df_dates['delivery_date'].unique() if 'delivery_date' in df_dates else "None")
