import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=creds)

mvd_id = "1qhtczBFg2iXx5cGtu64KwqbArMV3yYG3Mu8wIobtgfg"
try:
    meta = service.spreadsheets().get(spreadsheetId=mvd_id).execute()
    print("MVD title:", meta.get('properties', {}).get('title'))
    for s in meta.get('sheets', []):
        print("  Sheet:", s.get('properties', {}).get('title'))
    res = service.spreadsheets().values().get(spreadsheetId=mvd_id, range="A1:M5").execute()
    for r in res.get('values', []):
        print(r)
except Exception as e:
    print("Error accessing MVD sheet:", e)
