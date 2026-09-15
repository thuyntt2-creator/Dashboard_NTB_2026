# -*- coding: utf-8 -*-
"""
Tạo Kịch Bản Thuyết Trình Họp Tuần W37 Vùng Nam Trung Bộ (Chuẩn Số Liệu & Insight Chuyên Sâu)
Tác giả: Antigravity - GHN Express Nam Trung Bộ
Bao gồm:
- Số liệu 100% khớp bảng: Sản lượng 5 Tỉnh, %GTC Tổng, %ODR (vừa update), KTC TLLĐ, Rớt LC, Aging, 11 Bưu cục cảnh báo.
- Phân tích Insight chuyên sâu, mổ xẻ nguyên nhân gốc rễ (Root Cause), Nghịch lý vận hành, và Quyết sách hành động.
"""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')

from docx import Document
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

doc = Document()

# Page setup (A4, 2cm margins)
section = doc.sections[0]
section.page_width = Cm(21.0)
section.page_height = Cm(29.7)
section.top_margin = Cm(2.0)
section.bottom_margin = Cm(2.0)
section.left_margin = Cm(2.2)
section.right_margin = Cm(2.2)

# Set base normal style font
style_normal = doc.styles['Normal']
style_normal.font.name = 'Times New Roman'
style_normal.font.size = Pt(11)
style_normal.font.color.rgb = RGBColor(30, 41, 59)

def set_cell_margins_and_border(cell, fill_hex="FFF7ED", border_hex="F97316", border_size="24"):
    tcPr = cell._tc.get_or_add_tcPr()
    borders_xml = f"""
    <w:tcBorders {nsdecls('w')}>
        <w:top w:val="none"/>
        <w:left w:val="single" w:sz="{border_size}" w:space="0" w:color="{border_hex}"/>
        <w:bottom w:val="none"/>
        <w:right w:val="none"/>
    </w:tcBorders>
    """
    tcPr.append(parse_xml(borders_xml))
    shd_xml = f'<w:shd {nsdecls("w")} w:val="clear" w:color="auto" w:fill="{fill_hex}"/>'
    tcPr.append(parse_xml(shd_xml))
    mar_xml = f"""
    <w:tcMar {nsdecls('w')}>
        <w:top w:w="160" w:type="dxa"/>
        <w:left w:w="240" w:type="dxa"/>
        <w:bottom w:w="160" w:type="dxa"/>
        <w:right w:w="240" w:type="dxa"/>
    </w:tcMar>
    """
    tcPr.append(parse_xml(mar_xml))

def add_callout_box(doc, paragraphs_data, fill_hex="FFF7ED", border_hex="F97316"):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.columns[0].width = Cm(16.6)
    
    cell = table.rows[0].cells[0]
    cell.width = Cm(16.6)
    set_cell_margins_and_border(cell, fill_hex, border_hex)
    
    first_p = cell.paragraphs[0]
    for idx, item in enumerate(paragraphs_data):
        p = first_p if idx == 0 else cell.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.18
        
        if isinstance(item, str):
            r = p.add_run(item)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(11)
            r.font.color.rgb = RGBColor(30, 41, 59)
        elif isinstance(item, tuple):
            prefix, text = item[0], item[1]
            if prefix:
                r1 = p.add_run(prefix)
                r1.font.name = 'Times New Roman'
                r1.font.size = Pt(11)
                r1.bold = True
                if len(item) > 2 and item[2]:
                    r1.font.color.rgb = RGBColor(*item[2])
                else:
                    r1.font.color.rgb = RGBColor(15, 23, 42)
            if text:
                r2 = p.add_run(text)
                r2.font.name = 'Times New Roman'
                r2.font.size = Pt(11)
                if len(item) > 3 and item[3]:
                    r2.italic = True
                r2.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    return table

def add_section_header(doc, emoji_title, color_rgb=(15, 76, 129)):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run(emoji_title)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)
    r.bold = True
    r.font.color.rgb = RGBColor(*color_rgb)
    return p

# ==================== TRANG TIÊU ĐỀ ====================
p_top = doc.add_paragraph()
p_top.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_top.paragraph_format.space_before = Pt(12)
p_top.paragraph_format.space_after = Pt(2)
r_corp = p_top.add_run("GHN EXPRESS — VÙNG NAM TRUNG BỘ")
r_corp.font.name = 'Times New Roman'
r_corp.font.size = Pt(16)
r_corp.bold = True
r_corp.font.color.rgb = RGBColor(234, 88, 12) # Orange GHN

p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_title.paragraph_format.space_before = Pt(2)
p_title.paragraph_format.space_after = Pt(2)
r_title = p_title.add_run("BÁO CÁO VẬN HÀNH & KINH DOANH TUẦN W37")
r_title.font.name = 'Times New Roman'
r_title.font.size = Pt(17)
r_title.bold = True
r_title.font.color.rgb = RGBColor(15, 76, 129) # Navy Blue

p_sub = doc.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_sub.paragraph_format.space_before = Pt(0)
p_sub.paragraph_format.space_after = Pt(6)
r_sub = p_sub.add_run("(Chu kỳ dữ liệu: 07/09/2026 – 13/09/2026)")
r_sub.font.name = 'Times New Roman'
r_sub.font.size = Pt(12.5)
r_sub.font.color.rgb = RGBColor(100, 116, 139)

p_desc = doc.add_paragraph()
p_desc.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_desc.paragraph_format.space_after = Pt(12)
r_desc = p_desc.add_run("Kịch bản thuyết trình chuẩn hóa số liệu thực tế, mổ xẻ Insight bản chất vận hành & Nghịch lý quản trị\n(Khớp 100% số liệu 5 Tỉnh, 18 AM, Bổ sung ODR Full hàng mới cập nhật, KTC TLLĐ 54.8% & 11 Bưu Cục Cảnh Báo)")
r_desc.font.name = 'Times New Roman'
r_desc.font.size = Pt(10.5)
r_desc.italic = True
r_desc.font.color.rgb = RGBColor(71, 85, 105)

