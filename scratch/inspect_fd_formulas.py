import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import json

creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=creds)
title = 'FD '
res = service.spreadsheets().values().get(
    spreadsheetId='1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ',
    range=f"'{title}'!A1:Z60",
    valueRenderOption='FORMULA'
).execute()

with open('scratch/fd_formulas_out.json', 'w', encoding='utf-8') as f:
    json.dump(res.get('values', []), f, ensure_ascii=False, indent=2)

print("Saved formulas to scratch/fd_formulas_out.json")
