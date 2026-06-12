import sys
import os
import pandas as pd

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# Helper to normalize percentage columns
def normalize_pct_col(series):
    def convert_val(val):
        if pd.isna(val):
            return 0.0
        val_str = str(val).strip()
        if not val_str:
            return 0.0
        is_pct = False
        if val_str.endswith('%'):
            val_str = val_str[:-1]
            is_pct = True
        try:
            f_val = float(val_str)
            if is_pct:
                return f_val / 100.0
            if f_val > 1.0:
                return f_val / 100.0
            return f_val
        except:
            return 0.0
    return series.apply(convert_val)

csv_path = 'ops_ltc.csv'
if os.path.exists(csv_path):
    df_raw = pd.read_csv(csv_path)
    
    # Get unique times
    times = df_raw['Time'].dropna().unique()
    print("Unique times in CSV:", [str(t) for t in times[:5]])
    
    # The CSV lists latest dates first. Let's find the latest date
    latest_date = times[0]
    print("\nAnalyzing date:", latest_date)
    
    df_date = df_raw[df_raw['Time'] == latest_date].copy()
    print("Total rows for date:", len(df_date))
    
    df_gt = df_date[df_date['Cấp quản lý'] == 'Grand Total']
    print("\n--- Grand Total rows from CSV ---")
    print(df_gt[['Cấp quản lý', 'Ca', 'Volume', '%Gán', '%LTC', '%Đóng kiện', '%LC', 'Sản Lượng Lấy Thành Công']].to_string())
    
    # Details rows
    df_details = df_date[df_date['Cấp quản lý'] != 'Grand Total'].copy()
    df_details['Volume'] = pd.to_numeric(df_details['Volume'].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
    df_details['%LTC'] = normalize_pct_col(df_details['%LTC'])
    df_details['Sản Lượng Lấy Thành Công'] = pd.to_numeric(df_details['Sản Lượng Lấy Thành Công'], errors='coerce').fillna(0)
    
    # Sum details
    sum_vol = df_details['Volume'].sum()
    sum_success = df_details['Sản Lượng Lấy Thành Công'].sum()
    print("\n--- Summed values of details (excluding Grand Total) ---")
    print("Sum of Volume (Details):", sum_vol)
    print("Sum of Sản Lượng Lấy Thành Công (Details):", sum_success)
    print("Calculated overall LTC rate (Sản Lượng Lấy Thành Công / Volume * 100):", (sum_success / sum_vol * 100) if sum_vol > 0 else 0)
    
    # ltc_vol
    df_details['ltc_vol'] = df_details['Volume'] * df_details['%LTC']
    sum_ltc_vol = df_details['ltc_vol'].sum()
    print("Sum of ltc_vol (Volume * %LTC):", sum_ltc_vol)
    print("Calculated ltc_vol rate (sum_ltc_vol / sum_vol * 100):", (sum_ltc_vol / sum_vol * 100) if sum_vol > 0 else 0)
    
    # Let's inspect some rows to see if %LTC and %LC are different
    print("\n--- First 10 details rows ---")
    print(df_details[['Chi tiết', 'Ca', 'Volume', '%LTC', 'Sản Lượng Lấy Thành Công', 'ltc_vol']].head(10).to_string())

else:
    print("ops_ltc.csv not found!")
