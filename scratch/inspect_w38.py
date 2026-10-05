import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
with open('scratch/rewrite_w38_natural_16_parts.py', encoding='utf-8') as f:
    c = f.read()

titles = re.findall(r'section_title=["\'](.*?)["\']', c)
for i, t in enumerate(titles, 1):
    print(f'{i}: {t}')
