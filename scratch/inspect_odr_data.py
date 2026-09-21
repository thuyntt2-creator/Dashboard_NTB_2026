import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', encoding='utf-8') as f:
    d = json.load(f)

odr = d.get('odr', {})
print("=== ODR OVERVIEW ===")
print(json.dumps(odr.get('overview', []), indent=2, ensure_ascii=False))

print("\n=== ODR AM FULL (First 3) ===")
print(json.dumps(odr.get('am_full', [])[:3], indent=2, ensure_ascii=False))

print("\n=== ODR TINH FULL ===")
print(json.dumps(odr.get('tinh_full', []), indent=2, ensure_ascii=False))
