# -*- coding: utf-8 -*-
with open('scratch/test_super.py', 'r', encoding='utf-8') as f:
    text = f.read()

s = text.split('"""')[1]
lines = s.split('\n')
print("Total chars:", len(s))
print("Total lines:", len(lines))
# print each hub length
cur = ""
name = ""
with open('scratch/hub_breakdown.txt', 'w', encoding='utf-8') as out:
    for l in lines:
        if l.startswith(('1. [', '2. [', '3. [', '4. [', '5. [', '6. [', '7. [', '8. [', '9. [', '10. [', '11. [', 'NHÓM', 'III.', 'I. ')):
            if cur:
                out.write(f"{name}: {len(cur)} chars\n")
            cur = l + "\n"
            name = l[:20]
        else:
            cur += l + "\n"
    if cur:
        out.write(f"{name}: {len(cur)} chars\n")
