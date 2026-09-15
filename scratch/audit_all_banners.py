import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

matches = list(re.finditer(r'<div class="exec-banner[^"]*".*?</div>\s*</div>', text, re.DOTALL))
print(f"Total exec-banners found: {len(matches)}\n")

for i in range(min(12, len(matches))):
    m = matches[i]
    content = m.group(0)
    h3 = re.search(r'<h3[^>]*>(.*?)</h3>', content, re.DOTALL)
    h3_text = h3.group(1).strip() if h3 else 'NO TITLE'
    p = re.search(r'<p[^>]*>(.*?)</p>', content, re.DOTALL)
    p_text = p.group(1).strip() if p else 'NO TEXT'
    
    mentions = re.findall(r'W\d\d', p_text)
    print(f"==================================================")
    print(f"BANNER #{i+1}: {h3_text}")
    print(f"Weeks mentioned: {set(mentions)}")
    for line in p_text.split('<br>'):
        clean_l = re.sub(r'<[^>]+>', '', line).strip()
        if clean_l:
            print(f"  • {clean_l}")
    print()
