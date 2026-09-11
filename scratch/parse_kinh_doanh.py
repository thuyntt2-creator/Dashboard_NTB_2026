import json
import re
import sys
import pandas as pd

def parse_date(d):
    m = re.search(r'(\d+)\s+thg\s+(\d+)', str(d))
    if m:
        return f"{int(m.group(1)):02d}/{int(m.group(2)):02d}"
    return str(d)

SHOP_META_MAP = {
    "3910354": {"am": "Phan Đình Duy", "buu_cuc": "20495000 - (KHO) Nha Trang"},
    "5099749": {"am": "Thái Thị Thanh Thư", "buu_cuc": "22363000 - (KHO) Nam Nha Trang 3"},
    "4264387": {"am": "Huỳnh Thúc Duân", "buu_cuc": "22242000 - (DNO) Bắc Gia Nghĩa"},
    "5109892": {"am": "Lê Văn Trường", "buu_cuc": "22116000 - (LDO) Xuân Trường - Đà Lạt"},
    "3200594": {"am": "Lê Thanh Nhựt", "buu_cuc": "2357 - (BTH) Đồng Kho"},
    "3559462": {"am": "Nguyễn Lê Nguyên Vũ", "buu_cuc": "20663000 - (LDO) Đạ Tẻh"},
    "5197975": {"am": "Nguyễn Duy Long", "buu_cuc": "20499000 - (NTH) Phước Dinh"},
    "3950975": {"am": "Phan Đình Duy", "buu_cuc": "21046000 - (KHO) Vạn Ninh"},
    "4313038": {"am": "Hồng Bích Nga", "buu_cuc": "20785000 - (LDO) B'Lao"}
}

df = pd.read_csv('scratch/kinh_doanh_raw.csv')

# 1. Inspect main table (left side: columns 0 to 16)
df_main = df.iloc[:, 0:17].dropna(subset=['MaKH', 'Ngay']).copy()
df_main['date_clean'] = df_main['Ngay'].apply(parse_date)
df_main['DT'] = pd.to_numeric(df_main['DT'].astype(str).str.replace(',', '').str.strip(), errors='coerce').fillna(0)

all_dates = sorted(df_main['date_clean'].unique().tolist(), key=lambda x: (int(x.split('/')[1]), int(x.split('/')[0])))
print("All dates in Kinh Doanh:", all_dates)

latest_date = all_dates[-1] # '09/09'
# w1 date: 7 days before latest date, e.g. 02/09
day_num = int(latest_date.split('/')[0])
month_num = int(latest_date.split('/')[1])
w1_day = day_num - 7
w1_date = f"{w1_day:02d}/{month_num:02d}"
if w1_date not in all_dates:
    w1_date = all_dates[0]
print(f"Latest date: {latest_date}, W-1 date: {w1_date}")

# Group by shop
shops = []
shop_order = []
for makh, g in df_main.groupby('MaKH', sort=False):
    # Sort g by date
    g = g.sort_values('date_clean', key=lambda s: s.map(lambda x: (int(x.split('/')[1]), int(x.split('/')[0]))))
    last_row = g.iloc[-1]
    
    daily_dt = {}
    for _, r in g.iterrows():
        daily_dt[r['date_clean']] = float(r['DT'])
    
    # Fill missing dates with 0
    for d in all_dates:
        if d not in daily_dt:
            daily_dt[d] = 0.0
            
    dt_n1 = daily_dt.get(latest_date, 0.0)
    dt_w1 = daily_dt.get(w1_date, 0.0)
    diff_w1 = round(dt_n1 - dt_w1, 1)
    pct_w1 = round((diff_w1 / dt_w1) * 100, 1) if dt_w1 > 0 else (100.0 if dt_n1 > 0 else 0.0)
    
    # Clean numeric fields
    mtd_val = float(str(last_row.get('MTD', 0)).replace(',', '').strip())
    
    # Tinh: extract from Vung or use default
    vung = str(last_row.get('Vung', ''))
    tinh = vung.split('-')[-1].strip() if '-' in vung else vung
    
    shop_item = {
        "stt": str(int(last_row.get('STT', 0))),
        "makh": str(int(last_row.get('MaKH', 0))),
        "tenkh": str(last_row.get('TenKH', '')).strip(),
        "nhom_n": str(last_row.get('Nhom_N', '')).strip(),
        "nhomkh_1": str(last_row.get('NhomKH_1', '')).strip(),
        "ph_prev": str(last_row.get('PH_N-1', '')).strip(),
        "vung": vung,
        "tinh": tinh,
        "nhanvien": str(int(last_row.get('Nhanvien', 0))) if pd.notna(last_row.get('Nhanvien')) else "",
        "vol_cam_ket": str(last_row.get('Volume cam kết', '')).strip(),
        "aov": str(last_row.get('AOV', '')).strip(),
        "mtd": mtd_val,
        "pct_mtd_m1": str(last_row.get('% sv MTD M-1', '')).strip(),
        "pct_tru_hang": str(last_row.get('%Trụ hạng', '')).strip(),
        "am": str(last_row.get('AM', '')).strip() or SHOP_META_MAP.get(str(int(last_row.get('MaKH', 0))), {}).get('am', ''),
        "buu_cuc": str(last_row.get('Bưu cục', '')).strip() or SHOP_META_MAP.get(str(int(last_row.get('MaKH', 0))), {}).get('buu_cuc', ''),
        "daily_dt": daily_dt,
        "dt_w1": dt_w1,
        "dt_n1": dt_n1,
        "diff_w1": diff_w1,
        "pct_w1": pct_w1
    }
    shops.append(shop_item)

