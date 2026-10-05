import sys
from bs4 import BeautifulSoup
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

def dump_tab_tables(tid):
    div = soup.find('div', id=tid)
    if not div:
        print(f"Tab {tid} not found")
        return
    print(f"\n==================== TAB: {tid} ====================")
    tables = div.find_all('table')
    for ti, tbl in enumerate(tables):
        headers = [th.text.strip().replace('\n', ' ') for th in tbl.find_all('th')]
        print(f"\n-- Table {ti+1}: {headers} --")
        rows = tbl.find_all('tr')[1:]
        for ri, r in enumerate(rows[:10]):
            cells = [td.text.strip().replace('\n', ' ') for td in r.find_all(['td', 'th'])]
            print(f"  [{ri+1}] " + " | ".join(cells[:7]))
        if len(rows) > 10:
            print(f"  ... ({len(rows)} total rows)")

for t in ['tab-gan', 'tab-odr', 'tab-opr-tts', 'tab-rot-lc', 'tab-fd', 'tab-control', 'tab-truythu']:
    dump_tab_tables(t)
