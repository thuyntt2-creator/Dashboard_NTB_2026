import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import pandas as pd

creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=creds)

source_sheet_id = "1odUPX5mWpUYUUQOrhX_k8kXWV7drMUdQ58DRwgSQNS8"

meta = service.spreadsheets().get(spreadsheetId=source_sheet_id).execute()
for s in meta['sheets']:
    p = s['properties']
    if p['title'] == 'FD':
        print(f"FD sheet rowCount: {p.get('gridProperties', {}).get('rowCount')}")

# Let's inspect the last 500 rows
rowCount = 120000
for s in meta['sheets']:
    if s['properties']['title'] == 'FD':
        rowCount = s['properties']['gridProperties']['rowCount']

print(f"Total rowCount in FD: {rowCount}")
# Let's get rows from rowCount-500 to rowCount
res_end = service.spreadsheets().values().get(
    spreadsheetId=source_sheet_id,
    range=f"'FD'!A{max(1, rowCount-500)}:G{rowCount}"
).execute()
rows_end = res_end.get('values', [])
print(f"Rows at end: {len(rows_end)}")
if rows_end:
    for r in rows_end[-10:]:
        print(r)