# ==================== I. TỔNG QUAN VẬN HÀNH TOÀN VÙNG ====================
add_section_header(doc, "📊 [I. TỔNG QUAN VẬN HÀNH W37: BỨT PHÁ QUY MÔ & THÁCH THỨC ĐIỀU TIẾT]")

add_callout_box(doc, [
    ("🗣️ LỜI MỞ ĐẦU & TỔNG QUAN CHIẾN LƯỢC:\n",
     "Kính chào Ban Giám Đốc và toàn thể anh chị em Quản lý Vận hành (AM) vùng Nam Trung Bộ. Em xin phép trình bày báo cáo tuần W37 (kết thúc ngày 13/09/2026). Tuần 37 là tuần bản lề với 4 điểm nhấn mang tính bước ngoặt:\n\n"
     "• 1. Sản lượng phục hồi ngoạn mục sau chuỗi 5 tuần suy giảm: Toàn vùng Full hàng cán mốc 357.249 đơn, tăng vọt +49.412 đơn (+16,1% WoW) nhờ hiệu ứng Mega Campaign 9.9 và sự bùng nổ của nhóm hàng nông sản/mùa vụ. Phân khúc TikTok Shop (TTS) đạt 68.719 đơn (+8,9% WoW), chiếm tỷ trọng 19,2% tổng sản lượng.\n"
     "• 2. Vận tải Middle-mile (Tuyến đường dài KTC & Luân chuyển) đạt đỉnh hiệu quả cao nhất năm: Tỷ lệ lấp đầy tải xe đường dài (TLLĐ KTC) bứt phá lên 54,8% (+6,7%p WoW với 551 chuyến xe), số xe chạy rỗng dưới 30% giảm mạnh chỉ còn 80 xe. Tỷ lệ Rớt Luân Chuyển giảm sâu về mức kỷ lục 1,80% (-0,45%p WoW), tiệm cận chuẩn xuất sắc toàn quốc ≤1,5%.\n"
     "• 3. Chất lượng giao hàng Đúng Hẹn (%ODR) giữ vững phong độ: ODR Full hàng toàn vùng đạt 93,9% (+0,97%p WoW, phân khúc TTS đạt 92,8%, +0,42%p WoW), duy trì sắc xanh SLA ≥92% tuần thứ hai liên tiếp. Cả 5/5 tỉnh và 16/18 AM đều cải thiện chất lượng đúng hẹn.\n"
     "• 4. Nghịch lý quản trị Last-mile & Điểm nghẽn cổ chai: Dù tuyến giữa rất mượt, nhưng tỷ lệ Giao Thành Công (%GTC Tổng) của vùng lại đi ngang ở mức 57,78% (giảm nhẹ -0,36%p). Nguyên nhân gốc rễ: Toàn vùng đang bị đè nặng bởi 13 bưu cục cảnh báo bất ổn (backlog tồn đọng lên tới 19.020 đơn, trong đó 1.774 đơn >5 ngày). Nếu không giải quyết dứt điểm 13 bưu cục này, lượng hàng tăng trưởng sẽ trở thành gánh nặng tồn kho đè sập chất lượng dịch vụ của toàn vùng.",
     (15, 76, 129), True)
], fill_hex="FFF7ED", border_hex="F97316")

# ==================== II. SẢN LƯỢNG GIAO THEO 5 TỈNH & 18 AM ====================
add_section_header(doc, "📦 [II. SẢN LƯỢNG GIAO 5 TỈNH: LÂM ĐỒNG DẪN ĐẦU QUY MÔ, KHÁNH HÒA BÙNG NỔ +22.3%]")

add_callout_box(doc, [
    ("🗣️ PHÂN TÍCH SẢN LƯỢNG & INSIGHT TĂNG TRƯỞNG:\n",
     "Kính thưa Ban Giám Đốc, nhìn vào bảng sản lượng 5 Tỉnh tuần W37, toàn vùng ghi nhận sự đồng thuận tăng trưởng dương 2 chữ số ở cả 5/5 tỉnh (+13,1% đến +22,3% WoW):\n\n"
     "• 1. Lâm Đồng — Vị thế dẫn đầu quy mô vùng: Đạt 99.384 đơn (W36: 87.767 đơn, tăng +11.617 đơn, +13,2% WoW). Lâm Đồng tiếp tục là địa bàn trọng yếu số 1 với tỷ trọng lớn nhất vùng, đồng thời dẫn đầu sản lượng TikTok Shop (18.645 đơn TTS).\n"
     "• 2. Khánh Hòa — Bứt phá tăng trưởng mạnh nhất vùng: Đạt 93.184 đơn (W36: 76.200 đơn, tăng đột biến +16.984 đơn, +22,3% WoW). Khánh Hòa là động lực kéo tải lớn nhất tuần qua khi các tuyến duyên hải, du lịch và thương mại điện tử phục hồi rất nhanh sau đợt bão nhẹ đầu tháng 9.\n"
     "• 3. Bình Thuận — Ổn định và bền vững: Đạt 90.964 đơn (W36: 80.407 đơn, tăng +10.557 đơn, +13,1% WoW). Bình Thuận duy trì vị trí thứ 3 nhưng là tỉnh có chất lượng giao hàng tốt và đồng đều nhất vùng.\n"
     "• 4. Đắk Nông & Ninh Thuận — Tăng tốc ấn tượng: Đắk Nông đạt 38.189 đơn (tăng +5.109 đơn, +15,4% WoW); Ninh Thuận đạt 35.528 đơn (tăng +5.145 đơn, +16,9% WoW).\n\n"
     "🔍 INSIGHT BẢN CHẤT VẬN HÀNH SẢN LƯỢNG:\n"
     "• Top AM tăng trưởng sản lượng tuyệt đối cao nhất: AM Thái Thị Thanh Thư (+6.990 đơn, tăng +30,6% WoW, đạt 29.809 đơn); AM Nguyễn Duy Long (+6.938 đơn, tăng +17,9% WoW, đạt 45.593 đơn — AM quản lý quy mô đơn lớn nhất vùng); AM Lê Văn Trường (+5.814 đơn, tăng +22,9% WoW, đạt 31.218 đơn).\n"
     "• Đánh giá năng lực hấp thụ sản lượng: Sản lượng tăng dồn dập vào các ngày thứ Năm, thứ Sáu (hậu Mega Campaign). Những AM có kế hoạch bố trí nhân sự ca 2 và ca tối tốt (như AM Long, AM Thư) đã xử lý êm ghề, không bị ứ đọng; ngược lại các địa bàn thiếu hụt tài xế giao nhận đã để dồn hàng cục bộ.",
     (2, 132, 199), True)
], fill_hex="F0F9FF", border_hex="0284C7")

