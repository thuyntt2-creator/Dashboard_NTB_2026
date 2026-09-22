import re, sys

with open('KICH_BAN_THUYET_TRINH_W38_NAM_TRUNG_BO.html', 'r', encoding='utf-8') as f:
    text = f.read()

headers = re.findall(r'<div class="card-header">(.*?)</div>', text, re.DOTALL)
for i, h in enumerate(headers):
    # remove tags
    clean_h = re.sub(r'<[^>]+>', '', h).strip()
    print(f'{i}: {clean_h}')
