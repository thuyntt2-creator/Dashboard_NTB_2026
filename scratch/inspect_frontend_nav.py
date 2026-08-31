import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open("templates/index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(3790, 3950):
    if i < len(lines):
        print(f"Line {i+1}: {lines[i].rstrip()}")
