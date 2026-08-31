import pickle
import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r"c:\Users\lap4all\Desktop\New folder\scratch\raw_sheets_data.pkl", "rb") as f:
    data = pickle.load(f)

# Inspect "data theo tuần" (which seems to contain daily data)
print("=== data theo tuần ===")
df_week = data['data theo tuần']
print("Data type of Ngay:", df_week['Ngay'].dtype)
print("Unique Ngay values (first 20):", df_week['Ngay'].unique()[:20])
# Check if there are records for June 2026
june_records_week = df_week[df_week['Ngay'].astype(str).str.contains('thg 6, 2026')]
print("Number of June 2026 records in data theo tuần:", len(june_records_week))
if len(june_records_week) > 0:
    print("Unique June 2026 dates in data theo tuần:", june_records_week['Ngay'].unique())

# Inspect "datatheo ngày"
print("\n=== datatheo ngày ===")
df_day = data['datatheo ngày']
print("Data type of Tuan:", df_day['Tuan'].dtype)
print("Unique Tuan values (first 20):", df_day['Tuan'].unique()[:20])

# Inspect "data theo tháng"
print("\n=== data theo tháng ===")
df_month = data['data theo tháng']
print("Data type of Thang:", df_month['Thang'].dtype)
print("Unique Thang values (first 20):", df_month['Thang'].unique()[:20])

# Inspect "dataKHM"
print("\n=== dataKHM ===")
df_khm = data['dataKHM']
print("Unique dates in dataKHM (first 20):", df_khm['Ngày LTC đầu tiên'].unique()[:20])

# Let's see if we can convert Excel serial number to date
# Some serial numbers like 46082 are around year 2026.
# Let's check what date 46082 is in excel (46082 = 2026-02-28?)
# 46082 - 2 = 46080 days from 1900-01-01?
# Let's print out what 46082 corresponds to if we parse it.
print("Excel serial 46082 to datetime:")
print(pd.to_datetime(46082, unit='D', origin='1899-12-30'))
print("Excel serial 46113 to datetime:")
print(pd.to_datetime(46113, unit='D', origin='1899-12-30'))

# Let's print unique dates in df_day after converting Tuan column (if numeric)
df_day_numeric = df_day[pd.to_numeric(df_day['Tuan'], errors='coerce').notna()].copy()
df_day_numeric['Date'] = pd.to_datetime(df_day_numeric['Tuan'].astype(float), unit='D', origin='1899-12-30')
print("Unique dates in datatheo ngày (first 20):")
print(df_day_numeric['Date'].dt.strftime('%Y-%m-%d').unique()[:20])

# Let's also check dates in data theo tháng if they are serial numbers
df_month_numeric = df_month[pd.to_numeric(df_month['Thang'], errors='coerce').notna()].copy()
df_month_numeric['Date'] = pd.to_datetime(df_month_numeric['Thang'].astype(float), unit='D', origin='1899-12-30')
print("Unique dates in data theo tháng (first 20):")
print(df_month_numeric['Date'].dt.strftime('%Y-%m-%d').unique()[:20])
