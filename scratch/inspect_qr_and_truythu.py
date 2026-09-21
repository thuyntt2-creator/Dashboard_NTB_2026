import json
import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')
sheet_id = '1j6Xm7JRemUGRSfbL-wc8DMwt7qfR7j79w9q79_snVnU'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

creds = Credentials.from_authorized_user_file('authorized_user.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

sheets_to_check = [
    '1. Xu hướng 2 Tuần',
    '2. AM So Sánh 2 Tuần',
    '3. Chi tiết BC 2 Tuần',
    '4. Hướng xử lý AM',
    'truythu'
]

for title in sheets_to_check:
    print(f"================ SHEET: {title} ================")
    res = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=f"'{title}'!A1:Z30").execute()
    rows = res.get('values', [])
    print(f"Total rows fetched: {len(rows)}")
    for i, r in enumerate(rows[:15]):
        print(f"Row {i+1}: {r}")
    print("\n")
