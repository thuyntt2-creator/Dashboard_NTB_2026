import re

with open("app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

keywords = ["thu_cung_ky", "cung ky", "cùng kỳ", "volume", "tạo đơn", "tao_don", "vols", "DataLTC", "rawltc", "off_spe", "buu_cuc_bat_on"]

found = []
for idx, line in enumerate(lines):
    line_num = idx + 1
    for kw in keywords:
        if kw.lower() in line.lower():
            found.append((line_num, kw, line.strip()))

with open("scratch/search_app_res.txt", "w", encoding="utf-8") as out:
    for f in found:
        out.write(f"Line {f[0]} (kw: {f[1]}): {f[2]}\n")

print(f"Done, found {len(found)} occurrences.")
