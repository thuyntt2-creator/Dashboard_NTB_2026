import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

excel_path = r"c:\Users\lap4all\Desktop\New folder\downloaded_user_sheet.xlsx"
df = pd.read_excel(excel_path, sheet_name='dataGTC gốc full hàng')

df_cocau = pd.read_excel(excel_path, sheet_name='cocau')
df_cocau['BC_norm'] = df_cocau['BC'].str.strip().str.upper()
bc_to_am = dict(zip(df_cocau['BC_norm'], df_cocau['Am']))

df['BC_norm'] = df['Chi tiết'].str.strip().str.upper()
df['AM_mapped'] = df['BC_norm'].map(bc_to_am)

for am_name in ['Trầm Hữu Tiến', 'Huỳnh Thị Kim Chi', 'Thái Thị Thanh Thư', 'Nguyễn Duy Long']:
    am_df = df[(df['AM_mapped'] == am_name) & (df['Time'] == '2026/24')]
    
    # Scenario 1: All 3 kinds of goods (Ca 1, Ca 2, Tồn)
    vol_tot_3 = am_df['Volume'].sum()
    vol_gtc_3 = (am_df['Volume'] * am_df['% GTC']).sum()
    pct_gtc_3 = vol_gtc_3 / vol_tot_3 if vol_tot_3 > 0 else 0
    
    # Scenario 2: Only 'Hàng Mới Ca 1' and 'Hàng Mới Ca 2'
    am_m2 = am_df[am_df['Loại Hàng'].isin(['Hàng Mới Ca 1', 'Hàng Mới Ca 2'])]
    vol_tot_2 = am_m2['Volume'].sum()
    vol_gtc_2 = (am_m2['Volume'] * am_m2['% GTC']).sum()
    pct_gtc_2 = vol_gtc_2 / vol_tot_2 if vol_tot_2 > 0 else 0
    
    print(f"AM: {am_name}")
    print(f"  Scenario 1 (All 3 categories): {pct_gtc_3*100:.2f}%")
    print(f"  Scenario 2 (Only Ca 1 + Ca 2): {pct_gtc_2*100:.2f}%")
