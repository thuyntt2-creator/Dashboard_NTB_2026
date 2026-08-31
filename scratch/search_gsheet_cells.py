import gspread
from google.oauth2.service_account import Credentials
import sys

sys.stdout.reconfigure(encoding='utf-8')

CREDENTIALS_PATH = r'C:\Users\lap4all\Desktop\Backlog_Automation\credentials.json'
SPREADSHEET_ID   = '1XaziS_8UB2lCwL01bxam106EdIUHtlMISDGJX1PU5A8'
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

def main():
    creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
    ss = gspread.authorize(creds).open_by_key(SPREADSHEET_ID)
    
    print("Searching worksheets in current spreadsheet...")
    for ws in ss.worksheets():
        print(f"  Checking {ws.title}...")
        try:
            # Get all values
            values = ws.get_all_values()
            for r_idx, row in enumerate(values, 1):
                for c_idx, cell in enumerate(row, 1):
                    cell_str = str(cell)
                    if "so tuần trước" in cell_str or "EF :" in cell_str or "309," in cell_str:
                        print(f"    FOUND in cell {gspread.utils.rowcol_to_a1(r_idx, c_idx)}: {cell_str}")
        except Exception as e:
            print(f"    Error reading {ws.title}: {e}")

if __name__ == '__main__':
    main()
