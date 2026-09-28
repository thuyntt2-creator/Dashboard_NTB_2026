import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Overview banner
old_ov = '''            <h3 id="banner-overview-title">TỔNG HỢP TRỌNG TÂM HỌP TUẦN W38 — VÙNG NAM TRUNG BỘ</h3>
            <p id="banner-overview-summary">
              • <strong>Sản lượng Giao Full Hàng:</strong> Đạt <strong>345,994 đơn</strong> (Tuần W38 kết thúc 20/09/2026, -11,255 đơn / -3.2% WoW so với W37: 357,249 đơn).<br>
              • <strong>Sản lượng TikTok Shop (TTS):</strong> Đạt <strong>69,274 đơn</strong> (tăng <strong>+555 đơn / +0.8% WoW</strong> so với W37), chiếm 20.0% tổng sản lượng toàn vùng.<br>
              • <strong>Chất lượng vận hành:</strong> %ODR Full hàng đạt <strong>91.2%</strong>, %ODR TTS đạt <strong>90.8%</strong>, %LTC đạt <strong>90.4%</strong>. Tỷ lệ Rớt LC <strong>3.32%</strong>. Tỷ lệ %FD Hoàn Trả <strong>6.28%</strong>.<br>
              • <strong>Truy Thu & COD W38:</strong> Tiền Cần Truy Thu phát sinh <strong>282.4 Tr ₫</strong> (tăng +241.0 Tr ₫ WoW), Tỷ lệ tiền mặt COD đạt <strong>43.1%</strong> (tăng +3.0%p WoW).
            </p>
          </div>
        </div>
        <div class="exec-banner-actions">
          <span class="badge-tag badge-tag-amber" style="font-size: 12px; padding: 6px 12px;">
            <i data-lucide="target"></i> Mục tiêu W38: GTC ≥ 60%
          </span>'''

new_ov = '''            <h3 id="banner-overview-title">TỔNG HỢP TRỌNG TÂM HỌP TUẦN W39 — VÙNG NAM TRUNG BỘ</h3>
            <p id="banner-overview-summary">
              • <strong>Sản lượng Giao Full Hàng:</strong> Đạt <strong>328,925 đơn</strong> (Tuần W39 kết thúc 27/09/2026, -14,672 đơn / -4.3% WoW so với W38: 343,597 đơn).<br>
              • <strong>Sản lượng TikTok Shop (TTS):</strong> Đạt <strong>72,781 đơn</strong> (tăng <strong>+4,055 đơn / +5.9% WoW</strong> so với W38: 68,726 đơn), chiếm 22.1% tổng sản lượng toàn vùng.<br>
              • <strong>Chất lượng vận hành:</strong> %ODR Full hàng đạt <strong>90.8%</strong>, %LTC đạt <strong>90.1%</strong>. Tỷ lệ Rớt LC <strong>1.52%</strong> (giảm mạnh -1.80%p WoW). Tỷ lệ %FD Hoàn Trả <strong>7.64%</strong>.<br>
              • <strong>Truy Thu & COD W39:</strong> Tiền Cần Truy Thu phát sinh <strong>174.7 Tr ₫</strong> (giảm -21.2 Tr ₫ WoW), Tỷ lệ tiền mặt COD đạt <strong>40.1%</strong> (giảm -3.0%p WoW).
            </p>
          </div>
        </div>
        <div class="exec-banner-actions">
          <span class="badge-tag badge-tag-amber" style="font-size: 12px; padding: 6px 12px;">
            <i data-lucide="target"></i> Mục tiêu W39: GTC ≥ 60%
          </span>'''

if old_ov in html:
    html = html.replace(old_ov, new_ov)
    print("Replaced overview banner successfully!")
else:
    print("Warning: old_ov not found exactly, will use regex")
    html = re.sub(
        r'<h3 id="banner-overview-title">.*?</h3>\s*<p id="banner-overview-summary">.*?</p>\s*</div>\s*</div>\s*<div class="exec-banner-actions">\s*<span class="badge-tag badge-tag-amber"[^>]*>.*?</span>',
        new_ov,
        html,
        flags=re.DOTALL
    )

# 2. Week filter select options
html = html.replace(
    '''          <select id="filter-week" class="bi-select" title="Chọn tuần báo cáo">
            <option value="W38" selected>Tuần W38 (Hiện tại)</option>
            <option value="W37">Tuần W37 (Tuần trước)</option>
            <option value="W36">Tuần W36</option>
            <option value="W35">Tuần W35</option>
          </select>''',
    '''          <select id="filter-week" class="bi-select" title="Chọn tuần báo cáo">
            <option value="W39" selected>Tuần W39 (Hiện tại)</option>
            <option value="W38">Tuần W38 (Tuần trước)</option>
            <option value="W37">Tuần W37</option>
            <option value="W36">Tuần W36</option>
          </select>'''
)

# 3. Target and other banners in tabs
html = html.replace('Mục tiêu W38: GTC ≥ 60%', 'Mục tiêu W39: GTC ≥ 60%')
html = html.replace('Target ≥ 76.0% (W38: 71.36%)', 'Target ≥ 76.0% (W39: 73.5%)')
html = html.replace('Gán Tổng W38: 80.6% (Target ≥ 90.0%)', 'Gán Tổng W39: 82.5% (Target ≥ 90.0%)')
html = html.replace('OPR TTS W38: 83.0% (Đạt KPI ≥ 80.0%)', 'OPR TTS W39: 84.5% (Đạt KPI ≥ 80.0%)')
html = html.replace('Tổng rớt W38: 252 đơn (3.32%)', 'Tổng rớt W39: 115 đơn (1.52%)')
html = html.replace('BÁO CÁO ĐIỀU HÀNH KTC & VẬN TẢI — VÙNG NAM TRUNG BỘ (W38)', 'BÁO CÁO ĐIỀU HÀNH KTC & VẬN TẢI — VÙNG NAM TRUNG BỘ (W39)')
html = html.replace('Chu kỳ W38 (14/09 – 20/09/2026)', 'Chu kỳ W39 (21/09 – 27/09/2026)')
html = html.replace('W38 vs W37', 'W39 vs W38')
html = html.replace('W37 vs W38', 'W38 vs W39')
html = html.replace('Tuần W37 vs Tuần W38', 'Tuần W38 vs Tuần W39')
html = html.replace('TUẦN W37 vs TUẦN W38', 'TUẦN W38 vs TUẦN W39')
html = html.replace('TUẦN W37 vs TUẦN W38', 'TUẦN W38 vs TUẦN W39')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("index.html banners updated successfully!")
