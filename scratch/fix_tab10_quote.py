# -*- coding: utf-8 -*-
with open('scratch/make_final_script.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if 'Tab 11 xem Báo cáo điều hành KTC & Vận tải đường trục' in line:
        new_lines.append('Bây giờ, em xin phép chuyển sang Tab 11 xem Báo cáo điều hành KTC & Vận tải đường trục ạ!"""\n')
    else:
        new_lines.append(line)

with open('scratch/make_final_script.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Fixed Tab 10 quote successfully!")
