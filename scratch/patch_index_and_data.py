import json
import re

# 1. Update data.json with churn data
print("Updating data.json...")
with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

with open('scratch/top10_churn.json', 'r', encoding='utf-8') as f:
    churn_data = json.load(f)

if 'kinh_doanh' not in d:
    d['kinh_doanh'] = {}

d['kinh_doanh']['churn_top10'] = churn_data['top10_drop']
d['kinh_doanh']['churn_zero'] = churn_data['top_zero']

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

with open('data.js', 'w', encoding='utf-8') as f:
    f.write("window.DASHBOARD_DATA = " + json.dumps(d, ensure_ascii=False, indent=2) + ";\n")

print("data.json and data.js updated with churn data!")

# 2. Patch index.html
print("Patching index.html...")
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Tab 2 (Volume)
html = html.replace(
    'SẢN LƯỢNG GIAO 18 AM (CỘT W34 vs W35 + ĐƯỜNG BIẾN ĐỘNG Δ)',
    'SẢN LƯỢNG GIAO 18 AM (CỘT W35 vs W36 + ĐƯỜNG BIẾN ĐỘNG Δ)'
)
html = html.replace(
    'data-mode="w34_vs_w35_full">📊 Sản Lượng Full Hàng (Cột + Đường Line Δ)',
    'data-mode="w34_vs_w35_full">📊 Sản Lượng Full Hàng (Cột W35 vs W36 + Đường Line Δ)'
)
html = html.replace(
    'data-mode="w34_vs_w35_tts">⚡ Sản Lượng TikTok Shop (Cột + Đường Line Δ)',
    'data-mode="w34_vs_w35_tts">⚡ Sản Lượng TikTok Shop (Cột W35 vs W36 + Đường Line Δ)'
)
html = html.replace(
    '<th class="num">Full W34</th>\n                    <th class="num" style="background: var(--color-blue-bg); font-weight:800;">Full W35</th>',
    '<th class="num">Full W35</th>\n                    <th class="num" style="background: var(--color-blue-bg); font-weight:800;">Full W36</th>'
)
html = html.replace(
    '<th class="num">TTS W34</th>\n                    <th class="num" style="background: var(--color-amber-bg); font-weight:800; color:#ea580c;">TTS W35</th>',
    '<th class="num">TTS W35</th>\n                    <th class="num" style="background: var(--color-amber-bg); font-weight:800; color:#ea580c;">TTS W36</th>'
)

# Tab 3 (GTC Tổng)
html = html.replace(
    '<!-- TAB 3: %GTC TỔNG TOÀN MẠNG (W34 vs W35) -->',
    '<!-- TAB 3: %GTC TỔNG TOÀN MẠNG (W35 vs W36) -->'
)
html = html.replace(
    '<span id="chart-gtc-tong-title">BIỂU ĐỒ SO SÁNH %GTC TỔNG W34 vs W35 THEO 18 AM (FULL HÀNG)</span>',
    '<span id="chart-gtc-tong-title">BIỂU ĐỒ SO SÁNH %GTC TỔNG W35 vs W36 THEO 18 AM (FULL HÀNG)</span>'
)
html = html.replace(
    '<th class="num">W34</th>\n                    <th class="num" style="background: var(--color-blue-bg); font-weight: 800;">W35</th>',
    '<th class="num">W35</th>\n                    <th class="num" style="background: var(--color-blue-bg); font-weight: 800;">W36</th>'
)
html = html.replace(
    '<th class="num">TTS W34</th>\n                    <th class="num" style="background: var(--color-amber-bg); font-weight: 800; color: #ea580c;">TTS W35</th>',
    '<th class="num">TTS W35</th>\n                    <th class="num" style="background: var(--color-amber-bg); font-weight: 800; color: #ea580c;">TTS W36</th>'
)

# Tab 5 (Gán)
html = html.replace(
    '<th class="num" style="color: #ffffff;">W34</th>\n                    <th class="num" style="color: #ffffff;">W35</th>',
    '<th class="num" style="color: #ffffff;">W35</th>\n                    <th class="num" style="color: #ffffff;">W36</th>'
)
html = html.replace(
    '<th class="num">W34</th>\n                    <th class="num" style="background: var(--color-amber-bg); font-weight:800;">Ca 1+Tồn W35</th>',
    '<th class="num">W35</th>\n                    <th class="num" style="background: var(--color-amber-bg); font-weight:800;">Ca 1+Tồn W36</th>'
)
html = html.replace(
    '<th class="num">Tổng W34</th>\n                    <th class="num" style="background: var(--color-purple-bg); font-weight:800; color:#7e22ce;">Gán Tổng W35</th>',
    '<th class="num">Tổng W35</th>\n                    <th class="num" style="background: var(--color-purple-bg); font-weight:800; color:#7e22ce;">Gán Tổng W36</th>'
)

