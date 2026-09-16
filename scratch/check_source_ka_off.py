import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')
creds = Credentials.from_authorized_user_file('authorized_user.json')
service = build('sheets', 'v4', credentials=creds)

ss_follow = '1PjzFqJO-wkQ8SNsPHD721_CbPr6c_ArZKuGGU6KqDZg'
res = service.spreadsheets().values().get(spreadsheetId=ss_follow, range="'Tổng Hợp KA OFF'!A1:Z50").execute()
vals = res.get('values', [])
print("Source Tab: 'Tổng Hợp KA OFF'")
print("Rows count:", len(vals))
if vals:
    print("Header:", vals[0])
    for r in vals[1:6]:
        print("Row:", r)
