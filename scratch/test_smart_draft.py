import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=creds)

sheet_id_target = '1PjzFqJO-wkQ8SNsPHD721_CbPr6c_ArZKuGGU6KqDZg'

# Let's test what formula would work in DRAFT:
# Currently:
# raw_data, IFERROR(FILTER(data, INDEX(data,0,3)="NTB", INDEX(data,0,26)>TODAY()), "")
# If we allow either:
# INDEX(data,0,26)>TODAY() OR (INDEX(data,0,25)>=DATE(2026,9,1) * (INDEX(data,0,23)="DUYỆT"))
# or checking DATEVALUE / converting month 1 to month 10 if date was swapped

new_formula = """=LET(
  data, IMPORTRANGE("1PIyzade3_ml9Zq8OwTD5WGrc-paZJId7DfB06qSWJpg", "'Vùng đề xuất'!A2:AB"),
  headers, IMPORTRANGE("1PIyzade3_ml9Zq8OwTD5WGrc-paZJId7DfB06qSWJpg", "'Vùng đề xuất'!A1:AB1"),
  col26_fixed, BYROW(INDEX(data,0,26), LAMBDA(d, IF(d=DATE(2026,1,10), DATE(2026,10,1), d))),
  raw_data, IFERROR(FILTER(data, INDEX(data,0,3)="NTB", col26_fixed>TODAY()), ""),
  combined, IF(raw_data="", headers, {headers; SORTN(raw_data, 9^9, 2, 7, TRUE)}),
  QUERY(combined, "SELECT Col4, Col5, Col6, Col7, Col9, Col22, Col23, Col24, Col25, Col26", 1)
)"""

print("Updating DRAFT!A1 with smart formula...")
res = service.spreadsheets().values().update(
    spreadsheetId=sheet_id_target,
    range="'DRAFT'!A1",
    valueInputOption='USER_ENTERED',
    body={'values': [[new_formula]]}
).execute()

print("Result:", res)

# Check DRAFT rows now!
res_draft = service.spreadsheets().values().get(
    spreadsheetId=sheet_id_target,
    range="'DRAFT'!A1:K30"
).execute()
for i, r in enumerate(res_draft.get('values', [])):
    print(f"Row {i+1}: {r}")
