import json
with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

cod = d.get('cod_report', {})
print("cod_report keys:", list(cod.keys()))
print("prev_period:", cod.get('prev_period'))
print("curr_period:", cod.get('curr_period'))
print("metrics count:", len(cod.get('metrics', [])))
print("metrics:", cod.get('metrics'))
