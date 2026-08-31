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

# Check if there are formulas anywhere in report sheets
for s_name in report_sheets:
    ws = sh.worksheet(s_name)
    formulas = ws.get_all_values(value_render_option='FORMULA')
    has_formula = False
    for r_idx, row in enumerate(formulas):
        for c_idx, cell in enumerate(row):
            if str(cell).startswith('='):
                print(f"Formula in {s_name} at cell ({r_idx+1},{c_idx+1}): {cell}")
                has_formula = True
    if not has_formula:
        print(f"No formulas found in sheet {s_name}. All values are static/hardcoded.")

# Let's inspect raw sheets structure
for s_name in raw_sheets:
    ws = sh.worksheet(s_name)
    print(f"\n==================== RAW SHEET: {s_name} ====================")
    vals = ws.get_all_values(value_render_option='UNFORMATTED_VALUE')
    print(f"Dimensions: {len(vals)} rows")
    if len(vals) > 0:
        print("Header:", vals[0])
        print("Row 1:", vals[1] if len(vals) > 1 else "N/A")
        print("Row 2:", vals[2] if len(vals) > 2 else "N/A")
