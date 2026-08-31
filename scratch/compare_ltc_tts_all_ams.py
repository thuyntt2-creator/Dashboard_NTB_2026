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
# Slice each row to columns L to U (indices 11 to 20)
ltc_tts_data = []
for r in ltc_data[3:23]:
    row_sliced = r[11:21]
    if len(row_sliced) < 10:
        row_sliced += [""] * (10 - len(row_sliced))
    ltc_tts_data.append(row_sliced)

ltc_tts_df = pd.DataFrame(ltc_tts_data, columns=['AM', 'W21_Gan', 'W21_LTC', 'W22_Gan', 'W22_LTC', 'W23_Gan', 'W23_LTC', 'W24_Gan', 'W24_LTC', 'Diff'])

# 2. Get comparison sheet values
ws_comp = sh.worksheet('Phân tích AM W24 vs W23')
comp_data = ws_comp.get_all_values()
comp_df = pd.DataFrame(comp_data[1:21])

# Compare
print(f"{'AM':<25} | {'LTC TTS Tab W23':<15} | {'Comp TTS W23':<15} | {'LTC TTS Tab W24':<15} | {'Comp TTS W24':<15}")
print("-" * 100)

for _, r_comp in comp_df.iterrows():
    am = r_comp[0]
    # find in LTC TTS
    r_ltc = ltc_tts_df[ltc_tts_df['AM'].str.strip() == am.strip()]
    if not r_ltc.empty:
        ltc_w23 = r_ltc['W23_LTC'].values[0]
        ltc_w24 = r_ltc['W24_LTC'].values[0]
        comp_w23 = r_comp[14] # Index 14 is Tỉ lệ LTC TTS W23
        comp_w24 = r_comp[15] # Index 15 is Tỉ lệ LTC TTS W24
        print(f"{am:<25} | {ltc_w23:<15} | {comp_w23:<15} | {ltc_w24:<15} | {comp_w24:<15}")
    else:
        print(f"AM {am} NOT found in LTC TTS tab section")
