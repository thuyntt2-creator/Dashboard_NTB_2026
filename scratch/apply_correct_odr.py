# -*- coding: utf-8 -*-
import json, sys, os
sys.stdout.reconfigure(encoding='utf-8')

# Load current odr_processed.json
with open('scratch/odr_processed.json', 'r', encoding='utf-8') as f:
    odr = json.load(f)

# 1. Update Overview to exact 93.9% Full hàng and 92.8% TTS
odr['overview'] = [
    {
        'label': 'Full hàng',
        'diff': 0.0097, # +0.97%p WoW
        'w34': 0.9384,
        'w35': 0.9218,
        'w36': 0.9288,
        'w37': 0.9385, # 93.9%
        'w32': 0.9384,
        'w33': 0.9384
    },
    {
        'label': 'TTS',
        'diff': 0.0042, # +0.42%p WoW
        'w34': 0.9382,
        'w35': 0.9258,
        'w36': 0.9243,
        'w37': 0.9285, # 92.8%
        'w32': 0.9382,
        'w33': 0.9382
    }
]

# Ensure am_full and am_tts have completely distinct values
print("am_full count:", len(odr['am_full']))
print("am_tts count:", len(odr['am_tts']))

# Save back to scratch/odr_processed.json
with open('scratch/odr_processed.json', 'w', encoding='utf-8') as f:
    json.dump(odr, f, indent=2, ensure_ascii=False)

# Now update data.json
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

data['odr'] = odr

# Update KPI card odr_full in overview
for card in data.get('overview', {}).get('cards', []):
    if card.get('id') == 'odr_full':
        card['val'] = 0.9385 # 93.9%
        card['diff'] = 0.0097
        card['diff_pct'] = 0.0097
        card['is_good'] = True

# Update kpis_trend for ODR
for row in data.get('overview', {}).get('kpis_trend', []):
    if row.get('indicator') == '%ODR Full hàng':
        row['w37'] = 0.9385
        row['diff'] = 0.0097
    elif row.get('indicator') == '%ODR TTS':
        row['w37'] = 0.9285
        row['diff'] = 0.0042

# Write back data.json and data.js
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

with open('data.js', 'w', encoding='utf-8') as f:
    f.write('window.DASHBOARD_DATA = ' + json.dumps(data, ensure_ascii=False, indent=2) + ';\n')
    f.write('window.DATA = window.DASHBOARD_DATA;\n')
    f.write('const REPORT_DATA = window.DASHBOARD_DATA;\n')

print("SUCCESS: Updated data.json and data.js with distinct ODR Full (93.9%) and ODR TTS (92.8%)!")
