import re
import sys
from datetime import datetime
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

sys.stdout.reconfigure(encoding='utf-8')

CREDENTIALS_PATH = r'C:\Users\lap4all\Desktop\Backlog_Automation\credentials.json'
SPREADSHEET_ID   = '12VsqpIx1vLOqk6-JKHwgRmdrgu6fxSNPQcpyO0wpvdQ'
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

def main():
    creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
    ss = gspread.authorize(creds).open_by_key(SPREADSHEET_ID)
    
    data = ss.worksheet("khách hàng mơi").get_all_values(value_render_option='UNFORMATTED_VALUE')
    df_khm = pd.DataFrame(data[1:], columns=data[0])
    
    print("Columns in khách hàng mơi:")
    print(df_khm.columns.tolist())
    
    # Check rows where AM is 'Đã nghỉ' or contains it
    df_khm["AM_clean"] = df_khm["AM"].astype(str).str.strip()
    df_da_nghi = df_khm[df_khm["AM_clean"] == "Đã nghỉ"]
    print(f"\nNumber of 'Đã nghỉ' rows: {len(df_da_nghi)}")
    
    # Print unique values of other columns for 'Đã nghỉ' rows
    # Try to see if there are columns like 'Tỉnh', 'Vùng', 'Chi nhánh', 'Bưu cục', 'AM', 'Mã bưu cục', etc.
    cols_to_check = [col for col in df_khm.columns if col not in ["AM", "AM_clean", "Mã KH", "Tên KH"]]
    for col in cols_to_check:
        unique_vals = df_da_nghi[col].unique()
        if len(unique_vals) < 15:
            print(f"Unique values in '{col}': {unique_vals}")
        else:
            print(f"Unique values in '{col}': {len(unique_vals)} unique values (e.g. {unique_vals[:5]})")

if __name__ == "__main__":
    main()
