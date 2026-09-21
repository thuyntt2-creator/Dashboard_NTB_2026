import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Look for sidebar or menu
sidebar = re.findall(r'<(?:button|a|li|div)[^>]*class="[^"]*(?:nav|tab|menu|slide)[^"]*"[^>]*>(.*?)</(?:button|a|li|div)>', text)
print("Nav/Tab/Menu elements count:", len(sidebar))
for s in sidebar:
    clean = re.sub('<[^<]+?>', '', s).strip()
    if clean and len(clean) < 60:
        print(" ", clean)

# Also search for "phần" or "Phần" or numbers
print("\n--- Search for 'Phần' or 'phần' in index.html ---")
phan = re.findall(r'(phần\s*\d+[^<\n\r]+)', text, re.IGNORECASE)
for p in phan[:30]:
    print(" ", p)
