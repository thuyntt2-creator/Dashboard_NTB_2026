import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '5 TỈNH' in l or '5 Tỉnh' in l or 'tinh-full' in l or 'tinh-detailed' in l or 'table-vol-tinh' in l or 'table-gtc-tinh' in l or 'table-odr-tinh' in l:
        print(f"Line {i+1}: {l.strip()[:100]}")