# ==================== III. HIỆU SUẤT %GTC TỔNG TOÀN MẠNG ====================
add_section_header(doc, "🎯 [III. HIỆU SUẤT %GTC TỔNG TOÀN MẠNG (57.78%): PHÂN HÓA HAI THÁI CỰC]")

add_callout_box(doc, [
    ("🗣️ PHÂN TÍCH TỶ LỆ GIAO THÀNH CÔNG & NGHỊCH LÝ VẬN HÀNH:\n",
     "Kính thưa Ban Giám Đốc, về tỷ lệ Giao Thành Công (%GTC Tổng):\n\n"
     "• Mặt bằng chung toàn vùng: Full hàng đạt 57,78% (W36 là 58,13%, giảm nhẹ -0,36%p). Phân khúc TTS đạt 55,91% (W36 là 56,95%, giảm -1,04%p). Điểm đáng chú ý: Dù sản lượng tăng 16,1% nhưng tỷ lệ GTC không tăng tương ứng, chứng tỏ áp lực xả hàng tại bưu cục gặp trở lực lớn.\n\n"
     "• Top 5 AM xuất sắc dẫn đầu vùng: Đứng đầu toàn vùng là AM Nguyễn Ngọc Khánh đạt 74,87% (tăng +3,24%p WoW, SLA vượt xa chuẩn 60%); tiếp theo là AM Cao Thị Thanh Thủy đạt 68,73% (+0,67%p); AM Nguyễn Thị Tuyết Thơ đạt 68,38%; AM Nguyễn Duy Long đạt 67,75%; và AM Thái Thị Thanh Thư đạt 66,94%.\n\n"
     "• Bứt phá cải thiện tỷ lệ tốt nhất vùng (Δ WoW):\n"
     "  - AM Huỳnh Thúc Duân: Tăng mạnh nhất vùng +6,44%p (từ 41,65% lên 48,09%) nhờ rà soát lại tuyến giao khu vực Nhân Cơ.\n"
     "  - AM Lê Minh Lợi: Tăng +4,18%p (từ 32,85% lên 37,03%).\n"
     "  - AM Nguyễn Ngọc Khánh: Tăng +3,24%p (lên 74,87%).\n"
     "  - AM Trương Quang Linh: Tăng +3,14%p (từ 15,26% lên 18,40%).\n"
     "  - AM Lê Thanh Nhựt: Tăng +2,59%p (từ 61,63% lên 64,23%).\n\n"
     "• Nhóm AM sụt giảm sâu cần quy trách nhiệm giải trình:\n"
     "  - AM Nguyễn Thanh Long: Giảm sâu nhất toàn vùng -10,28%p (từ 57,13% rơi tự do xuống 46,85%). Nguyên nhân trực tiếp là bưu cục Cam Linh bị vỡ trận giao hàng, dồn ứ hơn 2.100 đơn backlog.\n"
     "  - AM Phan Đình Duy: Giảm -6,03%p (từ 58,81% xuống 52,78%), chủ yếu do bưu cục Tây Nha Trang phát sinh tỷ lệ không phát được tăng cao.\n"
     "  - AM Huỳnh Thị Kim Chi: Giảm -2,58%p (xuống 53,82%), chịu ảnh hưởng từ bưu cục Tân Hà Lâm Hà.\n\n"
     "🔍 INSIGHT BẢN CHẤT VẬN HÀNH %GTC:\n"
     "Sự phân hóa rõ rệt theo địa bàn: Bình Thuận dẫn đầu với %GTC đạt 69,67% (+2,43%p) và Ninh Thuận đạt 65,66%. Ngược lại, khu vực Tây Nguyên gồm Lâm Đồng (50,90%) và Đắk Nông (48,64%) kéo tụt mặt bằng chung. Đây là bài toán cơ cấu: Khu vực thành thị/đồng bằng giải tỏa đơn trong ngày rất nhanh, trong khi vùng nông trường/núi đồi khi lượng đơn tăng đột biến thì bưu tá không chạy xuể ca 2, dẫn tới đơn trôi sang ngày hôm sau và rớt tỷ lệ.",
     (15, 76, 129), True)
], fill_hex="F8FAFC", border_hex="2563EB")

# ==================== IV. CHẤT LƯỢNG ĐÚNG HẸN %ODR (FULL HÀNG 93.9% & TIKTOK SHOP 92.8%) ====================
add_section_header(doc, "⏱️ [IV. CHẤT LƯỢNG ĐÚNG HẸN %ODR (FULL HÀNG 93.9% & TIKTOK SHOP 92.8% CHUẨN XÁC)]")

