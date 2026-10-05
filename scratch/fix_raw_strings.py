# -*- coding: utf-8 -*-
with open('scratch/make_final_script.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('print("Saved docx to C:\\Users', 'print(r"Saved docx to C:\\Users')
text = text.replace('print("Successfully updated C:\\Users', 'print(r"Successfully updated C:\\Users')
text = text.replace('print(f"Notice: C:\\Users', 'print(rf"Notice: C:\\Users')

with open('scratch/make_final_script.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Fixed raw strings successfully!")
