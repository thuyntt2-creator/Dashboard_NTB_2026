import sys, re
with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('class="data-table" id="table-ca-report-am"', 'class="custom-table" id="table-ca-report-am"')
html = html.replace('class="data-table" id="table-ca-report-bc"', 'class="custom-table" id="table-ca-report-bc"')

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Fixed table class')
