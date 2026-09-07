import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

JSON_FILE = r'C:\Users\lap4all\Desktop\Backlog_Automation\credentials.json'
SHEET_ID = '1sTJEt8meKwVicbJAa8d7ml48yVoa_yD2_LAEbZ1ebGs'

creds = Credentials.from_service_account_file(
    JSON_FILE, 
    scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
)
gc = gspread.authorize(creds)
sh = gc.open_by_key(SHEET_ID)

def get_df(name):
    ws = sh.worksheet(name)
    data = ws.get_all_values()
    headers = data[0]
    return pd.DataFrame(data[1:], columns=headers)

df_cu = get_df('data cũ')
for col in ['Số tiền ban đầu', 'Điều chỉnh (+|-)', 'Đã truy thu', 'Cần truy thu thêm']:
    df_cu[col] = pd.to_numeric(df_cu[col], errors='coerce').fillna(0)

# Filter for Bưu Cục 56...
subset = df_cu[df_cu['Nơi vi phạm'] == 'Bưu Cục 56 Phan Đình Phùng-Cam Linh-Khánh Hòa']

print(f"Total rows for Bưu Cục 56...: {len(subset)}")
print(f"Total 'Cần truy thu thêm' for Bưu Cục 56...: {subset['Cần truy thu thêm'].sum():,}")

# Let's see unique values of columns to see what filters could be
print("\nUnique values of 'Hình thức truy thu':")
print(subset.groupby('Hình thức truy thu')['Cần truy thu thêm'].agg(['count', 'sum']))

print("\nUnique values of 'Loại truy thu':")
print(subset.groupby('Loại truy thu')['Cần truy thu thêm'].agg(['count', 'sum']))

print("\nUnique values of 'Chức vụ':")
print(subset.groupby('Chức vụ')['Cần truy thu thêm'].agg(['count', 'sum']))

print("\nUnique values of 'Nhân viên' - top 10:")
print(subset.groupby('Nhân viên')['Cần truy thu thêm'].agg(['count', 'sum']).sort_values(by='sum', ascending=False).head(10))

# Let's inspect the entire Bảng tổng hợp 1 and see its total sum or other values
ws1 = sh.worksheet('Bảng tổng hợp 1')
data1 = ws1.get_all_values()
df_bth1 = pd.DataFrame(data1[1:], columns=data1[0])
print("\n--- Bảng tổng hợp 1 in sheet (top 10) ---")
print(df_bth1.head(10))

# Let's look at Bảng tổng hợp 3 in sheet (top 10)
ws3 = sh.worksheet('Bảng tổng hợp 3')
data3 = ws3.get_all_values()
df_bth3 = pd.DataFrame(data3[1:], columns=data3[0])
print("\n--- Bảng tổng hợp 3 in sheet (top 10) ---")
print(df_bth3.head(10))

# Let's look at Bảng tổng hợp 6 in sheet (top 10)
ws6 = sh.worksheet('Bảng tổng hợp 6')
data6 = ws6.get_all_values()
df_bth6 = pd.DataFrame(data6[1:], columns=data6[0])
print("\n--- Bảng tổng hợp 6 in sheet (top 10) ---")
print(df_bth6.head(10))
