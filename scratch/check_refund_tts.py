import sys
import os
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

import gspread
import pandas as pd
from google.oauth2.credentials import Credentials as UserCredentials

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = UserCredentials.from_authorized_user_file('authorized_user.json', scopes=SCOPES)
gc = gspread.authorize(creds)
sheet_id = '1ll3CaTcBj-tp8kcamMUftBLb9OriIoIHFhIyL3LYzvo'
sh = gc.open_by_key(sheet_id)

print(f"Spreadsheet Title: {sh.title}")
target_ws = None
for ws in sh.worksheets():
    print(f"Worksheet: '{ws.title}', id: {ws.id}, rows: {ws.row_count}, cols: {ws.col_count}")
    if str(ws.id) == '1038815137':
        target_ws = ws

if not target_ws:
    target_ws = sh.get_worksheet(0)

print(f"\n--- Checking Worksheet '{target_ws.title}' (id: {target_ws.id}) ---")
rows = target_ws.get_all_values()
print(f"Total rows: {len(rows)}")
for i, r in enumerate(rows[:10]):
    print(f"Row {i}: {r[:15]}")
