import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('app.py', encoding='utf-8') as f:
    code = f.read()

lines = code.split('\n')
print("ALL 'Time' indexing in app.py:")
for i, line in enumerate(lines, 1):
    if 'time' in line.lower():
        if 'df[' in line or 'df_' in line or 'raw_' in line or 'groupby' in line or 'pivot' in line or '==' in line or 'sort_values' in line:
            print(f"Line {i}: {line.strip()[:120]}")
