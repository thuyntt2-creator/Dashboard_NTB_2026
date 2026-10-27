with open('app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'function renderControlTab' in l or 'function renderCod' in l or 'window.setCodSegment' in l:
        print(f"Line {i+1}: {l.strip()}")
