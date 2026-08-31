import pandas as pd
import os

path = "buu_cuc_bat_on.csv"
out_path = "scratch/analyze_bat_on_out.txt"

with open(out_path, "w", encoding="utf-8") as f:
    f.write("=== ANALYSIS OF BUU CUC BAT ON ===\n")
    if os.path.exists(path):
        df = pd.read_csv(path)
        # Columns start at row 2 (0-indexed)
        df_data = df.iloc[2:].copy()
        df_data.columns = df.iloc[2]
        df_data = df_data.iloc[1:].reset_index(drop=True)
        df_data.columns = [str(c).strip() for c in df_data.columns]
        
        f.write(f"Total rows: {len(df_data)}\n")
        f.write(f"Columns: {df_data.columns.tolist()}\n")
        
        # Filter where tinh_hinh == 'Bất ổn'
        df_bo = df_data[df_data['tinh_hinh'] == 'Bất ổn']
        f.write(f"Number of unstable (Bất ổn) post offices: {len(df_bo)}\n")
        
        # Sort by BL LM descending
        df_bo['BL LM'] = pd.to_numeric(df_bo['BL LM'], errors='coerce').fillna(0)
        df_bo['BL KTC'] = pd.to_numeric(df_bo['BL KTC'], errors='coerce').fillna(0)
        df_bo['BL LM >5 ngay'] = pd.to_numeric(df_bo['BL LM >5 ngay'], errors='coerce').fillna(0)
        df_bo['tao_n1'] = pd.to_numeric(df_bo['tao_n1'], errors='coerce').fillna(0)
        df_bo['gtc_n1'] = pd.to_numeric(df_bo['gtc_n1'], errors='coerce').fillna(0)
        df_bo['du_kien_clear_ton'] = pd.to_numeric(df_bo['du_kien_clear_ton'], errors='coerce').fillna(0)
        
        df_bo_sorted = df_bo.sort_values(by='BL LM', ascending=False)
        f.write("\n--- Top 15 Unstable Post Offices by BL LM (Backlog Last Mile) ---\n")
        cols_to_print = ['tinh_giao', 'kho_giao_name', 'BL LM', 'BL LM >5 ngay', '%BL LM >5 ngay', 'BL KTC', 'tao_n1', 'gtc_n1', 'du_kien_clear_ton', 'ly_do_bat_on']
        f.write(df_bo_sorted[cols_to_print].head(15).to_string() + "\n")
        
        # Look at the aging / backlog by province
        f.write("\n--- Backlog Summary by Province ---\n")
        prov_summary = df_data.groupby('tinh_giao').agg(
            total_lm_backlog=('BL LM', lambda x: pd.to_numeric(x, errors='coerce').sum()),
            total_ktc_backlog=('BL KTC', lambda x: pd.to_numeric(x, errors='coerce').sum()),
            unstable_count=('tinh_hinh', lambda x: (x == 'Bất ổn').sum())
        ).reset_index()
        f.write(prov_summary.to_string() + "\n")
        
    else:
        f.write("buu_cuc_bat_on.csv not found\n")

print("Done writing bat on analysis!")
