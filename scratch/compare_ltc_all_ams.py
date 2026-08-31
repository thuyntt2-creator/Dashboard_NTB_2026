import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

JSON_FILE = r'C:\Users\lap4all\Desktop\Backlog_Automation\credentials.json'
SHEET_ID = '1LEmer5MUw2iC40NXOsFI4BHJ0WHLdkxn8FSKG7cZLsc'

creds = Credentials.from_service_account_file(
    JSON_FILE, 
    scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
)
gc = gspread.authorize(creds)
sh = gc.open_by_key(SHEET_ID)

# 1. Get LTC sheet values
ws_ltc = sh.worksheet('LTC')
ltc_data = ws_ltc.get_all_values()
# Slice each row to first 10 columns
ltc_data_sliced = [r[:10] for r in ltc_data[3:23]]
ltc_df = pd.DataFrame(ltc_data_sliced, columns=['AM', 'W21_Gan', 'W21_LTC', 'W22_Gan', 'W22_LTC', 'W23_Gan', 'W23_LTC', 'W24_Gan', 'W24_LTC', 'Diff'])

# 2. Get comparison sheet values
ws_comp = sh.worksheet('Phân tích AM W24 vs W23')
comp_data = ws_comp.get_all_values()
comp_df = pd.DataFrame(comp_data[1:21]) # don't assign columns yet, use index

# Compare
print(f"{'AM':<25} | {'LTC Tab W23':<12} | {'Comp Sheet W23':<15} | {'LTC Tab W24':<12} | {'Comp Sheet W24':<15}")
print("-" * 90)

for _, r_comp in comp_df.iterrows():
    am = r_comp[0] # First column in row is AM
    # find in LTC tab
    r_ltc = ltc_df[ltc_df['AM'].str.strip() == am.strip()]
    if not r_ltc.empty:
        ltc_w23 = r_ltc['W23_LTC'].values[0]
        ltc_w24 = r_ltc['W24_LTC'].values[0]
        comp_w23 = r_comp[11] # Index 11 is Tỉ lệ LTC W23
        comp_w24 = r_comp[12] # Index 12 is Tỉ lệ LTC W24
        print(f"{am:<25} | {ltc_w23:<12} | {comp_w23:<15} | {ltc_w24:<12} | {comp_w24:<15}")
    else:
        print(f"AM {am} NOT found in LTC tab")
