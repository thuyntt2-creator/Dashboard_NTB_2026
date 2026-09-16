import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')
creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=creds)

sheets_to_check = [
    ('Current Sheet', '1PjzFqJO-wkQ8SNsPHD721_CbPr6c_ArZKuGGU6KqDZg'),
    ('De Xuat Sheet', '1PIyzade3_ml9Zq8OwTD5WGrc-paZJId7DfB06qSWJpg'),
]

for name, sid in sheets_to_check:
    print(f"\n=== {name} ({sid}) ===")
    meta = service.spreadsheets().get(spreadsheetId=sid).execute()
    for s in meta.get('sheets', []):
        p = s['properties']
        print(f"  Tab: {p['title']} (id: {p['sheetId']})")
