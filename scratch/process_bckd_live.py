import gspread
import pandas as pd
import json
import re
from datetime import datetime

print("Connecting to Google Sheet BCKD (1E9BdaxouCeTUBeGLh0kyieyWE6wZoymglbZw19LRKEo)...")
gc = gspread.oauth(authorized_user_filename='authorized_user.json')
doc = gc.open_by_key('1E9BdaxouCeTUBeGLh0kyieyWE6wZoymglbZw19LRKEo')

# 1. READ TONG_QUAN
ws_tq = doc.worksheet('tong_quan')
vals_tq = ws_tq.get_all_values()
df_tq = pd.DataFrame(vals_tq[1:], columns=vals_tq[0])
df_tq['d'] = pd.to_datetime(df_tq['NgayDate'], format='%d/%m/%Y', errors='coerce')
df_tq['dt'] = pd.to_numeric(df_tq['DoanhThu'], errors='coerce').fillna(0)
df_tq['vol'] = pd.to_numeric(df_tq['Volume'], errors='coerce').fillna(0)
df_tq['am'] = df_tq['AM_format'].astype(str).str.strip()

# 2. READ F30
ws_f30 = doc.worksheet('f30')
vals_f30 = ws_f30.get_all_values()
df_f30 = pd.DataFrame(vals_f30[1:], columns=vals_f30[0])
df_f30['d'] = pd.to_datetime(df_f30['NgayDate'], format='%d/%m/%Y', errors='coerce')
df_f30['dt'] = pd.to_numeric(df_f30['DoanhThu_NoVAT'], errors='coerce').fillna(0)
df_f30['vol'] = pd.to_numeric(df_f30['Volume'], errors='coerce').fillna(0)
df_f30['am'] = df_f30['AM'].astype(str).str.strip()

# 3. DEFINE REPORTING PERIODS FOR W38 VS W37
# GHN Standard Weekly Calendar:
# W38: 14/09/2026 - 20/09/2026
# W37: 07/09/2026 - 13/09/2026
curr_range = ('2026-09-14', '2026-09-20')
prev_range = ('2026-09-07', '2026-09-13')

sub_tq_curr = df_tq[(df_tq['d'] >= curr_range[0]) & (df_tq['d'] <= curr_range[1])]
sub_tq_prev = df_tq[(df_tq['d'] >= prev_range[0]) & (df_tq['d'] <= prev_range[1])]

am_tq_c = sub_tq_curr.groupby('am').agg({'dt': 'sum', 'vol': 'sum'})
am_tq_p = sub_tq_prev.groupby('am').agg({'dt': 'sum', 'vol': 'sum'})

all_ams = sorted(list(set(am_tq_c.index) | set(am_tq_p.index)))
# Exclude empty or undefined if not needed, keep 'Không xác định' or clean
all_ams = [a for a in all_ams if a and a != 'nan']

tot_rev_c = float(sub_tq_curr['dt'].sum())
tot_rev_p = float(sub_tq_prev['dt'].sum())
tot_vol_c = int(sub_tq_curr['vol'].sum())
tot_vol_p = int(sub_tq_prev['vol'].sum())

kd_am = []
for a in all_ams:
    rc = float(am_tq_c.loc[a, 'dt']) if a in am_tq_c.index else 0.0
    rp = float(am_tq_p.loc[a, 'dt']) if a in am_tq_p.index else 0.0
    vc = int(am_tq_c.loc[a, 'vol']) if a in am_tq_c.index else 0
    vp = int(am_tq_p.loc[a, 'vol']) if a in am_tq_p.index else 0
    diff_r = rc - rp
    pct_diff_r = round((diff_r / rp) * 100, 1) if rp > 0 else (100.0 if rc > 0 else 0.0)
    pct_r = round((rc / tot_rev_c) * 100, 1) if tot_rev_c > 0 else 0.0
    kd_am.append({
        'am': a,
        'vol_prev': vp,
        'vol_curr': vc,
        'diff_vol': vc - vp,
        'rev_prev': rp,
        'rev_curr': rc,
        'diff_rev': diff_r,
        'pct_rev': pct_r,
        'pct_diff_rev': pct_diff_r
    })

