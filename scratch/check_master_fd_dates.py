import sys
sys.stdout.reconfigure(encoding='utf-8')
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import pandas as pd

creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=creds)

source_id = '1odUPX5mWpUYUUQOrhX_k8kXWV7drMUdQ58DRwgSQNS8'
res = service.spreadsheets().values().get(spreadsheetId=source_id, range="FD!A1:B100000").execute()
rows = res.get('values', [])
print(f"Total rows in FD: {len(rows)}")
if rows:
    df = pd.DataFrame(rows[1:], columns=rows[0])
    df_ntb = df[df['region_shortname'] == 'NTB']
    print(f"NTB rows: {len(df_ntb)}")
    print("NTB unique dates:", df_ntb['delivery_date'].dropna().unique())
