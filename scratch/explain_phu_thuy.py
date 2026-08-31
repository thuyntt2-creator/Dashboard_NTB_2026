import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Read the live sheet we just downloaded
df = pd.read_excel("scratch/vols_tao_don_live.xlsx", sheet_name="shopee_tiktok")
df.columns = [str(c).strip() for c in df.columns]
df['Date'] = pd.to_datetime(df['Date'])

# Filter bat_on (excluding 'BC Cũ/Không thuộc ĐCL')
df_filtered = df[df['bat_on'].fillna('').str.strip() != 'BC Cũ/Không thuộc ĐCL'].copy()

# Look at (BTH) Phú Thủy on 2026-07-16 and 2026-07-09
pt_d = df_filtered[(df_filtered['Bưu cục'] == '(BTH) Phú Thủy') & (df_filtered['Date'] == '2026-07-16')]
pt_d7 = df_filtered[(df_filtered['Bưu cục'] == '(BTH) Phú Thủy') & (df_filtered['Date'] == '2026-07-09')]

print("=== Detail for (BTH) Phú Thủy on 2026-07-16 (Latest Day D) ===")
print(pt_d[['Date', 'Bưu cục', 'Khách hàng', 'Volume']])
print("Sum of Volume for 2026-07-16:", pt_d['Volume'].sum())

print("\n=== Detail for (BTH) Phú Thủy on 2026-07-09 (Day D - 7) ===")
print(pt_d7[['Date', 'Bưu cục', 'Khách hàng', 'Volume']])
print("Sum of Volume for 2026-07-09:", pt_d7['Volume'].sum())

# Let's check if there are float volumes in the original sheet
pt_d_raw = df[(df['Bưu cục'] == '(BTH) Phú Thủy') & (df['Date'] == '2026-07-16')]
pt_d7_raw = df[(df['Bưu cục'] == '(BTH) Phú Thủy') & (df['Date'] == '2026-07-09')]
print("\nSum of raw Volume (without bat_on filter):")
print("  2026-07-16:", pt_d_raw['Volume'].sum())
print("  2026-07-09:", pt_d7_raw['Volume'].sum())
