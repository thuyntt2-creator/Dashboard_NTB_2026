import re
import sys
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

sys.stdout.reconfigure(encoding='utf-8')

CREDENTIALS_PATH = r'C:\Users\lap4all\Desktop\Backlog_Automation\credentials.json'
SPREADSHEET_ID   = '1XaziS_8UB2lCwL01bxam106EdIUHtlMISDGJX1PU5A8'
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

AM_EXTRA_MAP = {
    "Trần Công Hậu":          "Khánh Hòa",
    "Phạm Đức Thắng":         "Lâm Đồng",
    "Nguyễn Vĩnh Tường":      "Khánh Hòa",
    "Nguyễn Tống Hùng Phong": "Khánh Hòa",
}

def main():
    creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
    ss = gspread.authorize(creds).open_by_key(SPREADSHEET_ID)
    
    df_tq = pd.DataFrame(ss.worksheet("tong_quan").get_all_values(value_render_option='UNFORMATTED_VALUE'))
    df_tq.columns = df_tq.iloc[0]
    df_tq = df_tq.iloc[1:]
    
    df_coc = pd.DataFrame(ss.worksheet("CoCauVung").get_all_values(value_render_option='UNFORMATTED_VALUE'))
    df_coc.columns = df_coc.iloc[0]
    df_coc = df_coc.iloc[1:]
    
    am_tinh = (df_coc[["AM","Tỉnh"]].dropna()
               .drop_duplicates("AM").set_index("AM")["Tỉnh"].to_dict())
    am_tinh.update(AM_EXTRA_MAP)

    def get_tinh(am):
        am = str(am).strip()
        if am in am_tinh: return am_tinh[am]
        for k, v in am_tinh.items():
            if am in k or k in am: return v
        return None

    df_tq["Tinh"] = df_tq["AM_format"].apply(get_tinh)
    print("Unique values of Tinh:")
    print(df_tq["Tinh"].value_counts(dropna=False))
    
    TINH_ORDER = ["Khánh Hòa", "Lâm Đồng", "Đắk Nông", "Ninh Thuận", "Bình Thuận"]
    invalid_tinh = df_tq[~df_tq["Tinh"].isin(TINH_ORDER)]
    print("\nRows with invalid or empty Tinh:")
    print(invalid_tinh["AM_format"].value_counts(dropna=False))
    print("\nSample invalid rows:")
    print(invalid_tinh.head(10))

if __name__ == "__main__":
    main()
