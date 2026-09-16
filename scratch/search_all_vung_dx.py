import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = Credentials.from_authorized_user_file('authorized_user.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

sheet_id_source = '1PIyzade3_ml9Zq8OwTD5WGrc-paZJId7DfB06qSWJpg'

res = service.spreadsheets().values().get(
    spreadsheetId=sheet_id_source,
    range="'Vùng đề xuất'!A:AB"
).execute()

rows = res.get('values', [])
print("Total rows in 'Vùng đề xuất':", len(rows))
headers = rows[0]

found_rows = []
for r_idx, r in enumerate(rows[1:], start=2):
    r_str = " ".join(r)
    if '420106' in r_str or ('Đà Lạt' in r_str and 'Phường 3' in r_str):
        found_rows.append((r_idx, r))

print(f"Found {len(found_rows)} matching rows:")
for r_idx, r in found_rows:
    print(f"\n--- Row {r_idx} ---")
    for c_idx, val in enumerate(r):
        h = headers[c_idx] if c_idx < len(headers) else f"Col {c_idx+1}"
        print(f"Col {c_idx+1} ({h}): '{val}'")
