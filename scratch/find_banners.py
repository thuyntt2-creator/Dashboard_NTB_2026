import sys, re
sys.stdout.reconfigure(encoding='utf-8')

content = open('index.html', encoding='utf-8').read()
# find all exec-banner divs
# Pattern for exec-banner
matches = re.finditer(r'<div class="exec-banner"[^>]*>([\s\S]*?)(?=<div class="exec-banner"|<div id="tab-|$)', content)
for idx, m in enumerate(matches):
    b = m.group(0)
    m_title = re.search(r'<h[23][^>]*>(.*?)</h[23]>', b)
    title = m_title.group(1) if m_title else 'NO_TITLE'
    p = re.search(r'<p[^>]*>([\s\S]*?)</p>', b)
    text = re.sub(r'<[^>]+>', '', p.group(1)).strip() if p else ''
    badge = re.search(r'<span[^>]*class="badge-tag[^"]*"[^>]*>([\s\S]*?)</span>', b)
    badge_txt = re.sub(r'<[^>]+>', '', badge.group(1)).strip() if badge else ''
    print(f"=== Banner {idx+1}: {title} ===")
    print(f"Badge: {badge_txt}")
    print(f"Text: {text[:180]}...\n")
