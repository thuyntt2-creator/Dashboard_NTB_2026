import sys
import pandas as pd
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = Credentials.from_authorized_user_file('authorized_user.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

sheet_id_source = '1PIyzade3_ml9Zq8OwTD5WGrc-paZJId7DfB06qSWJpg'

res = service.spreadsheets().get(
    spreadsheetId=sheet_id_source,
    ranges=["'Vùng đề xuất'!A4000:Z4138"],
    fields="sheets(data(rowData(values(userEnteredValue,effectiveValue,formattedValue))))"
).execute()

rows = res['sheets'][0]['data'][0].get('rowData', [])
print(f"Inspecting rows from 4000 to {4000+len(rows)}:")

for idx, r in enumerate(rows, start=4000):
    vals = r.get('values', [])
    if len(vals) > 2:
        col3 = vals[2].get('effectiveValue', {}).get('stringValue', '')
        if col3 == 'NTB':
            col4 = vals[3].get('effectiveValue', {}).get('stringValue', '') if len(vals) > 3 else ''
            col6 = vals[5].get('effectiveValue', {}).get('stringValue', '') if len(vals) > 5 else ''
            col7 = vals[6].get('effectiveValue', {}).get('stringValue', '') if len(vals) > 6 else ''
            col25 = vals[24].get('effectiveValue', {}) if len(vals) > 24 else {}
            col26 = vals[25].get('effectiveValue', {}) if len(vals) > 25 else {}
            fmt25 = vals[24].get('formattedValue', '') if len(vals) > 24 else ''
            fmt26 = vals[25].get('formattedValue', '') if len(vals) > 25 else ''
            print(f"Row {idx}: {col4} - {col6} ({col7}) | Col25: {col25} ({fmt25}) | Col26: {col26} ({fmt26})")
