# -*- coding: utf-8 -*-
import sys, os, time, json
import gspread
from google.oauth2.credentials import Credentials

sys.stdout.reconfigure(encoding='utf-8')

creds_path = 'authorized_user.json'
creds = Credentials.from_authorized_user_file(creds_path, scopes=['https://www.googleapis.com/auth/spreadsheets'])
gc = gspread.authorize(creds)

SHEET_OPS_ID = '14cN4YAf01NqKtREtmhBngRP58OCdgby-PjVoixVlpZo'
SHEET_CB_ID = '1lmQv8KwHJzDFs_RMz64ydu4SOmG3M1YAzILNFGtzFec'

sh_ops = gc.open_by_key(SHEET_OPS_ID)

# 1. Update raw_buu_cuc_canh_bao to use raw_buu_cuc_canh_bao_2 (50% threshold)
print("1. Cập nhật tab raw_buu_cuc_canh_bao sang raw_buu_cuc_canh_bao_2...")
ws_raw = sh_ops.worksheet('raw_buu_cuc_canh_bao')
formula_raw = '=QUERY(IMPORTRANGE("1odUPX5mWpUYUUQOrhX_k8kXWV7drMUdQ58DRwgSQNS8", "raw_buu_cuc_canh_bao_2!A1:T20000"), "SELECT * WHERE Col2 = \'NTB\'", 1)'
ws_raw.update(range_name='A1', values=[[formula_raw]], value_input_option='USER_ENTERED')
print("-> Đã update formula raw_buu_cuc_canh_bao!")

time.sleep(3)

# 2. Check tab Bất ổn
ws_bo = sh_ops.worksheet('Bất ổn')
# Update Col16 >= 100 in A6 to match BC_canh_bao
formula_bo = '=QUERY(IMPORTRANGE("14cN4YAf01NqKtREtmhBngRP58OCdgby-PjVoixVlpZo","raw_buu_cuc_canh_bao!B2:T"), "SELECT * WHERE Col1 = \'NTB\' AND NOT LOWER(Col4) CONTAINS \'kd \' AND NOT LOWER(Col4) CONTAINS \'thanh lý\' AND NOT LOWER(Col4) CONTAINS \'kho \' AND NOT LOWER(Col4) CONTAINS \'test\' AND NOT LOWER(Col4) CONTAINS \'lh \' AND NOT LOWER(Col4) CONTAINS \'key\' AND NOT LOWER(Col4) CONTAINS \'b2b\' AND NOT LOWER(Col4) CONTAINS \'ck \' AND NOT LOWER(Col4) CONTAINS \'kim tân\' AND Col4 IS NOT NULL AND LOWER(Col19) <> \'bình thường\' AND Col16 >= 100 ORDER BY Col1, Col5", 0)'
ws_bo.update(range_name='A6', values=[[formula_bo]], value_input_option='USER_ENTERED')
print("-> Đã update formula Bất ổn A6!")

time.sleep(4)
bo_vals = ws_bo.get_all_values()
print(f"Số dòng hiện tại trong Bất ổn: {len(bo_vals)}")
for r in bo_vals[4:]:
    if len(r) >= 4 and r[3].strip():
        print("  BC cảnh báo:", r[1], r[2], r[3], r[4], r[5])

# 3. Update tab Kiểm tra
print("\n3. Cập nhật tab Kiểm tra công thức Target với mốc 0.50 (50%)...")
ws_kt = sh_ops.worksheet('Kiểm tra')

# Update cell D13 note
ws_kt.update(range_name='D13', values=[['(Điều kiện: %GTC 7 ngày >= 50% và >= 70% Lịch sử)']])

# Update formula in N3:N8 for 6 warning hubs
# In cell N{row}, the formula should use 0.50 instead of 0.45:
# ROUNDUP(MAX(0.7 * XLOOKUP(K{r}, 'Bất ổn'!$C:$C, 'Bất ổn'!$F:$F) * (SUM(QUERY('Theo dõi BC bể'!$A:$I, "SELECT C+D WHERE A = '"&L{r}&"' ORDER BY B DESC LIMIT 6 LABEL C+D ''", 0)) + M{r}) - SUM(QUERY('Theo dõi BC bể'!$A:$I, "SELECT G WHERE A = '"&L{r}&"' ORDER BY B DESC LIMIT 6 LABEL G ''", 0)), 0.50 * (SUM(QUERY('Theo dõi BC bể'!$A:$I, "SELECT C+D WHERE A = '"&L{r}&"' ORDER BY B DESC LIMIT 6 LABEL C+D ''", 0)) + M{r}) - SUM(QUERY('Theo dõi BC bể'!$A:$I, "SELECT G WHERE A = '"&L{r}&"' ORDER BY B DESC LIMIT 6 LABEL G ''", 0)), 0.2 * M{r}))

updates = []
for r in range(3, 14): # for rows 3..13
    f_n = f'=IF(M{r}=0, 0, ROUNDUP(MAX(0.7 * XLOOKUP(K{r}, \'Bất ổn\'!$C:$C, \'Bất ổn\'!$F:$F) * (SUM(QUERY(\'Theo dõi BC bể\'!$A:$I, "SELECT C+D WHERE A = \'"&L{r}&"\' ORDER BY B DESC LIMIT 6 LABEL C+D \'\'", 0)) + M{r}) - SUM(QUERY(\'Theo dõi BC bể\'!$A:$I, "SELECT G WHERE A = \'"&L{r}&"\' ORDER BY B DESC LIMIT 6 LABEL G \'\'", 0)), 0.50 * (SUM(QUERY(\'Theo dõi BC bể\'!$A:$I, "SELECT C+D WHERE A = \'"&L{r}&"\' ORDER BY B DESC LIMIT 6 LABEL C+D \'\'", 0)) + M{r}) - SUM(QUERY(\'Theo dõi BC bể\'!$A:$I, "SELECT G WHERE A = \'"&L{r}&"\' ORDER BY B DESC LIMIT 6 LABEL G \'\'", 0)), 0.2 * M{r})))'
    ws_kt.update(range_name=f'N{r}', values=[[f_n]], value_input_option='USER_ENTERED')

print("-> Đã cập nhật công thức N3:N13 sang mốc 0.50!")

# Also check cell F11 / D11 on single check
# Let's inspect D11/F11 single calculator
f_f11 = ws_kt.acell('D11', value_render_option='FORMULA').value
print("D11 formula:", f_f11)
f_d12 = ws_kt.acell('D12', value_render_option='FORMULA').value
print("D12 formula:", f_d12)

# Check cell D11 (or Target single check): where is Target in single check?
# In Row 11: Col 3 is Target GTC thoát nhóm cảnh báo HÔM NAY =>, Col 4 is D11 (Target value)
f_target_single = ws_kt.acell('D11', value_render_option='FORMULA').value
print("D11 formula:", f_target_single)
# Wait, let's see what formula is in D11 and F11
print("Kiểm tra xong Google Sheet!")
