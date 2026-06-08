import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx")
output_path = os.path.join(workspace_dir, "scratch", "inspect_data_sums_res.txt")

with open(output_path, "w", encoding="utf-8") as f:
    df = pd.read_excel(file_path, sheet_name="Data")
    df['clean_prov'] = df['Tỉnh'].apply(lambda x: str(x).strip().replace('Khánh Hoà', 'Khánh Hòa').replace('Đắc Nông', 'Đắk Nông'))
    df['date'] = pd.to_datetime(df['Time'].apply(lambda x: str(x).split(' - ')[0]), errors='coerce')
    
    # Let's clean percentage strings to numeric
    for c in df.columns:
        if df[c].dtype == object:
            # check if it contains percentage
            sample = df[c].dropna().head(10).astype(str)
            if sample.str.contains('%').any():
                df[c] = df[c].astype(str).str.replace('%', '', regex=False).str.replace(',', '.', regex=False)
                df[c] = pd.to_numeric(df[c], errors='coerce') / 100.0
                
    # List of numeric columns
    num_cols = df.select_dtypes(include=['number']).columns.tolist()
    f.write(f"Numeric columns: {num_cols}\n\n")
    
    df_d = df[df['date'] == '2026-06-07']
    df_d1 = df[df['date'] == '2026-06-06']
    
    f.write("=== SUMS FOR 2026-06-07 ===\n")
    for c in num_cols:
        f.write(f"\nColumn: {c}\n")
        f.write(df_d.groupby('clean_prov')[c].sum().reset_index().to_string() + "\n")
        
    f.write("\n=== SUMS FOR 2026-06-06 ===\n")
    for c in num_cols:
        f.write(f"\nColumn: {c}\n")
        f.write(df_d1.groupby('clean_prov')[c].sum().reset_index().to_string() + "\n")

print("Done printing all column sums.")
