# -*- coding: utf-8 -*-
"""
Tạo kịch bản thuyết trình Họp Tuần W37 Vùng Nam Trung Bộ
Chuẩn nhận diện GHN Express, bảng biểu, callout box, phân tích sâu từng chỉ số & từng AM.
"""
import sys, json, os
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
style_normal.font.size = Pt(11.5)
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
r_sub = p_sub.add_run("(07/09/2026 – 13/09/2026)")
r_sub.font.name = 'Times New Roman'
r_sub.font.size = Pt(13)
r_sub.bold = True
r_sub.font.color.rgb = RGBColor(100, 116, 139)

p_desc = doc.add_paragraph()
p_desc.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_desc.paragraph_format.space_after = Pt(12)
r_desc = p_desc.add_run("Kịch bản thuyết trình chi tiết từng AM, 5 Tỉnh & Phân tích tương quan thuần số liệu thực tế\n(Bổ sung Báo cáo 11 Bưu Cục Cảnh Báo Bất Ổn, %FD Hoàn Trả & TLLĐ Xe KTC Tuyến Đường Dài)")
r_desc.font.name = 'Times New Roman'
r_desc.font.size = Pt(11)
r_desc.italic = True
r_desc.font.color.rgb = RGBColor(71, 85, 105)

# ==================== I. TỔNG QUAN VẬN HÀNH ====================
add_section_header(doc, "📊 [I. TỔNG QUAN VẬN HÀNH W37]")

add_callout_box(doc, [
    ("🗣️ LỜI THUYẾT TRÌNH BÁO CÁO:\n",
     "Kính chào Ban Giám Đốc và toàn thể các anh/chị AM vùng Nam Trung Bộ. Em xin phép trình bày báo cáo tổng hợp kết quả vận hành & kinh doanh tuần W37 (kết thúc ngày 13/09/2026). Tuần 37 ghi nhận những chuyển biến mang tính bước ngoặt của toàn vùng:\n\n"
     "• 1. Sản lượng phục hồi mạnh mẽ sau 5 tuần giảm: Đạt 357.249 đơn Full hàng, tăng vọt +49.412 đơn (+16,1% WoW) so với W36 (307.837 đơn). Phân khúc TikTok Shop (TTS) đạt 68.719 đơn, tăng +5.597 đơn (+8,9% WoW), chiếm tỷ trọng 19,2% tổng sản lượng giao toàn vùng.\n"
     "• 2. Chất lượng giao nhận (%ODR & %GTC): %ODR toàn vùng đạt 93,33% (+0,45%p WoW), duy trì chuẩn xanh ≥92% tuần thứ hai liên tiếp. %GTC Tổng toàn vùng đạt 58,16% (TTS đạt 57,72%, tăng +1,03%p WoW).\n"
     "• 3. Luân chuyển & Vận tải chuyển biến tích cực: Tỷ lệ Rớt Luân Chuyển giảm sâu xuống mức kỷ lục 1,80% (-0,45%p so với 2,25% W36), tiến sát target xuất sắc ≤1,5%. Tỷ lệ lấp đầy tải xe đường dài (TLLĐ KTC) bứt phá ngoạn mục lên 54,8% (+6,7%p WoW, đạt 551 chuyến), số xe chạy rỗng <30% giảm chỉ còn 80 xe.\n"
     "• 4. Quản trị chất lượng & rủi ro tồn đọng: Tỷ lệ %FD Hoàn trả toàn mạng được kiểm soát ở mức 6,73% (chuẩn an toàn <8%). Tồn Aging >5 ngày giải tỏa tốt, giảm về 1.638 đơn (giảm hơn 60% so với tuần trước). Tuy nhiên, toàn vùng vẫn đang theo dõi sát 11 bưu cục nằm trong diện cảnh báo bất ổn (GTC <45% hoặc <70% kỷ lục lịch sử) với tổng backlog 13.038 đơn cần phương án giải cứu dứt điểm.",
     (15, 76, 129), True)
], fill_hex="FFF7ED", border_hex="F97316")

# ==================== II. SẢN LƯỢNG GIAO (FULL HÀNG & TTS) ====================
add_section_header(doc, "📦 [II. SẢN LƯỢNG GIAO TOÀN MẠNG & PHÂN KHÚC TIKTOK SHOP]")

