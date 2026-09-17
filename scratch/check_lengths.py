# -*- coding: utf-8 -*-
with open('scratch/make_under_4k.py', 'r', encoding='utf-8') as f:
    text = f.read()

msg = text.split('"""')[1].strip()
lines = msg.split('\n')
with open('scratch/detailed_lines.txt', 'w', encoding='utf-8') as out:
    out.write(f"Total lines: {len(lines)}\n")
    out.write(f"Total chars: {len(msg)}\n")
    for i, l in enumerate(lines):
        out.write(f"{i+1:02d} ({len(l):03d}): {l}\n")
