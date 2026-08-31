import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import os

JSON_FILE = r'C:\Users\lap4all\Desktop\Backlog_Automation\credentials.json'
SHEET_ID = '1LEmer5MUw2iC40NXOsFI4BHJ0WHLdkxn8FSKG7cZLsc'
output_file = r"c:\Users\lap4all\Desktop\New folder\scratch\inspect_new_lc_cols_res.txt"

creds = Credentials.from_service_account_file(JSON_FILE, scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
gc = gspread.authorize(creds)
sh = gc.open_by_key(SHEET_ID)

ws = sh.worksheet('data rớt LC')
data = ws.get_all_values(value_render_option='UNFORMATTED_VALUE')

with open(output_file, "w", encoding="utf-8") as f:
    if data:
        headers = data[0]
        f.write(f"Columns: {headers}\n")
        from collections import Counter
        c = Counter(headers)
        f.write(f"Duplicate columns: { {k: v for k, v in c.items() if v > 1} }\n")
        
        df = pd.DataFrame(data[1:], columns=headers)
        f.write(f"DataFrame columns: {df.columns.tolist()}\n")
        f.write(f"Shape: {df.shape}\n")
        f.write(f"First row values: {df.iloc[0].to_dict()}\n")
        f.write(f"Unique values in column index 5 (Tuần?): {df.iloc[:, 5].unique().tolist() if df.shape[1] > 5 else 'N/A'}\n")
        
        # Check for empty columns or headers that are None/empty string
        f.write(f"Any empty column headers? { [i for i, h in enumerate(headers) if not h] }\n")
    else:
        f.write("No data found in worksheet 'data rớt LC'\n")
print("Done writing results.")
