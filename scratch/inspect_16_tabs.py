import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# find buttons or nav links corresponding to these tabs
tabs = [
    'tab-overview', 'tab-volume', 'tab-gtc-tong', 'tab-gtc-tts-ca1', 'tab-gan',
    'tab-odr', 'tab-ltc', 'tab-opr-tts', 'tab-rot-lc', 'tab-fd',
    'tab-ktc', 'tab-aging', 'tab-control', 'tab-truythu', 'tab-commercial', 'tab-bc-canhbao'
]

print(f"Total tabs: {len(tabs)}")
for i, tab in enumerate(tabs):
    # search where tab id is referenced in onclick or data-target or buttons
    pattern = rf'switchTab\(["\']{tab}["\']\)[^>]*>(.*?)<'
    match = re.search(pattern, text)
    if not match:
        pattern = rf'data-target=["\']{tab}["\'][^>]*>(.*?)<'
        match = re.search(pattern, text)
    if not match:
        pattern = rf'showTab\(["\']{tab}["\']\)[^>]*>(.*?)<'
        match = re.search(pattern, text)
    
    # Also find the banner title inside the tab
    banner_match = re.search(rf'id=["\']{tab}["\'].*?<h\d[^>]*>(.*?)</h\d>', text, re.DOTALL)
    banner_text = banner_match.group(1).strip() if banner_match else ""
    banner_clean = re.sub('<[^<]+?>', '', banner_text).strip()
    
    print(f"Phần {i+1} ({tab}): {banner_clean[:80]}")
