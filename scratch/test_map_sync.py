import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')
creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=creds)

sheet_id = '1PjzFqJO-wkQ8SNsPHD721_CbPr6c_ArZKuGGU6KqDZg'

# 1. Fetch map tab
res_map = service.spreadsheets().values().get(spreadsheetId=sheet_id, range="'map'!A1:D200").execute()
df_map = pd.DataFrame(res_map.get('values', [])[1:], columns=res_map.get('values', [])[0])
map_dict = {r['Bưu cục'].strip(): r['AM'].strip() for _, r in df_map.iterrows() if r.get('Bưu cục')}

# 2. Fetch KA OFF
res_ka = service.spreadsheets().values().get(spreadsheetId=sheet_id, range="'Tổng Hợp KA OFF'!A1:J30").execute()
df_ka = pd.DataFrame(res_ka.get('values', [])[1:], columns=res_ka.get('values', [])[0])

print("MAPPING CURRENT KA OFF BCs TO TAB 'map':")
for idx, r in df_ka.iterrows():
    bc = r['Bưu Cục']
    am_mapped = map_dict.get(bc, 'NOT FOUND')
    print(f"Row {idx+1}: {bc:<25} | Map AM: '{am_mapped}' | Current AM: '{r['AM']}'")
