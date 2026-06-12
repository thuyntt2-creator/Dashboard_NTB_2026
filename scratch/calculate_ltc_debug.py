import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import pandas as pd
import numpy as np

# Load function from app.py
from app import get_dataframes, process_operational_report, safe_read_csv, resolve_path, clean_ops_df, normalize_pct_col

df_ltc_raw = pd.read_csv('ops_ltc.csv')
print("Raw columns:", df_ltc_raw.columns.tolist())

# Check a single row
row0 = df_ltc_raw.iloc[0]
print("\nFirst row values:")
for col in df_ltc_raw.columns:
    print(f"  {col}: {row0[col]} (type: {type(row0[col])})")

# Run clean_ops_df
df_ltc_clean = clean_ops_df(df_ltc_raw, "ltc")
print("\nAfter clean_ops_df:")
print("  Volume type:", df_ltc_clean['Volume'].dtype)
print("  Volume values (first 5):", df_ltc_clean['Volume'].head(5).tolist())

# Run conversions in get_dataframes
df_ltc = df_ltc_clean[df_ltc_clean['Cấp quản lý'] != 'Grand Total'].dropna(subset=["Volume"]).copy()
print("\nAfter dropna and Grand Total filter:")
print("  Shape:", df_ltc.shape)
print("  Volume values (first 5):", df_ltc['Volume'].head(5).tolist())

# Convert Volume
# Note: we need to see how app.py currently converts Volume
# In app.py line 2121:
# df_ltc = raw_ltc[raw_ltc['Cấp quản lý'] != 'Grand Total'].dropna(subset=["Volume"]).copy()
# df_ltc['Leadtime'] = pd.to_numeric(df_ltc['Leadtime'], errors='coerce')
# Then at line 2235:
# df_ltc['Volume'] = pd.to_numeric(df_ltc['Volume'], errors='coerce').fillna(0)

# Let's see how app.py actually behaves
df_ltc_cache, _, _, _, _, _ = get_dataframes(force=True)
print("\nCaches loaded via get_dataframes(force=True)")
print("DF_LTC_CACHE shape:", df_ltc_cache.shape if df_ltc_cache is not None else "None")
if df_ltc_cache is not None:
    print("Columns:", df_ltc_cache.columns.tolist())
    print("First 3 rows of LTC Cache:")
    print(df_ltc_cache[['Chi tiết', 'Time', 'Volume', '%LTC', 'ltc_vol']].head(3).to_string())
    
    # Let's see overall LTC calculation
    latest_date = df_ltc_cache['Time'].dropna().unique()[-1]
    df_latest = df_ltc_cache[df_ltc_cache['Time'] == latest_date]
    print(f"\nLatest date: {latest_date}")
    print("Total volume:", df_latest['Volume'].sum())
    print("Total ltc_vol:", df_latest['ltc_vol'].sum())
    print("Overall LTC (%):", (df_latest['ltc_vol'].sum() / df_latest['Volume'].sum()) * 100 if df_latest['Volume'].sum() > 0 else 0)
