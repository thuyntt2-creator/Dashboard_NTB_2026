import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

sys.path.insert(0, os.path.join(os.getcwd(), 'scratch'))
from doc_builder_helpers import format_run, add_callout_box

def build_w40_16_topics():
    doc = docx.Document()
    
    # 0.8 inch margins
    for s in doc.sections:
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.8)
        s.right_margin = Inches(0.8)
        
    # --- HEADER BLOCK ---
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
    r3 = p3.add_run("Kịch bản thuyết trình 16 chuyên đề điều hành chuẩn hóa — Chỉ số Tỉnh đặt lên đầu, phân tích sâu theo 18 AM & Giao việc hiện trường")
    format_run(r3, font_size_pt=11, italic=True, color_rgb=(0xEA, 0x58, 0x0C))

    sections_data = [
        # TOPIC 1
        {
            "sec_title": "📊 [I. TỔNG HỢP TRỌNG TÂM HỌP TUẦN W40 — VÙNG NAM TRUNG BỘ]",
            "speech_title": "🗣️ LỜI MỞ ĐẦU & TỔNG QUAN ĐIỀU HÀNH VÙNG TUẦN W40 (BẬT TAB 1 DASHBOARD):",
            "speech_paragraphs": [
                "📍 1. BẢNG 10 CHỈ SỐ NHANH TRÊN MÀN HÌNH DASHBOARD (W40 vs W39):",
                "• 1. Sản Lượng Full Hàng: 311.503 đơn (-19.810 đơn / -5,98% so với W39 331.313 đơn).",
                "• 2. Sản Lượng TikTok Shop: 72.253 đơn (-1.190 đơn / -1,62%), chiếm tỷ trọng 23,2% sản lượng toàn vùng.",
                "• 3. %GTC Full Hàng: 60,87% (+4,19%p so với W39 56,68%) ➔ Bứt phá ngoạn mục, chính thức vượt mốc trần 60%!",
                "• 4. %GTC TikTok Shop: 63,38% (+5,84%p so với W39 57,54%) ➔ Lập đỉnh cao nhất từ trước đến nay, vượt Full hàng +2,51%p.",
                "• 5. %ODR (Giao Đúng Hẹn): 93,12% (+2,28%p so với W39 90,84%) ➔ Vượt chuẩn cam kết SLA ≥ 92,0% (TTS đạt 94,18%).",
                "• 6. %LTC (Lấy Hàng Thành Công): 91,35% (+1,22%p so với W39 90,13%; riêng TTS duy trì xuất sắc 94,97%).",
                "• 7. %Rớt Luân Chuyển KTC: 1,69% (W39: 1,52%, tăng nhẹ +0,17%p; 219 đơn rớt / 12.934 đơn cần luân chuyển).",
                "• 8. %FD (Tỷ Lệ Hoàn Trả): 7,77% (W39: 7,54%, tăng nhẹ +0,23%p; riêng TTS kiểm soát rất tốt ở mức 6,10%).",
                "• 9. Tổng Cần Truy Thu: 187,1 Tr ₫ (2.424 bản ghi, giảm -125,0 Tr ₫ / -40,1% so với 312,1 Tr ₫ tuần W39).",
                "• 10. Tỷ Lệ Tiền Mặt COD: 40,4% (so với 40,1% W39, tăng nhẹ +0,2%p; tỷ lệ chuyển khoản QR đạt 59,6%).",
                "🎙️ LỜI THOẠI THUYẾT TRÌNH TỰ NHIÊN (KHI BẬT TAB 1 DASHBOARD TỔNG QUAN):",
                "\"Dạ em chào Ban Giám Đốc, chào các anh chị AM và các phòng ban.",
                "Mở đầu buổi họp giao ban tuần W40 (chu kỳ dữ liệu từ 28/09 đến 04/10/2026), kính mời Ban Giám Đốc và các anh chị cùng nhìn lên màn hình Dashboard Tổng quan giúp em.",
                "Tuần 40 này, toàn vùng Nam Trung Bộ của chúng ta có một bước chuyển mình rất ấn tượng về chất lượng dịch vụ Last-mile:",
                "Đầu tiên là điểm sáng rực rỡ nhất: Tỷ lệ Giao thành công (%GTC Full) tuần này đã chính thức phá mốc 60%, chạm mức 60,87%, tăng tới hơn 4,19%p so với tuần trước. Đặc biệt ở kênh TikTok Shop, %GTC đã bay thẳng lên 63,38%, tăng gần 6%p! Đây là kết quả của việc các anh chị AM đã siết rất chặt việc giải tỏa đơn tồn đầu ngày và tăng cường chuyến giao.",
                "Điểm sáng thứ hai là chỉ số Giao đúng hẹn %ODR: Sau nhiều tuần ngấp nghé 90-91%, tuần này toàn vùng đã vượt ngưỡng cam kết SLA 92%, vươn lên 93,12% (hàng TikTok đạt tới 94,18%). Khâu lấy hàng First-mile cũng duy trì rất đều tay trên 91,3%, riêng TikTok Shop đạt gần 95%.",
                "Tuy nhiên, chúng ta vẫn phải nhìn thẳng vào các nút thắt lớn cần giải quyết ngay:",
                "Thứ nhất: Sản lượng tuần này hạ nhiệt nhẹ về 311.503 đơn, giảm khoảng 6% so với tuần W39 do tuần cuối tháng thị trường có sự chững lại.",
                "Thứ hai: Khâu vận tải KTC đang có 124 chuyến xe chạy non tải dưới 30% thùng xe, làm giảm hiệu suất khai thác phương tiện đường trục.",
                "Thứ ba: Mặc dù tổng số tiền cần truy thu giảm 40% về 187,1 triệu đồng, nhưng số tiền phát sinh ban đầu lại tăng vọt lên 433,1 triệu đồng, nổi cộm lên vụ việc chiếm dụng tiền hàng 48,7 triệu đồng tại bưu cục Bắc Cam Ranh thuộc cụm AM Nguyễn Thanh Long và 419 ticket truy thu dồn ứ tại địa bàn AM Lê Văn Trường.",
                "Bây giờ, em xin phép bấm chuyển qua Tab 2 để đi sâu vào sản lượng từng Tỉnh và từng anh chị AM nha!\""
            ],
            "insights": [
                "%GTC Full phá vỡ mốc 60% (đạt 60,87%) và TTS đạt đỉnh 63,38% khẳng định kỷ luật xuất tuyến Last-mile đã có chuyển biến thực chất.",
                "%ODR toàn vùng vượt chuẩn SLA 92% (đạt 93,12%), khâu lấy hàng First-mile TikTok Shop đạt 94,97% giữ vững uy tín với các sàn TMĐT."
            ],
            "warnings": [
                "Phát sinh 433,1 Tr ₫ cước truy thu ban đầu; vụ việc liên đới chiếm dụng 48,7 Tr ₫ tại Bắc Cam Ranh là hồi chuông cảnh báo đỏ về đạo đức nghề nghiệp và kiểm soát nội bộ.",
                "124 chuyến xe KTC chạy non tải dưới 30% thùng làm xói mòn biên lợi nhuận vận hành của vùng."
            ],
            "actions": [
                "Tuần W41 tập trung 3 mũi nhọn: Truy thu dứt điểm 187,1 Tr ₫ công nợ, tối ưu gộp chuyến 124 xe KTC non tải và cứu vãn ODR tại các bưu cục vùng sâu."
            ]
        },

        # TOPIC 2
        {
            "sec_title": "📦 [II. PHÂN TÍCH SẢN LƯỢNG GIAO TOÀN VÙNG, 5 TỈNH THÀNH & 18 AM (W40)]",
            "speech_title": "🗣️ PHÂN TÍCH SẢN LƯỢNG GIAO 5 TỈNH & BIẾN ĐỘNG THEO 18 AM (TAB 2):",
            "speech_paragraphs": [
                "📍 1. BẢNG SỐ LIỆU 5 TỈNH THÀNH TUẦN W40 (W40 vs W39):",
                "• Khánh Hòa: 84.777 đơn Full (giảm -10.304 đơn / -10,8% WoW) | TikTok Shop: 15.921 đơn (-2.784 đơn). Giữ vị trí số 1 sản lượng toàn vùng.",
                "• Bình Thuận: 83.686 đơn Full (tăng +2.869 đơn / +3,5% WoW) | TikTok Shop: 22.331 đơn (tăng mạnh +4.185 đơn / +23,1%!). Bứt phá ngoạn mục.",
                "• Lâm Đồng: 77.719 đơn Full (giảm -10.581 đơn / -12,0% WoW) | TikTok Shop: ~14.125 đơn. Giảm tải sau đợt cao điểm.",
                "• Ninh Thuận: 33.549 đơn Full (tăng +307 đơn / +0,9% WoW) | TikTok Shop: 11.156 đơn (tăng mạnh +2.863 đơn / +34,5%!).",
                "• Đắk Nông: 31.772 đơn Full (giảm -2.112 đơn / -6,2% WoW) | TikTok Shop: 8.720 đơn (-296 đơn / -3,3%).",
                "📍 2. BIẾN ĐỘNG THEO 18 AM:",
                "• Nhóm tăng trưởng tốt: AM Lê Thanh Nhựt (30.386 đơn, +1.316 đơn), AM Nguyễn Ngọc Khánh (27.379 đơn, +1.137 đơn), AM Cao Thị Thanh Thủy (16.786 đơn, +545 đơn), AM Nguyễn Thị Tuyết Thơ (9.296 đơn, +463 đơn), AM Nguyễn Duy Long (42.684 đơn, +178 đơn, đầu tàu tải lớn nhất vùng).",
                "• Nhóm giảm sâu: AM Thái Thị Thanh Thư (27.165 đơn, -7.600 đơn WoW), AM Lê Văn Trường (17.707 đơn, -4.544 đơn WoW), AM Hồng Bích Nga (17.961 đơn, -2.561 đơn WoW), AM Phan Nguyễn Yến Nhi (2.433 đơn, -2.104 đơn), AM Nguyễn Thanh Long (11.220 đơn, -1.974 đơn), AM Nguyễn Lê Nguyên Vũ (10.173 đơn, -1.973 đơn).",
                "🎙️ LỜI THOẠI THUYẾT TRÌNH TỰ NHIÊN (KHI BẬT TAB 2 SẢN LƯỢNG — 3 CHARTS):",
                "\"Dạ qua tới Tab 2 Sản Lượng, mời mọi người nhìn vào biểu đồ 5 Tỉnh ở trên cùng:",
                "Tuần W40 này, bức tranh sản lượng có sự phân hóa rất rõ nét giữa Duyên hải và Tây Nguyên:",
                "Điểm sáng lớn nhất thuộc về Bình Thuận và Ninh Thuận: Trong khi cả nước giảm đơn cuối tháng thì Bình Thuận lại tăng thêm gần 2.900 đơn Full và bùng nổ đơn TikTok Shop lên hơn 22 ngàn đơn, tăng tới hơn 4.100 đơn sàn (+23%)! Ninh Thuận của anh Nhựt cũng tăng tới 34% đơn TikTok. Đơn sàn TMĐT đổ về Bình Thuận và Ninh Thuận cực kỳ mạnh mẽ.",
                "Ngược lại, 2 địa bàn giảm sâu nhất tuần này là Khánh Hòa (giảm hơn 10 ngàn đơn) và Lâm Đồng (giảm hơn 10 ngàn đơn).",
                "Soi vào chi tiết 18 AM bên dưới:",
                "Em xin tuyên dương anh Long Bình Thuận: Vẫn luôn là đầu tàu gánh tải lớn nhất vùng với gần 43 ngàn đơn, và tuần này anh Long dẫn đầu toàn vùng khi kéo về hơn 22 ngàn đơn TikTok Shop cho tỉnh nhà!",
                "Anh Nhựt ở Ninh Thuận và anh Khánh ở Bình Thuận tuần này cũng làm rất xuất sắc, tăng trưởng trên 1.100 đến 1.300 đơn mỗi người.",
                "Tuy nhiên, có 2 điểm báo động về sản lượng cần lưu ý:",
                "Thứ nhất là cụm của chị Thư ở Khánh Hòa: Tuần trước chị Thư tăng mạnh thì tuần này lại sụt giảm tới 7.600 đơn (-21,8%). Chị Thư cần rà soát lại xem có shop lớn nào tại Nha Trang bị đối thủ kéo đi hay do bưu cục chia lại tuyến giao.",
                "Thứ hai là anh Trường ở Lâm Đồng: Giảm tiếp hơn 4.500 đơn. Địa bàn của anh Trường đang dính nhiều đơn tồn và ODR thấp, khi giao trễ khách hàng họ sẽ hủy đơn và shop sẽ có tâm lý giảm gửi qua GHN.",
                "Bây giờ em xin phép chuyển sang Tab 3 để xem tỷ lệ Giao thành công (%GTC) của từng tỉnh và từng AM nhé!\""
            ],
            "insights": [
                "Bình Thuận và Ninh Thuận bùng nổ sản lượng TikTok Shop (+23% đến +34% WoW), chứng minh sức mua online tại thị trường ven biển đang tăng rất mạnh.",
                "Khánh Hòa và Lâm Đồng giảm đồng thời hơn 20 ngàn đơn, cảnh báo nguy cơ mất thị phần tại các trung tâm thành phố lớn."
            ],
            "warnings": [
                "AM Thái Thị Thanh Thư sụt giảm 7.600 đơn và AM Lê Văn Trường sụt giảm 4.544 đơn cần phải được điều tra nguyên nhân ngay trong đầu tuần.",
                "Đắk Nông sản lượng tiếp tục giảm tuần thứ 3 liên tiếp (xuống 31,7k đơn), cần kích hoạt lại đội ngũ kinh doanh bưu cục huyện."
            ],
            "actions": [
                "AM Thư và AM Trường rà soát ngay danh sách top 20 khách hàng gửi lớn nhất trên địa bàn để nắm rõ lý do sụt giảm sản lượng."
            ]
        },

        # TOPIC 3
        {
            "sec_title": "🎯 [III. PHÂN TÍCH HIỆU SUẤT %GTC TỔNG TOÀN MẠNG THEO 18 AM & 5 TỈNH (W40)]",
            "speech_title": "🗣️ ĐÁNH GIÁ TỶ LỆ GIAO THÀNH CÔNG (%GTC) VÀ ĐỘ LỆCH THEO TỈNH & AM (TAB 3):",
            "speech_paragraphs": [
                "📍 1. BẢNG %GTC TỔNG THEO 5 TỈNH THÀNH (W40 vs W39):",
                "• Ninh Thuận: 67,49% (W39: 67,96%) ➔ Duy trì vị trí số 1 toàn vùng, tỷ lệ giao hoàn tất cực kỳ ổn định.",
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
                "🎙️ LỜI THOẠI THUYẾT TRÌNH TỰ NHIÊN (KHI BẬT TAB 3 %GTC TỔNG):",
                "\"Dạ mời Ban Giám Đốc nhìn tiếp sang Tab 3 về %GTC Tổng toàn mạng:",
                "Nhìn vào 5 Tỉnh thành ở bảng trên cùng:",
                "Bình Thuận vẫn giữ vững tỷ lệ với GTC 67,5%, cho thấy ae khu vực tại Bình Thuận chạy tuyến rất đều và khách nhận hàng rất chuẩn.",
                "Khánh Hòa và Ninh Thuận tuần này đã xuất sắc vượt qua mốc 60%. Đặc biệt Khánh Hòa tăng từ 58,8% lên 62,2%, đóng góp cực lớn vào tỷ lệ gtc chung của vùng.",
                "Hai tỉnh Đắk Nông và Lâm Đồng: Dù vẫn đứng ở 2 vị trí cuối bảng với 54,4%, nhưng tuần này anh em đã có sự nỗ lực. Lâm Đồng kéo tăng tới hơn 7,0%p, còn Đắk Nông tăng 5,7%p so với tuần trước. Về phần này có sự tuyên dương nỗ lực của các AM khu vực 2 tỉnh ĐN và LĐ.",
                "Nhìn xuống danh sách 18 AM:",
                "Top 1 GTC full hàng tuần này thuộc về kv AM Nguyễn Ngọc Khánh với tỷ lệ 74,5%, kế đến là chị Thái Thị Thanh Thư (Khánh Hòa) đạt 72,0% và anh Nguyễn Đỗ Minh Nghĩa (Lâm Đồng) đạt 70,4%.",
                "Đặc biệt, AM Duy Long tiếp tục là AM sản lượng lớn nhất toàn vùng, nhưng vẫn duy trì %GTC rất vững vàng ở mức 69,0%!",
                "Tuần này toàn vùng tăng mạnh +4,19%p KHÔNG PHẢI nhờ nhóm ven biển (vì Bình Thuận và Ninh Thuận đã ở mức trần nên đi ngang ~67,5%), mà công lớn nhất kéo cả vùng bứt phá tuần này thuộc về 3 AM có bước nhảy vọt thần tốc:",
                "Thứ nhất là chị Thái Thị Thanh Thư ở Khánh Hòa: Tăng vọt tới gần +10%p (từ 62,4% lên 72,0%) trên khối lượng gần 36 ngàn đơn, đưa chị Thư lên thẳng vị trí Á quân GTC toàn vùng và kéo bừng sáng cả tỉnh Khánh Hòa!",
                "Thứ hai là anh Lê Văn Trường ở Lâm Đồng: Tăng phi thường +11,9%p (từ 37,1% lên 49,0%) trên khối lượng cực lớn hơn 37 ngàn đơn! Chính anh Trường là đầu tàu kéo Lâm Đồng tăng hơn 7%p tuần này!",
                "Thứ ba là anh Trương Quang Linh ở Đắk Nông: Tăng bứt phá mạnh nhất toàn vùng với +14,5%p (từ 25,8% lên 40,3%). Bên cạnh đó, anh Vũ (+7,5%p), chị Nhi (+9,0%p) và chị Nhung (+3,5%p trên 37 ngàn đơn) cũng là những nhân tố nòng cốt kéo toàn bộ khu vực Tây Nguyên thoát đáy!",
                "Trong đó, anh Nguyễn Thanh Long ở Cam Ranh tăng trưởng kỷ lục +14,84%p GTC TTS, anh Lê Văn Trường kéo GTC TTS Lâm Đồng tăng tới hơn +10,3%p, và anh Nguyễn Duy Long tiếp tục là 'lá chắn thép' khi gánh tới gần 19 ngàn đơn TikTok Shop mà vẫn duy trì GTC TTS chuẩn đét ở mức 69,42%!",
                "Quán quân GTC TikTok Shop tuần này thuộc về anh Nguyễn Ngọc Khánh (75,56%) và anh Nguyễn Đỗ Minh Nghĩa (70,77%).",
                "Tuy nhiên, Ban Giám Đốc lưu ý giúp em nhóm các AM vẫn còn nằm dưới mốc 50% GTC: Dù anh Lợi (36,5%), chị Nhi (38,0%) và anh Linh (40,3%) đã có tiến bộ vượt bậc, nhưng GTC tuyệt đối vẫn còn dưới mốc 50%, shipper vẫn chưa linh hoạt đổi ca phát chiều tối.",
                "Em đề nghị trong tuần này, các AM nhóm dưới phải ngồi lại với từng bưu cục để tối ưu lại ca phát chiều. Giờ em xin chuyển qua Tab 4 mổ xẻ Ca 1 TikTok Shop ạ!\""
            ],
            "insights": [
                "Động lực tăng trưởng GTC tuần W40 (+4,19%p toàn vùng) chủ yếu đến từ sự bứt phá của AM Lê Văn Trường (+11,85%p / 37,4k đơn) và AM Thái Thị Thanh Thư (+9,63%p / 35,9k đơn).",
                "Kênh TikTok Shop đạt đỉnh 63,38% GTC (tăng +5,84%p WoW), trong đó Lâm Đồng bứt phá +10,36%p và Đắk Nông tăng +6,32%p."
            ],
            "warnings": [
                "6 AM (Lợi, Nhi, Linh, Duân, Trường, Vũ) vẫn chìm dưới 50% GTC, kéo tụt mặt bằng chung và làm tăng tỷ lệ hàng dồn tồn kho."
            ],
            "actions": [
                "Các AM nhóm dưới rà soát lộ trình di chuyển của bưu tá, bắt buộc gán phát chuyến 2 đối với các đơn chưa liên lạc được buổi sáng."
            ]
        },

        # TOPIC 4
        {
            "sec_title": "🔥 [IV. PHÂN TÍCH CHUYÊN SÂU %GTC CA 1 TIKTOK SHOP (TARGET SLA ≥ 76.0%) (W40)]",
            "speech_title": "🗣️ HIỆU SUẤT GIAO CA 1 TIKTOK SHOP (81.34% VƯỢT SLA 76%) & 19 AM (TAB 4):",
            "speech_paragraphs": [
                "📍 1. HIỆU SUẤT TOÀN VÙNG VÀ BẢNG 5 TỈNH THÀNH (W40 vs W39):",
                "• Toàn vùng TTS Ca 1: Bứt phá ngoạn mục đạt 81,34% (tăng mạnh +6,17%p WoW so với W39: 75,16%) ➔ Chính thức vượt xa Target cam kết SLA ≥ 76.0%!",
                "• Bình Thuận: 86,45% (W39: 84,64%, +1,81%p) ➔ Quán quân Ca 1 TTS toàn vùng, giữ phong độ đỉnh cao.",
                "• Ninh Thuận: 83,78% (W39: 84,75%) ➔ Á quân toàn vùng, tỷ lệ hoàn tất ca sáng rất chuẩn.",
                "• Lâm Đồng: 80,22% (W39: 66,85%, tăng bùng nổ +13,37%p!) ➔ Lần đầu tiên vượt ngưỡng chuẩn SLA 80%!",
                "• Khánh Hòa: 80,15% (W39: 75,77%, tăng +4,37%p) ➔ Chính thức gia nhập nhóm xuất sắc >80%.",
                "• Đắk Nông: 72,78% (W39: 67,81%, tăng mạnh +4,97%p) ➔ Rút ngắn khoảng cách chỉ còn thiếu 3,2%p để đạt SLA.",
                "📍 2. XẾP HẠNG 19 AM THEO %GTC CA 1 TIKTOK SHOP (TARGET SLA ≥ 76.0%):",
                "• Tỷ lệ đạt chuẩn: Đã có 14/19 AM xuất sắc đạt và vượt Target SLA ≥ 76.0% (nhuộm xanh bảng điều hành).",
                "• Top 5 AM dẫn đầu %GTC Ca 1 TTS: 🥇 AM Nguyễn Ngọc Khánh (88,94%), 🥈 AM Nguyễn Đỗ Minh Nghĩa (87,02%), 🥉 AM Cao Thị Thanh Thủy (87,01%), 👑 AM Nguyễn Duy Long (85,05% — gánh hơn 10 ngàn đơn Ca 1: 10.257 đơn), 5️⃣ AM Nguyễn Thị Tuyết Thơ (83,20%).",
                "• Top AM tăng trưởng Ca 1 TTS bứt phá nhất (Δ WoW): 🚀 AM Lê Văn Trường tăng vọt +24,72%p (từ 55,56% lên 80,28%, vượt chuẩn 76%!), 🚀 AM Trương Quang Linh (+18,94%p), 🚀 AM Phan Nguyễn Yến Nhi (+16,65%p), 🚀 AM Nguyễn Thanh Long (+16,40%p, lên 82,98%).",
                "• Nhóm 5 AM chưa đạt Target SLA 76% (cần thúc đẩy gấp): Huỳnh Thúc Duân (64,52%), Nguyễn Lê Nguyên Vũ (61,43%), Phan Nguyễn Yến Nhi (58,62%), Trương Quang Linh (58,14%), Lê Minh Lợi (46,67%).",
                "🎙️ LỜI THOẠI THUYẾT TRÌNH TỰ NHIÊN (KHI BẬT TAB 4 %GTC TTS CA 1):",
                "\"Dạ mời Ban Giám Đốc và các anh chị nhìn lên màn hình Tab 4: Phân tích chuyên sâu %GTC TikTok Shop Ca 1:",
                "Tuần W40 này ghi nhận một kỳ tích rất lớn của toàn vùng Nam Trung Bộ:",
                "Hiệu suất giao hàng sàn TikTok Shop chuyến sáng Ca 1 đã chính thức vượt xa cam kết SLA 76% khi bứt phá lên tới 81,34% (tăng mạnh tới +6,17%p so với mức 75,16% của tuần W39)!",
                "Nhìn vào 5 Tỉnh thành:",
                "Bình Thuận (86,5%) và Ninh Thuận (83,8%) tiếp tục giữ vững vị thế dẫn đầu. Nhưng điều đáng mừng nhất là tuần này cả Lâm Đồng (80,2%) và Khánh Hòa (80,2%) đều đã xuất sắc kéo GTC Ca 1 sàn vượt qua ngưỡng 80%!",
                "Đặc biệt, Lâm Đồng đã có bước nhảy vọt phi thường khi tăng hơn +13,3%p so với tuần trước.",
                "Nhìn vào bảng 19 AM bên dưới:",
                "Chúng ta đã có 14 trên tổng số 19 AM đạt chuẩn xanh ≥ 76%. Quán quân thuộc về anh Nguyễn Ngọc Khánh đạt 88,9%, anh Nguyễn Đỗ Minh Nghĩa đạt 87,0% và chị Cao Thị Thanh Thủy đạt 87,0%.",
                "Đặc biệt, em xin tuyên dương anh Nguyễn Duy Long: Một mình anh Long gánh khối lượng Ca 1 TTS khổng lồ với hơn 10 ngàn đơn (10.257 đơn, chiếm gần 1/4 sản lượng Ca 1 toàn vùng) nhưng vẫn đạt tỷ lệ xuất sắc lên tới 85,05%!",
                "Bên cạnh đó, anh Lê Văn Trường ở Lâm Đồng đã có cú lội ngược dòng ngoạn mục nhất khi kéo GTC Ca 1 TTS tăng gần +25%p (từ 55,6% nhảy vọt lên 80,3%), đưa địa bàn Đà Lạt từ điểm nóng cảnh báo trở thành điểm đạt chuẩn SLA!",
                "Tuy nhiên, trên biểu đồ mọi người thấy vẫn còn 5 AM hiển thị màu đỏ dưới mốc 76%:",
                "Đó là chỗ anh Duân (64,5%), anh Vũ (61,4%), chị Nhi (58,6%), anh Linh (58,1%) và anh Lợi (46,7%).",
                "Bản chất hiện trường ở đây là: GTC Ca 1 thuần đạt đỉnh 81,34%, nhưng nếu tính cả đơn tồn thì chỉ còn 66,47% (rơi tới gần 15%p)! Shipper buổi sáng vẫn còn thói quen lựa các kiện hàng mới về giao trước, dồn hàng tồn hôm trước xuống đáy sọt. Em đề nghị 5 AM nhóm dưới phải quán triệt bưu tá: Hàng cũ tồn hôm qua phải được gán và mang đi phát ngay chuyến đầu trước 8h30 sáng! Giờ em xin chuyển qua Tab 5 mổ xẻ Tỷ lệ gán vận hành ạ!\""
            ],
            "insights": [
                "GTC Ca 1 TikTok Shop đạt kỷ lục 81,34% (tăng +6,17%p WoW), chính thức đưa toàn vùng vượt qua cam kết SLA ≥ 76.0% với sàn TMĐT.",
                "Khoảng cách giữa Ca 1 thuần (81,34%) và Ca 1 có tồn (66,47%) lên tới 14,87%p, chứng minh hàng tồn chính là hố đen kéo tụt GTC cuối ngày."
            ],
            "warnings": [
                "Vẫn còn 5 AM (Duân, Vũ, Nhi, Linh, Lợi) dưới ngưỡng 76%, trong đó AM Lê Minh Lợi mới đạt 46,67%."
            ],
            "actions": [
                "Trưởng bưu cục bắt buộc phải kiểm tra sọt hàng của shipper trước khi xuất bến lúc 08h30: 100% đơn tồn hôm trước phải được xếp lên trên cùng để phát trước 10h30."
            ]
        },

        # TOPIC 5: TỶ LỆ GÁN
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
                "🎙️ LỜI THOẠI THUYẾT TRÌNH TỰ NHIÊN (KHI BẬT TAB 5 % GÁN):",
                "\"Dạ tiếp theo em xin mời Ban Giám Đốc và các anh chị cùng nhìn sang Tab 5 về Tỷ lệ Gán vận hành:",
                "Nhìn vào Bảng 1 tổng quan toàn vùng tuần W40:",
                "Tỷ lệ gán tổng của vùng mình đạt 86,3%, tăng gần 4%p so với tuần trước, riêng đơn sàn TikTok Shop được ưu tiên gán đạt tới 88,0%.",
                "Đặc biệt, ở chuyến sáng đầu ngày — tức là Ca 1 + Hàng Tồn — toàn vùng đạt tới 92,8% ở hàng Full và 94,8% ở TikTok Shop. Điều này chứng minh nỗ lực của các AM trong việc thúc ép bưu cục quét gán sạch kho trước 8h30 sáng đã phát huy tác dụng rõ rệt.",
                "Nhìn sang Bảng 2 (Xếp hạng AM theo tỷ lệ Gán Ca 1 + Tồn):",
                "Nhóm dẫn đầu giữ vững phong độ đỉnh cao trên 98%: Anh Nghĩa (99,1%), anh Khánh (98,9%), anh Nhựt (98,9%), chị Thư (98,4%) và chị Thủy (98,0%). Anh Long Ninh Thuận gánh tải khổng lồ nhưng gán sáng vẫn đạt chuẩn đét 97,0%!",
                "Đặc biệt, em xin tuyên dương sự bứt phá của 3 AM nhóm dưới: Chị Yến Nhi và anh Linh tăng vọt hơn +22%p, anh Lê Văn Trường tăng hơn +21%p! Tuần trước 3 anh chị chỉ gán được 58 - 61% thì tuần này đã kéo lên trên 80% - 83%, giúp giải phóng một lượng hàng tồn cực lớn ngay từ đầu ngày.",
                "TUY NHIÊN, KHI NHÌN XUỐNG BẢNG 3 (TỶ LỆ GÁN TỔNG CẢ NGÀY), NÚT THẮT LỘ RA RẤT RÕ:",
                "Trong khi gán sáng đạt gần 93%, thì gán tổng cả ngày của vùng mình vẫn bị kẹt ở mức 86,3%, chưa chạm được mục tiêu 90%.",
                "Bởi vì tỷ lệ gán của chuyến chiều (Ca 2) chỉ đạt 62,9% — tức là cứ 100 đơn hàng về kho ca trưa thì có tới gần 38 đơn bị 'ém' lại bưu cục, không được gán ra cho bưu tá mang đi phát!",
                "Điển hình như anh Duân (75,5%), chị Chi (77,6%), anh Lợi (78,2%) và anh Thanh Long (79,7%) vẫn còn nằm dưới mốc 80% gán tổng.",
                "Bản chất hiện trường ở đây là: Chuyến xe tải KTC trưa về đúng giờ nhân viên bưu cục đi ăn cơm trưa (12h30 - 13h30). Đến 14h00 bưu tá chuẩn bị xuất tuyến thì hàng trưa vẫn nằm nguyên trong bao tải chưa bắn phân tuyến. Bưu tá không có hàng mới để đi, chỉ mang lèo tèo vài đơn hẹn sáng rồi về sớm lúc 16h30, bỏ lỡ mất khung giờ vàng khách ở nhà nhận hàng (16h30 - 18h30).",
                "Em đề nghị tuần W41, các anh Duân, Chi, Lợi, Thanh Long: Bắt buộc bưu cục phải bố trí 1 nhân sự trực trưa từ 13h00 bắn phân loại hàng ngay khi xe KTC hạ tải, đảm bảo đúng 14h00 bưu tá có hàng mới xuất tuyến ca 2, kéo tỷ lệ gán Ca 2 lên trên 75% giúp em! Giờ em xin chuyển qua Tab 6 về ODR ạ!\""
            ],
            "insights": [
                "Gán Ca 1 + Tồn đạt 92,77% (TTS đạt 94,80%) chứng minh kỷ luật quét kho đầu ngày đã được chuẩn hóa.",
                "Tỷ lệ gán Ca 2 mới đạt 62,87% là nguyên nhân chính khiến 37% lượng hàng ca trưa bị biến thành hàng tồn sang ngày hôm sau."
            ],
            "warnings": [
                "Bưu cục không gán hàng ca trưa làm lãng phí khung giờ vàng 16h30 - 18h30 khi tỷ lệ khách ở nhà nhận hàng đạt cao nhất trong ngày."
            ],
            "actions": [
                "Bắt buộc bưu cục bố trí nhân sự trực trưa từ 13h00; AM kiểm tra tỷ lệ gán Ca 2 trên hệ thống lúc 14h15 hàng ngày, yêu cầu đạt tối thiểu 75%."
            ]
        },

        # TOPIC 6: ODR
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
                "• Nhóm dẫn đầu giữ chuẩn ODR xuất sắc trên 96% - 97% (Bảng 3 & 4): Chị Cao Thị Thanh Thủy (97,8% Full | 97,6% TTS), anh Nguyễn Ngọc Khánh (97,4% Full | 98,2% TTS), chị Thái Thị Thanh Thư (96,9%), anh Nguyễn Duy Long (96,6% Full | 97,2% TTS trên gần 13k đơn GTC), anh Nguyễn Hoàng Phi (96,6%).",
                "• Bứt phá tiến bộ: Chị Phan Nguyễn Yến Nhi (+8,76%p lên 76,1%), anh Nguyễn Thanh Long (+8,20%p lên 92,3%), anh Nguyễn Lê Nguyên Vũ (+6,79%p lên 87,2%).",
                "• 🔴 BÁO ĐỘNG ĐỎ — TỬ HUYỆT ODR TIKTOK SHOP VÙNG CAO (BẢNG 4 DB):",
                "  1. Lê Văn Trường: 62,13% (rơi tự do -17,39%p WoW).",
                "  2. Phan Nguyễn Yến Nhi: 44,57% (rơi tự do -22,39%p WoW).",
                "  3. Trương Quang Linh: 42,00% (rơi tự do -33,99%p WoW).",
                "  4. Lê Minh Lợi: 14,29% (rơi -27,24%p WoW).",
                "🎙️ LỜI THOẠI THUYẾT TRÌNH TỰ NHIÊN (KHI BẬT TAB 6 ODR):",
                "\"Dạ tiếp theo em xin chuyển sang Tab 6 là chỉ số Giao đúng hẹn %ODR:",
                "Nhìn vào Bảng 1 và Bảng 2 ở trên cùng: Tuần này toàn vùng mình có bước tiến rất dài khi chính thức vượt qua chuẩn cam kết SLA 92%, đạt 93,12% ở hàng Full và 94,18% ở kênh TikTok Shop!",
                "Ba tỉnh ven biển tiếp tục là 'bức tường thành' vững chắc: Bình Thuận dẫn đầu vùng với 96,7%, Khánh Hòa bứt phá lên 95,6% và Ninh Thuận đạt 94,2%.",
                "Nhìn xuống danh sách AM ở Bảng 3: Chị Cao Thị Thanh Thủy xuất sắc giữ vị trí Quán quân ODR toàn vùng với 97,8%, anh Khánh đạt 97,4%, chị Thư 96,9% và anh Long Ninh Thuận đạt 96,6%. Gần như 100 đơn xuất kho là giao đúng hẹn cho khách 97 - 98 đơn. Tuần này cũng biểu dương anh Thanh Long (+8,2%p) và chị Nhi (+8,8%p) đã có sự cải thiện ODR Full rất tích cực.",
                "NHƯNG EM XIN PHÉP GIÓNG HỒI CHUÔNG CẢNH BÁO ĐỎ KHI NHÌN VÀO BẢNG 4 (ODR TIKTOK SHOP):",
                "Trong khi ODR TTS toàn vùng đạt hơn 94%, thì tại 4 cụm Tây Nguyên của anh Trường, chị Nhi, anh Linh và anh Lợi, ODR TikTok Shop đang bị 'vỡ trận' nghiêm trọng:",
                "Anh Lê Văn Trường tụt xuống 62,1% (rơi -17,4%p), chị Phan Nguyễn Yến Nhi tụt xuống 44,6% (rơi -22,4%p), anh Trương Quang Linh tụt xuống 42,0% (rơi -34,0%p), và anh Lê Minh Lợi tụt xuống mức đáy không tưởng là 14,3%!",
                "Bản chất hiện trường ở đây là: Đơn sàn TikTok Shop có thời hạn cam kết giao siêu ngặt (tối đa 48h). Các bưu cục Quảng Tín, Đơn Dương, Lang Biang địa bàn rộng, đường đèo dốc xa 20-30km. Bưu tá ngại đi tuyến xa nên dồn hàng 2-3 ngày mới đi một chuyến. Hàng nằm ở kho quá 48h là hệ thống sàn tự động quét lỗi trễ hẹn ODR hàng loạt.",
                "Em yêu cầu anh Trường, chị Nhi, anh Linh và anh Lợi: Phải kích hoạt ngay danh sách 'Đơn cận giờ SLA' trên App bưu cục, đơn nào còn dưới 12 tiếng hết hạn phải ưu tiên mang đi phát ngay chuyến đầu sáng, kéo ODR TTS tuần tới vượt lên trên 75% giúp em!\""
            ],
            "insights": [
                "Khối Duyên hải (Bình Thuận, Khánh Hòa, Ninh Thuận) duy trì ODR trên 95% - 97% là chốt chặn bảo vệ uy tín thương hiệu GHN.",
                "ODR TikTok Shop tại 4 AM Tây Nguyên rơi xuống 14% - 62% do bưu tá dồn tuyến gom đơn 2-3 ngày mới đi phát một lần."
            ],
            "warnings": [
                "Sàn TikTok Shop tự động phạt gậy vi phạm và cắt luồng đơn các shop có tỷ lệ ODR dưới 80%."
            ],
            "actions": [
                "Cài đặt cảnh báo đơn cận hạn SLA 12h trên app bưu tá; bưu tá tuyến huyện bắt buộc gọi điện hẹn giờ với người nhận trước khi xuất phát."
            ]
        },

        # TOPIC 7: LTC
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
                "🎙️ LỜI THOẠI THUYẾT TRÌNH TỰ NHIÊN (KHI BẬT TAB 7 LTC):",
                "\"Dạ qua tới Tab 7 Lấy hàng First-mile, em xin báo cáo một kết quả rất đáng mừng:",
                "Toàn vùng tuần này tiếp tục duy trì phong độ lấy hàng rất cao, đạt 91,35% với Full hàng và gần 95% với đơn TikTok Shop!",
                "Cả 5 tỉnh đều làm rất tốt. Đặc biệt anh Nhựt với anh Nghĩa ở Ninh Thuận lấy hàng đạt đỉnh 97,6%. Shipper Ninh Thuận kết nối với các shop bán nho, tỏi, hải sản rất thân thiết, nhận đơn lấy là có mặt gom hàng ngay trong vòng 2 tiếng.",
                "Đắk Nông và Bình Thuận tuần này cũng tăng hơn 3,5%p, đưa tỷ lệ lấy hàng của vùng lên mức an toàn.",
                "Điểm cần lưu ý duy nhất ở khâu lấy hàng: Là tại các huyện miền núi của Lâm Đồng và Đắk Nông, một số shop nông sản đóng hàng muộn sau 17h00. Shipper bưu cục huyện ngại chạy xa vào rẫy nên xin shop dời sang sáng mai lấy.",
                "Việc dời đơn lấy này rất nguy hiểm với đơn TikTok Shop vì sàn tính giờ bàn giao (Handover SLA) rất ngặt. Em nhờ anh Tiến và anh Linh bố trí xe tải nhỏ hoặc shipper chuyên trách gom hàng chiều muộn cho các shop lớn nha!\""
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

        # TOPIC 8: OPR TTS
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
                "🎙️ LỜI THOẠI THUYẾT TRÌNH TỰ NHIÊN (KHI BẬT TAB 8 OPR TTS):",
                "\"Dạ qua tới Tab 8 về chỉ số OPR TikTok Shop — Tỷ lệ xử lý đơn đúng cam kết theo khung giờ tạo đơn của sàn:",
                "Mời mọi người nhìn vào sự tương phản một trời một vực giữa Ca Ngày và Ca Đêm trên màn hình:",
                "Ở Bảng 1 (Ca ngày từ 9h đến 19h), tất cả các AM đều làm cực kỳ xuất sắc, tỷ lệ đạt từ 88% đến 99%. Anh Duy đạt 99,0%, anh Vũ 99,1%, chị Thơ 98,8%, anh Long 97,3% và anh Khánh tăng vọt lên 95,0%. Chứng tỏ ban ngày quy trình bắn in bill và đóng gói của bưu cục rất trơn tru.",
                "THẾ NHƯNG, KHI BẬT SANG BẢNG 2 (CA ĐÊM TỪ 19H TỐI ĐẾN 9H SÁNG HÔM SAU):",
                "Biểu đồ ca đêm đang báo động đỏ rực toàn vùng:",
                "Anh Huỳnh Thúc Duân: 0,00% (0 trên 63 đơn xử lý kịp giờ)! Chị Trần Thị Nhung: 0,74% (chỉ có 1 trên 131 đơn kịp giờ)! Anh Lê Văn Trường: 24,0% (dính tới 371 đơn trễ giờ đêm)! Anh Nguyễn Đỗ Minh Nghĩa: 25,4%! Anh Nguyễn Hoàng Phi: 34,5%!",
                "Bản chất hiện trường ở đây là gì? Khách lướt livestream đặt hàng nhiều nhất là từ 20h đến 23h đêm. Theo chuẩn SLA, sáng hôm sau bưu cục phải hoàn tất xử lý trước 9h00.",
                "Thế nhưng 18h30 nhân viên bưu cục tắt máy khóa cửa đi về. Sáng hôm sau 8h00 - 8h30 mới tới mở cửa, đến 9h00 vẫn chưa ngồi vào máy tính quét in bill. Đơn hàng bị quá hạn OPR ngay từ lúc chưa rời khỏi kho bưu cục!",
                "Em đề nghị các anh Duân, Nhung, Trường, Nghĩa, Phi: Bắt buộc bưu cục phải phân công nhân sự mở cửa ca sáng từ 7h00 - 7h30 sáng, quét in bill sạch toàn bộ đơn livestream đêm trước 8h30 sáng để kéo OPR ca đêm vượt trên 65% giúp em!\""
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

        # TOPIC 9: RỚT LC
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
                "🎙️ LỜI THOẠI THUYẾT TRÌNH TỰ NHIÊN (KHI BẬT TAB 9 RỚT LUÂN CHUYỂN):",
                "\"Dạ qua tới Tab 9 về Rớt Luân Chuyển KTC:",
                "Tuần W40 này toàn vùng mình rớt 219 đơn, tương ứng tỷ lệ 1,69%, tăng nhẹ so với mức 1,52% tuần trước nhưng cơ bản vẫn giữ được dưới trần khống chế 1,8% của công ty.",
                "Hai tỉnh ven biển làm rất chuẩn chỉ là Bình Thuận (0,28%) và Khánh Hòa (0,48%), chị Thủy và chị Chi đạt tuyệt đối 0% rớt hàng.",
                "Tuy nhiên, nhìn vào con số tuyệt đối 219 đơn bị rớt lại trong tuần: Hơn một nửa số đơn rớt nằm trọn ở tỉnh Lâm Đồng (121 đơn) và 60 đơn nằm ở Ninh Thuận!",
                "Soi vào Bảng 1 và Bảng 3, 'ổ rớt xe' tập trung vào 4 AM: Chị Hồng Bích Nga (4,63%), chị Nguyễn Thị Tuyết Thơ (4,24%), anh Nguyễn Duy Long (rớt 60 đơn — nhiều nhất vùng) và anh Lê Văn Trường (2,77%).",
                "Nguyên nhân ở đây là gì? Bưu cục gom hàng First-mile về muộn sau 17h30. Nhân viên đóng bao bắn tải lề mề. Khi xe tải KTC theo lịch trình ghé bưu cục, bưu cục chưa niêm phong seal xong. Tài xế chờ 15 phút buộc phải chạy để kịp giờ cập Hub trung chuyển, bỏ lại các bao hàng nằm đắp chiếu ở góc bưu cục!",
                "Đơn bị rớt xe KTC là tự động trôi thêm 24 tiếng, hôm sau giao chắc chắn dính trễ SLA và khách hủy đơn.",
                "Em đề nghị chị Nga, chị Thơ, anh Long và anh Trường: Bắt buộc Trưởng các bưu cục trên phải đóng túi seal trước giờ xe đến tối thiểu 20 phút. Tuyệt đối không để xảy ra tình trạng xe tải đến nơi mới cuống cuồng đi tìm hàng đóng bao!\""
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

        # TOPIC 10: FD
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
                "🎙️ LỜI THOẠI THUYẾT TRÌNH TỰ NHIÊN (KHI BẬT TAB 10 %FD):",
                "\"Dạ tiếp theo là Tab 10 về tỷ lệ Hoàn trả %FD:",
                "Mặt bằng chung toàn vùng tuần này là 7,77% ở Full hàng (24.498 đơn hoàn / 315.328 đơn gán) và 6,10% ở kênh TikTok Shop, nhìn chung vẫn nằm trong biên độ an toàn dưới 8% của công ty.",
                "Anh Khánh Nha Trang tiếp tục dẫn đầu vùng khi kiểm soát hoàn chỉ 4,8%, chị Thủy 5,4%, anh Nhựt 5,8% và anh Long Ninh Thuận 6,5%.",
                "NHƯNG KHI NHÌN VÀO BẢNG 2 (TOP BƯU CỤC HOÀN HÀNG CAO NHẤT), CHÚNG TA THẤY MỘT SỰ THẬT ĐAU LÒNG:",
                "Có tới 4 bưu cục có tỷ lệ hoàn vượt ngưỡng 20% — tức là cứ giao 5 đơn thì có hơn 1 đơn bị quay đầu:",
                "Quảng Tín của anh Linh hoàn 22,95% (380 đơn hoàn), Lang Biang của anh Lợi hoàn 21,04% (444 đơn hoàn), Đơn Dương của chị Nhi hoàn 20,99% (653 đơn hoàn), và Đức Trọng 1 của anh Vũ hoàn 20,53% (334 đơn hoàn)!",
                "Kế tiếp là Kiến Đức của chị Nga (16,7%) và Cam Linh của anh Long (15,3%).",
                "Bản chất hiện trường ở đây là: Bưu tá phụ trách các tuyến đồi dốc xa xôi ngại đi đường dài. Khi gặp đơn hẹn lại hoặc gọi 1 cuộc chuông reo khách chưa kịp nhấc máy, bưu tá lập tức cập nhật lý do 'Khách từ chối nhận' hoặc 'Không liên lạc được 3 lần' để xả hàng về kho chuyển hoàn, trốn tránh việc phải quay lại giao lần 2, lần 3!",
                "Việc này làm các shop bán hàng họ rất bức xúc, vì họ mất tiền chạy quảng cáo, mất tiền đóng gói mà hàng chưa kịp tới tay người mua đã bị bấm hoàn về.",
                "Em đề nghị anh Linh, anh Lợi, chị Nhi, anh Vũ: Bắt đầu từ ngày mai, 100% đơn hàng tại 4 bưu cục trên trước khi bấm duyệt trạng thái Chuyển Hoàn, bắt buộc CS bưu cục phải gọi điện ngẫu nhiên phúc tra lại khách hàng qua tổng đài. Nếu phát hiện bưu tá bấm hoàn khống mà không có cuộc gọi thực tế thì xử lý kỷ luật nghiêm theo quy chế!\""
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

        # TOPIC 11: KTC
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
                "🎙️ LỜI THOẠI THUYẾT TRÌNH TỰ NHIÊN (KHI BẬT TAB 11 VẬN TẢI & KTC):",
                "\"Dạ qua tới Tab 11 về Điều hành KTC và Chi phí Vận tải đường trục:",
                "Mọi người nhìn vào con số %TLTĐ thùng xe tuần này: Rất đáng lo ngại khi tụt từ 47,7% xuống chỉ còn 45,6%, giảm mất -2,1%p!",
                "Và trên hệ thống giám sát hành trình tuần qua phát hiện có tới 124 CHUYẾN XE TẢI KTC lăn bánh trên đường với tỷ lệ lấp đầy thùng dưới 30%!",
                "Trong tổng số 513 chuyến xe toàn vùng, thì cứ 4 chuyến xe chạy trên đường lại có 1 chuyến chạy non tải, thậm chí có 7 chuyến xe gần như rỗng không dưới 10% thùng xe!",
                "Điểm nóng nhất nằm ở đâu? Chính là KTC Đức Trọng ở Lâm Đồng: Một mình Đức Trọng gánh tới 43 chuyến xe non tải, tỷ lệ lấp đầy rơi tự do xuống 40,6%! Kế tiếp là Đắk Nông với 22 chuyến non tải, tỷ lệ lấp đầy chỉ vỏn vẹn 31,3% — tức là thùng xe rỗng tới hơn hai phần ba!",
                "Chúng ta đang trả nguyên tiền cước xe, tiền dầu, tiền cầu đường cho những chuyến xe chở gió.",
                "Em đề xuất Ban Vận tải trong tuần W41 này: Phải rà soát và xử lý ngay 124 chuyến xe non tải này: Tuyến nào sản lượng ít thì gộp 2 chuyến làm một hoặc chuyển sang dùng xe tải nhỏ 1,5 tấn. Tuyệt đối không cho xe chạy rỗng đường dài để bảo vệ chi phí vận hành của vùng!\""
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

        # TOPIC 12: AGING
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
                "🎙️ LỜI THOẠI THUYẾT TRÌNH TỰ NHIÊN (KHI BẬT TAB 12 HÀNG AGING & TREO LC):",
                "\"Dạ qua tới Tab 12 về Hàng tồn Aging và Đơn treo luân chuyển:",
                "Tuần này nhờ sự đôn đốc của các AM, lượng hàng ngâm lâu trên 5 ngày đã giảm từ 1.638 đơn xuống 1.420 đơn, giải phóng được hơn 200 đơn.",
                "Tuy nhiên, con số 1.420 đơn vẫn là một khối u lớn trong kho bưu cục!",
                "Đặc biệt là 33 đơn tồn trên 15 ngày và 362 đơn tồn từ 8 đến 15 ngày. Những đơn này nằm lăn lóc ở góc kho từ nửa tháng trước, tỷ lệ giao được bây giờ chưa tới 3%, nhưng anh em cứ để đó không chịu bấm xử lý hoàn trả hay báo đền bù.",
                "Lại tiếp tục là 3 cái tên quen thuộc: Quảng Tín (312 đơn), Đức Trọng 1 (285 đơn) và Xuân Hương Đà Lạt (210 đơn).",
                "Thêm vào đó, hệ thống đang cảnh báo 118 đơn bị 'treo luân chuyển' trên 24 giờ. Tức là kho KTC đã bắn gửi đi từ hôm kia nhưng bưu cục nhận vẫn chưa quét nhập kho. Chỗ chị Nhung Đắk Nông dính 36 đơn và Lâm Đồng dính 45 đơn.",
                "Hàng treo luân chuyển này rất dễ bị rơi rớt trên thùng xe hoặc thất lạc mà không ai hay biết.",
                "Em yêu cầu các AM: Cho rà soát kho ngay trong chiều nay, tìm cho ra 118 đơn treo luân chuyển này để quét cập nhật lên hệ thống, và dọn sạch 395 đơn tồn trên 8 ngày trước ngày thứ Năm tuần này!\""
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

        # TOPIC 13: COD & QR
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
                "🎙️ LỜI THOẠI THUYẾT TRÌNH TỰ NHIÊN (KHI BẬT TAB 13 COD & QR):",
                "\"Dạ cuối cùng em xin chuyển sang Tab 13 về Quản trị dòng tiền COD và Thanh toán QR:",
                "Nhìn vào Bảng 1 tổng quan: Tuần này toàn vùng Nam Trung Bộ thu hộ tổng cộng 77.502 triệu đồng (~77,5 tỷ đồng). Trong đó, dòng tiền Chuyển khoản QR đạt 46.226 triệu đồng (chiếm 59,6%), và Tiền mặt shipper cầm về là 31.276 triệu đồng (chiếm 40,4%). So với tuần trước, tỷ lệ tiền mặt nhích nhẹ +0,2%p, hệ thống đánh giá ở mức Xấu đi ⚠️.",
                "Nhìn xuống Bảng 2 (Xếp hạng 19 AM theo tỷ lệ tiền mặt):",
                "Tấm gương sáng nhất toàn quốc: Tiếp tục là chị Thái Thị Thanh Thư (Khánh Hòa) khi tỷ lệ tiền mặt chỉ còn 4,0% — tức là 96,0% dòng tiền là quét mã VietQR! Chị Cao Thị Thanh Thủy đạt 16,1% tiền mặt (QR 83,9%), anh Duy Long Ninh Thuận đạt 23,4% tiền mặt (QR 76,6%). Đây là nhóm giúp giảm tải tối đa rủi ro tiền bạc cho công ty.",
                "Anh Trương Quang Linh Đắk Nông tuần này cũng tiến bộ vượt bậc khi kéo giảm tiền mặt từ 80,6% xuống 56,3% (giảm tới -24,3%p WoW!).",
                "NHƯNG NHÌN VÀO NHÓM ĐẦU BẢNG 2, XIN CẢNH BÁO ĐẶC BIỆT 3 AM ĐANG ÔM TIỀN MẶT QUÁ CAO:",
                "Anh Huỳnh Thúc Duân vọt lên 81,0% tiền mặt (tăng gần 10%p!), anh Lê Thanh Nhựt 80,4% tiền mặt và chị Huỳnh Thị Kim Chi 75,8% tiền mặt (tăng 7,2%p)!",
                "Hơn 31 tỷ đồng tiền mặt shipper cầm chạy ngoài đường và để qua đêm ở két sắt bưu cục huyện tiềm ẩn rủi ro cướp giật, mất mát và thâm hụt quỹ cực kỳ lớn.",
                "Nguyên nhân là do shipper lười mời khách quét QR, hoặc có tâm lý cố tình thu tiền mặt để giữ tiền xoay xở cá nhân.",
                "Em đề nghị anh Duân, anh Nhựt, chị Chi: Bắt buộc trang bị 100% thẻ đeo cổ in mã QR cho bưu tá. Kiểm tra số dư két tiền mặt bưu cục lúc 20h30 hàng ngày, bưu cục nào xa ngân hàng bắt buộc nộp tiền qua cây ATM hoặc Viettel Money, tuyệt đối không để tiền mặt tồn qua đêm tại két bưu cục quá 5 triệu đồng!\""
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

        # TOPIC 14: TRUY THU
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
                "🎙️ LỜI THOẠI THUYẾT TRÌNH TỰ NHIÊN (KHI BẬT TAB 14 TRUY THU):",
                "\"Kính thưa Ban Giám Đốc, sang Tab 14 là Báo cáo Truy Thu — Nội dung cảnh báo nóng nhất về Thất thoát tài chính và Kỷ luật vận hành:",
                "Nhìn vào Banner tổng quan ở trên cùng: Tuần W40 này, số tiền CẦN TRUY THU THỰC TẾ của vùng mình đã giảm được 40%, từ 312,1 triệu xuống còn 187,1 triệu đồng nhờ bộ phận Kế toán đã đối soát giảm trừ được gần 246 triệu đồng. Số bản ghi phát sinh cũng giảm từ 4.076 xuống còn 2.424 bản ghi.",
                "Hai tỉnh Bình Thuận (4,8 triệu) và Ninh Thuận (0,7 triệu) kiểm soát nghiệp vụ cực kỳ chuẩn chỉ.",
                "NHƯNG SỐ TIỀN PHÁT SINH BAN ĐẦU LẠI TĂNG VỌT TỪ 317 TRIỆU LÊN 433,1 TRIỆU ĐỒNG (+36,5%)!",
                "Và khi nhìn vào Bảng 1 (Các loại truy thu) và Bảng 4 (Theo AM), chúng ta thấy một vụ việc CỰC KỲ NGHIÊM TRỌNG:",
                "Dòng đầu tiên của Bảng 1: Lỗi 'Liên đới chiếm dụng' phát sinh 56,8 triệu đồng!",
                "Soi vào Bảng 4: AM NGUYỄN THANH LONG đứng đầu danh sách truy thu với 51,2 triệu đồng / 72 ticket, trong đó riêng bưu cục (KHO) Bắc Cam Ranh đã chiếm tới 48,7 triệu đồng do nhân sự chiếm dụng tiền hàng COD!",
                "Đây không còn là lỗi vận hành thông thường, mà là hành vi vi phạm đạo đức và pháp luật nghiêm trọng!",
                "Bên cạnh đó: Anh Lê Văn Trường đang ôm tới 419 ticket truy thu dồn ứ (nhiều ticket nhất toàn vùng, nợ cần thu 26,3 triệu đồng, tập trung tại bưu cục Đơn Dương 12,8 triệu). Anh Phước dính 288 ticket (22,9 triệu đồng, tập trung tại Quảng Tín 13,0 triệu). Chị Huỳnh Thị Kim Chi dính 110 ticket (21,3 triệu đồng tại Tân Hà Lâm Hà).",
                "Em xin kiến nghị Ban Giám Đốc chỉ đạo khẩn cấp: Yêu cầu anh Nguyễn Thanh Long và Trưởng bưu cục Bắc Cam Ranh phải có mặt tại văn phòng giải trình trực tiếp với Ban Giám Đốc và Thanh tra trong sáng ngày mai để thu hồi dứt điểm 48,7 triệu đồng. Anh Trường và chị Chi phải phân loại xử lý dứt điểm 419 ticket tại Lâm Đồng trước thứ Sáu. Tuyệt đối không để số tiền 187,1 triệu này biến thành nợ xấu khó đòi của công ty!\""
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

        # TOPIC 15: KINH DOANH
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
                "🎙️ LỜI THOẠI THUYẾT TRÌNH TỰ NHIÊN (KHI BẬT TAB 15 KINH DOANH & F30):",
                "\"Dạ qua tới Tab 15 về mảng Kinh Doanh và Khách Hàng Mới F30:",
                "Tuần này toàn vùng mang về hơn 1,12 tỷ đồng doanh thu và 35 ngàn đơn hàng gửi. So với tuần trước giảm nhẹ khoảng 3,6% theo nhịp thị trường cuối tháng.",
                "Về mặt tích cực:",
                "Em xin nhiệt liệt biểu dương anh Phan Đình Duy: Một mình cụm anh Duy mang về tới 479 triệu đồng doanh thu, chiếm gần một nửa doanh số của toàn vùng Nam Trung Bộ! Anh Duy tiếp tục giữ vững siêu shop 'Vận Chuyển Online' với doanh thu tháng này đã chạm mốc 5,7 tỷ đồng, đồng thời dẫn đầu toàn vùng khi phát triển thêm 16 shop mới F30.",
                "Anh Long Bình Thuận, anh Nhựt Ninh Thuận và anh Vũ Khánh Hòa cũng duy trì đà tăng trưởng rất tốt từ 2% đến 11%.",
                "TUY NHIÊN, có một điểm BÁO ĐỘNG ĐỎ CỰC KỲ NGUY HIỂM cần nhấn mạnh:",
                "Đó là địa bàn Đắk Nông của AM HUỲNH THÚC DUÂN!",
                "Chỉ trong vòng đúng 1 tuần, doanh thu của anh Duân đã tụt dốc không phanh mất -29,1% (mất trắng hơn 23,4 triệu đồng), và sản lượng bốc hơi tới 1.608 đơn gửi (-28,5%)!",
                "Đây là mức sụt giảm kinh doanh lớn nhất của cả vùng trong vòng 3 tháng qua. Kiểm tra tại bưu cục Gia Nghĩa và Nhân Cơ cho thấy có ít nhất 2 shop lớn bán nông sản và cà phê đã ngưng gửi hàng qua GHN và chuyển hẳn sang đối thủ cạnh tranh.",
                "Bên cạnh đó, chị Thư ở Khánh Hòa cũng giảm gần 12 triệu và chị Nhung giảm 8 triệu doanh thu.",
                "Em đề nghị anh Duân phải giải trình rõ nguyên nhân: Tại sao khách hàng lớn ở Gia Nghĩa lại bỏ đi? Có phải do bưu cục lấy hàng trễ hay thái độ phục vụ có vấn đề? Đầu tuần này anh Duân phải trực tiếp đến gặp lại chủ các shop này để thương lượng chính sách giá và kéo nguồn hàng quay trở lại GHN!\""
            ],
            "insights": [
                "AM Phan Đình Duy là trụ cột kinh doanh của toàn vùng khi đóng góp 42,7% doanh thu và quản lý siêu shop #1 nhóm A.",
                "F30 tăng thêm 20,7% (111 shop mới) cho thấy tiềm năng mở rộng tệp khách hàng cá nhân và shop online vừa và nhỏ còn rất lớn."
            ],
            "warnings": [
                "AM Huỳnh Thúc Duân mất 28,5% sản lượng (-1.608 đơn) tại Gia Nghĩa, Nhân Cơ là tín hiệu cảnh báo mất thị phần nghiêm trọng tại Đắk Nông.",
                "Khách hàng lớn nhóm A nếu bị đối thủ cạnh tranh lôi kéo sẽ làm suy giảm trực tiếp doanh thu tháng của khu vực."
            ],
            "actions": [
                "AM Huỳnh Thúc Duân đi thị trường Gia Nghĩa trong ngày thứ Ba, trực tiếp gặp 2 shop lớn vừa ngưng gửi để xử lý vướng mắc.",
                "Đẩy mạnh chương trình ưu đãi cước F30 cho 111 shop mới để chuyển đổi thành khách hàng thường xuyên (F60, F90)."
            ]
        },

        # TOPIC 16: TỔNG KẾT
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
                "🎙️ LỜI THOẠI KẾT LUẬN TOÀN BỘ BUỔI HỌP GIAO BAN:",
                "\"Kính thưa Ban Giám Đốc và toàn thể các anh chị em AM,",
                "Để kết luận lại buổi họp giao ban tuần W40 hôm nay, chúng ta thấy rất rõ: Toàn vùng Nam Trung Bộ đã chứng minh được khi toàn hệ thống đồng lòng siết kỷ luật, chúng ta hoàn toàn có thể đưa %GTC vượt 60% và ODR vượt 93%.",
                "Tuy nhiên, những thành tích đó sẽ bị vô hiệu hóa nếu chúng ta để rò rỉ 187 triệu tiền truy thu, để xảy ra vụ việc chiếm dụng tiền hàng ở Bắc Cam Ranh, hay để mất khách hàng lớn tại Đắk Nông.",
                "13 bưu cục cảnh báo đỏ trên màn hình chính là nơi quyết định chất lượng dịch vụ của vùng trong tuần tới. Giải tỏa xong 13 bưu cục này là toàn vùng Nam Trung Bộ sẽ đứng vững trong top đầu toàn quốc.",
                "Em xin cảm ơn Ban Giám Đốc và các anh chị đã lắng nghe. Kính chúc toàn vùng Nam Trung Bộ tuần W41 vận hành an toàn, bứt phá doanh số và đạt chuẩn SLA toàn diện!\""
            ],
            "insights": [
                "13 bưu cục này đang nắm giữ hơn 19.000 đơn backlog của vùng; chỉ cần giải tỏa dứt điểm 13 bưu cục này thì ODR và GTC toàn vùng sẽ tự động tăng thêm từ 2% đến 3%p.",
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

    for s_data in sections_data:
        add_callout_box(
            doc,
            section_title=s_data["sec_title"],
            speech_title=s_data["speech_title"],
            speech_paragraphs=s_data["speech_paragraphs"],
            insights=s_data.get("insights"),
            warnings=s_data.get("warnings"),
            actions=s_data.get("actions")
        )

    # Save multiple docx versions safely
    doc_paths = [
        "KICH_BAN_THUYET_TRINH_W40_NAM_TRUNG_BO.docx",
        "KICH_BAN_THUYET_TRINH_W40_CHUAN.docx",
        "KICH_BAN_THUYET_TRINH_MOI_NHAT.docx"
    ]
    for dp in doc_paths:
        try:
            doc.save(dp)
            print(f"Saved DOCX: {dp}")
        except Exception as e:
            print(f"Warning saving {dp}: {e}")

    # Downloads paths
    dl_paths = [
        r"C:\Users\lap4all\Downloads\KICH_BAN_W40_MOI_NHAT.docx",
        r"C:\Users\lap4all\Downloads\KICH_BAN_THUYET_TRINH_W40_CHUAN.docx",
        r"C:\Users\lap4all\Downloads\KICH_BAN_THUYET_TRINH_W40_NAM_TRUNG_BO.docx"
    ]
    for dlp in dl_paths:
        try:
            doc.save(dlp)
            print(f"Saved DOCX to Downloads: {dlp}")
        except Exception as e:
            print(f"Notice (file open in Word?): {dlp} => {e}")

    build_html_file(sections_data)
    build_md_file(sections_data)

def build_html_file(sections_data):
    html_lines = []
    html_lines.append("""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kịch Bản Thuyết Trình W40 — Vùng Nam Trung Bộ (Chuẩn 16 Chuyên Đề)</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --primary: #0f4c81;
            --primary-light: #e6f0fa;
            --accent: #ea580c;
            --accent-light: #fff7ed;
            --success: #16a34a;
            --success-light: #f0fdf4;
            --danger: #dc2626;
            --danger-light: #fef2f2;
            --bg: #f8fafc;
            --card-bg: #ffffff;
            --text-main: #1e293b;
            --text-muted: #64748b;
            --border: #e2e8f0;
        }
        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background: var(--bg);
            color: var(--text-main);
            margin: 0;
            padding: 40px 20px;
            line-height: 1.6;
        }
        .container {
            max-width: 1050px;
            margin: 0 auto;
        }
        .header-box {
            background: linear-gradient(135deg, #0f4c81 0%, #1e3a8a 100%);
            color: white;
            padding: 36px 30px;
            border-radius: 20px;
            text-align: center;
            margin-bottom: 35px;
            box-shadow: 0 10px 25px -5px rgba(15, 76, 129, 0.25);
        }
        .header-sub {
            font-size: 13px;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            font-weight: 700;
            color: #fdba74;
            margin-bottom: 8px;
        }
        .header-box h1 {
            margin: 0;
            font-size: 30px;
            font-weight: 800;
        }
        .header-desc {
            font-size: 14.5px;
            opacity: 0.9;
            margin-top: 10px;
            font-style: italic;
        }
        .section-card {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 26px 30px;
            margin-bottom: 25px;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
        }
        .section-title {
            font-size: 17px;
            font-weight: 800;
            color: var(--primary);
            display: flex;
            align-items: center;
            gap: 10px;
            border-bottom: 2px solid var(--primary-light);
            padding-bottom: 12px;
            margin-bottom: 18px;
        }
        .speech-heading {
            font-size: 15px;
            font-weight: 700;
            color: var(--accent);
            margin-bottom: 14px;
        }
        .bullet-point {
            margin-bottom: 8px;
            font-size: 14.5px;
        }
        .callout {
            border-radius: 12px;
            padding: 14px 18px;
            margin-top: 15px;
            font-size: 14px;
        }
        .callout-insight { background: #f0fdf4; border-left: 4px solid var(--success); }
        .callout-warning { background: #fef2f2; border-left: 4px solid var(--danger); }
        .callout-action  { background: #fff7ed; border-left: 4px solid var(--accent); }
        .callout-title { font-weight: 700; margin-bottom: 5px; }
        .top-btn {
            display: inline-block;
            background: var(--primary);
            color: white;
            padding: 10px 20px;
            border-radius: 30px;
            text-decoration: none;
            font-weight: 600;
            font-size: 14px;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header-box">
            <div class="header-sub">GHN Express — Vùng Nam Trung Bộ</div>
            <h1>KỊCH BẢN THUYẾT TRÌNH BÁO CÁO TUẦN W40</h1>
            <div class="header-desc">Chu kỳ: 28/09/2026 – 04/10/2026 | Chuẩn hóa 16 Chuyên Đề Bám Sát Dashboard & 18 AM</div>
        </div>
""")

    for s in sections_data:
        html_lines.append('        <div class="section-card">')
        html_lines.append(f'            <div class="section-title">{s["sec_title"]}</div>')
        html_lines.append(f'            <div class="speech-heading">{s["speech_title"]}</div>')
        for p in s["speech_paragraphs"]:
            if p.startswith("•") or p.startswith("📍"):
                html_lines.append(f'            <div class="bullet-point">{p}</div>')
            elif p.startswith("🎙️"):
                html_lines.append(f'            <p style="font-weight: 700; color: #ea580c; margin-top: 14px;">{p}</p>')
            else:
                html_lines.append(f'            <p>{p}</p>')
        
        if s.get("insights"):
            html_lines.append('            <div class="callout callout-insight">')
            html_lines.append('                <div class="callout-title"><i class="fa-solid fa-lightbulb"></i> Điểm sáng & Insight vận hành:</div>')
            for ins in s["insights"]:
                html_lines.append(f'                <div>• {ins}</div>')
            html_lines.append('            </div>')
            
        if s.get("warnings"):
            html_lines.append('            <div class="callout callout-warning">')
            html_lines.append('                <div class="callout-title"><i class="fa-solid fa-triangle-exclamation"></i> Cảnh báo rủi ro & Điểm nóng:</div>')
            for w in s["warnings"]:
                html_lines.append(f'                <div>• {w}</div>')
            html_lines.append('            </div>')

        if s.get("actions"):
            html_lines.append('            <div class="callout callout-action">')
            html_lines.append('                <div class="callout-title"><i class="fa-solid fa-circle-check"></i> Hành động cụ thể & Giao việc hiện trường:</div>')
            for a in s["actions"]:
                html_lines.append(f'                <div>• {a}</div>')
            html_lines.append('            </div>')

        html_lines.append('        </div>\n')

    html_lines.append("""
        <a href="#" class="top-btn"><i class="fa-solid fa-arrow-up"></i> Về đầu trang</a>
    </div>
</body>
</html>
""")

    out_html = "KICH_BAN_THUYET_TRINH_W40_NAM_TRUNG_BO.html"
    with open(out_html, "w", encoding="utf-8") as f:
        f.write("\n".join(html_lines))
    print(f"Saved HTML: {out_html}")
    
    # Also save HTML to Downloads
    try:
        with open(r"C:\Users\lap4all\Downloads\KICH_BAN_THUYET_TRINH_W40_NAM_TRUNG_BO.html", "w", encoding="utf-8") as f:
            f.write("\n".join(html_lines))
        print("Saved HTML to Downloads!")
    except Exception as e:
        print("Notice saving HTML to Downloads:", e)

def build_md_file(sections_data):
    md_lines = []
    md_lines.append("# GHN EXPRESS — VÙNG NAM TRUNG BỘ")
    md_lines.append("## BÁO CÁO VẬN HÀNH & KINH DOANH TUẦN W40")
    md_lines.append("*(Chu kỳ dữ liệu: 28/09/2026 – 04/10/2026)*")
    md_lines.append("**Kịch bản thuyết trình 16 chuyên đề điều hành chuẩn hóa — Chỉ số Tỉnh đặt lên đầu, phân tích sâu theo 18 AM & Giao việc hiện trường**\n")
    md_lines.append("---\n")

    for s in sections_data:
        md_lines.append(f"## {s['sec_title']}\n")
        md_lines.append(f"### {s['speech_title']}\n")
        for p in s["speech_paragraphs"]:
            if p.startswith("•"):
                md_lines.append(f"{p}\n")
            elif p.startswith("📍"):
                md_lines.append(f"**{p}**\n")
            elif p.startswith("🎙️"):
                md_lines.append(f"\n> **{p}**\n")
            else:
                md_lines.append(f"{p}\n")
        
        if s.get("insights"):
            md_lines.append("\n> 💡 **Điểm sáng & Insight vận hành:**")
            for ins in s["insights"]:
                md_lines.append(f"> - {ins}")
            md_lines.append("")

        if s.get("warnings"):
            md_lines.append("\n> ⚠️ **Cảnh báo rủi ro & Điểm nóng:**")
            for w in s["warnings"]:
                md_lines.append(f"> - {w}")
            md_lines.append("")

        if s.get("actions"):
            md_lines.append("\n> 🎯 **Hành động cụ thể & Giao việc hiện trường:**")
            for a in s["actions"]:
                md_lines.append(f"> - {a}")
            md_lines.append("")

        md_lines.append("\n---\n")

    out_md = "KICH_BAN_THUYET_TRINH_W40_NAM_TRUNG_BO.md"
    with open(out_md, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
    print(f"Saved MD: {out_md}")

if __name__ == "__main__":
    build_w40_16_topics()
