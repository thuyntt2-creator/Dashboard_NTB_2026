import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', encoding='utf-8') as f:
    content = f.read()

# Find all blocks with class="exec-banner" or class="header-callout" or containing W38
matches = []
for m in re.finditer(r'<div class="[^"]*banner[^"]*"[^>]*>([\s\S]*?)</div>\s*</div>', content):
    matches.append(m.group(0))

print(f"Total banners found: {len(matches)}")
for i, b in enumerate(matches):
    print(f"\n--- BANNER {i+1} ---")
    lines = [line.strip() for line in b.split('\n') if line.strip()]
    for line in lines[:8]:
        print("  ", line[:100])
