import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = Credentials.from_authorized_user_file('authorized_user.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

sheet_id_target = '1PjzFqJO-wkQ8SNsPHD721_CbPr6c_ArZKuGGU6KqDZg'
sheet_id_source = '1PIyzade3_ml9Zq8OwTD5WGrc-paZJId7DfB06qSWJpg'

print("=== CHECKING FORMULAS IN TAB 'DRAFT' ===")
res = service.spreadsheets().get(
    spreadsheetId=sheet_id_target,
    ranges=["'DRAFT'!A1:Z50"],
    fields="sheets(data(rowData(values(userEnteredValue,effectiveValue))))"
).execute()

for r_idx, row in enumerate(res['sheets'][0]['data'][0].get('rowData', [])):
    row_vals = []
    for c in row.get('values', []):
        uv = c.get('userEnteredValue', {})
        if 'formulaValue' in uv:
            row_vals.append(uv['formulaValue'])
        elif 'stringValue' in uv:
            row_vals.append(uv['stringValue'])
        elif 'numberValue' in uv:
            row_vals.append(str(uv['numberValue']))
        else:
            row_vals.append('')
    if any(row_vals):
        print(f"Row {r_idx+1}: {row_vals}")

print("\n=== CHECKING SOURCE SPREADSHEET ===")
try:
    meta_src = service.spreadsheets().get(spreadsheetId=sheet_id_source).execute()
    print("Source Title:", meta_src.get('properties', {}).get('title'))
    for s in meta_src.get('sheets', []):
        p = s['properties']
        print(f"Tab: {p['title']} (id: {p['sheetId']})")
except Exception as e:
    print("Error checking source spreadsheet:", e)
