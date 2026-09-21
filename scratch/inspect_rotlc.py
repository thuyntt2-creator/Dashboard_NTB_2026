import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
m = re.search(r'function renderRotLcTab\(\)[\s\S]*?(?=\n  function |\Z)', text)
if m:
    print(m.group(0)[:2500])
else:
    print("renderRotLcTab not found")

m2 = re.search(r'function renderRotLcChart\(\)[\s\S]*?(?=\n  function |\Z)', text)
if m2:
    print("\n--- renderRotLcChart ---")
    print(m2.group(0)[:1500])
