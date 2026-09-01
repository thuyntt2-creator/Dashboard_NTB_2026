import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# find all calls in renderTabCharts
p = text.find('function renderTabCharts')
p_end = text.find('function applyTheme')
chunk = text[p:p_end]

calls = re.findall(r'(render[A-Za-z0-9_]+)\(', chunk)
print("Chart functions called in renderTabCharts:")
for c in set(calls):
    if c != 'renderTabCharts':
        exists = f"function {c}" in text
        print(f"  {c}: {'EXISTS' if exists else 'MISSING!'}")
