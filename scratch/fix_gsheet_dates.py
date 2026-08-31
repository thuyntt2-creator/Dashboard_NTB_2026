import gspread
from google.oauth2.service_account import Credentials
import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

JSON_FILE = r'C:\Users\lap4all\Desktop\Backlog_Automation\credentials.json'
if not os.path.exists(JSON_FILE):
    JSON_FILE = 'credentials.json'

SPREADSHEET_ID = '1XaziS_8UB2lCwL01bxam106EdIUHtlMISDGJX1PU5A8'

# Regex to match Vietnamese date formats:
# e.g., "22 thg 4, 2026", "8 thg 6, 2026", "16 thg 06, 2026"
vn_date_pattern = re.compile(r'^\s*(\d+)\s+thg\s+(\d+),?\s+(\d{4})\s*$')

def parse_vn_date(val):
    if not isinstance(val, str):
        return None
    m = vn_date_pattern.match(val)
    if m:
        try:
            day = int(m.group(1))
            month = int(m.group(2))
            year = int(m.group(3))
            return f"{year:04d}-{month:02d}-{day:02d}"
        except Exception:
            return None
    return None

def main():
    print("Connecting to Google Sheets...")
    try:
        creds = Credentials.from_service_account_file(
            JSON_FILE, 
            scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        )
        gc = gspread.authorize(creds)
        sh = gc.open_by_key(SPREADSHEET_ID)
        print(f"Connected to sheet: '{sh.title}'")
    except Exception as e:
        print(f"Error connecting to Google Sheets: {e}")
        return

    worksheets = sh.worksheets()
    print(f"Found {len(worksheets)} worksheets:")
    for ws in worksheets:
        print(f" - {ws.title}")

    # For each worksheet, let's find columns with VN text dates and fix them
    for ws in worksheets:
        print(f"\nProcessing worksheet: '{ws.title}'...")
        # Get all values
        data = ws.get_all_values()
        if not data:
            print("  Empty worksheet.")
            continue
        
        headers = data[0]
        rows = data[1:]
        
        # Check which columns have VN date strings
        # We check the first 200 rows of each column to decide
        cols_to_fix = []
        for col_idx in range(len(headers)):
            sample_vals = [r[col_idx] for r in rows[:200] if col_idx < len(r)]
            vn_date_count = sum(1 for val in sample_vals if parse_vn_date(val) is not None)
            if vn_date_count > 0:
                print(f"  Detected Vietnamese date format in column '{headers[col_idx]}' (index {col_idx+1})")
                cols_to_fix.append(col_idx)
        
        if not cols_to_fix:
            print("  No columns to fix.")
            continue
            
        # We will do cell range updates using the loaded data
        for col_idx in cols_to_fix:
            col_letter = gspread.utils.rowcol_to_a1(1, col_idx + 1)[:-1] # E.g., 'C'
            print(f"  Fixing column {col_letter} ({headers[col_idx]})...")
            
            updates = []
            fixed_count = 0
            for r_idx, row_data in enumerate(rows):
                if col_idx < len(row_data):
                    val = row_data[col_idx]
                    parsed = parse_vn_date(val)
                    if parsed:
                        updates.append({
                            'range': f"{col_letter}{r_idx + 2}",
                            'values': [[parsed]]
                        })
                        fixed_count += 1
            
            if updates:
                print(f"    Updating {fixed_count} cells in column {col_letter}...")
                ws.batch_update(updates, value_input_option='USER_ENTERED')
                print(f"    Successfully updated column {col_letter}!")
            else:
                print(f"    No cells needed updates in column {col_letter}.")

if __name__ == '__main__':
    main()
