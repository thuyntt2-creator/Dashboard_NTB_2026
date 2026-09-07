import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix the broken JS and HTML replacements
html = html.replace(
    "onclick=\"switchTab('tab-ca-report',\n                'tab-fd', this)\"",
    "onclick=\"switchTab('tab-fd', this)\""
)
html = html.replace(
    "onclick=\"switchTab('tab-ca-report',\n                'tab-fd', document.querySelector('[onclick*=\\'tab-fd\\']'))\"",
    "onclick=\"switchTab('tab-fd', document.querySelector('[onclick*=\\'tab-fd\\']'))\""
)
html = html.replace(
    "{ id: 'tab-ca-report',\n                'tab-fd', name: 'Chỉ số FD' },",
    "{ id: 'tab-ca-report', name: 'Báo cáo Sản lượng Ca' },\n                { id: 'tab-fd', name: 'Chỉ số FD' },"
)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Fixed index.html syntax issues')