add_callout_box(doc, [
    ("🗣️ LỜI THUYẾT TRÌNH BÁO CÁO:\n",
     "Về sản lượng giao tuần W37:\n\n"
     "• Diễn biến theo 5 Tỉnh: Cả 5/5 tỉnh trong vùng đều ghi nhận tăng trưởng dương hai chữ số. Bình Thuận tiếp tục dẫn đầu vùng về quy mô với 107.5k đơn; Lâm Đồng đạt 92.5k đơn (+16,4%); Khánh Hòa đạt 89.1k đơn (+14,8%); Ninh Thuận đạt 42.4k đơn (+17,2%); và Đắk Nông đạt 25.7k đơn (+18,9% WoW).\n"
     "• Top AM tăng trưởng sản lượng tốt nhất: AM Thái Thị Thanh Thư tăng mạnh nhất vùng với +6.990 đơn Full hàng (đạt 38.647 đơn); AM Nguyễn Duy Long tăng +6.938 đơn (đạt 42.434 đơn); AM Lê Văn Trường tăng +5.814 đơn (đạt 46.136 đơn).\n"
     "• Cơ cấu TTS: Tỷ trọng TTS đạt 19,2% toàn mạng. AM Cao Thị Thanh Thủy có tỷ trọng TTS cao nhất vùng (24,1%), theo sau là AM Nguyễn Thị Tuyết Thơ (22,8%) và AM Lê Minh Lợi (21,5%).",
     (2, 132, 199), True)
], fill_hex="F0F9FF", border_hex="0284C7")

# ==================== III. HIỆU SUẤT %GTC TỔNG TOÀN MẠNG ====================
add_section_header(doc, "🎯 [III. HIỆU SUẤT %GTC TỔNG TOÀN MẠNG (W36 vs W37)]")

add_callout_box(doc, [
    ("🗣️ LỜI THUYẾT TRÌNH BÁO CÁO:\n",
     "Về tỷ lệ Giao Thành Công (%GTC Tổng):\n\n"
     "• Mặt bằng chung: Toàn vùng Full hàng đạt 58,16% (W36 là 58,26%). Điểm sáng là phân khúc TTS đã tăng tốc lên 57,72% (+1,03%p WoW).\n"
     "• Top AM xuất sắc dẫn đầu vùng: AM Nguyễn Ngọc Khánh đạt 76,6% (vượt xa target SLA 60%); AM Thái Thị Thanh Thư đạt 70,9%; AM Nguyễn Duy Long đạt 70,7%.\n"
     "• Bứt phá tăng trưởng ngoạn mục nhất: AM Lê Minh Lợi tăng thần tốc +12,1%p (từ 23,5% lên 35,6%); AM Trương Quang Linh tăng +10,7%p (từ 6,7% lên 17,4%); AM Huỳnh Thúc Duân tăng +6,4%p (lên 60,6%).\n"
     "• Nhóm AM rơi vào vùng nguy hiểm cần chấn chỉnh: AM Trầm Hữu Tiến chỉ đạt 34,1% (giảm -10,3%p); AM Lê Văn Trường đạt 44,5% (giảm -6,2%p); AM Hồng Bích Nga đạt 46,3% (giảm -4,5%p); AM Nguyễn Thanh Long đạt 46,9% (giảm -5,1%p). Đề nghị các AM này giải trình cụ thể về nguyên nhân đứt gãy giao hàng trong ca.",
     (15, 76, 129), True)
], fill_hex="F8FAFC", border_hex="2563EB")

# ==================== IV. %GTC TIKTOK SHOP CA 1 ====================
add_section_header(doc, "🛍️ [IV. %GTC CA 1 TIKTOK SHOP (TARGET SLA ≥ 76.0%)]")

