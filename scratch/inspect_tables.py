import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

soup = BeautifulSoup(open('index.html', 'r', encoding='utf-8').read(), 'html.parser')

check_tabs = ['tab-gan', 'tab-odr', 'tab-ltc', 'tab-opr-tts', 'tab-rot-lc']
for tid in check_tabs:
    t = soup.find('div', id=tid)
    print(f"==============================")
    print(f"TAB: {tid}")
    print(f"==============================")
    if t:
        tbls = t.find_all('table')
        for tbl in tbls:
            ths = [th.text.strip() for th in tbl.find_all('th')]
            print(f"  Table ID: {tbl.get('id')} (cols={len(ths)}): {ths}")
        canvases = [c.get('id') for c in t.find_all('canvas')]
        print(f"  Canvases: {canvases}")
    else:
        print("  NOT FOUND!")
