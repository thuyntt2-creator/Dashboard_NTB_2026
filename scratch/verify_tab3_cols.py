import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

soup = BeautifulSoup(open('index.html', 'r', encoding='utf-8').read(), 'html.parser')
tab3 = soup.find('div', id='tab-gtc-tong')
for tbl in tab3.find_all('table'):
    ths = [th.text.strip() for th in tbl.find_all('th')]
    print(f"Table ID: {tbl.get('id')} (cols={len(ths)}): {ths}")