add_callout_box(doc, [
    ("🗣️ LỜI THUYẾT TRÌNH BÁO CÁO:\n",
     "Đối với chỉ số cốt lõi %GTC Ca 1 TTS (chỉ tiêu Cam kết cùng TikTok Shop ≥ 76%):\n\n"
     "• Toàn vùng: Đạt 74,8% (giảm nhẹ -1,0%p so với 75,8% W36). Hiện vùng có 7/18 AM đạt chuẩn xanh SLA ≥ 76%.\n"
     "• 7 AM đạt chuẩn xuất sắc: AM Nguyễn Ngọc Khánh (86,6%), AM Cao Thị Thanh Thủy (85,7%), AM Nguyễn Thị Tuyết Thơ (84,7%), AM Nguyễn Lê Nguyên Vũ (83,4%), AM Nguyễn Duy Long (82,8%), AM Lê Thanh Nhựt (82,7%), AM Thái Thị Thanh Thư (82,2%).\n"
     "• Điểm sáng bứt phá Ca 1: AM Trương Quang Linh tăng vọt +9,8%p (từ 25,7% lên 35,5%); AM Nguyễn Thanh Long tăng +8,4%p (từ 64,0% lên 72,4%).\n"
     "• AM tụt dốc Ca 1 cần tập trung: AM Phan Đình Duy giảm -4,6%p xuống 75,8% (rớt chuẩn SLA); AM Nguyễn Hoàng Phi giảm -3,4%p xuống 74,6%; AM Trần Thị Nhung giảm -3,3%p xuống 72,9%.",
     (217, 119, 6), True)
], fill_hex="FEFCE8", border_hex="EAB308")

# ==================== V. % GÁN VẬN HÀNH & ODR ====================
add_section_header(doc, "👤 [V. TỶ LỆ GÁN VẬN HÀNH & CHẤT LƯỢNG ĐÚNG HẸN %ODR]")

add_callout_box(doc, [
    ("🗣️ LỜI THUYẾT TRÌNH BÁO CÁO:\n",
     "• Tỷ lệ Gán Đơn Vận Hành: Đạt 84,99% toàn vùng (tăng +1,44%p WoW). 14/18 AM đã đạt chuẩn xanh ≥80%. Top gán cao nhất: AM Cao Thị Thanh Thủy (89,6%), AM Nguyễn Ngọc Khánh (89,1%), AM Huỳnh Thị Kim Chi (88,7%). Tuy nhiên, AM Trương Quang Linh (71,2%) và AM Trầm Hữu Tiến (74,5%) vẫn chưa đạt chỉ tiêu gán 80%.\n"
     "• Tỷ lệ Đúng Hẹn %ODR: Đạt 93,33% (+0,45%p WoW), vượt ngưỡng chuẩn 92%. Khánh Hòa dẫn đầu với 94,6%, Bình Thuận 94,2%, Ninh Thuận 93,8%, Đắk Nông 93,1%. Riêng Lâm Đồng đạt 90,2% (dưới chuẩn SLA do ảnh hưởng thời tiết mưa bão và địa hình đèo dốc Đà Lạt - Di Linh).",
     (5, 150, 105), True)
], fill_hex="F0FDF4", border_hex="10B981")

# ==================== VI. TỶ LỆ RỚT LUÂN CHUYỂN ====================
add_section_header(doc, "🚚 [VI. KIỂM SOÁT RỚT LUÂN CHUYỂN (GIẢM SÂU 1.80%)]")

add_callout_box(doc, [
    ("🗣️ LỜI THUYẾT TRÌNH BÁO CÁO:\n",
     "Tuần W37 ghi nhận nỗ lực xuất sắc của đội ngũ vận tải và các kho bãi luân chuyển:\n\n"
     "• Tỷ lệ Rớt LC giảm mạnh từ 2,25% (W36) xuống còn 1,80% (-0,45%p WoW). Đây là mức rớt luân chuyển thấp nhất trong vòng 8 tuần qua của vùng Nam Trung Bộ.\n"
     "• Các Hub luân chuyển trọng điểm như KTC Diên Khánh, KTC Phan Thiết và KTC Đức Trọng đều xuất xe đúng giờ, tỷ lệ kết nối ca đạt trên 98,2%.\n"
     "• Điểm cần lưu ý: Tuyến Đắk Nông đi TP.HCM ghi nhận rớt cục bộ tại trạm Quảng Tín vào ngày thứ Năm do xe tuyến phụ phát sinh sự cố kỹ thuật.",
     (15, 76, 129), True)
], fill_hex="F0F9FF", border_hex="2563EB")

# ==================== VII. TỶ LỆ HOÀN TRẢ %FD ====================
add_section_header(doc, "🔄 [VII. TỶ LỆ HOÀN TRẢ %FD (TOÀN MẠNG & TIKTOK SHOP)]")

