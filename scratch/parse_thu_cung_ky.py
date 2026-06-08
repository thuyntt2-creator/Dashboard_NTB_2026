import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "thu_cung_ky.csv")
output_path = os.path.join(workspace_dir, "scratch", "parse_thu_cung_ky_res.txt")

os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w", encoding="utf-8") as f:
    df = pd.read_csv(file_path)
    f.write(f"Columns: {list(df.columns)}\n")
    f.write(f"Total rows: {len(df)}\n")
    
    # We want to find the section under "Tỉnh"
    # In df, look for when the first column is "Tỉnh"
    tinh_start_idx = None
    for idx, r in df.iterrows():
        if str(r.iloc[0]).strip() == "Tỉnh":
            tinh_start_idx = idx
            break
            
    f.write(f"Tỉnh section starts at row: {tinh_start_idx}\n")
    if tinh_start_idx is not None:
        df_tinh = df.iloc[tinh_start_idx+1:].copy()
        df_tinh.columns = df.iloc[tinh_start_idx].values
        
        # Rename columns to avoid issues
        df_tinh.columns = [str(c).strip() for c in df_tinh.columns]
        
        # Forward fill the "Tỉnh" column
        df_tinh['Tỉnh'] = df_tinh['Tỉnh'].ffill()
        
        # Filter out rows where Time is empty or is "Tổng cộng"
        df_tinh = df_tinh[df_tinh['Time'].notna()]
        df_tinh = df_tinh[~df_tinh['Time'].str.contains("Tổng cộng|Total", case=False, na=False)]
        
        f.write("\nProcessed historical rows under Tỉnh section:\n")
        f.write(df_tinh.head(40).to_string() + "\n")
        
        # Check date format and convert if needed
        # Dates look like: '2026-06-07 - Chủ Nhật'
        df_tinh['date_str'] = df_tinh['Time'].apply(lambda x: str(x).split(' - ')[0])
        df_tinh['date'] = pd.to_datetime(df_tinh['date_str'], errors='coerce')
        
        # Clean numeric columns (they might have dots as thousands separators, e.g. 17.802)
        # In Vietnam, 17.802 means 17802. Let's inspect raw strings first.
        f.write("\nRaw values in GTC and Volume:\n")
        f.write(df_tinh[['Tỉnh', 'Time', 'Volume', 'GTC']].head(10).to_string() + "\n")
        
        def clean_numeric(val):
            if pd.isna(val):
                return 0.0
            val_str = str(val).strip().replace(',', '')
            # If there's a dot, does it represent thousands?
            # Let's see: 17.802 -> 17802 if dot is thousands separator.
            # In python, pandas might parse "17.802" as 17.802 (float).
            # If so, we need to multiply by 1000 if it was string or if it's float.
            # Let's check: if we convert to float and it's small, let's see.
            try:
                # If it's already a float or parsed as float:
                f_val = float(val_str)
                # If it has a dot in the raw string and is less than 1000:
                if "." in str(val) and f_val < 1000:
                    # Let's count decimal places
                    parts = str(val).split(".")
                    if len(parts) > 1 and len(parts[1]) == 3:
                        return f_val * 1000
                return f_val
            except:
                return 0.0
                
        df_tinh['Volume_clean'] = df_tinh['Volume'].apply(clean_numeric)
        df_tinh['GTC_clean'] = df_tinh['GTC'].apply(clean_numeric)
        
        f.write("\nCleaned values:\n")
        f.write(df_tinh[['Tỉnh', 'Time', 'Volume_clean', 'GTC_clean']].head(15).to_string() + "\n")
        
        # Let's calculate WTD (2026-06-01 to 2026-06-07)
        df_wtd = df_tinh[(df_tinh['date'] >= '2026-06-01') & (df_tinh['date'] <= '2026-06-07')]
        prov_wtd_vol = df_wtd.groupby('Tỉnh')['Volume_clean'].sum().reset_index()
        prov_wtd_gtc = df_wtd.groupby('Tỉnh')['GTC_clean'].sum().reset_index()
        
        f.write("\nWTD Volume (2026-06-01 to 2026-06-07) by Province:\n")
        f.write(prov_wtd_vol.to_string() + "\n")
        f.write("\nWTD GTC (2026-06-01 to 2026-06-07) by Province:\n")
        f.write(prov_wtd_gtc.to_string() + "\n")
        
        # Let's check other date ranges:
        # WTD-1: 2026-05-25 to 2026-05-31
        df_wtd_1 = df_tinh[(df_tinh['date'] >= '2026-05-25') & (df_tinh['date'] <= '2026-05-31')]
        f.write("\nWTD-1 GTC by Province:\n")
        f.write(df_wtd_1.groupby('Tỉnh')['GTC_clean'].sum().reset_index().to_string() + "\n")
        f.write("WTD-1 Volume by Province:\n")
        f.write(df_wtd_1.groupby('Tỉnh')['Volume_clean'].sum().reset_index().to_string() + "\n")
        
        # WTD-2: 2026-05-18 to 2026-05-24
        df_wtd_2 = df_tinh[(df_tinh['date'] >= '2026-05-18') & (df_tinh['date'] <= '2026-05-24')]
        f.write("\nWTD-2 GTC by Province:\n")
        f.write(df_wtd_2.groupby('Tỉnh')['GTC_clean'].sum().reset_index().to_string() + "\n")
        f.write("WTD-2 Volume by Province:\n")
        f.write(df_wtd_2.groupby('Tỉnh')['Volume_clean'].sum().reset_index().to_string() + "\n")

print("Historical parsing completed.")