# Tab 6 (ODR)
html = html.replace(
    '<th class="num">W34</th>\n                    <th class="num" style="background: var(--color-green-bg); font-weight:800;">W35</th>',
    '<th class="num">W35</th>\n                    <th class="num" style="background: var(--color-green-bg); font-weight:800;">W36</th>'
)
html = html.replace(
    '<th class="num">TTS W34</th>\n                    <th class="num" style="background: var(--color-amber-bg); font-weight: 800; color: #ea580c;">TTS W35</th>',
    '<th class="num">TTS W35</th>\n                    <th class="num" style="background: var(--color-amber-bg); font-weight: 800; color: #ea580c;">TTS W36</th>'
)

# Tab 9 (Rớt LC Top BC)
html = html.replace(
    '<th class="num" style="background: var(--color-red-bg); font-weight:800; color:#b91c1c;">% Rớt LC (W35)</th>',
    '<th class="num" style="background: var(--color-red-bg); font-weight:800; color:#b91c1c;">% Rớt LC (W36)</th>'
)

# Tab 13: Add Top 10 Churn Table if not present
churn_html = '''
      <!-- ROW 4: TOP KHÁCH HÀNG GIẢM ĐƠN / RỜI BỎ (CHURN ANALYSIS) -->
      <div class="report-card" style="margin-top: 16px;">
        <div class="report-card-header" style="background: linear-gradient(135deg, rgba(239, 68, 68, 0.08), rgba(245, 158, 11, 0.08)); border-bottom: 1px solid rgba(239, 68, 68, 0.2);">
          <div class="report-card-title" style="color: #b91c1c; font-weight: 800; font-size: 15px;">
            <i data-lucide="user-x" style="color: #ef4444;"></i>
            TOP 10 KHÁCH HÀNG CÓ SẢN LƯỢNG GIẢM / RỜI BỎ LỚN NHẤT (KỲ 23–29/8 vs KỲ 30/8–5/9)
          </div>
          <div style="display: flex; gap: 8px; align-items: center;">
            <span class="badge-tag badge-tag-red">🔴 Rời Bỏ / Giảm Đơn Cao</span>
            <span class="badge-tag badge-tag-blue">Chuẩn Kỳ Kinh Doanh</span>
          </div>
        </div>
        <div class="report-card-body">
          <div class="bi-table-wrap">
            <table class="bi-table" id="table-kd-churn-top10">
              <thead>
                <tr style="background: #1e293b; color: #ffffff;">
                  <th class="center" style="width: 44px; color:#ffffff;">#</th>
                  <th style="color:#ffffff;">Mã KH</th>
                  <th style="color:#ffffff;">Tên Shop / Khách Hàng</th>
                  <th style="color:#ffffff;">AM Phụ Trách</th>
                  <th style="color:#ffffff;">Bưu Cục Quản Lý</th>
                  <th class="num" style="color:#ffffff;">Kỳ Trước (23–29/8)</th>
                  <th class="num" style="background: #ef4444; color:#ffffff; font-weight:800;">Kỳ Này (30/8–5/9)</th>
                  <th class="num" style="color:#ffffff;">Biến Động (Δ Đơn)</th>
                  <th class="num" style="color:#ffffff;">% Giảm</th>
                  <th class="center" style="color:#ffffff;">Tình Trạng</th>
                </tr>
              </thead>
              <tbody></tbody>
            </table>
          </div>
        </div>
      </div>
'''

if 'id="table-kd-churn-top10"' not in html:
    # insert before </div>\n\n  </main> of tab 13
    idx_end = html.find('<!-- Upload Modal -->')
    if idx_end != -1:
        # find last </div> before Upload Modal
        target_pos = html.rfind('</div>', 0, idx_end)
        html = html[:target_pos] + churn_html + '\n    ' + html[target_pos:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("index.html patched successfully!")
