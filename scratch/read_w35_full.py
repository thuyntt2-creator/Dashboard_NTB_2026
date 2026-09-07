import sys
sys.stdout.reconfigure(encoding='utf-8')
from docx import Document

doc = Document(r'C:\Users\lap4all\Downloads\KICH_BAN_THUYET_TRINH_W35_CHUAN_SO_LIEU_V4.docx')
lines = []
for i, para in enumerate(doc.paragraphs):
    if para.text.strip():
        lines.append(f'---P{i}---')
        lines.append(para.text)

content = '\n'.join(lines)
with open('scratch/w35_script_content.txt', 'w', encoding='utf-8') as f:
    f.write(content)
print('Saved', len(content), 'chars,', len(lines), 'lines')
