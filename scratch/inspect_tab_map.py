import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')
creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=creds)

res = service.spreadsheets().values().get(
    spreadsheetId='1PjzFqJO-wkQ8SNsPHD721_CbPr6c_ArZKuGGU6KqDZg',
    range="'map'!A1:Z200"
).execute()

rows = res.get('values', [])
print(f"Total rows in 'map': {len(rows)}")
df_map = pd.DataFrame(rows[1:], columns=rows[0])
print(df_map.to_string())