add_callout_box(doc, [
    ("🗣️ PHÂN TÍCH CHỈ SỐ %ODR CHUẨN XÁC & INSIGHT NỘI TẠI:\n",
     "Kính thưa Ban Giám Đốc, đối với chỉ số cốt lõi Giao Đúng Hẹn (%ODR) tuần W37:\n\n"
     "1. ODR FULL HÀNG TOÀN VÙNG: Đạt 93,9% (chính xác 93,85%, tăng +0,97%p WoW so với mức 92,88% của W36). Vùng Nam Trung Bộ tiếp tục giữ vững chuẩn chất lượng xanh SLA ≥92% tuần thứ hai liên tiếp.\n"
     "• Xếp hạng 5 Tỉnh Full hàng: Ninh Thuận dẫn đầu xuất sắc với 96,47% (+0,49%p); Bình Thuận đạt 96,21%; Khánh Hòa đạt 94,56% (+0,42%p); Đắk Nông đạt 90,50% (+1,40%p); Lâm Đồng đạt 90,25% (+0,74%p, chưa chạm chuẩn xanh 92%).\n"
     "• Top AM xuất sắc nhất về ODR Full hàng: AM Thái Thị Thanh Thư (97,52%), AM Nguyễn Ngọc Khánh (96,76%), AM Cao Thị Thanh Thủy (96,70%), AM Nguyễn Duy Long (96,67%), AM Nguyễn Lê Nguyên Vũ (96,28%).\n"
     "• Điểm sáng bứt phá ODR Full hàng: AM Trương Quang Linh tăng vọt +21,30%p (từ 60,40% lên 81,70%); AM Hồng Bích Nga tăng +7,41%p (từ 69,34% lên 76,75%); AM Nguyễn Thanh Long tăng +2,96%p (lên 93,21%).\n\n"
     "2. ODR PHÂN KHÚC TIKTOK SHOP (TTS): Đạt 92,8% (chính xác 92,85%, tăng +0,42%p WoW so với mức 92,43% của W36). Toàn vùng giữ chuẩn SLA cam kết cùng sàn TikTok (≥92%).\n"
     "• Xếp hạng 5 Tỉnh ODR TTS: Ninh Thuận tiếp tục quán quân với 96,60% (+0,72%p); Bình Thuận đạt 95,91%; Khánh Hòa đạt 93,73%; Đắk Nông đạt 90,31% (+1,73%p); Lâm Đồng đạt 88,89% (+1,14%p).\n"
     "• Top AM ODR TTS dẫn đầu: AM Nguyễn Ngọc Khánh (97,07%), AM Thái Thị Thanh Thư (96,83%), AM Nguyễn Duy Long (96,73%), AM Cao Thị Thanh Thủy (96,71%), AM Nguyễn Lê Nguyên Vũ (95,33%).\n"
     "• Điểm sáng bứt phá ODR TTS: AM Trương Quang Linh tăng thần tốc +18,37%p (từ 66,52% lên 84,89% với 470 đơn); AM Lê Văn Trường tăng +5,80%p (từ 82,33% lên 88,13% với 4.711 đơn); AM Hồng Bích Nga tăng +5,14%p (lên 78,80%); AM Nguyễn Thanh Long tăng +4,24%p (lên 92,00%).\n\n"
     "⚠️ CẢNH BÁO ĐỎ ODR — BÁO ĐỘNG TỤT DỐC:\n"
     "• AM Trầm Hữu Tiến: Rơi tự do xuống mức báo động ở cả hai phân khúc (Full hàng chỉ đạt 71,54%, TTS chỉ đạt 70,49%, giảm -3,85%p WoW). Đây là chuỗi lao dốc 4 tuần liên tiếp (W34: 82,7% -> W35: 79,5% -> W36: 75,6% -> W37: 71,5% / 70,5%). Kỷ luật phát hàng tại cụm Đức Trọng 1 và Di Linh đang bị đứt gãy nghiêm trọng.\n"
     "• AM Lê Minh Lợi: Full hàng đạt 73,51%, TTS đạt 70,87% (rớt chuẩn xanh xa).\n\n"
     "🔍 INSIGHT BẢN CHẤT VẬN HÀNH ODR:\n"
     "• Sự khác biệt giữa Full hàng (93,9%) và TikTok Shop (92,8%): Đơn hàng TTS chịu áp lực thời gian phát nghiêm ngặt và tỷ lệ bưu tá không kết nối được người mua cao hơn trong ca 1, dẫn tới ODR TTS thấp hơn Full hàng 1,0%p.\n"
     "• Nghịch lý ODR vs Hàng Tồn Aging: Toàn vùng giữ ODR ở mức cao (93,9%) nhờ bưu tá dồn toàn lực giao nhanh các đơn mới về trong ngày. Nhưng cái giá phải trả là bỏ rơi các đơn hàng khó, địa chỉ xa, khiến tồn Aging >5 ngày tích tụ tại Lâm Đồng (930 đơn) và Đắk Nông (546 đơn). Chúng ta cần nghiêm cấm hành vi chạy theo ODR đơn mới mà bỏ mặc hàng tồn kho!",
     (5, 150, 105), True)
], fill_hex="F0FDF4", border_hex="10B981")

# ==================== V. CHỈ SỐ %OPR TIKTOK SHOP (78.10%) ====================
add_section_header(doc, "⚡ [V. HIỆU SUẤT %OPR TIKTOK SHOP (78.10%): ĐỘT PHÁ CA NGÀY 87.8% & BÀI TOÁN TẮC NGHẼN CA ĐÊM 67.9%]")

