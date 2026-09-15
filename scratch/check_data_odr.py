# -*- coding: utf-8 -*-
import json, re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data.js', 'r', encoding='utf-8') as f:
    text = f.read()

# find overview cards
m = re.search(r'\"id\":\s*\"odr_full\"[^\}]+', text)
if m:
    print("data.js odr_full card:", m.group(0))

# find odr in kpis_trend
m = re.findall(r'\{\s*\"indicator\":\s*\"[^\"]*ODR[^\"]*\"[^\}]+\}', text)
for item in m:
    print("data.js kpis_trend:", item)

# check odr in D.odr
with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

odr_data = d.get('odr', {})
print("\nD.odr keys:", list(odr_data.keys()))
print("D.odr overview:", odr_data.get('overview'))
print("D.odr tinh_full:", odr_data.get('tinh_full'))
print("D.odr tinh_tts:", odr_data.get('tinh_tts'))
