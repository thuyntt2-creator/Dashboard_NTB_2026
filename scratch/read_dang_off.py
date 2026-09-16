import sys
import pandas as pd
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

creds = Credentials.from_authorized_user_file('authorized_user.json')
service = build('sheets', 'v4', credentials=creds)
ss_id = '1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ'

res = service.spreadsheets().values().get(spreadsheetId=ss_id, range="'Đang off'!A1:Z200").execute()
values = res.get('values', [])
print(f"Total rows fetched: {len(values)}")
if values:
    for idx, row in enumerate(values[:15]):
        print(f"Row {idx}: {row}")
    if len(values) > 15:
        print("...")
        for idx, row in enumerate(values[-5:], start=len(values)-5):
            print(f"Row {idx}: {row}")
