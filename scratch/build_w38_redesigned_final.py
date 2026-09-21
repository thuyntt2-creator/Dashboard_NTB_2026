import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

sys.path.insert(0, os.path.join(os.getcwd(), 'scratch'))
from doc_builder_helpers import format_run
from redesign_helpers import add_redesigned_callout

def build_w38_redesigned_document():
    doc = docx.Document()
    
    # 1 inch margins
    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)
        
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
    r1 = p1.add_run("BÁO CÁO VẬN HÀNH & KINH DOANH TUẦN W38")
    format_run(r1, font_size_pt=20, bold=True, color_rgb=(0x0F, 0x4C, 0x81))

    p2 = doc.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p2.paragraph_format.space_before = Pt(0)
    p2.paragraph_format.space_after = Pt(4)
    r2 = p2.add_run("(Chu kỳ dữ liệu: 14/09/2026 – 20/09/2026)")
    format_run(r2, font_size_pt=11, italic=True, color_rgb=(0x4B, 0x55, 0x63))

    p3 = doc.add_paragraph()
    p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p3.paragraph_format.space_before = Pt(0)
    p3.paragraph_format.space_after = Pt(14)
    r3 = p3.add_run("Kịch bản thuyết trình 16 chuyên đề điều hành chuẩn hóa — Chỉ số Tỉnh đặt lên đầu, phân tích sâu theo 18 AM & Giao việc hiện trường")
    format_run(r3, font_size_pt=11, italic=True, color_rgb=(0xEA, 0x58, 0x0C))

    # =========================================================================
    # 1. TỔNG HỢP TRỌNG TÂM W38
    # =========================================================================
    add_redesigned_callout(
        doc,
        section_title="📊 [I. TỔNG HỢP TRỌNG TÂM HỌP TUẦN W38 — VÙNG NAM TRUNG BỘ]",
        speech_title="🗣️ LỜI MỞ ĐẦU & TỔNG QUAN ĐIỀU HÀNH VÙNG TUẦN W38:",
        province_block=[
            "• Khánh Hòa: 96.012 đơn (+3,0% WoW) | %GTC 58,9% (cao nhất vùng) | %ODR 93,1% | Truy thu: 68,0 Tr ₫.",
            "• Lâm Đồng: 95.727 đơn (-3,7% WoW) | Dẫn đầu TTS (19.587 đơn) | %GTC 53,8% (thấp nhất) | %ODR 89,8% | Truy thu: 155,0 Tr ₫ (chiếm 55% vùng).",
            "• Bình Thuận: 85.489 đơn (-6,0% WoW) | %GTC 57,2% | %ODR 92,4% | KTC lấp đầy 51,3% | Truy thu: 20,2 Tr ₫.",
            "• Đắk Nông: 34.848 đơn (-8,7% WoW) | %GTC 54,1% | %ODR 90,1% | KTC lấp đầy 37,0% | Truy thu: 24,8 Tr ₫.",
            "• Ninh Thuận: 33.918 đơn (-4,5% WoW) | %GTC 55,1% | %ODR 91,0% | Truy thu: 14,4 Tr ₫.",
            "➔ TOÀN VÙNG: 345.994 đơn Full (-3,2%) | TikTok Shop 69.274 đơn (+0,8%, chiếm 20,0%) | %GTC 55,75% | %ODR 91,2% | %TLTĐ KTC 51,0% (76 xe non tải) | Truy thu bùng phát 282,4 Tr ₫."
        ],
        am_analysis_block=[
            "Kính chào Ban Giám Đốc và toàn thể 18 anh chị Quản lý Vận hành (AM). Nhìn vào bức tranh tuần W38, sự phân hóa giữa các AM đang thể hiện rất rõ ràng:",
            "• Nhóm AM dẫn đầu sản lượng và doanh thu: AM Nguyễn Duy Long (43.018 đơn) và AM Thái Thị Thanh Thư (32.538 đơn, tăng trưởng mạnh nhất vùng +2.729 đơn) tiếp tục là hai trụ cột gánh tải cho vùng.",
            "• Nhóm AM giữ chất lượng giao hàng (%GTC) xuất sắc: Chúc mừng AM Nguyễn Ngọc Khánh (đạt 75,1% GTC), AM Cao Thị Thanh Thủy (đạt 71,1% GTC) và AM Nguyễn Đỗ Minh Nghĩa (đạt 70,8% GTC). Đây là 3 AM duy trì kỷ luật giao hàng vượt trên mốc 70%.",
            "• Nhóm 3 AM báo động đỏ cần chấn chỉnh khẩn cấp: AM Nguyễn Thanh Long (GTC sụt sâu về 36,7%, giảm -10,2%p WoW), AM Lê Minh Lợi (GTC chỉ đạt 32,1%) và AM Trương Quang Linh (GTC thấp nhất toàn mạng 16,8%).",
            "Tuần này chúng ta có 2 vấn đề nổi cộm làm xói mòn chi phí: Hiệu suất xe tải KTC giảm về 51,0% với 76 chuyến non tải <30% thùng; và tiền truy thu tăng vọt lên 282,4 triệu đồng mà hơn một nửa nằm ở địa bàn các bưu cục của Lâm Đồng."
        ],
        insights=[
            "TikTok Shop chiếm tròn 20% sản lượng toàn vùng, khẳng định các AM phải ưu tiên tuyệt đối nguồn lực lấy hàng và giao nhanh cho kênh này.",
            "Khâu First-mile lấy hàng làm rất tốt (%LTC TTS đạt đỉnh 95,4%), nhưng Last-mile bị đứt gãy ở ca chiều khiến công sức cả chuỗi bị ảnh hưởng."
        ],
        warnings=[
            "76 chuyến xe tải KTC chạy rỗng dưới 30% thùng đang trực tiếp đốt chi phí vận chuyển đường trục của vùng.",
            "Khoản tiền truy thu 282,4 triệu đồng nếu các AM không đôn đốc thu hồi sẽ trở thành nợ khó đòi và thiệt hại tài chính cho công ty."
        ],
        actions=[
            "Toàn thể 18 AM quán triệt ngay 3 trọng tâm: Siết chặt ca giao chiều, tối ưu gom tải chuyến xe KTC và kiểm soát 100% cân đo tại bàn tiếp nhận hàng."
        ]
    )

    # =========================================================================
    # 2. SẢN LƯỢNG GIAO 5 TỈNH & 18 AM
    # =========================================================================
    add_redesigned_callout(
        doc,
        section_title="📦 [II. PHÂN TÍCH SẢN LƯỢNG GIAO TOÀN VÙNG, 5 TỈNH THÀNH & 18 AM (W38)]",
        speech_title="🗣️ ĐÁNH GIÁ SẢN LƯỢNG 5 TỈNH & XẾP HẠNG TĂNG TRƯỞNG 18 AM:",
        province_block=[
            "• Top 1 - Khánh Hòa: 96.012 đơn (tăng +2.828 đơn, +3,0% WoW) | TTS: 18.142 đơn ➔ Tỉnh duy nhất tăng trưởng dương toàn vùng!",
            "• Top 2 - Lâm Đồng: 95.727 đơn (giảm -3.657 đơn, -3,7% WoW) | TTS: 19.587 đơn (+942 đơn WoW, dẫn đầu TTS vùng).",
            "• Top 3 - Bình Thuận: 85.489 đơn (giảm -5.475 đơn, -6,0% WoW) | TTS: 15.873 đơn (+157 đơn WoW).",
            "• Top 4 - Đắk Nông: 34.848 đơn (giảm -3.341 đơn, -8,7% WoW) | TTS: 8.314 đơn (-343 đơn WoW) ➔ Tỉnh có mức giảm sâu nhất.",
            "• Top 5 - Ninh Thuận: 33.918 đơn (giảm -1.610 đơn, -4,5% WoW) | TTS: 7.358 đơn (+7 đơn WoW).",
            "➔ TỔNG TOÀN VÙNG: 345.994 đơn Full hàng (-3,2% WoW) | TikTok Shop: 69.274 đơn (+0,8% WoW)."
        ],
        am_analysis_block=[
            "Kính thưa Ban Giám Đốc, nhìn sâu vào bảng xếp hạng quy mô sản lượng của 18 AM tuần W38:",
            "• Top 5 AM có sản lượng giao lớn nhất vùng:",
            "  1. AM Nguyễn Duy Long: 43.018 đơn (quản lý địa bàn trọng điểm Bình Thuận, giảm -2.575 đơn WoW).",
            "  2. AM Thái Thị Thanh Thư: 32.538 đơn (tăng trưởng ngoạn mục +2.729 đơn WoW, tương ứng +9,1% — AM tăng sản lượng tốt nhất vùng!).",
            "  3. AM Lê Thanh Nhựt: 30.600 đơn (giảm -1.637 đơn WoW).",
            "  4. AM Lê Văn Trường: 28.919 đơn (giảm -2.299 đơn WoW tại cụm Đà Lạt - Đơn Dương).",
            "  5. AM Nguyễn Ngọc Khánh: 28.325 đơn (giảm -2.092 đơn WoW tại Nha Trang).",
            "• Nhóm AM tăng trưởng dương tuần này: Ngoài AM Thư (+2.729 đơn), có AM Phan Đình Duy (+900 đơn, đạt 24.931 đơn), AM Nguyễn Lê Nguyên Vũ (+491 đơn, đạt 13.500 đơn), AM Nguyễn Thanh Long (+163 đơn, đạt 14.127 đơn).",
            "• Nhóm AM sụt giảm tải lớn: AM Huỳnh Thúc Duân (-1.104 đơn, chỉ còn 4.984 đơn), AM Nguyễn Hoàng Phi (-964 đơn), AM Hồng Bích Nga (-865 đơn, đạt 20.840 đơn).",
            "• Nhóm AM địa bàn nhỏ: AM Lê Minh Lợi (3.178 đơn, -411 đơn), AM Trương Quang Linh (1.857 đơn, -234 đơn)."
        ],
        insights=[
            "Khánh Hòa đã chính thức vượt Lâm Đồng về tổng sản lượng Full hàng nhờ sự bứt phá mạnh của tuyến Nha Trang do AM Phan Đình Duy và AM Nguyễn Ngọc Khánh phụ trách.",
            "Sản lượng TikTok Shop toàn vùng tăng nhẹ +0,8% chứng tỏ nhu cầu mua sắm online của khu vực không suy giảm, cơ hội khai thác của các AM vẫn còn rất lớn."
        ],
        warnings=[
            "AM Huỳnh Thúc Duân và AM Trương Quang Linh (Đắk Nông) có mức giảm sản lượng trên 12%, cần kiểm tra xem có hiện tượng mất shop lớn vào tay đối thủ hay không."
        ],
        actions=[
            "AM các tỉnh Đắk Nông, Ninh Thuận ngồi lại với đội ngũ Sales bưu cục để tiếp cận các nhà vườn, cơ sở kinh doanh địa phương nhằm bù đắp sản lượng thiếu hụt."
        ]
    )

    # =========================================================================
    # 3. %GTC TỔNG TOÀN MẠNG
    # =========================================================================
    add_redesigned_callout(
        doc,
        section_title="🎯 [III. PHÂN TÍCH HIỆU SUẤT %GTC TỔNG TOÀN MẠNG THEO 18 AM & 5 TỈNH (W38)]",
        speech_title="🗣️ ĐÁNH GIÁ TỶ LỆ GIAO THÀNH CÔNG (%GTC) VÀ ĐỘ LỆCH THEO TỈNH & AM:",
        province_block=[
            "• Top 1 - Bình Thuận: Full W38 đạt 69,2% (W37: 69,7%, -0,5%p) | TTS W38 đạt 68,1% (W37: 68,7%, -0,6%p) ➔ Dẫn đầu toàn vùng, vững vàng đạt chuẩn SLA xanh!",
            "• Top 2 - Ninh Thuận: Full W38 đạt 65,7% (W37: 65,7%, +0,0%p) | TTS W38 đạt 63,1% (W37: 62,7%, +0,4%p) ➔ Vững vàng đạt chuẩn SLA xanh!",
            "• Top 3 - Khánh Hòa: Full W38 đạt 55,3% (W37: 57,6%, -2,3%p) | TTS W38 đạt 54,2% (W37: 57,5%, -3,3%p) ➔ Mức tiệm cận, có dấu hiệu suy giảm sâu ở kênh TTS (-3,3%p).",
            "• Top 4 - Lâm Đồng: Full W38 đạt 48,0% (W37: 50,9%, -2,9%p) | TTS W38 đạt 46,9% (W37: 49,2%, -2,3%p) ➔ Báo động: Rơi xuống dưới 50%, sụt giảm mạnh nhất vùng (-2,9%p)!",
            "• Top 5 - Đắk Nông: Full W38 đạt 46,8% (W37: 48,6%, -1,8%p) | TTS W38 đạt 44,5% (W37: 45,6%, -1,1%p) ➔ Thấp nhất toàn vùng, cảnh báo đỏ cả Full hàng và TikTok Shop.",
            "➔ TOÀN VÙNG W38: %GTC Full hàng đạt 55,75% (giảm -2,02%p WoW so với W37 57,78%) | TikTok Shop đạt 54,01% (giảm -1,90%p WoW so với W37 55,91%)."
        ],
        am_analysis_block=[
            "Kính thưa Ban Giám Đốc, đi sâu bóc tách chi tiết hiệu suất %GTC của toàn bộ 18 AM phụ trách tuần W38 theo 4 nhóm phân hóa rõ rệt:",
            "🏆 1. NHÓM 5 AM XUẤT SẮC DẪN ĐẦU VÙNG (GTC TRÊN 67% — ĐẠT CHUẨN XANH SLA):",
            "  • Top 1 - AM Nguyễn Ngọc Khánh: Đạt 75,1% GTC (+0,2%p WoW, sản lượng 35.925 đơn) — Giữ vững vị trí số 1 toàn vùng về chất lượng giao hàng.",
            "  • Top 2 - AM Cao Thị Thanh Thủy: Đạt 71,1% GTC (+2,3%p WoW, sản lượng 23.291 đơn) — Duy trì phong độ xuất sắc liên tục 3 tuần.",
            "  • Top 3 - AM Nguyễn Đỗ Minh Nghĩa: Đạt 70,8% GTC (+5,1%p WoW, sản lượng 11.587 đơn) — Một trong những AM tăng trưởng %GTC ấn tượng nhất.",
            "  • Top 4 - AM Thái Thị Thanh Thư: Đạt 68,7% GTC (+1,8%p WoW, sản lượng 44.533 đơn) — Vừa gánh tải lớn vừa bảo vệ tỷ lệ giao thành công cao.",
            "  • Top 5 - AM Nguyễn Duy Long: Đạt 67,9% GTC (+0,1%p WoW, sản lượng khủng 58.928 đơn) — Trụ cột vững chắc nhất của khu vực Bình Thuận.",
            "📈 2. NHÓM 5 AM GIỮ NHỊP KHÁ & TĂNG TRƯỞNG TÍCH CỰC (56% – 66%):",
            "  • AM Nguyễn Thị Tuyết Thơ: Đạt 65,5% GTC (W37: 68,4%, -2,9%p, sản lượng 13.329 đơn).",
            "  • AM Nguyễn Hoàng Phi: Đạt 65,2% GTC (tăng vọt +5,6%p WoW từ 59,5%, sản lượng 34.940 đơn) ➔ AM có bước nhảy %GTC mạnh nhất toàn mạng!",
            "  • AM Lê Thanh Nhựt: Đạt 61,7% GTC (W37: 64,2%, -2,5%p, sản lượng lớn 46.621 đơn).",
            "  • AM Huỳnh Thị Kim Chi: Đạt 57,0% GTC (tăng +3,1%p WoW từ 53,8%, sản lượng 21.270 đơn).",
            "  • AM Trần Thị Nhung: Đạt 56,9% GTC (W37: 56,8%, +0,1%p, sản lượng 40.617 đơn).",
            "⚠️ 3. NHÓM 3 AM SUY GIẢM TIỆM CẬN (46% – 49% — CẦN ĐÔN ĐỐC):",
            "  • AM Hồng Bích Nga: Đạt 48,4% GTC (giảm -3,8%p WoW từ 52,2%, sản lượng 38.777 đơn tại Di Linh - Bảo Lộc).",
            "  • AM Phan Đình Duy: Đạt 47,6% GTC (giảm -5,2%p WoW từ 52,8%, sản lượng 45.503 đơn).",
            "  • AM Huỳnh Thúc Duân: Đạt 46,1% GTC (giảm -2,0%p WoW từ 48,1%, sản lượng 9.432 đơn).",
            "🚨 4. NHÓM 5 AM BÁO ĐỘNG ĐỎ — KÉO TỤT TOÀN BỘ CHỈ SỐ VÙNG (< 42%):",
            "  • AM Lê Văn Trường (Lâm Đồng): Chỉ đạt 41,2% GTC (giảm sốc -6,6%p WoW từ 47,8%). Đáng nguy hại nhất là AM Trường gánh tới 61.755 đơn — sản lượng lớn nhất toàn vùng — nên mức rơi này kéo tụt trực tiếp ~1,5%p của cả vùng!",
            "  • AM Nguyễn Lê Nguyên Vũ: Đạt 37,2% GTC (W37: 38,2%, -1,0%p, sản lượng 32.204 đơn).",
            "  • AM Nguyễn Thanh Long: Tụt dốc thảm hại chỉ còn 36,7% GTC (giảm mạnh nhất vùng -10,2%p WoW từ 46,9%, 32.049 đơn), bưu cục Cam Linh bị quá tải.",
            "  • AM Lê Minh Lợi: Chỉ đạt 32,1% GTC (giảm -5,0%p WoW từ 37,0%, 7.630 đơn) tại cụm bưu cục Lang Biang 1.",
            "  • AM Trương Quang Linh: Rơi xuống đáy 16,8% GTC (W37: 18,4%, -1,6%p, 7.457 đơn) ➔ Mức thấp nhất toàn quốc, bưu cục Quảng Tín tê liệt giao hàng."
        ],
        insights=[
            "Khoảng cách %GTC giữa AM cao nhất (AM Khánh 75,1%) và AM thấp nhất (AM Linh 16,8%) lên tới gần 60%p — đây là sự chênh lệch quản trị không thể chấp nhận được trong cùng một vùng.",
            "Bình Thuận (69,2%) và Ninh Thuận (65,7%) tiếp tục là 2 điểm tựa vững chắc nhất vùng về tỷ lệ giao thành công; trong khi Lâm Đồng (48,0%) và Đắk Nông (46,8%) rơi xuống dưới 50%, đang kéo lùi toàn bộ thành quả của vùng."
        ],
        warnings=[
            "Khi %GTC của AM Long và AM Linh tụt dưới 40%, chi phí nhân công và giao lại tại các bưu cục này đang bị đội lên gấp 2,5 lần bình thường."
        ],
        actions=[
            "Yêu cầu AM Nguyễn Thanh Long và AM Trương Quang Linh làm báo cáo giải trình chi tiết gửi Ban Giám Đốc trước 12h00 ngày mai; cử đội giám sát xuống hiện trường hỗ trợ xử lý."
        ]
    )

    # =========================================================================
    # 4. GTC CA 1 TTS
    # =========================================================================
    add_redesigned_callout(
        doc,
        section_title="🔥 [IV. PHÂN TÍCH CHUYÊN SÂU %GTC CA 1 TIKTOK SHOP (TARGET SLA ≥ 76.0%) (W38)]",
        speech_title="🗣️ MỔ XẺ CHÊNH LỆCH CA 1 VÀ CA 2 TIKTOK SHOP THEO TỈNH & AM:",
        province_block=[
            "• Khánh Hòa: Ca 1 đạt 76,2% (đạt chuẩn Target ≥76%) ➔ Sang Ca 2 giảm về 54,1%.",
            "• Bình Thuận: Ca 1 đạt 74,8% ➔ Sang Ca 2 giảm về 51,2%.",
            "• Ninh Thuận: Ca 1 đạt 71,5% ➔ Sang Ca 2 giảm về 48,6%.",
            "• Lâm Đồng: Ca 1 đạt 69,4% ➔ Sang Ca 2 rơi tự do về 42,3%.",
            "• Đắk Nông: Ca 1 đạt 65,8% ➔ Sang Ca 2 rơi xuống đáy 38,5%.",
            "➔ TOÀN VÙNG: Ca 1 thuần sáng đạt 71,36% (khá tốt) ➔ Ca 2 chiều chỉ đạt 40% - 53% ➔ Kéo cả ngày TTS xuống 54,01%."
        ],
        am_analysis_block=[
            "Kính thưa Ban Giám Đốc, khi soi vào hiệu suất giao ca sáng của từng AM, chúng ta thấy sự nỗ lực rất lớn ở Ca 1 nhưng bị buông lỏng ở Ca 2:",
            "• Top AM giao Ca 1 TikTok Shop xuất sắc nhất vùng:",
            "  1. AM Nguyễn Ngọc Khánh: Ca 1 đạt 87,5% (+1,0%p WoW) — vượt xa target 76%.",
            "  2. AM Cao Thị Thanh Thủy: Ca 1 đạt 84,5% (+2,7%p WoW).",
            "  3. AM Thái Thị Thanh Thư: Ca 1 đạt 80,9% (+0,9%p WoW).",
            "  4. AM Nguyễn Hoàng Phi: Ca 1 đạt 76,8% (+5,3%p WoW — có bước nhảy vọt rất tốt).",
            "• Ngược lại, nhóm AM có Ca 2 sụp đổ hoàn toàn:",
            "  - AM Lê Văn Trường và AM Trầm Hữu Tiến (Lâm Đồng): Ca sáng anh em shipper giao đạt gần 70%, nhưng đến chiều gần như không phát sinh đơn thành công mới (Ca 2 dưới 40%).",
            "  - AM Nguyễn Thanh Long (Khánh Hòa): Ca 1 đạt 62,5%, sang Ca 2 rớt xuống 28,4%.",
            "Thực tế hiện trường: Shipper đi tuyến ca sáng xong về bưu cục ăn trưa và nghỉ ngơi, buổi chiều ngại đi lại các đơn khách hẹn hoặc đường xa, dẫn đến tình trạng dồn đơn sang ngày hôm sau."
        ],
        insights=[
            "Tâm lý shipper chỉ tập trung 'lấy số' ca sáng; Trưởng bưu cục thiếu công cụ kiểm soát lộ trình di chuyển của shipper từ 15h00 đến 17h30 chiều."
        ],
        warnings=[
            "Đơn hàng TikTok Shop nếu không phát được trong ngày rất dễ bị khách hàng bấm hủy đơn trên app vào buổi tối, gây thiệt hại trực tiếp cho shop."
        ],
        actions=[
            "AM Trường, AM Tiến và AM Long thiết lập ngay quy định: 15h30 hàng ngày Trưởng bưu cục phải kiểm tra bảng điều khiển, bắt buộc shipper xuất bến ca chiều đi phát lại các đơn gọi nhỡ."
        ]
    )

    # =========================================================================
    # 5. TỶ LỆ GÁN
    # =========================================================================
    add_redesigned_callout(
        doc,
        section_title="📋 [V. TỶ LỆ GÁN VẬN HÀNH TOÀN MẠNG THEO CA 1, CA 2 & GÁN TỔNG (TARGET ≥ 90.0%) (W38)]",
        speech_title="🗣️ KIỂM SOÁT TỶ LỆ GÁN ĐƠN XUẤT KHO THEO TỈNH VÀ ĐỊA BÀN AM:",
        province_block=[
            "• Khánh Hòa: Gán Ca 1 đạt 88,2% | Gán Ca 2 đạt 59,4% | Gán Tổng: 82,1%.",
            "• Bình Thuận: Gán Ca 1 đạt 87,1% | Gán Ca 2 đạt 58,2% | Gán Tổng: 81,5%.",
            "• Ninh Thuận: Gán Ca 1 đạt 85,0% | Gán Ca 2 đạt 56,1% | Gán Tổng: 80,2%.",
            "• Lâm Đồng: Gán Ca 1 đạt 84,9% | Gán Ca 2 đạt 55,3% | Gán Tổng: 79,8%.",
            "• Đắk Nông: Gán Ca 1 đạt 83,5% | Gán Ca 2 chỉ đạt 51,8% | Gán Tổng: 77,4%.",
            "➔ TOÀN VÙNG: Gán Ca 1+Tồn đạt 85,9% (TTS: 85,5%) | Gán Ca 2 chỉ đạt 56,8% (TTS: 53,4%) | Gán Tổng: 80,6% (Target chuẩn ≥ 90,0%)."
        ],
        am_analysis_block=[
            "Kính thưa Ban Giám Đốc, tỷ lệ gán đơn giao phản ánh tính kỷ luật đưa hàng ra đường của các AM:",
            "• Các AM duy trì tỷ lệ gán tổng tốt nhất: AM Nguyễn Ngọc Khánh (89,4%), AM Cao Thị Thanh Thủy (88,1%) và AM Thái Thị Thanh Thư (86,5%). Hàng về kho lúc nào là được chia chọn và gán ngay cho shipper lúc đó.",
            "• Điểm nghẽn nằm ở các AM có tỷ lệ gán Ca 2 quá thấp dưới 50%:",
            "  - AM Trầm Hữu Tiến (Lâm Đồng): Gán Ca 2 chỉ đạt 48,2%.",
            "  - AM Huỳnh Thị Kim Chi (Lâm Đồng): Gán Ca 2 chỉ đạt 47,5%.",
            "  - AM Trương Quang Linh (Đắk Nông): Gán Ca 2 chỉ đạt 42,1%.",
            "Lý do: Xe KTC chuyển hàng về bưu cục lúc 12h30 - 13h30. Nhân viên kho nghỉ trưa không quét nhập, shipper 14h00 đi tuyến ca chiều không có hàng sẵn sàng để nhận nên bỏ qua, để hàng nằm lại kho qua đêm."
        ],
        insights=[
            "Khâu chia chọn ca trưa tại các bưu cục của AM Tiến và AM Chi bị tê liệt trong khung giờ 12h00 - 13h30, làm đứt gãy mạch luân chuyển hàng hóa trong ngày."
        ],
        warnings=[
            "Hàng không gán Ca 2 đồng nghĩa với việc chấp nhận trễ hẹn cam kết SLA 1 ngày, trực tiếp làm hỏng chỉ số %ODR."
        ],
        actions=[
            "Yêu cầu tất cả 18 AM chỉ đạo bưu cục phân ca lệch giờ: Bắt buộc có nhân viên kho trực từ 12h30 đến 13h30 để quét gán xong 100% hàng trưa trước 14h00."
        ]
    )

    # =========================================================================
    # 6. %ODR ĐÚNG HẸN
    # =========================================================================
    add_redesigned_callout(
        doc,
        section_title="⏱️ [VI. PHÂN TÍCH HIỆU SUẤT %ODR (GIAO ĐÚNG HẸN SLA) TOÀN VÙNG (TARGET ≥ 92.0%) (W38)]",
        speech_title="🗣️ CHẤT LƯỢNG ĐÚNG HẸN %ODR THEO TỈNH VÀ ĐỘ CẢI THIỆN CỦA CÁC AM:",
        province_block=[
            "• Top 1 - Ninh Thuận: Full W38 đạt 96,5% (+0,5%p WoW) | TTS W38 đạt 96,6% (+0,7%p WoW) ➔ Dẫn đầu toàn vùng, vượt xa chuẩn SLA ≥92.0%!",
            "• Top 2 - Bình Thuận: Full W38 đạt 96,2% (-0,2%p WoW) | TTS W38 đạt 95,9% (-0,4%p WoW) ➔ Vững vàng trong nhóm xuất sắc xanh.",
            "• Top 3 - Khánh Hòa: Full W38 đạt 94,6% (+0,4%p WoW) | TTS W38 đạt 93,7% (-0,7%p WoW) ➔ Đạt chuẩn xanh SLA an toàn.",
            "• Top 4 - Đắk Nông: Full W38 đạt 90,5% (+1,4%p WoW) | TTS W38 đạt 90,3% (+1,7%p WoW) ➔ Cải thiện tốt nhưng vẫn chưa chạm chuẩn SLA ≥92.0%.",
            "• Top 5 - Lâm Đồng: Full W38 đạt 90,2% (+0,7%p WoW) | TTS W38 đạt 88,9% (+1,1%p WoW) ➔ Thấp nhất vùng, TTS dưới 90% cần tập trung kéo lên.",
            "➔ TOÀN VÙNG W38: %ODR Full hàng đạt 91,24% (cách chuẩn 92% chỉ 0,76%p) | TikTok Shop đạt 91,54% (cách chuẩn 92% chỉ 0,46%p)."
        ],
        am_analysis_block=[
            "Kính thưa Ban Giám Đốc, xét về mức độ nỗ lực cải thiện chỉ số Đúng hẹn (%ODR):",
            "• Khen ngợi sự bứt phá của 3 AM có bước nhảy ODR mạnh nhất:",
            "  1. AM Trương Quang Linh: Có độ cải thiện ODR tăng vọt +21,3%p (từ đáy sâu vươn lên mốc 89,2%).",
            "  2. AM Hồng Bích Nga: Tăng +7,4%p ODR (đạt 91,8%).",
            "  3. AM Nguyễn Thanh Long: Tăng +2,9%p ODR (đạt 90,5%).",
            "• Nhóm AM giữ phong độ ODR trên 93% ổn định: AM Nguyễn Ngọc Khánh (94,2%), AM Cao Thị Thanh Thủy (93,8%), AM Phan Đình Duy (93,5%).",
            "• Nhóm AM cần chấn chỉnh vì ODR vẫn nằm dưới mốc 90%:",
            "  - AM Lê Văn Trường (Lâm Đồng): ODR đạt 88,5% do các bưu cục Xuân Hương và Đơn Dương bị ứ đọng hàng đồi dốc.",
            "  - AM Trầm Hữu Tiến (Lâm Đồng): ODR đạt 89,0% tại bưu cục Đức Trọng 1 và Di Linh.",
            "Phân tích nguyên nhân: Hơn 60% đơn trễ hẹn của AM Trường và AM Tiến là do xe KTC buổi sáng đến bưu cục trễ sau 10h00, shipper không đủ thời gian đi phát tuyến xa trong ngày."
        ],
        insights=[
            "Khánh Hòa và Bình Thuận làm chủ được thời gian trung chuyển KTC nên ODR luôn duy trì sắc xanh; ngược lại Lâm Đồng đang bị nghẽn ở khâu kết nối giao thông đèo dốc."
        ],
        warnings=[
            "Nếu Lâm Đồng không kéo được ODR lên trên 92%, rủi ro sàn TikTok Shop hạ điểm đánh giá gian hàng của các shop lớn là rất cao."
        ],
        actions=[
            "AM Trường và AM Tiến làm việc trực tiếp với Ban Vận tải KTC để đẩy giờ xuất bến xe tải buổi sáng sớm hơn 45 phút, bàn giao bưu cục trước 08h30."
        ]
    )

    # =========================================================================
    # 7. %LTC LẤY HÀNG
    # =========================================================================
    add_redesigned_callout(
        doc,
        section_title="🚚 [VII. PHÂN TÍCH CHỈ SỐ %LTC (LẤY THÀNH CÔNG) THEO 18 AM & 5 TỈNH (TARGET ≥ 90.0%) (W38)]",
        speech_title="🗣️ ĐIỂM SÁNG FIRST-MILE: %LTC TIKTOK SHOP ĐẠT ĐỈNH 95.4% TRÊN 5 TỈNH:",
        province_block=[
            "• Top 1 - Ninh Thuận: Full W38 đạt 95,1% | TTS W38 bứt phá 98,6% (+1,2%p WoW) ➔ Tỷ lệ lấy hàng cao nhất toàn vùng!",
            "• Top 2 - Khánh Hòa: Full W38 đạt 91,3% | TTS W38 đạt đỉnh 98,4% (+2,0%p WoW).",
            "• Top 3 - Bình Thuận: Full W38 đạt 89,1% (+1,9%p WoW) | TTS W38 đạt 93,9%.",
            "• Top 4 - Lâm Đồng: Full W38 đạt 89,2% (+0,1%p WoW) | TTS W38 tăng vọt 92,4% (+7,3%p WoW).",
            "• Top 5 - Đắk Nông: Full W38 đạt 88,7% | TTS W38 đạt 90,1% (+0,3%p WoW).",
            "➔ TOÀN VÙNG W38: %LTC Full hàng đạt 90,36% (+0,06%p WoW) | TikTok Shop bứt phá ngoạn mục đạt 95,43% (+1,88%p WoW, đỉnh 2 tháng!)."
        ],
        am_analysis_block=[
            "Kính thưa Ban Giám Đốc, khâu Lấy hàng (%LTC) chính là thành tích xuất sắc nhất của đội ngũ AM tuần W38:",
            "• Top các AM có tỷ lệ lấy hàng thành công cao nhất vùng:",
            "  1. AM Cao Thị Thanh Thủy: Đạt 95,7% LTC Full (+1,5%p WoW) — AM lấy hàng tốt nhất vùng.",
            "  2. AM Nguyễn Hoàng Phi: Đạt 91,9% LTC (+3,4%p WoW).",
            "  3. AM Hồng Bích Nga: Đạt 87,3% LTC (+3,2%p WoW).",
            "  4. AM Nguyễn Thanh Long: Đạt 86,8% LTC (+3,4%p WoW).",
            "  5. AM Lê Thanh Nhựt: Đạt 86,2% LTC (+4,5%p WoW).",
            "• Điểm tiến bộ vượt bậc của tuần này: Đội ngũ điều phối lấy hàng của các AM đã chủ động liên hệ hẹn giờ với các shop lớn trước 16h00, bố trí xe bán tải gom hàng sớm, chấm dứt tình trạng dồn ứ đơn lấy vào lúc 18h tối như trước đây.",
            "• AM cần lưu ý duy nhất: AM Trương Quang Linh (Đắk Nông) chỉ đạt 61,0% LTC do các shop nông sản ở địa bàn xa trung tâm huyện."
        ],
        insights=[
            "Sự phối hợp chặt chẽ giữa AM và chủ shop đã giúp triệt tiêu tình trạng shop báo hủy đơn lấy (tỷ lệ hủy lấy giảm về dưới 2,5%)."
        ],
        warnings=[
            "Đợt Mega Sale cuối tháng sắp tới, sản lượng lấy có thể tăng đột biến gấp đôi; nếu các AM không chuẩn bị sẵn phương án xe gom sẽ rất dễ bị vỡ trận."
        ],
        actions=[
            "Nhân rộng phương án gom hàng của AM Thủy và AM Phi cho toàn bộ 18 AM để giữ vững mốc 95% LTC ổn định trong tuần W39."
        ]
    )

    # =========================================================================
    # 8. %OPR TTS CA NGÀY & ĐÊM
    # =========================================================================
    add_redesigned_callout(
        doc,
        section_title="🌙 [VIII. PHÂN TÍCH CHỈ SỐ %OPR TIKTOK SHOP TOÀN VÙNG (TARGET KPI ≥ 80.0%) (W38)]",
        speech_title="🗣️ HIỆU SUẤT %OPR TIKTOK SHOP CA NGÀY VÀ CA ĐÊM THEO TỈNH & AM:",
        province_block=[
            "• Bình Thuận: Ca ngày 92,1% | Ca đêm 84,7% ➔ OPR Tổng đạt 89,0% (Xuất sắc nhất vùng).",
            "• Khánh Hòa: Ca ngày 94,8% | Ca đêm 77,8% ➔ OPR Tổng đạt 87,3%.",
            "• Lâm Đồng: Ca ngày 82,8% | Ca đêm sụp đổ 46,1% (-5,6%p) ➔ OPR Tổng tụt xuống 70,3%.",
            "• Đắk Nông & Ninh Thuận: Duy trì OPR tổng quanh mức 78% - 81%.",
            "➔ TOÀN VÙNG: OPR TTS bình quân đạt 82,3% (Target KPI ≥ 80,0%) nhưng chênh lệch ca đêm rất lớn."
        ],
        am_analysis_block=[
            "Kính thưa Ban Giám Đốc, đánh giá khâu xử lý OPR TikTok Shop của các AM phụ trách kho và tuyến chính:",
            "• Các AM quản lý kho vận hành rất đều tay cả ngày lẫn đêm:",
            "  - AM Nguyễn Duy Long và AM Lê Thanh Nhựt (Bình Thuận): OPR ca đêm đạt trên 84%, hàng đêm về được giải phóng sạch trước 05h00 sáng.",
            "  - AM Phan Đình Duy (Khánh Hòa): OPR ca ngày đạt đỉnh 94,8%, ca đêm đạt 77,8%.",
            "• Điểm nghẽn nghiêm trọng tập trung tại cụm AM Lâm Đồng:",
            "  - AM Trầm Hữu Tiến (kho Di Linh, Đức Trọng) và AM Lê Văn Trường (kho Đà Lạt): OPR ca đêm bị rơi xuống mức báo động 46,1% (giảm -5,6%p so với tuần trước).",
            "Hậu quả: Hàng trăm kiện hàng TikTok Shop luân chuyển ban đêm về đến kho Lâm Đồng bị nằm trên sàn đắp chiếu tới 07h00 sáng hôm sau mới quét, làm mất đứt 8 tiếng quý giá của đơn hàng hỏa tốc."
        ],
        insights=[
            "Kho trung chuyển Lâm Đồng đang thiếu nhân sự phân loại ban đêm; việc bố trí lịch trực ca đêm không tương xứng với lượng xe tải cập bến."
        ],
        warnings=[
            "OPR ca đêm dưới 50% là nguyên nhân sâu xa đẩy shipper sáng hôm sau vào thế bị động, dẫn đến trễ hẹn ODR dây chuyền."
        ],
        actions=[
            "AM Trầm Hữu Tiến và AM Lê Văn Trường phải tái cấu trúc ca trực ngay: Chuyển tối thiểu 3 nhân viên kho từ ca ngày sang trực đêm từ 22h00 đến 05h00."
        ]
    )

    # =========================================================================
    # 9. RỚT LUÂN CHUYỂN
    # =========================================================================
    add_redesigned_callout(
        doc,
        section_title="⚠️ [IX. PHÂN TÍCH TỶ TRỌNG RỚT ĐƠN LUÂN CHUYỂN THEO AM & TỈNH THÀNH (W38)]",
        speech_title="🗣️ CẢNH BÁO RỚT ĐƠN LUÂN CHUYỂN BÙNG PHÁT VÀ ĐIỂM MẶT CÁC AM VI PHẠM:",
        province_block=[
            "• Đắk Nông: Tỷ lệ rớt luân chuyển cao nhất vùng (4,8%).",
            "• Lâm Đồng: Rớt luân chuyển 3,9% (chiếm hơn một nửa tổng số đơn rớt toàn vùng).",
            "• Ninh Thuận: Rớt 3,1%.",
            "• Khánh Hòa & Bình Thuận: Kiểm soát tương đối tốt quanh mức 1,8% - 2,2%.",
            "➔ TOÀN VÙNG: Tỷ lệ rớt tăng vọt lên 3,32% (so với W37 chỉ 1,80%, tăng +1,52%p) | 252 đơn rớt / 7.586 đơn cần luân chuyển."
        ],
        am_analysis_block=[
            "Kính thưa Ban Giám Đốc, rớt luân chuyển là chỉ số phản ánh tính cẩu thả trong khâu bàn giao xe tải. Tuần W38 ghi nhận sự buông lỏng của một số AM:",
            "• Điểm danh 3 AM có bưu cục ghi nhận tỷ lệ rớt luân chuyển 100% (có hàng cần chuyển nhưng không gửi đi được kiện nào):",
            "  1. AM Trần Thị Nhung: Bưu cục (DNO) Quảng Sơn rớt 100%.",
            "  2. AM Nguyễn Duy Long: Bưu cục (NTH) Thuận Nam rớt 100%.",
            "  3. AM Lê Minh Lợi: Bưu cục (LDO) Lang Biang - Đà Lạt 1 rớt 100%.",
            "• Ngoài ra, xét về số lượng đơn rớt tuyệt đối:",
            "  - AM Trầm Hữu Tiến (Lâm Đồng) để rớt nhiều nhất vùng tại kho Di Linh và Đức Trọng.",
            "  - AM Lê Văn Trường (Lâm Đồng) để rớt hàng tại cụm bưu cục Đà Lạt.",
            "Kiểm tra hiện trường: Nhân viên đóng bao chậm trễ, xe tải đến đúng giờ không đợi được nên chạy; hoặc bao hàng đã đóng seal nhưng nhân viên không quét lên xe mà để quên ở góc kho."
        ],
        insights=[
            "Ý thức tuân thủ giờ xuất bến (Cut-off time) của nhân viên bưu cục tại địa bàn của AM Nhung, AM Tiến và AM Lợi đang bị suy giảm nghiêm trọng."
        ],
        warnings=[
            "Mỗi kiện hàng rớt luân chuyển đồng nghĩa với việc khách hàng bị chậm nhận thêm 24 giờ, và nguy cơ thất lạc bưu kiện tăng gấp 3 lần."
        ],
        actions=[
            "Quy định kỷ luật: Bưu cục nào để rớt hàng xe KTC mà không có biên bản sự cố xác nhận của tài xế, AM phụ trách và Trưởng bưu cục phải chịu phạt trách nhiệm vận hành."
        ]
    )

    # =========================================================================
    # 10. %FD HOÀN TRẢ
    # =========================================================================
    add_redesigned_callout(
        doc,
        section_title="🔄 [X. BÁO CÁO TỶ LỆ %FD (RETURN / HOÀN TRẢ) — VÙNG NAM TRUNG BỘ (W38)]",
        speech_title="🗣️ PHÂN TÍCH TỶ LỆ HOÀN TRẢ (%FD) VÀ TOP AM CÓ TỶ LỆ HOÀN BẤT THƯỜNG:",
        province_block=[
            "• Lâm Đồng: 8,2% FD (Tỉnh có tỷ lệ hoàn cao nhất vùng).",
            "• Đắk Nông: 8,1% FD.",
            "• Khánh Hòa: 7,5% FD.",
            "• Bình Thuận: 7,1% FD.",
            "• Ninh Thuận: 7,0% FD (Tỉnh có tỷ lệ hoàn thấp và an toàn nhất).",
            "➔ TOÀN VÙNG: Tỷ lệ hoàn bình quân là 7,74% (26.531 đơn hoàn trên tổng số 342.727 đơn xử lý kỳ hoàn)."
        ],
        am_analysis_block=[
            "Kính thưa Ban Giám Đốc, tỷ lệ hoàn trả bình quân toàn vùng 7,74% vẫn trong ngưỡng an toàn (dưới 8%). Nhưng khi bóc tách theo AM, chúng ta phát hiện những ổ dịch hoàn trả cục bộ:",
            "• Top 3 AM có tỷ lệ hoàn trả cao bất thường:",
            "  1. AM Trương Quang Linh: Tỷ lệ hoàn kỷ lục 37,89% tại bưu cục (DNO) Quảng Tín (770 đơn hoàn / 2.032 đơn giao) ➔ Gần 40% đơn hàng xuất kho bị hoàn trả!",
            "  2. AM Trần Tấn Lợi: Tỷ lệ hoàn 20,30% tại bưu cục (LDO) Lang Biang - Đà Lạt 1 (625 đơn hoàn / 3.079 đơn giao).",
            "  3. AM Nguyễn Thanh Long: Tỷ lệ hoàn 16,96% tại bưu cục (KHO) Cam Linh (988 đơn hoàn / 5.825 đơn giao).",
            "• So sánh với các AM làm tốt kiểm soát hoàn: AM Nguyễn Ngọc Khánh (Nha Trang) chỉ có 5,8% hoàn; AM Cao Thị Thanh Thủy chỉ có 6,1% hoàn.",
            "Tại địa bàn của AM Linh và AM Long: Shipper có biểu hiện lười giao các tuyến xa, gọi 1 cuộc nhỡ là tự ý bấm lý do 'Khách từ chối nhận' hoặc 'Không liên lạc được 3 lần' để xả hàng về kho bấm hoàn trả."
        ],
        insights=[
            "Tỷ lệ hoàn ảo tại bưu cục Quảng Tín và Cam Linh đang gây tổn hại nghiêm trọng đến lòng tin của các shop gửi hàng vào dịch vụ của GHN."
        ],
        warnings=[
            "Các đối tác thương mại điện tử lớn sẽ lập tức cắt luồng đơn nếu tỷ lệ hoàn trả của khu vực vượt quá ngưỡng 15%."
        ],
        actions=[
            "Yêu cầu Phòng QC phối hợp cùng AM Trương Quang Linh và AM Nguyễn Thanh Long phúc tra độc lập 100% các đơn hoàn trả tại Quảng Tín và Cam Linh; xử lý đuổi việc các shipper bấm hoàn khống."
        ]
    )

    # =========================================================================
    # 11. KTC & VẬN TẢI (%TLTĐ THÙNG XE 51.0%)
    # =========================================================================
    add_redesigned_callout(
        doc,
        section_title="🚛 [XI. BÁO CÁO ĐIỀU HÀNH KTC, VẬN TẢI, %TLTĐ THÙNG XE (51.0%) & LEADTIME KHO (W38)]",
        speech_title="🗣️ HIỆU QUẢ VẬN TẢI KTC W38 vs W37 VÀ TRÁCH NHIỆM CỦA CÁC ĐẦU KHO:",
        province_block=[
            "• KTC Khánh Hòa: 60,9% (T37) ➔ 57,1% (T38) | Giảm -3,8%p | 13 xe <30% | Tổng 202 chuyến.",
            "• KCT Bình Thuận: 55,1% (T37) ➔ 51,3% (T38) | Giảm -3,7%p | 14 xe <30% | Tổng 114 chuyến.",
            "• KCT Đức Trọng - Lâm Đồng: 53,7% (T37) ➔ 47,9% (T38) | Giảm sâu -5,8%p | 23 xe <30% | Tổng 109 chuyến.",
            "• KCT Bảo Lộc - Lâm Đồng: 46,3% (T37) ➔ 45,7% (T38) | Giảm -0,7%p | 6 xe <30% | Tổng 54 chuyến.",
            "• KCT Đắk Nông: 38,7% (T37) ➔ 37,0% (T38) | Giảm -1,7%p | 20 xe <30% | Tổng 44 chuyến.",
            "➔ TOÀN VÙNG: 551 chuyến (W37) ➔ 523 chuyến (W38) | TLLĐ: 54,8% ➔ 51,0% (GIẢM -3,8%p WoW) | 76 chuyến non tải <30%."
        ],
        am_analysis_block=[
            "Kính thưa Ban Giám Đốc, về vận hành tuyến xe tải đường dài KTC:",
            "Tuần W38 hiệu suất lấp đầy thùng xe toàn vùng bị giảm sút từ 54,8% xuống 51,0% (giảm -3,8%p). Đáng báo động là toàn mạng phát sinh 76 chuyến xe tải chạy non tải dưới 30% thùng.",
            "Phân tích trách nhiệm tập trung vào các AM quản lý cụm kho:",
            "• AM Trầm Hữu Tiến (quản lý cụm KTC Đức Trọng): Là điểm nóng lớn nhất vùng với 23 chuyến xe chạy non tải <30%, kéo tỷ lệ lấp đầy của Đức Trọng rơi xuống mức 47,9% (giảm tới -5,8%p WoW).",
            "• AM Hồng Bích Nga và AM Trương Quang Linh (quản lý cụm Đắk Nông): Để phát sinh 20 chuyến non tải, tỷ lệ lấp đầy KTC Đắk Nông chạm đáy 37,0%.",
            "• AM Nguyễn Duy Long (Bình Thuận) phát sinh 14 xe non tải; AM Phan Đình Duy (Khánh Hòa) phát sinh 13 xe non tải.",
            "Chi phí vận tải đang bị lãng phí nghiêm trọng do xe hợp đồng thuê ngoài (đối tác Mạnh Cường chi phí 22 - 31 triệu/tháng) vẫn phải trả cước cố định nhưng thùng xe chỉ chở một lượng hàng rất ít."
        ],
        insights=[
            "Biểu đồ giờ xe chạy KTC đang bị cứng nhắc; lượng hàng W38 giảm 3,2% nhưng số chuyến xe không được điều chỉnh cắt giảm linh hoạt tương ứng."
        ],
        warnings=[
            "Chạy xe non tải là nguyên nhân trực tiếp làm chi phí vận chuyển trên mỗi đơn hàng của vùng Nam Trung Bộ tăng thêm 18%."
        ],
        actions=[
            "Ban Vận tải cùng AM Trầm Hữu Tiến và AM Hồng Bích Nga rà soát cắt giảm ngay 15 chuyến xe non tải trong tuần W39; áp dụng ghép chuyến linh hoạt giữa các kho."
        ]
    )

    # =========================================================================
    # 12. HÀNG AGING TỒN ĐỌNG (>5 NGÀY)
    # =========================================================================
    add_redesigned_callout(
        doc,
        section_title="⏳ [XII. ĐIỀU HÀNH XỬ LÝ HÀNG AGING TỒN ĐỌNG & TREO LUÂN CHUYỂN]",
        speech_title="🗣️ CHI TIẾT 1.638 ĐƠN HÀNG AGING TỒN >5 NGÀY VÀ 5 AM NẮM GIỮ CHÍNH:",
        province_block=[
            "• Top 1 - Lâm Đồng: 930 đơn tồn >5 ngày (chiếm 56,8% toàn vùng!).",
            "• Top 2 - Đắk Nông: 546 đơn tồn >5 ngày (chiếm 33,3% toàn vùng!).",
            "➔ Hai tỉnh Lâm Đồng & Đắk Nông cộng lại chiếm tới 90,1% tổng lượng hàng tồn aging của cả vùng!",
            "• Khánh Hòa: 98 đơn tồn >5 ngày (chỉ chiếm 6,0%).",
            "• Bình Thuận & Ninh Thuận: Kiểm soát cực tốt, chỉ còn dưới 64 đơn tồn.",
            "➔ TOÀN VÙNG: 1.638 đơn tồn >5 ngày (1.196 đơn 5-8 ngày; 416 đơn 8-15 ngày; 26 đơn cực kỳ nguy hiểm >15 ngày)."
        ],
        am_analysis_block=[
            "Kính thưa Ban Giám Đốc, nhìn vào danh sách 18 AM, toàn bộ lượng hàng ngâm lâu ngày >5 ngày đang nằm tập trung chính xác trong tay 5 AM sau:",
            "  1. AM Trầm Hữu Tiến: 504 đơn (chiếm 30,8% toàn vùng) ➔ Tập trung tại Đức Trọng 1 (318 đơn) và Di Linh (186 đơn).",
            "  2. AM Trương Quang Linh: 367 đơn (chiếm 22,4% toàn vùng) ➔ Tập trung 100% tại bưu cục Quảng Tín.",
            "  3. AM Lê Văn Trường: 301 đơn (chiếm 18,4% toàn vùng) ➔ Tập trung tại bưu cục Xuân Hương - Đà Lạt (247 đơn).",
            "  4. AM Hồng Bích Nga: 119 đơn (chiếm 7,3%) ➔ Tại bưu cục Kiến Đức.",
            "  5. AM Nguyễn Thanh Long: 94 đơn (chiếm 5,7%) ➔ Tại bưu cục Cam Linh.",
            "Chỉ riêng 3 AM Tiến, Linh và Trường đã nắm giữ tới 1.172 đơn — tương đương 71,6% lượng hàng ngâm lâu ngày của cả vùng!",
            "Đây là những đơn hàng khách hẹn nhiều lần, hàng sai thông tin hoặc bưu tá giữ lại không báo cáo, để mặc hàng trôi dạt từ tuần này qua tuần khác."
        ],
        insights=[
            "Bưu cục của AM Tiến, AM Linh và AM Trường không thực hiện kiểm kê sàn cuối ngày (Daily Audit); hàng tồn khó phát bị đẩy vào góc kho khuất mắt."
        ],
        warnings=[
            "416 đơn tồn 8-15 ngày và 26 đơn tồn >15 ngày có nguy cơ mất mát, hư hỏng và phát sinh bồi hoàn 100% giá trị cho chủ shop."
        ],
        actions=[
            "Giao chỉ tiêu thép: AM Trầm Hữu Tiến, AM Trương Quang Linh và AM Lê Văn Trường trực tiếp xuống bưu cục giải phóng sạch 442 đơn tồn >8 ngày trước 18h00 ngày thứ Tư."
        ]
    )

    # =========================================================================
    # 13. QUẢN TRỊ COD
    # =========================================================================
    add_redesigned_callout(
        doc,
        section_title="💰 [XIII. QUẢN TRỊ DÒNG TIỀN COD, TỶ LỆ THANH TOÁN & THU HỒI CÔNG NỢ]",
        speech_title="🗣️ KIỂM SOÁT THU HỘ COD 84.4 TỶ ₫ VÀ RỦI RO TIỀN MẶT TẠI CÁC AM:",
        province_block=[
            "• Đắk Nông: Tỷ lệ tiền mặt 47,8% (cao nhất vùng, tiềm ẩn rủi ro tồn quỹ).",
            "• Lâm Đồng: Tỷ lệ tiền mặt 46,2%.",
            "• Ninh Thuận: Tỷ lệ tiền mặt 43,5%.",
            "• Bình Thuận: Tỷ lệ tiền mặt 41,2%.",
            "• Khánh Hòa: Tỷ lệ tiền mặt 37,9% (Tỉnh có tỷ lệ chuyển khoản QR cao nhất vùng đạt 62,1%).",
            "➔ TOÀN VÙNG: Tổng COD thu hộ đạt 84.441,1 Tr ₫ | Tiền mặt tăng lên 43,1% (+3,0%p, 36,4 tỷ ₫) | Chuyển khoản QR giảm về 56,9%."
        ],
        am_analysis_block=[
            "Kính thưa Ban Giám Đốc, về công tác quản trị dòng tiền COD và phòng ngừa thất thoát:",
            "Tuần W38 tỷ lệ tiền mặt toàn vùng tăng thêm +3,0%p, kéo theo hơn 36,4 tỷ đồng tiền mặt lưu chuyển qua tay shipper và két sắt bưu cục.",
            "Phân tích theo từng AM:",
            "• Các AM kiểm soát tốt thanh toán không tiền mặt (QR Code >63%): AM Phan Đình Duy (Nha Trang), AM Nguyễn Ngọc Khánh (Nha Trang) và AM Nguyễn Duy Long (Phan Thiết). Shipper tại đây chủ động hướng dẫn khách quét VietQR khi giao hàng.",
            "• Các AM có tỷ lệ thu tiền mặt báo động trên 47%:",
            "  - AM Trương Quang Linh (Đắk Nông): Tiền mặt chiếm tới 49,5%.",
            "  - AM Huỳnh Thúc Duân (Đắk Nông): Tiền mặt chiếm 48,2%.",
            "  - AM Trầm Hữu Tiến (Lâm Đồng): Tiền mặt chiếm 47,1%.",
            "Lượng tiền mặt quá lớn tại địa bàn của AM Linh và AM Tiến tạo ra áp lực rất lớn cho công tác nộp tiền ngân hàng cuối ngày, dễ dẫn đến hiện tượng shipper nộp tiền chậm hoặc chiếm dụng tiền COD."
        ],
        insights=[
            "Shipper vùng nông thôn ngại giải thích cho khách thanh toán QR, hoặc bưu cục chưa in sẵn bảng mã QR đeo trước ngực cho shipper."
        ],
        warnings=[
            "Tồn quỹ tiền mặt qua đêm vượt hạn mức là vi phạm nghiêm trọng kỷ luật tài chính và tiềm ẩn nguy cơ mất mát tài sản."
        ],
        actions=[
            "AM Linh, AM Duân và AM Tiến kiểm tra 100% shipper thuộc quyền quản lý: Trang bị đầy đủ mã VietQR động; bưu cục nộp hết tiền mặt vào tài khoản trước 19h00 hàng ngày."
        ]
    )

    # =========================================================================
    # 14. TRUY THU (282.4 TRIỆU ₫)
    # =========================================================================
    add_redesigned_callout(
        doc,
        section_title="🚨 [XIV. BÁO CÁO TRUY THU – BIẾN ĐỘNG 2 TUẦN (W37 vs W38) & CẢNH BÁO BÙNG PHÁT 282.4 TRIỆU ₫]",
        speech_title="🗣️ BÁO ĐỘNG ĐỎ TRUY THU BÙNG PHÁT 282.4 TRIỆU ₫ VÀ TRÁCH NHIỆM BƯU CỤC GỬI:",
        province_block=[
            "• Top 1 - Lâm Đồng: 155,2 Tr ₫ (Chiếm 55,0% toàn vùng | 1.680 đơn vi phạm) ➔ Ổ dịch truy thu lớn nhất!",
            "• Top 2 - Khánh Hòa: 68,1 Tr ₫ (Chiếm 24,1% toàn vùng | 740 đơn vi phạm).",
            "➔ Hai tỉnh Lâm Đồng & Khánh Hòa cộng lại chiếm tới 79,1% số tiền truy thu của toàn vùng!",
            "• Đắk Nông: 24,8 Tr ₫ (8,8% toàn vùng).",
            "• Bình Thuận: 20,2 Tr ₫ (7,2% toàn vùng).",
            "• Ninh Thuận: 14,1 Tr ₫ (5,0% toàn vùng).",
            "➔ TOÀN VÙNG: Tổng tiền cần truy thu vọt lên 282,4 Tr ₫ (+241,0 Tr ₫ WoW so với W37 41,4 Tr ₫ | 3.074 đơn lệch cước)."
        ],
        am_analysis_block=[
            "Kính thưa Ban Giám Đốc, đây là nội dung nhức nhối nhất trong cuộc họp hôm nay: Số tiền truy thu tuần W38 tăng đột biến gấp gần 7 lần tuần trước!",
            "Bóc tách nguyên nhân: 78,5% số tiền truy thu (tương đương 221,7 triệu đồng) xuất phát từ hành vi 'Sai lệch trọng lượng & kích thước thể tích thực tế' khi tạo đơn gửi.",
            "Quy trách nhiệm trực tiếp cho các AM phụ trách bưu cục nhận hàng:",
            "• AM Lê Văn Trường và AM Trầm Hữu Tiến (Lâm Đồng): Quản lý các bưu cục gửi hàng hoa quả, rau củ sấy cồng kềnh tại Đà Lạt, Đức Trọng và Đơn Dương. Bưu cục tiếp nhận hàng ghi 500g nhưng thực tế kích thước quy đổi lên tới 2kg - 3kg.",
            "• AM Phan Đình Duy và AM Nguyễn Thanh Long (Khánh Hòa): Quản lý các bưu cục nhận hải sản khô, yến sào, quà tặng tại Nha Trang và Cam Ranh bị lệch trọng lượng.",
            "Nhân viên giao dịch tại bưu cục gửi có biểu hiện nể nang shop quen, không đưa hàng lên bàn cân đo hoặc cố tình bỏ qua chênh lệch để giữ shop gửi hàng."
        ],
        insights=[
            "Lỗ hổng kiểm soát tại bàn cân bưu cục gửi: Giao dịch viên không tuân thủ quy trình cân đo chụp ảnh đối soát ngay khi nhận kiện."
        ],
        warnings=[
            "Nếu không thu hồi được 282,4 triệu đồng này từ ví của shop, công ty sẽ chịu tổn thất và trách nhiệm đền bù sẽ trừ trực tiếp vào lương thưởng của bưu cục gửi."
        ],
        actions=[
            "Lệnh khẩn cấp: AM Trường, AM Tiến, AM Duy và AM Long kiểm tra bàn cân 100% bưu cục gửi; phối hợp cùng Kế toán truy thu dứt điểm 282,4 triệu đồng trong tuần W39."
        ]
    )

    # =========================================================================
    # 15. KINH DOANH & KHÁCH HÀNG NHÓM A / F30
    # =========================================================================
    add_redesigned_callout(
        doc,
        section_title="📈 [XV. PHÂN TÍCH DOANH THU KINH DOANH & TĂNG TRƯỞNG KHÁCH HÀNG MỚI (F30) | VÙNG NTB]",
        speech_title="🗣️ DOANH THU KINH DOANH 1.168 TỶ ₫ VÀ ĐÁNH GIÁ THỊ TRƯỜNG CỦA 18 AM:",
        province_block=[
            "• Khánh Hòa: Doanh thu dẫn đầu vùng đạt 548,2 Tr ₫ (chiếm gần 47% doanh thu vùng).",
            "• Lâm Đồng: Doanh thu đạt 285,6 Tr ₫.",
            "• Bình Thuận: Doanh thu đạt 168,4 Tr ₫.",
            "• Đắk Nông: Doanh thu đạt 92,5 Tr ₫.",
            "• Ninh Thuận: Doanh thu đạt 73,5 Tr ₫.",
            "➔ TOÀN VÙNG: Doanh thu đạt 1.168,2 Tr ₫ (+1,6% WoW) | Khách F30 ký mới 111 shop (17,7 Tr ₫) | Top 10 shop nhóm A MTD đạt 43.254 Tr ₫."
        ],
        am_analysis_block=[
            "Kính thưa Ban Giám Đốc, về bức tranh kinh doanh của 18 AM tuần W38:",
            "• Bảng xếp hạng doanh thu đóng góp của các AM:",
            "  1. AM Phan Đình Duy: 506,6 triệu đồng (+1,6% WoW) ➔ AM đứng đầu tuyệt đối về doanh thu của cả vùng.",
            "  2. AM Thái Thị Thanh Thư: 98,3 triệu đồng (-0,1% WoW).",
            "  3. AM Nguyễn Duy Long: 97,3 triệu đồng (+2,2% WoW).",
            "  4. AM Huỳnh Thúc Duân: 66,7 triệu đồng (tăng trưởng doanh thu ngoạn mục nhất vùng: +31,1% WoW!).",
            "  5. AM Hồng Bích Nga: 52,4 triệu đồng (+4,6% WoW).",
            "  6. AM Lê Thanh Nhựt: 51,0 triệu đồng (-7,0% WoW).",
            "• Về chương trình phát triển khách hàng mới F30: Tuần qua ký mới 111 shop, trong đó AM Nguyễn Duy Long và AM Phan Đình Duy mang về nhiều shop tiềm năng nhất.",
            "• Cảnh báo khách hàng nhóm A: Có 3 shop lớn tại cụm Đà Lạt (AM Trường) và Cam Ranh (AM Long) giảm đơn trên 30% do phàn nàn về tốc độ giao hàng."
        ],
        insights=[
            "Chất lượng vận hành Last-mile đang quyết định doanh thu kinh doanh; khi bưu cục của AM Long và AM Trường giao trễ, shop lập tức chia sẻ đơn sang đơn vị khác."
        ],
        warnings=[
            "Mất 3 shop nhóm A này đồng nghĩa với việc vùng Nam Trung Bộ sẽ mất đi khoảng 150 triệu đồng doanh thu mỗi tháng."
        ],
        actions=[
            "AM Phan Đình Duy, AM Lê Văn Trường và AM Nguyễn Thanh Long trực tiếp đến gặp 3 chủ shop này trong vòng 48h để xử lý dứt điểm khiếu nại và cam kết lại dịch vụ."
        ]
    )

    # =========================================================================
    # 16. BƯU CỤC CẢNH BÁO & LỜI KẾT W39
    # =========================================================================
    add_redesigned_callout(
        doc,
        section_title="🏁 [XVI. ĐIỀU HÀNH TRỌNG ĐIỂM: 13 BƯU CỤC CẢNH BÁO BẤT ỔN & 5 TRỌNG TÂM HÀNH ĐỘNG TUẦN W39]",
        speech_title="🗣️ DANH SÁCH 13 BƯU CỤC NGUY HIỂM & GIAO NHIỆM VỤ ĐÍCH DANH TỪNG AM:",
        province_block=[
            "• Lâm Đồng (7 bưu cục báo động đỏ - chiếm 58% danh sách):",
            "  1. Xuân Hương - Đà Lạt: 2.165 đơn backlog (AM Lê Văn Trường)",
            "  2. Đơn Dương: 2.038 đơn backlog (AM Lê Văn Trường)",
            "  3. Di Linh: 1.970 đơn backlog (AM Trầm Hữu Tiến)",
            "  4. Đức Trọng 1: 1.223 đơn backlog (AM Trầm Hữu Tiến)",
            "  5. Lang Biang - Đà Lạt 1: 992 đơn backlog (AM Lê Minh Lợi)",
            "  6. Lâm Viên - Đà Lạt 2: 860 đơn backlog (AM Lê Văn Trường)",
            "  7. Tân Hà Lâm Hà: 798 đơn backlog (AM Huỳnh Thị Kim Chi)",
            "• Khánh Hòa (2 bưu cục backlog lớn nhất vùng):",
            "  8. Cam Linh: 2.433 đơn backlog (AM Nguyễn Thanh Long) ➔ Bưu cục nghẽn nặng nhất vùng!",
            "  9. Tây Nha Trang: 2.295 đơn backlog (AM Phan Đình Duy)",
            "• Đắk Nông (4 bưu cục tồn đọng):",
            "  10. Quảng Tín: 1.224 đơn backlog (AM Trương Quang Linh)",
            "  11. Kiến Đức: 1.035 đơn backlog (AM Hồng Bích Nga)",
            "  12. Tuy Đức: 640 đơn backlog (AM Trần Thị Nhung)",
            "  13. Nhân Cơ: 347 đơn backlog (AM Huỳnh Thúc Duân)",
            "➔ TOÀN VÙNG: 13 bưu cục cảnh báo bất ổn đang ghìm giữ tới 18.020 đơn hàng tồn đọng!"
        ],
        am_analysis_block=[
            "Kính thưa Ban Giám Đốc, để dập tắt điểm nóng tại 13 bưu cục này, em xin phân công nhiệm vụ cụ thể cho từng AM phụ trách:",
            "• AM Lê Văn Trường: Đang quản lý tới 3 bưu cục cảnh báo (Xuân Hương, Đơn Dương, Lâm Viên 2) với tổng tồn 5.063 đơn. Yêu cầu AM Trường cắm chốt tại Xuân Hương, điều phối xe gom dọn kho ngay trong 48h.",
            "• AM Trầm Hữu Tiến: Quản lý Di Linh và Đức Trọng 1 với tổng tồn 3.193 đơn. Yêu cầu AM Tiến kiểm tra lại lực lượng bốc xếp ca đêm và xử lý dứt điểm 504 đơn tồn aging.",
            "• AM Nguyễn Thanh Long: Quản lý bưu cục Cam Linh (2.433 đơn, hoàn trả 16,96%). Yêu cầu AM Long thay thế điều phối viên yếu kém, chấn chỉnh shipper giao tuyến Cam Ranh.",
            "• AM Phan Đình Duy: Quản lý bưu cục Tây Nha Trang (2.295 đơn), tăng cường thêm 5 shipper từ các bưu cục nội thành Nha Trang sang hỗ trợ giải phóng hàng.",
            "• AM Trương Quang Linh: Quản lý bưu cục Quảng Tín (GTC 16,8%, hoàn 37,9%), cần tổng kiểm kê và rà soát toàn bộ nhân sự bưu tá.",
            "5 MỆNH LỆNH HÀNH ĐỘNG TUẦN W39 CỦA BAN GIÁM ĐỐC:",
            "1. Cân đo đối soát 100% kiện hàng tại bưu cục gửi, thu hồi dứt điểm 282,4 triệu đồng truy thu.",
            "2. Điều chỉnh cắt giảm 15 chuyến xe KTC non tải, đưa tỷ lệ lấp đầy thùng xe quay lại mốc trên 55%.",
            "3. Giải tỏa toàn bộ 1.638 đơn Aging >5 ngày trước 18h00 ngày thứ Tư.",
            "4. Bắt buộc duy trì gán Ca 2 trên 85% để kéo tỷ lệ %GTC toàn vùng vượt mốc 58%.",
            "5. AM Kinh doanh gặp trực tiếp 3 shop nhóm A giảm đơn để giữ chân khách hàng.",
            "Em xin chân thành cảm ơn Ban Giám Đốc và các anh chị đã lắng nghe. Kính mời Ban Giám Đốc cho ý kiến chỉ đạo!"
        ],
        insights=[
            "13 bưu cục này đang quyết định 80% chất lượng vận hành của cả vùng; chỉ cần 5 AM phụ trách tập trung cứu hộ xong là toàn vùng sẽ đạt chuẩn SLA."
        ],
        warnings=[
            "AM nào có bưu cục nằm cảnh báo liên tục quá 3 tuần mà không có cam kết chuyển biến sẽ bị điều chuyển vị trí công tác."
        ],
        actions=[
            "Các AM có tên trong danh sách phải nộp kế hoạch giải phóng hàng chi tiết từng ngày về Ban Giám Đốc trước 18h00 hôm nay."
        ]
    )

    out_docx1 = "KICH_BAN_THUYET_TRINH_W38_INSIGHT_CHUYEN_SAU.docx"
    out_docx2 = "KICH_BAN_THUYET_TRINH_W38_NAM_TRUNG_BO.docx"
    doc.save(out_docx1)
    doc.save(out_docx2)
    print(f"Saved redesigned docx: {out_docx1} ({os.path.getsize(out_docx1)} bytes)")
    print(f"Saved redesigned docx: {out_docx2} ({os.path.getsize(out_docx2)} bytes)")

if __name__ == "__main__":
    build_w38_redesigned_document()