kd_am.sort(key=lambda x: x['rev_curr'], reverse=True)

# F30 by AM
sub_f_curr = df_f30[(df_f30['d'] >= curr_range[0]) & (df_f30['d'] <= curr_range[1])]
sub_f_prev = df_f30[(df_f30['d'] >= prev_range[0]) & (df_f30['d'] <= prev_range[1])]

f_am_c = sub_f_curr.groupby('am').agg({'dt': 'sum', 'Mã KH': 'count'})
f_am_p = sub_f_prev.groupby('am').agg({'dt': 'sum', 'Mã KH': 'count'})

all_f_ams = sorted(list(set(f_am_c.index) | set(f_am_p.index)))
all_f_ams = [a for a in all_f_ams if a and a != 'nan']

f30_am = []
for a in all_f_ams:
    kc = int(f_am_c.loc[a, 'Mã KH']) if a in f_am_c.index else 0
    kp = int(f_am_p.loc[a, 'Mã KH']) if a in f_am_p.index else 0
    rc = float(f_am_c.loc[a, 'dt']) if a in f_am_c.index else 0.0
    rp = float(f_am_p.loc[a, 'dt']) if a in f_am_p.index else 0.0
    diff_k = kc - kp
    diff_r = rc - rp
    pct_k = round((diff_k / kp) * 100, 1) if kp > 0 else (100.0 if kc > 0 else 0.0)
    f30_am.append({
        'am': a,
        'kh_prev': kp,
        'kh_curr': kc,
        'diff_kh': diff_k,
        'pct_diff_kh': pct_k,
        'rev_prev': rp,
        'rev_curr': rc,
        'diff_rev': diff_r
    })

f30_am.sort(key=lambda x: x['kh_curr'], reverse=True)

# 4. READ KH A (GROUP A CUSTOMERS)
ws_kha = doc.worksheet('KH A')
vals_kha = ws_kha.get_all_values()
df_kha = pd.DataFrame(vals_kha[1:], columns=vals_kha[0])

def parse_date_str(d):
    m = re.search(r'(\d+)\s+thg\s+(\d+)', str(d))
    if m:
        return f"{int(m.group(1)):02d}/{int(m.group(2)):02d}"
    return str(d)

df_kha['clean_date'] = df_kha['Ngay'].apply(parse_date_str)
df_kha['DT_num'] = pd.to_numeric(df_kha['DT'].astype(str).str.replace(',', '').str.strip(), errors='coerce').fillna(0)

# September dates in chronological order
all_kha_dates = sorted(
    [d for d in df_kha['clean_date'].unique() if '/09' in d],
    key=lambda x: int(x.split('/')[0])
)

SHOP_META = {
    "3200594": {"am": "Lê Thanh Nhựt", "buu_cuc": "2357 - (BTH) Đồng Kho"},
    "3559462": {"am": "Nguyễn Lê Nguyên Vũ", "buu_cuc": "20663000 - (LDO) Đạ Tẻh"},
    "3910354": {"am": "Phan Đình Duy", "buu_cuc": "20495000 - (KHO) Nha Trang"},
    "3950975": {"am": "Phan Đình Duy", "buu_cuc": "21046000 - (KHO) Vạn Ninh"},
    "4264387": {"am": "Huỳnh Thúc Duân", "buu_cuc": "22242000 - (DNO) Bắc Gia Nghĩa"},
    "4313038": {"am": "Hồng Bích Nga", "buu_cuc": "20785000 - (LDO) B'Lao"},
    "5099749": {"am": "Thái Thị Thanh Thư", "buu_cuc": "22363000 - (KHO) Nam Nha Trang 3"},
    "5109892": {"am": "Lê Văn Trường", "buu_cuc": "22116000 - (LDO) Xuân Trường - Đà Lạt"},
    "5197975": {"am": "Nguyễn Duy Long", "buu_cuc": "20499000 - (NTH) Phước Dinh"},
    "5212344": {"am": "Huỳnh Thúc Duân", "buu_cuc": "22242000 - (DNO) Bắc Gia Nghĩa"}
}

