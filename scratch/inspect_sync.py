import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open("app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if "def sync_sheets_directly_as_csv" in line:
        print(f"Line {idx+1}: {line.strip()}")
        # print some lines after
        for j in range(1, 100):
            if idx + j < len(lines):
                print(f"  +{j}: {lines[idx+j].rstrip()}")
        print("-" * 40)
