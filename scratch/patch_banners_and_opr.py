import re, sys
sys.stdout.reconfigure(encoding='utf-8')

# ==============================================================================
# PART 1: UPDATE ALL BLACK EXECUTIVE BANNERS IN index.html
# ==============================================================================
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. BANNER 2: SẢN LƯỢNG (Tab 2: tab-volume)
old_banner_2 = """          <div class="exec-banner-text">
            <h3 id="banner-volume-title">PHÂN TÍCH SẢN LƯỢNG GIAO TOÀN VÙNG, 5 TỈNH THÀNH & 18 AM</h3>
            <p id="banner-volume-summary">
              • <strong>Sản lượng Toàn Mạng (W37):</strong> Full hàng đạt <strong>357,249 đơn</strong> (tăng <strong>+49,412 đơn / +16.1% WoW</strong> so với W36). Phân khúc TikTok Shop (TTS) đạt <strong>68,719 đơn</strong> (tăng <strong>+5,597 đơn / +8.9% WoW</strong>), chiếm tỷ trọng <strong>19.2%</strong> tổng sản lượng vùng.<br>
              • <strong>Theo 5 Tỉnh:</strong> Cả 5 tỉnh đều tăng trưởng sản lượng tuần W37 — Bình Thuận (107.5k đơn), Khánh Hòa (89.1k đơn), Lâm Đồng (92.5k đơn), Ninh Thuận (42.4k đơn), Đắk Nông (25.7k đơn).<br>
              • <strong>Biến động AM:</strong> AM Thái Thị Thanh Thư dẫn đầu tăng trưởng (+6,990 đơn Full), tiếp theo là Nguyễn Duy Long (+6,938 đơn), Lê Văn Trường (+5,814 đơn).
            </p>
          </div>
        </div>
        <div class="exec-banner-actions">
          <span class="badge-tag badge-tag-blue" id="banner-volume-badge" style="font-size: 12px; padding: 6px 12px;">
            Full: 357.2k đơn | TTS: 68.7k đơn
          </span>"""

new_banner_2 = """          <div class="exec-banner-text">
            <h3 id="banner-volume-title">PHÂN TÍCH SẢN LƯỢNG GIAO TOÀN VÙNG, 5 TỈNH THÀNH & 18 AM (W38)</h3>
            <p id="banner-volume-summary">
              • <strong>Sản lượng Toàn Mạng (W38):</strong> Full hàng đạt <strong>345,994 đơn</strong> (giảm <strong>-11,255 đơn / -3.15% WoW</strong> so với W37: 357,249 đơn). Phân khúc TikTok Shop (TTS) đạt <strong>69,274 đơn</strong> (tăng <strong>+555 đơn / +0.81% WoW</strong> so với W37: 68,719 đơn), chiếm tỷ trọng <strong>20.0%</strong> tổng sản lượng vùng.<br>
              • <strong>Theo 5 Tỉnh:</strong> Khánh Hòa dẫn đầu quy mô đạt <strong>96,012 đơn</strong> (TTS: 18,142 đơn), Lâm Đồng thứ 2 đạt <strong>95,727 đơn</strong> (TTS: 19,587 đơn), Bình Thuận đạt <strong>85,489 đơn</strong> (TTS: 15,873 đơn), Đắk Nông đạt <strong>34,848 đơn</strong> (TTS: 8,314 đơn), Ninh Thuận đạt <strong>33,918 đơn</strong> (TTS: 7,358 đơn).<br>
              • <strong>Biến động AM:</strong> AM Nguyễn Hoàng Phi dẫn đầu tăng trưởng (+3,210 đơn Full), tiếp theo là Cao Thị Thanh Thủy (+2,828 đơn), Huỳnh Thị Kim Chi (+1,452 đơn).
            </p>
          </div>
        </div>
        <div class="exec-banner-actions">
          <span class="badge-tag badge-tag-blue" id="banner-volume-badge" style="font-size: 12px; padding: 6px 12px;">
            Full: 346.0k đơn | TTS: 69.3k đơn
          </span>"""

assert old_banner_2 in html, "Banner 2 not found in index.html"
html = html.replace(old_banner_2, new_banner_2, 1)

# 2. BANNER 3: %GTC TỔNG (Tab 3: tab-gtc-tong)
old_banner_3 = """          <div class="exec-banner-text">
            <h3>PHÂN TÍCH HIỆU SUẤT %GTC TỔNG TOÀN MẠNG THEO 18 AM & 5 TỈNH</h3>
            <p id="gtc-tong-banner-summary">
              • <strong>%GTC Tổng Toàn Vùng:</strong> Full hàng đạt <strong>57.78%</strong> (-0.36% WoW); Phân khúc TTS đạt <strong>55.91%</strong> (-1.04% WoW).<br>
              • <strong>Top AM dẫn đầu:</strong> <strong>Nguyễn Ngọc Khánh (74.9%)</strong>, <strong>Cao Thị Thanh Thủy (68.7%)</strong>, <strong>Nguyễn Thị Tuyết Thơ (68.4%)</strong>, <strong>Nguyễn Duy Long (67.8%)</strong>.<br>
              • <strong>Bứt phá tăng trưởng WoW:</strong> <strong>Huỳnh Thúc Duân</strong> tăng mạnh nhất +6.4% (lên 48.1%); <strong>Lê Minh Lợi</strong> tăng +4.2% (lên 37.0%); <strong>Nguyễn Ngọc Khánh</strong> tăng +3.2% (lên 74.9%); <strong>Trương Quang Linh</strong> tăng +3.1% (lên 18.4%).<br>
              • <strong>Nhóm AM cần cải thiện GTC:</strong> <strong>Trương Quang Linh (18.4%)</strong>, <strong>Trầm Hữu Tiến (30.0%)</strong>, <strong>Lê Minh Lợi (37.0%)</strong>, <strong>Nguyễn Thanh Long (46.9%)</strong>, <strong>Lê Văn Trường (47.8%)</strong>.
            </p>
          </div>
        </div>
        <div class="exec-banner-actions">
          <span class="badge-tag badge-tag-blue" style="font-size: 12px; padding: 6px 12px;">
            Target %GTC Tổng ≥ 60.0%
          </span>"""

new_banner_3 = """          <div class="exec-banner-text">
            <h3>PHÂN TÍCH HIỆU SUẤT %GTC TỔNG TOÀN MẠNG THEO 18 AM & 5 TỈNH (W38)</h3>
            <p id="gtc-tong-banner-summary">
              • <strong>%GTC Tổng Toàn Vùng (W38):</strong> Full hàng đạt <strong>55.75%</strong> (-2.02%p WoW so với W37: 57.78%); Phân khúc TTS đạt <strong>54.01%</strong> (-1.90%p WoW so với W37: 55.91%).<br>
              • <strong>Top AM dẫn đầu:</strong> <strong>Nguyễn Ngọc Khánh (73.2%)</strong>, <strong>Cao Thị Thanh Thủy (70.1%)</strong>, <strong>Nguyễn Duy Long (67.8%)</strong>, <strong>Nguyễn Thị Tuyết Thơ (66.5%)</strong>.<br>
              • <strong>Bứt phá tăng trưởng WoW:</strong> <strong>Nguyễn Hoàng Phi</strong> tăng mạnh nhất +5.3%p (lên 76.8%); <strong>Cao Thị Thanh Thủy</strong> tăng +2.7%p (lên 84.5%); <strong>Nguyễn Ngọc Khánh</strong> tăng +1.0%p (lên 87.5%).<br>
              • <strong>Nhóm AM suy giảm cần thúc đẩy xả tồn:</strong> <strong>Nguyễn Thanh Long (42.5% / giảm -16.8%p)</strong>, <strong>Phan Đình Duy (59.1% / giảm -8.5%p)</strong>, <strong>Lê Văn Trường (52.9% / giảm -8.5%p)</strong>, <strong>Lê Minh Lợi (41.4% / giảm -7.3%p)</strong>.
            </p>
          </div>
        </div>
        <div class="exec-banner-actions">
          <span class="badge-tag badge-tag-blue" style="font-size: 12px; padding: 6px 12px;">
            Full: 55.75% | TTS: 54.01% (Target ≥ 60.0%)
          </span>"""

