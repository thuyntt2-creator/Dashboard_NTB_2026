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
    max_cols = max(len(row) for row in data)
    if len(headers) < max_cols:
        headers += [f"Unnamed_{i}" for i in range(len(headers)+1, max_cols+1)]
    return pd.DataFrame(data[1:], columns=headers)

df_cu = get_df('data cũ')
for col in ['Số tiền ban đầu', 'Điều chỉnh (+|-)', 'Đã truy thu', 'Cần truy thu thêm']:
    df_cu[col] = pd.to_numeric(df_cu[col], errors='coerce').fillna(0)

subset = df_cu[df_cu['Nơi vi phạm'] == 'Bưu Cục 56 Phan Đình Phùng-Cam Linh-Khánh Hòa'].copy()

# Target value: 8,980,808
# Let's test combinations of 'Hình thức truy thu', 'Loại truy thu', 'Chức vụ'
import itertools

cat_cols = ['Hình thức truy thu', 'Chức vụ', 'Loại truy thu']
# Get all unique values for each category column
unique_vals = {col: list(subset[col].unique()) for col in cat_cols}

print("Brute-forcing subset sums for 'Cần truy thu thêm' or 'Số tiền ban đầu' to match 8,980,808...")

# We want to find a filter condition (e.g., col1 in list1 & col2 in list2 & col3 in list3)
# Let's check sub-groupings first:
for r in range(1, 4):
    for combo_cols in itertools.combinations(cat_cols, r):
        print(f"\nGrouping by columns: {combo_cols}")
        grouped = subset.groupby(list(combo_cols))['Cần truy thu thêm'].sum().reset_index()
        match_add = grouped[grouped['Cần truy thu thêm'] == 8980808]
        if not match_add.empty:
            print("Found match in 'Cần truy thu thêm'!")
            print(match_add)
            
        grouped_init = subset.groupby(list(combo_cols))['Số tiền ban đầu'].sum().reset_index()
        match_init = grouped_init[grouped_init['Số tiền ban đầu'] == 8980808]
        if not match_init.empty:
            print("Found match in 'Số tiền ban đầu'!")
            print(match_init)

# What if the filter is excluding some categories of 'Loại truy thu'?
# Let's list all combinations of 'Loại truy thu' to exclude
types = list(subset['Loại truy thu'].unique())
for r in range(1, len(types)):
    for exclude_types in itertools.combinations(types, r):
        df_f = subset[~subset['Loại truy thu'].isin(exclude_types)]
        
        # Check if sum is 8980808
        s_add = df_f['Cần truy thu thêm'].sum()
        s_init = df_f['Số tiền ban đầu'].sum()
        
        if s_add == 8980808:
            print(f"Match by excluding types {exclude_types} (Cần truy thu thêm = 8,980,808)")
        if s_init == 8980808:
            print(f"Match by excluding types {exclude_types} (Số tiền ban đầu = 8,980,808)")

        # What if we filter by Chức vụ as well?
        for cv in subset['Chức vụ'].unique():
            df_f_cv = df_f[df_f['Chức vụ'] == cv]
            if df_f_cv['Cần truy thu thêm'].sum() == 8980808:
                print(f"Match by excluding types {exclude_types} AND Chức vụ = {cv} (Cần truy thu thêm = 8,980,808)")
            if df_f_cv['Số tiền ban đầu'].sum() == 8980808:
                print(f"Match by excluding types {exclude_types} AND Chức vụ = {cv} (Số tiền ban đầu = 8,980,808)")

        # What if we filter by Hình thức truy thu as well?
        for ht in subset['Hình thức truy thu'].unique():
            df_f_ht = df_f[df_f['Hình thức truy thu'] == ht]
            if df_f_ht['Cần truy thu thêm'].sum() == 8980808:
                print(f"Match by excluding types {exclude_types} AND Hình thức truy thu = {ht} (Cần truy thu thêm = 8,980,808)")
            if df_f_ht['Số tiền ban đầu'].sum() == 8980808:
                print(f"Match by excluding types {exclude_types} AND Hình thức truy thu = {ht} (Số tiền ban đầu = 8,980,808)")
