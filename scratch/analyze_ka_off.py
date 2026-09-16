import sys
import pandas as pd
import unicodedata
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
sheet_id = '1PjzFqJO-wkQ8SNsPHD721_CbPr6c_ArZKuGGU6KqDZg'

creds = Credentials.from_authorized_user_file('authorized_user.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

def clean_text(s):
    if not s:
        return ""
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

# 1. Fetch co_cau
res = service.spreadsheets().values().get(spreadsheetId=sheet_id, range="'cơ cấu'!A1:Z1500").execute()
df_cc = to_df(res.get('values', []))

# 2. Fetch Đang OFF
res = service.spreadsheets().values().get(spreadsheetId=sheet_id, range="'Đang OFF'!A1:Z100").execute()
df_dang = to_df(res.get('values', []))
dang_off_ids = set(df_dang['ID phường/xã\n(MÀU ĐỎ LÀ ĐANG OFF)'].astype(str).str.strip().tolist())
print(f"Đang OFF IDs: {dang_off_ids}")

# 3. Fetch KA off
res = service.spreadsheets().values().get(spreadsheetId=sheet_id, range="'KA off'!A1:Z100").execute()
df_ka = to_df(res.get('values', []))

# Custom mapping dictionary for known codes
special_map = {
    'nghĩa phú': '630102',
    'nghĩa tân': '630103',
}

results = []
for idx, r in df_ka.iterrows():
    # KA off columns:
    # 0: Vùng, 1: Tỉnh, 2: Huyện, 3: Xã, 4: BC, 5: HRBP, 6: Kết quả, 7: % Cap, 8: Tg tắt, 9: Tg mở
    vung = r.iloc[0]
    tinh = r.iloc[1]
    huyen = r.iloc[2]
    xa = r.iloc[3]
    bc_ka = r.iloc[4]
    hrbp = r.iloc[5]
    ket_qua = r.iloc[6]
    cap_down = r.iloc[7]
    tg_tat = r.iloc[8]
    tg_mo = r.iloc[9]
    
    c_tinh = clean_text(tinh)
    c_huyen = clean_text(huyen)
    c_xa = clean_text(xa)
    
    ward_code = ''
    bc_new = ''
    am = ''
    
    if c_xa in special_map:
        ward_code = special_map[c_xa]
        # find in cc
        m = df_cc[df_cc['ward_code'] == ward_code]
        if not m.empty:
            bc_new = m.iloc[0]['Bưu Cục new']
            am = m.iloc[0]['AM']
    else:
        # match in cc
        matches = []
        for _, cr in df_cc.iterrows():
            if not cr['ward_code']:
                continue
            if c_xa == clean_text(cr['Phường/Xã']):
                cc_tinh = clean_text(cr['c'])
                if c_tinh in cc_tinh or cc_tinh in c_tinh:
                    matches.append(cr)
        if len(matches) == 1:
            ward_code = matches[0]['ward_code']
            bc_new = matches[0]['Bưu Cục new']
            am = matches[0]['AM']
        elif len(matches) > 1:
            # refine by huyen
            h_matches = [m for m in matches if c_huyen == clean_text(m['Huyện/TP'])]
            if len(h_matches) >= 1:
                ward_code = h_matches[0]['ward_code']
                bc_new = h_matches[0]['Bưu Cục new']
                am = h_matches[0]['AM']
                
    # Also find AM from 'map' tab if co_cau has empty AM
    results.append({
        'row_idx': idx + 2,
        'tinh': tinh,
        'huyen': huyen,
        'xa': xa,
        'ward_code': ward_code,
        'bc_ka': bc_ka,
        'bc_new': bc_new,
        'tg_tat': tg_tat,
        'tg_mo': tg_mo,
        'in_dang_off': ward_code in dang_off_ids
    })

df_res = pd.DataFrame(results)
print("\n--- ALL KA OFF ROWS MAPPED ---")
print(df_res.to_string())

# Unique by ward_code
df_unique = df_res.drop_duplicates(subset=['ward_code']).copy()
print(f"\nTotal rows in KA off: {len(df_res)}")
print(f"Total unique ward_codes in KA off: {len(df_unique)}")
print("\n--- UNIQUE ROUTES IN KA OFF ---")
print(df_unique[['ward_code', 'tinh', 'huyen', 'xa', 'bc_ka', 'tg_tat', 'tg_mo', 'in_dang_off']].to_string())
