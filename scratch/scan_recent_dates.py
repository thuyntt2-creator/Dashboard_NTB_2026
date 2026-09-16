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
    ranges=["'Vùng đề xuất'!A4000:AB4070"],
    fields="sheets(data(rowData(values(userEnteredValue,effectiveValue,formattedValue))))"
).execute()

rows = res['sheets'][0]['data'][0].get('rowData', [])
for idx, r in enumerate(rows, start=4000):
    vals = r.get('values', [])
    for c_idx, v in enumerate(vals):
        fmt = v.get('formattedValue', '')
        eff = v.get('effectiveValue', {})
        if '01/10' in fmt or '1/10' in fmt or eff.get('numberValue') == 46296:
            col_letter = chr(65 + c_idx) if c_idx < 26 else f"A{chr(65 + c_idx - 26)}"
            print(f"Row {idx} Col {col_letter} ({c_idx+1}): fmt='{fmt}', eff={eff}")
