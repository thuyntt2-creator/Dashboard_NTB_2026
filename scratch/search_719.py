import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_csv("vols_tao_don.csv")
df['Date'] = pd.to_datetime(df['Date'])

df_ntb = df[df['Vùng'] == 'NTB'].copy()

# Let's test WTD vs WTD1 for each post office
# WTD: Monday to Tuesday of current week (since latest_dt is 2026-07-14, which is Tuesday. Wait! let's check what weekday 2026-07-14 is)
# Tuesday: 2026-07-14.
# Weekday is 1 (Monday is 0, Tuesday is 1).
# So WTD is Monday 2026-07-13 to Tuesday 2026-07-14.
# WTD1 is Monday 2026-07-06 to Tuesday 2026-07-07.

latest_dt = df_ntb['Date'].max()
weekday = latest_dt.weekday()
wtd_start = latest_dt - pd.Timedelta(days=weekday)
wtd_end = latest_dt

wtd1_start = wtd_start - pd.Timedelta(days=7)
wtd1_end = latest_dt - pd.Timedelta(days=7)

print(f"Latest Date: {latest_dt.strftime('%Y-%m-%d')} (Weekday: {weekday})")
print(f"WTD: {wtd_start.strftime('%Y-%m-%d')} to {wtd_end.strftime('%Y-%m-%d')}")
print(f"WTD1: {wtd1_start.strftime('%Y-%m-%d')} to {wtd1_end.strftime('%Y-%m-%d')}")

# Sum for WTD
df_wtd = df_ntb[(df_ntb['Date'] >= wtd_start) & (df_ntb['Date'] <= wtd_end)]
wtd_sum = df_wtd.groupby('Bưu cục')['Volume'].sum()

# Sum for WTD1
df_wtd1 = df_ntb[(df_ntb['Date'] >= wtd1_start) & (df_ntb['Date'] <= wtd1_end)]
wtd1_sum = df_wtd1.groupby('Bưu cục')['Volume'].sum()

merged = pd.DataFrame({
    'WTD': wtd_sum,
    'WTD1': wtd1_sum
}).fillna(0)

merged['growth'] = merged['WTD'] - merged['WTD1']
merged = merged.sort_values(by='growth', ascending=False)

print("\n=== Top 10 growth by WTD vs WTD1 ===")
print(merged.head(10))

# What about 7-day total vs previous 7-day total?
# Last 7 days: 2026-07-08 to 2026-07-14
# Previous 7 days: 2026-07-01 to 2026-07-07
d7_start = latest_dt - pd.Timedelta(days=6)
d14_start = latest_dt - pd.Timedelta(days=13)

df_last7 = df_ntb[(df_ntb['Date'] >= d7_start) & (df_ntb['Date'] <= latest_dt)]
df_prev7 = df_ntb[(df_ntb['Date'] >= d14_start) & (df_ntb['Date'] < d7_start)]

last7_sum = df_last7.groupby('Bưu cục')['Volume'].sum()
prev7_sum = df_prev7.groupby('Bưu cục')['Volume'].sum()

merged7 = pd.DataFrame({
    'Last7': last7_sum,
    'Prev7': prev7_sum
}).fillna(0)

merged7['growth'] = merged7['Last7'] - merged7['Prev7']
merged7 = merged7.sort_values(by='growth', ascending=False)

print("\n=== Top 10 growth by Last 7 Days vs Prev 7 Days ===")
print(merged7.head(10))
