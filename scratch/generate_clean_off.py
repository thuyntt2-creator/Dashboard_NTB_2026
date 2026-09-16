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

# 1. Cơ cấu
res = service.spreadsheets().values().get(spreadsheetId=sheet_id, range="'cơ cấu'!A1:Z1500").execute()
df_cc = to_df(res.get('values', []))

# 2. Đang OFF
res = service.spreadsheets().values().get(spreadsheetId=sheet_id, range="'Đang OFF'!A1:Z100").execute()
df_dang = to_df(res.get('values', []))
dang_off_map = {}
for _, r in df_dang.iterrows():
    w = str(r.get('ID phường/xã\n(MÀU ĐỎ LÀ ĐANG OFF)', '')).strip()
    if w:
        dang_off_map[w] = r

# 3. KA off
res = service.spreadsheets().values().get(spreadsheetId=sheet_id, range="'KA off'!A1:Z100").execute()
df_ka = to_df(res.get('values', []))

special_map = {
    'nghĩa phú': '630102',
    'nghĩa tân': '630103',
}

# Process unique routes from KA off
seen_wards = set()
clean_rows = []

for idx, r in df_ka.iterrows():
    tinh = r.iloc[1].strip()
    huyen = r.iloc[2].strip()
    xa = r.iloc[3].strip()
    bc_ka = r.iloc[4].strip()
    tg_tat = r.iloc[8].strip()
    tg_mo = r.iloc[9].strip()

    c_tinh = clean_text(tinh)
    c_huyen = clean_text(huyen)
    c_xa = clean_text(xa)

    ward_code = ''
    bc_new = ''
    am = ''

    if c_xa in special_map:
        ward_code = special_map[c_xa]
        m = df_cc[df_cc['ward_code'] == ward_code]
        if not m.empty:
            bc_new = m.iloc[0]['Bưu Cục new']
            am = m.iloc[0]['AM']
            huyen = m.iloc[0]['Huyện/TP']
            tinh = m.iloc[0]['c']
            xa = m.iloc[0]['Phường/Xã']
    else:
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
            huyen = matches[0]['Huyện/TP']
            tinh = matches[0]['c']
            xa = matches[0]['Phường/Xã']
        elif len(matches) > 1:
            h_matches = [m for m in matches if c_huyen == clean_text(m['Huyện/TP'])]
            if len(h_matches) >= 1:
                ward_code = h_matches[0]['ward_code']
                bc_new = h_matches[0]['Bưu Cục new']
                am = h_matches[0]['AM']
                huyen = h_matches[0]['Huyện/TP']
                tinh = h_matches[0]['c']
                xa = h_matches[0]['Phường/Xã']

    if not ward_code:
        print(f"WARNING: Could not map row {idx+2}: {tinh} | {huyen} | {xa}")
        continue

    if ward_code in seen_wards:
        continue
    seen_wards.add(ward_code)

    # Use standard BC if mapped, else fallback
    final_bc = bc_new if bc_new else bc_ka

    # If AM is blank, look up from 'map' tab
    if not am:
        if '(LDO)' in final_bc:
            if 'Đơn Dương' in final_bc:
                am = 'Lê Văn Trường'
            elif 'Đức Trọng' in final_bc:
                am = 'Nguyễn Minh Hoàng'
        elif '(DNO)' in final_bc:
            if 'Gia Nghĩa' in final_bc:
                am = 'Huỳnh Thúc Duân'
            elif 'Quảng Tín' in final_bc or 'Kiến Đức' in final_bc:
                am = 'Huỳnh Thúc Duân'
            elif 'Quảng Sơn' in final_bc:
                am = 'Huỳnh Thúc Duân'

    # Check relation with Đang OFF
    in_dang_off = ward_code in dang_off_map
    if in_dang_off:
        phan_loai = "Đã có trong sheet 'Đang OFF' (Vùng RQ)"
    else:
        if tg_tat == '16/09/2026':
            phan_loai = "SPE đề xuất MỚI (Tắt từ 16/09)"
        else:
            phan_loai = "SPE đề xuất THÊM (Chưa có trong Đang OFF)"

    clean_rows.append({
        'Tỉnh': tinh,
        'Quận/ huyện': huyen,
        'Phường/xã cần tắt': xa,
        'ID phường/xã': ward_code,
        'Bưu Cục': final_bc,
        'AM': am,
        'Kết quả (KA) update': 'DUYỆT',
        'Thời gian tắt (KA)': tg_tat,
        'Thời gian mở (KA)': tg_mo,
        'Phân loại đề xuất': phan_loai
    })

df_clean = pd.DataFrame(clean_rows)
print(f"Processed {len(df_clean)} unique routes:")
print(df_clean.to_string())

# Save to local csv
df_clean.to_csv("scratch/tong_hop_ka_off.csv", index=False, encoding='utf-8-sig')
print("Saved to scratch/tong_hop_ka_off.csv")
