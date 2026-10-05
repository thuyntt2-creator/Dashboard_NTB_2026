import os
import sys
import pandas as pd
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"c:\Users\lap4all\Desktop\New folder"
cred_file = os.path.join(BASE_DIR, 'authorized_user.json')
creds = Credentials.from_authorized_user_file(cred_file, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
service = build('sheets', 'v4', credentials=creds)

LINK_1_ID = '1j6Xm7JRemUGRSfbL-wc8DMwt7qfR7j79w9q79_snVnU'
LINK_2_ID = '1hdJ_QhdiY4dhkW2JXBd5eHGH6r5ULqNao69nBDYWsoY'

# Check truythu
print("Fetching full 'truythu'...")
res_tt = service.spreadsheets().values().get(spreadsheetId=LINK_1_ID, range="'truythu'!A:Z").execute()
rows_tt = res_tt.get('values', [])
print(f"Total rows in 'truythu': {len(rows_tt)}")
if rows_tt:
    print("Header:", rows_tt[0])
    print("Row 1:", rows_tt[1] if len(rows_tt) > 1 else "None")
    print("Row last:", rows_tt[-1] if len(rows_tt) > 1 else "None")

# Check tong_quan
print("\nFetching full 'tong_quan' (Kinh Doanh)...")
res_kd = service.spreadsheets().values().get(spreadsheetId=LINK_2_ID, range="'tong_quan'!A:Z").execute()
rows_kd = res_kd.get('values', [])
print(f"Total rows in 'tong_quan': {len(rows_kd)}")
if rows_kd:
    header = rows_kd[0]
    print("Header:", header)
    df_kd = pd.DataFrame(rows_kd[1:], columns=header)
    print("Distinct dates in 'Ngay':", df_kd['Ngay'].dropna().unique()[-15:])
