import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Find sections in tabs
for tab_name in ['tab-volume', 'tab-gtc-tong', 'tab-odr', 'tab-ltc']:
    match = re.search(rf'id=["\']{tab_name}["\'].*?</section>', text, re.DOTALL)
    if match:
        tab_content = match.group(0)
        # Find subheaders or card titles or table ids
        cards = re.findall(r'<(?:div|table|section)[^>]*(?:id|class)=["\']([^"\']*(?:tinh|province|am|table|grid|card)[^"\']*)["\']', tab_content)
        print(f"=== {tab_name} ===")
        print("  Length:", len(tab_content))
        # Find h2, h3, h4 titles
        headings = re.findall(r'<h[234][^>]*>(.*?)</h[234]>', tab_content)
        for h in headings:
            print("   Heading:", re.sub('<[^<]+?>', '', h).strip())
