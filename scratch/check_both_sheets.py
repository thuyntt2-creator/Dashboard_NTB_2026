import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')
creds = Credentials.from_authorized_user_file('authorized_user.json')
service = build('sheets', 'v4', credentials=creds)

sids = [
    ('1PjzFqJO-wkQ8SNsPHD721_CbPr6c_ArZKuGGU6KqDZg', 'Previous Sheet'),
    ('1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ', 'User Sheet (Dash Board)')
]

for sid, label in sids:
    meta = service.spreadsheets().get(spreadsheetId=sid).execute()
    print(f"\n=== {label} ({sid}) ===")
    print("Title:", meta.get('properties', {}).get('title'))
    for s in meta.get('sheets', []):
        props = s.get('properties', {})
        print(f"  - {props.get('title')} (gid: {props.get('sheetId')})")
