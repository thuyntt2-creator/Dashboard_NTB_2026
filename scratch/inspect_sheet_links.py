import os
import sys
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"c:\Users\lap4all\Desktop\New folder"
cred_file = os.path.join(BASE_DIR, 'authorized_user.json')
creds = Credentials.from_authorized_user_file(cred_file, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
service = build('sheets', 'v4', credentials=creds)

LINK_1_ID = '1j6Xm7JRemUGRSfbL-wc8DMwt7qfR7j79w9q79_snVnU'
LINK_2_ID = '1hdJ_QhdiY4dhkW2JXBd5eHGH6r5ULqNao69nBDYWsoY'

print("=== LINK 1 (Operations, Truy thu, etc.) ===")
res1 = service.spreadsheets().get(spreadsheetId=LINK_1_ID).execute()
for s in res1.get('sheets', []):
    p = s['properties']
    print(f"  ID: {p['sheetId']} - Title: {p['title']}")

print("\n=== LINK 2 (Business, Kinh Doanh, F30) ===")
res2 = service.spreadsheets().get(spreadsheetId=LINK_2_ID).execute()
for s in res2.get('sheets', []):
    p = s['properties']
    print(f"  ID: {p['sheetId']} - Title: {p['title']}")
