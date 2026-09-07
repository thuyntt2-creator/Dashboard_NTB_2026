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

print("Loading data...")
df_cu = get_df('data cũ')
df_moi = get_df('data mới')
df_cocau = get_df('CoCauVung')

print(f"data cũ shape: {df_cu.shape}")
print(f"data mới shape: {df_moi.shape}")
print(f"CoCauVung shape: {df_cocau.shape}")

# Inspect columns and data types
for col in ['Số tiền ban đầu', 'Điều chỉnh (+|-)', 'Đã truy thu', 'Cần truy thu thêm']:
    df_cu[col] = pd.to_numeric(df_cu[col], errors='coerce').fillna(0)
    df_moi[col] = pd.to_numeric(df_moi[col], errors='coerce').fillna(0)

# Check total sum for data cũ
print("\n--- data cũ Sums ---")
print(f"Số tiền ban đầu: {df_cu['Số tiền ban đầu'].sum():,}")
print(f"Điều chỉnh (+|-): {df_cu['Điều chỉnh (+|-)'].sum():,}")
print(f"Đã truy thu: {df_cu['Đã truy thu'].sum():,}")
print(f"Cần truy thu thêm: {df_cu['Cần truy thu thêm'].sum():,}")

# Let's map AM to df_cu
# Build CoCauVung mapping
df_cocau['BC_norm'] = df_cocau['Bưu cục'].str.strip().str.lower()
bc_to_am = dict(zip(df_cocau['BC_norm'], df_cocau['AM']))

def get_am(bc_name):
    if not bc_name:
        return "Unknown"
    norm = bc_name.strip().lower()
    return bc_to_am.get(norm, "Unknown")

df_cu['AM_mapped'] = df_cu['Nơi vi phạm'].apply(get_am)
df_moi['AM_mapped'] = df_moi['Nơi vi phạm'].apply(get_am)

# Replicate Bảng tổng hợp 5 (Loại truy thu)
print("\n--- Replicating Bảng tổng hợp 5 (Loại truy thu) ---")
bth5 = df_cu.groupby('Loại truy thu').agg(
    So_tien_ban_dau=('Số tiền ban đầu', 'sum'),
    Dieu_chinh=('Điều chỉnh (+|-)', 'sum'),
    Can_truy_thu_them=('Cần truy thu thêm', 'sum')
).reset_index()
print(bth5.to_string(index=False))

# Replicate Bảng tổng hợp 1 (Nơi vi phạm)
print("\n--- Replicating Bảng tổng hợp 1 (Nơi vi phạm) - Top 5 ---")
bth1 = df_cu.groupby('Nơi vi phạm').agg(
    So_tien_ban_dau=('Số tiền ban đầu', 'sum'),
    Dieu_chinh=('Điều chỉnh (+|-)', 'sum'),
    Can_truy_thu_them=('Cần truy thu thêm', 'sum')
).reset_index().sort_values(by='Can_truy_thu_them', ascending=False)
print(bth1.head(5).to_string(index=False))

# Let's check what Vol phạt and Số tiền tạm tính are in Bảng tổng hợp 3
# Bảng tổng hợp 3 has: Nơi vi phạm, AM, Vol phạt, Số tiền tạm tính
# Wait, let's see how many rows match:
# Bưu Cục 56 Phan Đình Phùng-Cam Linh-Khánh Hòa for Võ Tấn Lợi: Vol phạt = 22, Số tiền tạm tính = 9,144,688
# Wait, let's check what columns are used.
# Let's group by Nơi vi phạm and AM_mapped.
print("\n--- Replicating Bảng tổng hợp 3 (Nơi vi phạm + AM) - Top 5 ---")
# Wait, does the raw data have an 'AM' column or did they map it?
# Let's check unique values of AM mapped for Bưu Cục 56 Phan Đình Phùng-Cam Linh-Khánh Hòa
subset_bc = df_cu[df_cu['Nơi vi phạm'] == 'Bưu Cục 56 Phan Đình Phùng-Cam Linh-Khánh Hòa']
print(f"Rows for Bưu Cục 56...: {len(subset_bc)}")
print(subset_bc.groupby('AM_mapped').size())
# Wait! In CoCauVung, what is the AM for Bưu Cục 56 Phan Đình Phùng-Cam Linh-Khánh Hòa?
print("CoCauVung for Bưu Cục 56...:")
print(df_cocau[df_cocau['Bưu cục'].str.contains('56 Phan Đình Phùng')])

# Let's count unique tickets or just rows?
# In Bảng tổng hợp 3, row count or ticket count? Let's check.
bth3 = df_cu.groupby(['Nơi vi phạm', 'AM_mapped']).agg(
    Vol_phat=('Mã ticket', 'count'),
    So_tien_tam_tinh=('Cần truy thu thêm', 'sum')
).reset_index()
print(bth3[bth3['Nơi vi phạm'] == 'Bưu Cục 56 Phan Đình Phùng-Cam Linh-Khánh Hòa'])
