import sys
sys.stdout.reconfigure(encoding='utf-8')
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import pandas as pd

creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=creds)

work_id = '15Z-aMM6OFfiWUXd2Zwz6BFNq_Y0KWwHiVDqxkioHufM'
res = service.spreadsheets().values().get(spreadsheetId=work_id, range="'RAW FD N-1 (HUB)'!A1:H").execute()
rows = res.get('values', [])
print(f"Total rows in RAW FD N-1 (HUB): {len(rows)}")
if rows:
    df = pd.DataFrame(rows[1:], columns=rows[0])
    print(df.head(3))
    print("Dates in RAW FD N-1 (HUB):", df['delivery_date'].dropna().unique())
