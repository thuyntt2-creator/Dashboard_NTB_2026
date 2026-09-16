import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = Credentials.from_authorized_user_file('authorized_user.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

sheet_id_source = '1PIyzade3_ml9Zq8OwTD5WGrc-paZJId7DfB06qSWJpg'
sheet_id_target = '1PjzFqJO-wkQ8SNsPHD721_CbPr6c_ArZKuGGU6KqDZg'

print("=== 1. CHECKING ROW 4062 IN SOURCE SHEET ===")
res = service.spreadsheets().get(
    spreadsheetId=sheet_id_source,
    ranges=["'Vùng đề xuất'!A4062:AB4062"],
    fields="sheets(data(rowData(values(userEnteredValue,effectiveValue,formattedValue))))"
).execute()

vals = res['sheets'][0]['data'][0]['rowData'][0]['values']
for idx, v in enumerate(vals):
    print(f"Col {idx+1}: uv={v.get('userEnteredValue')} | eff={v.get('effectiveValue')} | fmt='{v.get('formattedValue')}'")

print("\n=== 2. SEARCH ALL 420106 IN SOURCE SHEET ===")
res_all = service.spreadsheets().values().get(
    spreadsheetId=sheet_id_source,
    range="'Vùng đề xuất'!A:AB"
).execute()
rows = res_all.get('values', [])
for i, r in enumerate(rows):
    if len(r) > 6 and r[6] == '420106':
        print(f"Row {i+1}: Col3='{r[2] if len(r)>2 else ''}', Col6='{r[5] if len(r)>5 else ''}', Col7='{r[6]}', Col23='{r[22] if len(r)>22 else ''}', Col25='{r[24] if len(r)>24 else ''}', Col26='{r[25] if len(r)>25 else ''}'")

print("\n=== 3. CHECK TAB DRAFT CURRENT CONTENT ===")
res_draft = service.spreadsheets().values().get(
    spreadsheetId=sheet_id_target,
    range="'DRAFT'!A1:K30"
).execute()
for i, r in enumerate(res_draft.get('values', [])):
    print(f"DRAFT Row {i+1}: {r}")
