import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('app.py', encoding='utf-8') as f:
    code = f.read()

lines = code.split('\n')
print("ALL occurrences of 'Tỉnh' or 'tỉnh' in app.py:")
for i, line in enumerate(lines, 1):
    if 'tỉnh' in line.lower():
        if 'df[' in line or 'df_' in line or 'raw_' in line or 'dict(' in line or 'fillna' in line or 'groupby' in line:
            print(f"Line {i}: {line.strip()}")
