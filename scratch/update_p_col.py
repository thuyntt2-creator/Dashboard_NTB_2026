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

p_formulas = []
for r in range(3, 14):
    f_p = f'=IF(VALUE(M{r})=0, "Chưa có hàng", IF(VALUE(O{r})>=VALUE(N{r}), "✅ ĐÃ THOÁT", IF(VALUE(N{r})>VALUE(M{r}), "🔴 CẦN MAX " & TEXT(M{r}, "#,##0") & " (Cần thêm ngày)", "🔴 THIẾU " & TEXT(VALUE(N{r})-VALUE(O{r}), "#,##0") & " ĐƠN")))'
    p_formulas.append([f_p])

ws_kt.update(range_name='P3:P13', values=p_formulas, value_input_option='USER_ENTERED')
print("Đã cập nhật P3:P13 với VALUE() thành công!")

time.sleep(2)
vals = ws_kt.get_values('I2:P9')
print("\n=== KẾT QUẢ BẢNG TIẾN ĐỘ THOÁT BỂ MỚI NHẤT ===")
for r in vals:
    print(r)
