import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

def scan_file(filepath):
    print(f"=== SCANNING {filepath} ===")
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for idx, line in enumerate(lines, 1):
        if any(term in line for term in ['W35', 'W36', '(W36', 'W36 vs W35', 'W35 vs W36', 'so với W36', 'so với W35', 'sv W36', 'sv W35', '31/08', '06/09', '31/8', '6/9', '23–29/8', '30/8–5/9']):
            print(f"{idx}: {line.strip()[:120]}")

scan_file('index.html')
scan_file('app.js')
