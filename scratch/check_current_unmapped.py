import re
import sys
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
    
    df_khm = pd.DataFrame(ss.worksheet("khách hàng mơi").get_all_values(value_render_option='UNFORMATTED_VALUE')[1:], columns=ss.worksheet("khách hàng mơi").get_all_values(value_render_option='UNFORMATTED_VALUE')[0])
    df_coc = pd.DataFrame(ss.worksheet("Cocauvung").get_all_values(value_render_option='UNFORMATTED_VALUE')[1:], columns=ss.worksheet("Cocauvung").get_all_values(value_render_option='UNFORMATTED_VALUE')[0])
    
    AM_EXTRA_MAP = {
        "Trần Công Hậu":          "Khánh Hòa",
        "Phạm Đức Thắng":         "Lâm Đồng",
        "Nguyễn Vĩnh Tường":      "Khánh Hòa",
        "Nguyễn Tống Hùng Phong": "Khánh Hòa",
    }
    
    am_tinh = (df_coc[["AM","Tỉnh"]].dropna()
               .drop_duplicates("AM").set_index("AM")["Tỉnh"].to_dict())
    am_tinh.update(AM_EXTRA_MAP)
    
    df_khm["AM_clean"] = df_khm["AM"].astype(str).str.strip()
    unmapped = df_khm[~df_khm["AM_clean"].isin(am_tinh.keys())].copy()
    
    print(f"Total unmapped rows in current KHM: {len(unmapped)}")
    print("\nValue counts of unmapped AMs:")
    print(unmapped["AM_clean"].value_counts())
    
    # Check if any unmapped records belong to NTB provinces
    ntb_provinces = ["Khánh Hòa", "Lâm Đồng", "Đắk Nông", "Ninh Thuận", "Bình Thuận"]
    unmapped_ntb = unmapped[unmapped["Tinh"].isin(ntb_provinces)]
    print(f"\nUnmapped records belonging to NTB: {len(unmapped_ntb)}")
    if not unmapped_ntb.empty:
        print(unmapped_ntb[["AM_clean", "Tinh", "Bưu Cục SO"]].value_counts())

if __name__ == "__main__":
    main()
