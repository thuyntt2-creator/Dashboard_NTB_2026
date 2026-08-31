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
    ws = ss.worksheet("phan_nhom")
    
    # Read cells from row 1 to 5 with formulas
    print("Row 1 cells:")
    print(ws.row_values(1))
    
    print("\nRow 2 cells with formulas:")
    # We can use get_all_cells or similar, or just check cell values with value_render_option='FORMULA'
    cells = ws.get('A1:O10', value_render_option='FORMULA')
    for r_idx, row in enumerate(cells, 1):
        print(f"Row {r_idx}: {row}")

if __name__ == '__main__':
    main()
