import sys
import pandas as pd
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
sheet_id = '1PjzFqJO-wkQ8SNsPHD721_CbPr6c_ArZKuGGU6KqDZg'

creds = Credentials.from_authorized_user_file('authorized_user.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

def to_df(rows):
    if not rows:
        return pd.DataFrame()
    max_c = max(len(r) for r in rows)
    padded = [r + [''] * (max_c - len(r)) for r in rows]
    return pd.DataFrame(padded[1:], columns=padded[0])

# Fetch all of co_cau
res = service.spreadsheets().values().get(spreadsheetId=sheet_id, range="'cơ cấu'!A1:Z1500").execute()
df_cocau = to_df(res.get('values', []))
print("Co cau columns:", df_cocau.columns.tolist())
print(f"Co cau total rows: {len(df_cocau)}")

# Fetch KA off
res = service.spreadsheets().values().get(spreadsheetId=sheet_id, range="'KA off'!A1:Z100").execute()
df_ka = to_df(res.get('values', []))
print("\nKA off columns:", df_ka.columns.tolist())
print(f"KA off total rows: {len(df_ka)}")

# Fetch Đang OFF
res = service.spreadsheets().values().get(spreadsheetId=sheet_id, range="'Đang OFF'!A1:Z100").execute()
df_dang_off = to_df(res.get('values', []))
print("\nĐang OFF columns:", df_dang_off.columns.tolist())
print(f"Đang OFF total rows: {len(df_dang_off)}")

print("\n--- Đang OFF rows ---")
print(df_dang_off)

print("\n--- KA off rows ---")
print(df_ka.to_string())
