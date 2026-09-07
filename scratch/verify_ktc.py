import sys, json
sys.stdout.reconfigure(encoding='utf-8')

with open('data.js', 'r', encoding='utf-8') as f:
    content = f.read()

has_ktc = '"ktc"' in content
print('Has KTC in data.js:', has_ktc)

with open('app.js', 'r', encoding='utf-8') as f:
    app_content = f.read()

print('Has renderKtcTab:', 'function renderKtcTab' in app_content)
print('Has renderFillRateChart:', 'function renderFillRateChart' in app_content)
print('Has renderKtcBacklog:', 'function renderKtcBacklog' in app_content)
print('renderAll has KTC:', 'renderKtcTab()' in app_content)
print('tab-ktc in renderTabCharts:', 'tab-ktc' in app_content)
