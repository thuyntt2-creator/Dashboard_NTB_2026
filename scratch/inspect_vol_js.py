import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

p1 = text.find('function renderVolumeTab')
p2 = text.find('function renderGtcTongTab')
print(text[p1:p2 if p2 != -1 else p1+3500])
