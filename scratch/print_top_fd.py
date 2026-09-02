import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/fd_rows_raw.json', 'r', encoding='utf-8') as f:
    rows = json.load(f)

for i in range(min(27, len(rows))):
    print(f"Row {i+1:2d}: {rows[i]}")
