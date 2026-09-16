import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')
creds = Credentials.from_authorized_user_file('authorized_user.json')
service = build('sheets', 'v4', credentials=creds)
ss_id = '1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ'

meta = service.spreadsheets().get(spreadsheetId=ss_id).execute()
dang_off_sheet = None
for s in meta.get('sheets', []):
    if s['properties']['sheetId'] == 887739629:
        dang_off_sheet = s
        break

print("Sheet Properties:", dang_off_sheet['properties'])

res = service.spreadsheets().values().get(
    spreadsheetId=ss_id,
    range="'Đang off'!A1:ZZ100"
).execute()
vals = res.get('values', [])
print("Total rows:", len(vals))
for i, row in enumerate(vals):
    print(f"Row {i:02d} (len {len(row)}): {row}")
