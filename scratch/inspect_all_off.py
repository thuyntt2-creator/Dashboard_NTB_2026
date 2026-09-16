import sys
import pandas as pd
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
sheet_id = '1PjzFqJO-wkQ8SNsPHD721_CbPr6c_ArZKuGGU6KqDZg'

creds = Credentials.from_authorized_user_file('authorized_user.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

def fetch_all(tab_name):
    res = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=f"'{tab_name}'!A1:Z500").execute()
    values = res.get('values', [])
    return values

print("=== ĐANG OFF ALL ROWS ===")
dang_off = fetch_all('Đang OFF')
print(f"Total rows: {len(dang_off)}")
for i, r in enumerate(dang_off):
    print(f"{i+1}: {r}")

print("\n=== KA OFF ALL ROWS ===")
ka_off = fetch_all('KA off')
print(f"Total rows: {len(ka_off)}")
for i, r in enumerate(ka_off):
    print(f"{i+1}: {r}")

print("\n=== CO CAU SAMPLE ROWS ===")
co_cau = fetch_all('cơ cấu')
print(f"Total co_cau rows: {len(co_cau)}")
for i, r in enumerate(co_cau[:10]):
    print(f"{i+1}: {r}")
