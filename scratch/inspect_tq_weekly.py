import pandas as pd
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
    
    df_tq = ws_to_df(ss, "tong_quan")
    df_coc = ws_to_df(ss, "CoCauVung")
    
    # Filter out empty/trailing rows from CoCauVung
    df_coc = df_coc[df_coc["AM"].astype(str).str.strip() != ""]
    df_coc = df_coc[df_coc["Tỉnh"].astype(str).str.strip() != ""]

    AM_EXTRA_MAP = {
        "Trần Công Hậu":          "Khánh Hòa",
        "Phạm Đức Thắng":         "Lâm Đồng",
        "Nguyễn Vĩnh Tường":      "Khánh Hòa",
        "Nguyễn Tống Hùng Phong": "Khánh Hòa",
    }
    
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

    def parse_vn_date(s):
        if isinstance(s, (int, float)):
            return pd.to_datetime(s, unit='D', origin='1899-12-30').to_pydatetime()
        s = str(s).strip()
        if s.isdigit():
            return pd.to_datetime(int(s), unit='D', origin='1899-12-30').to_pydatetime()
        _MONTH_MAP = {f"thg {i}": i for i in range(1, 13)}
        for m, num in _MONTH_MAP.items():
            if m in s:
                parts = re.split(r'\D+', s)
                parts = [p for p in parts if p.isdigit()]
                if len(parts) >= 2:
                    return datetime(int(parts[-1]), num, int(parts[0]))
        return None

    import re
    from datetime import datetime
    df_tq["date"]     = df_tq["Ngay"].apply(parse_vn_date)
    df_tq["DoanhThu"] = pd.to_numeric(df_tq["DoanhThu"], errors="coerce").fillna(0)
    df_tq["Volume"]   = pd.to_numeric(df_tq["Volume"],   errors="coerce").fillna(0)
    df_tq = df_tq.dropna(subset=["date"])
    df_tq = df_tq[~df_tq["AM_format"].astype(str).str.contains(",", na=False)]
    df_tq["Tinh"] = df_tq["AM_format"].apply(get_tinh)
    df_tq = df_tq[df_tq["Tinh"].notna() & (df_tq["Tinh"] != "")]
    
    df_tq["Tuan"] = df_tq["date"].apply(lambda d: f"{d.year}/{d.isocalendar()[1]:02d}" if d else None)
    
    for w in ['2026/25', '2026/24']:
        week_df = df_tq[df_tq['Tuan'] == w]
        total_rev = week_df['DoanhThu'].sum()
        total_vol = week_df['Volume'].sum()
        print(f"Week {w}: Total Revenue = {total_rev/1e6:.2f} million, Vol = {total_vol:,.0f}")

def ws_to_df(ss, name):
    data = ss.worksheet(name).get_all_values(value_render_option='UNFORMATTED_VALUE')
    df = pd.DataFrame(data[1:], columns=data[0])
    return df

if __name__ == '__main__':
    main()
