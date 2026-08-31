import os
import sys
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
import pandas as pd
import pickle

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

sheets_to_download = ['Theo ngày', 'Theo Tuần', 'Theo Tháng', 'khách hàng mơi']

# Load existing pickle
output_pkl = r"c:\Users\lap4all\Desktop\New folder\scratch\raw_sheets_data.pkl"
try:
    with open(output_pkl, 'rb') as f:
        data_dict = pickle.load(f)
except Exception as e:
    data_dict = {}

for s_name in sheets_to_download:
    print(f"Downloading sheet {s_name}...")
    ws = sh.worksheet(s_name)
    vals = ws.get_all_values(value_render_option='UNFORMATTED_VALUE')
    if not vals:
        df = pd.DataFrame()
    else:
        headers = vals[0]
        rows = vals[1:]
        max_cols = max(len(r) for r in vals)
        headers = headers + [''] * (max_cols - len(headers))
        padded_rows = []
        for r in rows:
            padded_rows.append(r + [''] * (max_cols - len(r)))
        df = pd.DataFrame(padded_rows, columns=headers)
    data_dict[s_name] = df

# Save all data locally
with open(output_pkl, 'wb') as f:
    pickle.dump(data_dict, f)
print("Saved all sheet data to raw_sheets_data.pkl successfully.")
