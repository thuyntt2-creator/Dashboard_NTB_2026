with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'ops_fd' in l or 'process_fd_report' in l:
        print(f"Line {i+1}: {l.strip()}")
