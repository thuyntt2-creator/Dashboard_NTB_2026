import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/fd_rows_raw.json', 'r', encoding='utf-8') as f:
    rows = json.load(f)

for i, r in enumerate(rows):
    # filter out empty trailing strings
    non_empty = [c for c in r if str(c).strip() != '']
    print(f"Row {i+1:3d} ({len(r)} cols): {r}")
