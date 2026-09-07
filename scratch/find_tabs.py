import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()
lines = html.split('\n')
results = []
for i, line in enumerate(lines):
    if 'data-tab' in line or 'id="tab-' in line:
        s = line.strip()[:120]
        results.append(str(i+1) + ': ' + s)
for r in results[:50]:
    print(r)