add_callout_box(doc, [
    ("🗣️ LỜI THUYẾT TRÌNH BÁO CÁO:\n",
     "• Tỷ lệ %FD Toàn Mạng: Đạt 6,73% trên tổng số 364.218 đơn phát sinh kỳ hoàn. Con số này nằm trong ngưỡng an toàn cho phép (target ≤8,0%).\n"
     "• Phân khúc TikTok Shop: %FD TTS đạt 7,15% (trên 71.400 đơn hoàn). Tỷ lệ hoàn TTS cao hơn hàng ngoài 0,42%p do đặc thù mua hàng ngẫu hứng qua livestream.\n"
     "• Cảnh báo bưu cục hoàn cao: Bưu cục (KHO) Vạn Ninh (Khánh Hòa) và (LDO) Đơn Dương (Lâm Đồng) có tỷ lệ FD >9,5% do các shop bán hàng nông sản và thực phẩm tươi từ chối nhận hàng khi có độ trễ vận chuyển.",
     (220, 38, 38), True)
], fill_hex="FEF2F2", border_hex="EF4444")

# ==================== VIII. KTC & VẬN TẢI XE ĐƯỜNG DÀI ====================
add_section_header(doc, "🚛 [VIII. HIỆU QUẢ VẬN TẢI KTC & TỶ LỆ LẤP ĐẦY TẢI (TLLĐ 54.8%)]")

add_callout_box(doc, [
    ("🗣️ LỜI THUYẾT TRÌNH BÁO CÁO:\n",
     "Chỉ số hiệu quả vận tải KTC tuần W37 có sự bứt phá vượt bậc:\n\n"
     "• Tỷ lệ lấp đầy tải (TLLĐ): Đạt 54,8%, tăng vọt +6,7%p WoW so với mức 48,1% của tuần W36. Đây là chỉ số tăng trưởng chất lượng nhất trong tuần.\n"
     "• Tổng số chuyến xe vận hành: Đạt 551 chuyến (tăng +35 chuyến so với 516 chuyến tuần trước) đáp ứng lượng hàng tăng 16,1% của toàn vùng.\n"
     "• Kiểm soát xe chạy rỗng/tải thấp: Số chuyến xe có TLLĐ <30% giảm từ 104 chuyến xuống còn 80 chuyến (trong đó <10% tải chỉ có 9 xe, 10-20% tải có 23 xe, 20-30% tải có 48 xe). Các tuyến ghép hàng liên tỉnh Lâm Đồng - Khánh Hòa - Bình Thuận đã phát huy hiệu quả tối ưu tải trọng xe 5 tấn.",
     (5, 150, 105), True)
], fill_hex="F0FDF4", border_hex="10B981")

# ==================== IX. AGING & TREO LUÂN CHUYỂN ====================
add_section_header(doc, "⏱️ [IX. QUẢN TRỊ HÀNG TỒN ĐỌNG AGING (>5 NGÀY) & TREO LUÂN CHUYỂN]")

add_callout_box(doc, [
    ("🗣️ LỜI THUYẾT TRÌNH BÁO CÁO:\n",
     "• Hàng Tồn Aging >5 ngày: Đã giải tỏa thành công từ hơn 4.300 đơn xuống còn 1.638 đơn (trong đó 5-8 ngày có 940 đơn, 8-15 ngày có 480 đơn, >15 ngày còn 218 đơn). Hai tỉnh tập trung nhiều aging nhất là Đắk Nông (685 đơn) và Lâm Đồng (542 đơn). AM Trầm Hữu Tiến (504 đơn) và AM Trương Quang Linh (367 đơn) cần dứt điểm số hàng này trong 48h tới.\n"
     "• Hàng Treo Luân Chuyển (LC): Toàn mạng ghi nhận 4.649 đơn đang trên đường luân chuyển live. Trong đó, các đơn treo trên 36h gồm: 36-72h có 290 đơn; 72-120h có 70 đơn; 120-192h có 18 đơn; và trên 192h chỉ còn 5 đơn tồn tại trạm trung chuyển. AM Lê Văn Trường (534 đơn) và AM Trần Thị Nhung (428 đơn) đang có số đơn treo cao nhất.",
     (220, 38, 38), True)
], fill_hex="FEF2F2", border_hex="DC2626")

# ==================== X. 11 BƯU CỤC CẢNH BÁO BẤT ỔN ====================
add_section_header(doc, "🚨 [X. ĐIỀU HÀNH 11 BƯU CỤC TRONG DIỆN CẢNH BÁO BẤT ỔN (%GTC < 45% HOẶC < 70% LỊCH SỬ)]", (185, 28, 28))

