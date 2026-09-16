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
    # remove prefixes
    for p in ['thị trấn ', 'thị xã ', 'thành phố ', 'quận ', 'huyện ', 'phường ', 'xã ']:
        if s.startswith(p):
            s = s[len(p):]
    s = s.replace("'", "").replace("’", "").replace("-", " ")
    return " ".join(s.split())

# Fetch cơ cấu
res = service.spreadsheets().values().get(spreadsheetId=sheet_id, range="'cơ cấu'!A1:I1500").execute()
rows_cc = res.get('values', [])
max_c = max(len(r) for r in rows_cc)
cc_padded = [r + [''] * (max_c - len(r)) for r in rows_cc]
df_cc = pd.DataFrame(cc_padded[1:], columns=cc_padded[0])

# Fetch KA off
res = service.spreadsheets().values().get(spreadsheetId=sheet_id, range="'KA off'!A1:K100").execute()
rows_ka = res.get('values', [])

print("Mapping KA off with co_cau:")
# KA off rows:
# col 0: Vùng ('NTB')
# col 1: Tỉnh
# col 2: Quận/huyện
# col 3: Phường/xã
# col 4: Bưu cục
# col 8: Thời gian tắt
# col 9: Thời gian mở

mapped_results = []
for idx, r in enumerate(rows_ka[1:], start=2):
    tinh = r[1] if len(r) > 1 else ''
    huyen = r[2] if len(r) > 2 else ''
    xa = r[3] if len(r) > 3 else ''
    bc = r[4] if len(r) > 4 else ''
    tg_tat = r[8] if len(r) > 8 else ''
    tg_mo = r[9] if len(r) > 9 else ''
    
    # Try match with co_cau
    c_tinh = clean_text(tinh)
    c_huyen = clean_text(huyen)
    c_xa = clean_text(xa)
    
    matches = []
    for _, cr in df_cc.iterrows():
        cc_tinh = clean_text(cr['c'])
        cc_huyen = clean_text(cr['Huyện/TP'])
        cc_xa = clean_text(cr['Phường/Xã'])
        
        if c_xa == cc_xa:
            # check tinh or huyen
            if c_tinh in cc_tinh or cc_tinh in c_tinh:
                matches.append(cr)
                
    if len(matches) == 1:
        m = matches[0]
        mapped_results.append({
            'row': idx,
            'tinh': tinh,
            'huyen': huyen,
            'xa': xa,
            'ward_code': m['ward_code'],
            'bc_cocau': m['Bưu Cục new'],
            'am': m['AM'],
            'tg_tat': tg_tat,
            'tg_mo': tg_mo,
            'status': 'OK'
        })
    elif len(matches) > 1:
        # filter by huyen
        h_matches = [m for m in matches if c_huyen == clean_text(m['Huyện/TP'])]
        if len(h_matches) == 1:
            m = h_matches[0]
            mapped_results.append({
                'row': idx,
                'tinh': tinh,
                'huyen': huyen,
                'xa': xa,
                'ward_code': m['ward_code'],
                'bc_cocau': m['Bưu Cục new'],
                'am': m['AM'],
                'tg_tat': tg_tat,
                'tg_mo': tg_mo,
                'status': 'OK'
            })
        else:
            mapped_results.append({
                'row': idx,
                'tinh': tinh,
                'huyen': huyen,
                'xa': xa,
                'ward_code': f"MULTI ({len(matches)})",
                'bc_cocau': '',
                'am': '',
                'tg_tat': tg_tat,
                'tg_mo': tg_mo,
                'status': 'MULTI'
            })
    else:
        mapped_results.append({
            'row': idx,
            'tinh': tinh,
            'huyen': huyen,
            'xa': xa,
            'ward_code': 'NOT FOUND',
            'bc_cocau': '',
            'am': '',
            'tg_tat': tg_tat,
            'tg_mo': tg_mo,
            'status': 'NOT FOUND'
        })

df_mapped = pd.DataFrame(mapped_results)
print(df_mapped.to_string())
