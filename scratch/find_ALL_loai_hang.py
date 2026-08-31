import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('app.py', encoding='utf-8') as f:
    code = f.read()

lines = code.split('\n')
print("ALL 'Loại Hàng' indexing in app.py:")
for i, line in enumerate(lines, 1):
    if 'loại hàng' in line.lower():
        if 'df[' in line or 'df_' in line or 'raw_' in line or 'groupby' in line or 'pivot' in line or '==' in line:
            print(f"Line {i}: {line.strip()[:120]}")
