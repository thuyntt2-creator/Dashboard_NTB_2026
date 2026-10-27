import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')
sheet_id = '1j6Xm7JRemUGRSfbL-wc8DMwt7qfR7j79w9q79_snVnU'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

creds = Credentials.from_authorized_user_file('authorized_user.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

res1 = service.spreadsheets().values().get(spreadsheetId=sheet_id, range="'1. Xu hướng 2 Tuần'!A1:G15").execute()
rows1 = res1.get('values', [])
print("--- 1. Xu hướng 2 Tuần ---")
for r in rows1:
    print(r)

res2 = service.spreadsheets().values().get(spreadsheetId=sheet_id, range="'2. AM So Sánh 2 Tuần'!A1:G10").execute()
rows2 = res2.get('values', [])
print("\n--- 2. AM So Sánh 2 Tuần ---")
for r in rows2:
    print(r)
