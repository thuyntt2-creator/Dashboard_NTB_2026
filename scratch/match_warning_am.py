import json
import pandas as pd

df_stuck = pd.read_csv('sheet_stuck.csv', encoding='utf-8')
bc_to_am = {}
for _, r in df_stuck.iterrows():
    bc_to_am[str(r['warehouse_name']).strip()] = str(r['am_name']).strip()

with open('scratch/bc_canh_bao_calculated.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

# Also check data.json for other AM mappings
with open('data.json', 'r', encoding='utf-8') as f:
    dj = json.load(f)

for item in items:
    bc_name = item['bc']
    # try direct match
    if bc_name in bc_to_am:
        item['am'] = bc_to_am[bc_name]
    else:
        # substring match
        matched = False
        for k, v in bc_to_am.items():
            if k in bc_name or bc_name in k or k.replace('(KHO) ', '').replace('(LDO) ', '').replace('(DNO) ', '') in bc_name:
                item['am'] = v
                matched = True
                break
        if not matched:
            # check in aging or other tables
            for r in dj.get('aging', {}).get('top_bc', []):
                if r.get('bc') == bc_name:
                    item['am'] = r.get('am', '')
                    matched = True
                    break

# Manual check for any remaining
fallback_am = {
    "(DNO) Quảng Tín": "Trương Quang Linh",
    "(LDO) Đức Trọng 1": "Nguyễn Hữu Tiến",
    "(LDO) Xuân Hương - Đà Lạt": "Lê Văn Trường",
    "(DNO) Kiến Đức": "Hồng Bích Nga",
    "(KHO) Cam Linh": "Nguyễn Thanh Long",
    "(KHO) Tây Nha Trang": "Phan Đình Duy",
    "(LDO) Lang Biang - Đà Lạt 1": "Trần Tấn Lợi",
    "(DNO) Tuy Đức": "Huỳnh Thúc Duân",
    "(LDO) Di Linh": "Trầm Hữu Tiến",
    "(LDO) Tân Hà Lâm Hà": "Lê Thị Kim Chi",
    "(DNO) Nhân Cơ": "Huỳnh Thúc Duân"
}

for item in items:
    if not item.get('am') or item['am'] == '':
        item['am'] = fallback_am.get(item['bc'], '---')

with open('scratch/bc_canh_bao_final.json', 'w', encoding='utf-8') as f:
    json.dump(items, f, ensure_ascii=False, indent=2)

print("Finished matching AMs! Sample item:")
print(json.dumps(items[0], ensure_ascii=False, indent=2))
