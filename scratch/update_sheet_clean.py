# -*- coding: utf-8 -*-
import sys, os, time
import gspread
from google.oauth2.credentials import Credentials

sys.stdout.reconfigure(encoding='utf-8')

creds_path = 'authorized_user.json'
creds = Credentials.from_authorized_user_file(creds_path, scopes=['https://www.googleapis.com/auth/spreadsheets'])
gc = gspread.authorize(creds)

SHEET_OPS_ID = '14cN4YAf01NqKtREtmhBngRP58OCdgby-PjVoixVlpZo'
sh_ops = gc.open_by_key(SHEET_OPS_ID)
ws_kt = sh_ops.worksheet('Kiểm tra')

# 1. Update D13 and G13
d13_formula = "=IFERROR(XLOOKUP(VALUE(A4), 'Bất ổn'!C:C, 'Bất ổn'!F:F), IFERROR(XLOOKUP(TO_TEXT(A4), 'Bất ổn'!C:C, 'Bất ổn'!F:F), 0.5))"
ws_kt.update(range_name='D13', values=[[d13_formula]], value_input_option='USER_ENTERED')
ws_kt.update(range_name='G13', values=[['(Điều kiện: %GTC 7 ngày >= 50% và >= 70% Lịch sử)']])
print("1. Đã cập nhật D13 & G13!")

# 2. Update F11
f11_formula = "=IF(D11=0, 0, CEILING(MAX(ROUNDUP((SUM(D4:D9)+D11)*0.7*D13 - SUM(F4:F9)), ROUNDUP((SUM(D4:D9)+D11)*0.50 - SUM(F4:F9)), ROUNDUP(D11*0.2)), 1))"
ws_kt.update(range_name='F11', values=[[f11_formula]], value_input_option='USER_ENTERED')
print("2. Đã cập nhật F11 với mốc 0.50!")

# 3. Update table N3:N13 in a single batch call
n_formulas = []
for r in range(3, 14):
    f_n = f"=IF(M{r}=0, 0, ROUNDUP(MAX(0.7 * XLOOKUP(K{r}, 'Bất ổn'!$C:$C, 'Bất ổn'!$F:$F) * (SUM(QUERY('Theo dõi BC bể'!$A:$I, \"SELECT C+D WHERE A = '\"&L{r}&\"' ORDER BY B DESC LIMIT 6 LABEL C+D ''\", 0)) + M{r}) - SUM(QUERY('Theo dõi BC bể'!$A:$I, \"SELECT G WHERE A = '\"&L{r}&\"' ORDER BY B DESC LIMIT 6 LABEL G ''\", 0)), 0.50 * (SUM(QUERY('Theo dõi BC bể'!$A:$I, \"SELECT C+D WHERE A = '\"&L{r}&\"' ORDER BY B DESC LIMIT 6 LABEL C+D ''\", 0)) + M{r}) - SUM(QUERY('Theo dõi BC bể'!$A:$I, \"SELECT G WHERE A = '\"&L{r}&\"' ORDER BY B DESC LIMIT 6 LABEL G ''\", 0)), 0.2 * M{r})))"
    n_formulas.append([f_n])

ws_kt.update(range_name='N3:N13', values=n_formulas, value_input_option='USER_ENTERED')
print("3. Đã cập nhật N3:N13 trong 1 lượt duy nhất!")

time.sleep(2)

# Check values in Kiểm tra rows 3..9
vals = ws_kt.get_values('I2:P9')
print("\n=== KẾT QUẢ BẢNG TIẾN ĐỘ THOÁT BỂ TRÊN SHEET KIỂM TRA ===")
for r in vals:
    print(r)
