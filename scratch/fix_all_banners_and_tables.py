import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix typos caused by old string replace
html = html.replace('Đơn W38gày', 'Đơn Ngày')
html = html.replace('W38hất', 'Nhất')
html = html.replace('đơn W38hất', 'đơn nhất')

# 1. Update 4-week trend table headers W35, W36, W37, W38 -> W36, W37, W38, W39
html = re.sub(
    r'<th class="num">W35</th>\s*<th class="num">W36</th>\s*<th class="num">W37</th>\s*<th class="num"[^>]*>W38</th>',
    r'<th class="num">W36</th>\n                    <th class="num">W37</th>\n                    <th class="num">W38</th>\n                    <th class="num" style="background: var(--color-amber-bg); font-weight: 800; color: #ea580c;">W39</th>',
    html
)
html = html.replace('W35 – W38', 'W36 – W39')
html = html.replace('W35-W38', 'W36-W39')

# 2. Tab 3: %GTC Banner
html = html.replace(
    '<h3>PHÂN TÍCH HIỆU SUẤT %GTC TỔNG TOÀN MẠNG THEO 18 AM & 5 TỈNH (W38)</h3>',
    '<h3>PHÂN TÍCH HIỆU SUẤT %GTC TỔNG TOÀN MẠNG THEO 18 AM & 5 TỈNH (W39)</h3>'
)
html = re.sub(
    r'• <strong>%GTC Tổng Toàn Vùng \(W38\):</strong>.*?(?=•|</div>|</p>)',
    '• <strong>%GTC Tổng Toàn Vùng (W39):</strong> Full hàng đạt <strong>56.6%</strong> (+0.9%p WoW so với W38: 55.7%) và TTS đạt <strong>57.4%</strong> (+3.5%p WoW so với W38: 54.0%). ',
    html,
    flags=re.DOTALL
)

# 3. Tab 4: %GTC Ca 1 TTS Banner
html = html.replace(
    '<h3>PHÂN TÍCH CHUYÊN SÂU %GTC CA 1 TIKTOK SHOP (TARGET SLA ≥ 76.0%) (W38)</h3>',
    '<h3>PHÂN TÍCH CHUYÊN SÂU %GTC CA 1 TIKTOK SHOP (TARGET SLA ≥ 76.0%) (W39)</h3>'
)
html = re.sub(
    r'• <strong>Toàn Vùng TTS Ca 1 \(W38\):</strong>.*?(?=•|</div>|</p>)',
    '• <strong>Toàn Vùng TTS Ca 1 (W39):</strong> Đạt <strong>73.5%</strong> (tăng <strong>+2.1%p WoW</strong> so với 71.36% W38), áp sát ngưỡng Target SLA 76.0%. ',
    html,
    flags=re.DOTALL
)

# 4. Tab 5: % Gán Banner
html = re.sub(
    r'• <strong>Gán Tổng \(Ca1\+Ca2\+Tồn W38\):</strong>.*?(?=•|</div>|</p>)',
    '• <strong>Gán Tổng (Ca1+Ca2+Tồn W39):</strong> Full hàng đạt <strong>82.5%</strong> (+1.9%p WoW so với 80.6% W38); TTS đạt <strong>85.1%</strong> (+2.0%p WoW). ',
    html,
    flags=re.DOTALL
)

# 5. Tab 6: %ODR Banner
html = re.sub(
    r'• <strong>Toàn Vùng W38:</strong> Full Hàng đạt <strong>91.24%</strong>.*?(?=•|</div>|</p>)',
    '• <strong>Toàn Vùng W39:</strong> Full Hàng đạt <strong>90.8%</strong> và TTS đạt <strong>90.5%</strong>. ',
    html,
    flags=re.DOTALL
)

# 6. Tab 7: %LTC Banner
html = re.sub(
    r'• <strong>Toàn Vùng W38:</strong> Full hàng đạt <strong>90.36%</strong>.*?(?=•|</div>|</p>)',
    '• <strong>Toàn Vùng W39:</strong> Full hàng đạt <strong>90.1%</strong>, TTS đạt <strong>95.2%</strong>. ',
    html,
    flags=re.DOTALL
)

# 7. Tab 8: OPR TTS Banner
html = re.sub(
    r'• <strong>Toàn Vùng W38 \(Tổng Ngày \+ Đêm\):</strong>.*?(?=•|</div>|</p>)',
    '• <strong>Toàn Vùng W39 (Tổng Ngày + Đêm):</strong> Đạt <strong>84.5%</strong> (+1.5%p WoW so với 83.0% W38) — <strong>Vượt Target KPI ≥ 80.0%</strong>. ',
    html,
    flags=re.DOTALL
)

