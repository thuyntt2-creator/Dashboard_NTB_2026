# -*- coding: utf-8 -*-
with open('scratch/test_exact.py', 'r', encoding='utf-8') as f:
    text = f.read()

msg = text.split('"""')[1]

with open('scratch/line_analysis.txt', 'w', encoding='utf-8') as out:
    out.write(f"Total length: {len(msg)}\n")
    lines = msg.split('\n')
    for i, l in enumerate(lines):
        out.write(f"Line {i+1} ({len(l)} chars): {l}\n")
