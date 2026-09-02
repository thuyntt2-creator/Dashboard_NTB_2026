import json
import sys
import os
import pandas as pd
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

SHEET_ID = "1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ"
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

try:
    creds = Credentials.from_authorized_user_file('authorized_user.json', SCOPES)
    service = build('sheets', 'v4', credentials=creds)

    meta = service.spreadsheets().get(spreadsheetId=SHEET_ID).execute()
    sheet_title = meta.get('properties', {}).get('title', '')
    print(f"Connected to '{sheet_title}'")
    
    sheets = meta.get('sheets', [])
    for s in sheets:
        p = s.get('properties', {})
        print(f"Sheet: {p.get('title')} (id: {p.get('sheetId')})")
        if str(p.get('sheetId')) == "626823626" or p.get('title') == "FD":
            title = p.get('title')
            res = service.spreadsheets().values().get(spreadsheetId=SHEET_ID, range=f"'{title}'!A1:ZZ100").execute()
            rows = res.get('values', [])
            print(f"\n--- Tab {title} ({len(rows)} rows) ---")
            for i, r in enumerate(rows[:40]):
                print(f"Row {i+1}: {r}")
                
            # save all rows to ops_fd_new.json / ops_fd.csv
            full_res = service.spreadsheets().values().get(spreadsheetId=SHEET_ID, range=f"'{title}'!A1:ZZ1000").execute()
            full_rows = full_res.get('values', [])
            with open('scratch/fd_rows_raw.json', 'w', encoding='utf-8') as f:
                json.dump(full_rows, f, ensure_ascii=False, indent=2)
            print(f"Saved {len(full_rows)} rows to scratch/fd_rows_raw.json")
except Exception as e:
    print(f"Error: {e}")
