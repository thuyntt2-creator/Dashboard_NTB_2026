import gspread
from google.oauth2.service_account import Credentials
import sys

sys.stdout.reconfigure(encoding='utf-8')

CREDENTIALS_PATH = r'C:\Users\lap4all\Desktop\Backlog_Automation\credentials.json'
SPREADSHEET_ID = '1x8MxOZV0wMFi7NmXlMaxjBbWjr6zyylUE2rjI4votmw'
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

def main():
    creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
    ss = gspread.authorize(creds).open_by_key(SPREADSHEET_ID)
    
    print("Searching worksheets in Báo cáo gán spreadsheet...")
    for ws in ss.worksheets():
        print(f"  Checking {ws.title}...")
        try:
            values = ws.get_all_values()
            for r_idx, row in enumerate(values, 1):
                for c_idx, cell in enumerate(row, 1):
                    cell_str = str(cell)
                    if "so tuần trước" in cell_str or "EF :" in cell_str or "309," in cell_str:
                        print(f"    FOUND in {ws.title} cell {gspread.utils.rowcol_to_a1(r_idx, c_idx)}: {cell_str}")
        except Exception as e:
            print(f"    Error reading {ws.title}: {e}")

if __name__ == '__main__':
    main()
