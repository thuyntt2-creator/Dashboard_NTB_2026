import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

# -------------------------------------------------------------
# 1. UPDATE index.html
# -------------------------------------------------------------
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Filter option
html = html.replace('<option value="W39" selected>Tuần W39 (Hiện tại)</option>',
                    '<option value="W40" selected>Tuần W40 (Hiện tại)</option>')

# Tab 1: Overview
html = html.replace('TỔNG HỢP TRỌNG TÂM HỌP TUẦN W39 — VÙNG NAM TRUNG BỘ',
                    'TỔNG HỢP TRỌNG TÂM HỌP TUẦN W40 — VÙNG NAM TRUNG BỘ')

overview_summary_w39 = """              • <strong>Sản lượng Giao Full Hàng:</strong> Đạt <strong>328,925 đơn</strong> (Tuần W39 kết thúc 27/09/2026, -14,672 đơn / -4.3% WoW so với W38: 343,597 đơn).<br>
              • <strong>Sản lượng TikTok Shop (TTS):</strong> Đạt <strong>72,781 đơn</strong> (tăng <strong>+4,055 đơn / +5.9% WoW</strong> so với W38: 68,726 đơn), chiếm 22.1% tổng sản lượng toàn vùng.<br>
              • <strong>Chất lượng vận hành:</strong> %ODR Full hàng đạt <strong>90.8%</strong>, %LTC đạt <strong>90.1%</strong>. Tỷ lệ Rớt LC <strong>1.52%</strong> (giảm mạnh -1.80%p WoW). Tỷ lệ %FD Hoàn Trả <strong>7.64%</strong>.<br>
              • <strong>Truy Thu & COD W39:</strong> Tiền Cần Truy Thu phát sinh <strong>174.7 Tr ₫</strong> (giảm -21.2 Tr ₫ WoW), Tỷ lệ tiền mặt COD đạt <strong>40.1%</strong> (giảm -3.0%p WoW)."""

overview_summary_w40 = """              • <strong>Sản lượng Giao Full Hàng:</strong> Đạt <strong>311,503 đơn</strong> (Tuần W40 kết thúc 04/10/2026, -19,810 đơn / -6.0% WoW so với W39: 331,313 đơn).<br>
              • <strong>Sản lượng TikTok Shop (TTS):</strong> Đạt <strong>72,253 đơn</strong> (-1,190 đơn / -1.6% WoW so với W39: 73,443 đơn), chiếm 23.2% tổng sản lượng toàn vùng.<br>
              • <strong>Chất lượng vận hành bứt phá:</strong> %ODR Full hàng đạt <strong>93.1%</strong> (+2.3%p WoW), %LTC đạt <strong>91.4%</strong> (+1.2%p WoW). Tỷ lệ Rớt LC <strong>1.69%</strong> (kiểm soát dưới ngưỡng 2.0%). Tỷ lệ %FD Hoàn Trả <strong>7.77%</strong>.<br>
              • <strong>Hiệu suất GTC:</strong> Full hàng đạt <strong>60.9%</strong> (+4.2%p WoW so với W39: 56.7%), TTS đạt <strong>63.4%</strong> (+5.8%p WoW so với W39: 57.5%) — Hoàn thành mục tiêu GTC ≥ 60%!"""

html = html.replace(overview_summary_w39, overview_summary_w40)
html = html.replace('Mục tiêu W39: GTC ≥ 60%', 'Mục tiêu W40: GTC ≥ 60% (Đạt 60.9%)')

# Card headers in Overview
html = html.replace('XU HƯỚNG CÁC CHỈ SỐ VẬN HÀNH CHÍNH (W36 – W39)', 'XU HƯỚNG CÁC CHỈ SỐ VẬN HÀNH CHÍNH (W37 – W40)')
html = html.replace('XU HƯỚNG CÁC CHỈ SỐ VẬN HÀNH CHÍNH (W36 - W39)', 'XU HƯỚNG CÁC CHỈ SỐ VẬN HÀNH CHÍNH (W37 – W40)')
html = html.replace('SẢN LƯỢNG GIAO THEO 5 TỈNH THÀNH (FULL HÀNG vs TTS — W39)', 'SẢN LƯỢNG GIAO THEO 5 TỈNH THÀNH (FULL HÀNG vs TTS — W40)')
html = html.replace('SẢN LƯỢNG GIAO THEO 5 TỈNH THÀNH (FULL HÀNG VS TTS — W39)', 'SẢN LƯỢNG GIAO THEO 5 TỈNH THÀNH (FULL HÀNG vs TTS — W40)')
html = html.replace('ĐIỂM NỔI BẬT & ĐÁNH GIÁ W39', 'ĐIỂM NỔI BẬT & ĐÁNH GIÁ W40')
html = html.replace('ĐIỂM NỔI BẬT &amp; ĐÁNH GIÁ W39', 'ĐIỂM NỔI BẬT &amp; ĐÁNH GIÁ W40')
html = html.replace('BẢNG TỔNG HỢP CÁC CHỈ SỐ VÙNG NTB (W36 – W39) — FULL HÀNG & TTS', 'BẢNG TỔNG HỢP CÁC CHỈ SỐ VÙNG NTB (W37 – W40) — FULL HÀNG & TTS')
html = html.replace('BẢNG TỔNG HỢP CÁC CHỈ SỐ VÙNG NTB (W36 – W39) — FULL HÀNG &amp; TTS', 'BẢNG TỔNG HỢP CÁC CHỈ SỐ VÙNG NTB (W37 – W40) — FULL HÀNG &amp; TTS')
html = html.replace('Dữ liệu so sánh W36 – W39 kèm đường Xu Hướng (Trend)', 'Dữ liệu so sánh W37 – W40 kèm đường Xu Hướng (Trend)')
html = html.replace('%GTC W39</th>', '%GTC W40</th>')

