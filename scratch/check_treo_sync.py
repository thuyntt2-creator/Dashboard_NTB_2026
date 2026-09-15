import json

with open('scratch/treo_lc_calculated.json', 'r', encoding='utf-8') as f:
    calc = json.load(f)

with open('data.json', 'r', encoding='utf-8') as f:
    dj = json.load(f)

with open('data.js', 'r', encoding='utf-8') as f:
    js_text = f.read()

print("calc total_u24:", calc.get('total_u24'))
print("data.json total_u24:", dj.get('treo_lc', {}).get('total_u24'))
print("calc top_am[0] keys:", list(calc['top_am'][0].keys()))
print("data.json top_am[0] keys:", list(dj.get('treo_lc', {}).get('top_am', [{}])[0].keys()))
print("data.js has total_u24:", "total_u24" in js_text)
