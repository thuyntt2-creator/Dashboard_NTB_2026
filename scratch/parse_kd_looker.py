import os
import sys
import pandas as pd
import json
import re
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

downloads = r'C:\Users\lap4all\Downloads'
xl_path = os.path.join(downloads, '_NTB - BÁO CÁO TUẦN KINH DOANH (Looker).xlsx')

if not os.path.exists(xl_path):
    print(f"File not found: {xl_path}")
    sys.exit(1)

print(f"Loading {xl_path}...")

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

# Check dates in tong_quan
df_tq = pd.read_excel(xl_path, sheet_name='tong_quan')
df_tq['parsed_date'] = df_tq['Ngay'].apply(parse_date)
df_tq['dt'] = pd.to_numeric(df_tq['DoanhThu'], errors='coerce').fillna(0)
df_tq['vol'] = pd.to_numeric(df_tq['Volume'], errors='coerce').fillna(0)
df_tq['am'] = df_tq['AM_format'].astype(str).str.strip()

# Check F30
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

# Print metrics for both 20-26/9 vs 27/9-03/10 AND 21-27/9 vs 28/9-04/10
for name, (p1, p2), (c1, c2) in [
    ("Cycle 20-26/9 vs 27/9-03/10", ('2026-09-20', '2026-09-26'), ('2026-09-27', '2026-10-03')),
    ("ISO W39 vs W40 (21-27/9 vs 28/9-04/10)", ('2026-09-21', '2026-09-27'), ('2026-09-28', '2026-10-04'))
]:
    tq_p = df_tq[(df_tq['parsed_date'] >= p1) & (df_tq['parsed_date'] <= p2)]
    tq_c = df_tq[(df_tq['parsed_date'] >= c1) & (df_tq['parsed_date'] <= c2)]
    f_p = df_f30[(df_f30['parsed_date'] >= p1) & (df_f30['parsed_date'] <= p2)]
    f_c = df_f30[(df_f30['parsed_date'] >= c1) & (df_f30['parsed_date'] <= c2)]
    
    print(f"\n=== {name} ===")
    print(f"Kỳ trước ({p1} -> {p2}): DT = {tq_p['dt'].sum()/1e6:,.1f} Tr, Vol = {int(tq_p['vol'].sum()):,}, F30 = {len(f_p)} shops ({f_p['dt'].sum()/1e6:,.1f} Tr)")
    print(f"Kỳ này   ({c1} -> {c2}): DT = {tq_c['dt'].sum()/1e6:,.1f} Tr, Vol = {int(tq_c['vol'].sum()):,}, F30 = {len(f_c)} shops ({f_c['dt'].sum()/1e6:,.1f} Tr)")
    diff_dt = (tq_c['dt'].sum() - tq_p['dt'].sum()) / 1e6
    pct_dt = (tq_c['dt'].sum() - tq_p['dt'].sum()) / tq_p['dt'].sum() * 100
    diff_vol = int(tq_c['vol'].sum() - tq_p['vol'].sum())
    pct_vol = diff_vol / tq_p['vol'].sum() * 100
    print(f"Diff DT: {diff_dt:+,.1f} Tr ({pct_dt:+.1f}%), Diff Vol: {diff_vol:+,} ({pct_vol:+.1f}%)")
