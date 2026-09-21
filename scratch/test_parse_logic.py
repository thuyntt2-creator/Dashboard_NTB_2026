import pandas as pd
import numpy as np
import sys
import re
from datetime import datetime
import json
import os

sys.stdout.reconfigure(encoding='utf-8')

# Read truythu raw
df = pd.read_csv('scratch/truythu_raw.csv', low_memory=False)

def parse_ghn_date(val):
    if not val or not isinstance(val, str):
        return None
    val = val.strip()
    m = re.search(r'(\d{1,2})\s+thg\s+(\d{1,2}),?\s+(\d{4})', val)
    if m:
        d, mth, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
        return datetime(y, mth, d)
    m2 = re.search(r'(\d{4})-(\d{2})-(\d{2})', val)
    if m2:
        return datetime(int(m2.group(1)), int(m2.group(2)), int(m2.group(3)))
    m3 = re.search(r'(\d{1,2})/(\d{1,2})/(\d{4})', val)
    if m3:
        return datetime(int(m3.group(3)), int(m3.group(2)), int(m3.group(1)))
    return None

df['date'] = df['Ngày kết luận truy thu'].apply(parse_ghn_date)

# Parse numbers
def parse_vn(s):
    if pd.isnull(s):
        return 0.0
    if isinstance(s, (int, float)):
        return float(s)
    s = str(s).strip()
    try:
        # Check if contains both dot and comma
        if '.' in s and ',' in s:
            # Vietnamese format like 1.234,56
            s = s.replace('.', '').replace(',', '.')
            return float(s)
        # If multiple dots, e.g. 4.200.000
        if s.count('.') > 1:
            return float(s.replace('.', ''))
        # If single dot: is it thousands or decimal?
        # In GHN table, numbers like 32.964 are often float from excel or 32964?
        # Let's check: 32.964, 86.334, 10.313 - these look like thousands or 3 decimals from division!
        # Wait, if it came from Excel, let's check whether it's float or string
        return float(s)
    except:
        return 0.0

# But wait! Let's check how parse_vn was done in process_truy_thu_report.py:
# def parse_vn(s):
#     try:
#         return float(str(s).replace('.', '').replace(',', '.'))
#     except:
#         return 0.0
# Notice that replacing '.' with '' converts '4.200.000' -> 4200000.0, BUT '32.964' -> 32964.0!
# And 32,964 VNĐ makes total sense for a delivery fee backlog penalty! (e.g. 33k VNĐ, 86k VNĐ, 266k VNĐ)!
# In Vietnam logistics, GHN penalties are in VND! 32,964 VND is typical for backlog of 1-2 orders!
# Whereas 25 was 25 or 25,000? Wait, let's check!

print("Testing parse_vn on sample values:")
for v in ['45', '120', '32.964', '169', '25', '86.334', '266.667', '102', '4.200.000', '10.313']:
    v_clean = str(v).replace('.', '').replace(',', '.')
    print(f"{v} -> {v_clean}")