# Tab 2: Sản Lượng
html = html.replace('PHÂN TÍCH SẢN LƯỢNG GIAO TOÀN VÙNG, 5 TỈNH THÀNH & 18 AM (W39)',
                    'PHÂN TÍCH SẢN LƯỢNG GIAO TOÀN VÙNG, 5 TỈNH THÀNH & 18 AM (W40)')
html = html.replace('PHÂN TÍCH SẢN LƯỢNG GIAO TOÀN VÙNG, 5 TỈNH THÀNH &amp; 18 AM (W39)',
                    'PHÂN TÍCH SẢN LƯỢNG GIAO TOÀN VÙNG, 5 TỈNH THÀNH &amp; 18 AM (W40)')

vol_summary_w39 = """              • <strong>Sản lượng Toàn Mạng (W39):</strong> Full hàng đạt <strong>328,925 đơn</strong> (giảm <strong>-14,672 đơn / -4.3% WoW</strong> so với W38: 343,597 đơn); Kênh TikTok Shop đạt <strong>72,781 đơn</strong> (+4,055 đơn / +5.9% WoW). • <strong>Theo 5 Tỉnh:</strong> Khánh Hòa dẫn đầu quy mô đạt <strong>96,012 đơn</strong> (TTS: 18,142 đơn), Lâm Đồng thứ 2 đạt <strong>95,727 đơn</strong> (TTS: 19,587 đơn), Bình Thuận đạt <strong>85,489 đơn</strong> (TTS: 15,873 đơn), Đắk Nông đạt <strong>34,848 đơn</strong> (TTS: 8,314 đơn), Ninh Thuận đạt <strong>33,918 đơn</strong> (TTS: 7,358 đơn).<br>
              • <strong>Biến động AM:</strong> AM Nguyễn Hoàng Phi dẫn đầu tăng trưởng (+3,210 đơn Full), tiếp theo là Cao Thị Thanh Thủy (+2,828 đơn), Huỳnh Thị Kim Chi (+1,452 đơn)."""

vol_summary_w40 = """              • <strong>Sản lượng Toàn Mạng (W40):</strong> Full hàng đạt <strong>311,503 đơn</strong> (giảm <strong>-19,810 đơn / -6.0% WoW</strong> so với W39: 331,313 đơn); Kênh TikTok Shop đạt <strong>72,253 đơn</strong> (-1,190 đơn / -1.6% WoW so với W39: 73,443 đơn). • <strong>Theo 5 Tỉnh:</strong> Khánh Hòa đạt <strong>84,777 đơn</strong> (TTS: 15,921 đơn), Bình Thuận đạt <strong>83,686 đơn</strong> (TTS: 22,331 đơn), Ninh Thuận đạt <strong>33,549 đơn</strong> (TTS: 11,156 đơn), Đắk Nông đạt <strong>31,772 đơn</strong> (TTS: 8,720 đơn).<br>
              • <strong>Biến động AM:</strong> AM Lê Thanh Nhựt tăng trưởng dẫn đầu (+1,316 đơn Full), các AM còn lại kiểm soát tốt tải vận hành."""

html = html.replace(vol_summary_w39, vol_summary_w40)
html = html.replace('Full: 346.0k đơn | TTS: 69.3k đơn', 'Full: 311.5k đơn | TTS: 72.3k đơn')

html = html.replace('2. BÓC TÁCH CHI TIẾT SẢN LƯỢNG THEO 18 AM PHỤ TRÁCH (CỘT W38 vs W39 + LINE Δ)',
                    '2. BÓC TÁCH CHI TIẾT SẢN LƯỢNG THEO 18 AM PHỤ TRÁCH (CỘT W39 vs W40 + LINE Δ)')
html = html.replace('SẢN LƯỢNG GIAO 18 AM (CỘT W38 vs W39 + ĐƯỜNG BIẾN ĐỘNG Δ)',
                    'SẢN LƯỢNG GIAO 18 AM (CỘT W39 vs W40 + ĐƯỜNG BIẾN ĐỘNG Δ)')
html = html.replace('📊 Sản Lượng Full Hàng (Cột W38 vs W39 + Đường Line Δ)',
                    '📊 Sản Lượng Full Hàng (Cột W39 vs W40 + Đường Line Δ)')
html = html.replace('⚡ Sản Lượng TikTok Shop (Cột W38 vs W39 + Đường Line Δ)',
                    '⚡ Sản Lượng TikTok Shop (Cột W39 vs W40 + Đường Line Δ)')

# Tab 3: %GTC Tổng
html = html.replace('PHÂN TÍCH HIỆU SUẤT %GTC TỔNG TOÀN MẠNG THEO 18 AM & 5 TỈNH (W39)',
                    'PHÂN TÍCH HIỆU SUẤT %GTC TỔNG TOÀN MẠNG THEO 18 AM & 5 TỈNH (W40)')
html = html.replace('PHÂN TÍCH HIỆU SUẤT %GTC TỔNG TOÀN MẠNG THEO 18 AM &amp; 5 TỈNH (W39)',
                    'PHÂN TÍCH HIỆU SUẤT %GTC TỔNG TOÀN MẠNG THEO 18 AM &amp; 5 TỈNH (W40)')

