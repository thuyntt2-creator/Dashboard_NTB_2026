import sys
import pandas as pd
from datetime import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = Credentials.from_authorized_user_file('authorized_user.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

sheet_id_source = '1PIyzade3_ml9Zq8OwTD5WGrc-paZJId7DfB06qSWJpg'

res = service.spreadsheets().values().get(
    spreadsheetId=sheet_id_source,
    range="'Vùng đề xuất'!A1:AB100"
).execute()

rows = res.get('values', [])
headers = rows[0]
print("Headers count:", len(headers))
for i, h in enumerate(headers):
    print(f"Col {i+1}: {h}")

print("\n=== SEARCHING FOR 420106 OR 'Phường 3' OR 'Đà Lạt' ===")
for r_idx, r in enumerate(rows[1:], start=2):
    r_str = " | ".join(r)
    if '420106' in r_str or 'Phường 3' in r_str or 'Đà Lạt' in r_str:
        print(f"\nRow {r_idx}:")
        for i, val in enumerate(r):
            h_name = headers[i] if i < len(headers) else f"Col {i+1}"
            print(f"  Col {i+1} ({h_name}): {val}")

print("\n=== ALL ROWS IN 'Vùng đề xuất' WITH Col 3 = NTB ===")
for r_idx, r in enumerate(rows[1:], start=2):
    col3 = r[2] if len(r) > 2 else ''
    if col3 == 'NTB':
        col4 = r[3] if len(r) > 3 else ''
        col5 = r[4] if len(r) > 4 else ''
        col6 = r[5] if len(r) > 5 else ''
        col7 = r[6] if len(r) > 6 else ''
        col26 = r[25] if len(r) > 25 else ''
        print(f"Row {r_idx}: Col3='{col3}', Col4='{col4}', Col5='{col5}', Col6='{col6}', Col7='{col7}', Col26='{col26}'")
