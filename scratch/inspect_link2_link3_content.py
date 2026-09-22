import sys, json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = Credentials.from_authorized_user_file('authorized_user.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

# 1. Inspect Link 2 (Kinh doanh)
link2_id = '1hdJ_QhdiY4dhkW2JXBd5eHGH6r5ULqNao69nBDYWsoY'
print("=== LINK 2: TONG QUAN ===")
res = service.spreadsheets().values().get(spreadsheetId=link2_id, range='tong_quan!A1:G10').execute()
for r in res.get('values', []):
    print(r)

print("\n=== LINK 2: F30 ===")
res = service.spreadsheets().values().get(spreadsheetId=link2_id, range='f30!A1:G10').execute()
for r in res.get('values', []):
    print(r)

print("\n=== LINK 2: KH A ===")
res = service.spreadsheets().values().get(spreadsheetId=link2_id, range='KH A!A1:G10').execute()
for r in res.get('values', []):
    print(r)

# 2. Inspect Link 3 (Lấp đầy)
link3_id = '1rfoi8QaZSZNiYf8IyKNN4QLrjAVxCCGrX9Yli0D8T84'
print("\n=== LINK 3: BAO CAO TUAN ===")
res = service.spreadsheets().values().get(spreadsheetId=link3_id, range='Bao cao Tuan!A1:H15').execute()
for r in res.get('values', []):
    print(r)

print("\n=== LINK 3: DUOI 30% ===")
res = service.spreadsheets().values().get(spreadsheetId=link3_id, range='Duoi 30% (giai trinh)!A1:H10').execute()
for r in res.get('values', []):
    print(r)
