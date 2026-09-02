import json
import csv

with open('scratch/fd_rows_raw.json', 'r', encoding='utf-8') as f:
    rows = json.load(f)

with open('ops_fd.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    for r in rows:
        writer.writerow(r)

print(f"Written {len(rows)} rows to ops_fd.csv")
