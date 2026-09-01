import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

text = text.replace("renderGtcTongBarChart();\n      renderGtcTinhChart();", "renderGtcTongBarChart();")
text = text.replace("renderGtcTongBarChart(); renderGtcTinhChart();", "renderGtcTongBarChart();")
text = text.replace("renderGtcTinhChart();", "")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(text)

print("Fixed renderGtcTinhChart call in app.js successfully!")
