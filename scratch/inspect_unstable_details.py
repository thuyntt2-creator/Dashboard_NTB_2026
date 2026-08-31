import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

unstable_names = [
    "1322 Hùng Vương-Di Linh-Lâm Đồng",
    "Thôn Phúc Hưng-Xã Tân Hà Lâm Hà-Lâm Đồng",
    "56 Phan Đình Phùng-Cam Linh-Khánh Hòa",
    "Langbiang-Lạc Dương-Lâm Đồng",
    "Thôn R'Chai 2-Xã Đức Trọng-Lâm Đồng",
    "TDP Nghĩa Đức-Thạnh Mỹ-Đơn Dương-Lâm Đồng",
    "06 Lê Hồng Phong-TP.Nha Trang-Khánh Hòa",
    "337 Hùng Vương-Lộc Thắng-Bảo Lâm-Lâm Đồng"
]

df_gtc = pd.read_csv("ops_gtc.csv")
df_gtc_13 = df_gtc[df_gtc["Time"] == "2026-06-13 - Thứ 7"]

out_path = "scratch/inspect_unstable_details_res.txt"

with open(out_path, "w", encoding="utf-8") as f:
    f.write("=== UNSTABLE POS DETAILED METRICS FOR 13/06/2026 ===\n\n")
    for name in unstable_names:
        f.write(f"--- {name} ---\n")
        # Find matches in Chi tiết
        sub = df_gtc_13[df_gtc_13["Chi tiết"].str.contains(name, na=False, case=False)]
        if sub.empty:
            f.write("No matching row in ops_gtc for 13/06/2026\n")
        else:
            f.write(sub[["Chi tiết", "Loại Hàng", "Volume", "% Gán", "% GTC", "Leadtime", "Sản Lượng Giao Thành Công", "Sản Lượng Tồn", "Sản Lượng Chưa Gán", "AM"]].to_string() + "\n")
        f.write("\n")

print("Done details check!")
