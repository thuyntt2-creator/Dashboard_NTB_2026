import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Tab 4 GTC Ca 1 TTS
old_t4_banner = '''            <h3>PHÂN TÍCH CHUYÊN SÂU %GTC CA 1 TIKTOK SHOP (TARGET SLA ≥ 76.0%)</h3>
            <p>
              • <strong>Toàn Vùng TTS Ca 1:</strong> Đạt <strong>75.8%</strong> (giảm nhẹ <strong>-0.2% WoW</strong> so với 76.0% W34). Có <strong>10/18 AM</strong> đạt chuẩn xanh SLA ≥76.0%.<br>
              • <strong>Top AM Dẫn Đầu Vùng:</strong> <strong>Nguyễn Ngọc Khánh (89.1%)</strong>, <strong>Nguyễn Duy Long (86.8%)</strong>, <strong>Nguyễn Lê Nguyên Vũ (86.0%)</strong>, <strong>Thái Thị Thanh Thư (85.5%)</strong>, <strong>Lê Thanh Nhựt (83.4%)</strong>, <strong>Cao Thị Thanh Thủy (82.2%)</strong>.<br>
              • <strong>Bứt Phá Tăng Trưởng Ca 1:</strong> <strong>Lê Minh Lợi</strong> tăng đột phá <strong>+27.3%</strong> (từ 16.3% lên <strong>43.7%</strong>); <strong>Nguyễn Thanh Long</strong> tăng <strong>+3.2%</strong> (lên <strong>64.0%</strong>); <strong>Trương Quang Linh</strong> tăng <strong>+2.8%</strong> (lên <strong>25.7%</strong>); <strong>Trần Thị Nhung</strong> tăng <strong>+2.3%</strong> (lên <strong>76.2%</strong> — đạt chuẩn xanh).<br>
              • <strong>Nhóm AM Cần Thúc Đẩy Ca 1:</strong> <strong>Lê Văn Trường (60.2% / giảm -6.8%)</strong>, <strong>Huỳnh Thúc Duân (62.3% / giảm -5.1%)</strong>, <strong>Trầm Hữu Tiến (47.2% / giảm -4.3%)</strong>.
            </p>'''

new_t4_banner = '''            <h3>PHÂN TÍCH CHUYÊN SÂU %GTC CA 1 TIKTOK SHOP (TARGET SLA ≥ 76.0%)</h3>
            <p>
              • <strong>Toàn Vùng TTS Ca 1:</strong> Đạt <strong>74.8%</strong> (giảm nhẹ <strong>-1.0% WoW</strong> so với 75.8% W35). Có <strong>7/18 AM</strong> đạt chuẩn xanh SLA ≥76.0%.<br>
              • <strong>Top AM Dẫn Đầu Vùng:</strong> <strong>Nguyễn Ngọc Khánh (86.6%)</strong>, <strong>Cao Thị Thanh Thủy (85.7%)</strong>, <strong>Nguyễn Thị Tuyết Thơ (84.7%)</strong>, <strong>Nguyễn Lê Nguyên Vũ (83.4%)</strong>, <strong>Nguyễn Duy Long (82.8%)</strong>, <strong>Lê Thanh Nhựt (82.7%)</strong>, <strong>Thái Thị Thanh Thư (82.2%)</strong>.<br>
              • <strong>Bứt Phá Tăng Trưởng Ca 1:</strong> <strong>Trương Quang Linh</strong> tăng mạnh nhất <strong>+9.8%</strong> (từ 25.7% lên <strong>35.5%</strong>); <strong>Nguyễn Thanh Long</strong> tăng <strong>+8.4%</strong> (lên <strong>72.4%</strong>); <strong>Cao Thị Thanh Thủy</strong> (+3.5%), <strong>Nguyễn Thị Tuyết Thơ</strong> (+3.5%), <strong>Lê Văn Trường</strong> (+2.8%).<br>
              • <strong>Nhóm AM Cần Thúc Đẩy Ca 1:</strong> <strong>Phan Đình Duy (75.8% / giảm -4.6%)</strong>, <strong>Nguyễn Duy Long (82.8% / giảm -4.0%)</strong>, <strong>Nguyễn Hoàng Phi (74.6% / giảm -3.4%)</strong>, <strong>Trần Thị Nhung (72.9% / giảm -3.3%)</strong>.
            </p>'''

