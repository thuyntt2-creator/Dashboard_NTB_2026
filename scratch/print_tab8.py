import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

p1 = text.find('id="tab-opr-tts"')
p2 = text.find('id="tab-rot-lc"')
print(text[p1-30:p2])
