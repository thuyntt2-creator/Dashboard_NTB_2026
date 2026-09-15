import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

banners = re.findall(r'(<div class="exec-banner".*?</div>\s*</div>\s*</div>)', content, re.DOTALL)
print(f"Found {len(banners)} exec-banners in index.html:")
for i, b in enumerate(banners):
    # print line number approx
    idx = content.find(b)
    line_num = content[:idx].count('\n') + 1
    # print header
    title = re.findall(r'<h3>(.*?)</h3>', b)
    t = title[0] if title else "No Title"
    print(f"\n--- Banner {i+1} at Line {line_num}: {t} ---")
    p = re.findall(r'<p>(.*?)</p>', b, re.DOTALL)
    if p:
        clean_p = re.sub(r'<.*?>', '', p[0]).strip()
        print(clean_p[:200] + '...' if len(clean_p) > 200 else clean_p)
