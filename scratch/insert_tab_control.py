# -*- coding: utf-8 -*-
with open('scratch/tab_control_extracted.html', 'r', encoding='utf-8') as f:
    tab_control_html = f.read().strip()

with open('index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()

target = """<!-- ==================================================================== -->
<!-- TAB 13: QR CODE & COD TIỀN MẶT (4 SHEET GOOGLE SHEETS) -->
<!-- ==================================================================== -->
</div>"""

replacement = f"""<!-- ==================================================================== -->
<!-- TAB 13: QR CODE & COD TIỀN MẶT (4 SHEET GOOGLE SHEETS) -->
<!-- ==================================================================== -->
{tab_control_html}"""

if target in index_html:
    new_index_html = index_html.replace(target, replacement, 1)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_index_html)
    print("SUCCESSFULLY INSERTED TAB-CONTROL INTO INDEX.HTML!")
else:
    print("ERROR: Target marker not found in index.html!")
