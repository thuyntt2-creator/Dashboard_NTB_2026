import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

excel_path = r"c:\Users\lap4all\Desktop\New folder\downloaded_user_sheet.xlsx"
df_tot = pd.read_excel(excel_path, sheet_name='dataGTC gốc full hàng')
df_tts = pd.read_excel(excel_path, sheet_name='dataGTC gốc TTS')

# Clean datasets
for df in [df_tot, df_tts]:
    df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce')
    df['% Gán'] = pd.to_numeric(df['% Gán'], errors='coerce')
    df['% GTC'] = pd.to_numeric(df['% GTC'], errors='coerce')

weeks = ['2026/21', '2026/22', '2026/23', '2026/24']

print("GTC Tổng (all 3 categories):")
for wk in weeks:
    sub = df_tot[(df_tot['Time'] == wk) & (df_tot['Chi tiết'] != 'Grand Total') & (df_tot['Loại Hàng'].isin(['Hàng Mới Ca 1', 'Hàng Mới Ca 2', 'Hàng Tồn']))]
    vol_tot = sub['Volume'].sum()
    vol_gtc = (sub['Volume'] * sub['% GTC']).sum()
    vol_gan = (sub['Volume'] * sub['% Gán']).sum()
    print(f"  {wk}: %Gán = {vol_gan/vol_tot*100:.2f}% | %GTC = {vol_gtc/vol_tot*100:.2f}%")

print("\nGTC TTS (Ca 1 + Ca 2 only):")
for wk in weeks:
    sub = df_tts[(df_tts['Time'] == wk) & (df_tts['Chi tiết'] != 'Grand Total') & (df_tts['Loại Hàng'].isin(['Hàng Mới Ca 1', 'Hàng Mới Ca 2']))]
    vol_tot = sub['Volume'].sum()
    vol_gtc = (sub['Volume'] * sub['% GTC']).sum()
    vol_gan = (sub['Volume'] * sub['% Gán']).sum()
    print(f"  {wk}: %Gán = {vol_gan/vol_tot*100:.2f}% | %GTC = {vol_gtc/vol_tot*100:.2f}%")
