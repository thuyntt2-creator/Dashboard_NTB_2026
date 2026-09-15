# -*- coding: utf-8 -*-
import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find all exec-banner or tab headers
matches = re.findall(r'<div class="exec-banner[^"]*"[\s\S]*?</div>\s*</div>\s*</div>', html)
print(f"Found {len(matches)} banner blocks in index.html:")
for i, m in enumerate(matches, 1):
    # Extract h2 or h3 and first 150 chars of p
    title = re.search(r'<h[23][^>]*>(.*?)</h[23]>', m)
    p = re.search(r'<p[^>]*>([\s\S]*?)</p>', m)
    t_text = title.group(1) if title else "No title"
    p_text = p.group(1)[:120].replace('\n', ' ') if p else "No p"
    print(f"\nBanner {i}: {t_text}")
    print(f"  Snippet: {p_text}...")
