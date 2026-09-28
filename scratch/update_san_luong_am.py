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

def update_san_luong_am_focused(doc_path):
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
    r_t = p0.add_run("🗣️ KỊCH BẢN THUYẾT TRÌNH SẢN LƯỢNG — BÓC TÁCH CHI TIẾT 18 AM QUA 3 BIỂU ĐỒ:")
    r_t.bold = True
    r_t.font.name = 'Arial'
    r_t.font.size = Pt(11)
    r_t.font.color.rgb = RGBColor(194, 65, 12)
    
    blocks = [
        ('"Kính thưa Ban Giám Đốc, phần báo cáo Sản lượng giao tuần W39 xin đi sâu bóc tách chi tiết hiệu quả của 18 Quản lý Vận hành (AM) tuần tự qua 3 biểu đồ trực quan trên màn hình:', 'intro'),
        
        ('📊 CHART 1: BÓC TÁCH SẢN LƯỢNG FULL HÀNG 18 AM (CỘT W38 vs W39 + ĐƯỜNG LINE Δ)', 'header_c1'),
        ('(Chiếu Chart 1: Sản Lượng Full Hàng 18 AM)', 'action'),
        ('• Điểm sáng bứt phá tăng trưởng duy nhất toàn mạng: Biểu dương AM Thái Thị Thanh Thư là AM duy nhất bứt phá ngược dòng tăng tới +2.227 đơn (+6,8% WoW, từ 32.538 lên 34.765 đơn), chính thức vượt qua AM Lê Thanh Nhựt và AM Lê Văn Trường để chiếm lĩnh vị trí Top 2 sản lượng toàn vùng!', 'bullet'),
        ('• Trụ cột gánh tải số 1: AM Nguyễn Duy Long tiếp tục là "đầu tàu số 1" với 42.506 đơn (chiếm 12,9% sản lượng cả vùng, giữ nhịp ổn định chỉ giảm nhẹ -512 đơn). Cùng nhóm gánh tải lớn: AM Lê Thanh Nhựt (29.070 đơn), AM Lê Văn Trường (26.787 đơn), AM Nguyễn Ngọc Khánh (26.242 đơn), AM Trần Thị Nhung (24.581 đơn), AM Phan Đình Duy (23.282 đơn).', 'bullet'),
        ('• Nhóm 4 AM suy giảm sản lượng mạnh nhất (chiếm 50% mức giảm cả vùng): Giảm sâu nhất là AM Lê Văn Trường (-2.132 đơn), AM Nguyễn Ngọc Khánh (-2.083 đơn), AM Phan Đình Duy (-1.649 đơn), và AM Lê Thanh Nhựt (-1.530 đơn) do sức mua sau đợt cao điểm tạm hạ nhiệt.', 'bullet'),
        
        ('⚡ CHART 2: ĐỘNG LỰC TĂNG TRƯỞNG TIKTOK SHOP TRÊN 18 AM (CỘT TTS W38 vs W39 + LINE Δ)', 'header_c2'),
        ('(Bấm chuyển sang Chart 2: Sản Lượng TikTok Shop 18 AM)', 'action'),
        ('• Bùng nổ diện rộng: Có tới 12/18 AM tăng trưởng dương TTS! Trong đó, AM Nguyễn Duy Long thiết lập kỷ lục vô địch toàn mạng khi tăng thêm +1.379 đơn TTS (+15,0% WoW, từ 9.205 lên 10.584 đơn), trở thành AM đầu tiên vượt mốc 10.000 đơn TTS/tuần (chiếm gần 15% lượng TTS cả vùng)!', 'bullet'),
        ('• Nhóm 8 AM tăng tốc TTS rất ấn tượng (>350 - 800 đơn): Dẫn đầu là AM Lê Thanh Nhựt tăng +800 đơn (đạt 7.108 đơn), AM Hồng Bích Nga tăng +610 đơn (đạt 4.900 đơn), AM Nguyễn Hoàng Phi tăng +593 đơn (đạt 5.390 đơn), AM Phan Đình Duy tăng +531 đơn (đạt 5.347 đơn), AM Nguyễn Ngọc Khánh tăng +516 đơn (đạt 5.155 đơn), AM Cao Thị Thanh Thủy tăng +513 đơn (đạt 3.592 đơn), AM Thái Thị Thanh Thư tăng +511 đơn (đạt 5.562 đơn), AM Trần Thị Nhung tăng +379 đơn (đạt 6.057 đơn, giữ Top 3 TTS toàn vùng).', 'bullet'),
        ('• Cảnh báo đỏ 2 AM sụt giảm TTS sốc: Báo động nhất là AM Nguyễn Thanh Long rơi tự do mất -1.186 đơn TTS (-40,5% WoW, từ 2.930 đơn tụt xuống chỉ còn 1.744 đơn) do các shop live lớn tại Cam Ranh tạm ngưng hoặc đổi đơn vị vận chuyển. Kế tiếp là AM Lê Minh Lợi giảm -637 đơn TTS (rơi từ 844 về 207 đơn).', 'bullet'),
        
        ('📦 CHART 3: TỶ TRỌNG PHỤ THUỘC TTS TRÊN 18 AM — PHÂN HÓA 3 NHÓM CHIẾN LƯỢC', 'header_c3'),
        ('(Bấm chuyển sang Chart 3: So Sánh Full Hàng vs TTS 18 AM)', 'action'),
        ('• Nhóm 1: Phụ thuộc nặng TMĐT (TTS chiếm 24,5% – 34,8% sản lượng): Đứng đầu là AM Trương Quang Linh (TTS chiếm tới 34,8%), AM Huỳnh Thúc Duân (29,0%), AM Nguyễn Hoàng Phi (25,1%), AM Nguyễn Duy Long (24,9%), AM Nguyễn Thị Tuyết Thơ (24,7%), AM Trần Thị Nhung (24,6%), AM Lê Thanh Nhựt (24,5%), AM Nguyễn Lê Nguyên Vũ (24,5%). Áp lực vận hành của nhóm này tập trung 100% vào ca phát sáng và lấy hàng chiều, trễ giờ là rớt SLA sàn ngay!', 'bullet'),
        ('• Nhóm 2: Cơ cấu cân bằng (TTS chiếm 20% – 24%): Gồm Hồng Bích Nga (23,9%), Phan Đình Duy (23,0%), Nguyễn Đỗ Minh Nghĩa (22,4%), Cao Thị Thanh Thủy (22,1%), Huỳnh Thị Kim Chi (22,1%), Lê Văn Trường (20,3%). Đây là nhóm giữ nhịp vận hành ổn định nhất.', 'bullet'),
        ('• Nhóm 3: Vùng trũng TTS — Dư địa tăng trưởng còn rất lớn (< 16%): Nổi bật nhất là AM Thái Thị Thanh Thư (dù Full đứng Top 2 với 34.7k đơn nhưng TTS chỉ chiếm 16,0%, 5.5k đơn), AM Nguyễn Thanh Long (13,2%), và AM Lê Minh Lợi (8,2%). Đây là 3 địa bàn mà khối Kinh doanh cần tập trung săn đón các shop TikTok Shop mới trong tuần W40."', 'bullet'),
        
        ('🔍 INSIGHT ĐIỀU HÀNH 18 AM:', 'sec_in'),
        ('• AM Nguyễn Duy Long và AM Thái Thị Thanh Thư đang là 2 trụ cột gánh tải vững chắc nhất mạng lưới; tuy nhiên sự sụt giảm sốc -1.186 đơn TTS của AM Nguyễn Thanh Long (Cam Ranh) là tín hiệu cảnh báo cần can thiệp thương mại gấp.', 'in_bullet'),
        ('🎯 MỆNH LỆNH TÁC CHIẾN TUẦN W40:', 'sec_ac'),
        ('• Khối KD cử nhân sự xuống hỗ trợ cụm Cam Ranh (AM Long) để giữ chân các shop livestream; Khối Vận hành ưu tiên xuất tuyến trước 08h15 cho nhóm 8 AM có tỷ trọng TTS trên 24,5%.', 'ac_bullet')
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
    print(f"Updated AM-focused Section II in {doc_path} successfully!")

targets = [
    'KICH_BAN_THUYET_TRINH_MOI_NHAT.docx',
    'KICH_BAN_THUYET_TRINH_W39_INSIGHT_CHUYEN_SAU.docx',
    'KICH_BAN_THUYET_TRINH_W39_INSIGHT_CHUYEN_SAU_CHINH_SUA.docx',
    'KICH_BAN_THUYET_TRINH_W39_NAM_TRUNG_BO.docx'
]
for t in targets:
    update_san_luong_am_focused(t)
