import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=creds)

res = service.spreadsheets().get(
    spreadsheetId='1PIyzade3_ml9Zq8OwTD5WGrc-paZJId7DfB06qSWJpg',
    ranges=["'Vùng đề xuất'!Z4029:Z4030", "'Vùng đề xuất'!Z4062:Z4063"],
    fields="sheets(data(rowData(values(userEnteredFormat,effectiveFormat,userEnteredValue,effectiveValue,formattedValue))))"
).execute()

for s_idx, d in enumerate(res['sheets'][0]['data']):
    row = d['rowData'][0]['values'][0]
    print(f"\n--- Range {s_idx+1} ---")
    print("userEnteredValue:", row.get('userEnteredValue'))
    print("effectiveValue:", row.get('effectiveValue'))
    print("formattedValue:", row.get('formattedValue'))
    print("effectiveFormat numberFormat:", row.get('effectiveFormat', {}).get('numberFormat'))
