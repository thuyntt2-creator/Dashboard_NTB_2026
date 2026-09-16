import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=creds)

sheet_id_source = '1PIyzade3_ml9Zq8OwTD5WGrc-paZJId7DfB06qSWJpg'
sheet_id_target = '1PjzFqJO-wkQ8SNsPHD721_CbPr6c_ArZKuGGU6KqDZg'

print("=== 1. Checking Z4062 before update ===")
res = service.spreadsheets().get(
    spreadsheetId=sheet_id_source,
    ranges=["'Vùng đề xuất'!Z4062:Z4062"],
    fields="sheets(data(rowData(values(userEnteredValue,effectiveValue,formattedValue))))"
).execute()
print("Before:", res['sheets'][0]['data'][0]['rowData'][0]['values'][0])

print("\n=== 2. Updating Z4062 with date 01/10/2026 ===")
try:
    up_res = service.spreadsheets().values().update(
        spreadsheetId=sheet_id_source,
        range="'Vùng đề xuất'!Z4062",
        valueInputOption='USER_ENTERED',
        body={'values': [['01/10/2026']]}
    ).execute()
    print("Update result:", up_res)
except Exception as e:
    print("Update error:", e)

print("\n=== 3. Checking Z4062 after update ===")
res_after = service.spreadsheets().get(
    spreadsheetId=sheet_id_source,
    ranges=["'Vùng đề xuất'!Z4062:Z4062"],
    fields="sheets(data(rowData(values(userEnteredValue,effectiveValue,formattedValue))))"
).execute()
print("After:", res_after['sheets'][0]['data'][0]['rowData'][0]['values'][0])

print("\n=== 4. Checking if Phường 3 jumped to DRAFT ===")
res_draft = service.spreadsheets().values().get(
    spreadsheetId=sheet_id_target,
    range="'DRAFT'!A1:K30"
).execute()
found = False
for i, r in enumerate(res_draft.get('values', [])):
    if '420106' in r or 'Phường 3' in r:
        print(f"🎉 FOUND IN DRAFT Row {i+1}: {r}")
        found = True
if not found:
    print("Still not found in DRAFT. All DRAFT rows:")
    for i, r in enumerate(res_draft.get('values', [])):
        print(f"  Row {i+1}: {r}")
