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
    
    df_ntb['DT_vol'] = pd.to_numeric(df_ntb['DT'], errors='coerce').fillna(0)
    df_ntb['AOV'] = pd.to_numeric(df_ntb['AOV'], errors='coerce').fillna(0)
    df_ntb['Revenue'] = df_ntb['DT_vol'] * df_ntb['AOV']
    
    dates = sorted(df_ntb['Ngay'].dropna().unique())
    print("--- ROLLING 7 DAYS ---")
    for i in range(6, len(dates)):
        end_date = dates[i]
        start_date = dates[i-6]
        period_df = df_ntb[(df_ntb['Ngay'] >= start_date) & (df_ntb['Ngay'] <= end_date)]
        total_rev = period_df['Revenue'].sum()
        by_group = period_df.groupby('Nhom')['Revenue'].sum()
        
        # Check if it matches roughly
        a_val = by_group.get('A', 0) / 1e6
        bcd_val = by_group.get('BCD', 0) / 1e6
        ef_val = by_group.get('EF', 0) / 1e6
        g_val = by_group.get('G', 0) / 1e6
        
        print(f"Ending {end_date.date()} (Total: {total_rev/1e6:.1f}M):")
        print(f"  A: {a_val:.1f}M, BCD: {bcd_val:.1f}M, EF: {ef_val:.1f}M, G: {g_val:.1f}M")

if __name__ == '__main__':
    main()
