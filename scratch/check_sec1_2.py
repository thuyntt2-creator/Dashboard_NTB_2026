import sys
sys.stdout.reconfigure(encoding='utf-8')
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=creds)
work_id = '15Z-aMM6OFfiWUXd2Zwz6BFNq_Y0KWwHiVDqxkioHufM'

sheet_res = service.spreadsheets().get(
    spreadsheetId=work_id,
    ranges=["'Top 10 FD (T2-Gio)'!A38:J52"],
    includeGridData=True
).execute()

data = sheet_res['sheets'][0]['data'][0].get('rowData', [])
for r_idx, r in enumerate(data):
    vals = [c.get('formattedValue', '') for c in r.get('values', [])]
    print(f"Row {r_idx+38}: {vals}")
