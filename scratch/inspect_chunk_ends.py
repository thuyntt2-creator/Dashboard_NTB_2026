import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

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

import re
positions = []
for tid in tab_ids:
    m = re.search(r'<div id=["\']' + tid + r'["\']', text)
    if m:
        positions.append((m.start(), tid))

positions.sort()

for idx, (pos, tid) in enumerate(positions):
    next_pos = positions[idx+1][0] if idx+1 < len(positions) else text.find('</main>')
    raw_chunk = text[pos:next_pos]
    
    # check if closing tag is at end
    print(f"=== TAB: {tid} ===")
    print(f"Start: {raw_chunk[:100]}...")
    print(f"End: ...{raw_chunk[-150:]}")
    print()
