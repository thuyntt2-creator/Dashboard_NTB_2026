import pickle
import pandas as pd
import numpy as np
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r"c:\Users\lap4all\Desktop\New folder\scratch\raw_sheets_data.pkl", "rb") as f:
    data = pickle.load(f)

# Inspect RPT_Ngày
print("=== RPT_Ngày Structure ===")
df_rpt_ngay = data['RPT_Ngày']
print(df_rpt_ngay.head(15))

# Inspect RPT_Tuần
print("\n=== RPT_Tuần Structure ===")
df_rpt_tuan = data['RPT_Tuần']
print(df_rpt_tuan.head(15))

# Inspect RPT_Tháng
print("\n=== RPT_Tháng Structure ===")
df_rpt_thang = data['RPT_Tháng']
print(df_rpt_thang.head(15))

# Inspect RPT_KHM
print("\n=== RPT_KHM Structure ===")
df_rpt_khm = data['RPT_KHM']
print(df_rpt_khm.head(15))

# Inspect Cocauvung
df_cocau = data['Cocauvung']
print("\n=== Cocauvung sample ===")
print(df_cocau.head(10))
print("Unique Tỉnh in Cocauvung:", df_cocau['Tỉnh'].unique())
print("Unique AM in Cocauvung:", df_cocau['AM'].unique())

# Inspect datatheo ngày (used for RPT_Ngày?)
df_day = data['datatheo ngày']
print("\n=== datatheo ngày sample ===")
print(df_day.head(5))
print("Unique Tuan / Dates in datatheo ngày:", df_day['Tuan'].unique()[:20])

# Inspect data theo tuần
df_week = data['data theo tuần']
print("\n=== data theo tuần sample ===")
print(df_week.head(5))
print("Unique Ngay / Dates in data theo tuần:", df_week['Ngay'].unique()[:20])

# Inspect data theo tháng
df_month = data['data theo tháng']
print("\n=== data theo tháng sample ===")
print(df_month.head(5))
print("Unique Thang / Dates in data theo tháng:", df_month['Thang'].unique()[:20])

# Inspect dataKHM
df_khm = data['dataKHM']
print("\n=== dataKHM sample ===")
print(df_khm.head(5))
print("Unique dates in dataKHM:", df_khm['Ngày LTC đầu tiên'].unique()[:20])
