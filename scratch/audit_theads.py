import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

theads = re.findall(r'<table[^>]*id=["\']([^"\']+)["\'][^>]*>.*?<thead>(.*?)</thead>', html, re.DOTALL)
for tid, th in theads:
    th_cleaned = re.sub(r'<[^>]+>', ' ', th)
    th_cleaned = ' '.join(th_cleaned.split())
    if 'W37' in th_cleaned or 'W36' in th_cleaned or 'W35' in th_cleaned:
        print(f"{tid}: {th_cleaned}")
