# -*- coding: utf-8 -*-
with open('scratch/make_final_script.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('Báo cáo Truy thu 2 tuần ạ!"\n    },', 'Báo cáo Truy thu 2 tuần ạ!"""\n    },')
text = text.replace('Kinh doanh & Khách hàng F30 ạ!"\n    },', 'Kinh doanh & Khách hàng F30 ạ!"""\n    },')

with open('scratch/make_final_script.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Fixed closing quotes for Tab 13 and Tab 14 successfully!")
