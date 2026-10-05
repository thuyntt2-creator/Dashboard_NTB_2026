import os
import sys
import pandas as pd
import json
import re
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

print("🚀 Running process_kd_looker_w40.py...")

downloads = r'C:\Users\lap4all\Downloads'
xl_path = os.path.join(downloads, '_NTB - BÁO CÁO TUẦN KINH DOANH (Looker).xlsx')

if not os.path.exists(xl_path):
    print(f"❌ File not found: {xl_path}")
    sys.exit(1)

def parse_date(v):
    if v is None or pd.isna(v): return None
    if isinstance(v, (pd.Timestamp, datetime)):
        return v.strftime('%Y-%m-%d')
    s = str(v).strip()
    m = re.search(r'(\d{1,2})\s+thg\s+(\d{1,2}),?\s+(\d{4})', s)
    if m:
        return f'{int(m.group(3)):04d}-{int(m.group(2)):02d}-{int(m.group(1)):02d}'
    m2 = re.search(r'(\d{4})-(\d{2})-(\d{2})', s)
    if m2:
        return m2.group(0)
    m3 = re.search(r'(\d{1,2})/(\d{1,2})/(\d{4})', s)
    if m3:
        return f'{int(m3.group(3)):04d}-{int(m3.group(2)):02d}-{int(m3.group(1)):02d}'
    return None

# =========================================================================
# 1. READ TONG_QUAN
# =========================================================================
print("Reading sheet 'tong_quan'...")
df_tq = pd.read_excel(xl_path, sheet_name='tong_quan')
df_tq['parsed_date'] = df_tq['Ngay'].apply(parse_date)
df_tq['dt'] = pd.to_numeric(df_tq['DoanhThu'], errors='coerce').fillna(0)
df_tq['vol'] = pd.to_numeric(df_tq['Volume'], errors='coerce').fillna(0)
df_tq['am'] = df_tq['AM_format'].astype(str).str.strip()

# Business Reporting Cycle:
# Prev: 20/09/2026 - 26/09/2026
# Curr: 27/09/2026 - 03/10/2026
prev_range = ('2026-09-20', '2026-09-26')
curr_range = ('2026-09-27', '2026-10-03')

sub_tq_prev = df_tq[(df_tq['parsed_date'] >= prev_range[0]) & (df_tq['parsed_date'] <= prev_range[1])]
sub_tq_curr = df_tq[(df_tq['parsed_date'] >= curr_range[0]) & (df_tq['parsed_date'] <= curr_range[1])]

tot_rev_p = float(sub_tq_prev['dt'].sum())
tot_rev_c = float(sub_tq_curr['dt'].sum())
tot_vol_p = int(sub_tq_prev['vol'].sum())
tot_vol_c = int(sub_tq_curr['vol'].sum())
diff_rev = tot_rev_c - tot_rev_p
pct_diff_rev = round((diff_rev / tot_rev_p) * 100, 1) if tot_rev_p > 0 else 0.0
diff_vol = tot_vol_c - tot_vol_p
pct_diff_vol = round((diff_vol / tot_vol_p) * 100, 1) if tot_vol_p > 0 else 0.0

print(f"Tổng quan Kinh Doanh: DT {tot_rev_p/1e6:,.1f} Tr -> {tot_rev_c/1e6:,.1f} Tr ({diff_rev/1e6:+,.1f} Tr / {pct_diff_rev:+.1f}%)")
print(f"Tổng Volume: {tot_vol_p:,} -> {tot_vol_c:,} ({diff_vol:+,} / {pct_diff_vol:+.1f}%)")

# Group by AM
am_tq_p = sub_tq_prev.groupby('am').agg({'dt': 'sum', 'vol': 'sum'})
am_tq_c = sub_tq_curr.groupby('am').agg({'dt': 'sum', 'vol': 'sum'})
all_ams = sorted(list(set(am_tq_c.index) | set(am_tq_p.index)))
all_ams = [a for a in all_ams if a and a != 'nan' and a != 'Không xác định']