gtc_summary_w39 = """              • <strong>%GTC Tổng Toàn Vùng (W39):</strong> Full hàng đạt <strong>56.6%</strong> (+0.9%p WoW so với W38: 55.7%) và TTS đạt <strong>57.4%</strong> (+3.5%p WoW so với W38: 54.0%). • <strong>Top AM dẫn đầu:</strong> <strong>Nguyễn Ngọc Khánh (73.2%)</strong>, <strong>Cao Thị Thanh Thủy (70.1%)</strong>, <strong>Nguyễn Duy Long (67.8%)</strong>, <strong>Nguyễn Thị Tuyết Thơ (66.5%)</strong>.<br>
              • <strong>Bứt phá tăng trưởng WoW:</strong> <strong>Nguyễn Hoàng Phi</strong> tăng mạnh nhất +5.3%p (lên 76.8%); <strong>Cao Thị Thanh Thủy</strong> tăng +2.7%p (lên 84.5%); <strong>Nguyễn Ngọc Khánh</strong> tăng +1.0%p (lên 87.5%).<br>
              • <strong>Nhóm AM suy giảm cần thúc đẩy xả tồn:</strong> <strong>Nguyễn Thanh Long (42.5% / giảm -16.8%p)</strong>, <strong>Phan Đình Duy (59.1% / giảm -8.5%p)</strong>, <strong>Lê Văn Trường (52.9% / giảm -8.5%p)</strong>, <strong>Lê Minh Lợi (41.4% / giảm -7.3%p)</strong>."""

gtc_summary_w40 = """              • <strong>%GTC Tổng Toàn Vùng (W40):</strong> Full hàng đạt <strong>60.87%</strong> (+4.19%p WoW so với W39: 56.68%) và TTS đạt <strong>63.38%</strong> (+5.84%p WoW so với W39: 57.54%) — Cả hai đều xuất sắc vượt chuẩn Target ≥ 60.0%! • <strong>Theo 5 Tỉnh:</strong> Bình Thuận (67.45%), Khánh Hòa (62.23%), Đắk Nông (54.46%), Lâm Đồng (54.43%).<br>
              • <strong>Bứt phá tăng trưởng WoW:</strong> 18 AM đồng loạt tăng trưởng mạnh mẽ, tỷ lệ giao thành công nâng cao rõ rệt."""

html = html.replace(gtc_summary_w39, gtc_summary_w40)
html = html.replace('Full: 55.75% | TTS: 54.01% (Target ≥ 60.0%)', 'Full: 60.87% | TTS: 63.38% (Target ≥ 60.0%)')
html = html.replace('2. BÓC TÁCH HIỆU SUẤT %GTC THEO 18 AM PHỤ TRÁCH (CỘT W38 vs W39 + LINE Δ)',
                    '2. BÓC TÁCH HIỆU SUẤT %GTC THEO 18 AM PHỤ TRÁCH (CỘT W39 vs W40 + LINE Δ)')
html = html.replace('BIỂU ĐỒ SO SÁNH %GTC TỔNG W38 vs W39 THEO 18 AM (FULL HÀNG)',
                    'BIỂU ĐỒ SO SÁNH %GTC TỔNG W39 vs W40 THEO 18 AM (FULL HÀNG)')

# Tab 4: %GTC Ca 1 TTS
html = html.replace('PHÂN TÍCH CHUYÊN SÂU %GTC CA 1 TIKTOK SHOP (TARGET SLA ≥ 76.0%) (W39)',
                    'PHÂN TÍCH CHUYÊN SÂU %GTC CA 1 TIKTOK SHOP (TARGET SLA ≥ 76.0%) (W40)')
html = html.replace('Target ≥ 76.0% (W39: 75.10%)', 'Target ≥ 76.0% (W40: 81.34%)')

gtc_ca1_summary_w39 = """              • <strong>Toàn Vùng TTS Ca 1 (W39):</strong> Đạt <strong>75.10%</strong> (tăng <strong>+3.84%p WoW</strong> so với 71.26% W38), áp sát mục tiêu cam kết Target SLA 76.0% (chỉ còn thiếu 0.90%p). • <strong>Top 7 AM Đạt Chuẩn (≥76%):</strong> <strong>Nguyễn Ngọc Khánh (89.1%)</strong>, <strong>Nguyễn Đỗ Minh Nghĩa (86.9%)</strong>, <strong>Cao Thị Thanh Thủy (86.0%)</strong>, <strong>Nguyễn Duy Long (85.5%)</strong>, <strong>Nguyễn Thị Tuyết Thơ (81.6%)</strong>, <strong>Lê Thanh Nhựt (80.0%)</strong>, <strong>Nguyễn Hoàng Phi (79.0%)</strong>.<br>
              • <strong>Bứt Phá Tăng Trưởng Ca 1:</strong> <strong>Nguyễn Thanh Long (Cam Ranh)</strong> bứt phá ngoạn mục nhất <strong>+24.1%p</strong> (từ 42.5% lên <strong>66.6%</strong>); <strong>Phan Đình Duy</strong> tăng <strong>+15.9%p</strong> (từ 59.1% lên <strong>75.0%</strong>); <strong>Hồng Bích Nga</strong> tăng <strong>+8.2%p</strong> (lên <strong>74.7%</strong>).<br>
              • <strong>Nhóm AM Cần Thúc Đẩy Ca 1:</strong> <strong>Lê Minh Lợi (38.7%)</strong>, <strong>Trương Quang Linh (39.2%)</strong>, <strong>Lê Văn Trường (51.2%)</strong>, <strong>Nguyễn Lê Nguyên Vũ (53.1%)</strong>; đặc biệt <strong>Thái Thị Thanh Thư tụt dốc -7.1%p</strong> (từ 82.1% xuống 75.0%)."""

