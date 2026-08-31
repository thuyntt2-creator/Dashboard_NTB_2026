import os
import sys
import gspread
from oauth2client.service_account import ServiceAccountCredentials

sys.stdout.reconfigure(encoding='utf-8')

SERVICE_ACCOUNT_CANDIDATES = [
    r"C:\Users\lap4all\Desktop\Backlog_Automation\credentials.json",
    r"C:\Users\lap4all\Downloads\credentials.json",
    r"C:\Users\lap4all\Downloads\service_account.json",
    r"C:\Users\lap4all\Desktop\credentials.json",
    "credentials.json",
    "service_account.json",
]

def find_service_account_file():
    for p in SERVICE_ACCOUNT_CANDIDATES:
        if os.path.isfile(p):
            return p
    raise FileNotFoundError("No credentials.json found.")

SHEET_ID = "1lmQv8KwHJzDFs_RMz64ydu4SOmG3M1YAzILNFGtzFec"
SHEET_NTB_NAME = "NTB"

def main():
    creds_path = find_service_account_file()
    print(f"Using credentials from: {creds_path}")
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
    client = gspread.authorize(creds)
    sh = client.open_by_key(SHEET_ID)
    ntb_ws = sh.worksheet(SHEET_NTB_NAME)
    ntb_data = ntb_ws.get_all_values()
    
    print(f"Total rows: {len(ntb_data)}")
    
    # Print headers (row 4, which is index 3)
    if len(ntb_data) > 3:
        print("\n--- Row 4 (index 3) Headers ---")
        for i, val in enumerate(ntb_data[3]):
            print(f"Col {i} ({gspread.utils.rowcol_to_a1(4, i+1).replace('4', '')}): {repr(val)}")
            
    # Print first 10 data rows starting from row 5 (index 4)
    print("\n--- First 10 Data Rows starting from row 5 (index 4) ---")
    for r_idx, row in enumerate(ntb_data[4:14], start=5):
        print(f"\nRow {r_idx}:")
        for c_idx, val in enumerate(row):
            col_name = ntb_data[3][c_idx] if c_idx < len(ntb_data[3]) else f"Col_{c_idx}"
            print(f"  Col {c_idx} ({col_name}): {repr(val)}")

if __name__ == "__main__":
    main()
