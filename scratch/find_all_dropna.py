import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('app.py', encoding='utf-8') as f:
    code = f.read()

lines = code.split('\n')
print("All dropna(subset=...) in app.py:")
for i, line in enumerate(lines, 1):
    if 'dropna(subset=' in line:
        print(f"Line {i}: {line.strip()}")