assert old_t4_banner in content, 'old_t4_banner not found'
content = content.replace(old_t4_banner, new_t4_banner)

old_t4_th = '''                  <th class="num">%GTC TTS Ca 1 (W34)</th>
                  <th class="num" style="background: var(--color-amber-bg); font-weight:800; color:#c2410c;">%GTC TTS Ca 1 (W35)</th>'''

new_t4_th = '''                  <th class="num">%GTC TTS Ca 1 (W35)</th>
                  <th class="num" style="background: var(--color-amber-bg); font-weight:800; color:#c2410c;">%GTC TTS Ca 1 (W36)</th>'''

assert old_t4_th in content, 'old_t4_th not found'
content = content.replace(old_t4_th, new_t4_th)

# 2. Tab 5 Gan
old_t5_banner = '''            <h3>TỶ LỆ GÁN VẬN HÀNH TOÀN MẠNG THEO CA 1, CA 2 & GÁN TỔNG (TARGET ≥ 90.0%)</h3>
            <p>
              • <strong>Gán Tổng (Ca1+Ca2+Tồn):</strong> Full hàng đạt <strong>82.1%</strong> (+0.8% WoW); TTS đạt <strong>82.3%</strong> (+1.6% WoW so với 80.7% W34).<br>
              • <strong>Gán Ca 1 + Tồn:</strong> Full hàng đạt <strong>86.5%</strong> (+0.5% WoW); TTS đạt <strong>86.9%</strong> (+1.8% WoW so với 85.2% W34).<br>
              • <strong>Gán Ca 2:</strong> Full hàng đạt <strong>62.4%</strong> (+1.5% WoW); TTS đạt <strong>60.0%</strong> (+0.7% WoW so với 59.3% W34).<br>
              • <strong>Điểm nhấn 18 AM:</strong> Top Gán Tổng cao nhất: <strong>Thái Thị Thanh Thư (97.8%)</strong>, <strong>Nguyễn Duy Long (94.5%)</strong>, <strong>Nguyễn Ngọc Khánh (94.2%)</strong>. Cần thúc đẩy: <strong>Trương Quang Linh (9.7%)</strong>, <strong>Lê Minh Lợi (38.2%)</strong>, <strong>Trầm Hữu Tiến (71.9%)</strong>.
            </p>'''

new_t5_banner = '''            <h3>TỶ LỆ GÁN VẬN HÀNH TOÀN MẠNG THEO CA 1, CA 2 & GÁN TỔNG (TARGET ≥ 90.0%)</h3>
            <p>
              • <strong>Gán Tổng (Ca1+Ca2+Tồn):</strong> Full hàng đạt <strong>83.5%</strong> (+1.4% WoW); TTS đạt <strong>83.4%</strong> (+1.1% WoW so với 82.3% W35).<br>
              • <strong>Gán Ca 1 + Tồn:</strong> Full hàng đạt <strong>89.3%</strong> (+2.8% WoW); TTS đạt <strong>89.0%</strong> (+2.1% WoW so với 86.9% W35).<br>
              • <strong>Gán Ca 2:</strong> Full hàng đạt <strong>60.2%</strong> (-2.2% WoW); TTS đạt <strong>57.7%</strong> (-2.3% WoW so với 60.0% W35).<br>
              • <strong>Điểm nhấn 18 AM:</strong> Top Gán Tổng cao nhất: <strong>Thái Thị Thanh Thư (97.0%)</strong>, <strong>Nguyễn Thị Tuyết Thơ (94.7%)</strong>, <strong>Nguyễn Thanh Long (93.0%)</strong>, <strong>Phan Đình Duy (91.6%)</strong>, <strong>Nguyễn Duy Long (91.3%)</strong>, <strong>Nguyễn Ngọc Khánh (91.3%)</strong>, <strong>Cao Thị Thanh Thủy (90.4%)</strong>. Cần thúc đẩy: <strong>Trương Quang Linh (42.9%)</strong>, <strong>Trầm Hữu Tiến (63.0%)</strong>, <strong>Lê Văn Trường (69.7%)</strong>.
            </p>'''

