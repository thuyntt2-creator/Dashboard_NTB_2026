import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Load vols_tao_don.csv
df = pd.read_csv("vols_tao_don.csv")
df['Date'] = pd.to_datetime(df['Date'])

# Filter for NTB region
df_ntb = df[df['Vùng'] == 'NTB'].copy()

# Look for post office matching "Phú Thủy"
phu_thuy_df = df_ntb[df_ntb['Bưu cục'].str.contains("Phú Thủy", na=False)].copy()

output = []
output.append(f"Available columns: {df.columns.tolist()}")
output.append(f"\nUnique post offices matching 'Phú Thủy':")
output.append(str(phu_thuy_df['Bưu cục'].unique()))

# Group by Date and Bưu cục to get daily volumes
daily_vols = phu_thuy_df.groupby(['Date', 'Bưu cục'])['Volume'].sum().unstack(fill_value=0)
output.append("\nDaily volumes for Phú Thủy post offices:")
output.append(daily_vols.to_string())

# Find the latest date in the entire dataset
latest_dt = df_ntb['Date'].max()
output.append(f"\nLatest date in dataset: {latest_dt.strftime('%Y-%m-%d')}")

# Calculate growth like the dashboard does
df_d = df_ntb[df_ntb['Date'] == latest_dt]
df_d7 = df_ntb[df_ntb['Date'] == (latest_dt - pd.Timedelta(days=7))]

vol_d = df_d.groupby('Bưu cục')['Volume'].sum().reset_index()
vol_d7 = df_d7.groupby('Bưu cục')['Volume'].sum().reset_index()

merged = pd.merge(vol_d, vol_d7, on='Bưu cục', suffixes=('_d', '_d7'), how='left').fillna(0)
merged['growth_abs'] = merged['Volume_d'] - merged['Volume_d7']

output.append("\nComputed growth (D vs D-7) for Phú Thủy:")
output.append(merged[merged['Bưu cục'].str.contains("Phú Thủy", na=False)].to_string())

# Print to console (using utf-8 stdout)
result_text = "\n".join(output)
print(result_text)

# Also write to a file
with open("scratch/phu_thuy_vols.txt", "w", encoding="utf-8") as f:
    f.write(result_text)
