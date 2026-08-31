import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_csv("vols_tao_don.csv")
df['Date'] = pd.to_datetime(df['Date'])

# Filter for (BTH) Phú Thủy
df_pt = df[df['Bưu cục'] == '(BTH) Phú Thủy'].copy()

# Print details of Volume on 2026-07-14
pt_latest = df_pt[df_pt['Date'] == '2026-07-14']
print("=== Details for (BTH) Phú Thủy on 2026-07-14 ===")
print(pt_latest[['Date', 'Khách hàng', 'Volume', 'warehouse_id']])
print("Total Volume on 2026-07-14:", pt_latest['Volume'].sum())

# Print details of Volume on 2026-07-07
pt_d7 = df_pt[df_pt['Date'] == '2026-07-07']
print("\n=== Details for (BTH) Phú Thủy on 2026-07-07 ===")
print(pt_d7[['Date', 'Khách hàng', 'Volume', 'warehouse_id']])
print("Total Volume on 2026-07-07:", pt_d7['Volume'].sum())

# Let's search if there are other dates where the calculation of 719 might apply
# E.g. maybe the latest date is not 2026-07-14 for some other filters?
# Or maybe the formula is comparing different dates?
# Let's find all pairs of (Date, Date - 7) where volume difference is 719 or close to 719
dates = sorted(df_pt['Date'].unique())
print("\n=== Difference between Date and Date - 7 for (BTH) Phú Thủy ===")
for d in dates:
    d7 = d - pd.Timedelta(days=7)
    if d7 in dates:
        vol_d = df_pt[df_pt['Date'] == d]['Volume'].sum()
        vol_d7 = df_pt[df_pt['Date'] == d7]['Volume'].sum()
        diff = vol_d - vol_d7
        print(f"{d7.strftime('%Y-%m-%d')} ({int(vol_d7)}) -> {d.strftime('%Y-%m-%d')} ({int(vol_d)}) | Diff: {int(diff)}")
