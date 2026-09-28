import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', encoding='utf-8') as f:
    text = f.read()

for m in re.finditer(r'<div class="kpi-tile-value"[^>]*>([\s\S]*?)</div>', text):
    val_text = m.group(0).strip().replace('\n', ' ')
    if 'W38' in val_text or 'W37' in val_text or 'W35' in val_text:
        print("MATCHING KPI TILE:", val_text[:120])
