import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
sheet_id = '1PjzFqJO-wkQ8SNsPHD721_CbPr6c_ArZKuGGU6KqDZg'

try:
    creds = Credentials.from_authorized_user_file('authorized_user.json', SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    meta = service.spreadsheets().get(spreadsheetId=sheet_id).execute()
    print('Spreadsheet Title:', meta.get('properties', {}).get('title'))
    for s in meta.get('sheets', []):
        p = s.get('properties', {})
        print(f"Sheet: {p.get('title')} | ID: {p.get('sheetId')}")
except Exception as e:
    print('Error:', e)
