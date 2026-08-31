import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('app.py', encoding='utf-8') as f:
    code = f.read()

lines = code.split('\n')
print("Direct indexing of Chi tiết in app.py:")
for i, line in enumerate(lines, 1):
    if "['Chi tiết']" in line or '["Chi tiết"]' in line or "groupby('Chi tiết')" in line:
        print(f"Line {i}: {line.strip()[:100]}")