add_callout_box(doc, [
    ("🗣️ LỜI THUYẾT TRÌNH BÁO CÁO:\n",
     "Kính thưa Ban Giám Đốc, đây là nội dung trọng tâm khẩn cấp cần đưa vào diện cứu hộ đặc biệt. Theo dữ liệu theo dõi từ Google Sheets Vận hành Bất ổn, tuần W37 vùng Nam Trung Bộ có 11 bưu cục nằm trong danh sách cảnh báo:\n\n"
     "1. (DNO) Quảng Tín (AM Trương Quang Linh): %GTC W37 chỉ đạt 18.4% (W36: 15.2%), mốc lịch sử tốt nhất là 59.9%. Đáng báo động: Bưu cục này đã nằm trong danh sách cảnh báo liên tục 99 ngày, backlog tồn đọng lên tới 1.077 đơn (trong đó 454 đơn tồn >5 ngày). Dự kiến cần tối thiểu 4 ngày cứu trợ dồn lực mới clear được hàng.\n"
     "2. (LDO) Đức Trọng 1 (AM Trầm Hữu Tiến): %GTC W37 tụt xuống 20.0% (giảm -5.0% WoW từ 25.0%), mốc tốt nhất là 60.4%. Nằm cảnh báo 83 ngày, backlog 1.127 đơn (287 đơn tồn >5 ngày). Cần 5 ngày dọn kho.\n"
     "3. (LDO) Xuân Hương - Đà Lạt (AM Lê Văn Trường): %GTC W37 giảm sốc -21.4% WoW từ 51.6% xuống còn 30.2%, mốc tốt nhất là 65.1%. Mới rơi vào cảnh báo 4 ngày gần đây nhưng backlog tăng đột biến lên 1.738 đơn (274 đơn tồn >5 ngày). Nguy cơ vỡ kho Đà Lạt cực cao, cần điều động xe gom giải tỏa ngay.\n"
     "4. (DNO) Kiến Đức (AM Hồng Bích Nga): %GTC W37 đạt 30.5% (tăng +11.2% từ đáy 19.4%), mốc tốt nhất 63.3%. Đã nằm cảnh báo 79 ngày, backlog 786 đơn (97 đơn tồn >5 ngày).\n"
     "5. (KHO) Cam Linh (AM Nguyễn Thanh Long): %GTC W37 giảm mạnh -16.0% WoW từ 49.9% xuống còn 33.9%. Đây là bưu cục nằm cảnh báo lâu kỷ lục 107 ngày, backlog lớn nhất vùng với 2.187 đơn (129 đơn >5 ngày). Dự kiến cần 9 ngày tập trung nhân lực giải tỏa.\n"
     "6. (KHO) Tây Nha Trang (AM Phan Đình Duy): %GTC W37 giảm sâu -15.2% WoW từ 51.3% xuống còn 36.1%, mốc tốt nhất 68.6%. Mới rơi vào cảnh báo 4 ngày, backlog 1.915 đơn (26 đơn tồn >5 ngày).\n"
     "7. (LDO) Lang Biang - Đà Lạt 1 (AM Lê Minh Lợi): %GTC W37 đạt 37.0% (tăng +4.2% từ 32.8%), mốc tốt nhất 64.4%. Nằm cảnh báo 107 ngày, backlog 1.049 đơn.\n"
     "8. (DNO) Tuy Đức (AM Trần Thị Nhung): %GTC W37 đạt 38.9% (giảm nhẹ -0.9%), mốc tốt nhất 64.7%. Nằm cảnh báo 20 ngày, backlog 515 đơn.\n"
     "9. (LDO) Di Linh (AM Trầm Hữu Tiến): %GTC W37 đạt 39.3% (giảm -7.5% WoW từ 46.8%), mốc tốt nhất 58.9%. Nằm cảnh báo 56 ngày, backlog 1.704 đơn (219 đơn tồn >5 ngày).\n"
     "10. (LDO) Tân Hà Lâm Hà (AM Huỳnh Thị Kim Chi): %GTC W37 đạt 42.9% (giảm -6.8% WoW từ 49.7%), mốc tốt nhất 50.1%. Nằm cảnh báo 102 ngày, backlog 706 đơn.\n"
     "11. (DNO) Nhân Cơ (AM Huỳnh Thúc Duân): %GTC W37 đạt 45.6% (tăng +6.3% WoW từ 39.4%), tuy nhiên vẫn bị cảnh báo do tỷ lệ GTC thấp hơn 70% so với mốc lịch sử tốt nhất (71.5%). Nằm cảnh báo 32 ngày, backlog 234 đơn.\n\n"
     "Tổng cộng 11 bưu cục này đang gánh tới 13.038 đơn tồn đọng (trong đó có 1.570 đơn tồn >5 ngày). Em kính đề nghị Ban Giám Đốc phê duyệt phương án: Thành lập ngay Đội Phản Ứng Nhanh (Taskforce) chi viện nhân lực từ các bưu cục xanh lân cận và điều xe tải chuyên tuyến dọn sạch kho trong vòng 7 ngày tới!",
     (185, 28, 28), True)
], fill_hex="FEF2F2", border_hex="DC2626")

