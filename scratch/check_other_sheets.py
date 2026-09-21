import sys
sys.stdout.reconfigure(encoding='utf-8')
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import pandas as pd

creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=creds)
work_id = '15Z-aMM6OFfiWUXd2Zwz6BFNq_Y0KWwHiVDqxkioHufM'

for title in ['Raw FD_Tổng', 'RAW FD_COD', 'RAW FD_TTS', 'data']:
    try:
        res = service.spreadsheets().values().get(spreadsheetId=work_id, range=f"'{title}'!A1:B100").execute()
        rows = res.get('values', [])
        print(f"Sheet {title}: {len(rows)} sample rows, header = {rows[0] if rows else []}")
    except Exception as e:
        print(f"Error {title}: {e}")
