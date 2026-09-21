import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', encoding='utf-8') as f:
    d = json.load(f)

cards = d.get('overview', {}).get('cards', [])
print(f"Total cards: {len(cards)}")
for i, c in enumerate(cards):
    print(f"Card {i}: id={c.get('id')}, title={c.get('title')}, val={c.get('val')}, diff={c.get('diff')}, sub={c.get('sub')}, diff_pct={c.get('diff_pct')}, is_good={c.get('is_good')}")

print("\n--- KPIS TREND ---")
for row in d.get('overview', {}).get('kpis_trend', []):
    print(row)
