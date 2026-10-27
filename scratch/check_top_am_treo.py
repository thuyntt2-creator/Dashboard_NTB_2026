import sys
import os
import json
import pandas as pd
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=creds)

SID_LC = '1MjLW8NbD5ZjoOdd90myGv0i1NGAtlvScxebfAXMM1j8'
res_lc = service.spreadsheets().values().get(spreadsheetId=SID_LC, range="'stuck'!A:J").execute()
rows_lc = res_lc.get('values', [])
df_lc = pd.DataFrame(rows_lc[1:], columns=rows_lc[0])
df_lc['am_clean'] = df_lc['am_name'].astype(str).str.strip().str.replace('Hồng Bích Nga', 'Hồng Bích Nga').str.replace('Nguyễn Thanh Long', 'Nguyễn Thanh Long')

col_time = 'Thời gian tồn đọng'

am_summary = []
for am, g in df_lc.groupby('am_clean'):
    vc = g[col_time].value_counts().to_dict()
    u24 = vc.get('0_6', 0) + vc.get('6_12', 0) + vc.get('12_24', 0)
    h24 = vc.get('24_36', 0)
    h36 = vc.get('36_48', 0) + vc.get('48_72', 0)
    h72 = vc.get('72_96', 0) + vc.get('96_120', 0)
    h120 = vc.get('120_192', 0) + vc.get('192', 0)
    treo24 = h24 + h36 + h72 + h120
    vol = len(g)
    tinh = g['province_name'].mode()[0] if len(g['province_name']) > 0 else ''
    am_summary.append({
        'am': am,
        'tinh': tinh,
        'vol': vol,
        'u24': u24,
        'h24': h24,
        'h36': h36,
        'h72': h72,
        'h120': h120,
        'treo24': treo24,
        'rate_treo': round(treo24 / vol * 100, 1) if vol else 0
    })

am_summary.sort(key=lambda x: x['treo24'], reverse=True)
print("TOP 10 AM TREO LC >= 24H NGÀY 27/10:")
for i, r in enumerate(am_summary[:10], 1):
    print(f"{i}. {r['am']} ({r['tinh']}): Treo {r['treo24']} đ / Tổng {r['vol']} đ ({r['rate_treo']}%) | 24-36h: {r['h24']}, 36-72h: {r['h36']}, 72-120h: {r['h72']}, >120h: {r['h120']}")
