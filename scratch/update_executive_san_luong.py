import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
import shutil

sys.stdout.reconfigure(encoding='utf-8')

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=140, bottom=140, left=180, right=180):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def update_san_luong_section(doc_path):
    doc = docx.Document(doc_path)
    if len(doc.tables) < 2:
        return
    
    cell = doc.tables[1].rows[0].cells[0]
    
    # Clear existing paragraphs
    p0 = cell.paragraphs[0]
    p0.text = ""
    for p in cell.paragraphs[1:]:
        p._p.getparent().remove(p._p)
        
    p0.paragraph_format.space_before = Pt(2)
    p0.paragraph_format.space_after = Pt(4)
    r_t = p0.add_run("🗣️ KỊCH BẢN THUYẾT TRÌNH SẢN LƯỢNG — INSIGHT CHUYÊN SÂU 3 BIỂU ĐỒ:")
    r_t.bold = True
    r_t.font.name = 'Arial'
    r_t.font.size = Pt(11)
    r_t.font.color.rgb = RGBColor(194, 65, 12)
    
    blocks = [
        ('"Kính thưa Ban Giám Đốc, về bức tranh sản lượng tuần W39, em xin đi thẳng vào 3 insight cốt lõi tương ứng với 3 biểu đồ trên màn hình:', 'intro'),
        
        ('📊 CHART 1: BẢN CHẤT HẠ NHIỆT FULL HÀNG & NGHỊCH LÝ TĂNG TRƯỞNG NỘI ĐÔ', 'header_c1'),
        ('(Chiếu Chart 1: Sản Lượng Full Hàng)', 'action'),
        ('• Tổng quan: Full hàng toàn vùng đạt 328.925 đơn (-4,3% WoW, giảm -14,7k đơn). Sự sụt giảm này mang tính quy luật sau chuỗi ngày sale lớn, tập trung chủ yếu ở Lâm Đồng (-7,4k đơn do mưa bão đồi dốc) và cụm AM Trường, AM Khánh (-4,2k đơn).', 'bullet'),
        ('• Nghịch lý bứt phá: Giữa bức tranh giảm chung, AM Thái Thị Thanh Thư (Khánh Hòa) lội ngược dòng ngoạn mục tăng +2.227 đơn (+6,8% WoW, đạt 34.765 đơn), chính thức vươn lên Top 2 toàn vùng nhờ tóm trọn sức mua tiêu dùng nội thị Nha Trang. Ở thái cực ổn định, AM Nguyễn Duy Long tiếp tục là "xương sống" số 1 toàn mạng gánh 42.506 đơn (chiếm 12,9% sản lượng vùng).', 'bullet'),
        
        ('⚡ CHART 2: TIKTOK SHOP — ĐỘNG LỰC TĂNG TRƯỞNG & ĐIỂM NGHẼN BẤT THƯỜNG', 'header_c2'),
        ('(Bấm chuyển sang Chart 2: Sản Lượng TikTok Shop)', 'action'),
        ('• Động lực bứt phá: Trái ngược với Full hàng, TikTok Shop chính là điểm sáng cứu cánh cho toàn vùng khi tăng trưởng +5,9% WoW, đạt 72.781 đơn với 5/5 tỉnh đều tăng dương. Cực tăng trưởng mạnh nhất nằm ở Bình Thuận (+14,3% WoW) do AM Nguyễn Duy Long bứt tốc kéo thêm +1.379 đơn TTS (đạt 10.584 đơn, chiếm 15% TTS cả vùng).', 'bullet'),
        ('• Cảnh báo bất thường: Toàn mạng có 12/18 AM tăng trưởng TTS, nhưng bộc lộ 1 điểm nghẽn nghiêm trọng tại Cam Ranh khi AM Nguyễn Thanh Long rơi tự do -1.186 đơn TTS (-40% WoW, chỉ còn 1.744 đơn) do một số shop live thời trang tạm ngưng hoạt động. Khối KD cần vào cuộc giữ shop ngay.', 'bullet'),
        
        ('📦 CHART 3: TỶ TRỌNG TTS LẬP ĐỈNH 22.1% & PHÂN HÓA 2 THÁI CỰC VẬN HÀNH', 'header_c3'),
        ('(Bấm chuyển sang Chart 3: So Sánh Full Hàng vs TTS)', 'action'),
        ('• Cơ cấu toàn mạng: Tỷ trọng TTS chính thức lập kỷ lục mới 22,1% (cứ 5 đơn giao ra có hơn 1 đơn là TikTok Shop), định hình rõ 2 thái cực:', 'bullet'),
        ('  - Nhóm phụ thuộc nặng TMĐT (TTS chiếm 25-29%): Điển hình là Huỳnh Thúc Duân (29,0%), Nguyễn Hoàng Phi (25,1%), Nguyễn Duy Long (24,9%), Trần Thị Nhung (24,6%). Nhóm này chịu sức ép cực lớn về cam kết SLA ca sáng, nếu bưu tá xuất tuyến trễ là vỡ trận ODR ngay lập tức.', 'bullet'),
        ('  - Nhóm thuần truyền thống (TTS còn thấp <16%): Như AM Thái Thị Thanh Thư (16,0%) và AM Nguyễn Thanh Long (13,2%). Đây là "mỏ vàng" còn nguyên dư địa để khối Kinh doanh đánh mạnh shop F30 phân khúc TikTok trong tuần W40."', 'bullet'),
        
        ('🔍 INSIGHT ĐIỀU HÀNH CỐT LÕI:', 'sec_in'),
        ('• TikTok Shop đã trở thành động lực sống còn gánh sản lượng vùng, nhưng tính chất phân hóa tỷ trọng (từ 13% đến 29%) đòi hỏi công tác điều tiết bưu tá ca sáng phải linh hoạt theo từng cụm AM.', 'in_bullet'),
        ('🎯 MỆNH LỆNH TÁC CHIẾN TUẦN W40:', 'sec_ac'),
        ('• Khối KD lập tức rà soát cụm Cam Ranh (AM Long) để kéo lại các shop livestream; Khối Vận Hành ưu tiên xuất tuyến trước 08h15 cho 4 AM có tỷ trọng TTS trên 25%.', 'ac_bullet')
    ]
    
    for text, kind in blocks:
        p = cell.add_paragraph()
        p.paragraph_format.line_spacing = 1.25
        
        if kind == 'intro':
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(4)
            r = p.add_run(text)
            r.italic = True
            r.font.name = 'Arial'
            r.font.size = Pt(9.5)
            r.font.color.rgb = RGBColor(15, 23, 42)
        elif kind in ['header_c1', 'header_c2', 'header_c3']:
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(1)
            r = p.add_run(text)
            r.bold = True
            r.font.name = 'Arial'
            r.font.size = Pt(10)
            if kind == 'header_c1':
                r.font.color.rgb = RGBColor(15, 76, 129)
            elif kind == 'header_c2':
                r.font.color.rgb = RGBColor(194, 65, 12)
            else:
                r.font.color.rgb = RGBColor(109, 40, 217)
        elif kind == 'action':
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(text)
            r.italic = True
            r.bold = True
            r.font.name = 'Arial'
            r.font.size = Pt(8.5)
            r.font.color.rgb = RGBColor(100, 116, 139)
        elif kind == 'bullet':
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(3)
            if ':' in text and not text.strip().startswith('- '):
                parts = text.split(':', 1)
                r_pre = p.add_run(parts[0] + ":")
                r_pre.bold = True
                r_pre.font.name = 'Arial'
                r_pre.font.size = Pt(9.5)
                r_pre.font.color.rgb = RGBColor(15, 23, 42)
                r_post = p.add_run(parts[1])
                r_post.font.name = 'Arial'
                r_post.font.size = Pt(9.5)
                r_post.font.color.rgb = RGBColor(51, 65, 85)
            else:
                r = p.add_run(text)
                r.font.name = 'Arial'
                r.font.size = Pt(9.5)
                r.font.color.rgb = RGBColor(51, 65, 85)
        elif kind == 'sec_in':
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(1)
            r = p.add_run(text)
            r.bold = True
            r.font.name = 'Arial'
            r.font.size = Pt(9.5)
            r.font.color.rgb = RGBColor(15, 76, 129)
        elif kind == 'in_bullet':
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(text)
            r.font.name = 'Arial'
            r.font.size = Pt(9)
            r.font.color.rgb = RGBColor(51, 65, 85)
        elif kind == 'sec_ac':
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(1)
            r = p.add_run(text)
            r.bold = True
            r.font.name = 'Arial'
            r.font.size = Pt(9.5)
            r.font.color.rgb = RGBColor(194, 65, 12)
        elif kind == 'ac_bullet':
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(text)
            r.font.name = 'Arial'
            r.font.size = Pt(9)
            r.font.color.rgb = RGBColor(51, 65, 85)
            
    doc.save(doc_path)
    print(f"Updated Section II in {doc_path} successfully!")

targets = [
    'KICH_BAN_THUYET_TRINH_MOI_NHAT.docx',
    'KICH_BAN_THUYET_TRINH_W39_INSIGHT_CHUYEN_SAU.docx',
    'KICH_BAN_THUYET_TRINH_W39_INSIGHT_CHUYEN_SAU_CHINH_SUA.docx',
    'KICH_BAN_THUYET_TRINH_W39_NAM_TRUNG_BO.docx'
]
for t in targets:
    update_san_luong_section(t)
