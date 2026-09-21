with open('app.js', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

import re
# Look for slide titles or list of slides
slides = re.findall(r'title:\s*["\']([^"\']+)["\']', text)
print("Titles found in app.js:", len(slides))
for i, t in enumerate(slides[:30]):
    print(f"  {i+1}: {t}")

# Look for slides array or navigation items
nav = re.findall(r'{\s*id:\s*["\']([^"\']+)["\'],\s*name:\s*["\']([^"\']+)["\']', text)
print("\nNav objects found:", len(nav))
for i, n in enumerate(nav):
    print(f"  {i+1}: {n[0]} -> {n[1]}")
