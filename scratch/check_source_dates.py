import sys
sys.stdout.reconfigure(encoding='utf-8')
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import pandas as pd

creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=creds)

work_id = '15Z-aMM6OFfiWUXd2Zwz6BFNq_Y0KWwHiVDqxkioHufM'
source_id = '1odUPX5mWpUYUUQOrhX_k8kXWV7drMUdQ58DRwgSQNS8'

# Check RAW FD N-1 (HUB)
res1 = service.spreadsheets().values().get(spreadsheetId=work_id, range="'RAW FD N-1 (HUB)'!A1:A").execute()
rows1 = [r[0] for r in res1.get('values', [])[1:] if r]
print("RAW FD N-1 (HUB) dates:", pd.Series(rows1).unique())

# Check Master FD
res2 = service.spreadsheets().values().get(spreadsheetId=source_id, range="FD!A1:B").execute()
rows2 = res2.get('values', [])
if rows2:
    df_src = pd.DataFrame(rows2[1:], columns=rows2[0])
    print("Master FD total rows:", len(df_src))
    df_ntb = df_src[df_src['region_shortname'] == 'NTB']
    print("Master FD NTB dates:", df_ntb['delivery_date'].dropna().unique())
