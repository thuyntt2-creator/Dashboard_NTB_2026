import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = Credentials.from_authorized_user_file('authorized_user.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

sheet_id_target = '1PjzFqJO-wkQ8SNsPHD721_CbPr6c_ArZKuGGU6KqDZg'
sheet_id_source = '1PIyzade3_ml9Zq8OwTD5WGrc-paZJId7DfB06qSWJpg'

meta_src = service.spreadsheets().get(spreadsheetId=sheet_id_source).execute()
print("Source Locale:", meta_src.get('properties', {}).get('locale'))

meta_tgt = service.spreadsheets().get(spreadsheetId=sheet_id_target).execute()
print("Target Locale:", meta_tgt.get('properties', {}).get('locale'))

# Check cell effectiveValue for Row 4062 Col 26
res = service.spreadsheets().get(
    spreadsheetId=sheet_id_source,
    ranges=["'Vùng đề xuất'!Y4062:Z4062"],
    fields="sheets(data(rowData(values(userEnteredValue,effectiveValue,formattedValue))))"
).execute()

cells = res['sheets'][0]['data'][0]['rowData'][0]['values']
print("Row 4062 Col 25 (Thời gian tắt):", cells[0])
print("Row 4062 Col 26 (Thời gian mở):", cells[1])
