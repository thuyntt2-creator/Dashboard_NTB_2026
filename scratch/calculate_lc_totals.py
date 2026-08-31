import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
user_file = os.path.join(workspace_dir, "downloaded_user_sheet.xlsx")
output_file = os.path.join(workspace_dir, "scratch", "calculate_lc_totals_res.txt")

with open(output_file, "w", encoding="utf-8") as f:
    df_lc = pd.read_excel(user_file, sheet_name="data rớt LC")
    
    # 1. Clean columns
    df_lc['Vol cần LC'] = pd.to_numeric(df_lc['Vol cần LC'], errors='coerce').fillna(0)
    
    def parse_pct(val):
        if pd.isna(val):
            return 0.0
        if isinstance(val, (int, float)):
            return float(val)
        val_str = str(val).strip().replace('%', '')
        try:
            return float(val_str) / 100.0
        except:
            return 0.0
            
    df_lc['pct_float'] = df_lc['%_rot_lc'].apply(parse_pct)
    # Re-calculate Vol rớt LC using Vol cần LC * %_rot_lc
    df_lc['Vol rớt LC'] = df_lc['Vol cần LC'] * df_lc['pct_float']
    
    f.write("--- Weekly Totals for data rớt LC ---\n")
    # Group by week and calculate sum of Vol cần LC, sum of Vol rớt LC, and overall %_rot_lc
    weekly_summary = df_lc.groupby('Tuần').agg(
        total_need_lc=('Vol cần LC', 'sum'),
        total_fail_lc=('Vol rớt LC', 'sum'),
        num_records=('Vol cần LC', 'count')
    ).reset_index()
    weekly_summary['overall_pct_fail'] = (weekly_summary['total_fail_lc'] / weekly_summary['total_need_lc']).fillna(0)
    
    f.write(weekly_summary.to_string(index=False) + "\n\n")
    
    # Let's inspect the specific comparison between W23 and W24
    w23_row = weekly_summary[weekly_summary['Tuần'] == 'Tuần 23']
    w24_row = weekly_summary[weekly_summary['Tuần'] == 'Tuần 24']
    
    if not w23_row.empty and not w24_row.empty:
        w23_need = w23_row['total_need_lc'].values[0]
        w23_fail = w23_row['total_fail_lc'].values[0]
        w23_pct = w23_row['overall_pct_fail'].values[0]
        
        w24_need = w24_row['total_need_lc'].values[0]
        w24_fail = w24_row['total_fail_lc'].values[0]
        w24_pct = w24_row['overall_pct_fail'].values[0]
        
        f.write("Comparison (W23 vs W24):\n")
        f.write(f"W23: Vol Cần = {w23_need:,.1f}, Vol Rớt = {w23_fail:,.1f}, % Rớt = {w23_pct:.4%}\n")
        f.write(f"W24: Vol Cần = {w24_need:,.1f}, Vol Rớt = {w24_fail:,.1f}, % Rớt = {w24_pct:.4%}\n")
        f.write(f"Difference in % Rớt: {w24_pct - w23_pct:+.4%}\n\n")
        
    # 2. Top 20 Post Offices (Bưu cục) in W24 sorted by % rớt lc descending
    f.write("--- Top 20 post offices in W24 sorted by % rớt lc ---\n")
    df_w24 = df_lc[df_lc['Tuần'] == 'Tuần 24'].copy()
    
    # Group by post office name ('Chi tiết' column)
    # Wait, does the user want the raw records, or aggregate by post office?
    # Usually, if there are multiple records per post office, we aggregate.
    # Let's check both ways.
    # Grouped by Chi tiết:
    po_grouped = df_w24.groupby('Chi tiết').agg(
        vol_can_sum=('Vol cần LC', 'sum'),
        vol_rot_sum=('Vol rớt LC', 'sum')
    ).reset_index()
    po_grouped['pct_fail'] = (po_grouped['vol_rot_sum'] / po_grouped['vol_can_sum']).fillna(0)
    
    top_20_agg = po_grouped.sort_values(by='pct_fail', ascending=False).head(20)
    f.write("\nAggregate by Post Office (Chi tiết):\n")
    f.write(top_20_agg.to_string(index=False) + "\n\n")
    
    # Raw records:
    top_20_raw = df_w24.sort_values(by='pct_float', ascending=False).head(20)
    f.write("\nRaw Records:\n")
    f.write(top_20_raw[['Quản lý', 'Chi tiết', 'Loại ngày', 'Vol cần LC', '%_rot_lc', 'Vol rớt LC']].to_string(index=False) + "\n")
