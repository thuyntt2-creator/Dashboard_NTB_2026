import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/fd_rows_raw.json', 'r', encoding='utf-8') as f:
    rows = json.load(f)

print(f"Total rows in FD: {len(rows)}")
for i, r in enumerate(rows):
    print(f"Row {i+1:3d}: {r}")
