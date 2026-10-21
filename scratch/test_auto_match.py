# -*- coding: utf-8 -*-
import sys, os, gspread, unicodedata
sys.path.append(os.path.abspath('.'))
import pandas as pd
sys.stdout.reconfigure(encoding='utf-8')
from google.oauth2.credentials import Credentials

def normalize_nfc(text):
    if not text:
        return ""
    return unicodedata.normalize('NFC', str(text)).strip()

creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
gc = gspread.authorize(creds)

# 1. Đọc sheet Năng suất tab auto
sh_ns = gc.open_by_key('1-p9VUXndK_7BoiT-a81UfTCbUi953XNmVBoXaTGis_c')
ws_auto = sh_ns.worksheet('auto')
rows_auto = ws_auto.get_all_values()
headers = rows_auto[3]
df_auto = pd.DataFrame(rows_auto[4:], columns=headers)

df_auto['Giao TC'] = pd.to_numeric(df_auto['Giao TC'].str.replace(',', ''), errors='coerce').fillna(0)
df_auto['Gán Giao'] = pd.to_numeric(df_auto['Gán Giao'].str.replace(',', ''), errors='coerce').fillna(0)

agg_auto = df_auto.groupby('Bưu Cục').agg({'Giao TC': 'sum', 'Gán Giao': 'sum'}).reset_index()

# 2. Đọc 11 bưu cục từ report_BC_canh_bao_gtalk
import report_BC_canh_bao_gtalk as rpt
cb_items, update_time, n1_comp = rpt.load_data()

print(f"Tổng số bưu cục cảnh báo: {len(cb_items)}")

# Tạo map chuẩn hóa từ auto
auto_map = {}
for _, r in agg_auto.iterrows():
    bc_name = normalize_nfc(r['Bưu Cục'])
    gtc = int(r['Giao TC'])
    gan = int(r['Gán Giao'])
    auto_map[bc_name] = (gtc, gan)
    # Thêm bản không có prefix (LDO), (DNO), ...
    if ')' in bc_name:
        clean = bc_name.split(')', 1)[1].strip()
        auto_map[clean] = (gtc, gan)

def find_auto(bc):
    nbc = normalize_nfc(bc).lower()
    for k, v in auto_map.items():
        nk = k.lower()
        if nbc in nk or nk in nbc:
            return v
    # Thử tách từ
    parts = [p for p in nbc.split() if len(p) >= 3 and p not in ['ldo', 'dno', 'kho', 'bth', 'nth', 'bưu', 'cục']]
    for k, v in auto_map.items():
        nk = k.lower()
        if any(p in nk for p in parts):
            return v
    return 0, 0

print("\n" + "="*85)
print(f"{'BƯU CỤC':<26} | {'VOL HÔM NAY':<11} | {'TARGET':<8} | {'GTC LIVE':<9} | {'CÒN THIẾU':<10} | {'TIẾN ĐỘ'}")
print("="*85)

for it in cb_items:
    name = it['bc_name']
    vol = it['vol_today']
    target = it['req_gtc']
    gtc_live, gan_live = find_auto(name)
    thieu = max(0, target - gtc_live)
    pct = round(gtc_live / target * 100) if target > 0 else 0
    status = f"Thiếu {thieu:,} đ" if thieu > 0 else "🎉 ĐÃ ĐẠT TARGET"
    if target > vol:
        status += " (Bể sâu)"
    print(f"{name:<26} | {vol:<11,f} | {target:<8,f} | {gtc_live:<9,f} | {thieu:<10,f} | {pct:>3}% ({status})")
print("="*85)
