from bs4 import BeautifulSoup

with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

soup = BeautifulSoup(content, 'html.parser')
main = soup.find('main')
if main:
    direct_tabs = main.find_all('div', class_='tab-view', recursive=False)
    print(f'Direct children of main with class tab-view: {len(direct_tabs)}')
    for t in direct_tabs:
        print(f'  - {t.get("id")}')
        
    all_tabs = soup.find_all('div', class_='tab-view')
    print(f'\nTotal tab-view in doc: {len(all_tabs)}')
    for t in all_tabs:
        parent = t.parent.name
        parent_id = t.parent.get('id', '')
        parent_class = t.parent.get('class', [])
        print(f'  Tab {t.get("id")}: parent is <{parent} id="{parent_id}" class="{parent_class}">')
