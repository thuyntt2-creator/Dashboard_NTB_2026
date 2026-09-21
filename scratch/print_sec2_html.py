import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('KICH_BAN_THUYET_TRINH_W38_NAM_TRUNG_BO.html', 'r', encoding='utf-8') as f:
    text = f.read()

p = text.find('id="sec-2"')
print(text[p:p+1200])
