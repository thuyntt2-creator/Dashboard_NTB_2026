import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

excel_path = r"c:\Users\lap4all\Desktop\New folder\downloaded_user_sheet.xlsx"
df_tot = pd.read_excel(excel_path, sheet_name='dataLTC full hàng')
df_tts = pd.read_excel(excel_path, sheet_name='dataLTC TTS')

weeks = ['2026/21', '2026/22', '2026/23', '2026/24']

# Clean datasets
for df in [df_tot, df_tts]:
    df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce')
    df['%Gán'] = pd.to_numeric(df['%Gán'], errors='coerce')
    df['%LTC'] = pd.to_numeric(df['%LTC'], errors='coerce')

print("LTC Total rates per week:")
for wk in weeks:
    sub_tot = df_tot[(df_tot['Time'] == wk) & (df_tot['Cấp quản lý'] != 'Grand Total')]
    
    # Formula A: (V * L) / V
    r_a = (sub_tot['Volume'] * sub_tot['%LTC']).sum() / sub_tot['Volume'].sum()
    
    # Formula B: (V * G * L) / (V * G)
    r_b = (sub_tot['Volume'] * sub_tot['%Gán'] * sub_tot['%LTC']).sum() / (sub_tot['Volume'] * sub_tot['%Gán']).sum()
    
    print(f"  {wk}: Formula A = {r_a*100:.2f}% | Formula B = {r_b*100:.2f}%")

print("\nLTC TTS rates per week:")
for wk in weeks:
    sub_tts = df_tts[(df_tts['Time'] == wk) & (df_tts['Cấp quản lý'] != 'Grand Total')]
    
    # Formula A: (V * L) / V
    r_a = (sub_tts['Volume'] * sub_tts['%LTC']).sum() / sub_tts['Volume'].sum()
    
    # Formula B: (V * G * L) / (V * G)
    r_b = (sub_tts['Volume'] * sub_tts['%Gán'] * sub_tts['%LTC']).sum() / (sub_tts['Volume'] * sub_tts['%Gán']).sum()
    
    print(f"  {wk}: Formula A = {r_a*100:.2f}% | Formula B = {r_b*100:.2f}%")
