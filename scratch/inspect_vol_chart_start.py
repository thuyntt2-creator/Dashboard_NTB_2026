import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

p = text.find('function renderVolAMChart()')
print(text[p:p+1200])
