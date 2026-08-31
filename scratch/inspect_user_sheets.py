import os
import sys
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')
load_dotenv()

JSON_FILE = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS') or r'C:\Users\lap4all\Desktop\Backlog_Automation\credentials.json'
if not os.path.exists(JSON_FILE):
    JSON_FILE = 'credentials.json'

sheet_id = "12VsqpIx1vLOqk6-JKHwgRmdrgu6fxSNPQcpyO0wpvdQ"
creds = Credentials.from_service_account_file(
    JSON_FILE, 
    scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
)
gc = gspread.authorize(creds)
sh = gc.open_by_key(sheet_id)

report_sheets = ['RPT_Ngày', 'RPT_Tuần', 'RPT_Tháng', 'RPT_KHM']
raw_sheets = ['datatheo ngày', 'data theo tuần', 'data theo tháng', 'dataKHM', 'Cocauvung']

for s_name in report_sheets:
    try:
        ws = sh.worksheet(s_name)
        print(f"\n==================== SHEET: {s_name} ====================")
        # Get values with formulas
        values_formula = ws.get_all_values(value_render_option='FORMULA')
        values_val = ws.get_all_values(value_render_option='UNFORMATTED_VALUE')
        
        print(f"Dimensions: {len(values_val)} rows")
        if len(values_val) > 0:
            print("First 5 rows (VALUES):")
            for r in values_val[:10]:
                print(r[:10])
            print("First 5 rows (FORMULAS if any different):")
            for r_f, r_v in zip(values_formula[:10], values_val[:10]):
                has_formula = False
                for cell_f, cell_v in zip(r_f[:10], r_v[:10]):
                    if str(cell_f).startswith('='):
                        has_formula = True
                        break
                if has_formula:
                    print(r_f[:10])
    except Exception as e:
        print(f"Error reading {s_name}: {e}")
