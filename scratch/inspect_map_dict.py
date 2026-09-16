import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')
creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=creds)

res_map = service.spreadsheets().values().get(
    spreadsheetId='1PjzFqJO-wkQ8SNsPHD721_CbPr6c_ArZKuGGU6KqDZg',
    range="'map'!A1:D200"
).execute()
rows_map = res_map.get('values', [])
df_map = pd.DataFrame(rows_map[1:], columns=rows_map[0])

map_dict = {}
for _, r in df_map.iterrows():
    bc = r['Bưu cục'].strip()
    am = r['AM'].strip()
    map_dict[bc] = am

print("Map dict has", len(map_dict), "bưu cục.")
for k, v in sorted(map_dict.items()):
    if any(x in k for x in ['(LDO)', '(DNO)']):
        print(f"  {k:<35} -> {v}")
