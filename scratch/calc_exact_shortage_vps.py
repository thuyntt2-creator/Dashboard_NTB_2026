# -*- coding: utf-8 -*-
import sys, os, gspread, unicodedata
import pandas as pd
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(os.path.abspath('.'))
from google.oauth2.credentials import Credentials

def norm_txt(s):
    if not s:
        return ""
    return unicodedata.normalize('NFC', str(s)).strip().lower()

creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
gc = gspread.authorize(creds)

# 1. Đọc GTC realtime từ tab 'auto' của sheet Năng suất
sh_ns = gc.open_by_key('1-p9VUXndK_7BoiT-a81UfTCbUi953XNmVBoXaTGis_c')
ws_auto = sh_ns.worksheet('auto')
rows_auto = ws_auto.get_all_values()
headers = rows_auto[3]
df_auto = pd.DataFrame(rows_auto[4:], columns=headers)

df_auto['Giao TC'] = pd.to_numeric(df_auto['Giao TC'].str.replace(',', ''), errors='coerce').fillna(0)
df_auto['Gán Giao'] = pd.to_numeric(df_auto['Gán Giao'].str.replace(',', ''), errors='coerce').fillna(0)

agg_auto = df_auto.groupby('Bưu Cục').agg({'Giao TC': 'sum', 'Gán Giao': 'sum'}).reset_index()

# 2. Đọc file BC Cảnh Báo để lấy target và 6 ngày
# Sử dụng trực tiếp logic từ report_BC_canh_bao_gtalk.py để tính chuẩn xác
from report_BC_canh_bao_gtalk import (
    load_cocau, load_historical_data, calculate_rolling_metrics,
    determine_warning_group, calculate_target_gtc, NGUONG_AN_TOAN_PCT,
    HE_SO_LICH_SU, BUU_CUC_CANH_BAO_11
)

cocau_df = load_cocau()
hist_df = load_historical_data()
rolling_df, dates_used = calculate_rolling_metrics(hist_df, cocau_df)

print(f"Dates used for 6-day history: {dates_used}")

# Lấy Vol hôm nay từ file 21/10
file_21 = r"C:\Users\lap4all\Downloads\Bao_cao_ton_dong_lay_giao_tra_2026-10-21_at_09_00_03.xlsx"
df_today = pd.read_excel(file_21)
# Bưu cục là cột B (Tên kho giao)
col_bc_today = [c for c in df_today.columns if 'kho' in str(c).lower() or 'bưu cục' in str(c).lower()][0]
vol_today_map = df_today[col_bc_today].value_counts().to_dict()

# Chuẩn hóa map vol hôm nay
norm_vol_today = {norm_txt(k): v for k, v in vol_today_map.items()}

# Chuẩn hóa map live gtc
norm_live_gtc = {}
norm_live_gan = {}
for _, r in agg_auto.iterrows():
    bc_name = r['Bưu Cục']
    # remove prefix like (LDO), (DNO), etc.
    clean_bc = bc_name
    if ')' in clean_bc:
        clean_bc = clean_bc.split(')', 1)[1].strip()
    norm_live_gtc[norm_txt(bc_name)] = r['Giao TC']
    norm_live_gtc[norm_txt(clean_bc)] = r['Giao TC']
    norm_live_gan[norm_txt(bc_name)] = r['Gán Giao']
    norm_live_gan[norm_txt(clean_bc)] = r['Gán Giao']

def find_live(bc):
    nbc = norm_txt(bc)
    for k, v in norm_live_gtc.items():
        if nbc in k or k in nbc:
            return v, norm_live_gan[k]
    return 0, 0

def find_vol(bc):
    nbc = norm_txt(bc)
    for k, v in norm_vol_today.items():
        if nbc in k or k in nbc:
            return v
    return 0

results = []
for _, row in rolling_df.iterrows():
    bc = row['Bưu cục']
    # Check if in 11 warning
    is_in_11 = any(norm_txt(w) in norm_txt(bc) for w in BUU_CUC_CANH_BAO_11)
    if not is_in_11:
        continue
    
    vol_td = find_vol(bc)
    gtc_live, gan_live = find_live(bc)
    
    gtc_6d = row['gtc_6d']
    vol_6d = row['vol_6d']
    best_pct = row['best_pct_7d']
    
    target, t1, t2, t3 = calculate_target_gtc(vol_td, gtc_6d, vol_6d, best_pct)
    
    con_thieu = max(0, target - gtc_live)
    
    pct_live = (gtc_live / vol_td * 100) if vol_td > 0 else 0
    pct_live_gan = (gtc_live / gan_live * 100) if gan_live > 0 else 0
    
    kha_nang = "✅ Có thể thoát hôm nay" if target <= vol_td else "🔴 Cần thêm ngày (Max target)"
    if con_thieu == 0 and gtc_live >= target:
        kha_nang = "🎉 ĐÃ ĐẠT TARGET THOÁT BỂ!"
        
    results.append({
        'Bưu cục': bc,
        'AM': row['AM'],
        'Tỉnh': row['Tỉnh'],
        'Vol 21/10': vol_td,
        'Gán Live': gan_live,
        'GTC Live (VPS)': gtc_live,
        '%GTC/Gán': pct_live_gan,
        'Target Thoát Bể': target,
        'Còn Thiếu': con_thieu,
        'Khả năng': kha_nang
    })

res_df = pd.DataFrame(results)
print("\n" + "="*95)
print(f"{'BƯU CỤC':<24} | {'VOL 21/10':<9} | {'GTC LIVE':<8} | {'TARGET':<8} | {'CÒN THIẾU':<9} | {'TRẠNG THÁI / KHẢ NĂNG'}")
print("="*95)
for _, r in res_df.iterrows():
    print(f"{r['Bưu cục']:<24} | {r['Vol 21/10']:<9.0f} | {r['GTC Live (VPS)']:<8.0f} | {r['Target Thoát Bể']:<8.0f} | {r['Còn Thiếu']:<9.0f} | {r['Khả năng']}")
print("="*95)