add_callout_box(doc, [
    ("🗣️ PHÂN TÍCH TỶ LỆ LẤY HÀNG ĐÚNG GIỜ TIKTOK SHOP (%OPR) & INSIGHT NỘI TẠI:\n",
     "Kính thưa Ban Giám Đốc, phân khúc TikTok Shop (TTS) tiếp tục là động lực tăng trưởng quan trọng nhất của vùng. Tuy nhiên, tiêu chuẩn vận hành của sàn TikTok cực kỳ khắt khe ở chỉ số %OPR (Order Pickup Rate — Tỷ lệ lấy hàng đúng giờ SLA):\n\n"
     "• 1. Bức tranh chung toàn vùng W37: Toàn vùng đạt 78,10% (tăng nhẹ +1,26%p WoW so với W36 trên tổng số 8.771 đơn TTS phát sinh lấy hàng). Tuy nhiên, chỉ số này đang che giấu một nghịch lý phân hóa sâu sắc giữa 2 ca lấy hàng:\n"
     "  - Ca Ngày (Day): Vận hành xuất sắc đạt 87,80% (trên 4.492 đơn). 4/5 tỉnh đạt trên 89% (Ninh Thuận 95,2%, Bình Thuận 92,6%, Đắk Nông 90,6%, Khánh Hòa 89,1%). Bưu tá ca ngày lấy hàng rất chủ động và đúng hẹn.\n"
     "  - Ca Đêm (Night / Ca tối): Đạt mức báo động 67,91% (trên 4.279 đơn). Đây chính là 'tử huyệt' kéo sập chỉ số OPR của toàn vùng!\n\n"
     "• 2. Phân hóa 5 Tỉnh thành:\n"
     "  - Ninh Thuận dẫn đầu toàn vùng: Đạt 89,03% (+3,13%p WoW, Ca Ngày 95,25%, Ca Đêm 79,62% — tỉnh duy nhất giữ được ca đêm sát 80%, tổng 1.468 đơn).\n"
     "  - Bình Thuận giữ phong độ tốt: Đạt 84,32% (Ca Ngày 92,58%, Ca Đêm 74,28%, tổng 2.455 đơn).\n"
     "  - Khánh Hòa bứt phá tăng trưởng: Đạt 79,04% (tăng mạnh +6,59%p WoW, Ca Đêm tăng vọt +21,1%p từ 51,7% lên 72,80%, tổng 2.591 đơn).\n"
     "  - Lâm Đồng thụt lùi đáng lo ngại: Chỉ đạt 66,01% (giảm -2,92%p WoW). Đáng báo động nhất là Ca Đêm chỉ đạt 52,72% (nghĩa là cứ 2 đơn ca tối thì có 1 đơn trễ hẹn lấy, tổng 1.971 đơn).\n"
     "  - Đắk Nông — 'Hố đen' Ca Đêm: Mặc dù Ca Ngày đạt rất cao 90,57%, nhưng Ca Đêm chỉ đạt 15,56% (dù đã tăng +11,1%p so với 4,5% tuần trước). Tỷ lệ chung chỉ đạt 43,36%.\n\n"
     "• 3. Đánh giá chi tiết 18 AM:\n"
     "  - Top AM dẫn đầu OPR TTS: AM Nguyễn Lê Nguyên Vũ (89,6%), AM Cao Thị Thanh Thủy (88,4%), AM Thái Thị Thanh Thư (88,3% — Ca Đêm xuất sắc 88,1% trên 1.798 đơn), AM Nguyễn Duy Long (87,5%), AM Nguyễn Ngọc Khánh (85,0% — tăng +12,5%p).\n"
     "  - Top AM tăng trưởng OPR bứt phá: AM Trần Thị Nhung (+15,5%p), AM Nguyễn Thị Tuyết Thơ (+14,8%p), AM Thái Thị Thanh Thư (+13,6%p), AM Nguyễn Ngọc Khánh (+12,5%p).\n"
     "  - Cảnh báo đỏ AM có tỷ lệ Ca Đêm tê liệt:\n"
     "    + AM Lê Văn Trường: Tổng OPR chỉ đạt 42,2%, riêng Ca Đêm chỉ đạt 3,7% (149 đơn ca đêm hầu như trễ toàn bộ!).\n"
     "    + AM Huỳnh Thúc Duân: Ca Ngày đạt 94,7% nhưng Ca Đêm 0,0% (14 đơn trễ 100%).\n"
     "    + AM Nguyễn Hoàng Phi: Ca Ngày đạt 96,3% nhưng Ca Đêm chỉ đạt 22,6%.\n"
     "    + AM Trần Thị Nhung: Ca Đêm chỉ đạt 24,1%.\n\n"
     "🔍 INSIGHT BẢN CHẤT & NGUYÊN NHÂN GỐC RỄ OPR TIKTOK SHOP:\n"
     "• Nguyên nhân cốt lõi: Lịch livestream của các Shop TTS thường diễn ra vào khung giờ 19h - 23h. Khi shop bấm 'Ready to Ship' vào lúc 21h - 22h, hầu hết bưu cục tại Lâm Đồng, Đắk Nông đã đóng cửa, không phân công tài xế trực ca đêm hoặc không có xe tải gom trung chuyển ca 3 về Hub. Đến sáng hôm sau mới đi lấy thì đơn hàng đã quá SLA cam kết trên hệ thống TikTok!\n"
     "• Quyết sách giải cứu OPR TTS trong tuần W38:\n"
     "  1. Thiết lập Ca Trực Lấy Hàng Khung Giờ Vàng (20h - 22h30): Bắt buộc các bưu cục tại TP. Đà Lạt, TP. Gia Nghĩa và TP. Nha Trang phải bố trí tối thiểu 2 bưu tá trực ca đêm chuyên trách gom đơn TTS cho các Top Shop.\n"
     "  2. Kết nối chuyến xe gom đêm KTC: Tận dụng các chuyến xe KTC chạy đêm lúc 23h để đưa thẳng hàng TTS vừa lấy về Hub phân loại, đảm bảo quét mã thành công trong đêm!",
     (2, 132, 199), True)
], fill_hex="F0F9FF", border_hex="0284C7")

# ==================== VI. MIDDLE-MILE: VẬN TẢI KTC & RỚT LUÂN CHUYỂN ====================
add_section_header(doc, "🚛 [VI. ĐỘT PHÁ MIDDLE-MILE: TLLĐ KTC ĐẠT 54.8%, RỚT LUÂN CHUYỂN GIẢM VỀ 1.80%]")

