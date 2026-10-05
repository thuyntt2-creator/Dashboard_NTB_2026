import os, sys, docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

sys.path.insert(0, os.path.join(os.getcwd(), 'scratch'))
from doc_builder_helpers import format_run, add_callout_box

def build_boss_script():
    doc = docx.Document()
    for s in doc.sections:
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.8)
        s.right_margin = Inches(0.8)

    # Title
    p0 = doc.add_paragraph()
    p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p0.paragraph_format.space_before = Pt(0)
    p0.paragraph_format.space_after = Pt(2)
    r0 = p0.add_run("GHN EXPRESS — VÙNG NAM TRUNG BỘ")
    format_run(r0, font_size_pt=11, bold=True, color_rgb=(0x0F, 0x4C, 0x81))

    p1 = doc.add_paragraph()
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p1.paragraph_format.space_before = Pt(2)
    p1.paragraph_format.space_after = Pt(2)
    r1 = p1.add_run("BÁO CÁO VẬN HÀNH & KINH DOANH TUẦN W40")
    format_run(r1, font_size_pt=20, bold=True, color_rgb=(0x0F, 0x4C, 0x81))

    p2 = doc.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p2.paragraph_format.space_before = Pt(0)
    p2.paragraph_format.space_after = Pt(4)
    r2 = p2.add_run("(Chu kỳ dữ liệu: 28/09/2026 – 04/10/2026)")
    format_run(r2, font_size_pt=11, italic=True, color_rgb=(0x4B, 0x55, 0x63))

    p3 = doc.add_paragraph()
    p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p3.paragraph_format.space_before = Pt(0)
    p3.paragraph_format.space_after = Pt(14)
    r3 = p3.add_run("Kịch bản điều hành trực tiếp từ Lãnh đạo Vùng — Đánh giá thực chiến 19 AM & Giao việc hiện trường")
    format_run(r3, font_size_pt=11, italic=True, color_rgb=(0xEA, 0x58, 0x0C))

    sections = [
        # TAB 1
        {
            "sec_title": "📊 [I. TỔNG HỢP TRỌNG TÂM HỌP TUẦN W40 — VÙNG NAM TRUNG BỘ]",
            "speech_title": "🗣️ LỜI MỞ ĐẦU & TỔNG QUAN ĐIỀU HÀNH VÙNG (BẬT TAB 1 DASHBOARD):",
            "speech_paragraphs": [
                "📍 1. BẢNG 10 CHỈ SỐ NHANH TRÊN MÀN HÌNH DASHBOARD (W40 vs W39):",
                "• 1. Sản Lượng Full Hàng: 311.503 đơn (-19.810 đơn / -5,98% so với W39 331.313 đơn).",
                "• 2. Sản Lượng TikTok Shop: 72.253 đơn (-1.190 đơn / -1,62%), chiếm 23,2% sản lượng vùng.",
                "• 3. %GTC Full Hàng: 60,87% (+4,19%p so với W39 56,68%) ➔ Chính thức phá vỡ mốc trần 60%!",
                "• 4. %GTC TikTok Shop: 63,38% (+5,84%p so với W39 57,54%) ➔ Lập đỉnh cao nhất từ trước đến nay.",
                "• 5. %ODR Đúng Hẹn: 93,12% (+2,28%p so với W39 90,84%) ➔ Vượt chuẩn cam kết SLA ≥ 92,0% (TTS đạt 94,18%).",
                "• 6. %LTC Lấy Hàng: 91,35% (+1,22%p so với W39 90,13%; riêng TTS đạt 94,97%).",
                "• 7. %Rớt Luân Chuyển: 1,69% (W39: 1,52%, tăng nhẹ +0,17%p; 219 đơn rớt / 12.934 đơn cần luân chuyển).",
                "• 8. %FD Hoàn Trả: 7,77% (W39: 7,54%, tăng nhẹ +0,23%p; riêng TTS kiểm soát 6,10%).",
                "• 9. Tổng Cần Truy Thu: 187,1 Tr ₫ (2.424 bản ghi, giảm -125,0 Tr ₫ so với 312,1 Tr ₫ W39).",
                "• 10. Tỷ Lệ Tiền Mặt COD: 40,4% (so với 40,1% W39; tỷ lệ chuyển khoản QR đạt 59,6%).",
                "🎙️ LỜI NÓI CỦA SẾP ĐIỀU HÀNH VÙNG (KHI MỞ TAB 1 TỔNG QUAN):",
                "\"Chào tất cả các anh chị em AM và các bộ phận vận hành.",
                "Hôm nay chúng ta ngồi lại nhìn nhận tuần W40 (chu kỳ từ 28/09 đến 04/10). Nhìn tổng thể lên màn hình Dashboard Tab 1, tuần này tôi ghi nhận sự nỗ lực rất lớn của toàn thể anh em Last-mile:",
                "Điểm sáng đầu tiên phải biểu dương: %GTC Full hàng tuần này của vùng ta đã chính thức vượt qua mốc 60%, chạm mức 60,87% (tăng hơn 4,1%p). Đặc biệt là kênh TikTok Shop, anh em kéo lên tới 63,38%, tăng gần 6%p! Điều này chứng minh khi chúng ta quyết liệt siết xuất bến ca sáng và xử lý hàng tồn, hiệu quả ra ngay.",
                "Thứ hai là chỉ số Giao đúng hẹn %ODR: Toàn vùng đã vượt ngưỡng cam kết SLA 92%, vươn lên 93,12% (TikTok Shop đạt 94,18%). First-mile lấy hàng cũng giữ vững trên 91,3%.",
                "Tuy nhiên, khen thì phải đi kèm với chấn chỉnh. Tôi yêu cầu các AM nhìn thẳng vào các ung nhọt vận hành đang bào mòn uy tín và chi phí của vùng:",
                "Thứ nhất: Sản lượng tuần này chững lại ở mức 311 ngàn đơn, giảm gần 6% so với tuần trước. Một phần do thị trường cuối tháng, nhưng phần lớn là do một số địa bàn để mất khách hàng lớn vào tay đối thủ.",
                "Thứ hai: Tỷ lệ lấp đầy xe tải KTC tụt xuống 45,6%, có tới 124 chuyến xe chạy non tải dưới 30% thùng. Chúng ta đang trả tiền tấn cho những chuyến xe chở gió!",
                "Thứ ba: Nợ truy thu dù đã đối soát giảm về 187 triệu, nhưng số phát sinh ban đầu lại vọt lên 433 triệu đồng. Nổi cộm lên vụ việc chiếm dụng 48,7 triệu tiền COD tại Bắc Cam Ranh và hơn 400 ticket dồn ứ ở Lâm Đồng. Đây là vấn đề kỷ luật và đạo đức nghề nghiệp, tôi tuyệt đối không dung thứ!",
                "Bây giờ, chúng ta bấm qua Tab 2 để đi vào mổ xẻ sản lượng từng tỉnh và từng AM!\""
            ],
            "insights": [
                "%GTC vượt 60% và ODR vượt 93% chứng minh năng lực điều hành khi toàn vùng đồng lòng siết kỷ luật.",
                "Rủi ro thất thoát từ 124 xe non tải và vụ việc chiếm dụng tiền hàng 48,7 Tr ₫ cần được xử lý dứt điểm."
            ],
            "warnings": [
                "Không để thành tích GTC che lấp các sai phạm về thất thoát quỹ và quản lý kho bãi."
            ],
            "actions": [
                "Tuần W41 tập trung 3 mũi nhọn: Xử lý dứt điểm 187,1 Tr ₫ truy thu, tối ưu 124 xe non tải và bịt lỗ rò ODR vùng cao."
            ]
        },

        # TAB 2: SẢN LƯỢNG
        {
            "sec_title": "📦 [II. PHÂN TÍCH SẢN LƯỢNG GIAO TOÀN VÙNG, 5 TỈNH THÀNH & 18 AM (W40)]",
            "speech_title": "🗣️ PHÂN TÍCH SẢN LƯỢNG GIAO 5 TỈNH & BIẾN ĐỘNG THEO 18 AM (TAB 2):",
            "speech_paragraphs": [
                "📍 1. BẢNG SỐ LIỆU 5 TỈNH THÀNH TUẦN W40 (W40 vs W39):",
                "• Khánh Hòa: 84.777 đơn Full (-10.304 đơn / -10,8% WoW) | TikTok Shop: 15.921 đơn (-2.784 đơn). Giữ vị trí số 1 sản lượng vùng.",
                "• Bình Thuận: 83.686 đơn Full (+2.869 đơn / +3,5% WoW) | TikTok Shop: 22.331 đơn (+4.185 đơn / +23,1%!). Bứt phá ngoạn mục.",
                "• Lâm Đồng: 77.719 đơn Full (-10.581 đơn / -12,0% WoW) | TikTok Shop: ~14.125 đơn.",
                "• Ninh Thuận: 33.549 đơn Full (+307 đơn / +0,9% WoW) | TikTok Shop: 11.156 đơn (+2.863 đơn / +34,5%!).",
                "• Đắk Nông: 31.772 đơn Full (-2.112 đơn / -6,2% WoW) | TikTok Shop: 8.720 đơn (-296 đơn).",
                "📍 2. BIẾN ĐỘNG THEO 18 AM:",
                "• Nhóm tăng trưởng tốt: AM Lê Thanh Nhựt (30.386 đơn, +1.316 đơn), AM Nguyễn Ngọc Khánh (27.379 đơn, +1.137 đơn), AM Cao Thị Thanh Thủy (16.786 đơn, +545 đơn), AM Nguyễn Thị Tuyết Thơ (9.296 đơn, +463 đơn), AM Nguyễn Duy Long (42.684 đơn, +178 đơn, đầu tàu gánh tải số 1 vùng).",
                "• Nhóm giảm sâu: AM Thái Thị Thanh Thư (27.165 đơn, -7.600 đơn WoW), AM Lê Văn Trường (17.707 đơn, -4.544 đơn WoW), AM Hồng Bích Nga (17.961 đơn, -2.561 đơn WoW), AM Phan Nguyễn Yến Nhi (2.433 đơn, -2.104 đơn), AM Nguyễn Thanh Long (11.220 đơn, -1.974 đơn), AM Nguyễn Lê Nguyên Vũ (10.173 đơn, -1.973 đơn).",
                "🎙️ LỜI NÓI CỦA SẾP ĐIỀU HÀNH VÙNG (KHI MỞ TAB 2 SẢN LƯỢNG):",
                "\"Các AM nhìn vào biểu đồ 5 Tỉnh ở Tab 2 giúp tôi:",
                "Tuần này thị trường chia làm 2 nửa rõ rệt giữa Duyên hải và Tây Nguyên:",
                "Bình Thuận và Ninh Thuận làm rất tốt: Trong khi toàn quốc giảm đơn cuối tháng thì Bình Thuận vẫn tăng gần 2.900 đơn Full và bùng nổ đơn sàn TikTok Shop lên hơn 22 ngàn đơn (+23%)! Ninh Thuận của anh Nhựt cũng tăng tới 34% đơn sàn. Đơn đổ về hai tỉnh này rất mạnh.",
                "Tôi biểu dương anh Duy Long: Vẫn luôn là đầu tàu gánh tải lớn nhất vùng với gần 43 ngàn đơn, và tuần này anh Long dẫn đầu toàn vùng khi kéo về hơn 22 ngàn đơn TikTok Shop cho địa bàn của mình. Anh Nhựt và anh Khánh cũng tăng trên 1.100 đến 1.300 đơn, giữ nhịp rất chắc tay.",
                "Tuy nhiên, tôi muốn chất vấn trực tiếp 2 điểm sụt giảm nghiêm trọng:",
                "Thứ nhất là chị Thư ở Khánh Hòa: Tuần trước chị tăng mạnh bao nhiêu thì tuần này tụt dốc bấy nhiêu, mất đứt 7.600 đơn (-21,8%)! Chị Thư phải rà soát lại ngay: Shop lớn nào ở Nha Trang ngưng gửi? Có phải đối thủ chào giá tốt hơn hay bưu cục phục vụ chậm trễ khiến họ cắt luồng?",
                "Thứ hai là anh Trường ở Lâm Đồng: Giảm tiếp hơn 4.500 đơn. Địa bàn của anh Trường đang dính nhiều đơn tồn và ODR thấp. Khi các anh giao trễ, khách hủy đơn thì shop họ lập tức tắt cổng GHN để chuyển qua đơn vị khác. Đó là cái giá phải trả của việc vận hành yếu kém!",
                "Hai anh chị phải ngồi lại với đội ngũ kinh doanh và CS bưu cục rà soát danh sách 20 shop lớn nhất ngay trong ngày mai. Giờ ta chuyển qua Tab 3 xem %GTC!\""
            ],
            "insights": [
                "Bình Thuận và Ninh Thuận bùng nổ đơn sàn (+23% đến +34% WoW) là cơ hội lớn để mở rộng mạng lưới giao.",
                "Khánh Hòa và Lâm Đồng giảm hơn 20 ngàn đơn cảnh báo nguy cơ mất thị phần tại các đô thị lớn."
            ],
            "warnings": [
                "AM Thư (-7.600 đơn) và AM Trường (-4.544 đơn) cần giải trình cụ thể danh sách khách hàng giảm đơn."
            ],
            "actions": [
                "AM Thư và AM Trường trực tiếp gặp các shop lớn sụt giảm sản lượng trong tuần W41."
            ]
        },

        # TAB 3: GTC TỔNG
        {
            "sec_title": "🎯 [III. PHÂN TÍCH HIỆU SUẤT %GTC TỔNG TOÀN MẠNG THEO 18 AM & 5 TỈNH (W40)]",
            "speech_title": "🗣️ ĐÁNH GIÁ TỶ LỆ GIAO THÀNH CÔNG (%GTC) VÀ ĐỘ LỆCH THEO TỈNH & AM (TAB 3):",
            "speech_paragraphs": [
                "📍 1. BẢNG %GTC TỔNG THEO 5 TỈNH THÀNH (W40 vs W39):",
                "• Ninh Thuận: 67,49% (W39: 67,96%) ➔ Duy trì vị trí số 1 toàn vùng, tỷ lệ giao cực kỳ ổn định.",
                "• Bình Thuận: 67,45% (W39: 67,49%) ➔ Bám sát vị trí dẫn đầu, giữ phong độ bền bỉ.",
                "• Khánh Hòa: 62,23% (W39: 58,82%, tăng +3,41%p) ➔ Bứt phá qua mốc 60%, đóng góp lớn vào vùng.",
                "• Lâm Đồng: 54,42% (W39: 47,39%, tăng bùng nổ +7,03%p!) ➔ Nỗ lực thoát đáy ngoạn mục.",
                "• Đắk Nông: 54,40% (W39: 48,72%, tăng mạnh +5,68%p!) ➔ Phục hồi mạnh mẽ.",
                "• Toàn vùng: 60,87% (+4,19%p so với W39 56,68%) | Riêng TikTok Shop: 63,38% (+5,84%p) ➔ Lập đỉnh cao nhất từ trước đến nay!",
                "📍 2. XẾP HẠNG 18 AM — TOP 1 GTC VÀ NHÂN TỐ TĂNG TRƯỞNG:",
                "• 🥇 Quán quân %GTC toàn vùng: AM Nguyễn Ngọc Khánh đạt 74,51% (Top 1 toàn vùng Nam Trung Bộ).",
                "• 🥈 Á quân %GTC: AM Thái Thị Thanh Thư (Khánh Hòa) đạt 72,02% (bứt phá +9,63%p trên gần 36k đơn).",
                "• 🥉 Top 3: AM Nguyễn Đỗ Minh Nghĩa (Lâm Đồng) đạt 70,42% (+0,26%p).",
                "• 👑 Đầu tàu gánh tải: AM Nguyễn Duy Long tiếp tục gánh sản lượng lớn nhất toàn vùng (hơn 42k đơn Full, gần 19k đơn TTS), duy trì %GTC vững vàng ở mức 68,95% (W39: 69,04%)!",
                "• 🚀 3 AM KÉO BÙNG NỔ TĂNG TRƯỞNG VÙNG (+4,19%p):",
                "  1. AM Lê Văn Trường (Lâm Đồng): Tăng phi thường +11,85%p (từ 37,14% lên 48,99%) trên khối lượng cực lớn 37,4k đơn!",
                "  2. AM Thái Thị Thanh Thư (Khánh Hòa): Tăng vọt +9,63%p (từ 62,39% lên 72,02%) trên 35,9k đơn!",
                "  3. AM Trương Quang Linh (Đắk Nông): Tăng bứt phá mạnh nhất toàn vùng với +14,49%p (từ 25,78% lên 40,27%)!",
                "  (Bên cạnh đó: AM Vũ +7,5%p, AM Nhi +9,0%p, AM Nhung +3,5%p trên 37k đơn kéo cả khu vực Tây Nguyên thoát đáy).",
                "• ⚠️ Nhóm AM vẫn còn dưới 50% GTC: Lê Minh Lợi (36,5%), Phan Nguyễn Yến Nhi (38,0%), Trương Quang Linh (40,3%), Huỳnh Thúc Duân (44,6%), Nguyễn Lê Nguyên Vũ (45,8%), Lê Văn Trường (49,0%).",
                "🎙️ LỜI NÓI CỦA SẾP ĐIỀU HÀNH VÙNG (KHI MỞ TAB 3 %GTC TỔNG):",
                "\"Các anh chị nhìn lên bảng 5 Tỉnh ở Tab 3:",
                "Bình Thuận vẫn giữ vững GTC 67,5%, anh em chạy tuyến rất đều và khách nhận hàng chuẩn chỉ. Khánh Hòa và Ninh Thuận tuần này đã xuất sắc vượt qua mốc 60%. Đặc biệt Khánh Hòa tăng từ 58,8% lên 62,2%, đóng góp cực lớn vào tỷ lệ GTC chung của vùng.",
                "Hai tỉnh Đắk Nông và Lâm Đồng: Dù vẫn đứng ở 2 vị trí cuối bảng với 54,4%, nhưng tuần này anh em đã có sự nỗ lực rất lớn. Lâm Đồng kéo tăng hơn 7%p, Đắk Nông tăng 5,7%p so với tuần trước. Tôi ghi nhận và tuyên dương sự chuyển biến này của các AM khu vực 2 tỉnh.",
                "Nhìn xuống danh sách 18 AM bên dưới:",
                "Quán quân GTC tuần này thuộc về khu vực anh Nguyễn Ngọc Khánh đạt 74,5%, kế đến là chị Thái Thị Thanh Thư đạt 72,0% và anh Nguyễn Đỗ Minh Nghĩa đạt 70,4%.",
                "Đặc biệt, anh Duy Long tiếp tục gánh khối lượng lớn nhất vùng nhưng vẫn giữ %GTC rất vững vàng ở mức gần 69%. Đây là phong độ của người làm chủ địa bàn.",
                "Và các anh chị phải thấy rõ: Tuần này toàn vùng tăng mạnh hơn 4,1%p KHÔNG PHẢI nhờ nhóm ven biển (vì Bình Thuận và Ninh Thuận đã ở mức trần nên đi ngang ~67,5%), mà công lớn nhất kéo cả vùng bứt phá tuần này thuộc về 3 AM có bước nhảy vọt thần tốc:",
                "Thứ nhất là chị Thư ở Khánh Hòa: Tăng vọt tới gần +10%p (từ 62,4% lên 72,0%) trên khối lượng gần 36 ngàn đơn, kéo bừng sáng cả tỉnh Khánh Hòa!",
                "Thứ hai là anh Lê Văn Trường ở Lâm Đồng: Tăng phi thường gần +12%p (từ 37,1% lên 49,0%) trên khối lượng cực lớn hơn 37 ngàn đơn! Chính anh Trường là đầu tàu kéo Lâm Đồng tăng hơn 7%p tuần này!",
                "Thứ ba là anh Trương Quang Linh ở Đắk Nông: Tăng bứt phá mạnh nhất toàn vùng với +14,5%p (từ 25,8% lên 40,3%). Bên cạnh đó, anh Vũ, chị Nhi và chị Nhung cũng là những nhân tố nòng cốt kéo toàn bộ khu vực Tây Nguyên thoát đáy!",
                "Tuy nhiên, tôi lưu ý các AM nhóm dưới: Anh Lợi (36,5%), chị Nhi (38,0%), anh Linh (40,3%), anh Duân (44,6%), anh Vũ (45,8%) và anh Trường (49,0%): Dù các anh chị có tiến bộ, nhưng điểm tuyệt đối vẫn đang nằm dưới 50%! Cứ giao 2 đơn là mất 1 đơn chưa thành công. Bưu tá vẫn còn lười đi ca chiều, shipper chưa chịu gọi lại cho khách.",
                "Tuần này các anh chị phải ngồi lại với từng bưu cục để tối ưu lại ca phát chiều, kéo dứt điểm toàn bộ lên trên 55%! Giờ ta qua Tab 4 xem Ca 1 TikTok Shop!\""
            ],
            "insights": [
                "Tăng trưởng GTC tuần W40 (+4,19%p toàn vùng) chủ yếu đến từ sự bứt phá của AM Lê Văn Trường (+11,85%p) và AM Thái Thị Thanh Thư (+9,63%p).",
                "Kênh TikTok Shop đạt đỉnh 63,38% GTC chứng minh tiềm năng giao thành công của hàng sàn cao hơn hàng ngoài nếu giao nhanh."
            ],
            "warnings": [
                "6 AM (Lợi, Nhi, Linh, Duân, Trường, Vũ) vẫn chìm dưới 50% GTC, là nơi phát sinh phần lớn hàng tồn bưu cục."
            ],
            "actions": [
                "Các AM nhóm dưới rà soát lộ trình di chuyển của bưu tá, bắt buộc gán phát chuyến 2 đối với các đơn chưa liên lạc được buổi sáng."
            ]
        },

        # TAB 4: GTC CA 1 TTS
        {
            "sec_title": "🔥 [IV. PHÂN TÍCH CHUYÊN SÂU %GTC CA 1 TIKTOK SHOP (TARGET SLA ≥ 76.0%) (W40)]",
            "speech_title": "🗣️ HIỆU SUẤT GIAO CA 1 TIKTOK SHOP (81.34% VƯỢT SLA 76%) & 19 AM (TAB 4):",
            "speech_paragraphs": [
                "📍 1. HIỆU SUẤT TOÀN VÙNG VÀ BẢNG 5 TỈNH THÀNH (W40 vs W39):",
                "• Toàn vùng TTS Ca 1: Bứt phá ngoạn mục đạt 81,34% (tăng mạnh +6,17%p WoW so với W39: 75,16%) ➔ Vượt xa Target cam kết SLA ≥ 76.0%!",
                "• Bình Thuận: 86,45% (+1,81%p) | Ninh Thuận: 83,78% | Lâm Đồng: 80,22% (+13,37%p!) | Khánh Hòa: 80,15% (+4,37%p) ➔ 4/5 tỉnh vượt 80%!",
                "• Đắk Nông: 72,78% (W39: 67,81%, tăng mạnh +4,97%p).",
                "📍 2. XẾP HẠNG 19 AM THEO %GTC CA 1 TIKTOK SHOP (TARGET SLA ≥ 76.0%):",
                "• 14/19 AM xuất sắc đạt và vượt Target SLA ≥ 76.0%.",
                "• Top 5 dẫn đầu: 🥇 Nguyễn Ngọc Khánh (88,94%), 🥈 Nguyễn Đỗ Minh Nghĩa (87,02%), 🥉 Cao Thị Thanh Thủy (87,01%), 👑 Nguyễn Duy Long (85,05% — gánh 10.257 đơn Ca 1), 5️⃣ Nguyễn Thị Tuyết Thơ (83,20%).",
                "• Top tăng trưởng ngoạn mục: 🚀 Lê Văn Trường tăng vọt +24,72%p (từ 55,56% lên 80,28%!), 🚀 Trương Quang Linh (+18,94%p), 🚀 Phan Nguyễn Yến Nhi (+16,65%p), 🚀 Nguyễn Thanh Long (+16,40%p, lên 82,98%).",
                "• Nhóm 5 AM chưa đạt Target SLA 76%: Huỳnh Thúc Duân (64,52%), Nguyễn Lê Nguyên Vũ (61,43%), Phan Nguyễn Yến Nhi (58,62%), Trương Quang Linh (58,14%), Lê Minh Lợi (46,67%).",
                "🎙️ LỜI NÓI CỦA SẾP ĐIỀU HÀNH VÙNG (KHI MỞ TAB 4 CA 1 TTS):",
                "\"Các AM nhìn vào Tab 4: Đây là chỉ số mà sàn TikTok Shop họ theo dõi sát sao từng giờ:",
                "Tuần W40 này chúng ta làm rất tốt ở khâu xuất phát sáng: Hiệu suất giao Ca 1 TikTok Shop của toàn vùng đạt tới 81,34%, tăng hơn 6%p và chính thức vượt xa cam kết SLA 76%! Cả 4 trên 5 tỉnh gồm Bình Thuận, Ninh Thuận, Lâm Đồng và Khánh Hòa đều đã xuất sắc kéo GTC Ca 1 vượt qua mốc 80%.",
                "Nhìn vào 19 AM bên dưới, có 14 anh chị đã đạt chuẩn xanh trên 76%. Anh Khánh đạt gần 89%, anh Nghĩa 87%, chị Thủy 87%. Đặc biệt anh Duy Long gánh khối lượng khổng lồ hơn 10 ngàn đơn Ca 1 mà vẫn giữ tỷ lệ 85%!",
                "Tôi biểu dương anh Lê Văn Trường ở Lâm Đồng: Cú lội ngược dòng tăng gần +25%p (từ 55,6% nhảy vọt lên 80,3%), đưa địa bàn Đà Lạt từ điểm nóng báo động trở thành điểm đạt chuẩn SLA!",
                "TUY NHIÊN, TÔI BÓC TRẦN BẢN CHẤT HIỆN TRƯỜNG ĐỂ CÁC AM KHÔNG ĐƯỢC CHỦ QUAN:",
                "Trên biểu đồ này là GTC Ca 1 THUẦN (hàng mới về sáng sớm) đạt 81,34%. Nhưng nếu tính cả ĐƠN TỒN thì tỷ lệ thành công lập tức tụt xuống còn 66,47% — chênh lệch nhau tới gần 15%p!",
                "Tại sao lại như vậy? Vì shipper sáng ra bốc hàng vẫn có thói quen khôn lỏi: Lựa kiện hàng mới tinh để giao trước cho nhanh được việc. Còn đơn tồn hôm trước dồn lại thì nhét dưới đáy giỏ hoặc vứt lại góc bưu cục. Hàng tồn càng để lâu khách càng đổi ý không lấy!",
                "Còn 5 AM đang hiển thị màu đỏ dưới 76%: Anh Duân (64,5%), anh Vũ (61,4%), chị Nhi (58,6%), anh Linh (58,1%) và anh Lợi (46,7%):",
                "Tôi yêu cầu 5 AM này: Sáng mai xuống ngay bưu cục kiểm tra sọt hàng bưu tá lúc 8h30. Bắt buộc 100% đơn tồn hôm qua phải xếp lên trên mặt giỏ để đi phát trước 10h30, không được găm hàng lại bưu cục! Giờ ta chuyển qua Tab 5 xem Tỷ lệ gán!\""
            ],
            "insights": [
                "GTC Ca 1 TikTok Shop đạt kỷ lục 81,34% đưa toàn vùng vượt qua cam kết SLA ≥ 76.0%.",
                "Khoảng cách 14,87%p giữa Ca 1 thuần và Ca 1 có tồn là bằng chứng cho thấy bưu tá đang né tránh giao hàng tồn vào buổi sáng."
            ],
            "warnings": [
                "5 AM (Duân, Vũ, Nhi, Linh, Lợi) dưới ngưỡng 76% làm tăng tỷ lệ khiếu nại của khách hàng sàn TMĐT."
            ],
            "actions": [
                "Cửa hàng trưởng kiểm tra sọt hàng bưu tá trước 8h30 sáng: Đơn tồn hôm trước phải được mang đi phát trong chuyến 1."
            ]
        },

        # TAB 5: TỶ LỆ GÁN
        {
            "sec_title": "📋 [V. TỶ LỆ GÁN VẬN HÀNH TOÀN MẠNG THEO CA 1, CA 2 & GÁN TỔNG (TARGET ≥ 90.0%) (W40)]",
            "speech_title": "🗣️ TỶ LỆ GÁN VẬN HÀNH: CA 1+TỒN (92.8%) VS GÁN TỔNG CẢ NGÀY (86.3%) (TAB 5):",
            "speech_paragraphs": [
                "📍 1. BẢNG 1 CHỈ TIÊU VÙNG NTB (W40 vs W39):",
                "• Gán Tổng Cả Ngày: Full hàng đạt 86,32% (W39: 82,47%, tăng +3,86%p) | Riêng TikTok Shop đạt 88,00% (W39: 82,83%, tăng +5,17%p).",
                "• Gán Ca 1 + Tồn (Xuất sáng): Full hàng đạt 92,77% (W39: 87,46%, tăng +5,32%p) | TTS đạt 94,80% (tăng +6,58%p) ➔ Vượt chuẩn xanh ≥ 90%!",
                "• Gán Ca 2 (Xuất chiều): Full hàng đạt 62,87% (+3,59%p) | TTS đạt 63,54% (+4,98%p) ➔ Điểm nghẽn làm chậm dòng chảy hàng hóa.",
                "📍 2. BẢNG 2 XẾP HẠNG AM THEO GÁN CA 1 + TỒN (TARGET ≥ 90%):",
                "• Top dẫn đầu phong độ xuất sắc (>97% - 99%): Nguyễn Đỗ Minh Nghĩa (99,05%), Nguyễn Ngọc Khánh (98,94%), Lê Thanh Nhựt (98,92%), Thái Thị Thanh Thư (98,41%), Cao Thị Thanh Thủy (98,02%), Nguyễn Duy Long (97,00%).",
                "• Top bứt phá tăng gán sáng ngoạn mục (Δ WoW): Phan Nguyễn Yến Nhi (+22,29%p, lên 82,52%), Lê Văn Trường (+21,50%p, lên 83,35%), Trương Quang Linh (+21,62%p, lên 79,98%), Nguyễn Lê Nguyên Vũ (+9,21%p, lên 77,51%).",
                "• Nhóm hụt gán sáng cần chấn chỉnh: Huỳnh Thúc Duân (84,71%, giảm -1,11%p), Nguyễn Thanh Long (85,79%), Huỳnh Thị Kim Chi (87,34%).",
                "📍 3. BẢNG 3 XẾP HẠNG AM THEO GÁN TỔNG CẢ NGÀY:",
                "• Đạt chuẩn ≥90%: Thái Thị Thanh Thư (97,46%), Nguyễn Ngọc Khánh (92,67%), Nguyễn Hoàng Phi (92,17%), Nguyễn Duy Long (91,60%), Nguyễn Thị Tuyết Thơ (91,59%), Nguyễn Đỗ Minh Nghĩa (91,17%), Cao Thị Thanh Thủy (90,65%).",
                "• Nhóm chưa đạt 80% gán tổng: Huỳnh Thúc Duân (75,46%), Lê Văn Trường (75,88%), Huỳnh Thị Kim Chi (77,62%), Lê Minh Lợi (78,19%), Nguyễn Thanh Long (79,71%), Trương Quang Linh (79,99%).",
                "🎙️ LỜI NÓI CỦA SẾP ĐIỀU HÀNH VÙNG (KHI MỞ TAB 5 % GÁN):",
                "\"Các anh chị nhìn sang Tab 5 về Tỷ lệ Gán vận hành giúp tôi:",
                "Nhìn vào Bảng 1, tuần này tỷ lệ gán Ca 1 + Tồn của vùng mình rất tốt: Full hàng đạt 92,8% và TikTok Shop đạt 94,8%. Tức là buổi sáng hàng về kho cơ bản các anh chị đã thúc bưu tá gán ra đường trước 8h30.",
                "Nhìn vào Bảng 2, tôi biểu dương chị Yến Nhi và anh Linh tăng hơn 22%p, anh Trường tăng hơn 21%p gán sáng. Tuần trước các anh chị chỉ gán được 60% thì tuần này đã kéo lên trên 80% - 83%.",
                "NHƯNG TÔI YÊU CẦU CÁC ANH CHỊ NHÌN XUỐNG BẢNG 3 (GÁN TỔNG CẢ NGÀY) VÀ CHỈ SỐ GÁN CA 2:",
                "Tại sao sáng gán được gần 93% mà tính chung cả ngày chỉ đạt 86,3%? Bởi vì tỷ lệ gán Ca 2 (chuyến chiều) của các anh chị chỉ đạt vỏn vẹn 62,9%!",
                "Cứ 100 đơn hàng chuyến xe trưa KTC chở về bưu cục, thì có tới gần 38 đơn bị 'ém' lại ở sàn kho, không thèm gán cho bưu tá mang đi phát!",
                "Anh Duân (75,5%), chị Chi (77,6%), anh Lợi (78,2%), anh Thanh Long (79,7%), anh Trường (75,9%) giải thích cho tôi xem: Tại sao hàng về kho mà không cho bưu tá mang đi giao?",
                "Tôi nói thẳng luôn lý do hiện trường: Khung giờ 12h30 đến 13h30 xe tải về, nhân viên kho bưu cục nghỉ ăn trưa. Đến 14h00 bưu tá chuẩn bị xuất tuyến ca chiều thì hàng trưa vẫn nằm nguyên trong bao tải chưa bắn phân tuyến. Bưu tá không có hàng mới để đi, chỉ cầm vài đơn hẹn sáng rồi lượn lờ về sớm lúc 16h30!",
                "Trong khi đó, từ 16h30 đến 18h30 là 'khung giờ vàng' người dân đi làm về nhà nhận hàng nhiều nhất thì bưu tá của các anh chị lại không có trên tuyến! Hàng ca trưa không giao biến thành hàng tồn ngày mai, làm sàn bưu cục lúc nào cũng chật như nêm cối!",
                "Tôi ra lệnh cho các AM nhóm dưới: Ngay trong tuần này, tất cả bưu cục phải sắp xếp 1 nhân sự trực trưa từ 13h00 bắn phân loại hàng ngay khi xe KTC hạ tải. Đúng 14h00 bưu tá có đủ hàng xuất tuyến Ca 2. Tôi sẽ kiểm tra hệ thống lúc 14h15 hàng ngày, AM nào để bưu cục gán Ca 2 dưới 75% thì chuẩn bị giải trình với tôi! Giờ ta chuyển qua Tab 6 ODR!\""
            ],
            "insights": [
                "Gán Ca 1 + Tồn đạt 92,77% chứng minh quy trình xuất bến ca sáng đã vào guồng.",
                "Gán Ca 2 chỉ đạt 62,87% là điểm nghẽn cơ học khiến gần 38% hàng chuyến trưa bị dồn ứ tại bưu cục."
            ],
            "warnings": [
                "Không gán ca chiều đồng nghĩa với việc bỏ lỡ khung giờ vàng nhận hàng 16h30 - 18h30 của khách hàng đô thị."
            ],
            "actions": [
                "Bưu cục bố trí nhân sự trực trưa lúc 13h00; AM kiểm tra tỷ lệ gán Ca 2 trên hệ thống lúc 14h15 hàng ngày, yêu cầu đạt tối thiểu 75%."
            ]
        },

        # TAB 6: ODR
        {
            "sec_title": "⏱️ [VI. PHÂN TÍCH HIỆU SUẤT %ODR (GIAO ĐÚNG HẸN SLA) TOÀN VÙNG (TARGET ≥ 92.0%) (W40)]",
            "speech_title": "🗣️ CHẤT LƯỢNG GIAO ĐÚNG HẸN %ODR: 5 TỈNH LÊN ĐẦU & ĐÁNH GIÁ 18 AM (TAB 6):",
            "speech_paragraphs": [
                "📍 1. BẢNG 1 & 2 %ODR GIAO ĐÚNG HẸN 5 TỈNH THÀNH (W40 vs W39):",
                "• Bình Thuận: 96,74% Full | 96,69% TTS (W39: 96,27%) ➔ Dẫn đầu toàn vùng, phong độ đỉnh cao.",
                "• Khánh Hòa: 95,59% Full | 95,95% TTS (W39: 91,94%, bứt phá +3,65%p) ➔ Vượt chuẩn xuất sắc.",
                "• Ninh Thuận: 94,20% Full | 95,48% TTS (W39: 92,80%) ➔ An toàn, đạt chuẩn SLA.",
                "• Đắk Nông: 90,42% Full | 87,48% TTS (chưa đạt SLA).",
                "• Lâm Đồng: 87,79% Full | 85,91% TTS (chưa đạt SLA).",
                "• Toàn vùng: Full hàng đạt 93,12% (+2,28%p) | TikTok Shop đạt 94,18% (+2,41%p) ➔ ĐẠT CHUẨN SLA TOÀN VÙNG!",
                "📍 2. BẢNG 3 & 4 PHÂN HÓA 2 THÁI CỰC THEO 18 AM:",
                "• Nhóm dẫn đầu giữ chuẩn ODR xuất sắc trên 96% - 97%: Chị Cao Thị Thanh Thủy (97,8% Full | 97,6% TTS), anh Nguyễn Ngọc Khánh (97,4% Full | 98,2% TTS), chị Thái Thị Thanh Thư (96,9%), anh Nguyễn Duy Long (96,6% Full | 97,2% TTS trên gần 13k đơn GTC), anh Nguyễn Hoàng Phi (96,6%).",
                "• Bứt phá tiến bộ: Chị Phan Nguyễn Yến Nhi (+8,76%p lên 76,1%), anh Nguyễn Thanh Long (+8,20%p lên 92,3%), anh Nguyễn Lê Nguyên Vũ (+6,79%p lên 87,2%).",
                "• 🔴 BÁO ĐỘNG ĐỎ — TỬ HUYỆT ODR TIKTOK SHOP VÙNG CAO (BẢNG 4 DB):",
                "  1. Lê Văn Trường: 62,13% (rơi tự do -17,39%p WoW).",
                "  2. Phan Nguyễn Yến Nhi: 44,57% (rơi tự do -22,39%p WoW).",
                "  3. Trương Quang Linh: 42,00% (rơi tự do -33,99%p WoW).",
                "  4. Lê Minh Lợi: 14,29% (rơi -27,24%p WoW).",
                "🎙️ LỜI NÓI CỦA SẾP ĐIỀU HÀNH VÙNG (KHI MỞ TAB 6 ODR):",
                "\"Các anh chị nhìn vào Tab 6 ODR — Chỉ số sinh mạng để giữ hợp đồng với các sàn TMĐT:",
                "Nhìn Bảng 1 và Bảng 2, toàn vùng đạt 93,12% Full và 94,18% TikTok Shop, cơ bản là đạt chuẩn SLA 92% của công ty. Nhóm Duyên hải chị Thủy (97,8%), anh Khánh (97,4%), anh Long (96,6%), chị Thư (96,9%) làm rất đều tay, tôi ghi nhận.",
                "NHƯNG TÔI YÊU CẦU TẤT CẢ CÁC AM NHÌN NGAY VÀO BẢNG 4 (ODR TIKTOK SHOP CỦA CÁC AM):",
                "Trong khi toàn vùng đạt 94%, thì tại 4 cụm Tây Nguyên, ODR TikTok Shop đang rơi tự do xuống đáy vực:",
                "Anh Lê Văn Trường tụt xuống 62,1% (rơi -17,4%p)! Chị Phan Nguyễn Yến Nhi tụt xuống 44,6% (rơi -22,4%p)! Anh Trương Quang Linh tụt xuống 42,0% (rơi -34,0%p)! Và anh Lê Minh Lợi tụt xuống mức không tưởng là 14,3%!",
                "Các anh chị làm ăn kiểu gì mà để ODR rớt thảm hại như thế này? Các anh chị có biết đơn sàn TikTok cam kết giao trong 48h không? Các shop họ phụ thuộc vào từng giờ giao hàng, ODR dưới 80% là sàn phạt gậy, khách bấm hủy đơn!",
                "Tôi chỉ thẳng nguyên nhân: Các bưu cục Quảng Tín, Đơn Dương, Lang Biang địa bàn rộng đồi dốc, bưu tá ngại đi tuyến xa nên dồn hàng 2-3 ngày mới đi gom phát một chuyến! Bưu tá lười đi, để đơn ngâm ở kho quá 48h thì hệ thống sàn nó tự động quét lỗi trễ hẹn hàng loạt chứ có oan ức gì đâu!",
                "Tôi ra chỉ thị cho anh Trường, chị Nhi, anh Linh, anh Lợi: Ngay ngày mai, bật tính năng cảnh báo 'Đơn cận SLA' trên app bưu tá. Đơn nào còn dưới 12 tiếng hết hạn là bắt buộc bưu tá phải mang đi phát ngay chuyến đầu sáng, cấm tuyệt đối việc dồn đơn sang ngày hôm sau. Tuần W41 ODR TikTok Shop của 4 AM này phải kéo lên trên 75% cho tôi! Giờ ta chuyển qua Tab 8 OPR!\""
            ],
            "insights": [
                "Khối Duyên hải duy trì ODR trên 96% - 97% là chốt chặn bảo vệ uy tín thương hiệu GHN.",
                "ODR TikTok Shop tại 4 AM Tây Nguyên rơi xuống 14% - 62% do bưu tá dồn tuyến gom đơn 2-3 ngày mới đi phát một lần."
            ],
            "warnings": [
                "Sàn TikTok Shop tự động phạt gậy vi phạm và cắt luồng đơn các shop có tỷ lệ ODR dưới 80%."
            ],
            "actions": [
                "Cài đặt cảnh báo đơn cận hạn SLA 12h trên app bưu tá; bưu tá tuyến huyện bắt buộc gọi điện hẹn giờ với người nhận trước khi xuất phát."
            ]
        },

        # TAB 7: LTC
        {
            "sec_title": "🚚 [VII. PHÂN TÍCH CHỈ SỐ %LTC (LẤY THÀNH CÔNG) THEO 18 AM & 5 TỈNH (TARGET ≥ 90.0%) (W40)]",
            "speech_title": "🗣️ PHONG ĐỘ FIRST-MILE: %LTC TOÀN VÙNG ĐẠT 91.35% (TTS ĐẠT 94.97%) (TAB 7):",
            "speech_paragraphs": [
                "📍 1. BẢNG CHỈ SỐ %LTC THEO 5 TỈNH THÀNH (W40 vs W39):",
                "• Ninh Thuận: 97,58% (W39: 96,10%, tăng +1,48%p) ➔ Dẫn đầu tuyệt đối về tỷ lệ lấy hàng thành công.",
                "• Khánh Hòa: 94,80% (W39: 93,50%, tăng +1,30%p) ➔ Phong độ rất vững vàng.",
                "• Lâm Đồng: 92,10% (W39: 90,80%, tăng +1,30%p) ➔ Khâu lấy hàng rau hoa, nông sản cải thiện rõ rệt.",
                "• Đắk Nông: 91,15% (W39: 87,79%, tăng mạnh +3,36%p) ➔ Chính thức vượt mốc 90%.",
                "• Bình Thuận: 89,82% (W39: 86,26%, tăng mạnh +3,56%p) ➔ Tiệm cận mục tiêu 90%.",
                "• Toàn vùng: Full hàng đạt 91,35% (+1,22%p) | TikTok Shop đạt 94,97% (+0,39%p).",
                "📍 2. ĐÁNH GIÁ 18 AM:",
                "• 15 trên 18 AM đã hoàn thành xuất sắc chỉ tiêu %LTC ≥ 90%. Top đầu: AM Lê Thanh Nhựt (98,1%), AM Nguyễn Đỗ Minh Nghĩa (97,0%), AM Cao Thị Thanh Thủy (96,8%).",
                "• 3 AM cần lưu ý: AM Trầm Hữu Tiến (88,9%), AM Trương Quang Linh (89,2%), AM Nguyễn Thị Tuyết Thơ (89,4%) — còn để rớt đơn lấy do shop hẹn lấy lại vào ngày hôm sau.",
                "🎙️ LỜI NÓI CỦA SẾP ĐIỀU HÀNH VÙNG (KHI MỞ TAB 7 LTC):",
                "\"Qua Tab 7 Lấy hàng First-mile:",
                "Toàn vùng tuần này tiếp tục duy trì phong độ lấy hàng rất cao, đạt 91,35% với Full hàng và gần 95% với đơn TikTok Shop. 15 trên 18 AM đã đạt chuẩn trên 90%.",
                "Tôi khen anh Nhựt với anh Nghĩa ở Ninh Thuận lấy hàng đạt đỉnh 97,6%. Anh em shipper Ninh Thuận kết nối với các shop bán nho, tỏi, hải sản rất thân thiết, nhận đơn lấy là có mặt gom hàng ngay trong vòng 2 tiếng. Đắk Nông và Bình Thuận tuần này cũng tăng hơn 3,5%p, đưa tỷ lệ lấy hàng của vùng lên mức an toàn.",
                "Điểm cần lưu ý: Tại các huyện miền núi của Lâm Đồng và Đắk Nông, một số shop nông sản đóng hàng muộn sau 17h00. Shipper bưu cục huyện ngại chạy xa vào rẫy nên xin shop dời sang sáng mai lấy.",
                "Việc dời đơn lấy này rất nguy hiểm với đơn TikTok Shop vì sàn tính giờ bàn giao (Handover SLA) rất ngặt. Anh Tiến và anh Linh bố trí xe tải nhỏ hoặc shipper chuyên trách gom hàng chiều muộn cho các shop lớn giúp tôi! Giờ ta qua Tab 8 OPR TikTok Shop!\""
            ],
            "insights": [
                "Khâu lấy hàng First-mile duy trì trên 91% là nền tảng vững chắc giúp GHN giữ vững thị phần trước các đối thủ.",
                "Mô hình shipper phụ trách shop ruột tại Ninh Thuận đạt 97,58% cần được nhân rộng ra các tỉnh khác."
            ],
            "warnings": [
                "Shop TikTok Shop nếu bị hoãn lấy hàng qua đêm sẽ bị hệ thống sàn tính trễ hạn lấy, dẫn đến nguy cơ shop chuyển sang đơn vị khác."
            ],
            "actions": [
                "Bố trí tuyến xe gom cố định sau 16h30 tại các vùng tập trung nhiều shop online để lấy dứt điểm đơn trước 18h30."
            ]
        },

        # TAB 8: OPR TTS
        {
            "sec_title": "🌙 [VIII. PHÂN TÍCH CHỈ SỐ %OPR TIKTOK SHOP TOÀN VÙNG (TARGET KPI ≥ 80.0%) (W40)]",
            "speech_title": "🗣️ HIỆU SUẤT %OPR TIKTOK SHOP: CA NGÀY (88-99%) VS CA ĐÊM (0-36%) (TAB 8):",
            "speech_paragraphs": [
                "📍 1. BẢNG 1 CA NGÀY (9H - 19H) — PHONG ĐỘ XUẤT SẮC TOÀN VÙNG:",
                "• Toàn vùng kiểm soát rất tốt từ 88% đến 99%: Khánh Hòa đạt 94,10%, Lâm Đồng 89,58%, Bình Thuận 88,05%.",
                "• Top AM xử lý ban ngày chuẩn mực: Phan Đình Duy (99,05%), Nguyễn Lê Nguyên Vũ (99,13%), Nguyễn Thị Tuyết Thơ (98,79%), Nguyễn Duy Long (97,27%), Nguyễn Ngọc Khánh (95,01%, tăng bứt phá +15,10%p).",
                "📍 2. BẢNG 2 CA ĐÊM (19H - 9H SÁNG HÔM SAU) — NÚT THẮT LÀM GÃY CHỈ SỐ:",
                "• Tỷ lệ xử lý ca đêm sụt giảm nghiêm trọng tại các cụm lớn:",
                "  - Huỳnh Thúc Duân: 0,00% (0/63 đơn xử lý kịp giờ).",
                "  - Trần Thị Nhung: 0,74% (chỉ có 1/131 đơn kịp giờ).",
                "  - Lê Văn Trường: 24,03% (dính tới 371/488 đơn trễ giờ đêm).",
                "  - Nguyễn Đỗ Minh Nghĩa: 25,44%.",
                "  - Nguyễn Hoàng Phi: 34,52% (525 đơn đêm).",
                "  - Lê Thanh Nhựt: 36,59% (960 đơn đêm).",
                "🎙️ LỜI NÓI CỦA SẾP ĐIỀU HÀNH VÙNG (KHI MỞ TAB 8 OPR TTS):",
                "\"Các AM nhìn sang Tab 8 OPR TikTok Shop — Tỷ lệ xử lý đơn đúng cam kết theo khung giờ tạo đơn của sàn:",
                "Mọi người nhìn vào sự tương phản một trời một vực giữa Ca Ngày và Ca Đêm trên màn hình giúp tôi:",
                "Ở Bảng 1 (Ca ngày 9h - 19h), anh em làm rất tốt: Toàn bộ đều xanh mướt trên 95% - 99%. Anh Duy đạt 99,0%, anh Vũ 99,1%, chị Thơ 98,8%, anh Long 97,3%, anh Khánh vọt lên 95,0%. Ban ngày quy trình bắn in bill và bàn giao rất mượt mà.",
                "THẾ NHƯNG KHI BẬT SANG BẢNG 2 (CA ĐÊM TỪ 19H TỐI ĐẾN 9H SÁNG HÔM SAU):",
                "Biểu đồ ca đêm đang báo động đỏ rực toàn vùng:",
                "Anh Huỳnh Thúc Duân đạt 0,00% (0 trên 63 đơn kịp giờ)! Chị Trần Thị Nhung đạt 0,74% (chỉ có 1 trên 131 đơn kịp giờ)! Anh Lê Văn Trường đạt 24,0% (dính tới 371 đơn trễ giờ đêm)! Anh Nghĩa 25,4%! Anh Phi 34,5%!",
                "Tôi hỏi các anh chị: Ban ngày làm được mà tại sao ban đêm lại gãy hoàn toàn như thế này?",
                "Bản chất hiện trường là gì? Khách lướt livestream đặt hàng nhiều nhất là từ 20h đến 23h đêm. Theo chuẩn SLA của sàn, sáng hôm sau bưu cục phải quét in bill xong trước 9h00 sáng.",
                "Nhưng 18h30 nhân viên bưu cục tắt máy khóa cửa đi về. Sáng hôm sau 8h00 - 8h30 mới tới mở cửa, ngồi uống cà phê, đến 9h00 vẫn chưa ngồi vào máy tính quét in bill. Đơn hàng bị quá hạn OPR ngay từ lúc chưa rời khỏi kho bưu cục!",
                "Tôi yêu cầu anh Duân, chị Nhung, anh Trường, anh Nghĩa, anh Phi: Bắt buộc các bưu cục có sản lượng TikTok Shop lớn phải phân công nhân sự mở cửa ca sáng từ 7h00 - 7h30 sáng, quét in bill sạch toàn bộ đơn livestream đêm trước 8h30 sáng. Tuần W41 OPR ca đêm toàn vùng phải kéo lên trên 65% cho tôi! Giờ ta qua Tab 9 Rớt luân chuyển!\""
            ],
            "insights": [
                "Khung giờ livestream đêm 20h - 23h chiếm lượng đơn lớn nhưng bưu cục chưa bố trí ca quét sáng sớm phù hợp.",
                "OPR ca đêm sụt giảm làm trễ toàn bộ thời gian cam kết 24h của sàn TikTok Shop."
            ],
            "warnings": [
                "Tỷ lệ OPR ca đêm dưới 30% khiến shop bị đánh giá xấu và đối mặt nguy cơ sàn hạ bậc xếp hạng vận chuyển."
            ],
            "actions": [
                "Bố trí ca làm việc sớm từ 7h00 sáng tại các bưu cục trọng điểm để quét hoàn tất đơn hàng đêm trước 8h30."
            ]
        },

        # TAB 9: RỚT LC
        {
            "sec_title": "⚠️ [IX. PHÂN TÍCH TỶ TRỌNG RỚT ĐƠN LUÂN CHUYỂN THEO AM & TỈNH THÀNH (W40)]",
            "speech_title": "🗣️ KIỂM SOÁT TỶ LỆ RỚT LUÂN CHUYỂN KTC TOÀN VÙNG (1.69%) (TAB 9):",
            "speech_paragraphs": [
                "📍 1. BẢNG 1 & 2 TỶ LỆ RỚT LUÂN CHUYỂN TOÀN VÙNG & TỈNH (W40):",
                "• Toàn vùng: 1,69% (tổng 219 đơn rớt trên 12.934 đơn cần luân chuyển, duy trì dưới trần kiểm soát 1,80%).",
                "• Bình Thuận: 0,28% (xuất sắc nhất vùng, chỉ rớt 12 đơn / 4.230 đơn).",
                "• Khánh Hòa: 0,48% (cực kỳ an toàn, chỉ rớt 16 đơn / 3.304 đơn).",
                "• Đắk Nông: 1,45% (ở mức chấp nhận được).",
                "• Ninh Thuận: 3,58% (rớt 60 đơn trên 1.676 đơn cần LC).",
                "• Lâm Đồng: 3,84% (rớt 121 đơn trên 3.150 đơn ➔ chiếm hơn một nửa tổng đơn rớt của cả vùng).",
                "📍 2. BẢNG 1 & 3 ĐIỂM MẶT 4 AM VÀ TOP BƯU CỤC RỚT HÀNG NHIỀU NHẤT:",
                "• Hồng Bích Nga: Rớt 4,63% (tăng +2,30%p WoW; rớt 46 đơn / 993 đơn).",
                "• Nguyễn Thị Tuyết Thơ: Rớt 4,24% (rớt 22 đơn / 519 đơn).",
                "• Nguyễn Duy Long: Rớt 3,29% (dính tới 60 đơn rớt — số lượng đơn bị bỏ lại nhiều nhất vùng, tập trung tại BC Phan Rang 38 đơn).",
                "• Lê Văn Trường: Rớt 2,77% (tập trung tại BC Đức Trọng 1 rớt 42 đơn, Lang Biang 29 đơn, Xuân Hương 24 đơn).",
                "• Kiểm soát xuất sắc (0% rớt): Cao Thị Thanh Thủy (0% / 1.188 đơn), Huỳnh Thị Kim Chi (0%), Nguyễn Thanh Long (kéo từ 2,68% về 0%).",
                "🎙️ LỜI NÓI CỦA SẾP ĐIỀU HÀNH VÙNG (KHI MỞ TAB 9 RỚT LUÂN CHUYỂN):",
                "\"Các AM nhìn vào Tab 9 về Rớt Luân Chuyển KTC:",
                "Toàn vùng tuần này rớt 219 đơn, tương ứng 1,69%. Hai tỉnh ven biển Bình Thuận (0,28%) và Khánh Hòa (0,48%) làm rất tốt, chị Thủy và chị Chi đạt tuyệt đối 0% rớt hàng.",
                "NHƯNG NHÌN VÀO CON SỐ TUYỆT ĐỐI 219 ĐƠN BỊ RỚT LẠI TRONG TUẦN:",
                "Hơn một nửa số đơn rớt dồn trọn vào Lâm Đồng (121 đơn) và Ninh Thuận (60 đơn)! Bốn cái tên để rớt hàng nhiều nhất là chị Hồng Bích Nga (4,63%), chị Nguyễn Thị Tuyết Thơ (4,24%), anh Nguyễn Duy Long (rớt 60 đơn) và anh Lê Văn Trường (2,77%).",
                "Nguyên nhân ở đây là gì? Bưu cục các anh chị gom hàng First-mile về muộn sau 17h30. Nhân viên đóng bao bắn tải lề mề. Khi xe tải KTC chạy theo giờ cố định ghé bưu cục, bưu cục các anh chị chưa niêm phong seal xong. Tài xế bấm còi chờ 15 phút buộc phải chạy để kịp giờ cập Hub, bỏ lại các bao hàng nằm đắp chiếu ở góc kho bưu cục!",
                "Đơn bị rớt xe KTC là tự động trôi thêm 24 tiếng, hôm sau giao chắc chắn dính trễ SLA và khách hủy đơn.",
                "Tôi yêu cầu chị Nga, chị Thơ, anh Long và anh Trường: Bắt buộc Trưởng các bưu cục trên phải đóng túi seal trước giờ xe đến tối thiểu 20 phút. Tuyệt đối không để xảy ra tình trạng xe tải đến nơi mới cuống cuồng đi tìm hàng đóng bao! Bưu cục nào làm trễ chuyến xe KTC mà không báo trước điều phối, tôi sẽ trừ điểm thi đua trực tiếp của AM! Giờ ta qua Tab 10 %FD!\""
            ],
            "insights": [
                "Hơn 55% lượng đơn rớt luân chuyển dồn ở Lâm Đồng do lịch xe KTC buổi tối chạy rất khắt khe.",
                "Bình Thuận và Khánh Hòa duy trì tỷ lệ rớt dưới 0,5% chứng minh quy trình đóng bao seal hoàn toàn có thể chuẩn hóa được."
            ],
            "warnings": [
                "219 đơn rớt luân chuyển đồng nghĩa với 219 khách hàng bị trễ hẹn ít nhất 1 ngày, gia tăng nguy cơ khiếu nại."
            ],
            "actions": [
                "Quy định giờ giới nghiêm đóng bao seal tại bưu cục trước giờ xe KTC cập bến 20 phút; xử lý kỷ luật bưu cục làm trễ chuyến xe KTC."
            ]
        },

        # TAB 10: FD
        {
            "sec_title": "🔄 [X. BÁO CÁO TỶ LỆ %FD (RETURN / HOÀN TRẢ) — VÙNG NAM TRUNG BỘ (W40)]",
            "speech_title": "🗣️ PHÂN TÍCH TỶ LỆ HOÀN TRẢ (%FD 7.77%) VÀ 4 BƯU CỤC HOÀN >20% (TAB 10):",
            "speech_paragraphs": [
                "📍 1. BẢNG 1 TỶ LỆ HOÀN TRẢ TOÀN VÙNG (W40 vs W39):",
                "• Toàn vùng: Full hàng đạt 7,77% (24.498 đơn hoàn / 315.328 đơn gán giao) | TikTok Shop đạt 6,10% (4.191 đơn hoàn / 68.719 đơn).",
                "• Nhóm kiểm soát tốt (<6,5%): Nguyễn Ngọc Khánh (4,8%), Cao Thị Thanh Thủy (5,4%), Lê Thanh Nhựt (5,8%), Nguyễn Duy Long (6,5%).",
                "📍 2. BẢNG 2 BÁO ĐỘNG ĐỎ — TOP 4 BƯU CỤC HOÀN HÀNG TRÊN 20%:",
                "• 1. (DNO) Quảng Tín (AM Trương Quang Linh): Hoàn 22,95% (380 đơn hoàn / 1.656 đơn gán).",
                "• 2. (LDO) Lang Biang - Đà Lạt 1 (AM Lê Minh Lợi): Hoàn 21,04% (444 đơn hoàn / 2.110 đơn gán).",
                "• 3. (LDO) Đơn Dương (AM Phan Nguyễn Yến Nhi): Hoàn 20,99% (653 đơn hoàn / 3.111 đơn gán).",
                "• 4. (LDO) Đức Trọng 1 (AM Nguyễn Lê Nguyên Vũ): Hoàn 20,53% (334 đơn hoàn / 1.627 đơn gán).",
                "• Kế tiếp: BC Kiến Đức (AM Nga: 16,71%), BC Cam Linh (AM Thanh Long: 15,33%), BC Đông Gia Nghĩa (AM Duân: 13,72%).",
                "🎙️ LỜI NÓI CỦA SẾP ĐIỀU HÀNH VÙNG (KHI MỞ TAB 10 %FD):",
                "\"Chuyển sang Tab 10 về tỷ lệ Hoàn trả %FD — Vết thương hở làm thất thoát doanh thu của vùng ta:",
                "Toàn vùng tuần này hoàn 7,77% ở hàng Full và 6,10% ở TikTok Shop, cơ bản là dưới trần 8% của công ty. Anh Khánh kiểm soát 4,8%, chị Thủy 5,4%, anh Nhựt 5,8% và anh Long 6,5% rất chuẩn.",
                "NHƯNG KHI NHÌN VÀO BẢNG 2, TÔI KHÔNG THỂ CHẤP NHẬN ĐƯỢC KHI THẤY 4 BƯU CỤC HOÀN TRÊN 20%:",
                "Quảng Tín của anh Linh hoàn 22,95% (380 đơn)! Lang Biang của anh Lợi hoàn 21,04% (444 đơn)! Đơn Dương của chị Nhi hoàn 20,99% (653 đơn)! Và Đức Trọng 1 của anh Vũ hoàn 20,53% (334 đơn)!",
                "Cứ phát 5 đơn hàng các anh chị để trả về mất 1 đơn! Các anh chị đừng đổ lỗi tại địa bàn đồi dốc hay tại khách khó tính. Bản chất ở đây là bưu tá của các anh chị lười đi tuyến xa!",
                "Gặp địa chỉ khó tìm hoặc gọi 1 cuộc chuông reo khách chưa kịp bắt máy là bưu tá bấm ngay lên app lý do 'Khách từ chối nhận' hoặc 'Không liên lạc được 3 lần' để xả hàng về kho bấm hoàn trả ảo, trốn tránh việc phải đi giao lại lần 2, lần 3!",
                "Việc này làm các shop họ phẫn nộ, họ mất tiền quảng cáo, mất tiền đóng gói mà hàng chưa kịp tới tay người mua đã bị bấm hoàn về.",
                "Tôi ra lệnh cho anh Linh, anh Lợi, chị Nhi, anh Vũ: Bắt đầu từ ngày mai, 100% đơn hàng tại 4 bưu cục trên trước khi bấm duyệt trạng thái Chuyển Hoàn, bắt buộc CS bưu cục phải gọi điện ngẫu nhiên phúc tra lại người nhận qua tổng đài. Nếu phát hiện bưu tá bấm hoàn khống mà không có cuộc gọi thực tế trên lịch sử tổng đài, đuổi việc ngay lập tức! Tuần W41 %FD của 4 bưu cục này phải kéo xuống dưới 12% cho tôi! Giờ ta qua Tab 13 COD & QR!\""
            ],
            "insights": [
                "TikTok Shop kiểm soát hoàn trả ở mức 6,10% chứng tỏ người mua trên sàn có độ cam kết nhận hàng cao hơn khách mua lẻ bên ngoài.",
                "Tỷ lệ hoàn cao trên 20% tại 4 bưu cục huyện miền núi chủ yếu bắt nguồn từ hành vi xả tải của shipper chứ không phải do lỗi của shop."
            ],
            "warnings": [
                "Bưu cục Quảng Tín hoàn 22,95% và Lang Biang hoàn 21,04% đang đẩy chi phí vận chuyển ngược lên rất cao và làm mất uy tín thương hiệu GHN."
            ],
            "actions": [
                "Bắt buộc CS bưu cục phúc tra độc lập 100% đơn hàng trước khi cho phép bấm hoàn trả tại các bưu cục có %FD > 12%."
            ]
        },

        # TAB 11: KTC
        {
            "sec_title": "🚛 [XI. BÁO CÁO ĐIỀU HÀNH KTC, VẬN TẢI, %TLTĐ THÙNG XE (45.6%) & 124 CHUYẾN NON TẢI (W40)]",
            "speech_title": "🗣️ HIỆU QUẢ VẬN TẢI KTC: XỬ LÝ 124 CHUYẾN XE NON TẢI DƯỚI 30% THÙNG (TAB 11):",
            "speech_paragraphs": [
                "📍 1. BẢNG CHỈ SỐ VẬN TẢI & KHO KTC (W40 vs W39):",
                "• Tỷ Lệ Lấp Đầy Thùng Xe KTC (%TLTĐ Toàn Vùng): Đạt 45,6% (W39: 47,7%, tụt giảm -2,1%p, cách rất xa mục tiêu tối ưu ≥ 55,0%).",
                "• Số chuyến xe chạy non tải (<30% thùng xe): Ghi nhận tới 124 chuyến xuất bến trong tuần (chiếm 24,2% tổng số 513 chuyến KTC), trong đó có 7 chuyến rỗng dưới 10%, 32 chuyến dưới 20% và 37 chuyến dưới 30%!",
                "• Tổng số chuyến xe KTC vận hành toàn vùng: 513 chuyến (giảm 14 chuyến so với 527 chuyến W39).",
                "• Chi tiết 5 kho KTC trọng điểm:",
                "  - KTC Khánh Hòa: 193 chuyến | TLTĐ 52,3% (-2,6%p) | 20 xe non tải <30%.",
                "  - KTC Đức Trọng - Lâm Đồng: 110 chuyến | TLTĐ 40,6% (-4,5%p) | 43 xe non tải <30% ➔ ĐIỂM NÓNG LÃNG PHÍ LỚN NHẤT VÙNG!",
                "  - KTC Bình Thuận: 113 chuyến | TLTĐ 47,7% (+1,1%p) | 20 xe non tải <30%.",
                "  - KTC Bảo Lộc - Lâm Đồng: 55 chuyến | TLTĐ 38,2% (-1,6%p) | 19 xe non tải <30%.",
                "  - KTC Đắk Nông: 42 chuyến | TLTĐ 31,3% (-1,9%p) | 22 xe non tải <30% (hơn một nửa số chuyến chạy non tải).",
                "🎙️ LỜI NÓI CỦA SẾP ĐIỀU HÀNH VÙNG (KHI MỞ TAB 11 VẬN TẢI KTC):",
                "\"Qua Tab 11 về Điều hành KTC và Chi phí Vận tải:",
                "Tỷ lệ lấp đầy thùng xe KTC tuần này tụt xuống còn 45,6%, giảm mất hơn 2%p! Và trên hệ thống tuần qua phát hiện có tới 124 CHUYẾN XE TẢI KTC chạy trên đường với tỷ lệ lấp đầy dưới 30% thùng!",
                "Cứ 4 chuyến xe chạy thì có 1 chuyến chạy non tải, thậm chí có 7 chuyến gần như rỗng không dưới 10% thùng xe! Điểm nóng nhất là KTC Đức Trọng gánh tới 43 chuyến non tải, và Đắk Nông với 22 chuyến non tải, tỷ lệ lấp đầy chỉ vỏn vẹn 31% — tức là thùng xe rỗng tới hơn hai phần ba!",
                "Chúng ta đang trả tiền cước xe, tiền dầu cho những chuyến xe chở gió. Ban Vận tải trong tuần W41 này phải rà soát và xử lý ngay 124 chuyến xe non tải này: Tuyến nào sản lượng ít thì gộp 2 chuyến làm một hoặc chuyển sang dùng xe tải nhỏ 1,5 tấn, dứt khoát không cho xe chạy rỗng đường dài! Giờ ta qua Tab 12 Aging!\""
            ],
            "insights": [
                "Biểu đồ chạy xe cố định đang không theo kịp biến động sản lượng hàng ngày trong tuần, gây lãng phí lớn vào các ngày đầu tuần.",
                "KTC Đức Trọng (43 xe non tải) và Đắk Nông (31,3% TLTĐ) là hai nút thắt trọng điểm cần tối ưu hóa phương tiện."
            ],
            "warnings": [
                "124 chuyến xe non tải trực tiếp làm đội chi phí trên mỗi đơn hàng (Cost Per Order - CPO) của vùng Nam Trung Bộ."
            ],
            "actions": [
                "Ban Vận tải làm việc với các nhà xe đối tác: Linh hoạt dời chuyến hoặc gộp tuyến bưu cục huyện có sản lượng dưới 30% thùng xe."
            ]
        },

        # TAB 12: AGING
        {
            "sec_title": "⏳ [XII. ĐIỀU HÀNH XỬ LÝ HÀNG AGING TỒN ĐỌNG & TREO LUÂN CHUYỂN (W40)]",
            "speech_title": "🗣️ CHIẾN DỊCH GIẢI TỎA 1.420 ĐƠN AGING >5 NGÀY & 118 ĐƠN TREO LUÂN CHUYỂN (TAB 12):",
            "speech_paragraphs": [
                "📍 1. BẢNG PHÂN BỔ HÀNG TỒN LÂU NGÀY (AGING TOÀN VÙNG W40):",
                "• Tổng đơn Aging tồn trên 5 ngày: 1.420 đơn (giảm được 218 đơn so với 1.638 đơn tuần W39).",
                "  - Tồn từ 5 đến 8 ngày: 1.025 đơn.",
                "  - Tồn từ 8 đến 15 ngày: 362 đơn.",
                "  - Tồn nguy hiểm trên 15 ngày: 33 đơn (nguy cơ bồi thường mất mát, hư hỏng rất cao).",
                "• Top 3 bưu cục tập trung Aging nhiều nhất: (DNO) Quảng Tín (312 đơn), (LDO) Đức Trọng 1 (285 đơn), (LDO) Xuân Hương - Đà Lạt (210 đơn). Ba bưu cục này chiếm hơn 56% tổng lượng hàng tồn lâu của cả vùng.",
                "📍 2. TÌNH HÌNH ĐƠN TREO LUÂN CHUYỂN (>24H):",
                "• Toàn vùng ghi nhận 118 đơn bị treo trạng thái luân chuyển quá 24 giờ chưa quét tới bưu cục nhận.",
                "• Nổi cộm: Cụm Đắk Nông (AM Trần Thị Nhung dính 36 đơn treo), Lâm Đồng dính 45 đơn treo.",
                "🎙️ LỜI NÓI CỦA SẾP ĐIỀU HÀNH VÙNG (KHI MỞ TAB 12 AGING & TREO LC):",
                "\"Qua Tab 12 về Hàng tồn Aging và Đơn treo luân chuyển:",
                "Tuần này lượng hàng tồn trên 5 ngày giảm từ 1.638 xuống 1.420 đơn, giải phóng được hơn 200 đơn. Nhưng con số 1.420 đơn vẫn là một khối u lớn trong kho!",
                "Đặc biệt là 33 đơn tồn trên 15 ngày và 362 đơn tồn từ 8 đến 15 ngày. Nằm lăn lóc ở góc kho từ nửa tháng trước mà anh em cứ để đó không chịu bấm xử lý hoàn trả hay báo đền bù. Lại tiếp tục là 3 cái tên quen thuộc: Quảng Tín (312 đơn), Đức Trọng 1 (285 đơn) và Xuân Hương Đà Lạt (210 đơn).",
                "Thêm vào đó, có 118 đơn bị treo luân chuyển trên 24 giờ. Kho KTC đã bắn gửi đi từ hôm kia nhưng bưu cục nhận vẫn chưa quét nhập kho. Chỗ chị Nhung Đắk Nông dính 36 đơn và Lâm Đồng dính 45 đơn. Các AM cho rà soát kho ngay trong chiều nay, tìm cho ra 118 đơn treo này và dọn sạch 395 đơn tồn trên 8 ngày trước thứ Năm cho tôi! Giờ ta qua Tab 13 COD & QR!\""
            ],
            "insights": [
                "Lượng hàng tồn aging giảm 218 đơn cho thấy các bưu cục đã bắt đầu quan tâm đến việc dọn kho cuối tuần.",
                "Đơn treo luân chuyển >24h tiềm ẩn nguy cơ mất cắp hoặc thất lạc trong quá trình vận chuyển giữa các chặng."
            ],
            "warnings": [
                "33 đơn tồn trên 15 ngày nếu không xử lý dứt điểm sẽ biến thành các khiếu nại đền bù thiệt hại tài chính."
            ],
            "actions": [
                "AM trực tiếp đến 3 bưu cục Quảng Tín, Đức Trọng 1, Xuân Hương chỉ đạo kiểm kê sàn kho và xử lý dứt điểm các đơn >8 ngày."
            ]
        },

        # TAB 13: COD & QR
        {
            "sec_title": "💰 [XIII. QUẢN TRỊ DÒNG TIỀN COD, TỶ LỆ THANH TOÁN QR & THU HỒI CÔNG NỢ (W40)]",
            "speech_title": "🗣️ QUẢN TRỊ DÒNG TIỀN COD (77.5 TỶ ₫), TỶ LỆ TIỀN MẶT & ĐIỂM NÓNG 80% TM (TAB 13):",
            "speech_paragraphs": [
                "📍 1. BẢNG 1 XU HƯỚNG DÒNG TIỀN 2 TUẦN (W40 vs W39):",
                "• Tổng tiền COD thu hộ tuần W40: 77.502,0 Triệu đồng (~77,5 tỷ đồng, giảm -4,0% so với 80.733,6 Tr W39).",
                "• Tiền mặt thu về: 31.276,0 Triệu đồng (chiếm 40,4%).",
                "• Chuyển khoản QR: 46.226,0 Triệu đồng (chiếm 59,6%).",
                "• Biến động: Tỷ lệ tiền mặt nhích nhẹ +0,2%p (từ 40,1% lên 40,4% ➔ Đánh giá: Xấu đi ⚠️).",
                "📍 2. BẢNG 2 XẾP HẠNG 19 AM THEO % TIỀN MẶT — PHÂN HÓA 3 NHÓM RÕ RỆT:",
                "• 🔴 Nhóm Tiền Mặt Cao Báo Động (≥70% TM — Nguy hiểm):",
                "  1. Huỳnh Thúc Duân: 81,0% TM (W39: 71,5%, tăng vọt +9,5%p ➔ Báo động đỏ).",
                "  2. Lê Thanh Nhựt: 80,4% TM (W39: 77,7%, tăng +2,7%p).",
                "  3. Huỳnh Thị Kim Chi: 75,8% TM (W39: 68,6%, tăng mạnh +7,2%p).",
                "• 🟡 Nhóm Cần Cải Thiện (50% - 70% TM): Trần Thị Nhung (64,1%), Phan Nguyễn Yến Nhi (59,2%), Nguyễn Đỗ Minh Nghĩa (58,6%), Trương Quang Linh (56,3%, đã giảm tốt -24,3%p từ 80,6%).",
                "• 🟢 Nhóm Thanh Toán Số Xuất Sắc (VietQR áp đảo):",
                "  - Thái Thị Thanh Thư (Khánh Hòa): Quán quân toàn mạng GHN, tỷ lệ tiền mặt chỉ còn 4,0% (tức 96,0% dòng tiền là quét mã QR!).",
                "  - Cao Thị Thanh Thủy (Bình Thuận): Tiền mặt chỉ 16,1% (QR đạt 83,9%).",
                "  - Nguyễn Duy Long (Ninh Thuận): Tiền mặt chỉ 23,4% (QR đạt 76,6%).",
                "🎙️ LỜI NÓI CỦA SẾP ĐIỀU HÀNH VÙNG (KHI MỞ TAB 13 COD & QR):",
                "\"Các AM nhìn sang Tab 13 về Quản trị dòng tiền COD và Thanh toán QR:",
                "Tuần này toàn vùng ta thu hộ hơn 77,5 tỷ đồng tiền hàng. Dòng tiền Chuyển khoản QR đạt 46,2 tỷ (chiếm gần 60%), tiền mặt shipper cầm về là hơn 31,2 tỷ (chiếm 40,4%). So với tuần trước, tỷ lệ tiền mặt nhích nhẹ +0,2%p, hệ thống báo xấu đi.",
                "Nhìn vào Bảng 2:",
                "Chị Thái Thị Thanh Thư ở Khánh Hòa tiếp tục là tấm gương sáng nhất toàn quốc: Tỷ lệ tiền mặt của chị Thư chỉ còn 4,0% — tức là 96,0% dòng tiền khách hàng tự quét mã QR thanh toán! Chị Thủy đạt 16,1% tiền mặt (QR 84%), anh Duy Long Ninh Thuận đạt 23,4% tiền mặt (QR gần 77%). Shipper không phải cầm tiền mặt, an toàn tuyệt đối cho anh em trên đường.",
                "Anh Trương Quang Linh Đắk Nông tuần này cũng tiến bộ rất lớn khi kéo giảm tiền mặt từ 80,6% xuống 56,3% (giảm tới hơn 24%p).",
                "NHƯNG TÔI PHẢI CẢNH BÁO RẤT NGHIÊM KHẮC 3 AM ĐANG ÔM TIỀN MẶT QUÁ CAO Ở ĐẦU BẢNG 2:",
                "Anh Huỳnh Thúc Duân vọt lên 81,0% tiền mặt (tăng gần 10%p!), anh Lê Thanh Nhựt 80,4% tiền mặt và chị Huỳnh Thị Kim Chi 75,8% tiền mặt (tăng hơn 7%p)!",
                "Tôi hỏi các anh chị: Hơn 31 tỷ đồng tiền mặt shipper cầm chạy ngoài đường và để qua đêm ở két sắt bưu cục huyện, các anh chị định chờ xảy ra cướp giật, mất mát hay bưu tá ôm tiền trốn mới sáng mắt ra à?",
                "Bản chất ở đây là bưu tá của các anh chị lười mời khách quét QR, hoặc có tâm lý cố tình thu tiền mặt để giữ tiền xoay xở cá nhân trong vài ngày trước khi nộp về bưu cục!",
                "Tôi yêu cầu anh Duân, anh Nhựt, chị Chi: Bắt buộc trang bị 100% thẻ đeo cổ in mã QR cho bưu tá. Kiểm tra số dư két tiền mặt bưu cục lúc 20h30 hàng ngày, bưu cục nào xa ngân hàng bắt buộc nộp tiền qua cây ATM hoặc Viettel Money trước 21h00, tuyệt đối không để tiền mặt tồn qua đêm tại két bưu cục quá 5 triệu đồng! Tuần W41 kéo tỷ lệ tiền mặt của 3 AM này từ 80% xuống dưới 65% cho tôi! Giờ ta qua Tab 14 Truy thu!\""
            ],
            "insights": [
                "Chị Thư Khánh Hòa đạt 96% thanh toán QR chứng minh thói quen thanh toán không tiền mặt hoàn toàn có thể nhân rộng nếu bưu tá quyết liệt hướng dẫn khách.",
                "Tỷ lệ tiền mặt của anh Duân (81%) và anh Nhựt (80%) tạo ra rủi ro thất thoát quỹ rất lớn."
            ],
            "warnings": [
                "Hơn 31 tỷ đồng tiền mặt shipper cầm chạy ngoài đường tiềm ẩn rủi ro an toàn và chiếm dụng vốn."
            ],
            "actions": [
                "Trang bị 100% thẻ đeo mã QR cho bưu tá; kiểm tra số dư quỹ tiền mặt bưu cục trên hệ thống lúc 20h30 hàng ngày."
            ]
        },

        # TAB 14: TRUY THU
        {
            "sec_title": "🚨 [XIV. BÁO CÁO TRUY THU – BIẾN ĐỘNG 2 TUẦN (W39 vs W40) & CẢNH BÁO BÙNG PHÁT 187.1 TRIỆU ₫]",
            "speech_title": "🗣️ BÁO CÁO TRUY THU: W40 CẦN THU 187.1 TR ₫ VÀ ĐIỂM NÓNG BẮC CAM RANH (TAB 14):",
            "speech_paragraphs": [
                "📍 1. BẢNG SO SÁNH BIẾN ĐỘNG 2 TUẦN (W40 vs W39):",
                "• Số bản ghi phát sinh: 2.424 bản ghi (W39: 4.076 bản ghi, giảm -1.652 đơn / -40,5%).",
                "• Số tiền truy thu ban đầu: 433,05 Tr ₫ (W39: 317,25 Tr ₫, TĂNG +115,8 Tr ₫ / +36,5%!).",
                "• Số tiền đã điều chỉnh / giảm trừ: -245,96 Tr ₫ (W39: -5,17 Tr ₫).",
                "• SỐ TIỀN CẦN TRUY THU THỰC TẾ: 187,09 Tr ₫ (giảm -124,99 Tr ₫ / -40,1% so với 312,08 Tr ₫ của W39).",
                "📍 2. BẢNG 1 CƠ CẤU THEO LOẠI TRUY THU TRỌNG ĐIỂM:",
                "• 1. Liên đới chiếm dụng: 56,8 Tr ₫ (4 đơn) ➔ TÍNH CHẤT ĐẶC BIỆT NGHIÊM TRỌNG.",
                "• 2. Tick mất hàng: 41,2 Tr ₫ (53 đơn).",
                "• 3. Mất / Thiếu / Tráo sản phẩm: 30,9 Tr ₫ (76 đơn).",
                "• 4. Khiếu nại chưa tick GTC: 8,8 Tr ₫.",
                "• 5. Đơn hàng hư hỏng: 8,2 Tr ₫ (giảm mạnh -67,8% so với 25,5 Tr W39).",
                "📍 3. BẢNG 4 THEO AM VÀ TOP BƯU CỤC NÓNG NHẤT:",
                "• 🔴 TOP 1 NGUY HIỂM: AM Nguyễn Thanh Long (Khánh Hòa): 51,2 Tr ₫ / 72 ticket ➔ ĐIỂM NÓNG BƯU CỤC (KHO) BẮC CAM RANH PHÁT SINH 48,7 TRIỆU ₫ LIÊN ĐỚI CHIẾM DỤNG TIỀN HÀNG!",
                "• 🔴 TOP 2: AM Lê Văn Trường (Lâm Đồng): 26,3 Tr ₫ / 419 ticket (nhiều ticket nhất vùng, bưu cục Đơn Dương chiếm 12,8 Tr ₫).",
                "• 🔴 TOP 3: AM Trần Văn Phước: 22,9 Tr ₫ / 288 ticket (bưu cục Quảng Tín chiếm 13,0 Tr ₫).",
                "• 🔴 TOP 4: AM Huỳnh Thị Kim Chi (Lâm Đồng): 21,3 Tr ₫ / 110 ticket (bưu cục Tân Hà Lâm Hà chiếm trọn 21,3 Tr ₫).",
                "🎙️ LỜI NÓI CỦA SẾP ĐIỀU HÀNH VÙNG (KHI MỞ TAB 14 TRUY THU):",
                "\"Các AM nhìn lên màn hình Tab 14 Báo cáo Truy Thu giúp tôi:",
                "Đây là vấn đề nhức nhối nhất và nghiêm trọng nhất trong buổi họp hôm nay.",
                "Nhìn con số tổng: Tuần W40 số tiền cần truy thu giảm được 40%, từ 312 triệu xuống còn 187,1 triệu đồng nhờ Kế toán đối soát giảm trừ được 246 triệu.",
                "NHƯNG SỐ TIỀN PHÁT SINH BAN ĐẦU LẠI TĂNG VỌT TỪ 317 TRIỆU LÊN 433 TRIỆU ĐỒNG (+36,5%)!",
                "Và khi nhìn vào dòng đầu tiên của Bảng 1 và Bảng 4, chúng ta thấy một vụ việc CỰC KỲ NGHIÊM TRỌNG:",
                "Lỗi 'Liên đới chiếm dụng' phát sinh tới 56,8 triệu đồng!",
                "Trong đó, chỉ riêng bưu cục Bắc Cam Ranh thuộc cụm của AM NGUYỄN THANH LONG đã chiếm tới 48,7 triệu đồng do nhân sự chiếm dụng tiền hàng COD!",
                "Anh Thanh Long đâu rồi? Đây không còn là chuyện nghiệp vụ cân đo sai hay làm mất hàng nữa, mà là dấu hiệu chiếm đoạt tài sản công ty và vi phạm pháp luật! Anh quản lý cụm thế nào mà để nhân viên thu tiền hàng của khách rồi giấu đi tiêu xài cá nhân suốt bao nhiêu ngày không ai hay biết?",
                "Tôi yêu cầu anh Long: 8h00 sáng mai dẫn đích danh Trưởng bưu cục Bắc Cam Ranh lên văn phòng gặp tôi và Ban Thanh tra, nộp đủ 48,7 triệu đồng hoàn quỹ và chuyển hồ sơ kỷ luật nhân sự vi phạm!",
                "Bên cạnh đó, anh Lê Văn Trường đang ôm tới 419 ticket truy thu — nhiều nhất toàn vùng Nam Trung Bộ, số tiền 26,3 triệu đồng, tập trung ở Đơn Dương 12,8 triệu. Anh Phước 288 ticket (22,9 triệu), chị Chi 110 ticket (21,3 triệu tại Tân Hà).",
                "Tiền của công ty chứ không phải lá đa mà các anh chị để ngâm từ tuần này qua tuần khác! Tôi giao hạn chót: Đến ngày 11/10, anh Trường, anh Phước, chị Chi phải giải tỏa dứt điểm 80% số ticket nợ tồn này cho tôi! Giờ ta qua Tab 15 Kinh doanh!\""
            ],
            "insights": [
                "Số tiền cần truy thu giảm 40% (xuống 187,1 Tr ₫) chứng minh khâu đối soát và điều chỉnh dữ liệu cước đã phát huy tác dụng.",
                "Vụ việc 48,7 Tr ₫ tại Bắc Cam Ranh cho thấy lỗ hổng trong công tác giám sát tiền hàng và bàn giao ca giữa Quản lý bưu cục và bưu tá."
            ],
            "warnings": [
                "Lỗi liên đới chiếm dụng 56,8 Tr ₫ là vi phạm pháp luật và quy chế tài chính nghiêm trọng nhất từ đầu quý.",
                "419 ticket dồn ứ tại địa bàn AM Lê Văn Trường thể hiện sự buông lỏng đối soát tại các bưu cục huyện Lâm Đồng."
            ],
            "actions": [
                "Chuyển hồ sơ bưu cục Bắc Cam Ranh sang Phòng Pháp chế / An ninh nội bộ điều tra thu hồi tiền ngay trong 48 giờ.",
                "AM Trường, AM Phước, AM Chi lập kế hoạch thu hồi từng ticket với các bưu cục trực thuộc, báo cáo tiến độ hàng ngày."
            ]
        },

        # TAB 15: KINH DOANH
        {
            "sec_title": "📈 [XV. PHÂN TÍCH DOANH THU KINH DOANH & TĂNG TRƯỞNG KHÁCH HÀNG MỚI (F30) | VÙNG NTB]",
            "speech_title": "🗣️ DOANH THU KINH DOANH 1.120 TỶ ₫, PHÁT TRIỂN 111 SHOP F30 & QUẢN TRỊ SHOP NHÓM A (TAB 15):",
            "speech_paragraphs": [
                "📍 1. BẢNG TỔNG HỢP KINH DOANH TUẦN W40 (Kỳ 27/09 – 03/10/2026 vs Kỳ trước 20/09 – 26/09/2026):",
                "• Tổng Doanh Thu Toàn Vùng: 1.120,5 Tr ₫ (giảm -42,2 Tr ₫ / -3,6% WoW).",
                "• Tổng Sản Lượng Gửi Toàn Vùng: 35.334 đơn (giảm -2.060 đơn / -5,5% WoW).",
                "• Khách hàng mới F30 (trong 30 ngày): Toàn vùng mang về 111 shop mới (tăng +19 shop / +20,7%), đóng góp 9,4 Tr ₫ doanh thu ban đầu.",
                "• Quản trị Shop Nhóm A (Top 10 khách hàng lớn nhất): Lũy kế doanh thu tháng 10 (MTD) đạt 8.840,0 Tr ₫. Dẫn đầu là siêu shop 'Vận Chuyển Online' do AM Phan Đình Duy quản lý đạt 5.688,0 Tr ₫.",
                "📍 2. BÓC TÁCH CHI TIẾT THEO AM KINH DOANH:",
                "• 🟢 TOP AM TĂNG TRƯỞNG XUẤT SẮC:",
                "  1. Phan Đình Duy (Khánh Hòa): Doanh thu 479,0 Tr ₫ (+0,7% WoW, chiếm 42,7% doanh thu cả vùng), sản lượng 10.088 đơn (+74 đơn). Dẫn đầu F30 với 16 shop mới (1,21 Tr ₫). Quản lý shop #1 nhóm A.",
                "  2. Nguyễn Duy Long (Bình Thuận): Doanh thu 98,2 Tr ₫ (+2,3% WoW), sản lượng 4.142 đơn (+113 đơn), phát triển 13 shop F30.",
                "  3. Lê Thanh Nhựt (Ninh Thuận): Doanh thu 60,9 Tr ₫ (+6,6% WoW), sản lượng 2.749 đơn (+274 đơn / +11,1%).",
                "  4. Nguyễn Lê Nguyên Vũ (Khánh Hòa): Doanh thu 25,4 Tr ₫ (+10,8% WoW), sản lượng 1.029 đơn (+105 đơn / +11,4%).",
                "• 🔴 TOP AM BÁO ĐỘNG ĐỎ VỀ KINH DOANH:",
                "  1. Huỳnh Thúc Duân (Đắk Nông): Doanh thu sụt giảm -29,1% WoW (-23,4 Tr ₫, từ 80,5 Tr xuống 57,1 Tr ₫); sản lượng bốc hơi -1.608 đơn (-28,5%, từ 5.648 xuống 4.040 đơn) tại các bưu cục Gia Nghĩa và Nhân Cơ.",
                "  2. Thái Thị Thanh Thư (Khánh Hòa): Doanh thu giảm -10,6% WoW (-11,8 Tr ₫, từ 111,4 Tr xuống 99,6 Tr ₫), sản lượng giảm -350 đơn.",
                "  3. Trần Thị Nhung (Đắk Nông): Doanh thu giảm -21,5% WoW (-8,0 Tr ₫, từ 37,1 Tr xuống 29,1 Tr ₫), sản lượng giảm -329 đơn (-16,4%).",
                "🎙️ LỜI NÓI CỦA SẾP ĐIỀU HÀNH VÙNG (KHI MỞ TAB 15 KINH DOANH):",
                "\"Qua Tab 15 về Kinh Doanh và Khách Hàng Mới F30:",
                "Toàn vùng tuần này mang về 1,12 tỷ đồng doanh thu và 35 ngàn đơn hàng gửi, giảm nhẹ 3,6% theo nhịp cuối tháng.",
                "Tôi nhiệt liệt biểu dương anh Phan Đình Duy: Một mình cụm anh Duy mang về tới 479 triệu đồng doanh thu, chiếm gần một nửa doanh số của toàn vùng Nam Trung Bộ! Anh Duy tiếp tục giữ vững siêu shop 'Vận Chuyển Online' với doanh thu tháng này đã chạm mốc 5,7 tỷ đồng, đồng thời dẫn đầu toàn vùng khi phát triển thêm 16 shop mới F30. Anh Long Bình Thuận, anh Nhựt Ninh Thuận và anh Vũ Khánh Hòa cũng tăng trưởng rất tốt từ 2% đến 11%.",
                "NHƯNG TÔI YÊU CẦU AM HUỲNH THÚC DUÂN GIẢI TRÌNH NGAY LẬP TỨC:",
                "Tại sao chỉ trong đúng 1 tuần, doanh thu của anh Duân tại Đắk Nông tụt dốc không phanh mất gần 30% (-23,4 triệu), và sản lượng bốc hơi tới 1.608 đơn gửi (-28,5%)?",
                "Đây là mức sụt giảm kinh doanh lớn nhất của cả vùng trong 3 tháng qua! Kiểm tra tại Gia Nghĩa và Nhân Cơ cho thấy có ít nhất 2 shop lớn nông sản và cà phê đã ngưng gửi hàng qua GHN và chuyển hẳn sang đối thủ cạnh tranh. Có phải do bưu cục lấy hàng trễ hay thái độ phục vụ có vấn đề? Đầu tuần này anh Duân phải trực tiếp đến gặp lại chủ các shop này để thương lượng chính sách giá và kéo nguồn hàng quay trở lại GHN cho tôi! Giờ ta qua Tab 16 Tổng kết!\""
            ],
            "insights": [
                "AM Phan Đình Duy là trụ cột kinh doanh của toàn vùng khi đóng góp 42,7% doanh thu và quản lý siêu shop #1 nhóm A.",
                "F30 tăng thêm 20,7% (111 shop mới) cho thấy tiềm năng mở rộng tệp khách hàng cá nhân và shop online vừa và nhỏ còn rất lớn."
            ],
            "warnings": [
                "AM Huỳnh Thúc Duân mất 28,5% sản lượng (-1.608 đơn) tại Gia Nghĩa, Nhân Cơ là tín hiệu cảnh báo mất thị phần nghiêm trọng tại Đắk Nông."
            ],
            "actions": [
                "AM Huỳnh Thúc Duân đi thị trường Gia Nghĩa trong ngày thứ Ba, trực tiếp gặp 2 shop lớn vừa ngưng gửi để xử lý vướng mắc."
            ]
        },

        # TAB 16: TỔNG KẾT
        {
            "sec_title": "🏁 [XVI. ĐIỀU HÀNH TRỌNG ĐIỂM: 13 BƯU CỤC CẢNH BÁO BẤT ỔN & 5 TRỌNG TÂM HÀNH ĐỘNG TUẦN W41]",
            "speech_title": "🗣️ DANH SÁCH 13 BƯU CỤC CẢNH BÁO ĐỎ & 5 NHIỆM VỤ ĐIỀU HÀNH HIỆN TRƯỜNG TUẦN W41 (TAB 16):",
            "speech_paragraphs": [
                "📍 1. DANH SÁCH 13 BƯU CỤC BẤT ỔN CẦN GIẢI TỎA KHẨN CẤP (W40):",
                "• 1. (DNO) Quảng Tín: GTC 18,1% (Cảnh báo 100 ngày liên tiếp) | Backlog 1.224 đơn (tồn >5 ngày: 490 đơn) | ODR 74,9% | Truy thu 13,0 Tr ₫ (AM Trương Quang Linh).",
                "• 2. (LDO) Đức Trọng 1: GTC 20,1% (Cảnh báo 84 ngày) | Backlog 1.223 đơn (tồn >5 ngày: 281 đơn) | Rớt LC 42 đơn (AM Trầm Hữu Tiến).",
                "• 3. (DNO) Kiến Đức: GTC 29,9% (Cảnh báo 80 ngày) | Backlog 1.035 đơn (AM Hồng Bích Nga).",
                "• 4. (LDO) Xuân Hương - Đà Lạt: GTC 30,2% | Backlog 2.165 đơn (tồn >5 ngày: 310 đơn) | ODR 78,3% (AM Lê Văn Trường).",
                "• 5. (KHO) Cam Linh: GTC 30,7% (Cảnh báo 108 ngày) | Backlog 2.433 đơn (AM Nguyễn Thanh Long).",
                "• 6. (KHO) Tây Nha Trang: GTC 33,3% | Backlog 2.295 đơn (AM Phan Đình Duy).",
                "• 7. (LDO) Lang Biang - Đà Lạt 1: GTC 36,5% (Cảnh báo 108 ngày) | Backlog 992 đơn | ODR 74,1% thấp nhất vùng (AM Lê Minh Lợi).",
                "• 8. (LDO) Di Linh: GTC 40,0% | Backlog 1.970 đơn (tồn >5 ngày: 219 đơn) (AM Nguyễn Lê Nguyên Vũ).",
                "• 9. (DNO) Tuy Đức: GTC 41,2% | Backlog 640 đơn (AM Trần Thị Nhung).",
                "• 10. (LDO) Tân Hà Lâm Hà: GTC 44,5% | Backlog 798 đơn (AM Huỳnh Thị Kim Chi).",
                "• 11. (DNO) Nhân Cơ: GTC 45,1% | Backlog 347 đơn | Doanh thu sụt giảm -29,1% (AM Huỳnh Thúc Duân).",
                "• 12. (LDO) Đơn Dương: GTC 45,3% | Backlog 2.038 đơn | Dính truy thu 12,8 Tr ₫ (AM Phan Nguyễn Yến Nhi).",
                "• 13. (LDO) Lâm Viên - Đà Lạt 2: GTC 46,2% | Backlog 860 đơn (AM Lê Văn Trường).",
                "📍 2. ĐÁNH GIÁ CHUNG VÀ GIAO VIỆC CỤ THỂ 18 AM:",
                "• 🟢 KHEN THƯỞNG: AM Phan Đình Duy (Top 1 Doanh thu), AM Nguyễn Ngọc Khánh (Quán quân GTC 74,5%), AM Nguyễn Duy Long (Đầu tàu Sản lượng vùng 42,7k đơn & GTC 69,0%), AM Cao Thị Thanh Thủy (Top 1 ODR 97,8%), AM Lê Thanh Nhựt (Tăng trưởng sản lượng +1.316 đơn).",
                "• 🔴 CẢNH BÁO ĐẶC BIỆT & GIAO NHIỆM VỤ HIỆN TRƯỜNG:",
                "  - AM Nguyễn Thanh Long: Trực tiếp phối hợp Pháp chế thu hồi 48,7 Tr ₫ vụ việc chiếm dụng tại Bắc Cam Ranh trước ngày 08/10; dọn sạch backlog 2.433 đơn tại Cam Linh.",
                "  - AM Huỳnh Thúc Duân: Xuống bưu cục Gia Nghĩa và Nhân Cơ cứu vãn sản lượng bốc hơi -1.608 đơn; giải trình trước Ban Giám Đốc.",
                "  - AM Lê Văn Trường: Trực tiếp xuống Đơn Dương và Xuân Hương xử lý 419 ticket truy thu (26,3 Tr ₫) và giải phóng 4.200 đơn backlog.",
                "  - AM Lê Minh Lợi & Trương Quang Linh: Viết cam kết đưa ODR Lang Biang và Quảng Tín từ 74% lên trên 85% trong tuần W41.",
                "  - AM Thái Thị Thanh Thư: Rà soát lại việc hụt 7.600 đơn sản lượng và 11,8 Tr ₫ doanh thu.",
                "  - AM Trần Thị Nhung: Xử lý dứt điểm 36 đơn treo luân chuyển >24h tại Đắk Nông.",
                "📍 3. 5 TRỌNG TÂM HÀNH ĐỘNG TUẦN W41 TOÀN VÙNG NAM TRUNG BỘ:",
                "• Trọng tâm 1: Duy trì kỷ luật Last-mile, giữ vững %GTC trên 60%, nâng tỷ lệ Gán Ca 2 từ 62,9% lên trên 75%.",
                "• Trọng tâm 2: Quyết liệt thu hồi công nợ & truy thu: Xử lý dứt điểm 187,1 Tr ₫, phong tỏa và thu hồi vụ 48,7 Tr ₫ tại Bắc Cam Ranh.",
                "• Trọng tâm 3: Cứu vãn ODR tại 4 điểm đáy: Nâng ODR Lang Biang, Quảng Tín, Đơn Dương, Đức Trọng 1 lên trên 75% - 85% bằng cơ chế phát tăng cường ca chiều tối.",
                "• Trọng tâm 4: Tối ưu chi phí vận tải: Gộp tuyến và cắt giảm 124 chuyến xe KTC non tải <30% thùng để đưa %TLTĐ vượt mốc 50%.",
                "• Trọng tâm 5: Chăm sóc giữ chân khách hàng nhóm A và phục hồi sản lượng kinh doanh tại Đắk Nông và Khánh Hòa.",
                "🎙️ LỜI NÓI KẾT LUẬN TOÀN BỘ BUỔI HỌP GIAO BAN:",
                "\"Thưa toàn thể các anh chị em AM,",
                "Để kết luận lại buổi họp hôm nay: Vùng ta đã chứng minh được khi toàn hệ thống siết kỷ luật, chúng ta hoàn toàn có thể đưa %GTC vượt 60% và ODR vượt 93%.",
                "Nhưng những kết quả đó sẽ trở nên vô nghĩa nếu chúng ta để rò rỉ 187 triệu tiền truy thu, để xảy ra vụ chiếm dụng tiền hàng ở Bắc Cam Ranh, hay để mất khách hàng lớn tại Đắk Nông!",
                "13 bưu cục cảnh báo đỏ trên màn hình chính là nơi quyết định chất lượng dịch vụ của vùng ta trong tuần tới. Giải tỏa xong 13 bưu cục này là toàn vùng Nam Trung Bộ sẽ đứng vững trong top đầu toàn quốc.",
                "Tôi yêu cầu tất cả các AM nhận việc, tập trung hành động dứt khoát tại hiện trường. Chúc anh em tuần W41 vận hành an toàn, bứt phá doanh số và đạt chuẩn SLA toàn diện!\""
            ],
            "insights": [
                "13 bưu cục này đang nắm giữ hơn 19.000 đơn backlog của vùng; giải tỏa dứt điểm 13 bưu cục này thì ODR và GTC toàn vùng sẽ tự động tăng thêm từ 2% đến 3%p.",
                "Sự chuyển dịch từ chỉ trích sang giao việc cụ thể với deadline rõ ràng sẽ giúp các AM chủ động hành động tại hiện trường."
            ],
            "warnings": [
                "Bưu cục nào nằm trong danh sách cảnh báo đỏ quá 4 tuần liên tiếp mà không có chuyển biến sẽ bị thay thế Trưởng bưu cục ngay trong tháng 10."
            ],
            "actions": [
                "Các AM có bưu cục trong danh sách cảnh báo bắt buộc gửi báo cáo tiến độ giải tỏa backlog và xử lý truy thu về nhóm điều hành trước 19h00 hàng ngày."
            ]
        }
    ]

    for s_data in sections:
        add_callout_box(
            doc,
            section_title=s_data["sec_title"],
            speech_title=s_data["speech_title"],
            speech_paragraphs=s_data["speech_paragraphs"],
            insights=s_data.get("insights"),
            warnings=s_data.get("warnings"),
            actions=s_data.get("actions")
        )

    # Save to workspace
    ws_doc = r"c:\Users\lap4all\Desktop\New folder\KICH_BAN_THUYET_TRINH_W40_NAM_TRUNG_BO.docx"
    ws_chuan = r"c:\Users\lap4all\Desktop\New folder\KICH_BAN_THUYET_TRINH_W40_CHUAN.docx"
    doc.save(ws_doc)
    doc.save(ws_chuan)
    print("Saved DOCX in workspace:", ws_doc)

    # Save to Downloads (new files that are NOT locked)
    dl_new = r"C:\Users\lap4all\Downloads\KICH_BAN_W40_MOI_NHAT.docx"
    dl_chuan = r"C:\Users\lap4all\Downloads\KICH_BAN_THUYET_TRINH_W40_CHUAN.docx"
    doc.save(dl_new)
    doc.save(dl_chuan)
    print("Saved DOCX in Downloads:", dl_new)

    # Try saving to the locked ones in case Word closed
    for p in [r"C:\Users\lap4all\Downloads\KICH_BAN_THUYET_TRINH_W40_NAM_TRUNG_BO.docx", r"C:\Users\lap4all\Downloads\kịch bản.docx"]:
        try:
            doc.save(p)
            print("Successfully overwritten:", p)
        except Exception as e:
            print("Cannot overwrite locked file (open in Word):", p)

    # Update HTML
    build_html_file(sections)
    # Update MD
    build_md_file(sections)

def build_html_file(sections):
    # build html
    from scratch.generate_w40_full_script import build_html_file as orig_build_html
    orig_build_html(sections)

def build_md_file(sections):
    from scratch.generate_w40_full_script import build_md_file as orig_build_md
    orig_build_md(sections)

if __name__ == "__main__":
    build_boss_script()
