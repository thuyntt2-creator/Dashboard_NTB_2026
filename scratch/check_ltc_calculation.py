import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import pandas as pd
from app import get_dataframes

# Load dataframes
df_gtc, df_ltc, df_aging, df_treo = get_dataframes(force=True)

# Filter for latest date
latest_date = df_ltc['Time'].dropna().unique()[-1]
df_ltc_latest = df_ltc[df_ltc['Time'] == latest_date]

print("Latest Date:", latest_date)
print("Number of rows:", len(df_ltc_latest))
print("Sum of Volume:", df_ltc_latest['Volume'].sum())
print("Sum of ltc_vol:", df_ltc_latest['ltc_vol'].sum())

# Print first 10 rows
print("\nFirst 10 rows:")
print(df_ltc_latest[['Cấp quản lý', 'Chi tiết', 'Volume', '%LTC', 'ltc_vol']].head(10).to_string())
