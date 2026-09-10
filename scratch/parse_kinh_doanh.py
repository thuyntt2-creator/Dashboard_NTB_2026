import json
import re
import sys
import pandas as pd

def parse_date(d):
    m = re.search(r'(\d+)\s+thg\s+(\d+)', str(d))
    if m:
        return f"{int(m.group(1)):02d}/{int(m.group(2)):02d}"
    return str(d)

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
        "am": str(last_row.get('AM', '')).strip(),
        "buu_cuc": str(last_row.get('Bưu cục', '')).strip(),
        "daily_dt": daily_dt,
        "dt_w1": dt_w1,
        "dt_n1": dt_n1,
        "diff_w1": diff_w1,
        "pct_w1": pct_w1
    }
    shops.append(shop_item)

# Sort shops by MTD descending
shops.sort(key=lambda s: s['mtd'], reverse=True)

# 2. Inspect warning table (right side: columns 19 to 32)
warnings = []
df_warn = df.iloc[:, 19:33].copy()
# Rename columns
warn_cols = ['stt', 'makh', 'tenkh', 'nhomkh', 'vung', 'nhanvien', 'vol_dt_cam_ket', 'mtd', 'pct_mtd_m1', 'aov', 'ngaynext', 'dt', 'am', 'buu_cuc']
df_warn.columns = warn_cols[:len(df_warn.columns)]
df_warn = df_warn.dropna(subset=['makh', 'ngaynext']).copy()
for _, r in df_warn.iterrows():
    try:
        warnings.append({
            "stt": str(int(r.get('stt', 1))),
            "makh": str(int(r.get('makh', 0))),
            "tenkh": str(r.get('tenkh', '')).strip(),
            "nhomkh": str(r.get('nhomkh', '')).strip(),
            "vung": str(r.get('vung', '')).strip(),
            "nhanvien": str(int(r.get('nhanvien', 0))) if pd.notna(r.get('nhanvien')) else "",
            "cam_ket": str(r.get('vol_dt_cam_ket', '')).strip(),
            "mtd": float(str(r.get('mtd', 0)).replace(',', '').strip()) if pd.notna(r.get('mtd')) else 0.0,
            "pct_mtd_m1": str(r.get('pct_mtd_m1', '')).strip(),
            "aov": str(r.get('aov', '')).strip(),
            "ngay": parse_date(r.get('ngaynext', '')),
            "dt": float(str(r.get('dt', 0)).replace(',', '').strip()) if pd.notna(r.get('dt')) else 0.0,
            "am": str(r.get('am', '')).strip(),
            "buu_cuc": str(r.get('buu_cuc', '')).strip()
        })
    except Exception as e:
        print("Warning row parse error:", e)

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
