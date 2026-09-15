import json

with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

# 1. Update overview.cards
for c in d.get('overview', {}).get('cards', []):
    if c.get('id') == 'odr_full':
        c['val'] = 0.939
        c['diff'] = 0.010
        c['diff_pct'] = 0.010
        print("Updated overview.cards odr_full")

# 2. Update overview.kpis_trend
for t in d.get('overview', {}).get('kpis_trend', []):
    ind = t.get('indicator', '')
    if 'ODR' in ind and ('Full' in ind or 'full' in ind):
        t['w37'] = 0.939
        t['w36'] = 0.929
        t['diff'] = 0.010
        print(f"Updated overview.kpis_trend {ind}")
    elif 'ODR' in ind and 'TTS' in ind:
        t['w37'] = 0.928
        t['w36'] = 0.924
        t['diff'] = 0.004
        print(f"Updated overview.kpis_trend {ind}")

# 3. Update d['odr']['overview']
if 'odr' in d and 'overview' in d['odr']:
    for row in d['odr']['overview']:
        if row.get('label') == 'Full hàng':
            row['w37'] = 0.939
            row['diff'] = 0.010
        elif row.get('label') == 'TTS':
            row['w37'] = 0.928
            row['diff'] = 0.004

# Write to data.json
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)
print("Saved data.json")

# Write to data.js
with open('data.js', 'w', encoding='utf-8') as f:
    f.write('window.DATA = ' + json.dumps(d, ensure_ascii=False) + ';')
print("Saved data.js")
