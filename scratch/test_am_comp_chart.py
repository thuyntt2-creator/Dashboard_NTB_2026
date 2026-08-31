import pandas as pd
import numpy as np
import os
import unicodedata
import matplotlib.pyplot as plt

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
user_file = os.path.join(workspace_dir, "downloaded_user_sheet.xlsx")
output_file = os.path.join(workspace_dir, "scratch", "test_am_comp_chart_res.txt")

with open(output_file, "w", encoding="utf-8") as f:
    df_gtc_full = pd.read_excel(user_file, sheet_name='dataGTC gốc full hàng')
    df_gtc_tts = pd.read_excel(user_file, sheet_name='dataGTC gốc TTS')
    df_ltc_full = pd.read_excel(user_file, sheet_name='dataLTC full hàng')
    df_ltc_tts = pd.read_excel(user_file, sheet_name='dataLTC TTS')
    df_odr_full = pd.read_excel(user_file, sheet_name='dataODRfull hàng ')
    df_odr_tts = pd.read_excel(user_file, sheet_name='dataODR TTS')
    df_cocau = pd.read_excel(user_file, sheet_name='cocau')
    
    def normalize_name(name):
        if pd.isna(name): return ""
        return unicodedata.normalize('NFC', str(name).strip()).upper()

    df_cocau['BC_norm'] = df_cocau['BC'].apply(normalize_name)
    bc_to_am = dict(zip(df_cocau['BC_norm'], df_cocau['Am']))

    def map_am(bc_name):
        return bc_to_am.get(normalize_name(bc_name), None)

    for df in [df_gtc_full, df_gtc_tts, df_ltc_full, df_ltc_tts, df_odr_full, df_odr_tts]:
        if 'Chi tiết' in df.columns:
            df['AM_mapped'] = df['Chi tiết'].apply(map_am)

    # Clean numeric columns
    for df in [df_gtc_full, df_gtc_tts]:
        for col in ['Volume', '% Gán', '% GTC']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    for df in [df_ltc_full, df_ltc_tts]:
        for col in ['Volume', '%Gán', '%LTC']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    for df in [df_odr_full, df_odr_tts]:
        for col in ['GTC', '%Ontime']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    # Let's filter for current week W24 (2026/24)
    week_key = '2026/24'
    
    # 1. Volume by AM
    df_gtc_w24 = df_gtc_full[(df_gtc_full['Loại Hàng'].isin(['Hàng Mới Ca 1', 'Hàng Mới Ca 2'])) & (df_gtc_full['Time'] == week_key) & (df_gtc_full['Chi tiết'] != 'Grand Total')].copy()
    am_vol = df_gtc_w24.groupby('AM_mapped')['Volume'].sum().reset_index()
    
    # 2. GTC rate by AM
    df_gtc_w24['Vol_GTC'] = df_gtc_w24['Volume'] * df_gtc_w24['% GTC']
    am_gtc_grouped = df_gtc_w24.groupby('AM_mapped').agg(v=('Volume', 'sum'), vg=('Vol_GTC', 'sum')).reset_index()
    am_gtc_grouped['% GTC'] = (am_gtc_grouped['vg'] / am_gtc_grouped['v']).fillna(0)
    
    # 3. LTC rate by AM
    df_ltc_w24 = df_ltc_full[(df_ltc_full['Cấp quản lý'] != 'Grand Total') & (df_ltc_full['Time'] == week_key)].copy()
    df_ltc_w24['Vol_Gan'] = df_ltc_w24['Volume'] * df_ltc_w24['%Gán']
    df_ltc_w24['Vol_LTC'] = df_ltc_w24['Volume'] * df_ltc_w24['%LTC']
    am_ltc_grouped = df_ltc_w24.groupby('AM_mapped').agg(v=('Vol_Gan', 'sum'), vl=('Vol_LTC', 'sum')).reset_index()
    am_ltc_grouped['% LTC'] = (am_ltc_grouped['vl'] / am_ltc_grouped['v']).fillna(0)
    
    # 4. ODR rate by AM
    df_odr_w24 = df_odr_full[(df_odr_full['Time'] == week_key) & (~df_odr_full['Quản lý'].astype(str).str.contains('Grand Total|Tổng cộng', case=False, na=False))].copy()
    df_odr_w24['Vol_Ontime'] = df_odr_w24['GTC'] * df_odr_w24['%Ontime']
    am_odr_grouped = df_odr_w24.groupby('AM_mapped').agg(v=('GTC', 'sum'), vo=('Vol_Ontime', 'sum')).reset_index()
    am_odr_grouped['% ODR'] = (am_odr_grouped['vo'] / am_odr_grouped['v']).fillna(0)
    
    # Merge all metrics for all AMs
    all_ams = df_cocau['Am'].dropna().unique()
    f.write(f"Total AMs in cocau: {len(all_ams)}\n\n")
    
    metrics_df = pd.DataFrame({'AM': all_ams})
    metrics_df = metrics_df.merge(am_vol, left_on='AM', right_on='AM_mapped', how='left').drop(columns='AM_mapped').rename(columns={'Volume': 'Volume_W24'}).fillna(0)
    metrics_df = metrics_df.merge(am_gtc_grouped[['AM_mapped', '% GTC']], left_on='AM', right_on='AM_mapped', how='left').drop(columns='AM_mapped').rename(columns={'% GTC': 'GTC_W24'}).fillna(0)
    metrics_df = metrics_df.merge(am_ltc_grouped[['AM_mapped', '% LTC']], left_on='AM', right_on='AM_mapped', how='left').drop(columns='AM_mapped').rename(columns={'% LTC': 'LTC_W24'}).fillna(0)
    metrics_df = metrics_df.merge(am_odr_grouped[['AM_mapped', '% ODR']], left_on='AM', right_on='AM_mapped', how='left').drop(columns='AM_mapped').rename(columns={'% ODR': 'ODR_W24'}).fillna(0)
    
    f.write("Merged AM metrics W24:\n")
    f.write(metrics_df.to_string(index=False) + "\n")

print("Inspection completed.")