assert old_banner_3 in html, "Banner 3 not found in index.html"
html = html.replace(old_banner_3, new_banner_3, 1)

# 3. BANNER 4: %GTC CA 1 TTS (Tab 4: tab-gtc-tts-ca1)
old_banner_4 = """          <div class="exec-banner-text">
            <h3>PHÂN TÍCH CHUYÊN SÂU %GTC CA 1 TIKTOK SHOP (TARGET SLA ≥ 76.0%)</h3>
            <p id="banner-gtc-ca1-summary">
              • <strong>Toàn Vùng TTS Ca 1:</strong> Đạt <strong>73.07%</strong> (giảm <strong>-1.71%p WoW</strong> so với 74.78% W36). Có <strong>7/18 AM</strong> đạt chuẩn xanh SLA ≥76.0%.<br>
              • <strong>Top AM Dẫn Đầu Vùng (≥76%):</strong> <strong>Nguyễn Ngọc Khánh (86.5%)</strong>, <strong>Nguyễn Lê Nguyên Vũ (83.8%)</strong>, <strong>Nguyễn Duy Long (82.5%)</strong>, <strong>Cao Thị Thanh Thủy (81.8%)</strong>, <strong>Nguyễn Thị Tuyết Thơ (81.5%)</strong>, <strong>Lê Thanh Nhựt (80.8%)</strong>, <strong>Thái Thị Thanh Thư (80.0%)</strong>.<br>
              • <strong>Bứt Phá Tăng Trưởng Ca 1:</strong> <strong>Trương Quang Linh</strong> tăng mạnh nhất <strong>+11.4%p</strong> (từ 32.6% lên <strong>43.9%</strong>); <strong>Huỳnh Thúc Duân</strong> tăng <strong>+7.3%p</strong> (lên <strong>62.1%</strong>); <strong>Lê Minh Lợi</strong> (+4.6%p lên <strong>49.5%</strong>).<br>
              • <strong>Nhóm AM Cần Thúc Đẩy Ca 1:</strong> <strong>Nguyễn Thanh Long (57.8% / giảm sâu -12.9%p)</strong>, <strong>Phan Đình Duy (65.2% / giảm -7.3%p)</strong>, <strong>Lê Văn Trường (59.8% / giảm -4.3%p)</strong>, <strong>Trầm Hữu Tiến (41.0% / giảm -2.4%p)</strong>.
            </p>
          </div>
        </div>
        <div class="exec-banner-actions">
          <span class="badge-tag badge-tag-amber" style="font-size: 12px; padding: 6px 12px;">
            Target Chuẩn Xanh ≥ 76.0%
          </span>"""

new_banner_4 = """          <div class="exec-banner-text">
            <h3>PHÂN TÍCH CHUYÊN SÂU %GTC CA 1 TIKTOK SHOP (TARGET SLA ≥ 76.0%) (W38)</h3>
            <p id="banner-gtc-ca1-summary">
              • <strong>Toàn Vùng TTS Ca 1 (W38):</strong> Đạt <strong>71.36%</strong> (giảm <strong>-1.71%p WoW</strong> so với 73.07% W37). Có <strong>6/18 AM</strong> đạt chuẩn xanh SLA ≥76.0%.<br>
              • <strong>Top AM Dẫn Đầu Vùng (≥76%):</strong> <strong>Nguyễn Ngọc Khánh (89.5%)</strong>, <strong>Cao Thị Thanh Thủy (86.1%)</strong>, <strong>Nguyễn Duy Long (83.1%)</strong>, <strong>Nguyễn Đỗ Minh Nghĩa (83.0%)</strong>, <strong>Thái Thị Thanh Thư (82.1%)</strong>, <strong>Lê Thanh Nhựt (81.5%)</strong>.<br>
              • <strong>Bứt Phá Tăng Trưởng Ca 1:</strong> <strong>Nguyễn Hoàng Phi</strong> tăng mạnh nhất <strong>+4.3%p</strong> (lên <strong>78.4%</strong>); <strong>Cao Thị Thanh Thủy</strong> tăng <strong>+3.0%p</strong> (lên <strong>86.1%</strong>); <strong>Nguyễn Ngọc Khánh</strong> tăng <strong>+2.1%p</strong> (lên <strong>89.5%</strong>).<br>
              • <strong>Nhóm AM Cần Thúc Đẩy Ca 1:</strong> <strong>Nguyễn Thanh Long (42.5% / giảm sâu -16.8%p)</strong>, <strong>Phan Đình Duy (59.1% / giảm -8.5%p)</strong>, <strong>Lê Văn Trường (52.9% / giảm -8.5%p)</strong>, <strong>Lê Minh Lợi (41.4% / giảm -7.3%p)</strong>, <strong>Trương Quang Linh (42.6% / giảm -4.6%p)</strong>.
            </p>
          </div>
        </div>
        <div class="exec-banner-actions">
          <span class="badge-tag badge-tag-amber" style="font-size: 12px; padding: 6px 12px;">
            Target ≥ 76.0% (W38: 71.36%)
          </span>"""

assert old_banner_4 in html, "Banner 4 not found in index.html"
html = html.replace(old_banner_4, new_banner_4, 1)

# 4. BANNER 5: %GÁN (Tab 5: tab-gan)
old_banner_5 = """          <div class="exec-banner-text">
            <h3>TỶ LỆ GÁN VẬN HÀNH TOÀN MẠNG THEO CA 1, CA 2 & GÁN TỔNG (TARGET ≥ 90.0%)</h3>
            <p>
              • <strong>Gán Tổng (Ca1+Ca2+Tồn):</strong> Full hàng đạt <strong>82.8%</strong> (-0.7%p WoW); TTS đạt <strong>82.4%</strong> (-1.0%p WoW so với 83.4% W36).<br>
              • <strong>Gán Ca 1 + Tồn:</strong> Full hàng đạt <strong>89.0%</strong> (-0.3%p WoW); TTS đạt <strong>88.4%</strong> (-0.6%p WoW so với 89.0% W36).<br>
              • <strong>Gán Ca 2:</strong> Full hàng đạt <strong>55.7%</strong> (-4.5%p WoW); TTS đạt <strong>51.9%</strong> (-5.8%p WoW so với 57.7% W36).<br>
              • <strong>Điểm nhấn 18 AM:</strong> Top Gán Tổng cao nhất: <strong>Nguyễn Thị Tuyết Thơ (95.3%)</strong>, <strong>Thái Thị Thanh Thư (94.2%)</strong>, <strong>Nguyễn Ngọc Khánh (93.6%)</strong>, <strong>Nguyễn Duy Long (91.0%)</strong>, <strong>Cao Thị Thanh Thủy (90.7%)</strong>. Cần thúc đẩy: <strong>Trương Quang Linh (38.2%)</strong>, <strong>Trầm Hữu Tiến (59.9%)</strong>, <strong>Lê Văn Trường (68.3%)</strong>.
            </p>
          </div>
        </div>
        <div class="exec-banner-actions">
          <span class="badge-tag badge-tag-purple" style="font-size: 12px; padding: 6px 12px;">
            Target Gán Tổng ≥ 90.0%
          </span>"""

new_banner_5 = """          <div class="exec-banner-text">
            <h3>TỶ LỆ GÁN VẬN HÀNH TOÀN MẠNG THEO CA 1, CA 2 & GÁN TỔNG (TARGET ≥ 90.0%) (W38)</h3>
            <p>
              • <strong>Gán Tổng (Ca1+Ca2+Tồn W38):</strong> Full hàng đạt <strong>80.6%</strong> (-2.2%p WoW so với 82.8% W37); TTS đạt <strong>80.2%</strong> (-2.2%p WoW so với 82.4% W37).<br>
              • <strong>Gán Ca 1 + Tồn:</strong> Full hàng đạt <strong>85.9%</strong> (-3.1%p WoW so với 89.0% W37); TTS đạt <strong>85.5%</strong> (-2.9%p WoW so với 88.4% W37).<br>
              • <strong>Gán Ca 2:</strong> Full hàng đạt <strong>56.8%</strong> (+1.2%p WoW so với 55.7% W37); TTS đạt <strong>53.4%</strong> (+1.5%p WoW so với 51.9% W37).<br>
              • <strong>Điểm nhấn 18 AM:</strong> Top Gán Tổng cao nhất: <strong>Cao Thị Thanh Thủy (93.0%)</strong>, <strong>Nguyễn Duy Long (91.2%)</strong>, <strong>Nguyễn Ngọc Khánh (91.0%)</strong>, <strong>Thái Thị Thanh Thư (90.5%)</strong>. Cần thúc đẩy: <strong>Trương Quang Linh (41.5%)</strong>, <strong>Huỳnh Thúc Duân (72.5%)</strong>, <strong>Hồng Bích Nga (71.4%)</strong>.
            </p>
          </div>
        </div>
        <div class="exec-banner-actions">
          <span class="badge-tag badge-tag-purple" style="font-size: 12px; padding: 6px 12px;">
            Gán Tổng W38: 80.6% (Target ≥ 90.0%)
          </span>"""

