import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

excel_path = r"c:\Users\lap4all\Desktop\New folder\downloaded_user_sheet.xlsx"
df = pd.read_excel(excel_path, sheet_name='dataLTC full hàng')

df_cocau = pd.read_excel(excel_path, sheet_name='cocau')
df_cocau['BC_norm'] = df_cocau['BC'].str.strip().str.upper()
bc_to_am = dict(zip(df_cocau['BC_norm'], df_cocau['Am']))

df['BC_norm'] = df['Chi tiết'].str.strip().str.upper()
df['AM_mapped'] = df['BC_norm'].map(bc_to_am)

for week in ['2026/23', '2026/24']:
    subset = df[(df['AM_mapped'] == 'Nguyễn Duy Long') & (df['Time'] == week)].copy()
    
    # Values
    V = subset['Volume']
    G = subset['%Gán']
    L = subset['%LTC']
    
    # 1. (V * L).sum() / V.sum()
    c1 = (V * L).sum() / V.sum()
    
    # 2. (V * G * L).sum() / (V * G).sum()
    c2 = (V * G * L).sum() / (V * G).sum()
    
    # 3. (V * G * L).sum() / V.sum()
    c3 = (V * G * L).sum() / V.sum()
    
    # 4. (V * L).sum() / (V * G).sum()
    c4 = (V * L).sum() / (V * G).sum()
    
    print(f"\nWeek {week}:")
    print(f"  Comb 1: (V * L).sum() / V.sum()                 = {c1*100:.4f}%")
    print(f"  Comb 2: (V * G * L).sum() / (V * G).sum()       = {c2*100:.4f}%")
    print(f"  Comb 3: (V * G * L).sum() / V.sum()             = {c3*100:.4f}%")
    print(f"  Comb 4: (V * L).sum() / (V * G).sum()           = {c4*100:.4f}%")
