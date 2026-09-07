import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd
import urllib.request

SHEET_VAN_HANH_ID = "1DAwY-46twFrHIs77R4p4IMuIZ6JTE-e58Aj-9Kcr5Jk"
url = f"https://docs.google.com/spreadsheets/d/{SHEET_VAN_HANH_ID}/export?format=xlsx"
req = urllib.request.Request(url)
req.add_header('User-Agent', 'Mozilla/5.0')
with urllib.request.urlopen(req) as response:
    with open("temp_debug.xlsx", 'wb') as f:
        f.write(response.read())

df_data = pd.read_excel("temp_debug.xlsx", sheet_name="Data")
pos = ["BC 1322 Hùng Vương", "BC 56 Phan Đình Phùng", "BC Thôn Phúc Hưng", "BC 53 Tôn Đức Thắng", "BC TDP Nghĩa Đức"]

# Filter date
df_day = df_data[df_data['Time'] == '2026-06-18 - Thứ 5']
for po in pos:
    print(f"\n--- PO: {po} ---")
    po_rows = df_day[df_day['Chi tiêt'].str.contains(po.split("-")[0].replace("BC","").strip(), case=False, na=False) if 'Chi tiêt' in df_day.columns else df_day['Chi tiết'].str.contains(po.split("-")[0].replace("BC","").strip(), case=False, na=False)]
    print(po_rows[['Time', 'Chi tiết', 'Volume', '% Gán', '% GTC', '% Chuyển trả', 'Leadtime']])

import os
if os.path.exists("temp_debug.xlsx"):
    os.remove("temp_debug.xlsx")
