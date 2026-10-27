with open('app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'function initDashboard' in l or 'initDashboard(' in l or 'addEventListener(\'DOMContentLoaded\'' in l or 'window.onload' in l:
        print(f"Line {i+1}: {l.strip()}")