kd_am = []
for a in all_ams:
    rc = float(am_tq_c.loc[a, 'dt']) if a in am_tq_c.index else 0.0
    rp = float(am_tq_p.loc[a, 'dt']) if a in am_tq_p.index else 0.0
    vc = int(am_tq_c.loc[a, 'vol']) if a in am_tq_c.index else 0
    vp = int(am_tq_p.loc[a, 'vol']) if a in am_tq_p.index else 0
    d_r = rc - rp
    pct_d_r = round((d_r / rp) * 100, 1) if rp > 0 else (100.0 if rc > 0 else 0.0)
    pct_r = round((rc / tot_rev_c) * 100, 1) if tot_rev_c > 0 else 0.0
    kd_am.append({
        'am': a,
        'vol_prev': vp,
        'vol_curr': vc,
        'diff_vol': vc - vp,
        'vol_diff': vc - vp,
        'rev_prev': rp,
        'rev_curr': rc,
        'diff_rev': d_r,
        'rev_diff': d_r,
        'pct_rev': pct_r,
        'rev_pct': pct_r,
        'pct_diff_rev': pct_d_r
    })

kd_am.sort(key=lambda x: x['rev_curr'], reverse=True)

# =========================================================================
# 2. READ F30
# =========================================================================
print("Reading sheet 'f30'...")
df_f30 = pd.read_excel(xl_path, sheet_name='f30')
date_col_f = [c for c in df_f30.columns if 'ngày' in c.lower()][0]
df_f30['parsed_date'] = df_f30[date_col_f].apply(parse_date)

def clean_f30_rev(v):
    if pd.isna(v): return 0.0
    try:
        val = float(str(v).replace(',', '').strip())
        if 0 < val < 1000:
            val = val * 1000
        return val
    except:
        return 0.0

df_f30['dt'] = df_f30['DoanhThu_NoVAT'].apply(clean_f30_rev)
df_f30['vol'] = pd.to_numeric(df_f30['Volume'], errors='coerce').fillna(0)
df_f30['am'] = df_f30['AM'].astype(str).str.strip()

sub_f_prev = df_f30[(df_f30['parsed_date'] >= prev_range[0]) & (df_f30['parsed_date'] <= prev_range[1])]
sub_f_curr = df_f30[(df_f30['parsed_date'] >= curr_range[0]) & (df_f30['parsed_date'] <= curr_range[1])]

f_tot_p_kh = len(sub_f_prev)
f_tot_c_kh = len(sub_f_curr)
f_diff_kh = f_tot_c_kh - f_tot_p_kh
f_pct_kh = round((f_diff_kh / f_tot_p_kh) * 100, 1) if f_tot_p_kh > 0 else 0.0

f_tot_p_rev = float(sub_f_prev['dt'].sum())
f_tot_c_rev = float(sub_f_curr['dt'].sum())
f_diff_rev = f_tot_c_rev - f_tot_p_rev
f_pct_rev = round((f_diff_rev / f_tot_p_rev) * 100, 1) if f_tot_p_rev > 0 else 0.0

print(f"Tổng F30: {f_tot_p_kh} shops -> {f_tot_c_kh} shops ({f_diff_kh:+d} / {f_pct_kh:+.1f}%), DT: {f_tot_p_rev/1e6:,.1f} Tr -> {f_tot_c_rev/1e6:,.1f} Tr")

# F30 by AM
f_am_p = sub_f_prev.groupby('am').agg({'dt': 'sum', 'Mã KH': 'count'})
f_am_c = sub_f_curr.groupby('am').agg({'dt': 'sum', 'Mã KH': 'count'})
all_f_ams = sorted(list(set(f_am_c.index) | set(f_am_p.index)))
all_f_ams = [a for a in all_f_ams if a and a != 'nan' and a != 'Không xác định']

