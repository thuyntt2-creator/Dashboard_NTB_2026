import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

funcs = ['renderGanTab', 'renderGanBarChart', 'renderOdrTab', 'renderOdrChart', 'renderLtcTab', 'renderLtcChart', 'renderOprTab', 'renderOprGroupedChart', 'renderTransportTab', 'renderRotLcChart']

for fn in funcs:
    p = text.find(f'function {fn}')
    if p != -1:
        print(f"=== FUNCTION {fn} ===")
        print(text[p:p+1200])
        print()
    else:
        print(f"MISSING: {fn}")
