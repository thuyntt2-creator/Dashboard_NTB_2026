import pandas as pd
import os

path = "treo_stuck.csv"
out_path = "scratch/analyze_treo_out.txt"

with open(out_path, "w", encoding="utf-8") as f:
    f.write("=== ANALYSIS OF TREO STUCK ===\n")
    if os.path.exists(path):
        df = pd.read_csv(path)
        f.write(f"Shape: {df.shape}\n")
        f.write(f"Columns: {df.columns.tolist()}\n")
        
        # Unique warehouse names
        f.write("\n--- Backlog by Warehouse Name ---\n")
        wh_counts = df.groupby(['warehouse_name', 'Loại đơn']).size().unstack(fill_value=0).reset_index()
        wh_counts['Total'] = wh_counts['Luân chuyển giao'] + wh_counts['Luân chuyển trả']
        wh_counts_sorted = wh_counts.sort_values(by='Total', ascending=False)
        f.write(wh_counts_sorted.to_string() + "\n")
        
        # Unique warehouse names in co_cau
        # KTC is usually Kho Trung Chuyển Khánh Hòa (1909) or others
        # Let's filter for warehouses containing "Khánh Hòa" or "Đức Trọng" or "Đắk Nông"
        f.write("\n--- Backlog by Warehouse Name (KTCs/Sort Centers) ---\n")
        ktc_names = ["Khánh Hòa", "Đức Trọng", "Đắk Nông", "Bình Thuận", "Bảo Lộc"]
        for name in ktc_names:
            sub = df[df['warehouse_name'].str.contains(name, case=False, na=False)]
            f.write(f"\nWarehouse matching '{name}' has {len(sub)} treo orders:\n")
            if len(sub) > 0:
                f.write(sub.groupby(['Loại đơn', 'Thời gian tồn đọng']).size().to_string() + "\n")
                
                # Top clients or statuses
                f.write("Status breakdown:\n" + sub.groupby('Trạng thái').size().to_string() + "\n")
                
    else:
        f.write("treo_stuck.csv not found\n")

print("Done writing treo analysis!")
