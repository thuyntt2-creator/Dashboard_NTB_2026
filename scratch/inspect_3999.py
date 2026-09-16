import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=creds)

res = service.spreadsheets().get(
    spreadsheetId='1PIyzade3_ml9Zq8OwTD5WGrc-paZJId7DfB06qSWJpg',
    ranges=["'Vùng đề xuất'!Y3999:Z3999"],
    fields="sheets(data(rowData(values(effectiveValue,formattedValue))))"
).execute()

print("Row 3999 values:", res['sheets'][0]['data'][0]['rowData'][0]['values'])