assert old_banner_5 in html, "Banner 5 not found in index.html"
html = html.replace(old_banner_5, new_banner_5, 1)

# 5. BANNER 6: %ODR (Tab 6: tab-odr)
old_banner_6 = """          <div class="exec-banner-text">
            <h3>PHÂN TÍCH HIỆU SUẤT %ODR (GIAO ĐÚNG HẸN SLA) TOÀN VÙNG (TARGET ≥ 92.0%)</h3>
            <p>
              • <strong>Toàn Vùng W37:</strong> Full Hàng đạt <strong>93.9%</strong> (+1.0%p WoW so với W36: 92.9%) và TTS đạt <strong>92.8%</strong> (+0.4%p WoW so với W36: 92.4%). Cả Full Hàng và TikTok Shop đều duy trì vững trên chuẩn xanh SLA ≥ 92.0%.<br>
              • <strong>Top AM Xuất Sắc:</strong> <strong>Thái Thị Thanh Thư (97.5%)</strong>, <strong>Nguyễn Ngọc Khánh (96.8%)</strong>, <strong>Cao Thị Thanh Thủy (96.7%)</strong>, <strong>Nguyễn Duy Long (96.7%)</strong>, <strong>Nguyễn Lê Nguyên Vũ (96.3%)</strong>.<br>
              • <strong>Điểm Nhấn Bứt Phá & Lưu Ý:</strong> <strong>Trương Quang Linh</strong> bứt phá ngoạn mục (<strong>+21.3%p</strong> lên <strong>81.7%</strong>); <strong>Trầm Hữu Tiến (71.5%)</strong>, <strong>Lê Minh Lợi (73.5%)</strong>, <strong>Lê Văn Trường (86.5%)</strong> cần tập trung xả tồn tránh trễ SLA.
            </p>
          </div>
        </div>
        <div class="exec-banner-actions">
          <span class="badge-tag badge-tag-green" style="font-size: 12px; padding: 6px 12px;">
            Target ODR ≥ 92.0%
          </span>"""

new_banner_6 = """          <div class="exec-banner-text">
            <h3>PHÂN TÍCH HIỆU SUẤT %ODR (GIAO ĐÚNG HẸN SLA) TOÀN VÙNG (TARGET ≥ 92.0%) (W38)</h3>
            <p>
              • <strong>Toàn Vùng W38:</strong> Full Hàng đạt <strong>91.24%</strong> (-2.10%p WoW so với W37: 93.34%) và TTS đạt <strong>91.54%</strong> (-1.31%p WoW so với W37: 92.85%).<br>
              • <strong>Theo 5 Tỉnh:</strong> Ninh Thuận (96.5%) và Bình Thuận (96.2%) tiếp tục dẫn đầu toàn vùng, bảo vệ vững chắc chuẩn xanh SLA ≥ 92%. Khánh Hòa đạt 94.6%. Cần cải thiện: Đắk Nông (90.5%), Lâm Đồng (90.2%).<br>
              • <strong>Top AM Xuất Sắc:</strong> <strong>Nguyễn Ngọc Khánh (96.8%)</strong>, <strong>Cao Thị Thanh Thủy (96.7%)</strong>, <strong>Thái Thị Thanh Thư (96.5%)</strong>, <strong>Nguyễn Duy Long (95.8%)</strong>. Cần đôn đốc xả tồn: <strong>Lê Văn Trường (84.2%)</strong>, <strong>Trầm Hữu Tiến (73.1%)</strong>.
            </p>
          </div>
        </div>
        <div class="exec-banner-actions">
          <span class="badge-tag badge-tag-green" style="font-size: 12px; padding: 6px 12px;">
            ODR Full: 91.2% | TTS: 91.5% (Target ≥ 92.0%)
          </span>"""

assert old_banner_6 in html, "Banner 6 not found in index.html"
html = html.replace(old_banner_6, new_banner_6, 1)

# 6. BANNER 7: %LTC (Tab 7: tab-ltc)
old_banner_7 = """          <div class="exec-banner-text">
            <h3>PHÂN TÍCH CHỈ SỐ %LTC (LẤY THÀNH CÔNG) THEO 18 AM & 5 TỈNH (TARGET ≥ 90.0%)</h3>
            <p>
              • <strong>Toàn Vùng:</strong> Đạt <strong>90.5%</strong>. Duy trì vượt chuẩn SLA ≥90.0%.<br>
              • <strong>Top AM Dẫn Đầu:</strong> <strong>Nguyễn Lê Nguyên Vũ (96.4%)</strong>, <strong>Phan Đình Duy (95.8%)</strong>.<br>
              • <strong>Bứt Phá Lấy Hàng:</strong> Nhiều AM giữ vững phong độ lấy hàng chuẩn giờ cam kết.
            </p>
          </div>
        </div>
        <div class="exec-banner-actions">
          <span class="badge-tag badge-tag-blue" style="font-size: 12px; padding: 6px 12px;">
            Target LTC ≥ 90.0%
          </span>"""

new_banner_7 = """          <div class="exec-banner-text">
            <h3>PHÂN TÍCH CHỈ SỐ %LTC (LẤY THÀNH CÔNG) THEO 18 AM & 5 TỈNH (TARGET ≥ 90.0%) (W38)</h3>
            <p>
              • <strong>Toàn Vùng W38:</strong> Full hàng đạt <strong>90.36%</strong> (+0.06%p WoW so với W37: 90.29%), TTS đạt <strong>95.43%</strong> (+1.88%p WoW so với W37: 93.55%). Cả Full hàng và TikTok Shop đều duy trì vững vượt chuẩn SLA ≥ 90.0%.<br>
              • <strong>Top AM Dẫn Đầu:</strong> <strong>Nguyễn Lê Nguyên Vũ (96.8%)</strong>, <strong>Phan Đình Duy (96.1%)</strong>, <strong>Nguyễn Duy Long (94.5%)</strong>.<br>
              • <strong>Bứt Phá Lấy Hàng:</strong> Tỷ lệ lấy thành công TTS tăng mạnh ở hầu hết các bưu cục trên địa bàn Khánh Hòa và Lâm Đồng.
            </p>
          </div>
        </div>
        <div class="exec-banner-actions">
          <span class="badge-tag badge-tag-blue" style="font-size: 12px; padding: 6px 12px;">
            Full: 90.4% | TTS: 95.4% (Target ≥ 90.0%)
          </span>"""

assert old_banner_7 in html, "Banner 7 not found in index.html"
html = html.replace(old_banner_7, new_banner_7, 1)

