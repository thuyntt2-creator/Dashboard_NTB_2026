import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Let's find all id in index.html
ids = re.findall(r'id=["\']([^"\']+)["\']', text)
# filter for slide- or tab- or view-
slide_ids = [i for i in ids if any(k in i.lower() for k in ['slide', 'tab', 'section', 'part', 'view', 'page'])]
print("Matching IDs count:", len(slide_ids))
for i, s in enumerate(slide_ids):
    print(f"  {i+1}: {s}")
