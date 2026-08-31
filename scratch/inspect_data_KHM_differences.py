import pickle
import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r"c:\Users\lap4all\Desktop\New folder\scratch\raw_sheets_data.pkl", "rb") as f:
    data = pickle.load(f)

df_khm_new = data['khách hàng mơi'].copy()
df_khm_data = data['dataKHM'].copy()

print(f"khách hàng mơi dimensions: {df_khm_new.shape}")
print(f"dataKHM dimensions: {df_khm_data.shape}")

# Parse Vietnamese months in date strings to Timestamp
def parse_vn_date(d_str):
    if not d_str or str(d_str).strip() == '':
        return None
    d_str = str(d_str).strip()
    parts = d_str.split('thg')
    if len(parts) == 2:
        day = int(parts[0].strip())
        sub_parts = parts[1].split(',')
        month = int(sub_parts[0].strip())
        year = int(sub_parts[1].strip())
        return pd.Timestamp(year=year, month=month, day=day)
    return None

df_khm_new['Timestamp'] = df_khm_new['Ngày LTC đầu tiên'].apply(parse_vn_date)
df_khm_data['Timestamp'] = df_khm_data['Ngày LTC đầu tiên'].apply(parse_vn_date)

df_khm_new['Volume'] = pd.to_numeric(df_khm_new['Volume'], errors='coerce').fillna(0)
df_khm_data['Volume'] = pd.to_numeric(df_khm_data['Volume'], errors='coerce').fillna(0)

# Group by date for June 16, 2026
print("\n=== Sum of Volume for 16/06/2026 ===")
print("khách hàng mơi:", df_khm_new[df_khm_new['Ngày LTC đầu tiên'] == '16 thg 6, 2026']['Volume'].sum())
print("dataKHM:", df_khm_data[df_khm_data['Ngày LTC đầu tiên'] == '16 thg 6, 2026']['Volume'].sum())

print("\n=== Sum of Volume for 15/06/2026 ===")
print("khách hàng mơi:", df_khm_new[df_khm_new['Ngày LTC đầu tiên'] == '15 thg 6, 2026']['Volume'].sum())
print("dataKHM:", df_khm_data[df_khm_data['Ngày LTC đầu tiên'] == '15 thg 6, 2026']['Volume'].sum())

print("\n=== Sum of Volume for June MTD (1-16) ===")
print("khách hàng mơi:", df_khm_new[(df_khm_new['Timestamp'] >= '2026-06-01') & (df_khm_new['Timestamp'] <= '2026-06-16')]['Volume'].sum())
print("dataKHM:", df_khm_data[(df_khm_data['Timestamp'] >= '2026-06-01') & (df_khm_data['Timestamp'] <= '2026-06-16')]['Volume'].sum())
