import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = Credentials.from_authorized_user_file('authorized_user.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

sheet_id_source = '1PIyzade3_ml9Zq8OwTD5WGrc-paZJId7DfB06qSWJpg'

res = service.spreadsheets().values().get(
    spreadsheetId=sheet_id_source,
    range="'Vùng đề xuất'!A:AB"
).execute()

rows = res.get('values', [])
for i, r in enumerate(rows):
    if len(r) > 6 and r[6] == '420116':
        print(f"Found 420116 at Row {i+1}: {r}")
