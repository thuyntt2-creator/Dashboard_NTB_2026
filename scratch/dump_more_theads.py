import re, sys
sys.stdout.reconfigure(encoding='utf-8')
content = open('index.html', encoding='utf-8').read()
for tid in [
    'table-overview-kpi-data', 'table-bc-canh-bao-overview',
    'table-vol-full-detailed', 'table-vol-tts-detailed',
    'table-gtc-full-detailed', 'table-gtc-tts-detailed',
    'table-bc-canh-bao', 'table-gan-ca1-detailed', 'table-gan-ca2-detailed',
    'table-odr-full-detailed', 'table-odr-tts-detailed',
    'table-ltc-detailed', 'table-ltc-tinh-detailed',
    'table-opr-day-detailed', 'table-opr-night-detailed',
    'table-fd-am-detailed', 'table-kd-churn-top10', 'table-bc-canhbao-tab'
]:
    m = re.search(r'(<table[^>]*id=["\']' + tid + r'["\'][\s\S]*?</thead>)', content)
    if m:
        print(f"=== {tid} ===\n{m.group(1)}\n")
