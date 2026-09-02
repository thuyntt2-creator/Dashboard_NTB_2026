import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/fd_rows_raw.json', 'r', encoding='utf-8') as f:
    rows = json.load(f)

for i, r in enumerate(rows):
    if len(r) > 7:
        trailing = [(col_idx, val) for col_idx, val in enumerate(r[7:], start=7) if str(val).strip()]
        if trailing:
            print(f"Row {i+1} has extra cols: {trailing}")