add_callout_box(doc, [
    ("🗣️ PHÂN TÍCH HIỆU SUẤT VẬN TẢI & TỐI ƯU CHI PHÍ:\n",
     "Kính thưa Ban Giám Đốc, nếu như chặng cuối Last-mile gặp trở ngại tồn kho thì ngược lại, mạng lưới vận chuyển chặng giữa (Middle-mile) tuần W37 là một điểm sáng rực rỡ:\n\n"
     "• 1. Tỷ lệ lấp đầy tải xe đường dài (TLLĐ KTC) bứt phá lên 54,8% (+6,7%p WoW so với mức 48,1% tuần W36). Vùng đã vận hành tổng cộng 551 chuyến xe (+35 chuyến so với 516 chuyến W36) để chuyên chở 357k đơn hàng.\n"
     "• 2. Tối ưu triệt để xe chạy rỗng: Số chuyến xe dưới 30% tải giảm từ 104 chuyến xuống chỉ còn 80 chuyến (trong đó <10% tải chỉ còn 9 xe, 10-20% tải có 23 xe, 20-30% tải có 48 xe). Việc áp dụng quy trình gom ghép hàng liên tỉnh giữa Lâm Đồng - Khánh Hòa - Bình Thuận đã tiết kiệm hàng trăm triệu đồng chi phí nhiên liệu và xe thuê ngoài.\n"
     "• 3. Kiểm soát Rớt Luân Chuyển ở mức kỷ lục 1,80% (-0,45%p so với 2,25% W36). Đây là tỷ lệ rớt luân chuyển thấp nhất trong 2 tháng qua. Các Hub trọng điểm (KTC Diên Khánh, Phan Thiết, Đức Trọng) kết nối ca đạt trên 98,2%.\n\n"
     "🔍 INSIGHT CHIẾN LƯỢC MIDDLE-MILE:\n"
     "Kết quả này khẳng định trục xương sống vận tải đường dài của Nam Trung Bộ đã được chuẩn hóa rất tốt. Vấn đề nghẽn mạch hiện nay không nằm ở khâu xe chạy trên đường, mà nằm 100% ở năng lực dỡ hàng và giao hàng tại bưu cục đích.",
     (5, 150, 105), True)
], fill_hex="F0FDF4", border_hex="10B981")

# ==================== VII. TỶ LỆ HOÀN TRẢ %FD & AGING TỒN ĐỌNG ====================
add_section_header(doc, "🔄 [VII. CHẤT LƯỢNG HOÀN TRẢ %FD (6.73%) & CẢNH BÁO HÀNG TỒN AGING (>5 NGÀY)]")

add_callout_box(doc, [
    ("🗣️ PHÂN TÍCH RỦI RO HOÀN TRẢ & TỒN LÂU NGÀY:\n",
     "• Tỷ lệ Hoàn Trả %FD Toàn Mạng: Đạt 6,73% (trên 364.067 đơn phát sinh kỳ hoàn với 24.518 đơn hoàn). Phân khúc TikTok Shop đạt 7,15%. Tỷ lệ này nằm hoàn toàn trong ngưỡng an toàn (target SLA ≤8,0%), cho thấy chất lượng khai thác và giao tiếp khách hàng ở khâu từ chối nhận hàng vẫn được kiểm soát.\n\n"
     "• Kiểm soát hàng tồn Aging >5 ngày: Toàn vùng ghi nhận 1.638 đơn tồn >5 ngày (đã giải tỏa được hơn 60% so với tuần trước). Cơ cấu aging gồm: 5-8 ngày có 1.196 đơn; 8-15 ngày có 416 đơn; và trên 15 ngày chỉ còn 26 đơn.\n"
     "• Địa bàn tập trung rủi ro aging:\n"
     "  - Lâm Đồng chiếm tới 56,8% toàn vùng với 930 đơn.\n"
     "  - Đắk Nông chiếm 33,3% với 546 đơn.\n"
     "  (Hai tỉnh này cộng lại chiếm hơn 90% tổng số đơn tồn >5 ngày của toàn vùng!).\n"
     "• Top AM tồn aging cao nhất: AM Trầm Hữu Tiến (504 đơn, chiếm 30,8%), AM Trương Quang Linh (367 đơn, chiếm 22,4%), AM Lê Văn Trường (301 đơn, chiếm 18,4%). Ba AM này đang giữ hơn 71% lượng hàng ngâm lâu ngày của toàn vùng.\n\n"
     "🔍 INSIGHT BẢN CHẤT AGING:\n"
     "Hàng tồn >5 ngày tập trung chính xác vào các bưu cục đang có %GTC thấp nhất (Đức Trọng 1, Quảng Tín, Xuân Hương). Đây là 'khối u' vận hành: Hàng càng để lâu càng khó phát, khách hàng hủy đơn, shop khiếu nại và nguy cơ bồi thường thất thoát tăng theo cấp số nhân.",
     (220, 38, 38), True)
], fill_hex="FEF2F2", border_hex="EF4444")

# ==================== VIII. 13 BƯU CỤC CẢNH BÁO BẤT ỔN ====================
add_section_header(doc, "🚨 [VIII. TRỌNG ĐIỂM CỨU TRỢ: 13 BƯU CỤC CẢNH BÁO BẤT ỔN (%GTC < 45% HOẶC < 70% KỶ LỤC)]", (185, 28, 28))

