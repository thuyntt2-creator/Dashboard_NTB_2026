import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')
sheet_id = '1j6Xm7JRemUGRSfbL-wc8DMwt7qfR7j79w9q79_snVnU'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

creds = Credentials.from_authorized_user_file('authorized_user.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

print('Fetching column A of truythu...')
res = service.spreadsheets().values().get(spreadsheetId=sheet_id, range="'truythu'!A:A").execute()
rows = res.get('values', [])
print('Actual rows in column A:', len(rows))
if rows:
    print('First 5:', rows[:5])
    print('Last 5:', rows[-5:])
