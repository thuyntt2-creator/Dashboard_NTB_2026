import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

cod = d.get('cod_report', {})
print("prev_period:", cod.get('prev_period'))
print("curr_period:", cod.get('curr_period'))
print("metrics:", json.dumps(cod.get('metrics', []), ensure_ascii=False, indent=2))
print("first 3 AMs:", json.dumps(cod.get('am_comparison', [])[:3], ensure_ascii=False, indent=2))
print("first 3 BCs:", json.dumps(cod.get('bc_details', [])[:3], ensure_ascii=False, indent=2))
print("actions count:", len(cod.get('actions', [])))
