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
    if not s or str(s).strip() == '' or str(s).strip() == '—':
        return None
    # e.g., "▼ 42.2%" or "▲ 10.2%"
    # extract float
    m = re.search(r'([▲▼]?)\s*([\d\.]+)%', str(s))
    if m:
        sign = -1 if m.group(1) == '▼' else 1
        return sign * float(m.group(2)) / 100.0
    return None

def parse_float_val(v):
    if v is None or str(v).strip() == '' or str(v).strip() == '—':
        return 0.0
    try:
        return float(str(v).replace(',', ''))
    except:
        return 0.0

# 1. Check Revenue table (rows 3 to 9 in 0-indexed DataFrame, i.e., Khánh Hòa to TỔNG VÙNG NTB)
print("=== CHECKING RPT_Ngày: REVENUE MATH ===")
for idx in range(4, 10): # rows 4 to 9 are 0-indexed rows (Khánh Hòa is row 4, TỔNG is row 9)
    row = df_rpt_ngay.iloc[idx]
    tinh = row[0]
    d = parse_float_val(row[1])
    d1 = parse_float_val(row[2])
    dod_d1_rpt = parse_pct_str(row[3])
    d7 = parse_float_val(row[4])
    dod_d7_rpt = parse_pct_str(row[5])
    
    # Calculate DoD vs D-1
    if d1 != 0:
        dod_d1_calc = (d - d1) / d1
        diff_d1 = abs(dod_d1_calc - dod_d1_rpt) if dod_d1_rpt is not None else 0
    else:
        dod_d1_calc = 0
        diff_d1 = 0
        
    # Calculate DoD vs D-7
    if d7 != 0:
        dod_d7_calc = (d - d7) / d7
        diff_d7 = abs(dod_d7_calc - dod_d7_rpt) if dod_d7_rpt is not None else 0
    else:
        dod_d7_calc = 0
        diff_d7 = 0
        
    print(f"Tỉnh: {tinh}")
    print(f"  DoD vs D-1: Rpt={row[3]} | Calc={dod_d1_calc:.1%} | Diff={diff_d1:.4f}")
    if diff_d1 > 0.005:
        print(f"    WARNING: DoD vs D-1 mismatch! {row[3]} vs {dod_d1_calc:.1%}")
    print(f"  DoD vs D-7: Rpt={row[5]} | Calc={dod_d7_calc:.1%} | Diff={diff_d7:.4f}")
    if diff_d7 > 0.005:
        print(f"    WARNING: DoD vs D-7 mismatch! {row[5]} vs {dod_d7_calc:.1%}")

# 2. Check Volume table (rows 13 to 19 in 0-indexed DataFrame, i.e., Khánh Hòa to TỔNG VÙNG NTB)
print("\n=== CHECKING RPT_Ngày: VOLUME MATH ===")
for idx in range(13, 20):
    row = df_rpt_ngay.iloc[idx]
    tinh = row[0]
    d = parse_float_val(row[1])
    d1 = parse_float_val(row[2])
    dod_d1_rpt = parse_pct_str(row[3])
    d7 = parse_float_val(row[4])
    dod_d7_rpt = parse_pct_str(row[5])
    
    # Calculate DoD vs D-1
    if d1 != 0:
        dod_d1_calc = (d - d1) / d1
        diff_d1 = abs(dod_d1_calc - dod_d1_rpt) if dod_d1_rpt is not None else 0
    else:
        dod_d1_calc = 0
        diff_d1 = 0
        
    # Calculate DoD vs D-7
    if d7 != 0:
        dod_d7_calc = (d - d7) / d7
        diff_d7 = abs(dod_d7_calc - dod_d7_rpt) if dod_d7_rpt is not None else 0
    else:
        dod_d7_calc = 0
        diff_d7 = 0
        
    print(f"Tỉnh: {tinh}")
    print(f"  DoD vs D-1: Rpt={row[3]} | Calc={dod_d1_calc:.1%} | Diff={diff_d1:.4f}")
    if diff_d1 > 0.005:
        print(f"    WARNING: DoD vs D-1 mismatch! {row[3]} vs {dod_d1_calc:.1%}")
    print(f"  DoD vs D-7: Rpt={row[5]} | Calc={dod_d7_calc:.1%} | Diff={diff_d7:.4f}")
    if diff_d7 > 0.005:
        print(f"    WARNING: DoD vs D-7 mismatch! {row[5]} vs {dod_d7_calc:.1%}")
