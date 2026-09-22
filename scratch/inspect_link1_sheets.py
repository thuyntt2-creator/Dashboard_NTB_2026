import sys, json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = Credentials.from_authorized_user_file('authorized_user.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

link1_id = '1j6Xm7JRemUGRSfbL-wc8DMwt7qfR7j79w9q79_snVnU'
sheets_to_check = [
    'tongquan', 'FD', 'data rớt LC', 'truythu', 'aging', 'stuck',
    'dataGTC full hàng', 'dataODR full hàng ', 'dataLTC full hàng', 'data OPR TTS'
]

for sname in sheets_to_check:
    try:
        res = service.spreadsheets().values().get(spreadsheetId=link1_id, range=f"'{sname}'!A1:H5").execute()
        rows = res.get('values', [])
        print(f"=== LINK 1 SHEET: {sname} ===")
        for r in rows:
            print(r)
        print()
    except Exception as e:
        print(f"Error checking {sname}: {e}")
