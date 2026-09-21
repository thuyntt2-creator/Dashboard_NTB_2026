import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find slides or sections
sections = re.findall(r'<section[^>]*id=["\']([^"\']+)["\'][^>]*>', html)
print("Sections in index.html:", len(sections))
for i, s in enumerate(sections):
    print(f"  {i+1}: {s}")

# Find navigation links/items
nav_items = re.findall(r'<(?:a|button|li)[^>]*(?:data-target|data-slide|href)=["\']#?([^"\']+)["\'][^>]*>(.*?)</(?:a|button|li)>', html)
print("\nNav items in index.html:", len(nav_items))
for i, n in enumerate(nav_items[:30]):
    text = re.sub('<[^<]+?>', '', n[1]).strip()
    if text:
        print(f"  {i+1}: {n[0]} -> {text}")
