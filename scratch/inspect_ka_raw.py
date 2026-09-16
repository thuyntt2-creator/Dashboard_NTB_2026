import sys
import pandas as pd
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
sheet_id = '1PjzFqJO-wkQ8SNsPHD721_CbPr6c_ArZKuGGU6KqDZg'

creds = Credentials.from_authorized_user_file('authorized_user.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

res = service.spreadsheets().values().get(spreadsheetId=sheet_id, range="'KA off'!A1:Z50").execute()
rows = res.get('values', [])
print("KA OFF RAW ROWS:")
for i, r in enumerate(rows):
    print(f"Row {i+1} (len {len(r)}): {r}")

