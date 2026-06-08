import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "buu_cuc_bat_on.xlsx")
output_path = os.path.join(workspace_dir, "scratch", "bat_on_tao_sums.txt")

os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w", encoding="utf-8") as f:
    try:
        xls = pd.ExcelFile(file_path)
        for sheet in ["Datatoday", "NTB"]:
            if sheet in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name=sheet)
                # For NTB sheet, row 2 contains the actual header
                if sheet == "NTB":
                    df = pd.read_excel(xls, sheet_name=sheet, skiprows=2)
                f.write(f"\n====================================\nSheet: {sheet}\n====================================\n")
                
                # Strip spaces from column names
                df.columns = [str(c).strip() for c in df.columns]
                
                # Columns we want: tinh_giao or Tỉnh, tao_n1, tao_avg_7ngay, gtc_n1, gtc_avg_7ngay
                tinh_col = next((c for c in df.columns if "tỉnh" in c.lower() or "tinh" in c.lower()), None)
                tao_n1_col = next((c for c in df.columns if "tao_n1" in c.lower() or "tạo_n1" in c.lower() or c == "tao_n1"), None)
                tao_avg_col = next((c for c in df.columns if "tao_avg" in c.lower() or "tạo_avg" in c.lower() or c == "tao_avg_7ngay"), None)
                gtc_n1_col = next((c for c in df.columns if "gtc_n1" in c.lower() or c == "gtc_n1"), None)
                gtc_avg_col = next((c for c in df.columns if "gtc_avg" in c.lower() or c == "gtc_avg_7ngay"), None)
                
                f.write(f"Tỉnh col: {tinh_col}, tao_n1 col: {tao_n1_col}, tao_avg col: {tao_avg_col}\n")
                
                if tinh_col and tao_n1_col:
                    # Clean numeric column
                    df[tao_n1_col] = pd.to_numeric(df[tao_n1_col], errors='coerce').fillna(0)
                    if tao_avg_col:
                        df[tao_avg_col] = pd.to_numeric(df[tao_avg_col], errors='coerce').fillna(0)
                    if gtc_n1_col:
                        df[gtc_n1_col] = pd.to_numeric(df[gtc_n1_col], errors='coerce').fillna(0)
                    if gtc_avg_col:
                        df[gtc_avg_col] = pd.to_numeric(df[gtc_avg_col], errors='coerce').fillna(0)
                        
                    # Clean province names
                    df[tinh_col] = df[tinh_col].astype(str).str.strip().replace({'Khánh Hoà': 'Khánh Hòa', 'Bình Phước': 'Lâm Đồng'})
                    
                    # Group by
                    agg_dict = {tao_n1_col: 'sum'}
                    if tao_avg_col: agg_dict[tao_avg_col] = 'sum'
                    if gtc_n1_col: agg_dict[gtc_n1_col] = 'sum'
                    if gtc_avg_col: agg_dict[gtc_avg_col] = 'sum'
                    
                    grouped = df.groupby(tinh_col).agg(agg_dict).reset_index()
                    f.write(grouped.to_string() + "\n")
                    
                    # Total
                    f.write("\nTotals:\n")
                    for k, v in agg_dict.items():
                        f.write(f"  {k}: {df[k].sum()}\n")
    except Exception as e:
         f.write(f"Error: {e}\n")

print("Completed.")
