import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', encoding='utf-8') as f:
    d = json.load(f)

print("Keys in data.json:", list(d.keys()))

def inspect_key(k, n=5):
    val = d.get(k)
    print(f"\n=== KEY: {k} (type: {type(val).__name__}) ===")
    if isinstance(val, list):
        print(f"List length: {len(val)}")
        for item in val[:n]:
            print(" ", item)
    elif isinstance(val, dict):
        for sub_k, sub_v in list(val.items())[:n]:
            print(f"  {sub_k}: {sub_v}")

for k in d.keys():
    if any(term in k.lower() for term in ['gan', 'odr', 'opr', 'rot', 'fd', 'control', 'cod', 'truythu', 'truy_thu']):
        inspect_key(k, 3)
