import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'tab-control' in l or 'tab-cod' in l or 'tab-qrcode' in l or 'cod-summary' in l or 'Tab 13' in l or 'QR Code' in l:
        print(f"Line {i+1}: {l.strip()}")
