import sys
import os
import pandas as pd
import unicodedata
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')
sheet_id = '1PjzFqJO-wkQ8SNsPHD721_CbPr6c_ArZKuGGU6KqDZg'
creds = Credentials.from_authorized_user_file('authorized_user.json')
service = build('sheets', 'v4', credentials=creds)

def clean_text(s):
    if not s:
        return ''
    s = unicodedata.normalize('NFC', str(s).strip().lower())
    for p in ['thị trấn ', 'thị xã ', 'thành phố ', 'quận ', 'huyện ', 'phường ', 'xã ']:
        if s.startswith(p):
            s = s[len(p):]
    s = s.replace("'", "").replace("’", "").replace("-", " ")
    return " ".join(s.split())

def to_df(rows):
    if not rows:
        return pd.DataFrame()
    max_c = max(len(r) for r in rows)
    padded = [r + [''] * (max_c - len(r)) for r in rows]
    return pd.DataFrame(padded[1:], columns=padded[0])

# 1. Map BC -> AM
res_map = service.spreadsheets().values().get(spreadsheetId=sheet_id, range="'map'!A1:D200").execute()
df_map = pd.DataFrame(res_map.get('values', [])[1:], columns=res_map.get('values', [])[0])
map_bc_am = {}
for _, mr in df_map.iterrows():
    bc = mr.get('Bưu cục', '').strip()
    am = mr.get('AM', '').strip()
    if bc and am:
        map_bc_am[bc] = am

# 2. Co cau
res_cc = service.spreadsheets().values().get(spreadsheetId=sheet_id, range="'cơ cấu'!A1:Z2000").execute()
df_cc = to_df(res_cc.get('values', []))

# 3. Đang OFF
res_dang = service.spreadsheets().values().get(spreadsheetId=sheet_id, range="'Đang OFF'!A1:L50").execute()
df_dang = to_df(res_dang.get('values', []))

# 4. KA off
res_ka = service.spreadsheets().values().get(spreadsheetId=sheet_id, range="'KA off'!A1:K100").execute()
df_ka = to_df(res_ka.get('values', []))

print(f"Đang OFF count: {len(df_dang)}")
print(f"KA off count: {len(df_ka)}")

# Check Tay Nha Trang in Đang OFF:
tnt = df_dang[df_dang['Bưu Cục\nVùng để trống cột bất kỳ từ cột B-> T\nNhập sai format\n=> KHÔNG REVIEW'] == '(KHO) Tây Nha Trang']
print(f"Tây Nha Trang in Đang OFF: {len(tnt)} rows")
for _, r in tnt.iterrows():
    print(r.tolist())
