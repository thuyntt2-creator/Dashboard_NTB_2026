import sys
import unicodedata
import pandas as pd
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

sheet_id = '1JSbLo353RgRCTuGyyMmPH7jiB48tNIRMXR6KMze39jg'
creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
service = build('sheets', 'v4', credentials=creds)

meta = service.spreadsheets().get(spreadsheetId=sheet_id).execute()
print('Spreadsheet Title:', meta.get('properties', {}).get('title'))
for s in meta.get('sheets', []):
    props = s.get('properties', {})
    print(f"Sheet: {props.get('title')} | gid: {props.get('sheetId')}")

res1 = service.spreadsheets().values().get(spreadsheetId=sheet_id, range='Sheet1').execute()
vals = res1.get('values', [])
print(f'Sheet1 total rows: {len(vals)}')
if vals:
    max_c = max(len(r) for r in vals)
    padded = [r + [''] * (max_c - len(r)) for r in vals]
    df = pd.DataFrame(padded[1:], columns=padded[0])
    print("Columns:", list(df.columns))
    print(df.head(10).to_string())
    df.to_csv('scratch/sheet1_current.csv', index=False, encoding='utf-8')
