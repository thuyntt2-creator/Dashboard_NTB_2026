import sys
sys.stdout.reconfigure(encoding='utf-8')
import gspread
from google.oauth2.credentials import Credentials as UserCredentials
import pandas as pd
import json
from datetime import datetime

scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = UserCredentials.from_authorized_user_file(r'C:\Users\lap4all\Desktop\auto-report\authorized_user.json', scopes=scopes)
gc = gspread.authorize(creds)

sh2 = gc.open_by_key('1lmQv8KwHJzDFs_RMz64ydu4SOmG3M1YAzILNFGtzFec')

# 1. Read raw_buu_cuc_canh_bao
ws_raw = sh2.worksheet('raw_buu_cuc_canh_bao')
raw_rows = ws_raw.get_all_values()
df_raw = pd.DataFrame(raw_rows[1:], columns=raw_rows[0])
df_ntb = df_raw[(df_raw['vung'] == 'NTB') & (df_raw['canh_bao_gtc'] != 'Bình thường')].copy()

# 2. Read luu_tru
ws_luu = sh2.worksheet('luu_tru')
luu_rows = ws_luu.get_all_values()
df_luu = pd.DataFrame(luu_rows[1:], columns=luu_rows[0])
df_luu_ntb = df_luu[df_luu['vung'] == 'NTB'].copy()
df_luu_ntb['bc_id'] = df_luu_ntb['bc_id'].astype(str)

# 3. Read Backlog
ws_bl = sh2.worksheet('Backlog')
bl_rows = ws_bl.get_all_values()
df_bl = pd.DataFrame(bl_rows[1:], columns=bl_rows[0])
for col in ['total_order', 'total_order_aging_5d', 'total_order_da_gan']:
    df_bl[col] = pd.to_numeric(df_bl[col], errors='coerce').fillna(0)
df_bl['kho_giao_id'] = df_bl['kho_giao_id'].astype(str)
bl_map = df_bl.groupby('kho_giao_id').agg({
    'total_order': 'sum',
    'total_order_aging_5d': 'sum'
}).to_dict(orient='index')

# Read AM mapping from data.json or raw_nhan_su
ws_ns = sh2.worksheet('raw_nhan_su')
ns_rows = ws_ns.get_all_values()
df_ns = pd.DataFrame(ns_rows[1:], columns=ns_rows[0])
am_col = [c for c in df_ns.columns if 'am' in c.lower()]
bc_col = [c for c in df_ns.columns if 'kho' in c.lower() or 'bc' in c.lower() or 'bưu cục' in c.lower()]
print("NS cols:", df_ns.columns)

# Get distinct dates in luu_tru
print("Luu tru dates count:", df_luu_ntb['ngay'].nunique())
dates = sorted(df_luu_ntb['ngay'].unique())
print("Earliest date:", dates[0], "Latest date:", dates[-1])

results = []
for _, r in df_ntb.iterrows():
    bid = str(r['bc_id'])
    bname = r['buu_cuc']
    tinh = r['tinh_quan']
    warn_type = r['canh_bao_gtc']
    
    # Filter luu_tru for this bc_id
    sub = df_luu_ntb[df_luu_ntb['bc_id'] == bid]
    
    # Days in warning
    warn_days_count = len(sub[sub['canh_bao_gtc'] != 'Bình thường'])
    
    # W36 vs W37 GTC
    # In raw, pct_gtc_7ngay is W37
    # Look for 2026-09-06 or 9/6/2026 in luu_tru for W36
    row_w36 = sub[sub['ngay'].str.contains('9/6/2026|2026-09-06|2026-09-07')]
    w36_val = None
    if len(row_w36) > 0:
        val_str = str(row_w36.iloc[-1]['pct_gtc_7ngay']).replace('%', '').strip()
        try:
            w36_val = float(val_str)
            if w36_val < 1.0: w36_val *= 100
        except:
            w36_val = None
            
    val_w37_str = str(r['pct_gtc_7ngay']).replace('%', '').strip()
    try:
        w37_val = float(val_w37_str)
        if w37_val < 1.0: w37_val *= 100
    except:
        w37_val = 0.0

    val_best_str = str(r['pct_gtc_lich_su_tot_nhat']).replace('%', '').strip()
    try:
        best_val = float(val_best_str)
        if best_val < 1.0: best_val *= 100
    except:
        best_val = 0.0

    bl_info = bl_map.get(bid, {'total_order': 0, 'total_order_aging_5d': 0})
    backlog = int(bl_info['total_order'])
    backlog_5d = int(bl_info['total_order_aging_5d'])
    
    # AM name
    am_name = ""
    # search in df_ns
    ns_match = df_ns[df_ns['bưu cục id'].astype(str) == bid] if 'bưu cục id' in df_ns.columns else pd.DataFrame()
    if len(ns_match) > 0 and 'AM' in ns_match.columns:
        am_name = ns_match.iloc[0]['AM']
    
    diff = round(w37_val - (w36_val if w36_val is not None else w37_val), 1)

    results.append({
        'id': bid,
        'bc': bname,
        'tinh': tinh,
        'am': am_name,
        'gtc_w36': round(w36_val, 1) if w36_val is not None else round(w37_val, 1),
        'gtc_w37': round(w37_val, 1),
        'diff': diff,
        'gtc_best': round(best_val, 1),
        'warn_type': warn_type,
        'days_warn': warn_days_count,
        'backlog': backlog,
        'backlog_5d': backlog_5d,
        'clear_days': max(1, round(backlog / 250)) if backlog > 0 else 1
    })

# Sort by gtc_w37 ascending (worst first)
results = sorted(results, key=lambda x: x['gtc_w37'])

print("\n--- RESULTS JSON ---")
print(json.dumps(results, ensure_ascii=False, indent=2))

with open('scratch/bc_canh_bao_calculated.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