assert old_t5_banner in content, 'old_t5_banner not found'
content = content.replace(old_t5_banner, new_t5_banner)

old_t5_chart = 'SO SÁNH TỶ LỆ GÁN 18 AM: % GÁN CA 1+TỒN vs % GÁN CA 2 vs % GÁN TỔNG (W35)'
new_t5_chart = 'SO SÁNH TỶ LỆ GÁN 18 AM: % GÁN CA 1+TỒN vs % GÁN CA 2 vs % GÁN TỔNG (W36)'
assert old_t5_chart in content, 'old_t5_chart not found'
content = content.replace(old_t5_chart, new_t5_chart)

# 3. Tab 9 Rot LC
old_t9_chart = '% RỚT LUÂN CHUYỂN THEO 18 AM PHỤ TRÁCH (W35)'
new_t9_chart = '% RỚT LUÂN CHUYỂN THEO 18 AM PHỤ TRÁCH (W36)'
assert old_t9_chart in content, 'old_t9_chart not found'
content = content.replace(old_t9_chart, new_t9_chart)

old_t9_th_am = '''                    <th class="num">% Rớt W34</th>
                    <th class="num" style="background: var(--color-red-bg); font-weight:800; color:#b91c1c;">% Rớt W35</th>'''
new_t9_th_am = '''                    <th class="num">% Rớt W35</th>
                    <th class="num" style="background: var(--color-red-bg); font-weight:800; color:#b91c1c;">% Rớt W36</th>'''

count_th = content.count(old_t9_th_am)
print(f'Found {count_th} occurrences of old_t9_th_am')
assert count_th >= 2, 'old_t9_th_am occurrences < 2'
content = content.replace(old_t9_th_am, new_t9_th_am)

old_t9_top20 = 'DANH SÁCH TOP 20 BƯU CỤC CÓ TỶ LỆ RỚT LUÂN CHUYỂN CAO NHẤT (W35)'
new_t9_top20 = 'DANH SÁCH TOP 20 BƯU CỤC CÓ TỶ LỆ RỚT LUÂN CHUYỂN CAO NHẤT (W36)'
assert old_t9_top20 in content, 'old_t9_top20 not found'
content = content.replace(old_t9_top20, new_t9_top20)

# 4. Tab 12 Truy Thu
old_tt_banner = '''            <h3>BÁO CÁO TRUY THU KHỐI LƯỢNG & TICKET VI PHẠM (OE-IA) | VÙNG NAM TRUNG BỘ</h3>
            <p id="truythu-banner-p">
              • <strong>Tổng quan toàn vùng:</strong> Tổng cộng <strong>8,892 bản ghi</strong> truy thu với số tiền ban đầu <strong>692.7 triệu VNĐ</strong> (Điều chỉnh: -19.5 triệu ➔ Cần truy thu thêm: <strong>673.2 triệu VNĐ</strong>).<br>
              • <strong>Top AM nhiều Ticket:</strong> Anh Trần Văn Phước (1,706 ticket | 200.4 Tr), anh Lê Minh Đại (644 ticket | 20.9 Tr), anh Lê Văn Trường (343 ticket | 27.0 Tr).<br>
              • <strong>Top BC Giao cần thu thêm:</strong> (DNO) Kiến Đức (134.2 Tr - 19.9%), (LDO) Tân Hà Lâm Hà (81.1 Tr - 11.7%), (DNO) Quảng Tín (60.5 Tr - 9.4%).
            </p>'''