# Sort shops by MTD descending
shops.sort(key=lambda s: s['mtd'], reverse=True)

# 2. Inspect warning table (consolidate to 1 row per shop)
warn_makhs = []
if len(df.columns) > 19:
    df_warn = df.iloc[:, 19:33].copy()
    warn_cols = ['stt', 'makh', 'tenkh', 'nhomkh', 'vung', 'nhanvien', 'vol_dt_cam_ket', 'mtd', 'pct_mtd_m1', 'aov', 'ngaynext', 'dt', 'am', 'buu_cuc']
    df_warn.columns = warn_cols[:len(df_warn.columns)]
    for val in df_warn['makh'].dropna().unique():
        try:
            warn_makhs.append(str(int(val)))
        except Exception:
            pass

candidate_shops = []
for s in shops:
    m_id = s['makh']
    is_in_warn_table = m_id in warn_makhs
    tru_hang_val = float(str(s.get('pct_tru_hang', 0)).replace('%', '').strip() or 0)
    is_dropping = (s.get('diff_w1', 0) < 0 and s.get('pct_w1', 0) <= -20) or tru_hang_val < 25
    if is_in_warn_table or is_dropping:
        candidate_shops.append(s)

# Sort by diff_w1 ascending (biggest drop first)
candidate_shops.sort(key=lambda s: s.get('diff_w1', 0))

warnings = []
for idx, s in enumerate(candidate_shops):
    m_id = s['makh']
    tru_hang_val = float(str(s.get('pct_tru_hang', 0)).replace('%', '').strip() or 0)
    reasons = []
    if s.get('diff_w1', 0) < 0:
        reasons.append(f"▼ Giảm {abs(s['pct_w1'])}% sv W-1 ({s['diff_w1']} Tr)")
    if tru_hang_val < 25:
        reasons.append(f"Nguy cơ rớt hạng (Trụ hạng {s['pct_tru_hang']})")
    elif s.get('pct_mtd_m1') and float(str(s['pct_mtd_m1']).replace('%', '').strip() or 100) < 60:
        reasons.append(f"MTD thấp ({s['pct_mtd_m1']} sv M-1)")
    
    canh_bao_str = " | ".join(reasons) if reasons else "Cần AM theo dõi sát"
    
    warnings.append({
        "stt": str(idx + 1),
        "makh": m_id,
        "tenkh": s['tenkh'],
        "nhomkh": s['nhom_n'],
        "vung": s.get('vung', ''),
        "nhanvien": s.get('nhanvien', ''),
        "cam_ket": s.get('vol_cam_ket', ''),
        "mtd": s['mtd'],
        "pct_mtd_m1": s['pct_mtd_m1'],
        "pct_tru_hang": s['pct_tru_hang'],
        "aov": s.get('aov', ''),
        "ngay": latest_date,
        "dt": s['dt_n1'],
        "dt_n1": s['dt_n1'],
        "dt_w1": s['dt_w1'],
        "diff_w1": s['diff_w1'],
        "pct_w1": s['pct_w1'],
        "am": s['am'],
        "buu_cuc": s['buu_cuc'],
        "canh_bao": canh_bao_str
    })

# 3. AM chart aggregation (Sum of MTD by AM)
am_totals = {}
for s in shops:
    am_totals[s['am']] = am_totals.get(s['am'], 0.0) + s['mtd']
total_mtd_all = sum(am_totals.values())
am_chart = []
for am, mtd_am in sorted(am_totals.items(), key=lambda x: x[1], reverse=True):
    am_chart.append({
        "am": am,
        "mtd": round(mtd_am, 1),
        "pct": round((mtd_am / total_mtd_all) * 100, 1) if total_mtd_all > 0 else 0.0
    })

# 4. Daily trend (Sum of daily DT for all shops by date)
daily_trend = []
for d in all_dates:
    sum_d = sum(s['daily_dt'].get(d, 0.0) for s in shops)
    daily_trend.append({
        "date": d,
        "dt": round(sum_d, 1)
    })

result = {
    "dates": all_dates,
    "shops": shops,
    "warning": warnings,
    "am_chart": am_chart,
    "daily_trend": daily_trend
}

with open('scratch/khach_hang_a.json', 'w', encoding='utf-8') as f_out:
    json.dump(result, f_out, ensure_ascii=False, indent=2)

print("Saved scratch/khach_hang_a.json successfully!")
print(f"Dates: {result['dates']}")
print(f"Total shops: {len(result['shops'])}")
print(f"Total warnings: {len(result['warning'])}")
print("Daily trend:", result['daily_trend'])