gtc_ca1_summary_w40 = """              • <strong>Toàn Vùng TTS Ca 1 (W40):</strong> Ca 1 thuần sáng bứt phá ngoạn mục đạt <strong>81.34%</strong> (tăng mạnh <strong>+6.17%p WoW</strong> so với 75.16% W39), vượt xa cam kết SLA ≥ 76.0%! Ca 1 + Tồn đạt <strong>66.47%</strong> (+6.58%p WoW).<br>
              • <strong>Đánh Giá:</strong> Hiệu suất giao ca 1 sáng TikTok Shop đồng loạt khởi sắc trên toàn mạng, khẳng định sự tập trung dồn lực xuất sắc của đội ngũ AM."""

html = html.replace(gtc_ca1_summary_w39, gtc_ca1_summary_w40)

# Tab 5: % Gán
html = html.replace('Gán Tổng W39: 82.5% (Target ≥ 90.0%)', 'Gán Tổng W40: 86.3% (Target ≥ 90.0%)')
html = html.replace('TỔNG QUAN VÙNG NTB — TỶ LỆ % GÁN (4 TUẦN W36 – W39)', 'TỔNG QUAN VÙNG NTB — TỶ LỆ % GÁN (4 TUẦN W37 – W40)')
html = html.replace('SO SÁNH TỶ LỆ GÁN 18 AM: % GÁN CA 1+TỒN vs % GÁN CA 2 vs % GÁN TỔNG (W37)',
                    'SO SÁNH TỶ LỆ GÁN 18 AM: % GÁN CA 1+TỒN vs % GÁN CA 2 vs % GÁN TỔNG (W40)')

gan_summary_w39 = """              • <strong>Gán Tổng (Ca1+Ca2+Tồn W39):</strong> Full hàng đạt <strong>82.5%</strong> (+1.9%p WoW so với 80.6% W38); TTS đạt <strong>85.1%</strong> (+2.0%p WoW). • <strong>Gán Ca 1 + Tồn:</strong> Full hàng đạt <strong>85.9%</strong> (-3.1%p WoW so với 89.0% W37); TTS đạt <strong>85.5%</strong> (-2.9%p WoW so với 88.4% W37).<br>
              • <strong>Gán Ca 2:</strong> Full hàng đạt <strong>56.8%</strong> (+1.2%p WoW so với 55.7% W37); TTS đạt <strong>53.4%</strong> (+1.5%p WoW so với 51.9% W37).<br>
              • <strong>Điểm nhấn 18 AM:</strong> Top Gán Tổng cao nhất: <strong>Cao Thị Thanh Thủy (93.0%)</strong>, <strong>Nguyễn Duy Long (91.2%)</strong>, <strong>Nguyễn Ngọc Khánh (91.0%)</strong>, <strong>Thái Thị Thanh Thư (90.5%)</strong>. Cần thúc đẩy: <strong>Trương Quang Linh (41.5%)</strong>, <strong>Huỳnh Thúc Duân (72.5%)</strong>, <strong>Hồng Bích Nga (71.4%)</strong>."""

gan_summary_w40 = """              • <strong>Gán Tổng (Ca1+Ca2+Tồn W40):</strong> Full hàng đạt <strong>86.32%</strong> (+3.86%p WoW so với 82.47% W39); TTS đạt <strong>87.99%</strong> (+5.17%p WoW so với 82.83% W39).<br>
              • <strong>Gán Ca 1 + Tồn:</strong> Full hàng bứt phá đạt <strong>92.77%</strong> (+5.32%p WoW, vượt chuẩn ≥ 90%); TTS đạt <strong>94.80%</strong> (+6.58%p WoW, vượt chuẩn ≥ 90%).<br>
              • <strong>Gán Ca 2:</strong> Full hàng đạt <strong>62.87%</strong> (+3.59%p WoW); TTS đạt <strong>63.54%</strong> (+4.98%p WoW)."""

html = html.replace(gan_summary_w39, gan_summary_w40)

# Tab 6: %ODR
odr_summary_w39 = """              • <strong>Toàn Vùng W39:</strong> Full Hàng đạt <strong>90.8%</strong> và TTS đạt <strong>90.5%</strong>. • <strong>Theo 5 Tỉnh:</strong> Ninh Thuận (96.5%) và Bình Thuận (96.2%) tiếp tục dẫn đầu toàn vùng, bảo vệ vững chắc chuẩn xanh SLA ≥ 92%. Khánh Hòa đạt 94.6%. Cần cải thiện: Đắk Nông (90.5%), Lâm Đồng (90.2%).<br>
              • <strong>Top AM Xuất Sắc:</strong> <strong>Nguyễn Ngọc Khánh (96.8%)</strong>, <strong>Cao Thị Thanh Thủy (96.7%)</strong>, <strong>Thái Thị Thanh Thư (96.5%)</strong>, <strong>Nguyễn Duy Long (95.8%)</strong>. Cần đôn đốc xả tồn: <strong>Lê Văn Trường (84.2%)</strong>, <strong>Trầm Hữu Tiến (73.1%)</strong>."""