# 7. BANNER 8: %OPR TIKTOK SHOP (Tab 8: tab-opr-tts)
old_banner_8 = """          <div class="exec-banner-text">
            <h3>PHÂN TÍCH CHỈ SỐ %OPR TIKTOK SHOP TOÀN VÙNG (TARGET KPI ≥ 80.0%)</h3>
            <p>
              • <strong>Toàn Vùng (Tổng):</strong> Đạt <strong>78.1%</strong> (+1.2%p WoW so với W36: 76.9%) — Tiệm cận sát mục tiêu KPI ≥ 80.0% (chỉ còn cách -1.9%p).<br>
              • <strong>Top AM Chưa Đạt KPI gây rớt đơn OPR nhiều nhất:</strong> <strong>Hồng Bích Nga (65.1% / rớt 297 đơn - 15.5%)</strong>, <strong>Nguyễn Hoàng Phi (51.2% / rớt 236 đơn - 12.3%)</strong>, <strong>Lê Văn Trường (42.2% / rớt 193 đơn - 10.0%)</strong>, <strong>Nguyễn Thị Tuyết Thơ (69.0% / rớt 144 đơn - 7.5%)</strong>, <strong>Lê Thanh Nhựt (79.2% / rớt 142 đơn - 7.4%)</strong>, <strong>Trần Thị Nhung (34.3% / rớt 92 đơn - 4.8%)</strong>.<br>
              • <strong>Nhóm Đạt KPI Vững Chắc (≥80.0%):</strong> <strong>Nguyễn Lê Nguyên Vũ (89.6%)</strong>, <strong>Cao Thị Thanh Thủy (88.4%)</strong>, <strong>Thái Thị Thanh Thư (88.3% — bứt phá ngoạn mục +13.6%p)</strong>, <strong>Nguyễn Duy Long (87.5%)</strong>, <strong>Nguyễn Ngọc Khánh (85.0%)</strong>, <strong>Huỳnh Thị Kim Chi (80.0%)</strong>.<br>
              • <strong>Khung Giờ Ngày vs Đêm:</strong> Ca Ngày (9h–19h) đạt <strong>87.8%</strong> (3.944/4.492 đơn đạt); Ca Đêm (19h–9h) đạt <strong>67.9%</strong> (tăng vọt <strong>+6.5%p WoW</strong> so với 61.4% W36; số đơn trễ giảm xuống còn 1.373 đơn).
            </p>
          </div>
        </div>
        <div class="exec-banner-actions">
          <span class="badge-tag badge-tag-red" style="font-size: 12px; padding: 6px 12px; font-weight:800;">
            Target OPR KPI ≥ 80.0%
          </span>"""

new_banner_8 = """          <div class="exec-banner-text">
            <h3>PHÂN TÍCH CHỈ SỐ %OPR TIKTOK SHOP TOÀN VÙNG (TARGET KPI ≥ 80.0%) (W38)</h3>
            <p>
              • <strong>Toàn Vùng W38 (Tổng Ngày + Đêm):</strong> Đạt <strong>83.02%</strong> (+7.22%p WoW so với 75.81% W37) — <strong>CHÍNH THỨC VƯỢT CHUẨN KPI ≥ 80.0%</strong>.<br>
              • <strong>Khung Giờ Ngày vs Đêm:</strong> Ca Ngày (9h–19h) đạt <strong>90.26%</strong> (3,631/4,023 đơn đạt); Ca Đêm (19h–9h) bứt phá ngoạn mục đạt <strong>71.45%</strong> (tăng vọt <strong>+9.76%p WoW</strong> so với 61.69% W37; số đơn trễ giảm xuống còn 717 đơn).<br>
              • <strong>Top AM Đạt KPI Xuất Sắc (≥80.0%):</strong> <strong>Thái Thị Thanh Thư (93.0%)</strong>, <strong>Cao Thị Thanh Thủy (91.4%)</strong>, <strong>Nguyễn Duy Long (90.6%)</strong>, <strong>Nguyễn Ngọc Khánh (89.5%)</strong>, <strong>Huỳnh Thị Kim Chi (88.5%)</strong>, <strong>Lê Thanh Nhựt (87.2%)</strong>.<br>
              • <strong>Top AM Chưa Đạt KPI gây trễ đơn OPR:</strong> <strong>Lê Văn Trường (54.9% / trễ 207 đơn)</strong>, <strong>Nguyễn Thị Tuyết Thơ (55.5% / trễ 122 đơn)</strong>, <strong>Trần Thị Nhung (37.9% / trễ 108 đơn)</strong>, <strong>Nguyễn Đỗ Minh Nghĩa (78.7% / trễ 35 đơn)</strong>, <strong>Huỳnh Thúc Duân (64.2% / trễ 29 đơn)</strong>.
            </p>
          </div>
        </div>
        <div class="exec-banner-actions">
          <span class="badge-tag badge-tag-green" style="font-size: 12px; padding: 6px 12px; font-weight:800;">
            OPR TTS W38: 83.0% (Đạt KPI ≥ 80.0%)
          </span>"""

assert old_banner_8 in html, "Banner 8 not found in index.html"
html = html.replace(old_banner_8, new_banner_8, 1)

# 8. BANNER 9: RỚT LUÂN CHUYỂN (Tab 9: tab-rot-lc)
old_banner_9 = """          <div class="exec-banner-text">
            <h3>PHÂN TÍCH TỶ TRỌNG RỚT ĐƠN LUÂN CHUYỂN THEO AM & TỈNH THÀNH (W38)</h3>
            <p>
              • <strong>Tổng đơn rớt toàn vùng W37:</strong> Tỷ lệ rớt đạt <strong>1.80%</strong> (giảm <strong>-0.45% WoW</strong> so với 2.25% W36, xu hướng cải thiện tích cực).<br>
              • <strong>Top 4 AM chiếm 77.0% lượng rớt toàn vùng:</strong> <strong>Hồng Bích Nga (63 đơn - 32.1%)</strong>, <strong>Nguyễn Duy Long (35 đơn - 17.9%)</strong>, <strong>Trần Thị Nhung (31 đơn - 15.8%)</strong>, <strong>Huỳnh Thúc Duân (22 đơn - 11.2%)</strong>. Riêng 4 AM này đã chiếm tới 151 / 196 đơn rớt của cả Vùng NTB.<br>
              • <strong>Theo Tỉnh thành:</strong> <strong>Lâm Đồng</strong> chiếm <strong>40.8%</strong> (80 đơn) và <strong>Đắk Nông</strong> chiếm <strong>28.6%</strong> (56 đơn) tổng đơn rớt toàn vùng.
            </p>
          </div>
        </div>
        <div class="exec-banner-actions">
          <span class="badge-tag badge-tag-red" style="font-size: 12px; padding: 6px 12px;">
            Tổng rớt: 252 đơn
          </span>"""

new_banner_9 = """          <div class="exec-banner-text">
            <h3>PHÂN TÍCH TỶ TRỌNG RỚT ĐƠN LUÂN CHUYỂN THEO AM & TỈNH THÀNH (W38)</h3>
            <p>
              • <strong>Tổng đơn rớt toàn vùng W38:</strong> Tỷ lệ rớt đạt <strong>3.32%</strong> (tăng <strong>+1.52%p WoW</strong> so với 1.80% ở W37, tổng <strong>252 đơn rớt</strong> trên 7,586 đơn cần luân chuyển).<br>
              • <strong>Top 5 AM rớt nhiều nhất (chiếm 71.8% lượng rớt):</strong> <strong>Thái Thị Thanh Thư (79 đơn - 7.13%)</strong>, <strong>Trần Thị Nhung (33 đơn - 19.76%)</strong>, <strong>Hồng Bích Nga (27 đơn - 4.49%)</strong>, <strong>Huỳnh Thúc Duân (21 đơn - 20.79%)</strong>, <strong>Lê Văn Trường (21 đơn - 4.24%)</strong>.<br>
              • <strong>Theo Tỉnh thành:</strong> <strong>Khánh Hòa</strong> chiếm <strong>102 đơn (5.09%)</strong>, <strong>Lâm Đồng</strong> 58 đơn (3.32%), <strong>Đắk Nông</strong> 57 đơn (20.73%), <strong>Bình Thuận</strong> 19 đơn (0.88%), <strong>Ninh Thuận</strong> 16 đơn (1.14%).
            </p>
          </div>
        </div>
        <div class="exec-banner-actions">
          <span class="badge-tag badge-tag-red" style="font-size: 12px; padding: 6px 12px;">
            Tổng rớt W38: 252 đơn (3.32%)
          </span>"""

assert old_banner_9 in html, "Banner 9 not found in index.html"
html = html.replace(old_banner_9, new_banner_9, 1)

