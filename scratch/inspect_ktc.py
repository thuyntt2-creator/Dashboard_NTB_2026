import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data.js', 'r', encoding='utf-8') as f:
    text = f.read()

prefix = "window.DASHBOARD_DATA = "
data = json.loads(text[len(prefix):].rstrip(';\n '))

print("ktc keys:", data.get('ktc', {}).keys())
for k, v in data.get('ktc', {}).items():
    if isinstance(v, dict):
        print(f"  {k}: {list(v.keys())}")
    elif isinstance(v, list):
        print(f"  {k}: {len(v)} items")
    else:
        print(f"  {k}: {v}")

print("transport_costs:", data.get('transport_costs'))
