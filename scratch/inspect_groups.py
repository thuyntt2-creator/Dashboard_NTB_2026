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
    
    print("Columns:", df.columns.tolist())
    print("First few rows:")
    print(df.head())
    
    # check unique values of Vung
    print("Vung unique values:", df['Vung'].unique().tolist())
    
    # check Ngay parsing
    def parse_nhom_date(val):
        if isinstance(val, (int, float)):
            return pd.to_datetime(val, unit='D', origin='1899-12-30')
        s = str(val).strip()
        if s.isdigit():
            return pd.to_datetime(int(s), unit='D', origin='1899-12-30')
        return pd.to_datetime(s, errors='coerce')
        
    df['Ngay'] = df['Ngay'].apply(parse_nhom_date)
    print("Dates in phan_nhom:", sorted(df['Ngay'].dropna().unique()))
    
    # Let's filter to NTB
    df_ntb = df[df['Vung'].astype(str).str.startswith('NTB')].copy()
    df_ntb['DT'] = pd.to_numeric(df_ntb['DT'], errors='coerce').fillna(0)
    
    # Let's see the sum of DT by group for each unique date
    for dt in sorted(df_ntb['Ngay'].dropna().unique()):
        day_df = df_ntb[df_ntb['Ngay'] == dt]
        total = day_df['DT'].sum()
        print(f"\nDate: {dt.date()} | Total DT: {total:,.2f}")
        by_group = day_df.groupby('Nhom')['DT'].sum()
        for group, val in by_group.items():
            pct = val / total * 100 if total > 0 else 0
            print(f"  Group {group}: {val:,.2f} ({pct:.1f}%)")

if __name__ == '__main__':
    main()
