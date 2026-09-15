import csv
import json

with open('buu_cuc_bat_on.csv', 'r', encoding='utf-8-sig', errors='ignore') as f:
    reader = csv.reader(f)
    rows = list(reader)

print(f"Total rows: {len(rows)}")
with open('scratch/inspect_output.json', 'w', encoding='utf-8') as out:
    json.dump(rows[:20], out, ensure_ascii=False, indent=2)

