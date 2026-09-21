import json
import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')
sheet_id = '1j6Xm7JRemUGRSfbL-wc8DMwt7qfR7j79w9q79_snVnU'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

creds = Credentials.from_authorized_user_file('authorized_user.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

print("--- SHEET 1: 1. Xu hướng 2 Tuần ---")
res1 = service.spreadsheets().values().get(spreadsheetId=sheet_id, range="'1. Xu hướng 2 Tuần'!A1:H20").execute()
for r in res1.get('values', []):
    print(r)

print("\n--- SHEET 2: 2. AM So Sánh 2 Tuần ---")
res2 = service.spreadsheets().values().get(spreadsheetId=sheet_id, range="'2. AM So Sánh 2 Tuần'!A1:H25").execute()
for r in res2.get('values', []):
    print(r)

print("\n--- SHEET 3: 3. Chi tiết BC 2 Tuần --- (first 5 rows and total count)")
res3 = service.spreadsheets().values().get(spreadsheetId=sheet_id, range="'3. Chi tiết BC 2 Tuần'!A1:I1000").execute()
rows3 = res3.get('values', [])
print(f"Total rows in Sheet 3: {len(rows3)}")
for r in rows3[:6]:
    print(r)

print("\n--- SHEET 4: 4. Hướng xử lý AM ---")
res4 = service.spreadsheets().values().get(spreadsheetId=sheet_id, range="'4. Hướng xử lý AM'!A1:H20").execute()
for r in res4.get('values', []):
    print(r)