new_tt_banner = '''            <h3>BÁO CÁO TRUY THU KHỐI LƯỢNG & TICKET VI PHẠM (OE-IA) | VÙNG NAM TRUNG BỘ</h3>
            <p id="truythu-banner-p">
              • <strong>Tổng quan toàn vùng W36:</strong> Tổng cộng <strong>5,033 bản ghi</strong> truy thu với số tiền ban đầu <strong>510.1 triệu VNĐ</strong> (Điều chỉnh: -335.4 triệu ➔ Cần truy thu thêm: <strong>174.7 triệu VNĐ</strong>).<br>
              • <strong>Top AM nhiều Ticket:</strong> Anh Trần Văn Phước (1,342 ticket | 52.8 Tr), anh Lê Văn Trường (512 ticket | 31.4 Tr), anh Lê Thanh Nhựt (498 ticket | 22.1 Tr).<br>
              • <strong>Top BC Giao cần thu thêm:</strong> (DNO) Kiến Đức, (LDO) Tân Hà Lâm Hà, (DNO) Quảng Tín.
            </p>'''

assert old_tt_banner in content, 'old_tt_banner not found'
content = content.replace(old_tt_banner, new_tt_banner)

old_tt_badge = '''          <span id="truythu-banner-badge" class="badge-tag badge-tag-red" style="font-size: 12px; padding: 6px 12px;">
            8,892 Bản Ghi | Cần Thu 673.2 Tr
          </span>'''

new_tt_badge = '''          <span id="truythu-banner-badge" class="badge-tag badge-tag-red" style="font-size: 12px; padding: 6px 12px;">
            5,033 Bản Ghi | Cần Thu 174.7 Tr
          </span>'''

assert old_tt_badge in content, 'old_tt_badge not found'
content = content.replace(old_tt_badge, new_tt_badge)

old_tt_kpi = '''          <div class="kpi-tile-value" id="truythu-kpi-records">8,892 <small>đơn</small></div>
          <div class="kpi-tile-meta"><span class="diff-tag diff-neutral">Toàn bộ 5 tỉnh NTB</span></div>
        </div>
        <div class="kpi-tile kpi-amber">
          <div class="kpi-tile-header">Tổng Tiền Ban Đầu</div>
          <div class="kpi-tile-value" id="truythu-kpi-bandau">692.7 <small>Tr ₫</small></div>
          <div class="kpi-tile-meta"><span class="diff-tag diff-neutral">Giá trị trước điều chỉnh</span></div>
        </div>
        <div class="kpi-tile kpi-green">
          <div class="kpi-tile-header">Tổng Tiền Điều Chỉnh</div>
          <div class="kpi-tile-value" id="truythu-kpi-dieuchinh">-19.5 <small>Tr ₫</small></div>
          <div class="kpi-tile-meta"><span class="diff-tag diff-down-good">Đã khấu trừ điều chỉnh</span></div>
        </div>
        <div class="kpi-tile kpi-red">
          <div class="kpi-tile-header">Cần Truy Thu Thêm</div>
          <div class="kpi-tile-value" id="truythu-kpi-canthu">673.2 <small>Tr ₫</small></div>'''

