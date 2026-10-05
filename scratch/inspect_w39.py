import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
with open('KICH_BAN_THUYET_TRINH_W39_NAM_TRUNG_BO.html', encoding='utf-8') as f:
    c = f.read()

titles = re.findall(r'<div class=["\']section-title["\']>(.*?)</div>', c)
for i, t in enumerate(titles, 1):
    print(f'{i}: {t}')