odr_summary_w40 = """              • <strong>Toàn Vùng W40:</strong> Full Hàng đạt <strong>93.12%</strong> (+2.28%p WoW) và TTS đạt <strong>94.18%</strong> (+2.41%p WoW) — Vượt xuất sắc chuẩn cam kết SLA ≥ 92.0%! • <strong>Theo 5 Tỉnh:</strong> Bình Thuận (96.74%), Khánh Hòa (95.59%), Đắk Nông (90.42%), Lâm Đồng (87.79%).<br>
              • <strong>Đánh Giá:</strong> Chất lượng giao đúng hẹn được giữ vững và cải thiện vượt bậc, đạt chuẩn xanh toàn diện."""

html = html.replace(odr_summary_w39, odr_summary_w40)
html = html.replace('ODR Full: 91.2% | TTS: 91.5% (Target ≥ 92.0%)', 'ODR Full: 93.1% | TTS: 94.2% (Target ≥ 92.0%)')
html = html.replace('2. BÓC TÁCH CHỈ SỐ %ODR THEO 18 AM PHỤ TRÁCH (CỘT W38 vs W39 + LINE Δ)',
                    '2. BÓC TÁCH CHỈ SỐ %ODR THEO 18 AM PHỤ TRÁCH (CỘT W39 vs W40 + LINE Δ)')

# Tab 7: %LTC
ltc_summary_w39 = """              • <strong>Toàn Vùng W39:</strong> Full hàng đạt <strong>90.1%</strong>, TTS đạt <strong>95.2%</strong>. • <strong>Top AM Dẫn Đầu:</strong> <strong>Nguyễn Lê Nguyên Vũ (96.8%)</strong>, <strong>Phan Đình Duy (96.1%)</strong>, <strong>Nguyễn Duy Long (94.5%)</strong>.<br>
              • <strong>Bứt Phá Lấy Hàng:</strong> Tỷ lệ lấy thành công TTS tăng mạnh ở hầu hết các bưu cục trên địa bàn Khánh Hòa và Lâm Đồng."""

ltc_summary_w40 = """              • <strong>Toàn Vùng W40:</strong> Full hàng đạt <strong>91.35%</strong> (+1.22%p WoW so với 90.13% W39); TTS đạt <strong>94.97%</strong> (+0.39%p WoW) — Tiếp tục giữ vững và vượt chuẩn cam kết Target ≥ 90.0%.<br>
              • <strong>Đánh Giá:</strong> Tiến độ thu gom hàng và xử lý ca lấy được kiểm soát nhịp nhàng trên toàn địa bàn 5 tỉnh thành."""

html = html.replace(ltc_summary_w39, ltc_summary_w40)
html = html.replace('Full: 90.4% | TTS: 95.4% (Target ≥ 90.0%)', 'Full: 91.4% | TTS: 95.0% (Target ≥ 90.0%)')

# Tab 8: %OPR TTS
opr_summary_w39 = """              • <strong>Toàn Vùng W39 (Tổng Ngày + Đêm):</strong> Đạt <strong>79.1%</strong> (giảm <strong>-3.8%p WoW</strong> so với 82.8% W38) — <strong style="color:#ef4444;">Chưa Đạt Target KPI ≥ 80.0%</strong> do Ca Đêm giảm sút nghiêm trọng. • <strong>Khung Giờ Ngày vs Đêm:</strong> Ca Ngày (9h–19h) giữ vững phong độ đạt <strong>91.0%</strong> (5,832/6,409 đơn đạt, +0.8%p WoW); Ca Đêm (19h–9h) sụt giảm sâu chỉ đạt <strong>61.1%</strong> (giảm <strong>-12.0%p WoW</strong> so với 73.1% W38; có tới 1,656 đơn trễ hạn xử lý đêm).<br>
              • <strong>Top AM Đạt KPI Xuất Sắc (≥80.0%):</strong> <strong>Phan Đình Duy (96.8% / +14.0%p)</strong>, <strong>Nguyễn Lê Nguyên Vũ (92.3%)</strong>, <strong>Nguyễn Duy Long (90.7%)</strong>, <strong>Thái Thị Thanh Thư (90.2%)</strong>, <strong>Nguyễn Thanh Long (87.4%)</strong>, <strong>Nguyễn Thị Tuyết Thơ (85.0% / +28.9%p)</strong>, <strong>Hồng Bích Nga (82.3%)</strong>, <strong>Cao Thị Thanh Thủy (82.1%)</strong>.<br>
              • <strong>Top AM Chưa Đạt KPI gây trễ đơn OPR:</strong> <strong>Lê Thanh Nhựt (67.6% / trễ 464 đơn)</strong>, <strong>Nguyễn Hoàng Phi (59.3% / trễ 346 đơn)</strong>, <strong>Lê Văn Trường (53.5% / trễ 266 đơn)</strong>, <strong>Trần Thị Nhung (25.3% / trễ 136 đơn)</strong>, <strong>Nguyễn Ngọc Khánh (76.1% / trễ 130 đơn)</strong>."""

