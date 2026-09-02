import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('templates/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if any(k in line.lower() for k in ['renderfd', 'tab-fd', '/api/fd', 'fd_cache', 'loadfd', 'api/batch-data']):
        print(f"Line {i+1}: {line.strip()[:140]}")
