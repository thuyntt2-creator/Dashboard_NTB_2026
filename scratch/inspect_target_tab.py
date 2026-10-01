import os
import sys
import json
import pandas as pd
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

sheet_id = '1JSbLo353RgRCTuGyyMmPH7jiB48tNIRMXR6KMze39jg'
target_gid = 1149501631

creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
service = build('sheets', 'v4', credentials=creds)
meta = service.spreadsheets().get(spreadsheetId=sheet_id).execute()
print('Spreadsheet Title:', meta.get('properties', {}).get('title'))

target_tab = None
for s in meta.get('sheets', []):
    props = s.get('properties', {})
    t = props.get('title')
    gid = props.get('sheetId')
    print(f"Tab: '{t}' | gid: {gid}")
    if gid == target_gid:
        target_tab = t

print('Target tab name:', target_tab)
if target_tab:
    res = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=target_tab).execute()
    values = res.get('values', [])
    print(f'Total rows in {target_tab}: {len(values)}')
    if values:
        max_cols = max(len(r) for r in values)
        padded = [r + [''] * (max_cols - len(r)) for r in values]
        df = pd.DataFrame(padded[1:], columns=padded[0])
        print("Columns:", list(df.columns))
        print("Shape:", df.shape)
        print("First 5 rows:")
        print(df.head(5).to_string())
        df.to_csv('scratch/target_orders_1149501631.csv', index=False, encoding='utf-8')