new_tt_kpi = '''          <div class="kpi-tile-value" id="truythu-kpi-records">5,033 <small>đơn</small></div>
          <div class="kpi-tile-meta"><span class="diff-tag diff-neutral">Toàn bộ 5 tỉnh NTB</span></div>
        </div>
        <div class="kpi-tile kpi-amber">
          <div class="kpi-tile-header">Tổng Tiền Ban Đầu</div>
          <div class="kpi-tile-value" id="truythu-kpi-bandau">510.1 <small>Tr ₫</small></div>
          <div class="kpi-tile-meta"><span class="diff-tag diff-neutral">Giá trị trước điều chỉnh</span></div>
        </div>
        <div class="kpi-tile kpi-green">
          <div class="kpi-tile-header">Tổng Tiền Điều Chỉnh</div>
          <div class="kpi-tile-value" id="truythu-kpi-dieuchinh">-335.4 <small>Tr ₫</small></div>
          <div class="kpi-tile-meta"><span class="diff-tag diff-down-good">Đã khấu trừ điều chỉnh</span></div>
        </div>
        <div class="kpi-tile kpi-red">
          <div class="kpi-tile-header">Cần Truy Thu Thêm</div>
          <div class="kpi-tile-value" id="truythu-kpi-canthu">174.7 <small>Tr ₫</small></div>'''

assert old_tt_kpi in content, 'old_tt_kpi not found'
content = content.replace(old_tt_kpi, new_tt_kpi)

# 5. Tab 13 Commercial
old_kd_banner = '''            <h3>PHÂN TÍCH DOANH THU KINH DOANH & TĂNG TRƯỞNG KHÁCH HÀNG MỚI (F30) | VÙNG NAM TRUNG BỘ</h3>
            <p>
              • <strong>Tăng trưởng Doanh Thu:</strong> Toàn vùng đạt <strong>1,073.3 triệu VNĐ</strong> (Kỳ trước: 1,048.9 triệu ➔ Tăng <strong>+24.4 triệu VNĐ / +2.3%</strong>).<br>
              • <strong>Top AM Doanh Thu Lớn Nhất:</strong> Anh Phan Đình Duy (495.0 Tr - 46.1%), anh Nguyễn Duy Long (98.1 Tr - 9.1%), chị Thái Thị Thanh Thư (92.2 Tr - 8.6%).<br>
              • <strong>Khách Hàng Mới (F30):</strong> Tổng cộng <strong>108 shop mới</strong> hoạt động (Kỳ trước: 82 shop ➔ Tăng <strong>+26 shop / +31.7%</strong>). Top phát triển KH mới: Nguyễn Duy Long (+9 shop), Thái Thị Thanh Thư (+7 shop), Trần Thị Nhung (+6 shop).
            </p>
          </div>
        </div>
        <div class="exec-banner-actions">
          <span class="badge-tag badge-tag-green" style="font-size: 12px; padding: 6px 12px;">
            Doanh Thu: 1,073.3 Tr (+2.3%) | 108 Shop F30
          </span>
        </div>'''

new_kd_banner = '''            <h3>PHÂN TÍCH DOANH THU KINH DOANH & TĂNG TRƯỞNG KHÁCH HÀNG MỚI (F30) | VÙNG NAM TRUNG BỘ</h3>
            <p>
              • <strong>Doanh Thu Toàn Vùng W36 (30/8–5/9):</strong> Đạt <strong>947.4 triệu VNĐ</strong> (Kỳ 23–29/8: 1,073.2 triệu ➔ Giảm <strong>-125.8 triệu VNĐ / -11.7%</strong>).<br>
              • <strong>Top AM Doanh Thu Lớn Nhất:</strong> Anh Phan Đình Duy (421.9 Tr - 44.5%), chị Thái Thị Thanh Thư (105.0 Tr - 11.1%), anh Nguyễn Duy Long (85.6 Tr - 9.0%), anh Nguyễn Lê Nguyên Vũ (47.7 Tr - 5.0%).<br>
              • <strong>Khách Hàng Mới (F30):</strong> Đạt <strong>93 shop mới</strong> (Kỳ trước: 95 shop ➔ Giảm <strong>-2 shop / -2.1%</strong> | Doanh thu F30: <strong>6.2 triệu ₫</strong>). Top KH mới: Thái Thị Thanh Thư (18 shop), Phan Đình Duy (16 shop), Nguyễn Duy Long (14 shop).
            </p>
          </div>
        </div>
        <div class="exec-banner-actions">
          <span class="badge-tag badge-tag-green" style="font-size: 12px; padding: 6px 12px;">
            Doanh Thu: 947.4 Tr (-11.7%) | 93 Shop F30
          </span>
        </div>'''

