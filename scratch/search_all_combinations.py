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
    
    # Extract Tinh from Vung
    df_ntb = df[df['Vung'].astype(str).str.startswith('NTB')].copy()
    df_ntb['Tinh'] = (df_ntb['Vung']
                      .str.replace('NTB-','',regex=False)
                      .str.replace(r'^BD$','Bình Thuận',regex=True)
                      .str.strip())
                      
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
    
    # We want to find a group breakdown matching:
    # A ~ 251.7
    # BCD ~ 261.4
    # EF ~ 309.8
    # G ~ 37.9
    # Let's search over all possible combinations of dates (like range of dates)
    # The date range length can be 1 to 10 days.
    
    dates = sorted(df_ntb['Ngay'].dropna().unique())
    matches = []
    
    for i in range(len(dates)):
        for j in range(i, min(i + 10, len(dates))):
            start_date = dates[i]
            end_date = dates[j]
            sub_df = df_ntb[(df_ntb['Ngay'] >= start_date) & (df_ntb['Ngay'] <= end_date)]
            
            by_group = sub_df.groupby('Nhom')['Revenue'].sum()
            a_val = by_group.get('A', 0) / 1e6
            bcd_val = by_group.get('BCD', 0) / 1e6
            ef_val = by_group.get('EF', 0) / 1e6
            g_val = by_group.get('G', 0) / 1e6
            
            # Distance function to our target: A=251.7, BCD=261.4, EF=309.8, G=37.9
            dist = (
                abs(a_val - 251.7) +
                abs(bcd_val - 261.4) +
                abs(ef_val - 309.8) +
                abs(g_val - 37.9)
            )
            
            matches.append((dist, start_date, end_date, a_val, bcd_val, ef_val, g_val))
            
    matches.sort(key=lambda x: x[0])
    
    print("Top 10 closest date range matches for NTB Region:")
    for dist, start, end, a, bcd, ef, g in matches[:10]:
        total = a + bcd + ef + g
        print(f"Dist: {dist:.2f} | {start.date()} to {end.date()} (Total: {total:.1f}M)")
        print(f"  A: {a:.1f}M, BCD: {bcd:.1f}M, EF: {ef:.1f}M, G: {g:.1f}M")

if __name__ == '__main__':
    main()