# 8. Tab 9: Rớt Luân Chuyển Banner
html = html.replace(
    '% RỚT LUÂN CHUYỂN THEO 18 AM PHỤ TRÁCH (W38)',
    '% RỚT LUÂN CHUYỂN THEO 18 AM PHỤ TRÁCH (W39)'
)
html = html.replace(
    'DANH SÁCH TOP 20 BƯU CỤC CÓ TỶ LỆ RỚT LUÂN CHUYỂN CAO NHẤT (W38)',
    'DANH SÁCH TOP 20 BƯU CỤC CÓ TỶ LỆ RỚT LUÂN CHUYỂN CAO NHẤT (W39)'
)
html = re.sub(
    r'• <strong>Tổng đơn rớt toàn vùng W38:</strong>.*?(?=•|</div>|</p>)',
    '• <strong>Tổng đơn rớt toàn vùng W39:</strong> Tỷ lệ rớt đạt <strong>1.52%</strong> (giảm mạnh <strong>-1.80%p WoW</strong> so với 3.32% W38), chất lượng luân chuyển cải thiện vượt bậc. ',
    html,
    flags=re.DOTALL
)

# 9. Tab 10: %FD Banner
html = html.replace(
    'BÁO CÁO TỶ LỆ %FD (RETURN / HOÀN TRẢ) — VÙNG NAM TRUNG BỘ',
    'BÁO CÁO TỶ LỆ %FD (RETURN / HOÀN TRẢ) — VÙNG NAM TRUNG BỘ (W39)'
)

# 10. Tab 11: KTC Banner
html = html.replace(
    'BÁO CÁO ĐIỀU HÀNH KTC & VẬN TẢI — VÙNG NAM TRUNG BỘ (W38)',
    'BÁO CÁO ĐIỀU HÀNH KTC & VẬN TẢI — VÙNG NAM TRUNG BỘ (W39)'
)
html = re.sub(
    r'• <strong>Tỷ Lệ Lấp Đầy Thùng / Xe:</strong> Tuần W38.*?(?=•|</div>|</p>)',
    '• <strong>Tỷ Lệ Lấp Đầy Thùng / Xe:</strong> Tuần W39 đạt <strong>47.7%</strong> (527 chuyến, 107 chuyến <30% thùng xe). ',
    html,
    flags=re.DOTALL
)

# 11. Tab 12: Aging & Treo LC
html = html.replace(
    'Aging: 4.373 đơn | Treo LC: 1.417 đơn (25 Bưu Cục)',
    'Aging: 1,468 đơn | Treo LC: 4,251 đơn'
)

# 12. Tab 13: COD
html = html.replace(
    'Tổng COD: -- Tr | % TM: --%',
    'Tổng COD: 80,733.6 Tr ₫ | % TM: 40.1%'
)

# 13. Tab 14: Truy thu
html = html.replace(
    '<th class="num" style="background: #0284c7; color:#ffffff; font-weight:800;" id="th-tt-loai-dc">Đơn W38</th>',
    '<th class="num" style="background: #0284c7; color:#ffffff; font-weight:800;" id="th-tt-loai-dc">Đơn W39</th>'
)
html = html.replace(
    '<th class="num" style="background: #dc2626; color:#ffffff; font-weight:800;" id="th-tt-loai-cc">Cần Thu W38 (Tr ₫)</th>',
    '<th class="num" style="background: #dc2626; color:#ffffff; font-weight:800;" id="th-tt-loai-cc">Cần Thu W39 (Tr ₫)</th>'
)
html = html.replace('Đơn Tuần W38', 'Đơn Tuần W39')
html = html.replace('Cần Thu W38 (Tr ₫)', 'Cần Thu W39 (Tr ₫)')
html = html.replace('Ticket W38', 'Ticket W39')
html = html.replace('Tiền Cần Thu Tuần W38', 'Tiền Cần Thu Tuần W39')

# 14. Tab 15: Kinh doanh
html = html.replace(
    '• <strong>Doanh Thu Toàn Vùng W38 (14–20/9):</strong> Đạt <strong>1,168.2 triệu VNĐ</strong>',
    '• <strong>Doanh Thu Toàn Vùng W39 (21–27/9):</strong> Đạt <strong>1,245.8 triệu VNĐ</strong>'
)
html = html.replace(
    '<div class="kpi-tile-header" id="kd-kpi-rev-header">Tổng Doanh Thu Kỳ Này (W38)</div>',
    '<div class="kpi-tile-header" id="kd-kpi-rev-header">Tổng Doanh Thu Kỳ Này (W39)</div>'
)
html = html.replace(
    '<th class="num" style="background: #ef4444; color:#ffffff; font-weight:800;">Kỳ Này (W38)</th>',
    '<th class="num" style="background: #ef4444; color:#ffffff; font-weight:800;">Kỳ Này (W39)</th>'
)

# 15. Single column replacements for tables
for col_name in ['Full', 'TTS', '%GTC', '%ODR', '%LTC', '%OPR', '% Rớt', 'FD']:
    html = html.replace(f'{col_name} W38</th>', f'{col_name} W39</th>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Comprehensive banner and table header updates applied successfully to index.html!")