# 9. BANNER 10: %FD (Tab 10: tab-fd)
html = html.replace(
    'BÁO CÁO TỶ LỆ %FD (RETURN / HOÀN TRẢ) — VÙNG NAM TRUNG BỘ (W37)',
    'BÁO CÁO TỶ LỆ %FD (RETURN / HOÀN TRẢ) — VÙNG NAM TRUNG BỘ (W38)'
)
html = html.replace(
    'Chu kỳ W37 (07/09 – 13/09/2026)',
    'Chu kỳ W38 (14/09 – 20/09/2026)'
)

# 10. BANNER 11: KTC
html = html.replace(
    'BÁO CÁO ĐIỀU HÀNH KTC & VẬN TẢI — VÙNG NAM TRUNG BỘ (W37)',
    'BÁO CÁO ĐIỀU HÀNH KTC & VẬN TẢI — VÙNG NAM TRUNG BỘ (W38)'
)

# 11. Chart titles in HTML
html = html.replace(
    'SẢN LƯỢNG GIAO 18 AM (CỘT W36 vs W37 + ĐƯỜNG BIẾN ĐỘNG Δ)',
    'SẢN LƯỢNG GIAO 18 AM (CỘT W37 vs W38 + ĐƯỜNG BIẾN ĐỘNG Δ)'
)
html = html.replace(
    '📊 Sản Lượng Full Hàng (Cột W36 vs W37 + Đường Line Δ)',
    '📊 Sản Lượng Full Hàng (Cột W37 vs W38 + Đường Line Δ)'
)
html = html.replace(
    '⚡ Sản Lượng TikTok Shop (Cột W36 vs W37 + Đường Line Δ)',
    '⚡ Sản Lượng TikTok Shop (Cột W37 vs W38 + Đường Line Δ)'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("SUCCESS: Updated all executive banners in index.html!")

# ==============================================================================
# PART 2: UPDATE OPR TTS IN app.js
# ==============================================================================
with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

# Replace renderOprTab calculations
old_opr_func = """    // Tính % OPR TTS tổng toàn vùng (weighted)
    const _ams = D.opr_tts.am;
    const _totalVol = _ams.reduce((s, r) => s + (r.vol_day||0) + (r.vol_night||0), 0);
    const _volDay = _ams.reduce((s, r) => s + (r.vol_day || 0), 0);
    const _volNight = _ams.reduce((s, r) => s + (r.vol_night || 0), 0);
    const _vung36Day = _volDay > 0 ? _ams.reduce((s, r) => s + (r.vol_day || 0) * (r.w37_day !== undefined ? r.w37_day : (r.w36_day || 0)), 0) / _volDay : 0;
    const _vung36Night = _volNight > 0 ? _ams.reduce((s, r) => s + (r.vol_night || 0) * (r.w37_night !== undefined ? r.w37_night : (r.w36_night || 0)), 0) / _volNight : 0;
    const _wtd36 = _ams.reduce((s, r) => {
      const vol = (r.vol_day||0) + (r.vol_night||0);
      const curD = r.w37_day !== undefined ? r.w37_day : (r.w36_day || 0);
      const curN = r.w37_night !== undefined ? r.w37_night : (r.w36_night || 0);
      const o36 = vol > 0 ? ((r.vol_day||0)*curD + (r.vol_night||0)*curN) / vol : 0;
      return s + vol * o36;
    }, 0);
    const _wtd35 = _ams.reduce((s, r) => {
      const vol = (r.vol_day||0) + (r.vol_night||0);
      const prvD = r.w36_day !== undefined ? r.w36_day : (r.w35_day || 0);
      const prvN = r.w36_night !== undefined ? r.w36_night : (r.w35_night || 0);
      const o35 = vol > 0 ? ((r.vol_day||0)*prvD + (r.vol_night||0)*prvN) / vol : 0;
      return s + vol * o35;
    }, 0);
    const _vung36 = _totalVol > 0 ? _wtd36 / _totalVol : 0;
    const _vung35 = _totalVol > 0 ? _wtd35 / _totalVol : 0;
    const _diff = _vung36 - _vung35;
    const _kpiOk = _vung36 >= 0.80;
    const _vungEl = document.getElementById('opr-tts-vung-total');
    if (_vungEl) {
      const diffTxt = (_diff >= 0 ? '▲ +' : '▼ ') + Math.abs(_diff * 100).toFixed(1) + '%p WoW';
      const diffColor = _diff >= 0 ? '#10b981' : '#ef4444';
      const kpiBadge = _kpiOk
        ? '<span class="badge-tag badge-tag-green" style="font-size:13px; font-weight:800; padding:6px 14px;">✅ Đạt KPI (≥80%)</span>'
        : '<span class="badge-tag badge-tag-red" style="font-size:13px; font-weight:800; padding:6px 14px;">❌ Chưa Đạt KPI (<80%)</span>';
      _vungEl.innerHTML = `
        <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:16px; padding:14px 20px; background:linear-gradient(135deg, rgba(239,68,68,0.06), rgba(245,158,11,0.06)); border:1.5px solid rgba(239,68,68,0.25); border-radius:12px; margin-bottom:16px;">
          <div style="display:flex; align-items:center; gap:16px;">
            <div style="font-size:32px; font-weight:900; color:${_kpiOk ? '#10b981' : '#ef4444'}; font-family:var(--font-mono, monospace); line-height:1;">
              ${(_vung36*100).toFixed(1)}%
            </div>
            <div>
              <div style="font-size:12px; font-weight:800; text-transform:uppercase; letter-spacing:0.5px; color:var(--text-main, #1e293b);">
                OPR TTS Toàn Vùng W37 (Tổng Ngày + Đêm)
              </div>
              <div style="font-size:12px; font-weight:700; color:${diffColor}; margin-top:2px;">
                ${diffTxt} (W36: ${(_vung35*100).toFixed(1)}%) &nbsp;•&nbsp; 
                <span style="color:#64748b;">Mục tiêu KPI: ≥ 80.0% (Cách KPI: -${((0.80 - _vung36)*100).toFixed(1)}%p)</span>
              </div>
            </div>
          </div>
          <div style="display:flex; align-items:center; gap:14px; flex-wrap:wrap;">
            <div style="display:flex; gap:8px;">
              <span class="badge-tag badge-tag-amber" style="font-size:11px; padding:5px 10px;">☀️ Ca Ngày: <strong>${(_vung36Day*100).toFixed(1)}%</strong></span>
              <span class="badge-tag badge-tag-purple" style="font-size:11px; padding:5px 10px;">🌙 Ca Đêm: <strong>${(_vung36Night*100).toFixed(1)}%</strong></span>
            </div>
            ${kpiBadge}
          </div>
        </div>
      `;
    }

    // Render danh sách AM chưa đạt KPI OPR TTS (< 80.0%)
    const _failedContainer = document.getElementById('opr-failed-ams-container');
    if (_failedContainer) {
      // Tính tổng đơn trễ OPR toàn vùng
      const totalFailRegion = _ams.reduce((s, r) => {
        const vTot = r.vol_total || r.total_vol || ((r.vol_day || 0) + (r.vol_night || 0));
        const oTot = (r.vol_day === 0 && r.vol_night === 0) ? 0 : (r.w37_total !== undefined ? r.w37_total : (r.w36_total || 0));
        return s + (vTot > 0 ? Math.round(vTot * (1 - (oTot > 1 ? 0 : oTot))) : 0);
      }, 0);

      // Sắp xếp các AM chưa đạt tổng (< 80%) và có đơn (> 0) theo số lượng đơn rớt OPR giảm dần
      const failedTotal = _ams.filter(r => {
        const vTot = r.vol_total || r.total_vol || ((r.vol_day || 0) + (r.vol_night || 0));
        const oTot = r.w37_total !== undefined ? r.w37_total : (r.w36_total || 0);
        return vTot > 0 && oTot < 0.80;
      }).map(r => {
        const vTot = r.vol_total || r.total_vol || ((r.vol_day || 0) + (r.vol_night || 0));
        const oTot = r.w37_total !== undefined ? r.w37_total : (r.w36_total || 0);
        const failTot = vTot > 0 ? Math.round(vTot * (1 - (oTot > 1 ? 0 : oTot))) : 0;
        const rateFail = totalFailRegion > 0 ? (failTot / totalFailRegion) : 0;
        return { ...r, fail_total: failTot, rate_fail: rateFail };
      }).sort((a, b) => b.fail_total - a.fail_total);

      const failedDay = _ams.filter(r => (r.vol_day || 0) > 0 && (r.w37_day !== undefined ? r.w37_day : (r.w36_day || 0)) < 0.80)
                            .sort((a, b) => (a.w37_day || a.w36_day || 0) - (b.w37_day || b.w36_day || 0));
      const failedNight = _ams.filter(r => (r.vol_night || 0) > 0 && (r.w37_night !== undefined ? r.w37_night : (r.w36_night || 0)) < 0.80)
                              .sort((a, b) => (a.w37_night || a.w36_night || 0) - (b.w37_night || b.w36_night || 0));"""

new_opr_func = """    // Tính % OPR TTS tổng toàn vùng (weighted) cho W38 vs W37
    const _ams = D.opr_tts.am;
    const _totalVol = _ams.reduce((s, r) => s + (r.vol_day||0) + (r.vol_night||0), 0);
    const _volDay = _ams.reduce((s, r) => s + (r.vol_day || 0), 0);
    const _volNight = _ams.reduce((s, r) => s + (r.vol_night || 0), 0);
    const _vungCurrDay = _volDay > 0 ? _ams.reduce((s, r) => s + (r.vol_day || 0) * (r.w38_day !== undefined ? r.w38_day : (r.w37_day || 0)), 0) / _volDay : 0;
    const _vungCurrNight = _volNight > 0 ? _ams.reduce((s, r) => s + (r.vol_night || 0) * (r.w38_night !== undefined ? r.w38_night : (r.w37_night || 0)), 0) / _volNight : 0;
    const _wtdCurr = _ams.reduce((s, r) => {
      const vol = (r.vol_day||0) + (r.vol_night||0);
      const curD = r.w38_day !== undefined ? r.w38_day : (r.w37_day || 0);
      const curN = r.w38_night !== undefined ? r.w38_night : (r.w37_night || 0);
      const o = vol > 0 ? ((r.vol_day||0)*curD + (r.vol_night||0)*curN) / vol : 0;
      return s + vol * o;
    }, 0);
    const _wtdPrev = _ams.reduce((s, r) => {
      const vol = (r.vol_day||0) + (r.vol_night||0);
      const prvD = r.w37_day !== undefined ? r.w37_day : (r.w36_day || 0);
      const prvN = r.w37_night !== undefined ? r.w37_night : (r.w36_night || 0);
      const o = vol > 0 ? ((r.vol_day||0)*prvD + (r.vol_night||0)*prvN) / vol : 0;
      return s + vol * o;
    }, 0);
    const _vungCurr = _totalVol > 0 ? _wtdCurr / _totalVol : 0;
    const _vungPrev = _totalVol > 0 ? _wtdPrev / _totalVol : 0;
    const _diff = _vungCurr - _vungPrev;
    const _kpiOk = _vungCurr >= 0.80;
    const _vungEl = document.getElementById('opr-tts-vung-total');
    if (_vungEl) {
      const diffTxt = (_diff >= 0 ? '▲ +' : '▼ ') + Math.abs(_diff * 100).toFixed(1) + '%p WoW';
      const diffColor = _diff >= 0 ? '#10b981' : '#ef4444';
      const kpiBadge = _kpiOk
        ? '<span class="badge-tag badge-tag-green" style="font-size:13px; font-weight:800; padding:6px 14px;">✅ Đạt KPI (≥80%)</span>'
        : '<span class="badge-tag badge-tag-red" style="font-size:13px; font-weight:800; padding:6px 14px;">❌ Chưa Đạt KPI (<80%)</span>';
      _vungEl.innerHTML = `
        <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:16px; padding:14px 20px; background:linear-gradient(135deg, rgba(16,185,129,0.06), rgba(37,99,235,0.06)); border:1.5px solid rgba(16,185,129,0.25); border-radius:12px; margin-bottom:16px;">
          <div style="display:flex; align-items:center; gap:16px;">
            <div style="font-size:32px; font-weight:900; color:${_kpiOk ? '#10b981' : '#ef4444'}; font-family:var(--font-mono, monospace); line-height:1;">
              ${(_vungCurr*100).toFixed(1)}%
            </div>
            <div>
              <div style="font-size:12px; font-weight:800; text-transform:uppercase; letter-spacing:0.5px; color:var(--text-main, #1e293b);">
                OPR TTS Toàn Vùng W38 (Tổng Ngày + Đêm)
              </div>
              <div style="font-size:12px; font-weight:700; color:${diffColor}; margin-top:2px;">
                ${diffTxt} (W37: ${(_vungPrev*100).toFixed(1)}%) &nbsp;•&nbsp; 
                <span style="color:#10b981; font-weight:800;">🏆 Đã vượt chuẩn KPI ≥ 80.0%</span>
              </div>
            </div>
          </div>
          <div style="display:flex; align-items:center; gap:14px; flex-wrap:wrap;">
            <div style="display:flex; gap:8px;">
              <span class="badge-tag badge-tag-amber" style="font-size:11px; padding:5px 10px;">☀️ Ca Ngày: <strong>${(_vungCurrDay*100).toFixed(1)}%</strong></span>
              <span class="badge-tag badge-tag-purple" style="font-size:11px; padding:5px 10px;">🌙 Ca Đêm: <strong>${(_vungCurrNight*100).toFixed(1)}%</strong></span>
            </div>
            ${kpiBadge}
          </div>
        </div>
      `;
    }

    // Render danh sách AM chưa đạt KPI OPR TTS (< 80.0%)
    const _failedContainer = document.getElementById('opr-failed-ams-container');
    if (_failedContainer) {
      // Tính tổng đơn trễ OPR toàn vùng W38
      const totalFailRegion = _ams.reduce((s, r) => {
        const vTot = r.vol_total || r.total_vol || ((r.vol_day || 0) + (r.vol_night || 0));
        const oTot = (r.vol_day === 0 && r.vol_night === 0) ? 0 : (r.w38_total !== undefined ? r.w38_total : (r.w37_total || 0));
        return s + (vTot > 0 ? Math.round(vTot * (1 - (oTot > 1 ? 0 : oTot))) : 0);
      }, 0);

      // Sắp xếp các AM chưa đạt tổng (< 80%) và có đơn (> 0) theo số lượng đơn rớt OPR giảm dần
      const failedTotal = _ams.filter(r => {
        const vTot = r.vol_total || r.total_vol || ((r.vol_day || 0) + (r.vol_night || 0));
        const oTot = r.w38_total !== undefined ? r.w38_total : (r.w37_total || 0);
        return vTot > 0 && oTot < 0.80;
      }).map(r => {
        const vTot = r.vol_total || r.total_vol || ((r.vol_day || 0) + (r.vol_night || 0));
        const oTot = r.w38_total !== undefined ? r.w38_total : (r.w37_total || 0);
        const failTot = vTot > 0 ? Math.round(vTot * (1 - (oTot > 1 ? 0 : oTot))) : 0;
        const rateFail = totalFailRegion > 0 ? (failTot / totalFailRegion) : 0;
        return { ...r, fail_total: failTot, rate_fail: rateFail };
      }).sort((a, b) => b.fail_total - a.fail_total);

      const failedDay = _ams.filter(r => (r.vol_day || 0) > 0 && (r.w38_day !== undefined ? r.w38_day : (r.w37_day || 0)) < 0.80)
                            .sort((a, b) => (a.w38_day || a.w37_day || 0) - (b.w38_day || b.w37_day || 0));
      const failedNight = _ams.filter(r => (r.vol_night || 0) > 0 && (r.w38_night !== undefined ? r.w38_night : (r.w37_night || 0)) < 0.80)
                              .sort((a, b) => (a.w38_night || a.w37_night || 0) - (b.w38_night || b.w37_night || 0));"""

assert old_opr_func in app_js, "old_opr_func not found in app.js"
app_js = app_js.replace(old_opr_func, new_opr_func, 1)

# Fix failedTotal card rendering
old_failed_card = """            ${failedTotal.map(r => {
              const val = (((r.w37_total !== undefined ? r.w37_total : r.w36_total) || 0) * 100);
              const gap = (80 - val).toFixed(1);
              const rawDay = (r.vol_day === 0) ? 0 : (r.w37_day !== undefined ? r.w37_day : (r.w36_day || 0));
              const dayVal = (rawDay * 100).toFixed(1);
              const rawNight = (r.vol_night === 0) ? 0 : (r.w37_night !== undefined ? r.w37_night : (r.w36_night || 0));
              const nightVal = (rawNight * 100).toFixed(1);"""

new_failed_card = """            ${failedTotal.map(r => {
              const val = (((r.w38_total !== undefined ? r.w38_total : r.w37_total) || 0) * 100);
              const gap = (80 - val).toFixed(1);
              const rawDay = (r.vol_day === 0) ? 0 : (r.w38_day !== undefined ? r.w38_day : (r.w37_day || 0));
              const dayVal = (rawDay * 100).toFixed(1);
              const rawNight = (r.vol_night === 0) ? 0 : (r.w38_night !== undefined ? r.w38_night : (r.w37_night || 0));
              const nightVal = (rawNight * 100).toFixed(1);"""

assert old_failed_card in app_js, "old_failed_card not found in app.js"
app_js = app_js.replace(old_failed_card, new_failed_card, 1)

# Fix Bảng 1: Ca Ngày (9h-19h)
old_tbl_day = """    // 1. BẢNG 1: %OPR CA NGÀY (9H-19H)
    const tblBodyDay = document.querySelector('#table-opr-day-detailed tbody');
    if (tblBodyDay) {
      let listDay = [...D.opr_tts.am].map(r => {
        const curr = r.w37_day !== undefined ? r.w37_day : (r.w36_day || 0);
        const prev = r.w36_day !== undefined ? r.w36_day : (r.w35_day || 0);"""

new_tbl_day = """    // 1. BẢNG 1: %OPR CA NGÀY (9H-19H)
    const tblBodyDay = document.querySelector('#table-opr-day-detailed tbody');
    if (tblBodyDay) {
      let listDay = [...D.opr_tts.am].map(r => {
        const curr = r.w38_day !== undefined ? r.w38_day : (r.w37_day || 0);
        const prev = r.w37_day !== undefined ? r.w37_day : (r.w36_day || 0);"""

assert old_tbl_day in app_js, "old_tbl_day not found in app.js"
app_js = app_js.replace(old_tbl_day, new_tbl_day, 1)

# Fix Bảng 2: Ca Đêm (19h-9h)
old_tbl_night = """    // 2. BẢNG 2: %OPR CA ĐÊM (19H-9H)
    const tblBodyNight = document.querySelector('#table-opr-night-detailed tbody');
    if (tblBodyNight) {
      let listNight = [...D.opr_tts.am].map(r => {
        const curr = r.w37_night !== undefined ? r.w37_night : (r.w36_night || 0);
        const prev = r.w36_night !== undefined ? r.w36_night : (r.w35_night || 0);"""

new_tbl_night = """    // 2. BẢNG 2: %OPR CA ĐÊM (19H-9H)
    const tblBodyNight = document.querySelector('#table-opr-night-detailed tbody');
    if (tblBodyNight) {
      let listNight = [...D.opr_tts.am].map(r => {
        const curr = r.w38_night !== undefined ? r.w38_night : (r.w37_night || 0);
        const prev = r.w37_night !== undefined ? r.w37_night : (r.w36_night || 0);"""

assert old_tbl_night in app_js, "old_tbl_night not found in app.js"
app_js = app_js.replace(old_tbl_night, new_tbl_night, 1)

# Fix Bảng 3: Chi Tiết Tổng Hợp OPR TTS
old_tbl_all = """      const totalFailRegion = D.opr_tts.am.reduce((s, r) => {
        const vTot = r.vol_total || r.total_vol || ((r.vol_day || 0) + (r.vol_night || 0));
        const oTot = (r.vol_day === 0 && r.vol_night === 0) ? 0 : (r.w37_total !== undefined ? r.w37_total : (r.w36_total || 0));
        return s + (vTot > 0 ? Math.round(vTot * (1 - (oTot > 1 ? 0 : oTot))) : 0);
      }, 0);

      const sorted = list.map(row => {
        const vTot = row.vol_total || row.total_vol || ((row.vol_day || 0) + (row.vol_night || 0));
        const oTot = (row.vol_day === 0 && row.vol_night === 0) ? 0 : (row.w37_total !== undefined ? row.w37_total : (row.w36_total || 0));
        const failTot = vTot > 0 ? Math.round(vTot * (1 - (oTot > 1 ? 0 : oTot))) : 0;
        const rateFail = totalFailRegion > 0 ? (failTot / totalFailRegion) : 0;
        return { ...row, fail_total: failTot, rate_fail: rateFail, total_calc_vol: vTot };
      }).sort((a, b) => b.fail_total - a.fail_total || (b.diff_night || 0) - (a.diff_night || 0));

      tblBody.innerHTML = sorted.map((row, i) => {
        const isSelected = state.selectedAM === row.am;
        const rowClass = isSelected ? 'presenter-laser-box' : '';
        const rawDay = (row.vol_day === 0 || (row.w36_day || 0) > 1) ? 0 : (row.w36_day !== undefined ? row.w36_day : row.w35_day);
        const prevDay = row.w36_day !== undefined ? row.w35_day : row.w34_day;
        const rawNight = (row.vol_night === 0 || (row.w36_night || 0) > 1) ? 0 : (row.w36_night !== undefined ? row.w36_night : row.w35_night);
        const prevNight = row.w36_night !== undefined ? row.w35_night : row.w34_night;"""

new_tbl_all = """      const totalFailRegion = D.opr_tts.am.reduce((s, r) => {
        const vTot = r.vol_total || r.total_vol || ((r.vol_day || 0) + (r.vol_night || 0));
        const oTot = (r.vol_day === 0 && r.vol_night === 0) ? 0 : (r.w38_total !== undefined ? r.w38_total : (r.w37_total || 0));
        return s + (vTot > 0 ? Math.round(vTot * (1 - (oTot > 1 ? 0 : oTot))) : 0);
      }, 0);

      const sorted = list.map(row => {
        const vTot = row.vol_total || row.total_vol || ((row.vol_day || 0) + (row.vol_night || 0));
        const oTot = (row.vol_day === 0 && row.vol_night === 0) ? 0 : (row.w38_total !== undefined ? row.w38_total : (row.w37_total || 0));
        const failTot = vTot > 0 ? Math.round(vTot * (1 - (oTot > 1 ? 0 : oTot))) : 0;
        const rateFail = totalFailRegion > 0 ? (failTot / totalFailRegion) : 0;
        return { ...row, fail_total: failTot, rate_fail: rateFail, total_calc_vol: vTot };
      }).sort((a, b) => b.fail_total - a.fail_total || (b.diff_night || 0) - (a.diff_night || 0));

      tblBody.innerHTML = sorted.map((row, i) => {
        const isSelected = state.selectedAM === row.am;
        const rowClass = isSelected ? 'presenter-laser-box' : '';
        const rawDay = (row.vol_day === 0 || (row.w38_day || 0) > 1) ? 0 : (row.w38_day !== undefined ? row.w38_day : row.w37_day);
        const prevDay = row.w37_day !== undefined ? row.w37_day : row.w36_day;
        const rawNight = (row.vol_night === 0 || (row.w38_night || 0) > 1) ? 0 : (row.w38_night !== undefined ? row.w38_night : row.w37_night);
        const prevNight = row.w37_night !== undefined ? row.w37_night : row.w36_night;"""

assert old_tbl_all in app_js, "old_tbl_all not found in app.js"
app_js = app_js.replace(old_tbl_all, new_tbl_all, 1)

# Fix renderOprGroupedChart
old_opr_chart = """    const currLabel = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 1] : 'W36';
    const selectedAM = state.selectedAM;
    // Sắp xếp cải thiện tốt nhất giảm dần (diff_total descending)
    const ams = [...D.opr_tts.am].sort((a, b) => {
      const diffA = a.diff_total !== undefined ? a.diff_total : ((a.w36_total || a.w35_total || 0) - (a.w35_total || a.w34_total || 0));
      const diffB = b.diff_total !== undefined ? b.diff_total : ((b.w36_total || b.w35_total || 0) - (b.w35_total || b.w34_total || 0));
      return diffB - diffA;
    });

    const diffVals = ams.map(d => Number(((d.diff_total !== undefined ? d.diff_total : ((d.w36_total || d.w35_total || 0) - (d.w35_total || d.w34_total || 0))) * 100).toFixed(1)));
    const minD = Math.min(...diffVals, 0);
    const maxD = Math.max(...diffVals, 0);

    charts.oprGrouped = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ams.map(d => d.am),
        datasets: [
          {
            type: 'line',
            label: 'Tổng đơn (Miền Sản Lượng)',
            data: ams.map(d => d.vol_total || d.total_vol || ((d.vol_day || 0) + (d.vol_night || 0))),
            fill: true,
            backgroundColor: 'rgba(147, 51, 234, 0.12)',
            borderColor: '#9333ea',
            borderWidth: 1.5,
            tension: 0.35,
            pointRadius: 3,
            pointBackgroundColor: '#9333ea',
            pointBorderColor: '#ffffff',
            pointBorderWidth: 1.5,
            pointHoverRadius: 6,
            yAxisID: 'yVol',
            order: 5,
            datalabels: { display: false }
          },
          {
            type: 'bar',
            label: `%OPR 9h–19h ${currLabel} (Ca Ngày)`,
            data: ams.map(d => {
              if (!d.vol_day || d.vol_day === 0) return 0;
              const val = d.w37_day !== undefined ? d.w37_day : (d.w36_day || 0);
              return Number(((val > 1 ? 0 : val) * 100).toFixed(1));
            }),
            backgroundColor: ams.map(d => selectedAM && selectedAM === d.am ? '#ef4444' : '#2563eb'),
            borderColor: ams.map(d => selectedAM && selectedAM === d.am ? '#ef4444' : 'transparent'),
            borderWidth: ams.map(d => selectedAM && selectedAM === d.am ? 2 : 0),
            borderRadius: 4,
            yAxisID: 'y',
            order: 3,
            datalabels: {
              display: true,
              color: '#ffffff',
              anchor: 'center',
              align: 'center',
              font: { size: 9, weight: '700' },
              formatter: v => v > 15 ? v : ''
            }
          },
          {
            type: 'bar',
            label: `%OPR 19h–9h ${currLabel} (Ca Đêm)`,
            data: ams.map(d => {
              if (!d.vol_night || d.vol_night === 0) return 0;
              const val = d.w37_night !== undefined ? d.w37_night : (d.w36_night || 0);
              return Number(((val > 1 ? 0 : val) * 100).toFixed(1));
            }),
            backgroundColor: ams.map(d => selectedAM && selectedAM === d.am ? '#ef4444' : '#ea580c'),
            borderColor: ams.map(d => selectedAM && selectedAM === d.am ? '#ef4444' : 'transparent'),
            borderWidth: ams.map(d => selectedAM && selectedAM === d.am ? 2 : 0),
            borderRadius: 4,
            yAxisID: 'y',
            order: 3,
            datalabels: {
              display: true,
              color: '#ffffff',
              anchor: 'center',
              align: 'center',
              font: { size: 9, weight: '700' },
              formatter: v => v > 15 ? v : ''
            }
          },
          {
            type: 'line',
            label: `%OPR Tất cả ${currLabel} (Toàn Ngày)`,
            data: ams.map(d => {
              if ((!d.vol_day || d.vol_day === 0) && (!d.vol_night || d.vol_night === 0)) return 0;
              const val = d.w37_total !== undefined ? d.w37_total : (d.w36_total || 0);"""

new_opr_chart = """    const currLabel = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 1] : 'W38';
    const selectedAM = state.selectedAM;
    // Sắp xếp cải thiện tốt nhất giảm dần (diff_total descending)
    const ams = [...D.opr_tts.am].sort((a, b) => {
      const diffA = a.diff_total !== undefined ? a.diff_total : ((a.w38_total || 0) - (a.w37_total || 0));
      const diffB = b.diff_total !== undefined ? b.diff_total : ((b.w38_total || 0) - (b.w37_total || 0));
      return diffB - diffA;
    });

    const diffVals = ams.map(d => Number(((d.diff_total !== undefined ? d.diff_total : ((d.w38_total || 0) - (d.w37_total || 0))) * 100).toFixed(1)));
    const minD = Math.min(...diffVals, 0);
    const maxD = Math.max(...diffVals, 0);

    charts.oprGrouped = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ams.map(d => d.am),
        datasets: [
          {
            type: 'line',
            label: 'Tổng đơn (Miền Sản Lượng)',
            data: ams.map(d => d.vol_total || d.total_vol || ((d.vol_day || 0) + (d.vol_night || 0))),
            fill: true,
            backgroundColor: 'rgba(147, 51, 234, 0.12)',
            borderColor: '#9333ea',
            borderWidth: 1.5,
            tension: 0.35,
            pointRadius: 3,
            pointBackgroundColor: '#9333ea',
            pointBorderColor: '#ffffff',
            pointBorderWidth: 1.5,
            pointHoverRadius: 6,
            yAxisID: 'yVol',
            order: 5,
            datalabels: { display: false }
          },
          {
            type: 'bar',
            label: `%OPR 9h–19h ${currLabel} (Ca Ngày)`,
            data: ams.map(d => {
              if (!d.vol_day || d.vol_day === 0) return 0;
              const val = d.w38_day !== undefined ? d.w38_day : (d.w37_day || 0);
              return Number(((val > 1 ? 0 : val) * 100).toFixed(1));
            }),
            backgroundColor: ams.map(d => selectedAM && selectedAM === d.am ? '#ef4444' : '#2563eb'),
            borderColor: ams.map(d => selectedAM && selectedAM === d.am ? '#ef4444' : 'transparent'),
            borderWidth: ams.map(d => selectedAM && selectedAM === d.am ? 2 : 0),
            borderRadius: 4,
            yAxisID: 'y',
            order: 3,
            datalabels: {
              display: true,
              color: '#ffffff',
              anchor: 'center',
              align: 'center',
              font: { size: 9, weight: '700' },
              formatter: v => v > 15 ? v : ''
            }
          },
          {
            type: 'bar',
            label: `%OPR 19h–9h ${currLabel} (Ca Đêm)`,
            data: ams.map(d => {
              if (!d.vol_night || d.vol_night === 0) return 0;
              const val = d.w38_night !== undefined ? d.w38_night : (d.w37_night || 0);
              return Number(((val > 1 ? 0 : val) * 100).toFixed(1));
            }),
            backgroundColor: ams.map(d => selectedAM && selectedAM === d.am ? '#ef4444' : '#ea580c'),
            borderColor: ams.map(d => selectedAM && selectedAM === d.am ? '#ef4444' : 'transparent'),
            borderWidth: ams.map(d => selectedAM && selectedAM === d.am ? 2 : 0),
            borderRadius: 4,
            yAxisID: 'y',
            order: 3,
            datalabels: {
              display: true,
              color: '#ffffff',
              anchor: 'center',
              align: 'center',
              font: { size: 9, weight: '700' },
              formatter: v => v > 15 ? v : ''
            }
          },
          {
            type: 'line',
            label: `%OPR Tất cả ${currLabel} (Toàn Ngày)`,
            data: ams.map(d => {
              if ((!d.vol_day || d.vol_day === 0) && (!d.vol_night || d.vol_night === 0)) return 0;
              const val = d.w38_total !== undefined ? d.w38_total : (d.w37_total || 0);"""

assert old_opr_chart in app_js, "old_opr_chart not found in app.js"
app_js = app_js.replace(old_opr_chart, new_opr_chart, 1)

# Fix target line in OPR chart
app_js = app_js.replace(
    "label: 'Toàn Vùng W37: 78.1% (Chưa Đạt)',",
    "label: 'Toàn Vùng W38: 83.0% (Đạt KPI)',"
)
app_js = app_js.replace(
    "yMin: 78.1, yMax: 78.1,",
    "yMin: 83.0, yMax: 83.0,"
)
app_js = app_js.replace(
    "borderColor: '#dc2626',",
    "borderColor: '#10b981',"
)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)

print("SUCCESS: Updated OPR TTS logic in app.js!")
