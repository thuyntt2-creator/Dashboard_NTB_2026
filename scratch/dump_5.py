import re, sys
sys.stdout.reconfigure(encoding='utf-8')
content = open('index.html', encoding='utf-8').read()
for tid in [
    'table-overview-kpi-data', 'table-vol-full-detailed', 'table-vol-tts-detailed',
    'table-gtc-full-detailed', 'table-gan-ca1-detailed'
]:
    m = re.search(r'(<table[^>]*id=["\']' + tid + r'["\'][\s\S]*?</thead>)', content)
    if m:
        print(f"=== {tid} ===\n{m.group(1)}\n")
