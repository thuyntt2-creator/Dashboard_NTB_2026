with open("automate_report_and_dashboard.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    line_lower = line.lower()
    if any(keyword in line_lower for keyword in ["gspread", "open_by", "update"]):
        print(f"Line {idx+1}: {line.strip()}")
