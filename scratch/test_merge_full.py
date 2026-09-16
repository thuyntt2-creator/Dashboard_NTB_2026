import sys
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

# We will collect all rows keyed by ward_code
all_rows = {}

# Process Đang OFF first
col_bc_dang = 'Bưu Cục\nVùng để trống cột bất kỳ từ cột B-> T\nNhập sai format\n=> KHÔNG REVIEW'
col_id_dang = 'ID phường/xã\n(MÀU ĐỎ LÀ ĐANG OFF)'

for _, r in df_dang.iterrows():
    w_id = str(r[col_id_dang]).strip()
    if not w_id or not w_id.isdigit():
        continue
    tinh = r['Tỉnh'].strip()
    huyen = r['Quận/ huyện'].strip()
    xa = r['Phường/xã cần tắt'].strip()
    bc = r[col_bc_dang].strip()
    kq = r.get('Kết quả (KA) update', 'DUYỆT') or 'DUYỆT'
    tg_tat = r.get('Thời gian tắt (KA)', '').strip()
    tg_mo = r.get('Thời gian mở (KA)', '').strip()
    
    # AM
    am = map_bc_am.get(bc, '')
    if 'Đức Trọng' in bc or 'Di Linh' in bc:
        am = 'Nguyễn Lê Nguyên Vũ'
    elif not am and 'AM' in r and r['AM']:
        am = r['AM'].strip()
    
    all_rows[w_id] = {
        'Tỉnh': tinh,
        'Quận/ huyện': huyen,
        'Phường/xã cần tắt': xa,
        'ID phường/xã': w_id,
        'Bưu Cục': bc,
        'AM': am,
        'Kết quả (KA) update': kq,
        'Thời gian tắt (KA)': tg_tat,
        'Thời gian mở (KA)': tg_mo,
        'Phân loại đề xuất': "Đã có trong sheet 'Đang OFF' (Vùng RQ)"
    }

print(f"Loaded {len(all_rows)} routes from Đang OFF.")

# Process KA off (SPE de xuat)
special_map = {
    'nghĩa phú': '630102',
    'nghĩa tân': '630103',
}

for idx, r in df_ka.iterrows():
    tinh = r.iloc[1].strip() if len(r) > 1 else ''
    huyen = r.iloc[2].strip() if len(r) > 2 else ''
    xa = r.iloc[3].strip() if len(r) > 3 else ''
    bc_ka = r.iloc[4].strip() if len(r) > 4 else ''
    tg_tat = r.iloc[8].strip() if len(r) > 8 else ''
    tg_mo = r.iloc[9].strip() if len(r) > 9 else ''

    c_tinh = clean_text(tinh)
    c_huyen = clean_text(huyen)
    c_xa = clean_text(xa)

    ward_code = ''
    bc_new = ''

    if c_xa in special_map:
        ward_code = special_map[c_xa]
        m = df_cc[df_cc['ward_code'] == ward_code]
        if not m.empty:
            bc_new = m.iloc[0]['Bưu Cục new']
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
            huyen = matches[0]['Huyện/TP']
            tinh = matches[0]['c']
            xa = matches[0]['Phường/Xã']
        elif len(matches) > 1:
            h_matches = [m for m in matches if c_huyen == clean_text(m['Huyện/TP'])]
            if len(h_matches) >= 1:
                ward_code = h_matches[0]['ward_code']
                bc_new = h_matches[0]['Bưu Cục new']
                huyen = h_matches[0]['Huyện/TP']
                tinh = h_matches[0]['c']
                xa = h_matches[0]['Phường/Xã']

    if not ward_code:
        continue

    final_bc = bc_new if bc_new else bc_ka
    if xa == 'Phường Nghĩa Tân':
        final_bc = '(DNO) Đông Gia Nghĩa'

    am = map_bc_am.get(final_bc, '')
    if 'Đức Trọng' in final_bc or 'Di Linh' in final_bc:
        am = 'Nguyễn Lê Nguyên Vũ'
    elif not am:
        if 'Đơn Dương' in final_bc or 'Đà Lạt' in final_bc:
            am = 'Lê Văn Trường'
        elif '(DNO)' in final_bc:
            am = 'Huỳnh Thúc Duân'

    if ward_code in all_rows:
        # Already exists from Đang OFF -> keep, but update times if needed
        pass
    else:
        phan_loai = "SPE đề xuất MỚI (Tắt từ 16/09)" if tg_tat == '16/09/2026' else "SPE đề xuất THÊM"
        all_rows[ward_code] = {
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
        }

df_merged = pd.DataFrame(list(all_rows.values()))
print(f"\nTotal combined unique routes: {len(df_merged)}")
print("\nGrouped by Bưu Cục & AM:")
print(df_merged.groupby(['AM', 'Bưu Cục']).size())
