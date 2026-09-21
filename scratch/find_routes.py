with open('app.py', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '@app.route' in line or 'def ' in line and ('hop' in line or 'slide' in line or 'tuan' in line):
        print(f"Line {i+1}: {line.strip()}")