opr_summary_w40 = """              • <strong>Toàn Vùng W40 (Tổng Ngày + Đêm):</strong> Đạt <strong>83.45%</strong> (tăng mạnh <strong>+4.3%p WoW</strong> so với 79.1% W39) — <strong style="color:#10b981;">Chính Thức Vượt Target KPI ≥ 80.0%</strong>! • <strong>Khung Giờ Ngày vs Đêm:</strong> Ca Ngày (9h–19h) đạt <strong>91.8%</strong> (+0.8%p WoW); Ca Đêm (19h–9h) bứt phá lên <strong>71.2%</strong> (tăng <strong>+10.1%p WoW</strong> so với 61.1% W39).<br>
              • <strong>Đánh Giá:</strong> Điểm nghẽn ca đêm đã được giải quyết cơ bản, đưa toàn vùng về chuẩn KPI cam kết."""

html = html.replace(opr_summary_w39, opr_summary_w40)
html = html.replace('OPR TTS W39: 79.1% (Chưa Đạt KPI &lt; 80.0%)', 'OPR TTS W40: 83.5% (Vượt Target KPI ≥ 80.0%)')

# Tab 9: % Rớt Luân Chuyển
rot_summary_w39 = """              • <strong>Tổng đơn rớt toàn vùng W39:</strong> Tỷ lệ rớt đạt <strong>1.52%</strong> (giảm mạnh <strong>-1.80%p WoW</strong> so với 3.32% W38), chất lượng luân chuyển cải thiện vượt bậc. • <strong>Top 5 AM rớt nhiều nhất (chiếm 71.8% lượng rớt):</strong> <strong>Thái Thị Thanh Thư (79 đơn - 7.13%)</strong>, <strong>Trần Thị Nhung (33 đơn - 19.76%)</strong>, <strong>Hồng Bích Nga (27 đơn - 4.49%)</strong>, <strong>Huỳnh Thúc Duân (21 đơn - 20.79%)</strong>, <strong>Lê Văn Trường (21 đơn - 4.24%)</strong>.<br>
              • <strong>Theo Tỉnh thành:</strong> <strong>Khánh Hòa</strong> chiếm <strong>102 đơn (5.09%)</strong>, <strong>Lâm Đồng</strong> 58 đơn (3.32%), <strong>Đắk Nông</strong> 57 đơn (20.73%), <strong>Bình Thuận</strong> 19 đơn (0.88%), <strong>Ninh Thuận</strong> 16 đơn (1.14%)."""

rot_summary_w40 = """              • <strong>Tổng đơn rớt toàn vùng W40:</strong> Tỷ lệ rớt đạt <strong>1.69%</strong> (tổng 219 đơn rớt / 12,934 đơn cần LC, tăng nhẹ +0.18%p WoW so với 1.52% W39) — Tiếp tục kiểm soát rất tốt dưới ngưỡng Target ≤ 2.00%!<br>
              • <strong>Đánh Giá:</strong> Các bưu cục và trung tâm khai thác phối hợp đồng bộ, hạn chế tối đa rớt kết nối ca luân chuyển."""

html = html.replace(rot_summary_w39, rot_summary_w40)
html = html.replace('Tổng rớt W39: 115 đơn (1.52%)', 'Tổng rớt W40: 219 đơn (1.69%)')
html = html.replace('% RỚT LUÂN CHUYỂN THEO 18 AM PHỤ TRÁCH (W39)', '% RỚT LUÂN CHUYỂN THEO 18 AM PHỤ TRÁCH (W40)')
html = html.replace('DANH SÁCH TOP 20 BƯU CỤC CÓ TỶ LỆ RỚT LUÂN CHUYỂN CAO NHẤT (W39)',
                    'DANH SÁCH TOP 20 BƯU CỤC CÓ TỶ LỆ RỚT LUÂN CHUYỂN CAO NHẤT (W40)')
html = html.replace('% Rớt LC (W39)', '% Rớt LC (W40)')

# Tab 10: %FD Hoàn Trả
html = html.replace('BÁO CÁO TỶ LỆ %FD (RETURN / HOÀN TRẢ) — VÙNG NAM TRUNG BỘ (W39)',
                    'BÁO CÁO TỶ LỆ %FD (RETURN / HOÀN TRẢ) — VÙNG NAM TRUNG BỘ (W40)')
html = html.replace('Chu kỳ W39 (21/09 – 27/09/2026) &nbsp;|&nbsp; So sánh biến động WoW với tuần trước (W38) &nbsp;|&nbsp; Tách riêng Full Hàng và TikTok Shop',
                    'Chu kỳ W40 (28/09 – 04/10/2026) &nbsp;|&nbsp; So sánh biến động WoW với tuần trước (W39) &nbsp;|&nbsp; Tách riêng Full Hàng và TikTok Shop')
html = html.replace('%FD Return Full Hàng (W39 vs W38)', '%FD Return Full Hàng (W40 vs W39)')
html = html.replace('%FD Return TikTok Shop (W39 vs W38)', '%FD Return TikTok Shop (W40 vs W39)')
html = html.replace('BẢNG 1: ĐIỀU HÀNH %FD 18 AM (FULL HÀNG vs TIKTOK SHOP — SO SÁNH W38 vs W39)',
                    'BẢNG 1: ĐIỀU HÀNH %FD 18 AM (FULL HÀNG vs TIKTOK SHOP — SO SÁNH W39 vs W40)')
html = html.replace('BẢNG 2: TOP BƯU CỤC CÓ TỶ LỆ %FD CAO NHẤT (SO SÁNH W39 vs W38)',
                    'BẢNG 2: TOP BƯU CỤC CÓ TỶ LỆ %FD CAO NHẤT (SO SÁNH W40 vs W39)')

