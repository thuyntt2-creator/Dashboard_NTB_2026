# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from bs4 import BeautifulSoup

with open('index.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

sec = soup.find(id='tab-fd')
print("=== TAB-FD CONTENT IN INDEX.HTML ===")
for h in sec.find_all(['h2', 'h3', 'h4', 'h5']):
    print("Header:", h.text.strip().replace('\n', ' '))

for idx, tbl in enumerate(sec.find_all('table')):
    headers = [th.text.strip().replace('\n', ' ') for th in tbl.find_all('th')]
    print(f"\nTable {idx} columns ({len(headers)}):", headers)
    for r in tbl.find_all('tr')[1:4]:
        cells = [c.text.strip().replace('\n', ' ') for c in r.find_all(['td', 'th'])]
        print("  Row:", cells)
