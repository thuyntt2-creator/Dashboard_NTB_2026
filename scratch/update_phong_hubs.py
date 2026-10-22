# -*- coding: utf-8 -*-
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

phong_hubs = {
    '20269000': '(DNO) Kiến Đức',
    '22048000': '(DNO) Đông Gia Nghĩa',
    '22048001': '(DNO) ĐL Nam Gia Nghĩa 2',
    '22242000': '(DNO) Bắc Gia Nghĩa',
    '23205000': '(DNO) Nhân Cơ 1'
}

with open('cocau_hubs.json', 'r', encoding='utf-8') as f:
    hubs = json.load(f)

existing_ids = set()
for h in hubs:
    wid = str(h.get('warehouse_id'))
    existing_ids.add(wid)
    if wid in phong_hubs:
        h['am'] = 'Lê Hồng Phong'
        print("Updated:", wid, h['bc'], "-> Lê Hồng Phong")

for wid, bc in phong_hubs.items():
    if wid not in existing_ids:
        hubs.append({'warehouse_id': wid, 'bc': bc, 'am': 'Lê Hồng Phong'})
        print("Added:", wid, bc, "-> Lê Hồng Phong")

with open('cocau_hubs.json', 'w', encoding='utf-8') as f:
    json.dump(hubs, f, ensure_ascii=False, indent=2)

print("Saved cocau_hubs.json successfully!")
