import sys, re
sys.stdout.reconfigure(encoding='utf-8')

content = open('index.html', encoding='utf-8').read()
tables = re.findall(r'<table[^>]*id=["\']([^"\']+)["\'][^>]*>([\s\S]*?)</table>', content)
for tid, tbl in tables:
    m = re.search(r'<thead>([\s\S]*?)</thead>', tbl)
    if m:
        th = m.group(1)
        if any(w in th for w in ['W34', 'W35', 'W36', 'W37']):
            ths = re.findall(r'<th[^>]*>(.*?)</th>', th, re.DOTALL)
            clean_ths = [re.sub(r'<[^>]+>', '', t).strip() for t in ths]
            print(f"{tid}: {' | '.join(clean_ths)}")
