import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('app.py', encoding='utf-8') as f:
    code = f.read()

lines = code.split('\n')
print("ALL occurrences of 'Chi tiết' or 'chi tiết' in app.py:")
for i, line in enumerate(lines, 1):
    if 'chi tiết' in line.lower():
        print(f"Line {i}: {line.strip()}")
