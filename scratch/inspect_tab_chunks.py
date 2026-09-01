import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Let's find each tab starting marker
tab_ids = [
    'tab-overview',
    'tab-volume',
    'tab-gtc-tong',
    'tab-gtc-tts-ca1',
    'tab-gan',
    'tab-odr',
    'tab-ltc',
    'tab-opr-tts',
    'tab-rot-lc',
    'tab-aging',
    'tab-commercial',
    'tab-control'
]

positions = []
for tid in tab_ids:
    m = re.search(r'<div id=["\']' + tid + r'["\']', text)
    if m:
        positions.append((m.start(), tid))

positions.sort()
print("Found tab positions:")
for idx, (pos, tid) in enumerate(positions):
    next_pos = positions[idx+1][0] if idx+1 < len(positions) else text.find('</main>')
    chunk = text[pos:next_pos]
    print(f"Tab {tid}: length={len(chunk)}, starts at {pos}")