f30_am = []
for a in all_f_ams:
    kc = int(f_am_c.loc[a, 'Mã KH']) if a in f_am_c.index else 0
    kp = int(f_am_p.loc[a, 'Mã KH']) if a in f_am_p.index else 0
    rc = float(f_am_c.loc[a, 'dt']) if a in f_am_c.index else 0.0
    rp = float(f_am_p.loc[a, 'dt']) if a in f_am_p.index else 0.0
    d_k = kc - kp
    pct_k = round((d_k / kp) * 100, 1) if kp > 0 else (100.0 if kc > 0 else 0.0)
    f30_am.append({
        'am': a,
        'kh_prev': kp,
        'kh_curr': kc,
        'diff_kh': d_k,
        'pct_diff_kh': pct_k,
        'rev_prev': rp,
        'rev_curr': rc,
        'diff_rev': rc - rp
    })

f30_am.sort(key=lambda x: x['kh_curr'], reverse=True)

# =========================================================================
# 3. READ KH A
# =========================================================================
print("Reading sheet 'KH A'...")
df_kha = pd.read_excel(xl_path, sheet_name='KH A')

def parse_date_str(d):
    m = re.search(r'(\d+)\s+thg\s+(\d+)', str(d))
    if m:
        return f"{int(m.group(1)):02d}/{int(m.group(2)):02d}"
    return str(d)

df_kha['clean_date'] = df_kha['Ngay'].apply(parse_date_str)
df_kha['DT_num'] = pd.to_numeric(df_kha['DT'].astype(str).str.replace(',', '').str.strip(), errors='coerce').fillna(0)

all_kha_dates = sorted(
    [d for d in df_kha['clean_date'].unique() if '/' in d],
    key=lambda x: (int(x.split('/')[1]), int(x.split('/')[0]))
)
print("KH A Dates:", all_kha_dates)

SHOP_META = {
    "3200594": {"am": "Lê Thanh Nhựt", "buu_cuc": "2357 - (BTH) Đồng Kho"},
    "3349413": {"am": "Phan Đình Duy", "buu_cuc": "(KHO) Diên Khánh 1"},
    "3559462": {"am": "Nguyễn Lê Nguyên Vũ", "buu_cuc": "20663000 - (LDO) Đạ Tẻh"},
    "3910354": {"am": "Phan Đình Duy", "buu_cuc": "20495000 - (KHO) Nha Trang"},
    "3950975": {"am": "Phan Đình Duy", "buu_cuc": "21046000 - (KHO) Vạn Ninh"},
    "4264387": {"am": "Huỳnh Thúc Duân", "buu_cuc": "22242000 - (DNO) Bắc Gia Nghĩa"},
    "4313038": {"am": "Hồng Bích Nga", "buu_cuc": "20785000 - (LDO) B'Lao"},
    "5099749": {"am": "Thái Thị Thanh Thư", "buu_cuc": "22363000 - (KHO) Nam Nha Trang 3"},
    "5109892": {"am": "Lê Văn Trường", "buu_cuc": "22116000 - (LDO) Xuân Trường - Đà Lạt"},
    "5197975": {"am": "Nguyễn Duy Long", "buu_cuc": "20499000 - (NTH) Phước Dinh"},
    "5212344": {"am": "Huỳnh Thúc Duân", "buu_cuc": "22242000 - (DNO) Bắc Gia Nghĩa"},
    "5234277": {"am": "Hồng Bích Nga", "buu_cuc": "(LDO) Bảo Lộc 1"}
}

latest_date = all_kha_dates[-1] if all_kha_dates else '04/10'
w1_date = all_kha_dates[0] if len(all_kha_dates) >= 1 else '01/10'

