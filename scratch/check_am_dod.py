import pickle
import pandas as pd
import numpy as np
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open(r"c:\Users\lap4all\Desktop\New folder\scratch\raw_sheets_data.pkl", "rb") as f:
    data = pickle.load(f)

df_rpt_ngay = data['RPT_Ngày']

def parse_pct_str(s):
    if not s or str(s).strip() == '' or str(s).strip() == '—' or str(s).strip() == '-':
        return None
    m = re.search(r'([▲▼]?)\s*([\d\.]+)%', str(s))
    if m:
        sign = -1 if m.group(1) == '▼' else 1
        return sign * float(m.group(2)) / 100.0
    return None

def parse_float_val(v):
    if v is None or str(v).strip() == '' or str(v).strip() == '—' or str(v).strip() == '-':
        return 0.0
    try:
        return float(str(v).replace(',', ''))
    except:
        return 0.0

print("=== CHECKING RPT_Ngày: AM DETAILS TABLE MATH ===")
# Detailed table is from row 23 to 44 (index 22 to 43)
for idx in range(22, 44):
    row = df_rpt_ngay.iloc[idx]
    am = row[0]
    prov = row[1]
    dt_16 = parse_float_val(row[2])
    vol_16 = parse_float_val(row[3])
    dt_15 = parse_float_val(row[4])
    vol_15 = parse_float_val(row[5])
    dod_dt_rpt = parse_pct_str(row[6])
    
    if dt_15 != 0:
        dod_dt_calc = (dt_16 - dt_15) / dt_15
        diff = abs(dod_dt_calc - dod_dt_rpt) if dod_dt_rpt is not None else 0
    else:
        dod_dt_calc = 0
        diff = 0
        
    print(f"AM: {am:<35} | Tỉnh: {prov:<15} | DT 16: {dt_16:<5} | DT 15: {dt_15:<5} | DoD Rpt: {row[6]:<10} | DoD Calc: {dod_dt_calc:.1%} | Diff: {diff:.4f}")
    if diff > 0.005:
        print(f"  WARNING: DoD DT mismatch! Rpt={row[6]} vs Calc={dod_dt_calc:.1%}")
