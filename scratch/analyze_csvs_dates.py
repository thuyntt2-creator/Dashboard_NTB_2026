import pandas as pd
import os

out_path = "scratch/analyze_csvs_dates_out.txt"

with open(out_path, "w", encoding="utf-8") as f:
    f.write("=== ANALYSIS OF CSV DATES AND LATEST METRICS ===\n")
    
    # 1. Check ops_gtc.csv
    if os.path.exists('ops_gtc.csv'):
        df = pd.read_csv('ops_gtc.csv')
        f.write("\n--- File: ops_gtc.csv ---\n")
        f.write(f"Shape: {df.shape}\n")
        unique_times = sorted(df['Time'].dropna().unique().tolist())
        f.write(f"Latest 5 times: {unique_times[-5:]}\n")
        
        # Let's see the metrics for the latest date
        latest_time = unique_times[-1]
        f.write(f"Latest time data summary ({latest_time}):\n")
        df_latest = df[df['Time'] == latest_time]
        f.write(f"Number of rows: {len(df_latest)}\n")
        # Let's aggregate by AM and Province for this latest date
        # Convert columns to numeric
        for col in ['Volume', 'Sản Lượng Giao Thành Công', 'Sản Lượng Tồn', 'Sản Lượng Chưa Gán']:
            df_latest[col] = pd.to_numeric(df_latest[col], errors='coerce').fillna(0)
        
        # Calculate %GTC as sum(GTC) / sum(Volume)
        grouped = df_latest.groupby(['AM', 'Tỉnh']).agg(
            Vol=('Volume', 'sum'),
            GTC_vol=('Sản Lượng Giao Thành Công', 'sum'),
            Ton_vol=('Sản Lượng Tồn', 'sum'),
            ChuaGan_vol=('Sản Lượng Chưa Gán', 'sum')
        ).reset_index()
        grouped['% GTC'] = (grouped['GTC_vol'] / grouped['Vol'] * 100).round(2)
        grouped['% Tồn'] = (grouped['Ton_vol'] / grouped['Vol'] * 100).round(2)
        grouped['% Chưa Gán'] = (grouped['ChuaGan_vol'] / grouped['Vol'] * 100).round(2)
        grouped = grouped.sort_values(by='% GTC')
        f.write(grouped.to_string() + "\n")

    # 2. Check ops_ltc.csv
    if os.path.exists('ops_ltc.csv'):
        df_ltc = pd.read_csv('ops_ltc.csv')
        f.write("\n--- File: ops_ltc.csv ---\n")
        f.write(f"Shape: {df_ltc.shape}\n")
        unique_times_ltc = sorted(df_ltc['Time'].dropna().unique().tolist())
        f.write(f"Latest 5 times: {unique_times_ltc[-5:]}\n")
        latest_time_ltc = unique_times_ltc[-1]
        f.write(f"Latest time data summary ({latest_time_ltc}):\n")
        df_ltc_latest = df_ltc[df_ltc['Time'] == latest_time_ltc]
        # Aggregate by AM and Province
        for col in ['Volume', 'Sản Lượng Lấy Thành Công']:
            df_ltc_latest[col] = pd.to_numeric(df_ltc_latest[col], errors='coerce').fillna(0)
        grouped_ltc = df_ltc_latest.groupby(['AM', 'Tỉnh']).agg(
            Vol=('Volume', 'sum'),
            LTC_vol=('Sản Lượng Lấy Thành Công', 'sum')
        ).reset_index()
        grouped_ltc['% LTC'] = (grouped_ltc['LTC_vol'] / grouped_ltc['Vol'] * 100).round(2)
        grouped_ltc = grouped_ltc.sort_values(by='% LTC')
        f.write(grouped_ltc.to_string() + "\n")

    # 3. Check ODR TTS.csv
    if os.path.exists('ODR TTS.csv'):
        df_odr = pd.read_csv('ODR TTS.csv')
        f.write("\n--- File: ODR TTS.csv ---\n")
        f.write(f"Shape: {df_odr.shape}\n")
        unique_times_odr = sorted(df_odr['Time'].dropna().unique().tolist())
        f.write(f"Latest 5 times: {unique_times_odr[-5:]}\n")
        latest_time_odr = unique_times_odr[-1]
        f.write(f"Latest time data summary ({latest_time_odr}):\n")
        df_odr_latest = df_odr[df_odr['Time'] == latest_time_odr]
        # Clean ODR
        df_odr_latest['%Ontime'] = df_odr_latest['%Ontime'].astype(str).str.replace('%', '').astype(float)
        # We need GTC weighted average %Ontime
        df_odr_latest['GTC'] = pd.to_numeric(df_odr_latest['GTC'], errors='coerce').fillna(0)
        df_odr_latest['Ontime_vol'] = df_odr_latest['GTC'] * df_odr_latest['%Ontime'] / 100
        grouped_odr = df_odr_latest.groupby(['Quản lý']).agg(
            GTC_tot=('GTC', 'sum'),
            Ontime_tot=('Ontime_vol', 'sum')
        ).reset_index()
        grouped_odr['% ODR'] = (grouped_odr['Ontime_tot'] / grouped_odr['GTC_tot'] * 100).round(2)
        f.write(grouped_odr.to_string() + "\n")

    # 4. Check buu_cuc_bat_on.csv
    if os.path.exists('buu_cuc_bat_on.csv'):
        f.write("\n--- File: buu_cuc_bat_on.csv ---\n")
        df_bo = pd.read_csv('buu_cuc_bat_on.csv')
        # Print column names
        f.write(f"Columns: {df_bo.columns.tolist()}\n")
        # Let's inspect rows from index 2 onwards
        df_bo_data = df_bo.iloc[2:].copy()
        # Set column names from row 2
        df_bo_data.columns = df_bo.iloc[2]
        df_bo_data = df_bo_data.iloc[1:] # remove the row used for headers
        f.write(f"Rows of warning: {len(df_bo_data)}\n")
        f.write(df_bo_data[['vung_giao', 'tinh_giao', 'kho_giao_name', 'BL LM', '%BL LM >5 ngay', 'tinh_hinh', 'ly_do_bat_on']].head(20).to_string() + "\n")

print("Done checking CSV dates!")
