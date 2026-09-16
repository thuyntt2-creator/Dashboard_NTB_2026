import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

creds = Credentials.from_authorized_user_file('authorized_user.json')
service = build('sheets', 'v4', credentials=creds)
ss_id = '1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ'
sheet_meta = service.spreadsheets().get(spreadsheetId=ss_id).execute()
print('Title:', sheet_meta.get('properties', {}).get('title'))
for s in sheet_meta.get('sheets', []):
    props = s.get('properties', {})
    print(f"Sheet: {props.get('title')} | sheetId (gid): {props.get('sheetId')}")
