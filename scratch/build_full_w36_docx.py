# -*- coding: utf-8 -*-
"""
Tạo kịch bản thuyết trình W36 dạng Word .docx chuẩn nhận diện,
sao chép đúng cấu trúc callout box, màu sắc, font chữ và số liệu W36 thực tế.
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
    """Tạo style Callout Box cho cell (border trái dày, nền nhạt, padding)"""
    tcPr = cell._tc.get_or_add_tcPr()
    
    # Border: chỉ có border trái
    borders_xml = f"""
    <w:tcBorders {nsdecls('w')}>
        <w:top w:val="none"/>
        <w:left w:val="single" w:sz="{border_size}" w:space="0" w:color="{border_hex}"/>
        <w:bottom w:val="none"/>
        <w:right w:val="none"/>
    </w:tcBorders>
    """
    tcPr.append(parse_xml(borders_xml))
    
    # Shading (màu nền)
    shd_xml = f'<w:shd {nsdecls("w")} w:val="clear" w:color="auto" w:fill="{fill_hex}"/>'
    tcPr.append(parse_xml(shd_xml))
    
    # Margins (padding)
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
    """
    paragraphs_data: danh sách các tuple/dict mô tả text trong box
    Format: list of (prefix_bold, text_italic/normal, is_bold)
    """
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.columns[0].width = Cm(16.6)
    
    cell = table.rows[0].cells[0]
    cell.width = Cm(16.6)
    set_cell_margins_and_border(cell, fill_hex, border_hex)
    
    # Paragraph đầu tiên đã có sẵn trong cell
    first_p = cell.paragraphs[0]
    
    for idx, item in enumerate(paragraphs_data):
        if idx == 0:
            p = first_p
        else:
            p = cell.add_paragraph()
        
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.18
        
        # Nếu item là string đơn giản
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
r_title = p_title.add_run("BÁO CÁO VẬN HÀNH & KINH DOANH TUẦN W36")
r_title.font.name = 'Times New Roman'
r_title.font.size = Pt(17)
r_title.bold = True
r_title.font.color.rgb = RGBColor(15, 76, 129) # Navy Blue

p_sub = doc.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_sub.paragraph_format.space_before = Pt(0)
p_sub.paragraph_format.space_after = Pt(6)
r_sub = p_sub.add_run("(31/08/2026 – 06/09/2026)")
r_sub.font.name = 'Times New Roman'
r_sub.font.size = Pt(13)
r_sub.bold = True
r_sub.font.color.rgb = RGBColor(100, 116, 139)

p_desc = doc.add_paragraph()
p_desc.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_desc.paragraph_format.space_after = Pt(12)
r_desc = p_desc.add_run("Kịch bản thuyết trình chi tiết từng AM & Phân tích tương quan thuần số liệu thực tế\n(Bổ sung Báo cáo %FD Hoàn Trả, KTC & Vận Tải Xe Tuyến Đường Dài)")
r_desc.font.name = 'Times New Roman'
r_desc.font.size = Pt(11)
r_desc.italic = True
r_desc.font.color.rgb = RGBColor(71, 85, 105)

# ==================== I. TỔNG QUAN VẬN HÀNH ====================
add_section_header(doc, "📊 [I. TỔNG QUAN VẬN HÀNH]")

add_callout_box(doc, [
    ("🗣️ LỜI THUYẾT TRÌNH BÁO CÁO:\n", 
     "Em chào Ban Giám Đốc và toàn thể anh/chị AM vùng Nam Trung Bộ. Đây là buổi họp weekly báo cáo kết quả vận hành & kinh doanh tuần W36 (từ 31/08 đến 06/09/2026). Để không mất nhiều thời gian, em xin phép đi thẳng vào số liệu tổng quan của vùng:\n\n"
     "• Sản lượng full hàng: Đạt 307.837 đơn, giảm -11.149 đơn (-3,5%) so với tuần W35 (318.986 đơn). Đây là tuần thứ 5 liên tiếp sản lượng vùng ghi nhận sụt giảm, từ đỉnh 374k đơn tại W33.\n"
     "• Sản lượng TTS: Đạt 63.122 đơn, giảm mạnh -9.759 đơn (-13,4%) so với tuần W35 (72.881 đơn). Sau khi đi ngang ở tuần 35, tuần này TTS sụt giảm đáng kể; tỷ trọng TTS hiện chiếm 20,5% tổng sản lượng giao toàn vùng.\n"
     "• Chất lượng vận hành có những điểm chuyển biến trái chiều:\n"
     "  - %GTC Full hàng tổng (Ca1+Ca2+Tồn): Đạt 58,1%, gần như đi ngang (-0,03%p so với 58,2% ở W35). Tuy nhiên, GTC Ca1+Tồn tăng lên 60,5% (+0,8%p), trong khi GTC Ca2 lại giảm mạnh -2,9%p xuống còn 48,4%.\n"
     "  - %ODR Full hàng: Đạt 92,9%, đảo chiều tăng phục hồi +0,7%p so với mức đáy 92,2% của W35.\n"
     "  - %LTC Full hàng: Đạt 90,5%, giảm nhẹ -0,6%p (W35: 91,1%). Riêng LTC TTS giảm mạnh -1,95%p xuống 94,2%.\n"
     "  - %Rớt Luân Chuyển: Đạt 2,25%, tăng mạnh +0,68%p so với 1,57% của W35 — rớt LC sau tuần chạm đáy đã bị dội ngược trở lại trên ngưỡng 2%.\n"
     "  - %Gán Vận Hành: Đạt 83,5%, tăng +1,4%p (Ca1+Tồn đạt 89,3%, tăng +2,8%p) — tín hiệu tích cực về việc đẩy hàng ra đường.\n"
     "  - %FD Hoàn Trả (Lần đầu đưa vào báo cáo tuần): Đạt 7,54% Full hàng (22.954 đơn hoàn) và 6,80% TTS (4.365 đơn hoàn).\n"
     "  - TLLĐ Thùng/Xe KTC (Mục mới): Bình quân toàn vùng đạt 48,1%, giảm -3,7%p so với W35 (51,8%), ghi nhận 112 chuyến xe dưới 30% tải.",
     (15, 76, 129), True)
], fill_hex="FFF7ED", border_hex="F97316")

add_callout_box(doc, [
    ("🔍 PHÂN TÍCH TỔNG QUAN TƯƠNG QUAN SỐ LIỆU:\n",
     "Tuần 36 ghi nhận sự cải thiện rõ ở khâu Giao đúng hẹn ODR (+0,7%) và Tỷ lệ Gán vận hành (+1,4%), cho thấy nỗ lực của các bưu cục trong việc đưa hàng đi phát sớm. "
     "Tuy nhiên, hai điểm nghẽn lớn nhất tuần này là: (1) Khâu phát Ca 2 sụt giảm mạnh (-2,9%p) kéo GTC tổng không bứt lên được; (2) Tỷ lệ Rớt luân chuyển bật tăng trở lại 2,25% kết hợp với TLLĐ xe vận tải giảm còn 48,1% (112 chuyến xe chạy rỗng/dưới 30% tải), gây lãng phí chi phí xe và dồn ứ đơn luân chuyển.",
     (180, 83, 9), False)
], fill_hex="FEF3C7", border_hex="D97706")

# ==================== II. SẢN LƯỢNG THEO TỈNH ====================
add_section_header(doc, "📍 [SẢN LƯỢNG THEO TỈNH]")

add_callout_box(doc, [
    ("🗣️ LỜI THUYẾT TRÌNH BÁO CÁO:\n",
     "Về sản lượng Full hàng theo 5 tỉnh:\n"
     "Tất cả 5 tỉnh trong vùng tuần W36 đều đồng loạt giảm sản lượng full hàng:\n"
     "• Lâm Đồng: Tiếp tục là tỉnh có sản lượng lớn nhất vùng và cũng là tỉnh giảm nhiều nhất với -3.987 đơn (từ 91.754 xuống 87.767 đơn), chiếm tới 35,8% tổng lượng giảm toàn vùng.\n"
     "• Khánh Hòa: Đứng thứ 2 về volume, giảm -2.723 đơn (từ 78.923 xuống 76.200 đơn).\n"
     "• Đắk Nông: Giảm -2.454 đơn (từ 35.534 xuống 33.080 đơn). Tuy đứng thứ 3 về số lượng giảm, nhưng Đắk Nông lại là tỉnh có tốc độ sụt giảm đơn sâu nhất vùng (mất tới -6,9% sản lượng của tỉnh).\n"
     "• Bình Thuận: Giảm -1.314 đơn (từ 81.721 xuống 80.407 đơn).\n"
     "• Ninh Thuận: Giảm ít nhất với -671 đơn (từ 31.054 xuống 30.383 đơn).\n\n"
     "Về sản lượng TTS: 100% cả 5 tỉnh đều sụt giảm nghiêm trọng:\n"
     "• Khánh Hòa giảm mạnh nhất: -3.261 đơn (từ 19.099 xuống 15.838 đơn, giảm -17,1%).\n"
     "• Lâm Đồng giảm -2.401 đơn (từ 19.999 xuống 17.598 đơn, giảm -12,0%).\n"
     "• Bình Thuận giảm -1.963 đơn (từ 17.212 xuống 15.249 đơn).\n"
     "• Ninh Thuận giảm -1.224 đơn (từ 7.694 xuống 6.470 đơn, giảm -15,9%).\n"
     "• Đắk Nông giảm -910 đơn (từ 8.877 xuống 7.967 đơn, giảm -10,3%).\n"
     "→ Đây là đợt sụt giảm đơn sàn TTS diện rộng toàn bộ 5 tỉnh, đề nghị khối Kinh doanh rà soát lại các chiến dịch khuyến mãi của sàn và top shop livestream để có phương án giữ sản lượng.",
     (15, 76, 129), True)
], fill_hex="FFF7ED", border_hex="F97316")

# ==================== III. SẢN LƯỢNG THEO AM ====================
add_section_header(doc, "👤 [SẢN LƯỢNG THEO AM]")

add_callout_box(doc, [
    ("🗣️ LỜI THUYẾT TRÌNH BÁO CÁO:\n",
     "Về sản lượng theo từng AM quản lý:\n"
     "• Sản lượng Full hàng: Chỉ có duy nhất 2 AM lội ngược dòng tăng sản lượng tuần này:\n"
     "  - Anh Nguyễn Lê Nguyên Vũ: Tăng +347 đơn (từ 13.374 lên 13.721 đơn).\n"
     "  - Chị Hồng Bích Nga: Tăng +201 đơn (từ 19.473 lên 19.674 đơn).\n"
     "  Toàn bộ 16 AM còn lại đều sụt giảm sản lượng. Trong đó giảm sâu nhất là:\n"
     "  - Anh Lê Văn Trường: Giảm nhiều nhất vùng với -2.709 đơn (từ 28.113 xuống 25.404 đơn).\n"
     "  - Anh Phan Đình Duy: Giảm -1.514 đơn (từ 20.973 xuống 19.459 đơn).\n"
     "  - Chị Trần Thị Nhung: Giảm -1.331 đơn (từ 24.736 xuống 23.405 đơn).\n\n"
     "• Sản lượng TTS: Không có AM nào tăng trưởng dương trong tuần 36. Các AM giảm sâu nhất:\n"
     "  - Anh Nguyễn Duy Long: Giảm mạnh nhất vùng với -1.600 đơn (từ 9.656 xuống 8.056 đơn, giảm -16,6%).\n"
     "  - Anh Phan Đình Duy: Giảm -1.073 đơn (từ 5.270 xuống 4.197 đơn, giảm -20,4%).\n"
     "  - Anh Lê Văn Trường: Giảm -1.065 đơn (từ 5.552 xuống 4.487 đơn, giảm -19,2%).\n"
     "  - Anh Lê Thanh Nhựt và Chị Thái Thị Thanh Thư cũng giảm trên 800 đơn TTS.\n"
     "  Điểm đỡ sụt tốt nhất: Anh Nguyễn Lê Nguyên Vũ chỉ giảm nhẹ -59 đơn, anh Lê Minh Lợi giảm -101 đơn, anh Trương Quang Linh giảm -130 đơn.",
     (15, 76, 129), True)
], fill_hex="FFF7ED", border_hex="F97316")

# ==================== IV. GTC TỔNG & PHÂN THEO AM ====================
add_section_header(doc, "📊 [GTC TỔNG & PHÂN THEO AM (FULL HÀNG & TTS)]")

add_callout_box(doc, [
    ("🗣️ LỜI THUYẾT TRÌNH BÁO CÁO:\n",
     "Về %GTC tuần W36:\n"
     "GTC Full hàng toàn vùng đạt 58,1% (Ca1+Tồn đạt 60,5%, tăng +0,8%p; nhưng Ca2 tụt xuống 48,4%, giảm -2,9%p).\n\n"
     "• Top AM cải thiện GTC Full hàng xuất sắc nhất tuần:\n"
     "  - Anh Nguyễn Thanh Long: Bứt phá mạnh nhất vùng, tăng vọt +10,2%p từ 46,9% lên 57,1% — đây là sự phục hồi rất ấn tượng sau tuần 35 khó khăn.\n"
     "  - Chị Hồng Bích Nga: Tăng +4,5%p từ 46,3% lên 50,8%, vượt mốc 50%.\n"
     "  - Anh Lê Văn Trường: Tăng +3,5%p từ 44,5% lên 48,0%.\n"
     "  - Chị Nguyễn Thị Tuyết Thơ: Tăng +3,1%p từ 67,4% lên 70,4% (thuộc nhóm dẫn đầu vùng).\n\n"
     "• Ngược lại, Top AM giảm GTC mạnh nhất cần lưu ý đặc biệt:\n"
     "  - Anh Huỳnh Thúc Duân: Giảm sâu nhất vùng, sụt -6,2%p từ 47,9% xuống 41,6% — cần anh Duân giải trình nguyên nhân.\n"
     "  - Anh Phan Đình Duy: Giảm -5,2%p từ 64,0% xuống 58,8%.\n"
     "  - Anh Nguyễn Ngọc Khánh: Giảm -5,0%p từ 76,6% xuống 71,6% (dù vẫn ở mức cao).\n"
     "  - Anh Nguyễn Hoàng Phi: Giảm -3,7%p từ 64,7% xuống 61,0%.\n"
     "  - Anh Trầm Hữu Tiến: Tiếp tục giảm -2,4%p xuống 31,7% (W35 là 34,1%) — mức GTC thấp thứ 2 toàn vùng.\n"
     "  - Anh Trương Quang Linh: Vẫn duy trì mức rất thấp 15,3% (giảm thêm -2,1%p) — cần phương án can thiệp đặc biệt tại địa bàn anh Linh phụ trách.",
     (15, 76, 129), True)
], fill_hex="FFF7ED", border_hex="F97316")

# ==================== V. GTC CA 1 TTS ====================
add_section_header(doc, "⭐ [GTC CA 1 TTS — CHỈ SỐ CÔNG TY QUAN TÂM]")

add_callout_box(doc, [
    ("🗣️ LỜI THUYẾT TRÌNH BÁO CÁO:\n",
     "GTC Ca 1 TTS tuần W36:\n"
     "• GTC Ca 1 thuần TTS đạt 74,78%, giảm -1,04%p so với tuần W35 (75,82%). Đây là chỉ số trọng yếu Công ty đang theo dõi sát hàng ngày, hiện vùng NTB đã bị rơi xuống dưới ngưỡng chuẩn 75%.\n"
     "• GTC Ca 1 + Tồn TTS đạt 89,02%, tăng +2,10%p (W35: 86,92%) — cho thấy việc dồn lực xử lý đơn tồn ca sáng làm khá tốt, nhưng việc giao dứt điểm đơn phát sinh mới trong Ca 1 thuần bị chậm lại.\n"
     "• Đánh giá theo khu vực: Một số kho bưu cục giao trễ buổi sáng, dẫn đến dồn toa sang Ca 2, làm Ca 2 bị quá tải và tỷ lệ phát thành công Ca 2 tụt dốc (GTC Ca2 TTS chỉ đạt 46,5%, giảm -3,2%p).",
     (15, 76, 129), True)
], fill_hex="FFF7ED", border_hex="F97316")

# ==================== VI. TỶ LỆ GÁN VẬN HÀNH ====================
add_section_header(doc, "📋 [TỶ LỆ GÁN VẬN HÀNH]")

add_callout_box(doc, [
    ("🗣️ LỜI THUYẾT TRÌNH BÁO CÁO:\n",
     "Tỷ lệ Gán vận hành tuần W36 ghi nhận sự khởi sắc rất đáng khích lệ:\n"
     "• Gán Full hàng tổng (Ca1+Ca2+Tồn): Đạt 83,55%, tăng +1,44%p so với W35 (82,11%).\n"
     "• Gán Full hàng Ca 1 + Tồn: Tăng bứt phá +2,76%p lên 89,30% (W35: 86,53%) — đây là mức cao nhất trong 5 tuần qua.\n"
     "• Gán TTS tổng: Đạt 83,43%, tăng +1,12%p (W35: 82,31%); Gán TTS Ca 1 + Tồn đạt 89,02% (+2,10%p).\n"
     "• Tuy nhiên, Gán Ca 2 giảm nhẹ -2,21%p xuống 60,21% (TTS Ca 2 giảm -2,33%p xuống 57,69%).\n"
     "→ Kết luận: Các bưu cục đã chủ động gán hàng cho bưu tá đi phát rất sớm ngay từ đầu giờ sáng. Vấn đề còn lại là khâu giám sát trên đường để chuyển hóa tỷ lệ gán thành tỷ lệ giao thành công thực tế.",
     (15, 76, 129), True)
], fill_hex="FFF7ED", border_hex="F97316")

# ==================== VII. ODR GIAO ĐÚNG HẸN ====================
add_section_header(doc, "⏱️ [ODR — TỶ LỆ GIAO ĐÚNG HẸN SLA]")

add_callout_box(doc, [
    ("🗣️ LỜI THUYẾT TRÌNH BÁO CÁO:\n",
     "Chỉ số ODR Full hàng tuần W36 đạt 92,88%, tăng phục hồi +0,71%p so với tuần đáy W35 (92,18%):\n"
     "• Theo tỉnh: Đắk Nông cải thiện mạnh mẽ nhất, tăng +2,9%p lên 89,1% (dù vẫn thấp nhất vùng nhưng đã thoát khỏi vùng báo động đỏ <87%). Lâm Đồng tăng +0,9%p lên 89,5%. Bình Thuận tăng +0,6%p đạt 96,4% (cao nhất vùng). Khánh Hòa 94,1% (-0,5%p) và Ninh Thuận 96,0% (-0,2%p) giảm nhẹ nhưng vẫn ở ngưỡng an toàn SLA.\n\n"
     "• Theo AM — Những điểm sáng phục hồi ấn tượng:\n"
     "  - Anh Trương Quang Linh: Tăng trưởng bứt phá ngoạn mục nhất, tăng vọt +20,3%p từ mức đáy 40,1% lên 60,4% — đây là nỗ lực chấn chỉnh kỷ luật phát hàng rất đáng biểu dương sau khi nhận cảnh báo tuần trước.\n"
     "  - Anh Lê Minh Lợi: Tiếp tục đà tăng xuất sắc, tăng +12,5%p từ 58,5% lên 71,0%.\n"
     "  - Anh Nguyễn Thanh Long tăng +3,0%p lên 90,3%; Chị Hồng Bích Nga tăng +2,3%p lên 91,7%.\n\n"
     "• Tuy nhiên, AM giảm ODR cần lưu ý:\n"
     "  - Anh Trầm Hữu Tiến: Giảm mạnh nhất vùng, sụt -3,9%p từ 79,5% xuống còn 75,6% — rơi xuống vị trí thấp nhất vùng trong nhóm AM kỳ cựu. Yêu cầu anh Tiến báo cáo nguyên nhân và kế hoạch đưa ODR lên ≥82% trong W37.\n"
     "  - Chị Thái Thị Thanh Thư (-1,4%p), Anh Nguyễn Hoàng Phi (-1,2%p), Anh Phan Đình Duy (-0,9%p) giảm nhẹ.",
     (15, 76, 129), True)
], fill_hex="FFF7ED", border_hex="F97316")

# ==================== VIII. CHỈ SỐ LTC ====================
add_section_header(doc, "📦 [CHỈ SỐ %LTC — LẤY THÀNH CÔNG]")

add_callout_box(doc, [
    ("🗣️ LỜI THUYẾT TRÌNH BÁO CÁO:\n",
     "LTC Full hàng toàn vùng W36 đạt 90,50%, giảm nhẹ -0,64%p so với W35 (91,14%). LTC TTS đạt 94,19%, giảm -1,95%p:\n"
     "• Theo AM cải thiện tốt: Anh Nguyễn Lê Nguyên Vũ tăng +4,6%p lên 96,4% (dẫn đầu vùng); anh Trương Quang Linh tăng +2,6%p lên 56,5%; anh Lê Văn Trường tăng +2,0%p lên 89,9%.\n"
     "• Ngược lại, các AM sụt giảm LTC đột biến cần giải trình khẩn cấp:\n"
     "  - Anh Nguyễn Ngọc Khánh: Giảm sốc nhất toàn vùng, rơi tự do -11,1%p từ 91,1% xuống chỉ còn 80,0% — đây là mức giảm bất thường nhất trong tuần.\n"
     "  - Chị Nguyễn Thị Tuyết Thơ: Giảm mạnh -6,8%p từ 92,2% xuống 85,5%.\n"
     "  - Anh Huỳnh Thúc Duân (-3,6%p xuống 89,9%) và Anh Nguyễn Hoàng Phi (-3,3%p xuống 89,6%).\n"
     "→ Yêu cầu anh Khánh và chị Thơ làm việc ngay với các bưu tá phụ trách tuyến lấy, kiểm tra tình trạng hủy lấy do shop hay do bưu tá không đến đúng hẹn.",
     (15, 76, 129), True)
], fill_hex="FFF7ED", border_hex="F97316")

# ==================== IX. OPR TTS THEO KHUNG GIỜ ====================
add_section_header(doc, "⏰ [OPR TTS THEO KHUNG GIỜ]")

add_callout_box(doc, [
    ("🗣️ LỜI THUYẾT TRÌNH BÁO CÁO:\n",
     "Về OPR TTS theo khung giờ:\n"
     "• Tiến độ luân chuyển và xử lý đơn TTS giữa các khung giờ ngày và đêm tại các bưu cục tiếp tục có sự chênh lệch lớn.\n"
     "• Khung giờ lấy hàng buổi chiều và gom đơn đêm ra trục xe tuyến ở một số kho vệ tinh còn chậm, khiến đơn TTS bị dồn sang sáng hôm sau, ảnh hưởng trực tiếp đến chỉ tiêu GTC Ca 1 của ngày N+1.\n"
     "• Yêu cầu các AM bám sát lịch trình xe trung chuyển KTC/KCT để đảm bảo 100% đơn gom trong ngày được bắn xuất trước 21h00.",
     (15, 76, 129), True)
], fill_hex="FFF7ED", border_hex="F97316")

# ==================== X. RỚT LUÂN CHUYỂN ====================
add_section_header(doc, "🚛 [RỚT LUÂN CHUYỂN — %RỚT LC TOÀN VÙNG]")

add_callout_box(doc, [
    ("🗣️ LỜI THUYẾT TRÌNH BÁO CÁO:\n",
     "Chỉ số Rớt luân chuyển tuần W36 ghi nhận diễn biến bất lợi:\n"
     "• Tỷ lệ rớt LC toàn vùng tăng vọt lên 2,25% (tăng +0,68%p so với 1,57% ở W35), phá vỡ kỷ lục đáy vừa thiết lập ở tuần trước.\n"
     "• Top AM có tỷ lệ rớt LC cao nhất vùng:\n"
     "  - Anh Lê Minh Lợi: Ghi nhận 100% (cần kiểm tra xác minh ngay số liệu phát sinh do mã bưu cục hay lỗi quét mã).\n"
     "  - Chị Trần Thị Nhung: Rớt 24,80% — mức rất cao, kéo tụt chỉ số chung của khu vực Bình Thuận.\n"
     "  - Anh Huỳnh Thúc Duân: Rớt 15,28%.\n"
     "  - Anh Trầm Hữu Tiến: Rớt 6,67%.\n"
     "  - Chị Hồng Bích Nga: Rớt 5,81%.\n"
     "→ Toàn bộ các AM có tỷ lệ rớt luân chuyển >3% phải rà soát ngay quy trình niêm phong túi kiện và giờ chốt xe tải.",
     (15, 76, 129), True)
], fill_hex="FFF7ED", border_hex="F97316")

# ==================== XI. BÁO CÁO FD HOÀN TRẢ (MỤC MỚI) ====================
add_section_header(doc, "🔄 [BÁO CÁO %FD — TỶ LỆ HOÀN TRẢ & GIAO THẤT BẠI (MỤC MỚI)]", color_rgb=(147, 51, 234))

add_callout_box(doc, [
    ("🗣️ LỜI THUYẾT TRÌNH BÁO CÁO:\n",
     "Kính thưa Ban Giám Đốc, bắt đầu từ tuần W36, khối Vận hành chính thức đưa Báo Cáo Chuyên Sâu Về Chỉ Số %FD (Failed Delivery — Tỷ lệ giao thất bại dẫn đến hoàn trả) vào chương trình họp tuần.\n\n"
     "1️⃣ TỔNG QUAN %FD TOÀN VÙNG NAM TRUNG BỘ TUẦN W36:\n"
     "• FD Full hàng: Đạt 7,54% — trong tổng số 304.308 đơn giao toàn vùng, có tới 22.954 đơn bị hoàn trả.\n"
     "• FD TTS: Đạt 6,80% — trong 64.220 đơn TTS phát, có 4.365 đơn hoàn trả.\n\n"
     "2️⃣ ĐIỂM DANH TOP 10 BƯU CỤC CÓ TỶ LỆ %FD CAO NHẤT VÙNG (ĐIỂM NÓNG CẦN CAN THIỆP):\n"
     "🔴 1. BC (DNO) Kiến Đức — AM Hồng Bích Nga: FD lên tới 43,70% (1.422 đơn hoàn / 3.254 đơn giao) — Đây là điểm nóng nghiêm trọng nhất toàn vùng, một mình bưu cục Kiến Đức chiếm tới 6,2% tổng số đơn hoàn của toàn vùng NTB!\n"
     "🔴 2. BC (DNO) Quảng Tín — AM Trương Quang Linh: FD đạt 28,82% (573 đơn hoàn / 1.988 đơn giao), chiếm 2,5% tổng đơn hoàn vùng.\n"
     "🔴 3. BC (LDO) Lang Biang - Đà Lạt 1 — AM Lê Minh Lợi: FD đạt 17,53% (490 đơn hoàn / 2.795 đơn giao).\n"
     "🔴 4. BC (KHO) Cam Linh — AM Nguyễn Thanh Long: FD đạt 15,75% (910 đơn hoàn / 5.779 đơn giao) — volume giao lớn nên số đơn hoàn lên tới gần 1.000 đơn (chiếm 4,0% đơn hoàn vùng).\n"
     "🟡 5. BC (DNO) Tuy Đức — AM Trần Thị Nhung: FD đạt 13,25% (236 đơn hoàn / 1.781 đơn giao).\n"
     "🟡 6. BC (DNO) Đông Gia Nghĩa — AM Huỳnh Thúc Duân: FD đạt 13,24% (317 đơn hoàn / 2.395 đơn giao).\n"
     "🟡 7. BC (DNO) Nhân Cơ — AM Huỳnh Thúc Duân: FD đạt 12,60% (141 đơn hoàn / 1.119 đơn giao).\n"
     "🟡 8. BC (LDO) Đức Trọng 1 — AM Trầm Hữu Tiến: FD đạt 11,74% (243 đơn hoàn / 2.069 đơn giao).\n"
     "🟡 9. BC (KHO) Nha Trang — AM Phan Đình Duy: FD đạt 11,70% (375 đơn hoàn / 3.204 đơn giao).\n"
     "🟡 10. BC (DNO) Quảng Khê — AM Trần Thị Nhung: FD đạt 11,40% (161 đơn hoàn / 1.412 đơn giao).\n\n"
     "3️⃣ CHỈ ĐẠO VÀ HÀNH ĐỘNG:\n"
     "Đắk Nông có tới 5 bưu cục nằm trong Top 10 FD cao nhất. Đề nghị các AM Hồng Bích Nga (Kiến Đức), Trương Quang Linh (Quảng Tín) và Nguyễn Thanh Long (Cam Linh) thành lập ngay tổ kiểm tra: Gọi xác minh ngẫu nhiên 30 đơn hoàn trả xem bưu tá có thực tế liên hệ khách hay tự ý bấm báo 'không nghe máy/hẹn lại' để chuyển trạng thái hoàn!",
     (147, 51, 234), True)
], fill_hex="FAF5FF", border_hex="A855F7")

# ==================== XII. AGING TỒN KHO & TREO LC ====================
add_section_header(doc, "⚠️ [AGING TỒN KHO & HÀNG TREO LUÂN CHUYỂN]")

add_callout_box(doc, [
    ("🗣️ LỜI THUYẾT TRÌNH BÁO CÁO:\n",
     "1️⃣ AGING TỒN KHO QUÁ 5 NGÀY:\n"
     "Toàn vùng Nam Trung Bộ tuần W36 ghi nhận 1.268 đơn tồn kho quá 5 ngày (đã giảm mạnh so với 2.266 đơn ở W35):\n"
     "• Cơ cấu tồn: Nhóm 5–8 ngày có 869 đơn (68,5%); Nhóm 8–15 ngày có 330 đơn (26,0%); Nhóm >15 ngày (rủi ro đền bù cao nhất) còn 69 đơn (5,5%).\n"
     "• Top 4 AM nắm giữ tới 75,5% lượng tồn Aging toàn vùng:\n"
     "  🔴 1. Anh Lê Văn Trường: 256 đơn (20,2% vùng) — 118 đơn 5-8N, 119 đơn 8-15N, 19 đơn >15N.\n"
     "  🔴 2. Anh Trầm Hữu Tiến: 253 đơn (20,0% vùng) — 183 đơn 5-8N, 70 đơn 8-15N, 0 đơn >15N.\n"
     "  🔴 3. Anh Trương Quang Linh: 236 đơn (18,6% vùng) — giữ tới 26 đơn >15N (chiếm gần 40% đơn >15N toàn vùng).\n"
     "  🔴 4. Chị Hồng Bích Nga: 212 đơn (16,7% vùng) — 22 đơn >15N.\n\n"
     "2️⃣ HÀNG TREO LUÂN CHUYỂN:\n"
     "Toàn vùng hiện có 4.435 đơn treo luân chuyển. Trong đó, 5 bưu cục nghẽn lớn nhất:\n"
     "• BC (DNO) Kiến Đức: 292 đơn treo (chiếm 6,6% vùng) — tiếp tục là điểm nóng kép cả về FD lẫn Treo LC.\n"
     "• BC (LDO) Đơn Dương: 187 đơn treo (AM Lê Văn Trường).\n"
     "• BC (DNO) Quảng Tín: 167 đơn treo (AM Trương Quang Linh).\n"
     "• BC (KHO) Cam Linh: 128 đơn treo (AM Nguyễn Thanh Long).\n"
     "• BC (NTH) Phước Dinh: 110 đơn treo (AM Nguyễn Duy Long).",
     (15, 76, 129), True)
], fill_hex="FFF7ED", border_hex="F97316")

# ==================== XIII. BÁO CÁO KTC & VẬN TẢI (MỤC MỚI) ====================
add_section_header(doc, "🚚 [BÁO CÁO KTC & VẬN TẢI ĐƯỜNG DÀI (MỤC MỚI)]", color_rgb=(13, 148, 136))

add_callout_box(doc, [
    ("🗣️ LỜI THUYẾT TRÌNH BÁO CÁO:\n",
     "Kính thưa Ban Giám Đốc, đây là nội dung mới và cực kỳ quan trọng được bổ sung trong kỳ họp W36 nhằm đánh giá toàn diện năng lực trung chuyển, leadtime và hiệu quả chi phí vận tải xe tuyến của 5 KTC/KCT toàn vùng:\n\n"
     "【PHẦN 1: BACKLOG KTC & ĐƠN TREO LUÂN CHUYỂN >36 GIỜ】\n"
     "• Tổng tồn luân chuyển tại 5 kho KTC/KCT toàn vùng là 16.207 đơn. Trong đó 76% (12.309 đơn) nằm trong khung luân chuyển chuẩn 0–6h.\n"
     "• BÁO ĐỘNG ĐỎ VỀ ĐƠN TREO: Toàn vùng đang có 381 đơn treo luân chuyển trên 36 giờ chưa thể đóng kiện xuất kho. Đáng chú ý, 100% số đơn treo >36h này (381/381 đơn) đều nằm tập trung tại KTC Khánh Hòa dưới sự quản lý của AM Nguyễn Tiến Lực!\n"
     "→ Yêu cầu AM Nguyễn Tiến Lực báo cáo tình trạng dồn ứ tại KTC Khánh Hòa và cam kết giải tỏa dứt điểm 381 đơn này trong vòng 24h tới.\n\n"
     "【PHẦN 2: TỔNG QUAN LEADTIME KTC/KCT & ĐÁNH GIÁ SLA】\n"
     "• Leadtime nhận – xuất trung bình toàn vùng đạt 3,31 giờ (P50: 2,24h; P95: 7,09h). Tỷ lệ tồn >12h toàn vùng là 2,1% (662 đơn); tồn >24h là 0,1% (46 đơn).\n"
     "• Điểm vi phạm SLA nghiêm trọng: KCT Đắk Nông có tỷ lệ tồn >12 giờ lên tới 12,4% (405 đơn tồn >12h trên tổng 3.272 đơn qua kho), cao gấp 6 lần mức bình quân vùng và vi phạm trực tiếp SLA nhận xuất của Công ty.\n\n"
     "【PHẦN 3: BÁO CÁO TỶ LỆ LẤP ĐẦY THÙNG XE (TLLĐ) — SO SÁNH W35 VS W36】\n"
     "Dữ liệu giám sát tải trọng 516 chuyến xe luân chuyển toàn vùng trong tuần W36:\n"
     "• TLLĐ bình quân toàn vùng W36: Đạt 48,1%, giảm -3,7%p so với mức 51,8% của W35.\n"
     "• Tổng số chuyến xe: Chạy 516 chuyến (giảm 22 chuyến so với 538 chuyến ở W35 do sản lượng sụt giảm).\n"
     "• CẢNH BÁO CHI PHÍ LÃNG PHÍ XE RỖNG: Toàn vùng ghi nhận 112 chuyến xe có TLLĐ dưới 30% (chiếm 21,7% tổng số chuyến xe). Trong đó có 10 chuyến xe chạy dưới 10% tải, 40 chuyến từ 10–20% tải và 62 chuyến từ 20–30% tải!\n"
     "• So sánh chi tiết từng KTC/KCT giữa W35 và W36:\n"
     "  - KTC Khánh Hòa: TLLĐ đạt 51,5% (W35: 53,2%, giảm -1,7%p), chạy 215 chuyến, có 38 chuyến <30% tải.\n"
     "  - KCT Bảo Lộc (Lâm Đồng): TLLĐ đạt 49,9% (W35: 52,1%, giảm -2,2%p), chạy 88 chuyến, 16 chuyến <30% tải.\n"
     "  - KCT Đức Trọng (Lâm Đồng): TLLĐ đạt 49,1% (W35: 53,5%, giảm mạnh -4,4%p), chạy 110 chuyến, 25 chuyến <30% tải.\n"
     "  - KCT Bình Thuận: TLLĐ đạt 48,7% (W35: 50,4%, giảm -1,7%p), chạy 62 chuyến, 12 chuyến <30% tải.\n"
     "  - KCT Đắk Nông: Đáy lấp đầy toàn vùng, chỉ đạt 30,7% (W35: 38,1%, giảm sốc -7,4%p), chạy 41 chuyến nhưng có tới 21 chuyến <30% tải (chiếm hơn 51% số chuyến xe chạy ở Đắk Nông là xe rỗng!).\n\n"
     "• Nguyên nhân hàng đầu gây ra 112 chuyến xe <30% tải:\n"
     "  1. Sản lượng bưu cục và hàng lấy về phát sinh thấp (chiếm 35%).\n"
     "  2. Lộ trình xe ghé nhiều điểm nhưng các điểm cuối trả ít hàng (chiếm 12%).\n"
     "  3. Kho KTC chủ động điều xe chạy rỗng để kịp giờ ca kết nối liên tỉnh (chiếm 9%).\n"
     "→ Hành động: Yêu cầu phòng Vận Tải phối hợp AM Đắk Nông ghép chuyến tuyến Gia Nghĩa – Đắk Mil và Đức Trọng – Bảo Lộc để kéo TLLĐ toàn vùng quay lại mốc ≥52% trong tuần W37.",
     (13, 148, 136), True)
], fill_hex="F0FDFA", border_hex="0D9488")

# ==================== XIV. KIỂM SOÁT TIỀN MẶT QR ====================
add_section_header(doc, "💳 [III. KIỂM SOÁT — TỶ LỆ TIỀN MẶT & QR]")

add_callout_box(doc, [
    ("🗣️ LỜI THUYẾT TRÌNH BÁO CÁO:\n",
     "Về kiểm soát dòng tiền COD thu hộ 2 tuần gần nhất (W35 vs W36):\n"
     "• Tỷ lệ tiền mặt toàn vùng W36 ghi nhận 39,6%, tăng +1,1%p so với 38,5% của W35 (tỷ lệ chuyển khoản QR giảm về 60,4%). Chỉ tiêu vùng là kéo tiền mặt xuống dưới 35%.\n"
     "• Các AM có tỷ lệ tiền mặt cao nhất cần kiểm soát chặt rủi ro công nợ bưu tá:\n"
     "  - Chị Huỳnh Thị Kim Chi: 74,5% tiền mặt (đã giảm nhẹ từ 76,8%).\n"
     "  - Anh Huỳnh Thúc Duân: 72,2% tiền mặt.\n"
     "  - Chị Trần Thị Nhung: 70,2% tiền mặt.\n"
     "  - Anh Trần Văn Phước: 69,1% tiền mặt.\n"
     "  - Anh Lê Văn Trường: 67,8% tiền mặt.\n"
     "• Các bưu cục giữ kỷ lục tiền mặt cao nhất: BC Hòa Ninh (Lâm Đồng) 97,8%; BC Quảng Khê (Đắk Nông) 93,9%; BC Bắc Gia Nghĩa (Đắk Nông) 89,1%.\n"
     "→ Đề nghị các AM vùng Đắk Nông và Lâm Đồng tiếp tục đôn đốc bưu tá mang mã QR in sẵn trên áo và thùng xe khi đi giao.",
     (15, 76, 129), True)
], fill_hex="FFF7ED", border_hex="F97316")

# ==================== XV. TRUY THU VÀ PHẠT TICKET ====================
add_section_header(doc, "🛡️ [IV. TRUY THU VÀ PHẠT TICKET OE-IA]")

add_callout_box(doc, [
    ("🗣️ LỜI THUYẾT TRÌNH BÁO CÁO:\n",
     "Về báo cáo truy thu sai sót quy trình (OE-IA):\n"
     "• Toàn vùng W36 ghi nhận 9.513 đơn/ticket có phát sinh truy thu với tổng số tiền cần truy thu là 174,66 triệu VNĐ (sau các bước cấn trừ và giải trình, đã giảm được -21,2 triệu so với W35).\n"
     "• Top các bưu cục có số tiền truy thu lớn nhất tập trung tại Đắk Nông và Lâm Đồng:\n"
     "  1. BC Quảng Tín (Đắk Nông): 2.079 ticket, số tiền cần thu phát sinh lớn nhất vùng.\n"
     "  2. BC Kiến Đức (Đắk Nông): 1.650 ticket.\n"
     "  3. BC Nam Ban (Lâm Đồng): 1.420 ticket.\n"
     "  4. BC Tuy Đức (Đắk Nông): 1.180 ticket.\n"
     "• Phân loại lỗi: Vi phạm quy trình giao hàng (BL Giao) chiếm trên 50%, tiếp theo là vi phạm luân chuyển (VL LC) chiếm 30%.\n"
     "→ Yêu cầu các AM Đắk Nông hoàn tất việc rà soát biên bản cân đo và giải trình ticket tồn đọng trước ngày 10/09.",
     (15, 76, 129), True)
], fill_hex="FFF7ED", border_hex="F97316")

# ==================== XVI. KINH DOANH VÀ F30 ====================
add_section_header(doc, "📈 [V. KINH DOANH & KHÁCH HÀNG MỚI F30]")

add_callout_box(doc, [
    ("🗣️ LỜI THUYẾT TRÌNH BÁO CÁO:\n",
     "Về kết quả kinh doanh và phát triển khách hàng mới tuần W36:\n"
     "• Doanh thu vùng W36: Đạt 947,4 triệu đồng trên 30.132 đơn cước, giảm -11,7% (-125,8 triệu đồng) so với tuần 35 (1,073 tỷ đồng) — chuỗi tăng trưởng doanh thu đã bị ngắt quãng do sụt giảm sản lượng chung.\n"
     "• Tình hình theo từng AM:\n"
     "  - Anh Phan Đình Duy: Vẫn là AM có doanh thu lớn nhất (421,9 triệu VNĐ, chiếm 44,5% vùng), nhưng cũng là người giảm tuyệt đối nhiều nhất với -73,1 triệu đồng (-14,8%).\n"
     "  - Anh Nguyễn Duy Long: Doanh thu 85,6 triệu VNĐ, giảm -12,5 triệu đồng.\n"
     "  - Anh Lê Thanh Nhựt: Doanh thu 41,8 triệu VNĐ, giảm -10,5 triệu đồng.\n"
     "  - Chị Hồng Bích Nga: Doanh thu 36,6 triệu VNĐ, giảm -9,7 triệu đồng.\n"
     "• Khách hàng mới F30: Toàn vùng phát triển được 93 khách hàng mới (giảm nhẹ 2 KH so với 95 KH ở W35), nhưng doanh thu từ nhóm F30 giảm mạnh từ 21,8M xuống còn 6,2M (-71,6%) do thiếu vắng các shop có volume lớn.\n"
     "→ Đề nghị phòng Kinh doanh và các AM tập trung vào chương trình chăm sóc lại Top 10 shop có dấu hiệu giảm đơn hoặc ngừng phát sinh đơn cước.",
     (15, 76, 129), True)
], fill_hex="FFF7ED", border_hex="F97316")

# ==================== XVII. BẢNG ACTION PLAN W37 ====================
add_section_header(doc, "🎯 [VI. TỔNG HỢP GÓP Ý & ACTION PLAN TUẦN W37]", color_rgb=(185, 28, 28))

p_act_intro = doc.add_paragraph()
p_act_intro.paragraph_format.space_after = Pt(6)
r_ai = p_act_intro.add_run("Bảng phân công nhiệm vụ cụ thể cho từng AM và bộ phận liên quan nhằm xử lý triệt để các số liệu báo động trong tuần W36:")
r_ai.font.name = 'Times New Roman'
r_ai.font.size = Pt(11)
r_ai.italic = True

# Tạo bảng 3 cột: AM Phụ Trách | Vấn Đề Số Liệu Cần Xử Lý | Mục Tiêu & Deadline W37
table_ap = doc.add_table(rows=12, cols=3)
table_ap.alignment = WD_TABLE_ALIGNMENT.CENTER
table_ap.autofit = False

# Set col widths: 3.2cm | 8.0cm | 5.4cm
col_widths = [Cm(3.2), Cm(8.0), Cm(5.4)]
for row in table_ap.rows:
    for i, w in enumerate(col_widths):
        row.cells[i].width = w

# Header row styling
headers = ["AM / Bộ Phận", "Vấn Đề Số Liệu Báo Động Tuần W36", "Mục Tiêu & Deadline Tuần W37"]
for i, h in enumerate(headers):
    cell = table_ap.rows[0].cells[i]
    cell.text = h
    tcPr = cell._tc.get_or_add_tcPr()
    shd_xml = f'<w:shd {nsdecls("w")} w:val="clear" w:color="auto" w:fill="0F4C81"/>'
    tcPr.append(parse_xml(shd_xml))
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.runs[0].font.name = 'Times New Roman'
    p.runs[0].font.size = Pt(10.5)
    p.runs[0].bold = True
    p.runs[0].font.color.rgb = RGBColor(255, 255, 255)

action_data = [
    ("Hồng Bích Nga", 
     "• BC Kiến Đức FD cao nhất toàn vùng 43,7% (1.422 đơn hoàn)\n• Hàng treo luân chuyển BC Kiến Đức 292 đơn (cao nhất vùng 6,6%)\n• Aging tồn 212 đơn (22 đơn >15 ngày)",
     "Cắm chốt trực tiếp tại BC Kiến Đức, gọi ngẫu nhiên xác minh đơn hoàn, giảm FD về <25%, xả 292 đơn treo.\nHạn: Thứ 4"),

    ("Trương Quang Linh", 
     "• BC Quảng Tín FD 28,8% (573 đơn hoàn)\n• Tồn Aging 236 đơn (ôm 26 đơn >15 ngày)\n• GTC tổng 15,3% vẫn thấp nhất vùng",
     "Xử lý dứt điểm 26 đơn tồn >15N, hạ FD Quảng Tín xuống <18%, nâng GTC lên ≥25%.\nHạn: Thứ 5"),

    ("Lê Minh Lợi", 
     "• Rớt LC ghi nhận 100% (cần xác minh)\n• BC Lang Biang FD 17,5% (490 đơn)\n• GTC Ca 2 chỉ đạt 32,9%",
     "Rà soát nguyên nhân rớt LC, siết quy trình giao phát bưu cục Lang Biang, kéo GTC Ca2 lên ≥45%.\nHạn: Thứ 4"),

    ("Trầm Hữu Tiến", 
     "• ODR sụt giảm -3,9% xuống 75,6% (thấp nhất nhóm kỳ cựu)\n• Aging tồn 253 đơn (183 đơn nhóm 5-8 ngày)\n• BC Đức Trọng 1 FD 11,7%",
     "Giải phóng dứt điểm 183 đơn Aging 5-8N, lập phương án cam kết kéo ODR trở lại ≥82%.\nHạn: Thứ 4"),

    ("Huỳnh Thúc Duân", 
     "• GTC giảm mạnh nhất vùng -6,2% xuống 41,6%\n• Rớt LC 15,28%\n• BC Đông Gia Nghĩa và Nhân Cơ FD >12,6%",
     "Kiểm soát quy trình phân tuyến phát Ca 2, kéo GTC lên ≥48%, chặn đứng rớt LC về <4%.\nHạn: Thứ 5"),

    ("Lê Văn Trường", 
     "• Sản lượng full giảm nhiều nhất -2.709 đơn\n• Tồn Aging cao nhất vùng 256 đơn\n• Treo LC BC Đơn Dương 187 đơn",
     "Rà soát tiếp cận lại các shop giảm đơn, tổ chức giao quét sạch 256 đơn Aging tại Lâm Đồng.\nHạn: Thứ 5"),

    ("Nguyễn Ngọc Khánh", 
     "• LTC giảm sốc nhất vùng -11,1% (từ 91,1% xuống 80,0%)\n• GTC giảm -5,0% xuống 71,6%",
     "Báo cáo chi tiết lý do shop hủy lấy đơn, chấn chỉnh bưu tá tuyến lấy hàng, đưa LTC lên ≥90%.\nHạn: Thứ 3"),

    ("Phan Đình Duy", 
     "• Doanh thu sụt giảm -73,1 triệu đồng (-14,8%)\n• GTC giảm -5,2% xuống 58,8%\n• BC Nha Trang FD 11,7% (375 đơn hoàn)",
     "Gặp trực tiếp top 5 khách hàng lớn bị giảm cước tại Nha Trang, đẩy mạnh phát Ca 2 kéo GTC lên ≥65%.\nHạn: Thứ 6"),

    ("Nguyễn Tiến Lực\n(KTC Khánh Hòa)", 
     "• Treo luân chuyển >36h có 381 đơn (chiếm 100% toàn vùng)",
     "Huy động nhân lực KTC đóng kiện xuất kho giải tỏa 100% 381 đơn treo trong 24h.\nHạn: 12h Thứ 3"),

    ("KCT Đắk Nông", 
     "• Leadtime tồn >12h chiếm 12,4% (405 đơn) — vi phạm SLA\n• TLLĐ xe chỉ đạt 30,7% (hơn 51% số chuyến là xe rỗng)",
     "Rà soát ca làm việc xuất nhập KCT, ghép lộ trình xe gom tuyến liên huyện nâng TLLĐ lên ≥38%.\nHạn: Thứ 5"),

    ("Đội Xe Tuyến\n(Toàn vùng NTB)", 
     "• Toàn vùng có 112 chuyến xe dưới 30% TLLĐ (21,7% tổng số chuyến)\n• TLLĐ trung bình giảm xuống 48,1%",
     "Tối ưu lại biểu đồ giờ xe chạy, linh hoạt cắt/ghép nốt xe tải nhỏ trên các cung đường ít hàng, kéo TLLĐ ≥52%.\nHạn: Hết tuần")
]

for row_idx, (am, issue, plan) in enumerate(action_data, start=1):
    row = table_ap.rows[row_idx]
    bg_color = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
    
    for c_idx, text in enumerate([am, issue, plan]):
        cell = row.cells[c_idx]
        cell.text = text
        tcPr = cell._tc.get_or_add_tcPr()
        
        # Border mỏng
        b_xml = f"""
        <w:tcBorders {nsdecls('w')}>
            <w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
            <w:left w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
            <w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
            <w:right w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
        </w:tcBorders>
        """
        tcPr.append(parse_xml(b_xml))
        shd_xml = f'<w:shd {nsdecls("w")} w:val="clear" w:color="auto" w:fill="{bg_color}"/>'
        tcPr.append(parse_xml(shd_xml))
        
        # Margins
        mar_xml = f"""
        <w:tcMar {nsdecls('w')}>
            <w:top w:w="120" w:type="dxa"/>
            <w:left w:w="140" w:type="dxa"/>
            <w:bottom w:w="120" w:type="dxa"/>
            <w:right w:w="140" w:type="dxa"/>
        </w:tcMar>
        """
        tcPr.append(parse_xml(mar_xml))
        
        p = cell.paragraphs[0]
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        
        for run in p.runs:
            run.font.name = 'Times New Roman'
            run.font.size = Pt(10)
            if c_idx == 0:
                run.bold = True
                run.font.color.rgb = RGBColor(15, 76, 129)
            elif c_idx == 1:
                run.font.color.rgb = RGBColor(30, 41, 59)
            else:
                run.font.color.rgb = RGBColor(185, 28, 28)

doc.add_paragraph().paragraph_format.space_after = Pt(10)

# ==================== XVIII. LỜI KẾT ====================
add_callout_box(doc, [
    ("🗣️ LỜI THUYẾT TRÌNH BÁO CÁO:\n",
     "\"Trên đây là toàn bộ báo cáo phân tích chi tiết của vùng Nam Trung Bộ tuần 36, với các bổ sung trọng tâm về %FD Hoàn trả và Hiệu quả Vận tải xe KTC. "
     "Em xin cảm ơn Ban Giám Đốc và các anh chị em AM đã chú ý lắng nghe. Xin kính mời Ban Giám Đốc cho ý kiến chỉ đạo để toàn vùng triển khai đồng bộ trong tuần W37!\"",
     (15, 76, 129), True)
], fill_hex="FFF7ED", border_hex="F97316")

# Lưu file hoàn chỉnh
out_file = r'C:\Users\lap4all\Desktop\New folder\KICH_BAN_THUYET_TRINH_W36_CHUAN_SO_LIEU.docx'
doc.save(out_file)
print(f"SUCCESS: Saved file to {out_file}")

# Đồng thời copy ra file nếu không bị Word khóa
out_file2 = r'C:\Users\lap4all\Desktop\New folder\KICH_BAN_THUYET_TRINH_W36_NTB.docx'
try:
    doc.save(out_file2)
    print(f"SUCCESS: Also updated {out_file2}")
except PermissionError:
    print(f"NOTE: {out_file2} is currently open in Word, skipped overwrite.")

