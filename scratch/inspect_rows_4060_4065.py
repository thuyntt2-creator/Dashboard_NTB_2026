import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = Credentials.from_authorized_user_file('authorized_user.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

sheet_id_source = '1PIyzade3_ml9Zq8OwTD5WGrc-paZJId7DfB06qSWJpg'

res = service.spreadsheets().get(
    spreadsheetId=sheet_id_source,
    ranges=["'Vùng đề xuất'!A4060:Z4065"],
    fields="sheets(data(rowData(values(userEnteredValue,effectiveValue,formattedValue))))"
).execute()

rows = res['sheets'][0]['data'][0].get('rowData', [])
for i, r in enumerate(rows, start=4060):
    vals = r.get('values', [])
    row_desc = []
    for c_idx in [3, 4, 5, 6, 8, 22, 24, 25]:
        v = vals[c_idx] if len(vals) > c_idx else {}
        row_desc.append(f"C{c_idx+1}:{v.get('formattedValue', '')} (eff: {v.get('effectiveValue')})")
    print(f"Row {i}: {' | '.join(row_desc)}")
