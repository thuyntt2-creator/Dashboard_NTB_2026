import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "vols_tao_don.xlsx")
output_path = os.path.join(workspace_dir, "scratch", "customer_groups_res.txt")

with open(output_path, "w", encoding="utf-8") as f:
    df = pd.read_excel(file_path, sheet_name="shopee_tiktok")
    f.write("=== Khách hàng value counts ===\n")
    f.write(df['Khách hàng'].value_counts(dropna=False).to_string() + "\n\n")
    f.write("=== Bưu cục value counts ===\n")
    f.write(df['Bưu cục'].value_counts(dropna=False).head(30).to_string() + "\n\n")

print("Done writing scratch/customer_groups_res.txt")
