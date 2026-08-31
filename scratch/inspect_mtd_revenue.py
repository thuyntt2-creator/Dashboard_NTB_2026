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
    ws = ss.worksheet("phan_nhom")
    data = ws.get_all_values(value_render_option='UNFORMATTED_VALUE')
    df = pd.DataFrame(data[1:], columns=data[0])
    
    df_ntb = df[df['Vung'].astype(str).str.startswith('NTB')].copy()
    def parse_nhom_date(val):
        if isinstance(val, (int, float)):
            return pd.to_datetime(val, unit='D', origin='1899-12-30')
        s = str(val).strip()
        if s.isdigit():
            return pd.to_datetime(int(s), unit='D', origin='1899-12-30')
        return pd.to_datetime(s, errors='coerce')
    df_ntb['Ngay'] = df_ntb['Ngay'].apply(parse_nhom_date)
    
    df_ntb['MTD_vol'] = pd.to_numeric(df_ntb['MTD'], errors='coerce').fillna(0)
    df_ntb['AOV'] = pd.to_numeric(df_ntb['AOV'], errors='coerce').fillna(0)
    df_ntb['MTD_Revenue'] = df_ntb['MTD_vol'] * df_ntb['AOV']
    
    for dt in [pd.Timestamp('2026-06-17'), pd.Timestamp('2026-06-10')]:
        day_df = df_ntb[df_ntb['Ngay'] == dt]
        total_rev = day_df['MTD_Revenue'].sum()
        total_vol = day_df['MTD_vol'].sum()
        print(f"\nDate: {dt.date()}")
        print(f"  Total MTD Vol: {total_vol:,.0f} orders")
        print(f"  Total MTD Revenue: {total_rev:,.0f} VND ({total_rev/1e6:.1f} million)")
        
        by_group = day_df.groupby('Nhom')['MTD_Revenue'].sum()
        for group, val in by_group.items():
            pct = val / total_rev * 100 if total_rev > 0 else 0
            print(f"    Group {group}: {val:,.0f} VND ({val/1e6:.1f} million, {pct:.1f}%)")

if __name__ == '__main__':
    main()
