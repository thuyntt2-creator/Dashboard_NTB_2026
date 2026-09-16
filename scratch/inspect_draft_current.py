import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = Credentials.from_authorized_user_file('authorized_user.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

sheet_id_target = '1PjzFqJO-wkQ8SNsPHD721_CbPr6c_ArZKuGGU6KqDZg'

res = service.spreadsheets().values().get(
    spreadsheetId=sheet_id_target,
    range="'DRAFT'!A1:K20"
).execute()

rows = res.get('values', [])
for i, r in enumerate(rows):
    print(f"DRAFT Row {i+1}: {r}")