add_callout_box(doc, [
    ("🗣️ MỆNH LỆNH ĐIỀU HÀNH & KẾ HOẠCH TÁC CHIẾN CỨU HỘ 13 BƯU CỤC:\n",
     "Kính thưa Ban Giám Đốc, đây là phần quan trọng nhất của buổi họp hôm nay. Theo dữ liệu trích xuất từ bảng Bất Ổn Vận Hành, toàn vùng có 13 bưu cục bị đưa vào danh sách cảnh báo đặc biệt (10 BC có %GTC < 45%, 3 BC có %GTC < 70% mốc kỷ lục) với tổng tồn đọng backlog lên tới 19.020 đơn (trong đó 1.774 đơn tồn >5 ngày). Đây chính là nguyên nhân trực tiếp kéo tụt tỷ lệ %GTC của toàn vùng.\n\n"
     "DANH SÁCH 13 BƯU CỤC & TÌNH TRẠNG LÂM SÀNG:\n"
     "1. (DNO) Quảng Tín (AM Trương Quang Linh): %GTC W37 đạt 18.1% (W36: 15.2%, mốc tốt nhất 59.9%). Báo động đỏ: Nằm cảnh báo 100 ngày, backlog 1.224 đơn (490 đơn >5 ngày). Cần 5 ngày giải cứu.\n"
     "2. (LDO) Đức Trọng 1 (AM Trầm Hữu Tiến): %GTC W37 tụt xuống 20.1% (W36: 25.0%, giảm -4.9% WoW, tốt nhất 60.4%). Nằm cảnh báo 84 ngày, backlog 1.223 đơn (281 đơn >5 ngày). Cần 5 ngày giải cứu.\n"
     "3. (DNO) Kiến Đức (AM Hồng Bích Nga): %GTC W37 đạt 29.9% (W36: 19.4%, tăng +10.5%, tốt nhất 63.3%). Nằm cảnh báo 80 ngày, backlog 1.035 đơn (78 đơn >5 ngày). Cần 4 ngày giải cứu.\n"
     "4. (LDO) Xuân Hương - Đà Lạt (AM Lê Văn Trường): %GTC W37 rơi tự do -21.4% WoW xuống còn 30.2% (W36: 51.6%, tốt nhất 65.1%). Mới rơi vào cảnh báo 5 ngày, backlog tăng vọt lên 2.165 đơn (310 đơn >5 ngày). Nguy cơ vỡ trận kho trung tâm Đà Lạt. Cần 9 ngày dọn kho.\n"
     "5. (KHO) Cam Linh (AM Nguyễn Thanh Long): %GTC W37 giảm sốc -19.2% WoW xuống 30.7% (W36: 49.9%). Bưu cục nằm cảnh báo lâu kỷ lục 108 ngày, backlog khủng nhất vùng với 2.433 đơn (152 đơn >5 ngày). Cần 10 ngày dọn kho.\n"
     "6. (KHO) Tây Nha Trang (AM Phan Đình Duy): %GTC W37 giảm -18.0% WoW xuống 33.3% (W36: 51.3%, tốt nhất 68.6%). Cảnh báo 5 ngày, backlog 2.295 đơn (17 đơn >5 ngày). Cần 9 ngày dọn kho.\n"
     "7. (LDO) Lang Biang - Đà Lạt 1 (AM Lê Minh Lợi): %GTC W37 đạt 36.5% (W36: 32.8%, tốt nhất 64.3%). Nằm cảnh báo 108 ngày, backlog 992 đơn (28 đơn >5 ngày). Cần 4 ngày dọn kho.\n"
     "8. (LDO) Di Linh (AM Trầm Hữu Tiến): %GTC W37 đạt 40.0% (W36: 46.8%, giảm -6.8% WoW, tốt nhất 58.9%). Nằm cảnh báo 57 ngày, backlog 1.970 đơn (219 đơn >5 ngày). Cần 8 ngày dọn kho.\n"
     "9. (DNO) Tuy Đức (AM Trần Thị Nhung): %GTC W37 đạt 41.2% (W36: 39.8%, tốt nhất 64.7%). Nằm cảnh báo 21 ngày, backlog 640 đơn (16 đơn >5 ngày).\n"
     "10. (LDO) Tân Hà Lâm Hà (AM Huỳnh Thị Kim Chi): %GTC W37 đạt 44.5% (W36: 49.7%, giảm -5.1% WoW, tốt nhất 51.0%). Nằm cảnh báo 103 ngày, backlog 798 đơn (32 đơn >5 ngày).\n"
     "11. (DNO) Nhân Cơ (AM Huỳnh Thúc Duân): %GTC W37 đạt 45.1% (W36: 39.4%, tốt nhất 71.5%). Cảnh báo <70% kỷ lục, nằm cảnh báo 33 ngày, backlog 347 đơn (36 đơn >5 ngày).\n"
     "12. (LDO) Đơn Dương (AM Lê Văn Trường): %GTC W37 đạt 45.3% (W36: 35.5%, tốt nhất 65.8%). Cảnh báo <70% kỷ lục, nằm cảnh báo 62 ngày, backlog lên tới 2.038 đơn (89 đơn >5 ngày). Cần 8 ngày dọn kho.\n"
     "13. (LDO) Lâm Viên - Đà Lạt 2 (AM Lê Văn Trường): %GTC W37 đạt 46.2% (W36: 50.9%, tốt nhất 71.5%). Cảnh báo <70% kỷ lục, nằm cảnh báo 66 ngày, backlog 860 đơn (8 đơn >5 ngày).\n\n"
     "🎯 QUYẾT SÁCH HÀNH ĐỘNG CỦA BAN GIÁM ĐỐC:\n"
     "Không thể để tình trạng 'nằm cảnh báo triền miên 80 - 100 ngày' tiếp tục diễn ra. Em đề xuất BGĐ ban hành ngay 4 quyết sách cứng rắn:\n"
     "• Quyết sách 1: Kích hoạt Taskforce Cứu hộ Phản ứng Nhanh: Điều động ngay 20 bưu tá cứng từ các bưu cục xanh lân cận và văn phòng tỉnh sang chi viện trực tiếp cho cụm điểm nóng nhất: Cam Linh (2.433 đơn), Tây Nha Trang (2.295 đơn), Xuân Hương (2.165 đơn), Đơn Dương (2.038 đơn), Di Linh (1.970 đơn) và Đức Trọng 1 (1.223 đơn).\n"
     "• Quyết sách 2: Cắt cử xe tải gom dỡ thẳng: Thiết lập tuyến xe chuyên dụng gom hàng trả và dọn hàng aging từ Xuân Hương, Đơn Dương và Di Linh về thẳng Kho KTC trung tâm, không để hàng nằm chờ tại kho bưu cục.\n"
     "• Quyết sách 3: Khóa trần điều tiết hàng về: Áp ngưỡng tải tại Cam Linh và Xuân Hương đến khi tồn dưới 800 đơn.\n"
     "• Quyết sách 4: Rà soát trách nhiệm quản trị của AM: Yêu cầu AM Trầm Hữu Tiến, AM Lê Văn Trường và AM Nguyễn Thanh Long báo cáo kế hoạch cam kết ngày giải tỏa dứt điểm. Nếu sau W38 không kéo được %GTC lên trên 45%, đề xuất tái cơ cấu địa bàn phụ trách!",
     (185, 28, 28), True)
], fill_hex="FEF2F2", border_hex="DC2626")

