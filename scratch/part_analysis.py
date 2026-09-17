# -*- coding: utf-8 -*-
with open('scratch/msg_under_4k_confirmed.txt', 'r', encoding='utf-8') as f:
    text = f.read()

parts = text.split('\n\n')
with open('scratch/parts_out.txt', 'w', encoding='utf-8') as out:
    out.write(f"Total parts: {len(parts)}\n")
    for i, p in enumerate(parts):
        first_line = p.split('\n')[0]
        out.write(f"Part {i+1} ({len(p)}): {first_line[:30]}\n")
