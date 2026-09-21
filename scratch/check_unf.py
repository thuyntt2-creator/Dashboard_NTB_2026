import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')
sheet_id = '1j6Xm7JRemUGRSfbL-wc8DMwt7qfR7j79w9q79_snVnU'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

creds = Credentials.from_authorized_user_file('authorized_user.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

res_unf = service.spreadsheets().values().get(
    spreadsheetId=sheet_id, 
    range="'truythu'!A6:Q15",
    valueRenderOption='UNFORMATTED_VALUE'
).execute()

for r in res_unf.get('values', []):
    print(r[0], '|', r[1], '|', r[8], '|', r[10], '| Số tiền ban đầu:', r[12], type(r[12]))
