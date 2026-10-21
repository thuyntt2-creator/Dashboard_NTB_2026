# -*- coding: utf-8 -*-
import sys, gspread
import pandas as pd
sys.stdout.reconfigure(encoding='utf-8')
from google.oauth2.credentials import Credentials

creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
gc = gspread.authorize(creds)
sh = gc.open_by_key('1-p9VUXndK_7BoiT-a81UfTCbUi953XNmVBoXaTGis_c')

# Check sheet 'Data'
ws_data = sh.worksheet('Data')
# Get first 5 rows and last 5 rows
rows_head = ws_data.get_values('A1:Z5')
print("=== TAB Data Header & First rows ===")
for r in rows_head:
    print(r)

# Check sheet 'auto'
ws_auto = sh.worksheet('auto')
rows_auto = ws_auto.get_values('A1:Z10')
print("\n=== TAB auto First rows ===")
for r in rows_auto:
    print(r)

# Check sheet 'NVPTT_Baseline_10h'
ws_base = sh.worksheet('NVPTT_Baseline_10h')
rows_base = ws_base.get_values('A1:E5')
print("\n=== TAB NVPTT_Baseline_10h ===")
for r in rows_base:
    print(r)
