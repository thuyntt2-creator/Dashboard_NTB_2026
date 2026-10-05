import os
import sys
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"c:\Users\lap4all\Desktop\New folder"
cred_file = os.path.join(BASE_DIR, 'authorized_user.json')
creds = Credentials.from_authorized_user_file(cred_file, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
service = build('sheets', 'v4', credentials=creds)

LINK_1_ID = '1j6Xm7JRemUGRSfbL-wc8DMwt7qfR7j79w9q79_snVnU'
LINK_2_ID = '1hdJ_QhdiY4dhkW2JXBd5eHGH6r5ULqNao69nBDYWsoY'

# 1. Check truythu from Link 1
print("=== PULLING TRUY THU FROM LINK 1 ===")
res_tt = service.spreadsheets().values().get(spreadsheetId=LINK_1_ID, range="'truythu'!A1:Q5").execute()
rows_tt = res_tt.get('values', [])
print("Truy thu header:", rows_tt[0] if rows_tt else "Empty")
# Pull last 5 rows of truythu
res_tt_last = service.spreadsheets().values().get(spreadsheetId=LINK_1_ID, range="'truythu'!A4100:Q4200").execute()
rows_last = res_tt_last.get('values', [])
print(f"Truy thu last rows count: {len(rows_last)}")
if rows_last:
    print("Truy thu sample last row:", rows_last[-1])

# 2. Check tong_quan from Link 2 (Kinh doanh)
print("\n=== PULLING TONG_QUAN FROM LINK 2 ===")
res_kd = service.spreadsheets().values().get(spreadsheetId=LINK_2_ID, range="'tong_quan'!A1:Z5").execute()
rows_kd = res_kd.get('values', [])
print("Kinh doanh header:", rows_kd[0] if rows_kd else "Empty")
if len(rows_kd) > 1:
    print("Kinh doanh sample row:", rows_kd[1])
