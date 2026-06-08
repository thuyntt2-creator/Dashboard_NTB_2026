import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "vols_tao_don.xlsx")
output_path = os.path.join(workspace_dir, "scratch", "calculate_pivot_table_res.txt")

with open(output_path, "w", encoding="utf-8") as f:
    df = pd.read_excel(file_path, sheet_name="shopee_tiktok")
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Filter
    df_filtered = df[df['bat_on'] != 'BC Cũ/Không thuộc ĐCL'].copy()
    
    # Latest date D
    latest_dt = df_filtered['Date'].max()
    latest_date_str = latest_dt.strftime('%Y-%m-%d')
    f.write(f"Latest Date D: {latest_date_str}\n\n")
    
    # Weekday of D (0 = Monday, ..., 6 = Sunday)
    weekday = latest_dt.weekday()
    f.write(f"Weekday of D: {weekday} (where 0 is Monday and 6 is Sunday)\n\n")
    
    # Range of WTD: Monday of current week to D
    wtd_start = latest_dt - pd.Timedelta(days=weekday)
    wtd_end = latest_dt
    
    # Range of WTD-1: Monday of previous week to D-7
    wtd1_start = wtd_start - pd.Timedelta(days=7)
    wtd1_end = latest_dt - pd.Timedelta(days=7)
    
    # Range of WTD-2: Monday of 2 weeks ago to D-14
    wtd2_start = wtd_start - pd.Timedelta(days=14)
    wtd2_end = latest_dt - pd.Timedelta(days=14)
    
    f.write(f"WTD range: {wtd_start.strftime('%Y-%m-%d')} to {wtd_end.strftime('%Y-%m-%d')}\n")
    f.write(f"WTD-1 range: {wtd1_start.strftime('%Y-%m-%d')} to {wtd1_end.strftime('%Y-%m-%d')}\n")
    f.write(f"WTD-2 range: {wtd2_start.strftime('%Y-%m-%d')} to {wtd2_end.strftime('%Y-%m-%d')}\n\n")
    
    # Aggregate WTD, WTD-1, WTD-2 by Tỉnh
    def sum_range(df_sub, start, end):
        mask = (df_sub['Date'] >= start) & (df_sub['Date'] <= end)
        return df_sub[mask].groupby('Tỉnh')['Volume'].sum()

    wtd_sums = sum_range(df_filtered, wtd_start, wtd_end)
    wtd1_sums = sum_range(df_filtered, wtd1_start, wtd1_end)
    wtd2_sums = sum_range(df_filtered, wtd2_start, wtd2_end)
    
    # Daily columns
    d_dt = latest_dt
    d1_dt = latest_dt - pd.Timedelta(days=1)
    d2_dt = latest_dt - pd.Timedelta(days=2)
    d7_dt = latest_dt - pd.Timedelta(days=7)
    
    def sum_day(df_sub, dt):
        return df_sub[df_sub['Date'] == dt].groupby('Tỉnh')['Volume'].sum()
        
    d_sums = sum_day(df_filtered, d_dt)
    d1_sums = sum_day(df_filtered, d1_dt)
    d2_sums = sum_day(df_filtered, d2_dt)
    d7_sums = sum_day(df_filtered, d7_dt)
    
    # Build pivot table
    provinces = ['Bình Thuận', 'Khánh Hòa', 'Lâm Đồng', 'Ninh Thuận', 'Đắk Nông']
    pivot_rows = []
    
    for p in provinces:
        wtd = wtd_sums.get(p, 0)
        wtd1 = wtd1_sums.get(p, 0)
        wtd2 = wtd2_sums.get(p, 0)
        
        d_val = d_sums.get(p, 0)
        d1_val = d1_sums.get(p, 0)
        d2_val = d2_sums.get(p, 0)
        d7_val = d7_sums.get(p, 0)
        
        # Calculate ratios
        wtd_wtd2 = (wtd / wtd2 * 100) if wtd2 > 0 else 0
        wtd_wtd1 = (wtd / wtd1 * 100) if wtd1 > 0 else 0
        d_d7 = (d_val / d7_val * 100) if d7_val > 0 else 0
        d_d1 = (d_val / d1_val * 100) if d1_val > 0 else 0
        
        pivot_rows.append({
            'Tỉnh': p,
            'WTD-2': int(wtd2),
            'WTD-1': int(wtd1),
            'WTD': int(wtd),
            'WTD/WTD-2': round(wtd_wtd2, 1),
            'WTD/WTD-1': round(wtd_wtd1, 1),
            'D/D-7': round(d_d7, 1),
            'D/D-1': round(d_d1, 1),
            'D-7': int(d7_val),
            'D-2': int(d2_val),
            'D-1': int(d1_val),
            'D': int(d_val)
        })
        
    pivot_df = pd.DataFrame(pivot_rows)
    
    # Add Total Row
    total_wtd = pivot_df['WTD'].sum()
    total_wtd1 = pivot_df['WTD-1'].sum()
    total_wtd2 = pivot_df['WTD-2'].sum()
    total_d = pivot_df['D'].sum()
    total_d1 = pivot_df['D-1'].sum()
    total_d2 = pivot_df['D-2'].sum()
    total_d7 = pivot_df['D-7'].sum()
    
    total_row = {
        'Tỉnh': 'Tổng cộng',
        'WTD-2': int(total_wtd2),
        'WTD-1': int(total_wtd1),
        'WTD': int(total_wtd),
        'WTD/WTD-2': round((total_wtd / total_wtd2 * 100) if total_wtd2 > 0 else 0, 1),
        'WTD/WTD-1': round((total_wtd / total_wtd1 * 100) if total_wtd1 > 0 else 0, 1),
        'D/D-7': round((total_d / total_d7 * 100) if total_d7 > 0 else 0, 1),
        'D/D-1': round((total_d / total_d1 * 100) if total_d1 > 0 else 0, 1),
        'D-7': int(total_d7),
        'D-2': int(total_d2),
        'D-1': int(total_d1),
        'D': int(total_d)
    }
    
    pivot_df = pd.concat([pivot_df, pd.DataFrame([total_row])], ignore_index=True)
    
    f.write("PIVOT COMPARISON TABLE:\n")
    f.write(pivot_df.to_string(index=False) + "\n")

print("Done writing calculate_pivot_table_res.txt")
