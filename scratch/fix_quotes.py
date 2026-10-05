# -*- coding: utf-8 -*-
with open('scratch/make_final_script.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if 'mổ xẻ tình trạng Rớt luân chuyển KTC' in line:
        new_lines.append('Bây giờ, em xin chuyển sang Tab 9 mổ xẻ tình trạng Rớt luân chuyển KTC ạ!"""\n')
    else:
        new_lines.append(line)

with open('scratch/make_final_script.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Line 472 fixed successfully!")
