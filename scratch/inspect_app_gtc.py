import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

p1 = text.find('renderGtcTongTab')
p2 = text.find('renderGtcCa1Tab')
if p2 == -1:
    p2 = text.find('renderGtcTtsCa1Tab')
if p2 == -1:
    p2 = text.find('renderGanTab')

print(text[p1-100:p2 if p2 != -1 else p1+2500])
