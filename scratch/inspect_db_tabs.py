import sys
from bs4 import BeautifulSoup
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

print("=== ALL TABS IN INDEX.HTML ===")
tabs = soup.find_all(attrs={'data-tab': True})
for t in tabs:
    tab_id = t.get('data-tab')
    text = t.text.strip().replace('\n', ' ')
    print(f"Tab ID: {tab_id:20s} | Title: {text}")

print("\n=== ALL TAB CONTENT CONTAINERS ===")
for div in soup.find_all(['div', 'section']):
    div_id = div.get('id', '')
    if div_id.startswith('tab-') or 'tab-pane' in div.get('class', []):
        headings = [h.text.strip() for h in div.find_all(['h1', 'h2', 'h3', 'h4'])]
        print(f"\n--- Container #{div_id} ---")
        for h in headings[:5]:
            print("  Header:", h)
