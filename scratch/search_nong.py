with open("tu_dong_bao_cao_nong.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    line_lower = line.lower()
    if any(keyword in line_lower for keyword in ["to_excel", "to_csv", "update", "open", "write"]):
        print(f"Line {idx+1}: {line.strip()}")
