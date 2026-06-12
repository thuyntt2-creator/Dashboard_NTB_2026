import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pandas as pd
from dotenv import load_dotenv
load_dotenv(override=True)
from app import get_dataframes, process_operational_report

# 1. Load dataframes from cache/DB
df_gtc, df_ltc, df_aging, df_treo = get_dataframes(force=True)

# 2. Get latest date in df_ltc
latest_date = df_ltc['Time'].dropna().unique()[-1]
df_ltc_latest = df_ltc[df_ltc['Time'] == latest_date]

print("Latest Date in DB/Cache:", latest_date)
print("Total rows:", len(df_ltc_latest))
print("Sum of Volume:", df_ltc_latest['Volume'].sum())
print("Sum of ltc_vol:", df_ltc_latest['ltc_vol'].sum())
if 'Sản Lượng Lấy Thành Công' in df_ltc_latest.columns:
    print("Sum of Sản Lượng Lấy Thành Công:", df_ltc_latest['Sản Lượng Lấy Thành Công'].sum())
else:
    print("Sản Lượng Lấy Thành Công column not found!")

# Calculate overall LTC rate using different formulas
overall_ltc_formula_1 = (df_ltc_latest['ltc_vol'].sum() / df_ltc_latest['Volume'].sum()) * 100
print("overall_ltc (ltc_vol / Volume) * 100:", overall_ltc_formula_1)

# Check the actual values in the original CSV file for the latest date
csv_path = 'ops_ltc.csv'
if os.path.exists(csv_path):
    df_raw_csv = pd.read_csv(csv_path)
    # Filter for the same latest date
    df_raw_latest = df_raw_csv[df_raw_csv['Time'] == latest_date]
    print("\n--- Raw CSV Info ---")
    print("Latest Date in CSV:", latest_date)
    print("Total rows in CSV:", len(df_raw_latest))
    grand_total_row = df_raw_latest[df_raw_latest['Cấp quản lý'] == 'Grand Total']
    if not grand_total_row.empty:
        print("Grand Total row values:")
        for col in grand_total_row.columns:
            val = grand_total_row[col].values[0]
            if pd.notnull(val):
                print(f"  {col}: {val}")
    else:
        print("No Grand Total row found in CSV for this date!")
