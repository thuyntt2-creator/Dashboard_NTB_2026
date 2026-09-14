import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

# 1. Update build_data_js.py
with open('build_data_js.py', 'r', encoding='utf-8') as f:
    bd = f.read()

bd = bd.replace("            {'id': 'cod_tm', 'title': 'Tỷ Lệ COD Tiền Mặt', 'val': 0.396, 'unit': '%', 'diff': 0.011, 'diff_pct': 0.030, 'is_good': False, 'icon': 'banknote'},\n", "")

with open('build_data_js.py', 'w', encoding='utf-8') as f:
    f.write(bd)
print("✓ Removed cod_tm from build_data_js.py")

# 2. Update app.js
with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Remove cod_tm from pairedCards
old_cod_card = """        {
          id: 'cod_tm',
          title: 'Tỷ Lệ COD Tiền Mặt',
          mainVal: fPct(codVal),
          mainUnit: 'Tiền mặt',
          subVal: `${fPct(1 - codVal)} (Chuyển khoản QR)`,
          diff: codDiff,
          isHigherBetter: false,
          colorCls: 'kpi-amber',
          icon: 'qr-code'
        },
"""
if old_cod_card in js:
    js = js.replace(old_cod_card, "")
    print("✓ Removed cod_tm card from pairedCards in app.js")
else:
    # try regex
    js = re.sub(r'\s*\{\s*id:\s*[\'"]cod_tm[\'"].*?icon:\s*[\'"]qr-code[\'"]\s*\},?', '', js, flags=re.DOTALL)
    print("✓ Removed cod_tm card via regex in app.js")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)

# 3. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Hide COD Tiền Mặt tab button and re-index
old_tab_nav = """          <button class="tab-item" data-tab="tab-control">
            <i data-lucide="wallet"></i> 13. COD Tiền Mặt
          </button>
          <button class="tab-item" data-tab="tab-truythu">
            <i data-lucide="shield-alert"></i> 14. Báo Cáo Truy Thu
          </button>
          <button class="tab-item" data-tab="tab-commercial">
            <i data-lucide="trending-up"></i> 15. Kinh Doanh & F30
          </button>"""

new_tab_nav = """          <button class="tab-item" data-tab="tab-truythu">
            <i data-lucide="shield-alert"></i> 13. Báo Cáo Truy Thu
          </button>
          <button class="tab-item" data-tab="tab-commercial">
            <i data-lucide="trending-up"></i> 14. Kinh Doanh & F30
          </button>"""

if old_tab_nav in html:
    html = html.replace(old_tab_nav, new_tab_nav)
    print("✓ Updated tab navigation buttons in index.html")
else:
    print("Tab nav match failed, trying alternate replace")
    html = html.replace('<button class="tab-item" data-tab="tab-control">\n            <i data-lucide="wallet"></i> 13. COD Tiền Mặt\n          </button>', '')
    html = html.replace('14. Báo Cáo Truy Thu', '13. Báo Cáo Truy Thu')
    html = html.replace('15. Kinh Doanh & F30', '14. Kinh Doanh & F30')

# Hide the tab-control content div
html = html.replace('<div id="tab-control" class="tab-view">', '<div id="tab-control" class="tab-view" style="display: none !important;">')

# Update cache buster
import time
ts = str(int(time.time()))
html = re.sub(r'data\.js\?v=\d+', f'data.js?v={ts}', html)
html = re.sub(r'app\.js\?v=\d+', f'app.js?v={ts}', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("✓ Updated index.html successfully!")
