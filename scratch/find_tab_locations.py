import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('templates/index.html', encoding='utf-8') as f:
    html = f.read()

lines = html.split('\n')
for i, line in enumerate(lines, 1):
    if 'id="tab-' in line:
        print(f"Line {i}: {line.strip()[:110]}")