# Tab 11: KTC
html = html.replace('BÁO CÁO ĐIỀU HÀNH KTC & VẬN TẢI — VÙNG NAM TRUNG BỘ (W39)',
                    'BÁO CÁO ĐIỀU HÀNH KTC & VẬN TẢI — VÙNG NAM TRUNG BỘ (W40)')
html = html.replace('BÁO CÁO ĐIỀU HÀNH KTC &amp; VẬN TẢI — VÙNG NAM TRUNG BỘ (W39)',
                    'BÁO CÁO ĐIỀU HÀNH KTC &amp; VẬN TẢI — VÙNG NAM TRUNG BỘ (W40)')
html = html.replace('🚚 3. Tỷ Lệ Lấp Đầy Thùng/Xe (W38 vs W39)', '🚚 3. Tỷ Lệ Lấp Đầy Thùng/Xe (W39 vs W40)')
html = html.replace('📊 Tuần (W36 vs W37)', '📊 Tuần (W39 vs W40)')
html = html.replace('W38: 51.0% → W39: 47.7% (▼ -3.3%p)', 'W39: 47.7% → W40: 48.2% (▲ +0.5%p)')

# Tab 13: COD
html = html.replace('BẢNG ĐỐI CHIẾU CÁC CHỈ SỐ COD CHÍNH (TUẦN W38 vs TUẦN W39)',
                    'BẢNG ĐỐI CHIẾU CÁC CHỈ SỐ COD CHÍNH (TUẦN W39 vs TUẦN W40)')
html = html.replace('BẢNG SO SÁNH TỶ LỆ TIỀN MẶT THEO 18 AM (TUẦN W38 vs TUẦN W39)',
                    'BẢNG SO SÁNH TỶ LỆ TIỀN MẶT THEO 18 AM (TUẦN W39 vs TUẦN W40)')
html = html.replace('Tổng COD: 80,733.6 Tr ₫ | % TM: 40.1%', 'Tổng COD: 77,502.0 Tr ₫ | % TM: 40.4%')

# Tab 14: Truy Thu
html = html.replace('BÁO CÁO TRUY THU – SO SÁNH BIẾN ĐỘNG 2 TUẦN (TUẦN W38 vs TUẦN W39)',
                    'BÁO CÁO TRUY THU – SO SÁNH BIẾN ĐỘNG 2 TUẦN (TUẦN W39 vs TUẦN W40)')
html = html.replace('BẢNG XẾP HẠNG CÁC LOẠI TRUY THU (TUẦN W38 vs TUẦN W39)',
                    'BẢNG XẾP HẠNG CÁC LOẠI TRUY THU (TUẦN W39 vs TUẦN W40)')
html = html.replace('SO SÁNH TIỀN CẦN TRUY THU THEO LOẠI VI PHẠM (TUẦN W38 vs TUẦN W39)',
                    'SO SÁNH TIỀN CẦN TRUY THU THEO LOẠI VI PHẠM (TUẦN W39 vs TUẦN W40)')
html = html.replace('Cột Xám: Tuần W38 | Cột Đỏ: Tuần W39', 'Cột Xám: Tuần W39 | Cột Đỏ: Tuần W40')
html = html.replace('SO SÁNH TRUY THU THEO 5 TỈNH THÀNH (TUẦN W38 vs TUẦN W39)',
                    'SO SÁNH TRUY THU THEO 5 TỈNH THÀNH (TUẦN W39 vs TUẦN W40)')
html = html.replace('BIỂU ĐỒ TOP 15 BƯU CỤC GIAO CẦN TRUY THU CAO NHẤT (TUẦN W38 vs TUẦN W39)',
                    'BIỂU ĐỒ TOP 15 BƯU CỤC GIAO CẦN TRUY THU CAO NHẤT (TUẦN W39 vs TUẦN W40)')
html = html.replace('Cột Xám: W38 (Tr ₫) | Cột Cam: W39 (Tr ₫)', 'Cột Xám: W39 (Tr ₫) | Cột Cam: W40 (Tr ₫)')
html = html.replace('BIỂU ĐỒ SO SÁNH TIỀN CẦN THU VÀ SỐ TICKET THEO AM (TUẦN W38 vs TUẦN W39)',
                    'BIỂU ĐỒ SO SÁNH TIỀN CẦN THU VÀ SỐ TICKET THEO AM (TUẦN W39 vs TUẦN W40)')
html = html.replace('Cột Xám: Tiền W38 | Cột Đỏ: Tiền W39 | Đường: Ticket W39',
                    'Cột Xám: Tiền W39 | Cột Đỏ: Tiền W40 | Đường: Ticket W40')
html = html.replace('BẢNG SO SÁNH TRUY THU THEO AM (TUẦN W38 vs TUẦN W39)',
                    'BẢNG SO SÁNH TRUY THU THEO AM (TUẦN W39 vs TUẦN W40)')
html = html.replace('Xếp hạng theo Tiền Cần Thu Tuần W39', 'Xếp hạng theo Tiền Cần Thu Tuần W40')

