# -*- coding: utf-8 -*-
import sys, gspread, traceback
import pandas as pd
sys.stdout.reconfigure(encoding='utf-8')
from google.oauth2.credentials import Credentials

try:
    creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
    gc = gspread.authorize(creds)
    sh = gc.open_by_key('1-p9VUXndK_7BoiT-a81UfTCbUi953XNmVBoXaTGis_c')
    
    ws = sh.worksheet('RawData')
    rows = ws.get_all_values()
    print('RawData rows:', len(rows))
    if rows:
        print('Header:', rows[0])
        for r in rows[1:6]:
            print(r)
        
        df = pd.DataFrame(rows[1:], columns=rows[0])
        col_bc = df.columns[0]
        col_date = df.columns[2]
        col_gan = df.columns[3]
        col_gtc = df.columns[4]
        
        df[col_gtc] = pd.to_numeric(df[col_gtc].str.replace(',', ''), errors='coerce').fillna(0)
        df[col_gan] = pd.to_numeric(df[col_gan].str.replace(',', ''), errors='coerce').fillna(0)
        
        agg = df.groupby(col_bc).agg({col_gtc: 'sum', col_gan: 'sum'}).reset_index()
        
        print("\n=== RAWDATA AGGREGATED ===")
        bc_alert = ['Tân Hà', 'Quảng Khê', 'Lang Biang', 'Đức An', 'Hòa Ninh', 'Đức Trọng', 'Tây Nha Trang', "D'Ran", 'Bắc Cam Ranh']
        for bc in bc_alert:
            m = agg[agg[col_bc].str.contains(bc, case=False, na=False)]
            for _, r in m.iterrows():
                print(f"{r[col_bc]:<30} | Gan: {r[col_gan]:<5.0f} | GTC: {r[col_gtc]:<5.0f}")

except Exception as e:
    traceback.print_exc()
