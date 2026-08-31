import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('app.py', encoding='utf-8') as f:
    code = f.read()

lines = code.split('\n')
print("Search for DB / Vercel / CSV reading in app.py:")
for i, line in enumerate(lines, 1):
    if 'VERCEL' in line or 'load_df_from_db' in line or 'save_df_to_db' in line or 'resolve_path' in line:
        if i % 10 == 0 or 'def ' in line or 'ops_ltc' in line:
            print(f'Line {i}: {line.strip()[:100]}')
