import sys
import pandas as pd
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
sheet_id = '1PjzFqJO-wkQ8SNsPHD721_CbPr6c_ArZKuGGU6KqDZg'

creds = Credentials.from_authorized_user_file('authorized_user.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

def inspect_tab(tab_name, max_rows=10):
    print(f"\n================ TAB: {tab_name} ================")
    res = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=f"'{tab_name}'!A1:Z100").execute()
    values = res.get('values', [])
    if not values:
        print("Empty sheet")
        return
    print(f"Total rows fetched: {len(values)}")
    for i, row in enumerate(values[:max_rows]):
        print(f"Row {i+1}: {row}")

for tab in ['Đang OFF', 'KA off', 'cơ cấu', 'DRAFT', 'map']:
    inspect_tab(tab, 8)
