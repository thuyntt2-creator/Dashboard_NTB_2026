import sys
import pandas as pd
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = Credentials.from_authorized_user_file('authorized_user.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

res = service.spreadsheets().values().get(spreadsheetId='1PjzFqJO-wkQ8SNsPHD721_CbPr6c_ArZKuGGU6KqDZg', range="'cơ cấu'!A1:Z1500").execute()
rows = res.get('values', [])
max_c = max(len(r) for r in rows)
padded = [r + [''] * (max_c - len(r)) for r in rows]
df = pd.DataFrame(padded[1:], columns=padded[0])

matches = df[df['Phường/Xã'].str.contains('Nghĩa Phú|Nghĩa Tân', na=False, case=False)]
for idx, r in matches.iterrows():
    print(r.to_dict())
