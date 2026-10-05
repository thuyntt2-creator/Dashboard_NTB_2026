import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

# 1. Update data.json
with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

cards = d.get('overview', {}).get('cards', [])
# Check if cod_tm already exists
has_cod = any(c.get('id') == 'cod_tm' for c in cards)
if not has_cod:
    cards.append({
        "id": "cod_tm",
        "title": "Tỷ Lệ Tiền Mặt COD",
        "val": 0.371,
        "unit": "%",
        "diff": -0.030,
        "diff_pct": -0.075,
        "is_good": True,
        "icon": "qr-code"
    })
    d['overview']['cards'] = cards
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    print("✓ Added cod_tm to data.json")
else:
    print("cod_tm already in data.json")

# 2. Update data.js
with open('data.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

# Replace or rewrite window.APP_DATA
prefix = "window.APP_DATA = "
if js_content.startswith(prefix):
    with open('data.js', 'w', encoding='utf-8') as f:
        f.write(prefix + json.dumps(d, ensure_ascii=False, indent=2) + ";\n")
    print("✓ Rebuilt data.js with cod_tm")
else:
    print("data.js does not start with expected prefix, checking regex")
