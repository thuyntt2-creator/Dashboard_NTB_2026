import sys
from bs4 import BeautifulSoup
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

target_tabs = ['tab-gan', 'tab-odr', 'tab-opr-tts', 'tab-rot-lc', 'tab-fd', 'tab-control', 'tab-truythu']

for tid in target_tabs:
    div = soup.find('div', id=tid)
    if not div:
        print(f"\nNOT FOUND: {tid}")
        continue
    print(f"\n==================== TAB: {tid} ====================")
    title = div.find(['h2', 'h3', 'h4'])
    print("Main title:", title.text.strip() if title else "No title")
    
    # find cards
    cards = div.find_all(class_='card') or div.find_all(class_='kpi-card') or div.find_all(class_='stat-card')
    print(f"Cards count: {len(cards)}")
    for c in cards[:6]:
        card_title = c.find(class_='card-title') or c.find(['h4', 'h5', 'div'])
        val = c.find(class_='card-value') or c.find(class_='stat-value') or c.find(class_='value')
        print("  Card:", (card_title.text.strip() if card_title else "")[:40], "=>", (val.text.strip() if val else "")[:30])
        
    # find tables
    tables = div.find_all('table')
    print(f"Tables count: {len(tables)}")
    for ti, tbl in enumerate(tables):
        headers = [th.text.strip() for th in tbl.find_all('th')]
        print(f"  Table {ti+1} Headers:", headers[:8])
        # first 2 rows
        rows = tbl.find_all('tr')
        for ri, r in enumerate(rows[1:3]):
            cells = [td.text.strip() for td in r.find_all('td')]
            print(f"    Row {ri+1}:", cells[:7])

    # find chart titles or canvas
    canvases = div.find_all('canvas')
    print(f"Canvases (Charts): {len(canvases)}")
    for cv in canvases:
        print("  Canvas ID:", cv.get('id'))
