import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', encoding='utf-8') as f:
    content = f.read()

# Find all blocks containing W38 within exec-banner or section-banner
for m in re.finditer(r'<div class="[^"]*banner[^"]*"[\s\S]*?</div>\s*</div>', content):
    b_text = m.group(0)
    if 'W38' in b_text or 'W37' in b_text:
        print("=== MATCHING BANNER ===")
        print(b_text[:400])
        print("...\n")
