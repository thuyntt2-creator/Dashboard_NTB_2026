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
                "• 10. Tỷ Lệ Tiền Mặt COD: 37,1% (giảm mạnh từ 40,1% xuống 37,1%, tỷ lệ chuyển khoản QR tăng vọt lên 62,9%).",
                "🎙️ LỜI THOẠI THUYẾT TRÌNH TỰ NHIÊN (KHI BẬT TAB 1 DASHBOARD TỔNG QUAN):",
                "\"Dạ em chào Ban Giám Đốc, chào các anh chị AM và các phòng ban.",
                "Mở đầu buổi họp giao ban tuần W40 (chu kỳ dữ liệu từ 28/09 đến 04/10/2026), kính mời Ban Giám Đốc và các anh chị cùng nhìn lên màn hình Dashboard Tổng quan giúp em.",
                "Tuần 40 này, toàn vùng Nam Trung Bộ của chúng ta có một bước chuyển mình rất ấn tượng về chất lượng dịch vụ Last-mile:",
                "Đầu tiên là điểm sáng rực rỡ nhất: Tỷ lệ Giao thành công (%GTC Full) tuần này đã chính thức phá mốc 60%, chạm mức 60,87%, tăng tới hơn 4,19%p so với tuần trước. Đặc biệt ở kênh TikTok Shop, %GTC đã bay thẳng lên 63,38%, tăng gần 6%p! Đây là kết quả của việc các anh chị AM đã siết rất chặt ca giao chiều và giải tỏa đơn tồn đầu ngày.",
                "Điểm sáng thứ hai là chỉ số Giao đúng hẹn %ODR: Sau nhiều tuần ngấp nghé 90-91%, tuần này toàn vùng đã vượt ngưỡng cam kết SLA 92%, vươn lên 93,12% (hàng TikTok đạt tới 94,18%). Khâu lấy hàng First-mile cũng duy trì rất đều tay trên 91,3%, riêng TikTok Shop đạt gần 95%.",
                "Về quản trị dòng tiền, tỷ lệ nộp COD bằng chuyển khoản QR tuần này đã tăng vọt lên gần 63%, giảm lượng tiền mặt shipper cầm về còn 37,1%, hạn chế tối đa rủi ro thất thoát quỹ.",
                "Tuy nhiên, chúng ta vẫn phải nhìn thẳng vào 3 nút thắt rất lớn cần giải quyết ngay:",
                "Thứ nhất: Sản lượng tuần này hạ nhiệt nhẹ về 311.503 đơn, giảm khoảng 6% so với tuần W39 do tuần cuối tháng thị trường có sự chững lại.",
                "Thứ hai: Khâu vận tải KTC đang báo động đỏ khi tỷ lệ lấp đầy thùng xe tụt xuống chỉ còn 45,6% (giảm -2,1%p so với 47,7% tuần W39), và số chuyến xe chạy non tải dưới 30% thùng xe tăng vọt lên tới 124 chuyến (chiếm gần một phần tư tổng số 513 chuyến KTC toàn vùng), gây lãng phí rất lớn chi phí nhiên liệu đường trục.",
                "Thứ ba: Mặc dù tổng số tiền cần truy thu giảm 40% về 187,1 triệu đồng, nhưng số tiền phát sinh ban đầu lại tăng vọt lên 433,1 triệu đồng, nổi cộm lên vụ việc chiếm dụng tiền hàng 48,7 triệu đồng tại bưu cục Bắc Cam Ranh thuộc cụm AM Nguyễn Thanh Long và 419 ticket truy thu dồn ứ tại địa bàn AM Lê Văn Trường.",
                "Bây giờ, em xin phép bấm chuyển qua Tab 2 để đi sâu vào sản lượng từng Tỉnh và từng anh chị AM nha!\""
            ],
            "insights": [
                "%GTC Full phá vỡ mốc 60% (đạt 60,87%) và TTS đạt đỉnh 63,38% khẳng định kỷ luật xuất tuyến Last-mile đã có chuyển biến thực chất.",
                "%ODR toàn vùng vượt chuẩn SLA 92% (đạt 93,12%), khâu lấy hàng First-mile TikTok Shop đạt 94,97% giữ vững uy tín với các sàn TMĐT."
            ],
            "warnings": [
                "Phát sinh 433,1 Tr ₫ cước truy thu ban đầu; vụ việc liên đới chiếm dụng 48,7 Tr ₫ tại Bắc Cam Ranh là hồi chuông cảnh báo đỏ về đạo đức nghề nghiệp và kiểm soát nội bộ.",
                "124 chuyến xe KTC chạy non tải dưới 30% thùng (chiếm 24,2% tổng số chuyến) làm xói mòn nghiêm trọng biên lợi nhuận vận hành của vùng."
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
                "Thứ hai là anh Trường ở Lâm Đồng: Giảm tiếp hơn 4.500 đơn. Địa bàn của anh Trường đang dính nhiều đơn tồn và ODR thấp, khi giao trễ khách hàng họ sẽ hủy đơn và shop giảm gửi qua GHN.",
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
                "• Đắk Nông: 54,46% (W39: 48,81%, tăng mạnh +5,65%p) ➔ Nỗ lực vượt bậc kéo GTC thoát đáy.",
                "• Lâm Đồng: 54,43% (W39: 47,38%, tăng mạnh +7,05%p) ➔ Mức tăng trưởng %GTC mạnh nhất vùng, nhưng vẫn đứng chót bảng 5 tỉnh.",
                "• Toàn vùng: Full hàng đạt 60,87% (+4,19%p) | TikTok Shop đạt 63,38% (+5,84%p).",
                "📍 2. XẾP HẠNG %GTC TUYỆT ĐỐI THEO 18 AM (TOP ĐẦU & ĐÁY BẢNG):",
                "• Top AM xuất sắc (>68%): Nguyễn Ngọc Khánh (74,5% - Top 1 GTC toàn vùng), Thái Thị Thanh Thư (72,0% - Top 2 GTC), Nguyễn Đỗ Minh Nghĩa (70,4%), Nguyễn Duy Long (69,0% - Đầu tàu sản lượng 42,7k đơn), Cao Thị Thanh Thủy (68,0%).",
                "• Top AM tiến bộ (60 - 68%): Nguyễn Thị Tuyết Thơ (67,6%), Nguyễn Hoàng Phi (64,6%), Lê Thanh Nhựt (60,2%).",
                "• Nhóm AM đáy (<50% cần kèm cặp gấp): Lê Minh Lợi (36,5%), Phan Nguyễn Yến Nhi (38,0%), Trương Quang Linh (40,3%), Huỳnh Thúc Duân (47,1%), Lê Văn Trường (48,9%), Nguyễn Lê Nguyên Vũ (49,0%).",
                "📍 3. TOP AM CÓ ĐÓNG GÓP TĂNG TRƯỞNG %GTC LỚN NHẤT TUẦN VỪA RỒI (Δ WoW W40 vs W39):",
                "• 🥇 AM Trương Quang Linh (Đắk Nông): Tăng mạnh nhất vùng +14,49%p (từ 25,85% lên 40,34%) ➔ Bước nhảy vọt thoát khỏi đáy tuyệt đối.",
                "• 🥈 AM Lê Văn Trường (Lâm Đồng): Tăng bứt phá +11,85%p (từ 37,10% lên 48,95%) trên tải lớn 37.411 đơn ➔ Công thần chủ lực kéo toàn tỉnh Lâm Đồng tăng vọt +7,05%p!",
                "• 🥉 AM Thái Thị Thanh Thư (Khánh Hòa): Tăng thần tốc +9,63%p (từ 62,38% lên 72,02%) trên tải lớn 35.889 đơn ➔ Nhân tố số 1 kéo tỉnh Khánh Hòa bứt phá vượt mốc 60%!",
                "• 4️⃣ AM Phan Nguyễn Yến Nhi (Lâm Đồng): Tăng +8,96%p (từ 29,00% lên 37,96%).",
                "• 5️⃣ AM Nguyễn Lê Nguyên Vũ (Lâm Đồng): Tăng +7,53%p (từ 41,44% lên 48,97%).",
                "• 6️⃣ AM Lê Minh Lợi (Lâm Đồng): Tăng +5,89%p (từ 30,61% lên 36,50%).",
                "• 7️⃣ AM Hồng Bích Nga (Lâm Đồng/Đắk Nông): Tăng +3,53%p (từ 55,87% lên 59,40%).",
                "• 8️⃣ AM Trần Thị Nhung (Đắk Nông): Tăng +3,49%p (từ 55,46% lên 58,95% với 37.073 đơn).",
                "🎙️ LỜI THOẠI THUYẾT TRÌNH TỰ NHIÊN (KHI BẬT TAB 3 GTC TỔNG):",
                "\"Dạ qua tới Tab 3 GTC Tổng, trên màn hình mọi người thấy toàn bộ các cột chỉ số đều nhuộm màu xanh tăng trưởng rất đẹp mắt!",
                "Nhìn vào 5 Tỉnh thành ở bảng trên cùng:",
                "Ninh Thuận và Bình Thuận tiếp tục là 2 điểm sáng dẫn đầu vùng về độ ổn định với GTC đạt xấp xỉ 67,5%.",
                "Khánh Hòa tuần này đã xuất sắc bứt phá qua mốc 60% khi đạt 62,2% (tăng +3,4%p so với W39: 58,8%), đóng góp cực lớn vào kỳ tích chung của toàn vùng.",
                "Hai tỉnh miền núi là Đắk Nông và Lâm Đồng: Dù vẫn đứng ở 2 vị trí cuối bảng với 54,4%, nhưng tuần này anh em đã có sự nỗ lực phi thường. Lâm Đồng kéo tăng tới hơn +7,0%p, còn Đắk Nông tăng hơn +5,6%p so với tuần trước.",
                "Đặc biệt, khi mổ xẻ đóng góp của 18 AM, Ban Giám Đốc sẽ thấy một điểm mấu chốt rất đáng biểu dương:",
                "Tuần này toàn vùng tăng mạnh +4,19%p KHÔNG PHẢI nhờ nhóm ven biển (vì Bình Thuận và Ninh Thuận đã ở mức trần nên đi ngang ~67,5%), mà công lớn nhất kéo cả vùng bứt phá tuần này thuộc về 3 AM có bước nhảy vọt thần tốc:",
                "Thứ nhất là chị Thái Thị Thanh Thư ở Khánh Hòa: Tăng vọt tới gần +10%p (từ 62,4% lên 72,0%) trên khối lượng gần 36 ngàn đơn, đưa chị Thư lên thẳng vị trí Á quân GTC toàn vùng và kéo bừng sáng cả tỉnh Khánh Hòa!",
                "Thứ hai là anh Lê Văn Trường ở Lâm Đồng: Tăng phi thường +11,9%p (từ 37,1% lên 49,0%) trên khối lượng cực lớn hơn 37 ngàn đơn! Chính anh Trường là đầu tàu kéo Lâm Đồng tăng hơn 7%p tuần này!",
                "Thứ ba là anh Trương Quang Linh ở Đắk Nông: Tăng bứt phá mạnh nhất toàn vùng với +14,5%p (từ 25,8% lên 40,3%). Bên cạnh đó, anh Vũ (+7,5%p), chị Nhi (+9,0%p) và chị Nhung (+3,5%p trên 37 ngàn đơn) cũng là những nhân tố nòng cốt kéo toàn bộ khu vực Tây Nguyên thoát đáy!",
                "Bên cạnh các AM tăng trưởng mạnh, em cũng xin ghi nhận anh Nguyễn Ngọc Khánh (Bình Thuận) giữ vững ngôi Quán quân GTC toàn vùng với 74,5%, và anh Nguyễn Duy Long tiếp tục là đầu tàu gánh sản lượng lớn nhất toàn vùng (gần 43 ngàn đơn Full hàng) với GTC rất vững 69,0%.",
                "Tuy nhiên, Ban Giám Đốc lưu ý giúp em nhóm các AM vẫn còn nằm dưới mốc 50%:",
                "Dù anh Lợi (+5,9%p), chị Nhi (+9,0%p) và anh Linh (+14,5%p) đã có tiến bộ vượt bậc, nhưng GTC tuyệt đối vẫn còn dưới 40%, shipper vẫn chưa linh hoạt đổi ca phát chiều tối.",
                "Em đề nghị tuần tới, các AM nhóm dưới phải duy trì đà tiến bộ này và ngồi lại với từng Trưởng bưu cục để tối ưu lại ca phát chiều. Giờ em xin chuyển qua Tab 4 mổ xẻ Ca 1 và Ca 2 ạ!\"",
            ],
            "insights": [
                "Động lực tăng trưởng GTC tuần W40 (+4,19%p toàn vùng) chủ yếu đến từ sự bứt phá của AM Lê Văn Trường (+11,85%p / 37,4k đơn) và AM Thái Thị Thanh Thư (+9,63%p / 35,9k đơn).",
                "Kênh TikTok Shop đạt 63,38% GTC, cao hơn Full hàng 2,51%p, cho thấy đơn sàn TMĐT có độ hoàn tất nhanh hơn đơn hàng ngoài."
            ],
            "warnings": [
                "6 AM (Lợi, Nhi, Linh, Duân, Trường, Vũ) dù đã có cải thiện mạnh về biến động nhưng mức tuyệt đối vẫn dưới 50% GTC, cần duy trì kỷ luật đôn đốc.",
                "Cần kiểm tra xem có hiện tượng shipper cố tình chọn đơn dễ giao để đẩy tỷ lệ GTC ảo hay không."
            ],
            "actions": [
                "Áp dụng quy trình kiểm soát ca 2 của Bình Thuận cho các AM nhóm đáy, bắt buộc gọi lại lần 2 cho 100% đơn chưa phát trước 17h30."
            ]
        },

        # TOPIC 4
        {
            "sec_title": "🔥 [IV. PHÂN TÍCH CHUYÊN SÂU %GTC CA 1 (HÀNG TỒN & HÀNG THUẦN) (W40)]",
            "speech_title": "🗣️ MỔ XẺ GIAO HÀNG CA 1 SÁNG: HÀNG TỒN (52.8%) VS HÀNG THUẦN (72.4%):",
            "speech_paragraphs": [
                "📍 1. BẢNG HIỆU SUẤT GIAO CA 1 THEO 5 TỈNH THÀNH (W40):",
                "• Toàn vùng: GTC Ca 1 Hàng Tồn đạt 52,80% (tăng +3,8%p) | GTC Ca 1 Hàng Thuần đạt 72,40% (tăng +3,1%p; TTS đạt đỉnh 75,80%).",
                "• Bình Thuận: Hàng Tồn 58,4% | Hàng Thuần 76,2% ➔ Đạt chuẩn SLA toàn diện.",
                "• Khánh Hòa: Hàng Tồn 56,1% | Hàng Thuần 74,5% ➔ Xử lý hàng tồn đầu ngày rất sạch.",
                "• Ninh Thuận: Hàng Tồn 53,2% | Hàng Thuần 71,8%.",
                "• Đắk Nông: Hàng Tồn 49,5% | Hàng Thuần 68,9% ➔ Hàng tồn đã kéo lên sát 50%.",
                "• Lâm Đồng: Hàng Tồn 48,2% | Hàng Thuần 67,5% ➔ Nút thắt lớn nhất nằm ở đơn tồn dồn toa.",
                "📍 2. BÓC TÁCH NGUYÊN NHÂN LỆCH PHA:",
                "• Hàng Thuần Ca 1 (hàng mới về trong đêm) được shipper ưu tiên chọn giao trước nên đạt tỷ lệ thành công rất cao (72,4%, riêng TTS đạt gần 76%).",
                "• Hàng Tồn Ca 1 (hàng của ngày hôm trước trôi sang) chỉ đạt 52,8%: Shipper có tâm lý ngại cầm hàng cũ đi phát vì sợ khách đổi ý không lấy hoặc địa chỉ khó tìm.",
                "🎙️ LỜI THOẠI THUYẾT TRÌNH TỰ NHIÊN (KHI BẬT TAB 4 & 5 GTC CA 1):",
                "\"Dạ khi chuyển sang Tab 4 và Tab 5 mổ xẻ chi tiết ca sáng, mọi người sẽ thấy rõ điểm nghẽn thực sự của khâu Last-mile:",
                "Nhìn vào hàng thuần mới về sáng sớm, toàn vùng giao cực kỳ tốt, đạt tới 72,4%, riêng đơn TikTok Shop lên tới gần 76%, chạm đúng trần kỳ vọng của sàn.",
                "Nhưng khi nhìn sang thẻ Hàng Tồn ở Tab 4, tỷ lệ thành công lập tức tụt xuống còn 52,8%, chênh lệch nhau tới gần 20%p!",
                "Tại sao lại như vậy?",
                "Qua kiểm tra thực tế tại các kho bưu cục ở Đà Lạt và Gia Nghĩa, em thấy shipper sáng ra lấy hàng chỉ chăm chăm lựa các kiện hàng thuần mới tinh để giao cho nhanh lấy số. Còn các đơn tồn từ hôm trước dồn lại thì để dưới đáy sọt hoặc để lại góc kho, không ưu tiên phát sớm.",
                "Hàng tồn để càng lâu thì tỷ lệ khách hủy càng cao. Ở Lâm Đồng hàng tồn Ca 1 chỉ đạt 48,2% và Đắk Nông đạt 49,5%.",
                "Anh Trường, anh Tiến với anh Linh phải quán triệt lại cho bưu tá: Quy tắc bất di bất dịch của GHN là 'First In - First Out', hàng cũ tồn hôm qua phải được gán và mang đi phát ngay chuyến đầu tiên lúc 8h sáng, không được găm hàng lại bưu cục!\""
            ],
            "insights": [
                "Hàng thuần ca 1 đạt 75,8% TTS chứng minh năng lực giao hàng của shipper GHN rất tốt khi khách có nhu cầu nhận ngay.",
                "Độ trễ 20%p giữa hàng tồn và hàng thuần khẳng định shipper đang phân biệt đối xử với các kiện hàng cũ."
            ],
            "warnings": [
                "Đơn tồn ca 1 dưới 50% tại Lâm Đồng và Đắk Nông đang biến hàng trăm kiện hàng thành đơn tồn aging và tăng tỷ lệ hoàn trả oan uổng."
            ],
            "actions": [
                "Trưởng bưu cục bắt buộc phải kiểm tra sọt hàng của shipper trước khi xuất bến lúc 08h15: 100% đơn tồn hôm trước phải được xếp lên trên cùng để phát trước 10h30."
            ]
        },

        # TOPIC 5
        {
            "sec_title": "📋 [V. TỶ LỆ GÁN VẬN HÀNH TOÀN MẠNG & HIỆU SUẤT %GTC CA 2 (W40)]",
            "speech_title": "🗣️ HIỆU SUẤT GIAO CA 2 (48.6%) VÀ TỶ LỆ GÁN ĐẦU NGÀY TOÀN VÙNG (TAB 6):",
            "speech_paragraphs": [
                "📍 1. BẢNG HIỆU SUẤT GIAO CA 2 THEO 5 TỈNH THÀNH (W40):",
                "• Toàn vùng: GTC Ca 2 đạt 48,60% (tăng +7,4%p so với W39 41,20%).",
                "• Bình Thuận: 52,10% | Khánh Hòa: 49,80% | Ninh Thuận: 48,90% | Lâm Đồng: 42,50% | Đắk Nông: 40,80%.",
                "📍 2. TỶ LỆ GÁN VẬN HÀNH TOÀN MẠNG (TARGET ≥ 90.0%):",
                "• Gán Ca 1 (Đầu ngày): Toàn vùng đạt 88,50% (Bình Thuận 92,1%, Khánh Hòa 90,4%, Lâm Đồng 84,2%).",
                "• Gán Ca 2 (Ca trưa/chiều): Toàn vùng chỉ đạt 62,40% (mặc dù tăng so với 56,8% W39 nhưng vẫn rất thấp so với target 90%).",
                "• Gán Tổng Toàn Mạng: Đạt 83,20% (chưa chạm ngưỡng 90%). Gần 17% đơn hàng về kho trong ngày không được đưa ra đường.",
                "🎙️ LỜI THOẠI THUYẾT TRÌNH TỰ NHIÊN (KHI BẬT TAB 6 GTC CA 2 & TỶ LỆ GÁN):",
                "\"Dạ mời Ban Giám Đốc nhìn tiếp sang Tab 6 về Ca 2 và Tỷ lệ gán đơn:",
                "Tuần này tỷ lệ GTC Ca 2 của toàn vùng đã có tiến bộ vượt bậc, kéo từ 41,2% lên 48,6%, tăng tới hơn 7%p. Bình Thuận thậm chí đã vượt 52% ca chiều.",
                "Tuy nhiên, nguyên nhân lớn nhất khiến GTC cả ngày của mình chưa vượt được 65% là do TỶ LỆ GÁN CA 2 QUÁ THẤP!",
                "Mọi người nhìn cái con số 62,4% này: Cứ 100 đơn hàng chuyến xe KTC trưa chở về bưu cục, thì có tới gần 38 đơn bị nằm lại sàn kho, không được gán cho shipper mang đi giao ca chiều!",
                "Tại sao hàng về mà không mang đi phát?",
                "Vẫn là câu chuyện cũ: Khung giờ 12h30 đến 13h30 xe KTC về, nhân viên kho bưu cục nghỉ ăn trưa. Đến 14h00 shipper chuẩn bị đi ca chiều thì hàng trưa vẫn chưa được bắn quét phân loại xong. Shipper không có hàng mới để đi, chỉ mang lèo tèo vài đơn hẹn buổi sáng rồi về sớm lúc 16h30.",
                "Trong khi đó, khung giờ từ 16h30 đến 18h30 là giờ vàng khách hàng đi làm về, ở nhà nhận hàng nhiều nhất thì shipper của mình lại không có trên tuyến!",
                "Em đề nghị tuần W41, tất cả các bưu cục phải sắp xếp lại ca trực trưa: Phải có 1 nhân viên trực bắn gán hàng từ 13h00, để đúng 14h00 shipper có đủ hàng xuất tuyến ca 2, kéo tỷ lệ gán Ca 2 lên trên 85% giúp em!\""
            ],
            "insights": [
                "Khung giờ 16h30 - 18h30 là 'khung giờ vàng' giao hàng cho người dân đô thị, nhưng tỷ lệ shipper trên tuyến lại thấp nhất trong ngày.",
                "Gán ca 2 đạt 62,4% là nút thắt cơ học làm nghẽn dòng chảy hàng hóa tại kho bưu cục."
            ],
            "warnings": [
                "Đơn hàng tồn ca trưa không gán sẽ trực tiếp bị rớt SLA ODR vào sáng hôm sau và làm chật chội mặt bằng sàn bưu cục."
            ],
            "actions": [
                "Trưởng bưu cục phân công nhân viên luân phiên trực trưa bắn phân loại hàng; AM kiểm tra tỷ lệ gán trên hệ thống lúc 14h15 hàng ngày."
            ]
        },

        # TOPIC 6
        {
            "sec_title": "⏱️ [VI. PHÂN TÍCH HIỆU SUẤT %ODR (GIAO ĐÚNG HẸN SLA) TOÀN VÙNG (TARGET ≥ 92.0%) (W40)]",
            "speech_title": "🗣️ CHẤT LƯỢNG GIAO ĐÚNG HẸN %ODR: 5 TỈNH LÊN ĐẦU & ĐÁNH GIÁ 18 AM (TAB 7):",
            "speech_paragraphs": [
                "📍 1. BẢNG %ODR GIAO ĐÚNG HẸN 5 TỈNH THÀNH (W40 vs W39):",
                "• Bình Thuận: 96,74% (W39: 96,27%, tăng +0,47%p) ➔ Dẫn đầu toàn vùng, vượt xa chuẩn cam kết 92%.",
                "• Khánh Hòa: 95,59% (W39: 91,94%, bứt phá +3,65%p) ➔ Vượt chuẩn xuất sắc.",
                "• Ninh Thuận: 94,20% (W39: 92,80%, tăng +1,40%p) ➔ Đạt chuẩn an toàn.",
                "• Đắk Nông: 90,42% (W39: 88,53%, tăng +1,89%p) ➔ Đã vượt mốc 90%, tiệm cận chuẩn 92%.",
                "• Lâm Đồng: 87,79% (W39: 84,69%, tăng +3,10%p) ➔ Tiến bộ lớn nhưng vẫn là tỉnh duy nhất chưa đạt chuẩn 92%.",
                "• Toàn vùng: Full hàng đạt 93,12% (+2,28%p) | TikTok Shop đạt 94,18% (+2,41%p) ➔ ĐẠT CHUẨN SLA TOÀN VÙNG!",
                "📍 2. PHÂN TÍCH CHI TIẾT 18 AM:",
                "• Top AM xuất sắc nhất vùng (%ODR > 96%):",
                "  1. Cao Thị Thanh Thủy (Khánh Hòa): 97,8% ➔ Quán quân ODR toàn vùng Nam Trung Bộ!",
                "  2. Thái Thị Thanh Thư (Khánh Hòa): 96,9% | Nguyễn Duy Long (Bình Thuận): 96,6% | Nguyễn Ngọc Khánh (Bình Thuận): 96,4% | Lê Thanh Nhựt (Ninh Thuận): 95,4%.",
                "• Bottom 3 AM báo động đỏ (%ODR < 80% — NGUY CƠ BỊ SÀN PHẠT):",
                "  1. Lê Minh Lợi (Lâm Đồng): 74,1% ➔ Thấp nhất toàn vùng, điểm nóng bưu cục Lang Biang - Đà Lạt 1.",
                "  2. Trương Quang Linh (Đắk Nông): 74,9% ➔ Điểm nóng bưu cục Quảng Tín.",
                "  3. Lê Văn Trường (Lâm Đồng): 78,3% ➔ Điểm nóng bưu cục Xuân Hương và Đơn Dương.",
                "🎙️ LỜI THOẠI THUYẾT TRÌNH TỰ NHIÊN (KHI BẬT TAB 7 ODR):",
                "\"Dạ qua tới Tab 7 ODR, đây là chỉ số sống còn để giữ hợp đồng với các sàn TMĐT và khách hàng VIP:",
                "Tin rất vui là tuần này toàn vùng mình đã chính thức vượt qua vạch đích SLA 92%, đạt 93,12% đối với Full hàng và TikTok Shop đạt tới 94,18%!",
                "3 tỉnh Duyên hải làm cực kỳ xuất sắc: Bình Thuận giữ vững phong độ 96,7%, Khánh Hòa bứt phá lên 95,6% và Ninh Thuận đạt 94,2%.",
                "Đặc biệt, em xin tuyên dương chị Thủy Khánh Hòa: Chị Thủy tuần này đạt ODR đỉnh toàn vùng 97,8%, gần như 100 đơn đi là giao đúng hẹn 98 đơn!",
                "Anh Long Bình Thuận và chị Thư Khánh Hòa cũng duy trì phong độ rất cao trên 96,6%.",
                "TUY NHIÊN, nhìn xuống 3 cái tên ở đáy bảng, em xin phép cảnh báo rất nghiêm khắc:",
                "Anh Lợi (74,1%), anh Linh (74,9%) và anh Trường (78,3%):",
                "Ba anh đang quản lý những địa bàn có ODR tụt xuống dưới 80%! Cứ 10 đơn giao thì có tới 2-3 đơn bị trễ hẹn với khách!",
                "Chỗ anh Lợi ở Đà Lạt: Bưu cục Lang Biang địa bàn đồi dốc xa xôi, tài xế KTC đưa hàng lên trễ thì shipper lại không đi phát tăng ca chiều tối, để đơn trôi qua 2-3 ngày.",
                "Chỗ anh Linh ở Đắk Nông: Bưu cục Quảng Tín đường xa nhưng shipper không chủ động hẹn khách trước, đi đến nơi khách vắng nhà lại quay xe về kho.",
                "ODR dưới 80% trên sàn TikTok Shop là shop bán hàng sẽ bị đánh gậy cảnh cáo, họ sẽ lập tức khóa cổng vận chuyển GHN. Em yêu cầu 3 anh Lợi, Linh, Trường phải viết cam kết phương án xử lý, đưa ODR cụm mình lên trên 85% ngay trong tuần W41 này!\""
            ],
            "insights": [
                "Chị Cao Thị Thanh Thủy đạt 97,8% ODR khẳng định việc quản lý chặt lộ trình di chuyển của bưu tá có thể triệt tiêu hoàn toàn đơn trễ hẹn.",
                "3 tỉnh ven biển (Bình Thuận, Khánh Hòa, Ninh Thuận) tạo thành trục vận hành vững chắc gánh số ODR cho toàn vùng."
            ],
            "warnings": [
                "3 AM (Lợi 74,1%, Linh 74,9%, Trường 78,3%) đối mặt nguy cơ bị đối tác sàn phạt vi phạm cam kết chất lượng dịch vụ (SLA Breach).",
                "Đơn giao trễ kéo dài tại các bưu cục huyện làm xói mòn lòng tin của người mua hàng vùng cao."
            ],
            "actions": [
                "Áp dụng cơ chế cảnh báo đơn cận giờ: Bưu cục ưu tiên chia chọn và giao trước các đơn hàng chỉ còn dưới 4 tiếng là hết hạn SLA."
            ]
        },

        # TOPIC 7
        {
            "sec_title": "🚚 [VII. PHÂN TÍCH CHỈ SỐ %LTC (LẤY THÀNH CÔNG) THEO 18 AM & 5 TỈNH (TARGET ≥ 90.0%) (W40)]",
            "speech_title": "🗣️ PHONG ĐỘ FIRST-MILE: %LTC TOÀN VÙNG ĐẠT 91.35% (TTS ĐẠT 94.97%) (TAB 8):",
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
                "🎙️ LỜI THOẠI THUYẾT TRÌNH TỰ NHIÊN (KHI BẬT TAB 8 LTC):",
                "\"Dạ qua tới Tab 8 Lấy hàng First-mile, em xin báo cáo một kết quả rất đáng mừng:",
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

        # TOPIC 8
        {
            "sec_title": "🌙 [VIII. PHÂN TÍCH CHỈ SỐ %OPR TIKTOK SHOP TOÀN VÙNG (TARGET KPI ≥ 80.0%) (W40)]",
            "speech_title": "🗣️ HIỆU SUẤT XỬ LÝ ĐƠN TIKTOK SHOP %OPR: CA NGÀY VS CA ĐÊM (TAB 9):",
            "speech_paragraphs": [
                "📍 1. BẢNG HIỆU SUẤT %OPR TIKTOK SHOP THEO 5 TỈNH THÀNH (W40):",
                "• Ninh Thuận: Ca Ngày 97,59% | Ca Đêm 85,19% | Tổng OPR: 93,79% ➔ Quán quân OPR toàn vùng.",
                "• Khánh Hòa: Ca Ngày 94,10% | Ca Đêm 84,57% | Tổng OPR: 89,23% ➔ Cả 2 ca đều làm rất đều tay.",
                "• Bình Thuận: Ca Ngày 88,05% | Ca Đêm 77,37% (tăng vọt từ 52,4% W39 lên 77,4%!) | Tổng OPR: 83,45%.",
                "• Lâm Đồng: Ca Ngày 89,58% | Ca Đêm 48,32% | Tổng OPR: 75,54% ➔ Ca đêm tiếp tục là nút thắt nghiêm trọng.",
                "• Đắk Nông: Ca Ngày 97,20% | Ca Đêm 7,24% | Tổng OPR: 62,80% ➔ Ca đêm gần như tê liệt hoàn toàn.",
                "• Toàn vùng: Hoàn thành 85,60% (vượt KPI ≥ 80,0%).",
                "📍 2. BÓC TÁCH NGUYÊN NHÂN TẠI LÂM ĐỒNG VÀ ĐẮK NÔNG:",
                "• Ca ngày tất cả 5 tỉnh đều làm cực kỳ xuất sắc (88% đến 97%).",
                "• Tuy nhiên, ban đêm tại kho KTC Lâm Đồng và Đắk Nông không bố trí đủ nhân sự phân loại, hàng đêm nhập kho bị ngâm đến sáng hôm sau mới quét OPR.",
                "🎙️ LỜI THOẠI THUYẾT TRÌNH TỰ NHIÊN (KHI BẬT TAB 9 OPR TTS):",
                "\"Dạ qua tới Tab 9 về OPR TikTok Shop, mời Ban Giám Đốc nhìn vào sự tương phản giữa ca ngày và ca đêm:",
                "Ban ngày thì tỉnh nào cũng làm cực kỳ xuất sắc, toàn 90% đến 97%, chứng tỏ quy trình ban ngày anh em vận hành rất trơn tru.",
                "Tuần này em xin đặc biệt biểu dương kho KTC Bình Thuận: Ca đêm tuần trước chỉ đạt 52% thì tuần này anh em đã chấn chỉnh, kéo vọt lên 77,4%, giúp OPR cả tỉnh đạt trên 83%!",
                "Nhưng nhìn sang Lâm Đồng và Đắk Nông:",
                "Ca đêm Lâm Đồng chỉ đạt 48,3%, và Đắk Nông thì ca đêm vỏn vẹn có 7,2%!",
                "Hàng TikTok Shop từ TP.HCM chạy xe KTC về tới kho Lâm Đồng và Đắk Nông lúc 23h đêm đến 2h sáng. Lúc đó kho chỉ có bảo vệ trực hoặc vài bạn bốc xếp, không có ai ngồi máy tính bắn quét nhập kho OPR.",
                "Hàng nằm im trên sàn xe đến tận 6h sáng hôm sau mới được xử lý. Điều này làm trễ toàn bộ thời gian cam kết 24h của sàn TikTok.",
                "Em đề nghị Giám đốc Vận hành chỉ đạo ngay: Bắt buộc KTC Lâm Đồng và các bưu cục lớn Đắk Nông phải xếp ca trực đêm có nhân viên thao tác hệ thống, giải phóng dứt điểm hàng trước 5h sáng!\""
            ],
            "insights": [
                "KTC Bình Thuận chứng minh việc bố trí lại nhân sự trực đêm có thể tăng ngay 25% hiệu suất OPR chỉ trong vài ngày.",
                "Kho KTC Lâm Đồng và Đắk Nông thiếu nhân sự ca đêm là nguyên nhân gốc rễ làm chậm luồng hàng buổi sáng."
            ],
            "warnings": [
                "OPR ca đêm dưới 50% làm lãng phí 8 tiếng vận chuyển ban đêm, khiến bưu tá sáng hôm sau bị trễ giờ xuất bến."
            ],
            "actions": [
                "Bổ sung tối thiểu 2 nhân sự trực ca đêm (22h00 - 05h00) tại KTC Lâm Đồng và Gia Nghĩa để quét nhập kho 100% hàng về đêm."
            ]
        },

        # TOPIC 9
        {
            "sec_title": "⚠️ [IX. PHÂN TÍCH TỶ TRỌNG RỚT ĐƠN LUÂN CHUYỂN THEO AM & TỈNH THÀNH (W40)]",
            "speech_title": "🗣️ KIỂM SOÁT TỶ LỆ RỚT LUÂN CHUYỂN KTC TOÀN VÙNG (1.69%) (TAB 10):",
            "speech_paragraphs": [
                "📍 1. BẢNG TỶ LỆ RỚT LUÂN CHUYỂN THEO 5 TỈNH THÀNH (W40):",
                "• Bình Thuận: 0,28% (xuất sắc nhất vùng, chỉ rớt 12 đơn trên 4.230 đơn cần luân chuyển).",
                "• Khánh Hòa: 0,48% (cực kỳ an toàn, chỉ rớt 16 đơn trên 3.304 đơn).",
                "• Đắk Nông: 1,45% (ở mức chấp nhận được).",
                "• Ninh Thuận: 3,58% (rớt 60 đơn trên 1.676 đơn ➔ tăng so với 2,40% W39).",
                "• Lâm Đồng: 3,84% (rớt 121 đơn trên 3.150 đơn ➔ chiếm hơn một nửa tổng đơn rớt của cả vùng).",
                "• Toàn vùng: 1,69% (tổng 219 đơn rớt trên 12.934 đơn cần luân chuyển, duy trì dưới trần kiểm soát 1,80%).",
                "📍 2. TOP BƯU CỤC RỚT LUÂN CHUYỂN NHIỀU NHẤT:",
                "• (LDO) Đức Trọng 1: Rớt 42 đơn (AM Trầm Hữu Tiến).",
                "• (NTH) Phan Rang: Rớt 38 đơn (AM Lê Thanh Nhựt).",
                "• (LDO) Lang Biang - Đà Lạt 1: Rớt 29 đơn (AM Lê Minh Lợi).",
                "• (LDO) Xuân Hương - Đà Lạt: Rớt 24 đơn (AM Lê Văn Trường).",
                "🎙️ LỜI THOẠI THUYẾT TRÌNH TỰ NHIÊN (KHI BẬT TAB 10 RỚT LUÂN CHUYỂN):",
                "\"Dạ qua tới Tab 10 về Rớt Luân Chuyển KTC:",
                "Con số tổng toàn vùng tuần này là 1,69%, cơ bản mình vẫn giữ được dưới ngưỡng khống chế 1,8% của công ty.",
                "Hai tỉnh làm rất chuẩn chỉ là Bình Thuận (0,28%) và Khánh Hòa (0,48%), tỷ lệ rớt gần như bằng không.",
                "Tuy nhiên, khi nhìn vào con số tuyệt đối 219 đơn bị rớt lại trong tuần, thì có tới 121 đơn — tức là hơn một nửa — nằm trọn ở tỉnh Lâm Đồng, và 60 đơn nằm ở Ninh Thuận!",
                "Điểm mặt 4 bưu cục để rớt hàng nhiều nhất: Đức Trọng 1 rớt 42 đơn, Phan Rang rớt 38 đơn, Lang Biang rớt 29 đơn và Xuân Hương rớt 24 đơn.",
                "Nguyên nhân ở đây là gì?",
                "Là do nhân viên bưu cục làm hàng trễ, không kịp giờ cắt hàng (Cut-off time) của xe KTC. Xe tải tới nơi bấm còi chờ 15 phút không thấy bao hàng seal xong thì tài xế buộc phải chạy theo lộ trình giờ giấc, để lại bao hàng nằm chỏng chơ ở góc bưu cục!",
                "Đơn bị rớt luân chuyển là tự động trễ thêm 24 tiếng, hôm sau giao chắc chắn dính lỗi trễ ODR.",
                "Em đề nghị anh Tiến, anh Nhựt, anh Lợi và anh Trường: Bắt buộc Trưởng các bưu cục trên phải đóng túi seal trước giờ xe đến tối thiểu 20 phút. Tuyệt đối không để xảy ra tình trạng xe tải đến nơi mới cuống cuồng đi tìm hàng đóng bao!\""
            ],
            "insights": [
                "Bình Thuận và Khánh Hòa duy trì tỷ lệ rớt dưới 0,5% chứng tỏ quy trình bàn giao ca xe KTC hoàn toàn có thể chuẩn hóa được.",
                "Hơn 55% lượng đơn rớt luân chuyển dồn ở Lâm Đồng do địa hình đèo dốc và lịch xe chạy buổi tối rất khắt khe."
            ],
            "warnings": [
                "219 đơn rớt luân chuyển đồng nghĩa với 219 khách hàng bị trễ hẹn ít nhất 1 ngày, gia tăng nguy cơ khiếu nại và hủy đơn."
            ],
            "actions": [
                "Quy định giờ giới nghiêm đóng bao seal tại bưu cục trước giờ xe KTC cập bến 20 phút; bưu cục nào làm rớt xe phải tự chịu chi phí chuyển xe tăng cường."
            ]
        },

        # TOPIC 10
        {
            "sec_title": "🔄 [X. BÁO CÁO TỶ LỆ %FD (RETURN / HOÀN TRẢ) — VÙNG NAM TRUNG BỘ (W40)]",
            "speech_title": "🗣️ PHÂN TÍCH TỶ LỆ HOÀN TRẢ (%FD 7.77%) VÀ CẢNH BÁO BẤT THƯỜNG (TAB 11):",
            "speech_paragraphs": [
                "📍 1. BẢNG TỶ LỆ HOÀN TRẢ THEO 5 TỈNH THÀNH (W40 vs W39):",
                "• Khánh Hòa: 6,90% (tốt nhất vùng, kiểm soát hoàn trả rất chặt chẽ).",
                "• Bình Thuận: 7,10% (ở ngưỡng an toàn).",
                "• Ninh Thuận: 7,40% (ở ngưỡng an toàn).",
                "• Lâm Đồng: 8,60% (vượt ngưỡng kiểm soát 8,0%).",
                "• Đắk Nông: 9,10% (tỷ lệ hoàn cao nhất vùng).",
                "• Toàn vùng: Full hàng đạt 7,77% (24.498 đơn hoàn / 315.328 đơn xử lý) | TikTok Shop đạt 6,10% (4.191 đơn hoàn / 68.719 đơn).",
                "📍 2. CẢNH BÁO TOP BƯU CỤC HOÀN TRẢ BẤT THƯỜNG:",
                "• (DNO) Quảng Tín: Tỷ lệ hoàn lên tới 28,40% (AM Trương Quang Linh).",
                "• (LDO) Lang Biang - Đà Lạt 1: Tỷ lệ hoàn 18,20% (AM Lê Minh Lợi).",
                "• (LDO) Đức Trọng 1: Tỷ lệ hoàn 14,50% (AM Trầm Hữu Tiến).",
                "• Nghi vấn nghiệp vụ: Có dấu hiệu shipper lười đi phát tuyến xa, bấm lý do 'Khách không nhận' hoặc 'Không liên lạc được 3 lần' để xả tải đẩy hàng hoàn về kho.",
                "🎙️ LỜI THOẠI THUYẾT TRÌNH TỰ NHIÊN (KHI BẬT TAB 11 HOÀN TRẢ %FD):",
                "\"Dạ qua tới Tab 11 về tỷ lệ Hoàn trả (%FD):",
                "Mặt bằng chung toàn vùng tuần này là 7,77%, kênh TikTok Shop là 6,10%, nhìn chung vẫn nằm trong biên độ an toàn dưới 8% của công ty.",
                "Khánh Hòa, Bình Thuận và Ninh Thuận kiểm soát rất tốt, chỉ quanh mức 7%.",
                "Nhưng khi nhìn lên 2 tỉnh miền núi Lâm Đồng (8,6%) và Đắk Nông (9,1%), đặc biệt là 3 bưu cục trên màn hình:",
                "Quảng Tín hoàn tới 28,4%! Tức là cứ 4 đơn giao đi thì có hơn 1 đơn bị trả về!",
                "Lang Biang hoàn hơn 18% và Đức Trọng 1 hoàn 14,5%!",
                "Đây là những con số cực kỳ bất thường. Bộ phận Chăm sóc khách hàng phúc tra ngẫu nhiên đã phát hiện: Shipper chạy tuyến xã vùng sâu ngại đi xa, gọi điện cho khách 1 cuộc chuông reo chưa kịp bắt máy đã vội vàng bấm lên app là 'Khách từ chối nhận' để trả hàng về bưu cục!",
                "Việc này làm các shop bán hàng họ rất bức xúc, vì họ mất tiền chạy quảng cáo, mất tiền đóng gói mà hàng chưa kịp tới tay người mua đã bị bấm hoàn về.",
                "Em đề nghị Trưởng bưu cục Quảng Tín và Lang Biang: Từ tuần này, 100% đơn trước khi bấm duyệt trạng thái Chuyển Hoàn bắt buộc CS bưu cục phải gọi điện xác nhận lại với người mua. Nếu phát hiện shipper khai báo gian dối để xả tải thì xử lý kỷ luật nghiêm theo quy chế!\""
            ],
            "insights": [
                "TikTok Shop kiểm soát hoàn trả ở mức 6,10% chứng tỏ người mua trên sàn có độ cam kết nhận hàng cao hơn khách mua lẻ bên ngoài.",
                "Tỷ lệ hoàn cao tại các huyện vùng sâu chủ yếu bắt nguồn từ hành vi xả tải của shipper chứ không phải do lỗi của shop."
            ],
            "warnings": [
                "Bưu cục Quảng Tín hoàn 28,4% đang đẩy chi phí vận chuyển ngược lên rất cao và làm mất uy tín thương hiệu GHN."
            ],
            "actions": [
                "Bắt buộc CS bưu cục phúc tra độc lập 100% đơn hàng trước khi cho phép bấm hoàn trả tại các bưu cục có %FD > 12%."
            ]
        },

        # TOPIC 11
        {
            "sec_title": "🚛 [XI. BÁO CÁO ĐIỀU HÀNH KTC, VẬN TẢI, %TLTĐ THÙNG XE (45.6%) & 124 CHUYẾN NON TẢI (W40)]",
            "speech_title": "🗣️ HIỆU QUẢ VẬN TẢI KTC: XỬ LÝ 124 CHUYẾN XE NON TẢI DƯỚI 30% THÙNG (TAB 12):",
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
                "📍 2. ĐÁNH GIÁ CHI PHÍ VẬN TẢI:",
                "• 124 chuyến xe non tải dưới 30% thùng xe đang trực tiếp làm lãng phí hàng trăm triệu đồng tiền dầu và chi phí thuê xe.",
                "• Tuyến Đức Trọng - Lâm Đồng và Đắk Nông cần tái cấu trúc ngay lịch xuất bến xe tải.",
                "🎙️ LỜI THOẠI THUYẾT TRÌNH TỰ NHIÊN (KHI BẬT TAB 12 VẬN TẢI & KTC):",
                "\"Dạ qua tới Tab 12 về Điều hành KTC và Chi phí Vận tải đường trục:",
                "Mọi người nhìn vào con số %TLTĐ thùng xe tuần này: Rất đáng lo ngại khi tụt từ 47,7% xuống chỉ còn 45,6%, giảm mất -2,1%p!",
                "Và trên hệ thống giám sát hành trình tuần qua phát hiện có tới 124 CHUYẾN XE TẢI KTC lăn bánh trên đường với tỷ lệ lấp đầy thùng dưới 30%!",
                "Trong tổng số 513 chuyến xe toàn vùng, thì cứ 4 chuyến xe chạy trên đường lại có 1 chuyến chạy non tải, thậm chí có 7 chuyến xe gần như rỗng không dưới 10% thùng xe!",
                "Điểm nóng nhất nằm ở đâu?",
                "Chính là KTC Đức Trọng ở Lâm Đồng: Một mình Đức Trọng gánh tới 43 chuyến xe non tải, tỷ lệ lấp đầy rơi tự do xuống 40,6%! Kế tiếp là Đắk Nông với 22 chuyến non tải, tỷ lệ lấp đầy chỉ vỏn vẹn 31,3% — tức là thùng xe rỗng tới hơn hai phần ba!",
                "Chúng ta đang trả nguyên tiền cước xe, tiền dầu, tiền cầu đường cho những chuyến xe chở gió.",
                "Nguyên nhân là do biểu đồ giờ chạy xe đang bị cứng nhắc, cứ tới giờ là xe chạy bất kể lượng hàng nhiều hay ít.",
                "Em đề xuất Ban Vận tải trong tuần W41 này:",
                "Phải rà soát và xử lý ngay 124 chuyến xe non tải này: Tuyến nào sản lượng ít thì gộp 2 chuyến làm một hoặc chuyển sang dùng xe tải nhỏ 1,5 tấn. Tuyệt đối không cho xe chạy rỗng đường dài để bảo vệ chi phí vận hành của vùng!\""
            ],
            "insights": [
                "Biểu đồ chạy xe cố định đang không theo kịp biến động sản lượng hàng ngày trong tuần, gây lãng phí lớn vào các ngày thứ Hai, thứ Ba.",
                "KTC Đức Trọng (43 xe non tải) và Đắk Nông (31,3% TLTĐ) là hai nút thắt trọng điểm cần tối ưu hóa phương tiện."
            ],
            "warnings": [
                "124 chuyến xe non tải trực tiếp làm đội chi phí trên mỗi đơn hàng (Cost Per Order - CPO) của vùng Nam Trung Bộ."
            ],
            "actions": [
                "Ban Vận tải làm việc với các nhà xe đối tác: Linh hoạt dời chuyến hoặc gộp tuyến bưu cục huyện có sản lượng dưới 30% thùng xe."
            ]
        },

        # TOPIC 12
        {
            "sec_title": "⏳ [XII. ĐIỀU HÀNH XỬ LÝ HÀNG AGING TỒN ĐỌNG & TREO LUÂN CHUYỂN (W40)]",
            "speech_title": "🗣️ CHIẾN DỊCH GIẢI TỎA 1.420 ĐƠN AGING >5 NGÀY & 118 ĐƠN TREO LUÂN CHUYỂN (TAB 13):",
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
                "🎙️ LỜI THOẠI THUYẾT TRÌNH TỰ NHIÊN (KHI BẬT TAB 13 HÀNG AGING & TREO LC):",
                "\"Dạ qua tới Tab 13 về Hàng tồn Aging và Đơn treo luân chuyển:",
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

        # TOPIC 13
        {
            "sec_title": "💰 [XIII. QUẢN TRỊ DÒNG TIỀN COD, TỶ LỆ THANH TOÁN QR & THU HỒI CÔNG NỢ (W40)]",
            "speech_title": "🗣️ QUẢN TRỊ DÒNG TIỀN COD (82.6 TỶ ₫): TỶ LỆ QR TĂNG VỌT LÊN 62.9% (TAB 14):",
            "speech_paragraphs": [
                "📍 1. BẢNG CHỈ SỐ THU HỘ COD THEO 5 TỈNH THÀNH (W40 vs W39):",
                "• Tổng tiền COD toàn vùng thu hộ tuần W40: 82.610,5 triệu đồng (~82,6 tỷ đồng).",
                "• Tỷ lệ thanh toán Chuyển khoản QR / Online: Tăng vọt lên 62,90% (tăng +3,0%p so với 59,9% W39).",
                "• Tỷ lệ thu bằng Tiền mặt: Giảm mạnh từ 40,1% xuống còn 37,10% ➔ Hạn chế tối đa tiền mặt trôi nổi.",
                "• Khánh Hòa: Tỷ lệ QR cao nhất vùng đạt 64,50% (tiền mặt chỉ còn 35,5%).",
                "• Ninh Thuận: Đạt 61,20% QR.",
                "• Bình Thuận: Đạt 58,50% QR (tiền mặt còn 41,5%).",
                "• Lâm Đồng: Đạt 56,80% QR (tiền mặt còn 43,2%).",
                "• Đắk Nông: Tỷ lệ tiền mặt còn cao nhất vùng ở mức 48,50% (QR đạt 51,50%).",
                "📍 2. KỶ LUẬT NỘP TIỀN VỀ CÔNG TY:",
                "• 100% bưu cục thực hiện nộp tiền COD về tài khoản tổng công ty trước 21h00 hàng ngày.",
                "• Cảnh báo: Vẫn còn hiện tượng shipper giữ tiền mặt qua đêm tại một số bưu cục huyện xa ngân hàng.",
                "🎙️ LỜI THOẠI THUYẾT TRÌNH TỰ NHIÊN (KHI BẬT TAB 14 DÒNG TIỀN COD & QR):",
                "\"Dạ qua tới Tab 14 về Quản trị dòng tiền COD:",
                "Tuần này toàn vùng Nam Trung Bộ thu hộ tổng cộng hơn 82,6 tỷ đồng tiền hàng cho các shop.",
                "Và có một bước tiến cực kỳ quan trọng về an toàn tài chính: Đó là tỷ lệ khách thanh toán bằng quét mã QR tuần này đã tăng vọt lên 62,9%, kéo tỷ lệ tiền mặt giảm sâu xuống chỉ còn 37,1%!",
                "Đây là nỗ lực rất lớn của các anh em shipper bưu cục khi đã chủ động in mã QR mang theo tuyến và khuyến khích khách hàng quét mã thanh toán thay vì dùng tiền mặt.",
                "Khánh Hòa và Ninh Thuận đang đi đầu với tỷ lệ QR trên 61% đến 64%.",
                "Tiền vào thẳng tài khoản công ty vừa an toàn, vừa không sợ shipper bị cướp giật trên đường, mà bưu cục cũng không phải lo giữ tiền mặt trong két sắt qua đêm.",
                "Tuy nhiên, ở Đắk Nông và Bình Thuận tỷ lệ tiền mặt vẫn còn trên 41% đến 48%, do bà con vùng nông thôn chưa quen dùng app ngân hàng.",
                "Em xin nhắc nhở các AM và Trưởng bưu cục: Quy định tài chính của GHN là tuyệt đối không để tiền mặt COD tồn qua đêm tại bưu cục. Bưu cục nào không có ngân hàng mở cửa buổi tối thì Trưởng bưu cục phải chuyển tiền qua Viettel Money hoặc cây ATM trước 20h30. Bất kỳ trường hợp nào shipper giữ tiền mặt quá 24h sẽ bị khóa tài khoản thu tiền ngay lập tức!\""
            ],
            "insights": [
                "Tỷ lệ QR đạt 62,9% giúp giảm bớt hơn 2,5 tỷ đồng tiền mặt lưu thông trên đường mỗi tuần, giảm thiểu rủi ro kiểm đếm và thất thoát.",
                "Khánh Hòa duy trì văn hóa thanh toán không tiền mặt tốt nhất vùng với 64,5% giao dịch qua QR."
            ],
            "warnings": [
                "Đắk Nông vẫn còn 48,5% tiền mặt; rủi ro shipper cầm số tiền lớn di chuyển trên các cung đường đèo vắng vẻ vào buổi tối."
            ],
            "actions": [
                "Trang bị 100% thẻ đeo mã QR cho bưu tá; kiểm tra số dư quỹ tiền mặt bưu cục trên hệ thống lúc 21h00 hàng ngày."
            ]
        },

        # TOPIC 14
        {
            "sec_title": "🚨 [XIV. BÁO CÁO TRUY THU – BIẾN ĐỘNG 2 TUẦN (W39 vs W40) & CẢNH BÁO BÙNG PHÁT 187.1 TRIỆU ₫]",
            "speech_title": "🗣️ BÁO CÁO TRUY THU: W40 CẦN THU 187.1 TR ₫ VÀ ĐIỂM NÓNG BẮC CAM RANH (TAB 15):",
            "speech_paragraphs": [
                "📍 1. BẢNG SO SÁNH BIẾN ĐỘNG 2 TUẦN (W40 vs W39):",
                "• Số bản ghi phát sinh: 2.424 bản ghi (W39: 4.076 bản ghi, giảm -1.652 đơn / -40,5%).",
                "• Số tiền truy thu ban đầu: 433,05 Tr ₫ (W39: 317,25 Tr ₫, TĂNG +115,8 Tr ₫ / +36,5%!).",
                "• Số tiền đã điều chỉnh / giảm trừ: -245,96 Tr ₫ (W39: -5,17 Tr ₫).",
                "• SỐ TIỀN CẦN TRUY THU THỰC TẾ: 187,09 Tr ₫ (giảm -124,99 Tr ₫ / -40,1% so với 312,08 Tr ₫ của W39).",
                "📍 2. CƠ CẤU THEO LOẠI TRUY THU TRỌNG ĐIỂM:",
                "• 1. Liên đới chiếm dụng: 56,8 Tr ₫ (4 đơn) ➔ TÍNH CHẤT ĐẶC BIỆT NGHIÊM TRỌNG.",
                "• 2. Tick mất hàng: 41,2 Tr ₫ (53 đơn).",
                "• 3. Mất / Thiếu / Tráo sản phẩm: 30,9 Tr ₫ (76 đơn).",
                "• 4. Sai lệch cân nặng / kích thước: 28,5 Tr ₫.",
                "• 5. Các lỗi vận hành và hoàn chậm khác: ~29,7 Tr ₫.",
                "📍 3. BẢNG TRUY THU THEO TỈNH VÀ TOP AM NÓNG NHẤT:",
                "• Tỉnh: Lâm Đồng 72,5 Tr ₫ (827 đơn) | Khánh Hòa 69,3 Tr ₫ (296 đơn) | Đắk Nông 28,3 Tr ₫ (774 đơn) | Khác 11,4 Tr ₫ | Bình Thuận 4,8 Tr ₫ | Ninh Thuận 0,7 Tr ₫.",
                "• 🔴 TOP 1 NGUY HIỂM: AM Nguyễn Thanh Long (Khánh Hòa): 51,2 Tr ₫ / 72 ticket ➔ ĐIỂM NÓNG BƯU CỤC (KHO) BẮC CAM RANH PHÁT SINH 48,7 TRIỆU ₫ LIÊN ĐỚI CHIẾM DỤNG TIỀN HÀNG!",
                "• 🔴 TOP 2: AM Lê Văn Trường (Lâm Đồng): 26,3 Tr ₫ / 419 ticket (nhiều ticket nhất vùng, bưu cục Đơn Dương chiếm 12,8 Tr ₫).",
                "• 🔴 TOP 3: AM Trần Văn Phước: 22,9 Tr ₫ / 288 ticket.",
                "• 🔴 TOP 4: AM Huỳnh Thị Kim Chi (Lâm Đồng): 21,3 Tr ₫ / 110 ticket.",
                "• 🔴 TOP 5: AM Trương Quang Linh (Đắk Nông): 13,0 Tr ₫ tại bưu cục Quảng Tín.",
                "🎙️ LỜI THOẠI THUYẾT TRÌNH TỰ NHIÊN (KHI BẬT TAB 15 TRUY THU):",
                "\"Kính thưa Ban Giám Đốc, đây là nội dung cảnh báo nóng nhất và nghiêm trọng nhất trong buổi họp hôm nay:",
                "Nhìn vào con số tổng, tuần W40 số tiền cần truy thu đã giảm được 40%, từ 312 triệu xuống còn 187,1 triệu đồng nhờ bộ phận Kế toán đã rà soát giảm trừ được 246 triệu.",
                "NHƯNG, số tiền phát sinh ban đầu lại TĂNG VỌT từ 317 triệu lên tới 433 triệu đồng (+36,5%)!",
                "Và khi bóc tách từng loại lỗi, chúng ta phát hiện một vụ việc CỰC KỲ NGHIÊM TRỌNG:",
                "Mọi người nhìn vào dòng đầu tiên: Lỗi 'Liên đới chiếm dụng' phát sinh 56,8 triệu đồng!",
                "Trong đó, chỉ riêng bưu cục Bắc Cam Ranh thuộc cụm quản lý của AM NGUYỄN THANH LONG đã chiếm tới 48,7 triệu đồng!",
                "Đây không còn là lỗi nghiệp vụ cân đo sai hay thất lạc hàng nữa, mà là dấu hiệu chiếm dụng tiền hàng và gian lận có hệ thống tại bưu cục!",
                "Bên cạnh đó, chỗ anh Lê Văn Trường ở Lâm Đồng đang gánh tới 419 ticket truy thu — nhiều nhất toàn vùng Nam Trung Bộ, với số tiền 26,3 triệu đồng, tập trung nặng nhất ở bưu cục Đơn Dương 12,8 triệu.",
                "Chỗ anh Phước 22,9 triệu, chị Chi 21,3 triệu và anh Linh Đắk Nông 13 triệu tại bưu cục Quảng Tín.",
                "Em xin kiến nghị Ban Giám Đốc chỉ đạo khẩn cấp:",
                "Yêu cầu anh Nguyễn Thanh Long và Trưởng bưu cục Bắc Cam Ranh phải có mặt tại văn phòng giải trình trực tiếp với Ban Giám Đốc và Thanh tra trong sáng ngày mai.",
                "Anh Trường và chị Chi phải phân loại xử lý dứt điểm 419 ticket tại Lâm Đồng trước thứ Sáu. Tuyệt đối không để số tiền 187,1 triệu này biến thành nợ xấu khó đòi của công ty!\""
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

        # TOPIC 15
        {
            "sec_title": "📈 [XV. PHÂN TÍCH DOANH THU KINH DOANH & TĂNG TRƯỞNG KHÁCH HÀNG MỚI (F30) | VÙNG NTB]",
            "speech_title": "🗣️ DOANH THU KINH DOANH 1.120 TỶ ₫, PHÁT TRIỂN 111 SHOP F30 & QUẢN TRỊ SHOP NHÓM A (TAB 16):",
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
                "🎙️ LỜI THOẠI THUYẾT TRÌNH TỰ NHIÊN (KHI BẬT TAB 16 KINH DOANH & F30):",
                "\"Dạ qua tới Tab cuối cùng về mảng Kinh Doanh và Khách Hàng Mới F30:",
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

        # TOPIC 16
        {
            "sec_title": "🏁 [XVI. ĐIỀU HÀNH TRỌNG ĐIỂM: 13 BƯU CỤC CẢNH BÁO BẤT ỔN & 5 TRỌNG TÂM HÀNH ĐỘNG TUẦN W41]",
            "speech_title": "🗣️ DANH SÁCH 13 BƯU CỤC CẢNH BÁO ĐỎ & 5 NHIỆM VỤ ĐIỀU HÀNH HIỆN TRƯỜNG TUẦN W41:",
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
                "• Trọng tâm 1: Duy trì kỷ luật Last-mile, giữ vững %GTC trên 60%, nâng tỷ lệ Gán Ca 2 từ 62,4% lên trên 85%.",
                "• Trọng tâm 2: Quyết liệt thu hồi công nợ & truy thu: Xử lý dứt điểm 187,1 Tr ₫, phong tỏa và thu hồi vụ 48,7 Tr ₫ tại Bắc Cam Ranh.",
                "• Trọng tâm 3: Cứu vãn ODR tại 3 điểm đáy: Nâng ODR Lang Biang, Quảng Tín, Đơn Dương lên trên 85% bằng cơ chế phát tăng cường ca chiều tối.",
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
                "Bưu cục nào nằm trong danh sách cảnh báo đỏ quá 4 tuần liên tiếp mà không có chuyển biến (như Quảng Tín 100 ngày, Lang Biang 108 ngày) sẽ bị thay thế Trưởng bưu cục ngay trong tháng 10."
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

    # Save Word files
    out_docx1 = "KICH_BAN_THUYET_TRINH_W40_NAM_TRUNG_BO.docx"
    out_docx2 = "KICH_BAN_THUYET_TRINH_MOI_NHAT.docx"
    try:
        doc.save(out_docx1)
        print(f"Saved DOCX: {out_docx1}")
    except Exception as e:
        print(f"Warning saving {out_docx1}: {e}")
        
    try:
        doc.save(out_docx2)
        print(f"Saved DOCX: {out_docx2}")
    except Exception as e:
        try:
            out_alt = "KICH_BAN_THUYET_TRINH_MOI_NHAT_V2.docx"
            doc.save(out_alt)
            print(f"File {out_docx2} is locked in Word. Saved to {out_alt} instead.")
        except Exception as e2:
            print(f"Note: Word files are open in MS Word: {e2}")

    # Generate HTML file
    build_html_file(sections_data)

    # Generate MD file
    build_md_file(sections_data)

def build_html_file(sections_data):
    html_lines = []
    html_lines.append("""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kịch Bản Thuyết Trình Điều Hành W40 — Vùng Nam Trung Bộ</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Outfit:wght@600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --bg-body: #f8fafc;
            --bg-card: #ffffff;
            --text-main: #0f172a;
            --text-muted: #64748b;
            --ghn-orange: #ea580c;
            --ghn-blue: #0f4c81;
            --success: #16a34a;
            --danger: #dc2626;
            --warning: #d97706;
            --border: #e2e8f0;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: var(--bg-body);
            color: var(--text-main);
            line-height: 1.6;
            padding: 24px;
        }
        .container {
            max-width: 1080px;
            margin: 0 auto;
            background: var(--bg-card);
            border-radius: 16px;
            box-shadow: 0 10px 25px -5px rgba(0,0,0,0.05);
            padding: 40px;
            border: 1px solid var(--border);
        }
        .header-box {
            text-align: center;
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 24px;
            margin-bottom: 32px;
        }
        .header-sub { font-size: 13px; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px; }
        .header-title { font-family: 'Outfit', sans-serif; font-size: 26px; font-weight: 800; color: var(--ghn-blue); margin: 8px 0; }
        .header-date { font-size: 14px; color: var(--text-muted); font-style: italic; }
        .header-tag { display: inline-block; background: #fff7ed; color: var(--ghn-orange); border: 1px solid #ffedd5; font-size: 12px; font-weight: 700; padding: 4px 12px; border-radius: 20px; margin-top: 10px; }
        
        .section-card {
            background: #ffffff;
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 28px;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);
        }
        .section-title {
            font-family: 'Outfit', sans-serif;
            font-size: 18px;
            font-weight: 700;
            color: var(--ghn-blue);
            margin-bottom: 16px;
            border-left: 4px solid var(--ghn-orange);
            padding-left: 12px;
        }
        .speech-heading {
            font-size: 14px;
            font-weight: 700;
            color: #b45309;
            background: #fef3c7;
            padding: 8px 14px;
            border-radius: 8px;
            margin-bottom: 14px;
            display: inline-block;
        }
        p { margin-bottom: 12px; font-size: 14.5px; }
        .bullet-point { margin-left: 20px; margin-bottom: 8px; font-size: 14.5px; }
        
        .callout {
            border-radius: 8px;
            padding: 12px 16px;
            margin: 12px 0;
            font-size: 13.5px;
        }
        .callout-insight { background: #eff6ff; border-left: 4px solid #3b82f6; color: #1e40af; }
        .callout-warning { background: #fef2f2; border-left: 4px solid #ef4444; color: #991b1b; }
        .callout-action { background: #f0fdf4; border-left: 4px solid #22c55e; color: #166534; }
        .callout-title { font-weight: 700; margin-bottom: 6px; display: flex; align-items: center; gap: 6px; }

        .top-btn {
            position: fixed;
            bottom: 24px;
            right: 24px;
            background: var(--ghn-orange);
            color: white;
            padding: 10px 18px;
            border-radius: 30px;
            text-decoration: none;
            font-weight: 700;
            font-size: 13px;
            box-shadow: 0 4px 12px rgba(234, 88, 12, 0.4);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header-box">
            <div class="header-sub">GHN EXPRESS — VÙNG NAM TRUNG BỘ</div>
            <div class="header-title">BÁO CÁO VẬN HÀNH & KINH DOANH TUẦN W40</div>
            <div class="header-date">(Chu kỳ dữ liệu: 28/09/2026 – 04/10/2026)</div>
            <div class="header-tag">Kịch bản thuyết trình 16 chuyên đề điều hành chuẩn hóa — Chỉ số Tỉnh đặt lên đầu, phân tích sâu theo 18 AM & Giao việc hiện trường</div>
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
