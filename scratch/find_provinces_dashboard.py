import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

current_tab = None
for i, line in enumerate(lines):
    if 'class="tab-view"' in line or 'class="tab-view ' in line or 'id="tab-' in line:
        current_tab = line.strip()
    if 'tinh' in line.lower() or 'tỉnh' in line.lower() or 'province' in line.lower():
        if any(tag in line for tag in ['<div', '<table', '<h2', '<h3', '<h4', '<button', 'class="report-card']):
            print(f"Tab: {current_tab} | Line {i+1}: {line.strip()[:110]}")
