import csv
import json

with open('buu_cuc_bat_on.csv', 'r', encoding='utf-8-sig') as f:
    rows = list(csv.reader(f))

header = rows[4]
data_rows = rows[5:18]

# no stdout prints to avoid cp1252 issues


parsed = []
for i, r in enumerate(data_rows):
    d = {header[j]: r[j] if j < len(r) else '' for j in range(len(header))}
    parsed.append(d)

with open('scratch/parsed_13_bc.json', 'w', encoding='utf-8') as out:
    json.dump(parsed, out, ensure_ascii=False, indent=2)