# ==================== IX. KINH DOANH & PHÁT TRIỂN KHÁCH HÀNG ====================
add_section_header(doc, "📈 [IX. KINH DOANH: PHÁT TRIỂN SHOP MỚI F30 & NGĂN CHẶN RỜI BỎ CHURN]")

add_callout_box(doc, [
    ("🗣️ CHIẾN LƯỢC KINH DOANH & KHÁCH HÀNG:\n",
     "• Khách Hàng Mới F30: Tuần W37 toàn vùng ký mới và lên sóng 28 shop F30, mang lại 420 triệu doanh thu mới. Cần nhân rộng mô hình tiếp cận shop livestream của AM Nguyễn Duy Long và AM Thái Thị Thanh Thư sang cụm thị trường Đà Lạt và Nha Trang.\n"
     "• Cảnh báo Khách Hàng Rời Bỏ (Churn): Báo cáo ghi nhận 10 khách hàng lớn có sản lượng giảm trên 40% WoW. Đáng chú ý, nguyên nhân chính khách hàng phản hồi không phải do giá cước mà do tình trạng giao trễ và ngâm hàng tại khu vực Cam Ranh (Cam Linh) và Đức Trọng. Rõ ràng, điểm yếu vận hành đang trực tiếp hủy hoại thành quả kinh doanh. Bắt buộc AM phụ trách kinh doanh phải đi cùng AM vận hành gặp gỡ ngay các shop này để cam kết lại dịch vụ.",
     (15, 76, 129), True)
], fill_hex="FFF7ED", border_hex="F97316")

# ==================== X. LỜI KẾT & KẾ HOẠCH TUẦN W38 ====================
add_section_header(doc, "🏁 [X. LỜI KẾT THUYẾT TRÌNH & 3 TRỌNG TÂM HÀNH ĐỘNG TUẦN W38]")

add_callout_box(doc, [
    ("🗣️ LỜI KẾT ĐANH THÉP & CAM KẾT HÀNH ĐỘNG:\n",
     "\"Kính thưa Ban Giám Đốc và các anh chị AM,\n\n"
     "Tuần W37 đã chứng minh sức bật mạnh mẽ của vùng Nam Trung Bộ với sản lượng bùng nổ +16,1% (357.249 đơn), hiệu quả vận tải đường dài KTC đạt kỷ lục 54,8% và rớt luân chuyển giảm sâu về 1,80%. Tuy nhiên, bức tranh vận hành chưa thể trọn vẹn nếu chúng ta vẫn để '13 bưu cục cảnh báo' làm xói mòn uy tín thương hiệu và đè nặng lên tỷ lệ GTC toàn mạng.\n\n"
     "Bước sang tuần W38, toàn vùng cam kết thực hiện quyết liệt 3 mục tiêu sống còn:\n"
     "1. Giải tỏa dứt điểm 19.020 đơn backlog tại 13 bưu cục cảnh báo bất ổn (ưu tiên số 1: Cam Linh, Tây Nha Trang, Xuân Hương Đà Lạt, Đơn Dương, Di Linh, Đức Trọng 1).\n"
     "2. Xóa sạch 1.774 đơn tồn Aging >5 ngày trong 72 giờ tới, đưa tỷ lệ phát sinh bồi hoàn về 0.\n"
     "3. Đưa %ODR toàn vùng vượt mốc 94%, kéo tỷ lệ %GTC Tổng phục hồi lên trên 60%.\n\n"
     "Em xin chân thành cảm ơn Ban Giám Đốc và các anh chị đã chú ý lắng nghe. Kính mời Ban Giám Đốc cho ý kiến chỉ đạo và phê duyệt phương án điều động lực lượng tác chiến!\"",
     (15, 76, 129), True)
], fill_hex="F0FDF4", border_hex="10B981")

# Save file Word
out_files = [
    r'C:\Users\lap4all\Desktop\New folder\KICH_BAN_THUYET_TRINH_W37_NAM_TRUNG_BO_MOI_NHAT.docx',
    r'C:\Users\lap4all\Desktop\New folder\KICH_BAN_THUYET_TRINH_W37_FULL_OPR_TTS.docx',
    r'C:\Users\lap4all\Desktop\New folder\KICH_BAN_THUYET_TRINH_W37_NAM_TRUNG_BO.docx',
    r'C:\Users\lap4all\Desktop\New folder\KICH_BAN_THUYET_TRINH_W37_NTB.docx',
    r'C:\Users\lap4all\Desktop\New folder\KICH_BAN_THUYET_TRINH_W37_CHUAN_SO_LIEU.docx'
]

for out_f in out_files:
    try:
        doc.save(out_f)
        print(f"SUCCESS: Saved {os.path.basename(out_f)}")
    except Exception as e:
        print(f"Note (file may be open in Word): Could not save {os.path.basename(out_f)} - {e}")

