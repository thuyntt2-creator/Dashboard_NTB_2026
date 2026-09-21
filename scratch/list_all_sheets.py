import json
import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')
sheet_id = '1j6Xm7JRemUGRSfbL-wc8DMwt7qfR7j79w9q79_snVnU'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

try:
    creds = Credentials.from_authorized_user_file('authorized_user.json', SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    meta = service.spreadsheets().get(spreadsheetId=sheet_id).execute()
    print('Title:', meta.get('properties', {}).get('title'))
    sheets = meta.get('sheets', [])
    print(f'Total sheets: {len(sheets)}')
    for idx, s in enumerate(sheets):
        p = s.get('properties', {})
        print(f"[{idx+1}] ID: {p.get('sheetId')} | Title: '{p.get('title')}'")
except Exception as e:
    print('Error:', e)
