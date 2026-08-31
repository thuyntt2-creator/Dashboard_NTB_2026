import pandas as pd
import numpy as np
import os

out_path = "scratch/analyze_ops_overall_out.txt"

with open(out_path, "w", encoding="utf-8") as f:
    f.write("=== REGION OVERALL METRICS ===\n")
    
    # 1. ODR Analysis
    if os.path.exists('ODR TTS.csv'):
        df_odr = pd.read_csv('ODR TTS.csv')
        df_odr['%Ontime'] = df_odr['%Ontime'].astype(str).str.replace('%', '').astype(float)
        df_odr['GTC'] = pd.to_numeric(df_odr['GTC'], errors='coerce').fillna(0)
        df_odr['Ontime_vol'] = df_odr['GTC'] * df_odr['%Ontime'] / 100
        
        # Unique dates
        dates = sorted(df_odr['Time'].dropna().unique().tolist())
        f.write(f"ODR Unique dates count: {len(dates)}\n")
        
        # Calculate ODR for June 13, June 12, June 6
        target_dates = ['2026-06-13 - Thứ 7', '2026-06-12 - Thứ 6', '2026-06-06 - Thứ 7']
        f.write("\n--- ODR by Date ---\n")
        for d in target_dates:
            if d in dates:
                sub = df_odr[df_odr['Time'] == d]
                tot_gtc = sub['GTC'].sum()
                tot_ontime = sub['Ontime_vol'].sum()
                avg_odr = (tot_ontime / tot_gtc * 100) if tot_gtc > 0 else 0
                f.write(f"Date: {d} | Total GTC: {tot_gtc:,.0f} | Overall ODR: {avg_odr:.2f}%\n")
                
                # By Province (Quản lý)
                prov_grouped = sub.groupby('Quản lý').agg(
                    GTC=('GTC', 'sum'),
                    Ontime=('Ontime_vol', 'sum')
                ).reset_index()
                prov_grouped['ODR'] = (prov_grouped['Ontime'] / prov_grouped['GTC'] * 100).round(2)
                f.write(prov_grouped.to_string() + "\n\n")
                
    # 2. GTC Analysis (Giao thành công)
    if os.path.exists('ops_gtc.csv'):
        df_gtc = pd.read_csv('ops_gtc.csv')
        for col in ['Volume', 'Sản Lượng Giao Thành Công', 'Sản Lượng Tồn', 'Sản Lượng Chưa Gán', 'Sản Lượng Chuyển Trả']:
            df_gtc[col] = pd.to_numeric(df_gtc[col], errors='coerce').fillna(0)
        
        df_gtc['GTC_vol'] = df_gtc['Sản Lượng Giao Thành Công']
        df_gtc['CT_vol'] = df_gtc['Sản Lượng Chuyển Trả']
        df_gtc['Ton_vol'] = df_gtc['Sản Lượng Tồn']
        df_gtc['ChuaGan_vol'] = df_gtc['Sản Lượng Chưa Gán']
        
        dates_gtc = sorted(df_gtc['Time'].dropna().unique().tolist())
        target_dates_gtc = ['2026-06-13 - Thứ 7', '2026-06-12 - Thứ 6', '2026-06-06 - Thứ 7']
        f.write("\n--- GTC (Delivery) Metrics by Date ---\n")
        for d in target_dates_gtc:
            if d in dates_gtc:
                sub = df_gtc[df_gtc['Time'] == d]
                tot_vol = sub['Volume'].sum()
                tot_gtc_vol = sub['GTC_vol'].sum()
                tot_ct_vol = sub['CT_vol'].sum()
                tot_ton_vol = sub['Ton_vol'].sum()
                tot_chuagan = sub['ChuaGan_vol'].sum()
                
                gtc_rate = (tot_gtc_vol / tot_vol * 100) if tot_vol > 0 else 0
                ct_rate = (tot_ct_vol / tot_vol * 100) if tot_vol > 0 else 0
                ton_rate = (tot_ton_vol / tot_vol * 100) if tot_vol > 0 else 0
                cg_rate = (tot_chuagan / tot_vol * 100) if tot_vol > 0 else 0
                
                f.write(f"Date: {d} | Total Vol: {tot_vol:,.0f} | GTC: {gtc_rate:.2f}% | CT: {ct_rate:.2f}% | Tồn: {ton_rate:.2f}% | Chưa Gán: {cg_rate:.2f}%\n")
                
                # Group by AM to see the worst performers
                am_grouped = sub.groupby('AM').agg(
                    Vol=('Volume', 'sum'),
                    GTC_v=('GTC_vol', 'sum'),
                    Ton_v=('Ton_vol', 'sum')
                ).reset_index()
                am_grouped['% GTC'] = (am_grouped['GTC_v'] / am_grouped['Vol'] * 100).round(2)
                am_grouped['% Tồn'] = (am_grouped['Ton_v'] / am_grouped['Vol'] * 100).round(2)
                am_grouped = am_grouped.sort_values(by='% GTC').head(5)
                f.write("Worst 5 AMs by %GTC:\n" + am_grouped.to_string() + "\n\n")

    # 3. LTC Analysis (Lấy thành công)
    if os.path.exists('ops_ltc.csv'):
        df_ltc = pd.read_csv('ops_ltc.csv')
        for col in ['Volume', 'Sản Lượng Lấy Thành Công', 'Sản Lượng Gán']:
            df_ltc[col] = pd.to_numeric(df_ltc[col], errors='coerce').fillna(0)
            
        dates_ltc = sorted(df_ltc['Time'].dropna().unique().tolist())
        target_dates_ltc = ['2026-06-13 - Thứ 7', '2026-06-12 - Thứ 6', '2026-06-06 - Thứ 7']
        f.write("\n--- LTC (Pick-up) Metrics by Date ---\n")
        for d in target_dates_ltc:
            if d in dates_ltc:
                sub = df_ltc[df_ltc['Time'] == d]
                tot_vol = sub['Volume'].sum()
                tot_ltc_vol = sub['Sản Lượng Lấy Thành Công'].sum()
                tot_gan = sub['Sản Lượng Gán'].sum()
                
                ltc_rate = (tot_ltc_vol / tot_vol * 100) if tot_vol > 0 else 0
                gan_rate = (tot_gan / tot_vol * 100) if tot_vol > 0 else 0
                
                f.write(f"Date: {d} | Total Vol: {tot_vol:,.0f} | LTC: {ltc_rate:.2f}% | Gán: {gan_rate:.2f}%\n")
                
                # Worst AMs by LTC
                am_grouped_ltc = sub.groupby('AM').agg(
                    Vol=('Volume', 'sum'),
                    LTC_v=('Sản Lượng Lấy Thành Công', 'sum')
                ).reset_index()
                am_grouped_ltc['% LTC'] = (am_grouped_ltc['LTC_v'] / am_grouped_ltc['Vol'] * 100).round(2)
                am_grouped_ltc = am_grouped_ltc.sort_values(by='% LTC').head(5)
                f.write("Worst 5 AMs by %LTC:\n" + am_grouped_ltc.to_string() + "\n\n")

print("Done calculating overall metrics!")
