import sys
import os
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=creds)

sheets_to_check = {
    'sheet_1j6': '1j6Xm7JRemUGRSfbL-wc8DMwt7qfR7j79w9q79_snVnU',
    'sheet_aging_agents_md': '1WCzgao34cA_SttyB9ytHfE1qKTNl_3iFqDbEfw3lbyU',
    'sheet_lc_agents_md': '1MjLW8NbD5ZjoOdd90myGv0i1NGAtlvScxebfAXMM1j8'
}

for name, sid in sheets_to_check.items():
    try:
        meta = service.spreadsheets().get(spreadsheetId=sid).execute()
        title = meta.get('properties', {}).get('title', '')
        sheets = [s['properties']['title'] for s in meta.get('sheets', [])]
        print(f"=== {name} ({sid}) ===")
        print(f"Title: {title}")
        print(f"Tabs: {sheets}")
        
        # Check first 5 rows of first tab
        first_tab = sheets[0]
        res = service.spreadsheets().values().get(spreadsheetId=sid, range=f"'{first_tab}'!A1:Z5").execute()
        rows = res.get('values', [])
        print(f"First row (headers) in '{first_tab}': {rows[0] if rows else 'None'}")
        if len(rows) > 1:
            print(f"Sample row 1: {rows[1][:8]}")
        print("-" * 50)
    except Exception as e:
        print(f"=== {name} ERROR: {e} ===")
