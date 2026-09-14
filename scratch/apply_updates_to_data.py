import json

with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('scratch/treo_lc_calculated.json', 'r', encoding='utf-8') as f:
    treo_calc = json.load(f)

with open('scratch/bc_canh_bao_final.json', 'r', encoding='utf-8') as f:
    bc_canh_bao = json.load(f)

# 1. Update treo_lc
data['treo_lc'] = treo_calc

# 2. Add bc_canh_bao
data['bc_canh_bao'] = bc_canh_bao

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

with open('data.js', 'w', encoding='utf-8') as f:
    f.write("const REPORT_DATA = ")
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write(";\n")

print("Successfully updated data.json and data.js!")
print(f"treo_lc total: {data['treo_lc']['total']}")
print(f"treo_lc top_am count: {len(data['treo_lc']['top_am'])}")
print(f"bc_canh_bao count: {len(data['bc_canh_bao'])}")
