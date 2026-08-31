import pandas as pd
import os

co_cau_path = "ops_co_cau.csv"
out_path = "scratch/verify_ams_out.txt"

with open(out_path, "w", encoding="utf-8") as f:
    f.write("=== AM MAPPINGS FOR CRITICAL POS ===\n")
    if os.path.exists(co_cau_path):
        df_cc = pd.read_csv(co_cau_path)
        critical_pos = [
            "1322 Hùng Vương-Di Linh",
            "Phan Đình Phùng-Cam Linh",
            "Nghĩa Đức-Thạnh Mỹ",
            "Lê Hồng Phong-TP.Nha Trang",
            "Phúc Hưng-Xã Tân Hà",
            "Langbiang-Lạc Dương",
            "R'Chai 2-Xã Đức Trọng",
            "337 Hùng Vương-Lộc Thắng"
        ]
        for po in critical_pos:
            match = df_cc[df_cc['Bưu cục'].str.contains(po, case=False, na=False)]
            if not match.empty:
                for idx, r in match.iterrows():
                    f.write(f"PO: {r['Bưu cục']} -> AM: {r['AM']} (Province: {r['Tỉnh']})\n")
            else:
                f.write(f"No match for: {po}\n")
    else:
        f.write("ops_co_cau.csv not found\n")

print("Done writing verify_ams!")
