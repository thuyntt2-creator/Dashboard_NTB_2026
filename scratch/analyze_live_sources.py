import sys
import os
import json
import pandas as pd
from datetime import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=creds)

SID_AGING = '1WCzgao34cA_SttyB9ytHfE1qKTNl_3iFqDbEfw3lbyU'
SID_LC = '1MjLW8NbD5ZjoOdd90myGv0i1NGAtlvScxebfAXMM1j8'

# 1. Aging
res_ag = service.spreadsheets().values().get(spreadsheetId=SID_AGING, range="'Đơn giao aging trên 5 ngày'!A:N").execute()
rows_ag = res_ag.get('values', [])
print(f"Aging rows: {len(rows_ag)}")
headers_ag = rows_ag[0]
df_ag = pd.DataFrame(rows_ag[1:], columns=headers_ag)

# Check run timestamp
run_time_ag = df_ag['thoi_diem_chay_bao_cao'].dropna().iloc[0] if 'thoi_diem_chay_bao_cao' in df_ag.columns and len(df_ag) > 0 else 'N/A'
print(f"Aging Run time: {run_time_ag}")

df_ag['days_num'] = pd.to_numeric(df_ag['Aging'], errors='coerce').fillna(5.0)
def classify_aging(days):
    if days > 15: return 'gt_15'
    elif days >= 8: return 'd_8_15'
    else: return 'd_5_8'

df_ag['bucket'] = df_ag['days_num'].apply(classify_aging)
print("Aging Buckets:")
print(df_ag['bucket'].value_counts())

# 2. Treo LC
res_lc = service.spreadsheets().values().get(spreadsheetId=SID_LC, range="'stuck'!A:J").execute()
rows_lc = res_lc.get('values', [])
print(f"\nTreo LC rows: {len(rows_lc)}")
headers_lc = rows_lc[0]
df_lc = pd.DataFrame(rows_lc[1:], columns=headers_lc)

col_time = next((c for c in df_lc.columns if 'thời gian' in c.lower() or 'thoi gian' in c.lower() or 'tồn' in c.lower() or 'ton' in c.lower()), 'Thời gian tồn đọng')
print(f"Treo LC time column: {col_time}")
vc_time = df_lc[col_time].value_counts().to_dict()
print(vc_time)

u24 = vc_time.get('0_6', 0) + vc_time.get('6_12', 0) + vc_time.get('12_24', 0)
h24 = vc_time.get('24_36', 0)
h36 = vc_time.get('36_48', 0) + vc_time.get('48_72', 0)
h72 = vc_time.get('72_96', 0) + vc_time.get('96_120', 0)
h120 = vc_time.get('120_192', 0) + vc_time.get('192', 0)
treo24 = h24 + h36 + h72 + h120
total_lc = len(df_lc)

print(f"Total LC: {total_lc:,}")
print(f"  < 24h: {u24:,} ({u24/total_lc*100:.1f}%)")
print(f"  24-36h: {h24:,} ({h24/total_lc*100:.1f}%)")
print(f"  36-72h: {h36:,} ({h36/total_lc*100:.1f}%)")
print(f"  72-120h: {h72:,} ({h72/total_lc*100:.1f}%)")
print(f"  >120h: {h120:,} ({h120/total_lc*100:.1f}%)")
print(f"  Treo >= 24h: {treo24:,} ({treo24/total_lc*100:.1f}%)")
