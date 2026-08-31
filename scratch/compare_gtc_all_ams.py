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

# 1. Get gtcnew sheet values
ws_gtc = sh.worksheet('gtcnew')
gtc_data = ws_gtc.get_all_values()
# Slice each row to first 10 columns
gtc_data_sliced = [r[:10] for r in gtc_data[3:23]]
gtc_df = pd.DataFrame(gtc_data_sliced, columns=['AM', 'W21_Gan', 'W21_GTC', 'W22_Gan', 'W22_GTC', 'W23_Gan', 'W23_GTC', 'W24_Gan', 'W24_GTC', 'Diff'])

# 2. Get comparison sheet values
ws_comp = sh.worksheet('Phân tích AM W24 vs W23')
comp_data = ws_comp.get_all_values()
comp_df = pd.DataFrame(comp_data[1:21])

# Compare
print(f"{'AM':<25} | {'gtcnew W23':<12} | {'Comp Sheet W23':<15} | {'gtcnew W24':<12} | {'Comp Sheet W24':<15}")
print("-" * 90)

for _, r_comp in comp_df.iterrows():
    am = r_comp[0]
    # find in gtcnew tab
    r_gtc = gtc_df[gtc_df['AM'].str.strip() == am.strip()]
    if not r_gtc.empty:
        gtc_w23 = r_gtc['W23_GTC'].values[0]
        gtc_w24 = r_gtc['W24_GTC'].values[0]
        comp_w23 = r_comp[5] # Index 5 is Tỉ lệ GTC W23
        comp_w24 = r_comp[6] # Index 6 is Tỉ lệ GTC W24
        print(f"{am:<25} | {gtc_w23:<12} | {comp_w23:<15} | {gtc_w24:<12} | {comp_w24:<15}")
    else:
        print(f"AM {am} NOT found in gtcnew tab")
