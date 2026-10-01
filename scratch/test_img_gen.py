import os
import pandas as pd
import gspread
from google.oauth2.credentials import Credentials as UserCredentials

auth_user = r'C:\Users\lap4all\Desktop\Backlog_Automation\authorized_user.json'
creds = UserCredentials.from_authorized_user_file(auth_user, scopes=['https://www.googleapis.com/auth/spreadsheets'])
gc = gspread.authorize(creds)
sh = gc.open_by_key('1CbXJb_-HqGGcOep8R6Zf6qBn8gGi_8EyLkr8ebhEdzI')

df_pivot_raw = pd.DataFrame(sh.worksheet('PIVOT').get_all_values())
xn_raw = sh.worksheet('Xuất Nhập KTC').get_all_values()
df_xuat_nhap = pd.DataFrame(xn_raw[1:], columns=xn_raw[0]) if xn_raw else pd.DataFrame()
for col in ['volumedonhang']:
    if col in df_xuat_nhap.columns:
        df_xuat_nhap[col] = pd.to_numeric(df_xuat_nhap[col], errors='coerce').fillna(0)

# Import create_img_pivot and create_img_xuat_nhap from none LT KTC
import sys
sys.path.append(r'C:\Users\lap4all\Documents\Auto report')
# We can load the functions
exec(open(r'C:\Users\lap4all\Documents\Auto report\none LT KTC.py', encoding='utf-8').read(), globals())

# Test image generation
path_p = create_img_pivot(df_pivot_raw)
print(f"Pivot image created: {path_p}, exists: {os.path.exists(path_p)}")

path_xn, xn_date = create_img_xuat_nhap(df_xuat_nhap)
print(f"Xuat nhap image created: {path_xn}, exists: {os.path.exists(path_xn)}, date: {xn_date}")
