import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
import os
import pandas as pd

# Test reading local ops_gtc.csv and ops_ltc.csv
df_gtc = pd.read_csv('ops_gtc.csv')
df_ltc = pd.read_csv('ops_ltc.csv')

print("GTC columns:", df_gtc.columns.tolist()[:5])
print("LTC columns:", df_ltc.columns.tolist()[:5])

times_gtc = set(df_gtc['Time'].dropna().unique())
times_ltc = set(df_ltc['Time'].dropna().unique())

all_times = times_gtc.union(times_ltc)
print("Total unique times:", len(all_times))

# Sort
dates_sorted = sorted(list(all_times), key=lambda x: pd.to_datetime(str(x).split(' - ')[0]))
print("Dates sorted (last 10):", dates_sorted[-10:])
print("Latest date:", dates_sorted[-1] if dates_sorted else None)

