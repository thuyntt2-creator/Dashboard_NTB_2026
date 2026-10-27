import sys
import os
import json
import pandas as pd
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=creds)

SID_AGING = '1WCzgao34cA_SttyB9ytHfE1qKTNl_3iFqDbEfw3lbyU'
SID_LC = '1MjLW8NbD5ZjoOdd90myGv0i1NGAtlvScxebfAXMM1j8'

# 1. Check Aging
print("=== AGING SHEET ===")
res_ag = service.spreadsheets().values().get(spreadsheetId=SID_AGING, range="'Đơn giao aging trên 5 ngày'!A:N").execute()
rows_ag = res_ag.get('values', [])
print(f"Total rows in Aging: {len(rows_ag)}")
if rows_ag:
    headers_ag = rows_ag[0]
    print(f"Headers: {headers_ag}")
    df_ag = pd.DataFrame(rows_ag[1:], columns=headers_ag)
    print(df_ag.head(3))
    if 'thoi_diem_chay_bao_cao' in df_ag.columns:
        print("Sample thoi_diem_chay_bao_cao:", df_ag['thoi_diem_chay_bao_cao'].dropna().unique()[:5])
    print("Aging value counts / summary:")
    print(df_ag['tinh'].value_counts())

# 2. Check Treo LC
print("\n=== TREO LC SHEET ===")
res_lc = service.spreadsheets().values().get(spreadsheetId=SID_LC, range="'stuck'!A:J").execute()
rows_lc = res_lc.get('values', [])
print(f"Total rows in Treo LC: {len(rows_lc)}")
if rows_lc:
    headers_lc = rows_lc[0]
    print(f"Headers: {headers_lc}")
    df_lc = pd.DataFrame(rows_lc[1:], columns=headers_lc)
    print(df_lc.head(3))
    col_time = next((c for c in df_lc.columns if 'thời gian' in c.lower() or 'thoi gian' in c.lower()), None)
    if col_time:
        print(f"Distribution of {col_time}:")
        print(df_lc[col_time].value_counts())
    print("Distribution of province_name:")
    print(df_lc['province_name'].value_counts())