latest_date = all_kha_dates[-1]  # '20/09'
w1_date = all_kha_dates[-8] if len(all_kha_dates) >= 8 else all_kha_dates[0]  # '13/09'

kha_shops = []
for makh, g in df_kha.groupby('MaKH', sort=False):
    g = g.sort_values('clean_date', key=lambda s: s.map(lambda x: int(x.split('/')[0]) if '/09' in str(x) else 0))
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
        "pct_mtd_m1": str(last_r.get('% sv MTD M-1', '')).strip(),
        "pct_tru_hang": str(last_r.get('%Trụ hạng', '')).strip(),
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
        reasons.append(f"▼ Giảm {abs(s['pct_w1'])}% sv W-1 ({s['diff_w1']} Tr)")
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

# 5. CHURN TOP 10 (From data.json or calculate from active data)
with open('data.json', 'r', encoding='utf-8') as f:
    orig_data = json.load(f)

churn_top10 = orig_data.get('kinh_doanh', {}).get('churn_top10', [])

# Assemble kinh_doanh and f30 objects
kinh_doanh_obj = {
    "total": {
        "vol_prev": tot_vol_p,
        "vol_curr": tot_vol_c,
        "diff_vol": tot_vol_c - tot_vol_p,
        "rev_prev": tot_rev_p,
        "rev_curr": tot_rev_c,
        "diff_rev": tot_rev_c - tot_rev_p,
        "pct_diff_rev": round((tot_rev_c - tot_rev_p) / tot_rev_p * 100, 1) if tot_rev_p > 0 else 0.0
    },
    "am": kd_am,
    "top_drop": [],
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
        "kh_prev": len(sub_f_prev),
        "kh_curr": len(sub_f_curr),
        "diff_kh": len(sub_f_curr) - len(sub_f_prev),
        "pct_diff_kh": round((len(sub_f_curr) - len(sub_f_prev)) / len(sub_f_prev) * 100, 1) if len(sub_f_prev) > 0 else 0.0,
        "rev_prev": float(sub_f_prev['dt'].sum()),
        "rev_curr": float(sub_f_curr['dt'].sum()),
        "diff_rev": float(sub_f_curr['dt'].sum() - sub_f_prev['dt'].sum()),
        "pct_diff_rev": round((sub_f_curr['dt'].sum() - sub_f_prev['dt'].sum()) / sub_f_prev['dt'].sum() * 100, 1) if sub_f_prev['dt'].sum() > 0 else 0.0
    },
    "am": f30_am,
    "top_drop": [x for x in f30_am if x['diff_kh'] < 0]
}

# Update data.json
orig_data['kinh_doanh'] = kinh_doanh_obj
orig_data['f30'] = f30_obj

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(orig_data, f, ensure_ascii=False, indent=2)

# Update data.js
with open('data.js', 'w', encoding='utf-8') as f:
    f.write("window.DASHBOARD_DATA = " + json.dumps(orig_data, ensure_ascii=False, indent=2) + ";\n")

print("SUCCESS: Updated data.json and data.js!")
print(f"Kinh Doanh W38: Doanh Thu = {kinh_doanh_obj['total']['rev_curr']:,.0f} đ (+{kinh_doanh_obj['total']['pct_diff_rev']}%), Volume = {kinh_doanh_obj['total']['vol_curr']:,}")
print(f"F30 W38: KH Mới = {f30_obj['total']['kh_curr']} shop ({f30_obj['total']['rev_curr']:,.0f} đ)")
print(f"Group A: {len(kha_shops)} shops, MTD = {tot_mtd:,.1f} Tr ₫, Latest Date = {latest_date}")
