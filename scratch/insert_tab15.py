import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

with open('scratch/make_bc_canhbao_prominent.py', 'r', encoding='utf-8') as f:
    sc = f.read()

start_marker = 'dedicated_tab_view = """'
end_marker = '"""\n\n# Insert dedicated_tab_view'

start_idx = sc.find(start_marker) + len(start_marker)
end_idx = sc.find(end_marker)

tab_view = sc[start_idx:end_idx].strip()

if 'id="tab-bc-canhbao"' not in html:
    pos = html.find('</main>')
    if pos != -1:
        html = html[:pos] + "\n  " + tab_view + "\n\n  " + html[pos:]
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("Successfully inserted tab-bc-canhbao before </main>!")
    else:
        print("Could not find </main>!")
else:
    print("tab-bc-canhbao already in html!")