assert old_kd_banner in content, 'old_kd_banner not found'
content = content.replace(old_kd_banner, new_kd_banner)

old_kd_kpi = '''        <div class="kpi-tile kpi-green">
          <div class="kpi-tile-header">Tổng Doanh Thu Kỳ Này</div>
          <div class="kpi-tile-value">1,073.3 <small>Tr ₫</small></div>
          <div class="kpi-tile-meta"><span class="diff-tag diff-up-good">▲ +24.4 Tr (+2.3%)</span></div>
        </div>
        <div class="kpi-tile kpi-blue">
          <div class="kpi-tile-header">Tổng Sản Lượng Giao</div>
          <div class="kpi-tile-value">38,400 <small>đơn</small></div>
          <div class="kpi-tile-meta"><span class="diff-tag diff-up-good">▲ +480 đơn</span></div>
        </div>
        <div class="kpi-tile kpi-purple">
          <div class="kpi-tile-header">Khách Hàng Mới (F30)</div>
          <div class="kpi-tile-value">108 <small>Shop</small></div>
          <div class="kpi-tile-meta"><span class="diff-tag diff-up-good">▲ +26 shop (+31.7%)</span></div>
        </div>
        <div class="kpi-tile kpi-amber">
          <div class="kpi-tile-header">Doanh Thu Shop Mới F30</div>
          <div class="kpi-tile-value">13.5 <small>Tr ₫</small></div>
          <div class="kpi-tile-meta"><span class="diff-tag diff-up-good">▲ +2.7 Tr (+25.0%)</span></div>
        </div>'''

new_kd_kpi = '''        <div class="kpi-tile kpi-green">
          <div class="kpi-tile-header">Tổng Doanh Thu Kỳ Này (W36)</div>
          <div class="kpi-tile-value">947.4 <small>Tr ₫</small></div>
          <div class="kpi-tile-meta"><span class="diff-tag diff-down-bad">▼ -125.8 Tr (-11.7%)</span></div>
        </div>
        <div class="kpi-tile kpi-blue">
          <div class="kpi-tile-header">Tổng Volume Giao</div>
          <div class="kpi-tile-value">30,132 <small>đơn</small></div>
          <div class="kpi-tile-meta"><span class="diff-tag diff-down-bad">▼ -2,607 đơn (-8.0%)</span></div>
        </div>
        <div class="kpi-tile kpi-purple">
          <div class="kpi-tile-header">Khách Hàng Mới (F30)</div>
          <div class="kpi-tile-value">93 <small>Shop</small></div>
          <div class="kpi-tile-meta"><span class="diff-tag diff-down-bad">▼ -2 shop (-2.1%)</span></div>
        </div>
        <div class="kpi-tile kpi-amber">
          <div class="kpi-tile-header">Doanh Thu Shop Mới F30</div>
          <div class="kpi-tile-value">6.2 <small>Tr ₫</small></div>
          <div class="kpi-tile-meta"><span class="diff-tag diff-down-bad">▼ -15.6 Tr (-71.6%)</span></div>
        </div>'''

assert old_kd_kpi in content, 'old_kd_kpi not found'
content = content.replace(old_kd_kpi, new_kd_kpi)

old_kd_chart_sub = '<span class="badge-tag badge-tag-blue">Kỳ 16–22/8 vs Kỳ 23–29/8</span>'
new_kd_chart_sub = '<span class="badge-tag badge-tag-blue">Kỳ 23–29/8 (W35) vs Kỳ 30/8–5/9 (W36)</span>'
assert old_kd_chart_sub in content, 'old_kd_chart_sub not found'
content = content.replace(old_kd_chart_sub, new_kd_chart_sub)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ index.html updated successfully with all W36 banners, headers, and KPI tiles!')