kha_shops = []
for makh, g in df_kha.groupby('MaKH', sort=False):
    g = g.sort_values('clean_date')
    last_r = g.iloc[-1]
    
    daily_dt = {}
    for _, r in g.iterrows():
        daily_dt[r['clean_date']] = float(r['DT_num'])
    for d in all_kha_dates:
        if d not in daily_dt:
            daily_dt[d] = 0.0
            
    dt_n1 = daily_dt.get(latest_date, 0.0)
    dt_w1 = daily_dt.get(w1_date, 0.0)
    diff_w1 = round(dt_n1 - dt_w1, 1)
    pct_w1 = round((diff_w1 / dt_w1) * 100, 1) if dt_w1 > 0 else (100.0 if dt_n1 > 0 else 0.0)
    
    mtd_val = float(str(last_r.get('MTD', 0)).replace(',', '').strip() or 0)
    vung = str(last_r.get('Vung', ''))
    tinh = vung.split('-')[-1].strip() if '-' in vung else vung
    
    pct_mtd_val = last_r.get('% sv MTD M-1', '')
    if isinstance(pct_mtd_val, (int, float)):
        pct_mtd_str = f"{pct_mtd_val * 100:.1f}%"
    else:
        pct_mtd_str = str(pct_mtd_val).strip()
        
    pct_tru_val = last_r.get('%Trụ hạng', '')
    if isinstance(pct_tru_val, (int, float)):
        pct_tru_str = f"{pct_tru_val * 100:.1f}%"
    else:
        pct_tru_str = str(pct_tru_val).strip()
    
    meta = SHOP_META.get(str(makh), {})
    am_name = meta.get('am', '') or str(last_r.get('AM', '')).strip()
    buu_cuc = meta.get('buu_cuc', '') or str(last_r.get('Bưu cục', '')).strip()
    
    kha_shops.append({
        "stt": str(len(kha_shops) + 1),
        "makh": str(makh),
        "tenkh": str(last_r.get('TenKH', '')).strip(),
        "nhom_n": str(last_r.get('Nhom_N', 'A5')).strip() or 'A5',
        "nhomkh_1": str(last_r.get('NhomKH_1', '')).strip(),
        "ph_prev": str(last_r.get('PH_N-1', '')).strip(),
        "vung": vung,
        "tinh": tinh,
        "nhanvien": str(last_r.get('Nhanvien', '')).strip(),
        "vol_cam_ket": str(last_r.get('Volume cam kết', '')).strip(),
        "aov": str(last_r.get('AOV', '')).strip(),
        "mtd": mtd_val,
        "pct_mtd_m1": pct_mtd_str,
        "pct_tru_hang": pct_tru_str,
        "am": am_name,
        "buu_cuc": buu_cuc,
        "daily_dt": daily_dt,
        "dt_w1": dt_w1,
        "dt_n1": dt_n1,
        "diff_w1": diff_w1,
        "pct_w1": pct_w1
    })

kha_shops.sort(key=lambda s: s['mtd'], reverse=True)
for idx, s in enumerate(kha_shops):
    s['stt'] = str(idx + 1)

# Group A warnings
kha_warnings = []
for s in kha_shops:
    tru_hang_val = float(str(s.get('pct_tru_hang', 0)).replace('%', '').strip() or 0)
    is_drop = s['diff_w1'] < 0 and s['pct_w1'] <= -20
    is_at_risk = tru_hang_val < 50
    
    reasons = []
    if s['diff_w1'] < 0:
        reasons.append(f"▼ Giảm {abs(s['pct_w1'])}% sv đầu kỳ ({s['diff_w1']} Tr)")
    if tru_hang_val < 25:
        reasons.append(f"Nguy cơ rớt hạng (Trụ hạng {s['pct_tru_hang']})")
    elif tru_hang_val < 60:
        reasons.append(f"Trụ hạng thấp ({s['pct_tru_hang']})")
    
    if is_drop or is_at_risk:
        kha_warnings.append({
            "stt": str(len(kha_warnings) + 1),
            "makh": s['makh'],
            "tenkh": s['tenkh'],
            "nhomkh": s['nhom_n'],
            "vung": s['vung'],
            "nhanvien": s['nhanvien'],
            "cam_ket": s['vol_cam_ket'],
            "mtd": s['mtd'],
            "pct_mtd_m1": s['pct_mtd_m1'],
            "pct_tru_hang": s['pct_tru_hang'],
            "aov": s['aov'],
            "ngay": latest_date,
            "dt": s['dt_n1'],
            "dt_n1": s['dt_n1'],
            "dt_w1": s['dt_w1'],
            "diff_w1": s['diff_w1'],
            "pct_w1": s['pct_w1'],
            "am": s['am'],
            "buu_cuc": s['buu_cuc'],
            "canh_bao": " | ".join(reasons) if reasons else "Cần theo dõi sát"
        })