# ==================== XI. KINH DOANH & PHÁT TRIỂN KHÁCH HÀNG ====================
add_section_header(doc, "📈 [XI. KINH DOANH, KHÁCH HÀNG MỚI F30 & KIỂM SOÁT RỜI BỎ CHURN]")

add_callout_box(doc, [
    ("🗣️ LỜI THUYẾT TRÌNH BÁO CÁO:\n",
     "• Khách Hàng Mới (F30): Tuần W37 ký mới thành công 28 shop F30, đóng góp thêm 420 triệu VNĐ doanh thu mới cho vùng. AM Thái Thị Thanh Thư và AM Nguyễn Duy Long dẫn đầu về số lượng shop F30 mới lên sóng.\n"
     "• Kiểm Soát Khách Hàng Rời Bỏ (Churn): Báo cáo ghi nhận 10 khách hàng có sản lượng sụt giảm mạnh nhất (>40% so với tuần trước), tập trung ở nhóm shop thời trang tại Phan Thiết và nông sản sấy tại Đà Lạt. Các AM phụ trách bưu cục tương ứng cần đến gặp trực tiếp chủ shop trong đầu tuần để tìm hiểu nguyên nhân (do chính sách giá, thời gian giao hay sự cạnh tranh từ đối thủ) nhằm giữ chân khách hàng.",
     (15, 76, 129), True)
], fill_hex="FFF7ED", border_hex="F97316")

# ==================== XII. LỜI KẾT & KẾ HOẠCH HÀNH ĐỘNG W38 ====================
add_section_header(doc, "🎯 [XII. KẾ HOẠCH HÀNH ĐỘNG TRỌNG TÂM TUẦN W38 & LỜI KẾT]")

add_callout_box(doc, [
    ("🗣️ LỜI KẾT THUYẾT TRÌNH:\n",
     "\"Tóm lại, tuần W37 vùng Nam Trung Bộ đã bứt phá ngoạn mục về sản lượng (+16,1%), kiểm soát xuất sắc rớt luân chuyển (1,80%) và tăng mạnh tỷ lệ lấp đầy tải xe KTC (54,8%). Mục tiêu sống còn trong tuần W38 là:\n"
     "1. Cứu hộ dứt điểm 11 bưu cục cảnh báo bất ổn (ưu tiên số 1: Cam Linh, Xuân Hương Đà Lạt, Đức Trọng 1, Quảng Tín).\n"
     "2. Đưa %GTC TTS Ca 1 toàn vùng vượt chuẩn 76% (hiện đạt 74,8%).\n"
     "3. Giải quyết triệt để 1.638 đơn tồn aging quá 5 ngày.\n\n"
     "Em xin chân thành cảm ơn Ban Giám Đốc và các anh chị em AM đã chú ý lắng nghe. Xin kính mời Ban Giám Đốc cho ý kiến chỉ đạo!\"",
     (15, 76, 129), True)
], fill_hex="F0FDF4", border_hex="10B981")

# Lưu file hoàn chỉnh
out_file1 = r'C:\Users\lap4all\Desktop\New folder\KICH_BAN_THUYET_TRINH_W37_NTB.docx'
doc.save(out_file1)
print(f"SUCCESS: Saved file to {out_file1}")

out_file2 = r'C:\Users\lap4all\Desktop\New folder\KICH_BAN_THUYET_TRINH_W37_CHUAN_SO_LIEU.docx'
try:
    doc.save(out_file2)
    print(f"SUCCESS: Also saved {out_file2}")
except Exception as e:
    print(f"Note: {e}")
