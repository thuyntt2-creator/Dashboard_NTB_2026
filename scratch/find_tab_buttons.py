import re

with open("scratch/raw_sheet.html", "r", encoding="utf-8") as f:
    html = f.read()

# Let's search for sheet IDs and names in the HTML preview format.
# Usually there is a script block or tab buttons at the bottom.
# E.g. <li id="sheet-button-843153285" class="..."><a>Tab Name</a></li>
# Or inside bootstrap data.
# Let's search for all list items starting with sheet-button
tab_matches = re.findall(r'id=["\']sheet-button-(\d+)["\'][^>]*>\s*<a[^>]*>([^<]+)</a>', html)
print("Tab matches via list item link:", tab_matches)

# Let's also do a search for 'sheet-button-' in general
all_buttons = re.findall(r'sheet-button-(\d+)', html)
print("All button IDs:", set(all_buttons))

# Let's look around one of the buttons
if all_buttons:
    btn_id = list(set(all_buttons))[0]
    idx = html.find(f"sheet-button-{btn_id}")
    if idx != -1:
        print(f"\nContext around sheet-button-{btn_id}:")
        print(html[max(0, idx - 100): min(len(html), idx + 300)])
