import sys
import pandas as pd
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
sheet_id = '1PjzFqJO-wkQ8SNsPHD721_CbPr6c_ArZKuGGU6KqDZg'

creds = Credentials.from_authorized_user_file('authorized_user.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

meta = service.spreadsheets().get(spreadsheetId=sheet_id).execute()
for s in meta.get('sheets', []):
    title = s['properties']['title']
    res = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=f"'{title}'!A1:Z50").execute()
    vals = res.get('values', [])
    print(f"\nTAB: {title} (rows: {len(vals)})")
    if vals:
        print("Header:", vals[0])
        if len(vals) > 1:
            print("Row 1:", vals[1])
