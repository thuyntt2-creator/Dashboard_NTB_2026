import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print("=== GTC 5 PROVINCES ===")
if 'gtc_tinh' in d:
    for item in d['gtc_tinh']:
        print(item)
elif 'gtc_provinces' in d:
    for item in d['gtc_provinces']:
        print(item)
else:
    # search keys
    for k in d.keys():
        if 'gtc' in k.lower() or 'tinh' in k.lower():
            print("Key:", k)

print("\n=== SAMPLE OF GTC DATA ===")
for k in d.keys():
    if 'gtc' in k.lower():
        val = d[k]
        if isinstance(val, list):
            print(f"Key {k} (list len {len(val)}):", val[:2])
        elif isinstance(val, dict):
            print(f"Key {k} (dict keys {list(val.keys())[:5]}):")