# AM Chart (Group A MTD)
am_totals = {}
for s in kha_shops:
    am_totals[s['am']] = am_totals.get(s['am'], 0.0) + s['mtd']
tot_mtd = sum(am_totals.values())
am_chart = []
for am, m in sorted(am_totals.items(), key=lambda x: x[1], reverse=True):
    am_chart.append({
        "am": am,
        "mtd": round(m, 1),
        "pct": round((m / tot_mtd) * 100, 1) if tot_mtd > 0 else 0.0
    })

# Daily trend (Group A)
daily_trend = []
for d in all_kha_dates:
    s_d = sum(s['daily_dt'].get(d, 0.0) for s in kha_shops)
    daily_trend.append({"date": d, "dt": round(s_d, 1)})

# =========================================================================
# 4. LOAD AND UPDATE DATA.JSON & DATA.JS
# =========================================================================
with open('data.json', 'r', encoding='utf-8') as f:
    orig_data = json.load(f)

churn_top10 = orig_data.get('kinh_doanh', {}).get('churn_top10', [])

kinh_doanh_obj = {
    "total": {
        "vol_prev": tot_vol_p,
        "vol_curr": tot_vol_c,
        "diff_vol": diff_vol,
        "vol_diff": diff_vol,
        "rev_prev": tot_rev_p,
        "rev_curr": tot_rev_c,
        "diff_rev": diff_rev,
        "rev_diff": diff_rev,
        "pct_diff_rev": pct_diff_rev,
        "pct_diff_vol": pct_diff_vol
    },
    "am": kd_am,
    "top_drop": [x for x in kd_am if x['diff_rev'] < 0],
    "churn_top10": churn_top10,
    "churn_zero": [],
    "khach_hang_a": {
        "dates": all_kha_dates,
        "shops": kha_shops,
        "warning": kha_warnings,
        "am_chart": am_chart,
        "daily_trend": daily_trend
    }
}

f30_obj = {
    "total": {
        "kh_prev": f_tot_p_kh,
        "kh_curr": f_tot_c_kh,
        "diff_kh": f_diff_kh,
        "pct_diff_kh": f_pct_kh,
        "rev_prev": f_tot_p_rev,
        "rev_curr": f_tot_c_rev,
        "diff_rev": f_diff_rev,
        "pct_diff_rev": f_pct_rev
    },
    "am": f30_am,
    "top_drop": [x for x in f30_am if x['diff_kh'] < 0]
}

orig_data['kinh_doanh'] = kinh_doanh_obj
orig_data['f30'] = f30_obj

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(orig_data, f, ensure_ascii=False, indent=2)

with open('data.js', 'w', encoding='utf-8') as f:
    f.write("window.DASHBOARD_DATA = " + json.dumps(orig_data, ensure_ascii=False, indent=2) + ";\n")
    f.write("window.DATA = window.DASHBOARD_DATA;\n")
    f.write("const REPORT_DATA = window.DASHBOARD_DATA;\n")

print("\n🎉 SUCCESS: Updated Kinh Doanh and F30 for W40!")
print(f"Kinh Doanh: Doanh Thu = {tot_rev_c/1e6:,.1f} Tr ({pct_diff_rev:+.1f}%), Volume = {tot_vol_c:,} ({pct_diff_vol:+.1f}%)")
print(f"F30: Khách hàng mới = {f_tot_c_kh} shops ({f_pct_kh:+.1f}%), Doanh Thu = {f_tot_c_rev/1e6:,.1f} Tr ({f_pct_rev:+.1f}%)")
print(f"Group A: {len(kha_shops)} shops, MTD = {tot_mtd:,.1f} Tr ₫, Warning = {len(kha_warnings)} shops")
