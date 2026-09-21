import re, sys
sys.stdout.reconfigure(encoding='utf-8')
content = open('index.html', encoding='utf-8').read()
for tid in [
    'table-vol-tinh-full', 'table-vol-tinh-tts',
    'table-gtc-tinh-full', 'table-gtc-tinh-tts',
    'table-gtc-tts-ca1-detailed', 'table-gan-overview-region',
    'table-odr-tinh-full', 'table-odr-tinh-tts',
    'table-rot-am-detailed', 'table-rot-tinh-detailed',
    'table-rot-lc-top-bc'
]:
    m = re.search(r'(<table[^>]*id=["\']' + tid + r'["\'][\s\S]*?</thead>)', content)
    if m:
        print(f"=== {tid} ===\n{m.group(1)}\n")
