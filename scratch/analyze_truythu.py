import json
import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')
sheet_id = '1j6Xm7JRemUGRSfbL-wc8DMwt7qfR7j79w9q79_snVnU'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

creds = Credentials.from_authorized_user_file('authorized_user.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

res = service.spreadsheets().values().get(spreadsheetId=sheet_id, range="'truythu'!A1:Z5000").execute()
rows = res.get('values', [])
print(f"Total rows in truythu: {len(rows)}")
if rows:
    header = rows[0]
    print(f"Header: {header}")
    df = pd.DataFrame(rows[1:], columns=header)
    print("DataFrame shape:", df.shape)
    print("\nUnique values in 'Ngày kết luận truy thu':")
    if 'Ngày kết luận truy thu' in df.columns:
        print(df['Ngày kết luận truy thu'].value_counts())
    print("\nUnique values in 'Loại truy thu':")
    if 'Loại truy thu' in df.columns:
        print(df['Loại truy thu'].value_counts())
    print("\nSample rows:")
    print(df.head(5).to_dict(orient='records'))
