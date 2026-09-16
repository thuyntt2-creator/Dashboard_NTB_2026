import sys
import pandas as pd
from datetime import datetime
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
    res = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=f"'{title}'!A1:Z200").execute()
    vals = res.get('values', [])
    for r_idx, row in enumerate(vals):
        for c_idx, cell in enumerate(row):
            text = str(cell).strip()
            # check if looks like date
            if '/' in text or '-' in text:
                for fmt in ['%d/%m/%Y', '%d-%m-%Y', '%m/%d/%Y', '%Y-%m-%d', '%d/%m/%y']:
                    try:
                        d = datetime.strptime(text, fmt)
                        if 2025 <= d.year <= 2027:
                            if d.date() < datetime(2026, 9, 16).date():
                                print(f"Sheet '{title}' R{r_idx+1}C{c_idx+1}: {text} -> {d.strftime('%Y-%m-%d')} (< today)")
                        break
                    except:
                        pass
