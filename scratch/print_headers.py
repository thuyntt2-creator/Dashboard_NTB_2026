import csv
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('ops_fd.csv', mode='r', encoding='utf-8') as f:
    reader = csv.reader(f)
    lines = list(reader)

for idx, line in enumerate(lines):
    line_str = str(line)
    if 'Bưu Cục' in line_str or 'AM' in line_str or 'Tỉnh' in line_str or 'Vol giao' in line_str:
        print(f"Row {idx}: {line}")
