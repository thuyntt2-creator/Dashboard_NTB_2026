import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

funcs = [
    'renderTrendSanLuongChart',
    'renderTrendRatesChart',
    'renderSanLuongTinhChart',
    'renderVolAMChart',
    'renderGtcTongBarChart',
    'renderGtcTinhChart',
    'renderGtcTtsCa1BarChart',
    'renderGanBarChart',
    'renderOdrChart',
    'renderLtcChart',
    'renderOprGroupedChart',
    'renderRotLcChart',
    'renderKdDoanhThuChart',
    'renderCodTmAmBar',
    'renderTruyThuLoaiBar'
]

for fn in funcs:
    print(f"{fn}: {'EXISTS' if ('function ' + fn) in text else 'MISSING'}")
