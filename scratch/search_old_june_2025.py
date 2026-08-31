import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import sys
import re
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

CREDENTIALS_PATH = r'C:\Users\lap4all\Desktop\Backlog_Automation\credentials.json'
OLD_SPREADSHEET_ID = '12VsqpIx1vLOqk6-JKHwgRmdrgu6fxSNPQcpyO0wpvdQ'
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

TINH_ORDER = ["Khánh Hòa", "Lâm Đồng", "Đắk Nông", "Ninh Thuận", "Bình Thuận"]
AM_EXTRA_MAP = {
    "Trần Công Hậu":          "Khánh Hòa",
    "Phạm Đức Thắng":         "Lâm Đồng",
    "Nguyễn Vĩnh Tường":      "Khánh Hòa",
    "Nguyễn Tống Hùng Phong": "Khánh Hòa",
}

_MONTH_MAP = {f"thg {i}": i for i in range(1, 13)}

def parse_vn_date(s):
    if isinstance(s, (int, float)):
        return pd.to_datetime(s, unit='D', origin='1899-12-30').to_pydatetime()
    s = str(s).strip()
    if s.isdigit():
        return pd.to_datetime(int(s), unit='D', origin='1899-12-30').to_pydatetime()
    for m, num in _MONTH_MAP.items():
        if m in s:
            parts = re.findall(r"\d+", s)
            if len(parts) >= 2:
                return datetime(int(parts[-1]), num, int(parts[0]))
    return None

def main():
    creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
    ss = gspread.authorize(creds).open_by_key(OLD_SPREADSHEET_ID)
    
    ws_day = ss.worksheet("Theo ngày")
    data_day = ws_day.get_all_values()
    df_day = pd.DataFrame(data_day[1:], columns=data_day[0])
    
    ws_coc = ss.worksheet("Cocauvung")
    data_coc = ws_coc.get_all_values(value_render_option='UNFORMATTED_VALUE')
    df_coc = pd.DataFrame(data_coc[1:], columns=data_coc[0])
    
    am_tinh = (df_coc[["AM","Tỉnh"]].dropna()
               .drop_duplicates("AM").set_index("AM")["Tỉnh"].to_dict())
    am_tinh.update(AM_EXTRA_MAP)

    def get_tinh(am):
        am = str(am).strip()
        if not am or am == "-": return None
        if am in am_tinh: return am_tinh[am]
        for k, v in am_tinh.items():
            if am in k or k in am: return v
        return None

    df_day["date"] = df_day["Ngay"].apply(parse_vn_date)
    df_day["DoanhThu"] = pd.to_numeric(df_day["DoanhThu"], errors="coerce").fillna(0)
    df_day["Volume"] = pd.to_numeric(df_day["Volume"], errors="coerce").fillna(0)
    df_day = df_day.dropna(subset=["date"])
    df_day["Tinh"] = df_day["AM_format"].apply(get_tinh)
    df_day = df_day[df_day["Tinh"].isin(TINH_ORDER)]
    
    # Let's sum June 1 to June 16, 2025:
    june_2025 = df_day[(df_day["date"] >= datetime(2025, 6, 1)) & (df_day["date"] <= datetime(2025, 6, 16))]
    print("June 1-16, 2025 daily records sum:")
    print(june_2025.groupby("Tinh")[["DoanhThu", "Volume"]].sum())
    print("Total DT:", june_2025["DoanhThu"].sum() / 1e6, "M")
    
    # What about May 1 to May 16, 2026 in the old sheet?
    may_2026 = df_day[(df_day["date"] >= datetime(2026, 5, 1)) & (df_day["date"] <= datetime(2026, 5, 16))]
    print("\nMay 1-16, 2026 daily records sum in old sheet:")
    print(may_2026.groupby("Tinh")[["DoanhThu", "Volume"]].sum())
    print("Total DT:", may_2026["DoanhThu"].sum() / 1e6, "M")

if __name__ == "__main__":
    main()