# Tab 15: Kinh Doanh
kd_summary_w39 = """              • <strong>Doanh Thu Toàn Vùng Kỳ 20–26/9 (W39):</strong> Đạt <strong>1.149,6 triệu VNĐ</strong> (Kỳ 13–19/9: 1.159,4 triệu ➔ Giảm <strong>-9,8 triệu VNĐ / -0,8% WoW</strong>).<br>
              • <strong>Tổng Volume Giao Kinh Doanh:</strong> Đạt <strong>37.046 đơn</strong> (Kỳ trước: 37.071 đơn ➔ Giảm nhẹ <strong>-25 đơn / -0,1% WoW</strong>).<br>
              • <strong>Top AM Doanh Thu Lớn Nhất:</strong> Anh Phan Đình Duy (475,7 Tr - 41,4%), chị Thái Thị Thanh Thư (110,7 Tr - 9,6%), anh Nguyễn Duy Long (96,0 Tr - 8,4%), anh Huỳnh Thúc Duân (76,0 Tr - 6,6%), anh Lê Thanh Nhựt (57,1 Tr - 5,0%), chị Hồng Bích Nga (52,7 Tr - 4,6%).<br>
              • <strong>Khách Hàng Mới (F30):</strong> Ghi nhận <strong>7 shop mới</strong> phát sinh doanh thu trong tuần (Doanh thu F30: <strong>0,20 triệu VNĐ</strong>). Kỳ trước: 121 shop (19,9 triệu VNĐ)."""

kd_summary_w40 = """              • <strong>Doanh Thu Toàn Vùng Kỳ 27/9–03/10 (W40):</strong> Đạt <strong>1.084,3 triệu VNĐ</strong> (Kỳ 20–26/9: 1.127,9 triệu ➔ Giảm <strong>-43,6 triệu VNĐ / -3,9% WoW</strong>).<br>
              • <strong>Tổng Volume Giao Kinh Doanh:</strong> Đạt <strong>34.412 đơn</strong> (Kỳ 20–26/9: 36.516 đơn ➔ Giảm <strong>-2.104 đơn / -5,8% WoW</strong>).<br>
              • <strong>Đánh Giá:</strong> Doanh thu và volume kinh doanh điều chỉnh nhẹ sau chuỗi tuần tăng trưởng cao."""

html = html.replace(kd_summary_w39, kd_summary_w40)
html = html.replace('Doanh Thu W39: 1.149,6 Tr (-0,8%) | Volume: 37.046 đ (-0,1%) | 7 Shop F30',
                    'Doanh Thu W40: 1.084,3 Tr (-3,9%) | Volume: 34.412 đ (-5,8%)')
html = html.replace('Tổng Doanh Thu Kỳ Này (20–26/9 - W39)', 'Tổng Doanh Thu Kỳ Này (27/9–03/10 - W40)')
html = html.replace('Kỳ 13–19/9 (W38) vs Kỳ 20–26/9 (W39)', 'Kỳ 20–26/9 (W39) vs Kỳ 27/9–03/10 (W40)')

# Tab 16: Bưu cục cảnh báo
html = html.replace('SO SÁNH W36 vs W37 &amp; SỐ NGÀY NẰM TRONG DANH SÁCH',
                    'SO SÁNH W39 vs W40 &amp; SỐ NGÀY NẰM TRONG DANH SÁCH')
html = html.replace('Cập nhật đồng bộ trực tiếp từ Google Sheets | Tuần W37',
                    'Cập nhật đồng bộ trực tiếp từ Google Sheets | Tuần W40')

# Table columns general pattern:
# W36, W37, W38, W39 -> W37, W38, W39, W40
html = re.sub(
    r'<th class="num">W36</th>\s*<th class="num">W37</th>\s*<th class="num">W38</th>\s*<th class="num"[^>]*>W39</th>',
    r'<th class="num">W37</th>\n                    <th class="num">W38</th>\n                    <th class="num">W39</th>\n                    <th class="num" style="background: var(--color-amber-bg); font-weight: 800; color: #ea580c;">W40</th>',
    html
)

html = re.sub(
    r'<th class="num">W35</th>\s*<th class="num">W36</th>\s*<th class="num">W37</th>\s*<th class="num"[^>]*>%GTC W39</th>',
    r'<th class="num">W37</th>\n                    <th class="num">W38</th>\n                    <th class="num">W39</th>\n                    <th class="num" style="background: var(--color-blue-bg); font-weight: 800;">%GTC W40</th>',
    html
)

html = re.sub(
    r'<th class="num">W35</th>\s*<th class="num">W36</th>\s*<th class="num">W37</th>\s*<th class="num"[^>]*>%ODR W39</th>',
    r'<th class="num">W37</th>\n                    <th class="num">W38</th>\n                    <th class="num">W39</th>\n                    <th class="num" style="background: var(--color-green-bg); font-weight: 800;">%ODR W40</th>',
    html
)

html = re.sub(
    r'<th class="num">W35</th>\s*<th class="num">W36</th>\s*<th class="num">W37</th>\s*<th class="num"[^>]*>%LTC W39</th>',
    r'<th class="num">W37</th>\n                    <th class="num">W38</th>\n                    <th class="num">W39</th>\n                    <th class="num" style="background: var(--color-blue-bg); font-weight: 800;">%LTC W40</th>',
    html
)

# Replace table single th tags
for col in ['Full', 'TTS', '%GTC', '%ODR', '%LTC', '%OPR', '% Rớt', 'FD', 'Đơn Tuần', 'Ticket', 'Cần Thu']:
    html = html.replace(f'{col} W38</th>', f'{col} W39</th>')
    html = html.replace(f'{col} W39</th>', f'{col} W40</th>')
    html = html.replace(f'{col} W37</th>', f'{col} W39</th>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Applied index.html replacements successfully!")
