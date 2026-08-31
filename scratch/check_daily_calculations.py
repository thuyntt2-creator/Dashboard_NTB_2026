import pickle
import pandas as pd
import numpy as np
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r"c:\Users\lap4all\Desktop\New folder\scratch\raw_sheets_data.pkl", "rb") as f:
    data = pickle.load(f)

df_rpt_ngay = data['RPT_Ngày']
df_raw = data['data theo tuần'].copy()

# Parse Vietnamese numbers
def parse_val(val):
    if val is None or val == '' or val == '—':
        return 0.0
    val_str = str(val).strip()
    # Check if it has dots as thousands separator (e.g. 87.499.268)
    # If there are multiple dots, it's definitely thousands separator.
    # If there is one dot, it could be decimal or thousands. Let's see:
    # If it is like '2.295' and it's volume, it represents 2295.
    # Let's count dots.
    dots = val_str.count('.')
    commas = val_str.count(',')
    if dots > 0 and commas == 0:
        # If it matches something like 2.295 (volume) or 87.499.268 (revenue)
        # let's remove dots.
        # But wait! If it is a decimal in the report, like '101.9' million VND, that is a python float.
        # But here we are parsing the raw data. In raw data, are they integers?
        # Let's inspect the raw values of DoanhThu and Volume to see.
        return float(val_str.replace('.', ''))
    elif commas > 0:
        return float(val_str.replace('.', '').replace(',', '.'))
    try:
        return float(val_str)
    except:
        return 0.0

# Apply parsing
df_raw['DT_clean'] = df_raw['DoanhThu'].apply(parse_val)
df_raw['Vol_clean'] = df_raw['Volume'].apply(parse_val)

# Let's extract AM mapping from RPT_Ngày detailed table
# Rows 23 to 44 in our preview corresponds to indices 22 to 43 (0-indexed)
am_mapping = {}
print("=== AM Mapping in RPT_Ngày ===")
for idx in range(22, 44):
    row = df_rpt_ngay.iloc[idx]
    am_name = str(row[0]).strip()
    province = str(row[1]).strip()
    am_mapping[am_name] = province
    print(f"'{am_name}' -> '{province}'")

# Let's write a function to map raw AM names to clean names
def clean_raw_am(raw_am):
    if not raw_am or raw_am == '-':
        return ""
    parts = str(raw_am).split('-')
    if len(parts) > 1:
        return parts[1].strip()
    return str(raw_am).strip()

df_raw['AM_clean'] = df_raw['AM'].apply(clean_raw_am)

# Check if there are any AMs in raw data that are not in our mapping
unmapped_ams = set()
for raw_am in df_raw['AM'].unique():
    clean_name = clean_raw_am(raw_am)
    if clean_name and clean_name not in am_mapping:
        unmapped_ams.add(clean_name)
print("\nAMs in raw data not in RPT_Ngày AM details table:", unmapped_ams)

# Group raw data by clean AM and date
df_raw_grouped = df_raw.groupby(['AM_clean', 'Ngay']).agg(
    dt_vnd=('DT_clean', 'sum'),
    vol=('Vol_clean', 'sum')
).reset_index()

df_raw_grouped['dt_tr'] = df_raw_grouped['dt_vnd'] / 1000000.0

# Let's check for specific dates: '16 thg 6, 2026', '15 thg 6, 2026', '9 thg 6, 2026'
target_dates = ['16 thg 6, 2026', '15 thg 6, 2026', '9 thg 6, 2026']

print("\n=== Calculations Check for 16/06/2026 ===")
for dt in target_dates:
    print(f"\n--- DATE: {dt} ---")
    sub = df_raw_grouped[df_raw_grouped['Ngay'] == dt]
    for idx, r in sub.iterrows():
        print(f"AM: '{r['AM_clean']}' | Revenue={r['dt_tr']:.2f}M | Vol={r['vol']:.0f}")
