import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('app.py', encoding='utf-8') as f:
    code = f.read()

lines = code.split('\n')
print("ALL percentage column indexing in app.py:")
for i, line in enumerate(lines, 1):
    if '%' in line:
        if 'df[' in line or 'df_' in line or 'raw_' in line or 'normalize_pct_col' in line or 'dropna' in line:
            print(f"Line {i}: {line.strip()[:120]}")
