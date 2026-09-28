import os
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

def add_speech_section(doc, sec_title, speech_heading, paragraphs_text, insights=None, warnings=None, actions=None, border_color="EA580C", bg_color="FFF7ED"):
    # Section Header
    p_sec = doc.add_paragraph()
    p_sec.paragraph_format.space_before = Pt(14)
    p_sec.paragraph_format.space_after = Pt(4)
    r_sec = p_sec.add_run(sec_title)
    r_sec.bold = True
    r_sec.font.name = 'Arial'
    r_sec.font.size = Pt(12)
    r_sec.font.color.rgb = RGBColor(15, 76, 129)
    
    # Table Callout
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.9)
    
    set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=160, bottom=160, left=220, right=200)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="none"/>
            <w:left w:val="single" w:sz="36" w:space="0" w:color="{border_color}"/>
            <w:bottom w:val="none"/>
            <w:right w:val="none"/>
        </w:tcBorders>
    ''')
    tcPr.append(borders)
    
    # Heading
    p0 = cell.paragraphs[0]
    p0.paragraph_format.space_before = Pt(2)
    p0.paragraph_format.space_after = Pt(4)
    r0 = p0.add_run(speech_heading)
    r0.bold = True
    r0.font.name = 'Arial'
    r0.font.size = Pt(10.5)
    r0.font.color.rgb = RGBColor(194, 65, 12) if border_color=="EA580C" else RGBColor(15, 76, 129)
    
    # Speech paragraphs
    for p_idx, text in enumerate(paragraphs_text):
        p = cell.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.25
        
        t_clean = text.strip()
        if t_clean.startswith(('•', '-', '*')) or (len(t_clean) > 2 and t_clean[0].isdigit() and t_clean[1] in ['.', ')']):
            if ':' in t_clean:
                parts = t_clean.split(':', 1)
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
                r = p.add_run(t_clean)
                r.font.name = 'Arial'
                r.font.size = Pt(9.5)
                r.font.color.rgb = RGBColor(30, 41, 59)
        elif t_clean.startswith('📊') or t_clean.startswith('⚡') or t_clean.startswith('📦'):
            r = p.add_run(t_clean)
            r.bold = True
            r.font.name = 'Arial'
            r.font.size = Pt(10)
            r.font.color.rgb = RGBColor(15, 76, 129) if '📊' in t_clean else (RGBColor(194, 65, 12) if '⚡' in t_clean else RGBColor(109, 40, 217))
        elif t_clean.startswith('"') or t_clean.endswith('"'):
            r = p.add_run(t_clean)
            r.italic = True
            r.font.name = 'Arial'
            r.font.size = Pt(9.5)
            r.font.color.rgb = RGBColor(15, 23, 42)
        else:
            r = p.add_run(t_clean)
            r.font.name = 'Arial'
            r.font.size = Pt(9.5)
            r.font.color.rgb = RGBColor(30, 41, 59)
            
    # Insights, warnings, actions
    if insights:
        p_in = cell.add_paragraph()
        p_in.paragraph_format.space_before = Pt(6)
        p_in.paragraph_format.space_after = Pt(2)
        r_in_t = p_in.add_run("🔍 INSIGHT BẢN CHẤT & NGUYÊN NHÂN CỐT LÕI:")
        r_in_t.bold = True
        r_in_t.font.name = 'Arial'
        r_in_t.font.size = Pt(9.5)
        r_in_t.font.color.rgb = RGBColor(15, 76, 129)
        for item in insights:
            p_item = cell.add_paragraph()
            p_item.paragraph_format.space_before = Pt(1)
            p_item.paragraph_format.space_after = Pt(2)
            r = p_item.add_run(f"• {item}")
            r.font.name = 'Arial'
            r.font.size = Pt(9)
            r.font.color.rgb = RGBColor(51, 65, 85)
            
    if warnings:
        p_w = cell.add_paragraph()
        p_w.paragraph_format.space_before = Pt(4)
        p_w.paragraph_format.space_after = Pt(2)
        r_w_t = p_w.add_run("⚠️ CẢNH BÁO ĐỎ & NGUY CƠ TIỀM ẨN:")
        r_w_t.bold = True
        r_w_t.font.name = 'Arial'
        r_w_t.font.size = Pt(9.5)
        r_w_t.font.color.rgb = RGBColor(220, 38, 38)
        for item in warnings:
            p_item = cell.add_paragraph()
            p_item.paragraph_format.space_before = Pt(1)
            p_item.paragraph_format.space_after = Pt(2)
            r = p_item.add_run(f"• {item}")
            r.font.name = 'Arial'
            r.font.size = Pt(9)
            r.font.color.rgb = RGBColor(51, 65, 85)
            
    if actions:
        p_a = cell.add_paragraph()
        p_a.paragraph_format.space_before = Pt(4)
        p_a.paragraph_format.space_after = Pt(2)
        r_a_t = p_a.add_run("🎯 QUYẾT SÁCH HÀNH ĐỘNG & MỆNH LỆNH TÁC CHIẾN:")
        r_a_t.bold = True
        r_a_t.font.name = 'Arial'
        r_a_t.font.size = Pt(9.5)
        r_a_t.font.color.rgb = RGBColor(194, 65, 12)
        for item in actions:
            p_item = cell.add_paragraph()
            p_item.paragraph_format.space_before = Pt(1)
            p_item.paragraph_format.space_after = Pt(2)
            r = p_item.add_run(f"• {item}")
            r.font.name = 'Arial'
            r.font.size = Pt(9)
            r.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

def build_full_w39_docx():
    doc = docx.Document()
    
    # Page setup - 0.8 inch margins
    for sec in doc.sections:
        sec.top_margin = Inches(0.8)
        sec.bottom_margin = Inches(0.8)
        sec.left_margin = Inches(0.8)
        sec.right_margin = Inches(0.8)
        
    # --- HEADER BLOCK ---
    p0 = doc.add_paragraph()
    p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p0.paragraph_format.space_before = Pt(0)
    p0.paragraph_format.space_after = Pt(2)
    r0 = p0.add_run("CÔNG TY CỔ PHẦN GIAO HÀNG NHANH — GHN EXPRESS")
    r0.bold = True
    r0.font.name = 'Arial'
    r0.font.size = Pt(10)
    r0.font.color.rgb = RGBColor(100, 116, 139)

    p1 = doc.add_paragraph()
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p1.paragraph_format.space_before = Pt(2)
    p1.paragraph_format.space_after = Pt(4)
    r1 = p1.add_run("BÁO CÁO VẬN HÀNH & KINH DOANH TUẦN W39 — VÙNG NAM TRUNG BỘ")
    r1.bold = True
    r1.font.name = 'Arial'
    r1.font.size = Pt(16)
    r1.font.color.rgb = RGBColor(15, 76, 129) # GHN Blue

    p2 = doc.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p2.paragraph_format.space_before = Pt(0)
    p2.paragraph_format.space_after = Pt(4)
    r2 = p2.add_run("(Chu kỳ dữ liệu: 21/09/2026 – 27/09/2026 | Đối soát tuần W38 vs W39)")
    r2.italic = True
    r2.font.name = 'Arial'
    r2.font.size = Pt(10)
    r2.font.color.rgb = RGBColor(100, 116, 139)

    p3 = doc.add_paragraph()
    p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p3.paragraph_format.space_before = Pt(2)
    p3.paragraph_format.space_after = Pt(14)
    r3 = p3.add_run("KỊCH BẢN THUYẾT TRÌNH ĐIỀU HÀNH 16 CHUYÊN ĐỀ — BÓC TÁCH CHI TIẾT 18 AM & 5 TỈNH")
    r3.bold = True
    r3.font.name = 'Arial'
    r3.font.size = Pt(11)
    r3.font.color.rgb = RGBColor(234, 88, 12) # GHN Orange

    # 1. TỔNG QUAN
    add_speech_section(
        doc,
        sec_title="📊 [I. TỔNG HỢP TRỌNG TÂM HỌP TUẦN W39 — VÙNG NAM TRUNG BỘ]",
        speech_heading="🗣️ LỜI MỞ ĐẦU & TỔNG QUAN BỨC TRANH ĐIỀU HÀNH TUẦN W39:",
        paragraphs_text=[
            "Kính thưa Ban Giám Đốc cùng toàn thể các anh chị Quản lý Vận hành (AM), Trưởng bưu cục và các khối phòng ban Vùng Nam Trung Bộ.",
            "Bước vào tuần vận hành W39 (chu kỳ 21/09 đến 27/09/2026), toàn mạng lưới ghi nhận sự nỗ lực rất lớn với sản lượng Full hàng đạt 328.925 đơn (-4,27% WoW, giảm -14.672 đơn so với W38 là 343.597 đơn theo đúng quy luật thị trường sau cao điểm). Điểm sáng vượt bậc và cực kỳ ấn tượng là kênh TikTok Shop (TTS) tiếp tục tăng trưởng bứt phá, đạt 72.781 đơn (+5,90% WoW, tăng thêm +4.055 đơn so với W38 là 68.726 đơn) — chính thức đưa tỷ trọng TTS lên mức kỷ lục 22,1% toàn vùng!",
            "Về chất lượng dịch vụ: Tỷ lệ Giao thành công %GTC cải thiện đồng đều ở cả 2 phân khúc: %GTC Full hàng đạt 56,60% (+0,92%p WoW) và %GTC TikTok Shop đạt 57,45% (+3,55%p WoW). Tỷ lệ Rớt luân chuyển giảm ngoạn mục từ 3,32% xuống chỉ còn 1,52% (-1,81%p WoW). Khâu Lấy hàng First-mile duy trì phong độ vượt trội với %LTC TTS đạt 94,58% và Full hàng đạt 90,12%. Chỉ số Giao đúng hẹn %ODR đạt 90,79% Full hàng và 91,72% TTS.",
            "Tuy nhiên, tuần W39 cũng đặt ra 3 trọng tâm cấp bách cần giải quyết ngay:",
            "Thứ nhất, tỷ lệ tiền mặt COD tăng lên 64% so với 36% chuyển khoản, tiềm ẩn rủi ro tồn quỹ;",
            "Thứ hai, số tiền cần truy thu phát sinh 306,9 triệu đồng trên 4.013 bản ghi do khâu kiểm soát cân đo và lỗi đóng gói;",
            "Thứ ba, danh sách bưu cục cảnh báo tăng từ 13 lên 15 bưu cục, trong đó có 6 bưu cục mới xuất hiện và 9 bưu cục mãn tính cần can thiệp xử lý dứt điểm. Sau đây, em xin phép đi sâu vào từng chuyên đề."
        ],
        insights=[
            "TikTok Shop tăng tốc lên 72.781 đơn (+5,9% WoW) khẳng định Nam Trung Bộ tiếp tục là thị trường tiêu thụ TMĐT cực kỳ sôi động.",
            "Tỷ lệ GTC TTS tăng vọt +3,55%p lên 57,45% và rớt luân chuyển giảm sâu về 1,52% cho thấy các biện pháp kiểm soát vận tải tuần qua đã bắt đầu phát huy hiệu quả rõ rệt."
        ],
        warnings=[
            "Tiền truy thu phát sinh 306,9 triệu đồng tại 4.013 đơn đòi hỏi siết chặt cân đo tại khâu tiếp nhận.",
            "Áp lực bưu cục cảnh báo tăng lên 15 điểm nóng, cần điều tiết tải ngay trong tuần W40."
        ],
        actions=[
            "Quán triệt 3 mệnh lệnh tuần W40: Triển khai Cap Volume giải tỏa bưu cục nghẽn, kiểm soát 100% cân đo tại quầy, và đẩy mạnh thu COD qua VietQR."
        ]
    )

    # 2. SẢN LƯỢNG - CẤU TRÚC CHUẨN XÁC TUẦN TỰ THEO 3 CHART (KHÔNG NHẢY QUA LẠI)
    add_speech_section(
        doc,
        sec_title="📦 [II. PHÂN TÍCH SẢN LƯỢNG GIAO TOÀN VÙNG, 5 TỈNH THÀNH & 18 AM (W39)]",
        speech_heading="🗣️ KỊCH BẢN THUYẾT TRÌNH SẢN LƯỢNG TUẦN TỰ THEO 3 BIỂU ĐỒ TRỰC QUAN:",
        paragraphs_text=[
            "Kính thưa Ban Giám Đốc, phần báo cáo Sản lượng giao tuần W39 được chia thành 3 phần rõ rệt, tương ứng trực tiếp với 3 Biểu đồ trực quan trên màn hình dashboard:",
            "",
            "📊 PHẦN 1: THUYẾT TRÌNH CHART 1 — BỨC TRANH SẢN LƯỢNG FULL HÀNG (CỘT W38 vs W39 + ĐƯỜNG LINE Δ):",
            "(Người thuyết trình chọn Chart 1: Sản lượng Full Hàng)",
            "• Nhìn vào biểu đồ đầu tiên về Sản lượng Full hàng: Tuần W39 toàn vùng chúng ta đạt 328.925 đơn, hạ nhiệt nhẹ -4,27% WoW (-14.672 đơn so với W38 là 343.597 đơn) theo đúng nhịp thị trường sau các đợt mua sắm cao điểm.",
            "• Thứ hạng 5 Tỉnh thành về Full hàng:",
            "  - Khánh Hòa tiếp tục giữ vững vị trí dẫn đầu toàn vùng với 92.696 đơn (W38: 93.615 đơn, giảm nhẹ -919 đơn).",
            "  - Lâm Đồng xếp thứ hai đạt 88.287 đơn (W38: 95.727 đơn, giảm -7.440 đơn do thời tiết mưa bão vùng cao).",
            "  - Bình Thuận đứng thứ ba đạt 80.817 đơn (W38: 85.489 đơn, giảm -4.672 đơn).",
            "  - Đắk Nông đạt 33.883 đơn (giảm -965 đơn) và Ninh Thuận đạt 33.242 đơn (giảm -676 đơn).",
            "• Bóc tách 18 AM trên biểu đồ Full hàng (sắp xếp theo biến động tăng/giảm):",
            "  - Điểm sáng tăng trưởng Full hàng duy nhất toàn mạng: Biểu dương AM Thái Thị Thanh Thư (Khánh Hòa) là AM duy nhất có bước bứt phá ngoạn mục tăng tới +2.227 đơn (+6,8% WoW, từ 32.538 lên 34.765 đơn), chính thức vươn lên vị trí Top 2 sản lượng toàn vùng nhờ khai thác rất tốt sức mua khu vực nội thị Nha Trang!",
            "  - Về quy mô tuyệt đối: AM Nguyễn Duy Long (Bình Thuận) tiếp tục là quán quân số 1 gánh tải lớn nhất vùng với 42.506 đơn (chiếm 12,9% sản lượng toàn mạng, giảm nhẹ -512 đơn).",
            "  - Top các AM gánh tải lớn tiếp theo gồm: AM Lê Thanh Nhựt (29.070 đơn), AM Lê Văn Trường (26.787 đơn), AM Nguyễn Ngọc Khánh (26.242 đơn), AM Trần Thị Nhung (24.581 đơn), AM Phan Đình Duy (23.282 đơn).",
            "  - Nhóm các AM suy giảm đơn theo nhịp thị trường: Lượng giảm tập trung ở AM Lê Văn Trường (-2.132 đơn), AM Nguyễn Ngọc Khánh (-2.083 đơn), AM Phan Đình Duy (-1.649 đơn), AM Lê Thanh Nhựt (-1.530 đơn) do sức mua các shop đầu nguồn tạm chững lại.",
            "",
            "⚡ PHẦN 2: THUYẾT TRÌNH CHART 2 — ĐIỂM SÁNG BỨT PHÁ TIKTOK SHOP (CỘT TTS W38 vs W39 + LINE Δ):",
            "(Người thuyết trình bấm chuyển sang Chart 2: Sản lượng TikTok Shop)",
            "• Kính mời Ban Giám Đốc nhìn sang biểu đồ thứ hai — đây chính là điểm sáng rực rỡ nhất trong tuần W39 đến từ kênh TikTok Shop (TTS):",
            "• Tăng trưởng toàn vùng: Sản lượng TTS bứt phá mạnh mẽ đạt 72.781 đơn, tăng thêm +4.055 đơn (+5,90% WoW so với W38: 68.726 đơn)! Đặc biệt, toàn bộ 5/5 tỉnh thành đều ghi nhận đà tăng trưởng dương ở phân khúc này.",
            "• Thứ hạng 5 Tỉnh thành về TikTok Shop:",
            "  - Lâm Đồng tiếp tục là thị trường tiêu thụ TikTok Shop lớn nhất vùng với 19.283 đơn (chiếm 26,5% sản lượng TTS toàn mạng).",
            "  - Bình Thuận tăng trưởng mạnh nhất khu vực đạt 18.146 đơn (tăng vọt +2.273 đơn WoW, tăng +14,3% so với W38: 15.873 đơn).",
            "  - Khánh Hòa bám sát đạt 18.043 đơn (tăng +449 đơn WoW).",
            "  - Hai tỉnh Tây Nguyên tăng trưởng rất ấn tượng: Ninh Thuận đạt 8.293 đơn (tăng +935 đơn WoW, +12,7%) và Đắk Nông đạt 9.016 đơn (tăng +702 đơn WoW, +8,4%).",
            "• Bóc tách 18 AM trên biểu đồ TTS (ghi nhận tới 12/18 AM tăng trưởng dương):",
            "  - Quán quân TTS toàn vùng: AM Nguyễn Duy Long dẫn đầu tuyệt đối với 10.584 đơn TTS, đồng thời là người có mức tăng trưởng TTS cao nhất toàn mạng khi tăng thêm +1.379 đơn (+15,0% WoW)! Riêng AM Long đã chiếm gần 15% tổng lượng đơn TTS cả vùng.",
            "  - Nhóm AM tăng trưởng TTS xuất sắc tiếp theo: AM Lê Thanh Nhựt tăng +800 đơn (đạt 7.108 đơn), AM Hồng Bích Nga tăng +610 đơn (đạt 4.900 đơn), AM Nguyễn Hoàng Phi tăng +593 đơn (đạt 5.390 đơn), AM Phan Đình Duy tăng +531 đơn (đạt 5.347 đơn), AM Nguyễn Ngọc Khánh tăng +516 đơn (đạt 5.155 đơn), AM Cao Thị Thanh Thủy tăng +513 đơn (đạt 3.592 đơn), AM Thái Thị Thanh Thư tăng +511 đơn (đạt 5.562 đơn), AM Trần Thị Nhung tăng +379 đơn (đạt 6.057 đơn), AM Lê Văn Trường đạt 5.440 đơn (+131 đơn).",
            "  - Hai AM suy giảm TTS cần lưu ý: AM Nguyễn Thanh Long giảm -1.186 đơn (đạt 1.744 đơn) do một số shop thời trang lớn tạm nghỉ live tại Cam Ranh, và AM Lê Minh Lợi giảm -637 đơn (đạt 207 đơn).",
            "",
            "📦 PHẦN 3: THUYẾT TRÌNH CHART 3 — TỶ TRỌNG TTS TRONG FULL HÀNG & CƠ CẤU MẠNG LƯỚI 18 AM:",
            "(Người thuyết trình bấm chuyển sang Chart 3: So Sánh Full Hàng vs TTS)",
            "• Kính mời Ban Giám Đốc chuyển sang biểu đồ thứ ba — biểu đồ so sánh cơ cấu tương quan giữa Full Hàng, TTS và đường % Tỷ Trọng:",
            "• Tỷ trọng TTS toàn vùng lập đỉnh mới: Đạt mức kỷ lục 22,1% (tăng từ mức 20,0% của các tuần trước). Điều này có nghĩa là cứ 5 đơn hàng giao ra trên toàn vùng thì có hơn 1 đơn là hàng TikTok Shop!",
            "• Bóc tách tỷ trọng phụ thuộc TTS trên từng AM (xếp theo sản lượng Full từ cao xuống thấp):",
            "  - Nhóm AM có tỷ trọng TTS cao vượt trội (> 24% – 29%): Dẫn đầu là AM Huỳnh Thúc Duân (tỷ trọng TTS chiếm tới 29,0%), AM Nguyễn Hoàng Phi (25,1%), AM Nguyễn Duy Long (24,9%), AM Nguyễn Thị Tuyết Thơ (24,7%), AM Trần Thị Nhung (24,6%), AM Lê Thanh Nhựt (24,5%), AM Nguyễn Lê Nguyên Vũ (24,5%), AM Hồng Bích Nga (23,9%). Đây là các địa bàn mà sự tăng trưởng doanh thu gắn chặt với sức khỏe của sàn TikTok Shop, cần ưu tiên nhân lực lấy hàng và bảo vệ SLA ca sáng!",
            "  - Nhóm AM giữ tỷ trọng TTS cân bằng (20% – 23%): Gồm AM Phan Đình Duy (23,0%), AM Nguyễn Đỗ Minh Nghĩa (22,4%), AM Cao Thị Thanh Thủy (22,1%), AM Huỳnh Thị Kim Chi (22,1%), và AM Lê Văn Trường (20,3%).",
            "  - Nhóm AM có tỷ trọng TTS còn thấp (< 18%): AM Thái Thị Thanh Thư (16,0% — dù sản lượng Full rất lớn 34.7k đơn nhưng chủ yếu là khách hàng TMĐT sàn khác và hàng truyền thống), AM Nguyễn Thanh Long (13,2%), và AM Lê Minh Lợi (8,2%). Đây là những cụm bưu cục còn rất nhiều dư địa để khối Kinh doanh đẩy mạnh tiếp cận các shop TikTok Shop mới trong các tuần tới."
        ],
        insights=[
            "Biểu đồ 1 cho thấy Full hàng hạ nhiệt theo nhịp thị trường nhưng AM Thái Thị Thanh Thư (+2.227 đơn) và AM Nguyễn Duy Long (42.5k đơn) giữ vững trận địa sản lượng.",
            "Biểu đồ 2 khẳng định TikTok Shop là động lực tăng trưởng số 1 của toàn vùng với 72.781 đơn (+5,9% WoW), lan tỏa trên cả 5 tỉnh và 12/18 AM.",
            "Biểu đồ 3 chỉ ra cơ cấu tỷ trọng TTS đạt đỉnh 22,1%, định hình rõ 2 nhóm AM: nhóm phụ thuộc mạnh vào TMĐT livestream (cần ưu tiên SLA) và nhóm còn dư địa mở rộng thị phần."
        ],
        warnings=[
            "Sự sụt giảm TTS của AM Nguyễn Thanh Long (-1.186 đơn) tại Cam Ranh cần được khối Kinh doanh rà soát để kịp thời giữ chân các shop live lớn."
        ],
        actions=[
            "Khối Kinh doanh đẩy mạnh khai thác shop F30 phân khúc TikTok Shop tại cụm Nha Trang (AM Thư) và Cam Ranh (AM Long) để gia tăng sản lượng trong tuần W40."
        ]
    )

    # 3. GTC TỔNG
    add_speech_section(
        doc,
        sec_title="🎯 [III. PHÂN TÍCH HIỆU SUẤT %GTC TỔNG TOÀN MẠNG THEO 18 AM & 5 TỈNH (W39)]",
        speech_heading="🗣️ PHÂN TÍCH TỶ LỆ GIAO THÀNH CÔNG (%GTC) 5 TỈNH & NGHỊCH LÝ ĐIỀU HÀNH 18 AM:",
        paragraphs_text=[
            "Kính thưa Ban Giám Đốc, về tỷ lệ Giao Thành Công (%GTC Tổng) — chỉ số phản ánh năng lực xả hàng Last-mile thực tế:",
            "• Mặt bằng chung toàn vùng: Tuần W39 ghi nhận sự phục hồi rất tích cực: %GTC Full hàng đạt 56,60% (tăng +0,92%p WoW so với W38: 55,68%) và %GTC TikTok Shop bứt phá đạt 57,45% (tăng mạnh +3,55%p WoW so với W38: 53,90%)!",
            "• Đánh giá theo 5 Tỉnh thành:",
            "- Ninh Thuận xuất sắc vươn lên dẫn đầu toàn vùng với %GTC Full đạt 67,96% (+2,28%p WoW) và TTS đạt 68,09% (+5,00%p WoW).",
            "- Bình Thuận giữ vững vị trí thứ hai với %GTC Full đạt 67,49% và TTS đạt 67,94%.",
            "- Khánh Hòa có bước tiến vượt bậc nhất vùng: %GTC Full tăng vọt +3,57%p lên 58,56% (W38: 54,99%) và TTS nhảy vọt +5,78%p lên 59,60% (W38: 53,82%) nhờ dọn dẹp xong điểm nghẽn tại cụm Cam Linh và Nha Trang!",
            "- Đắk Nông cải thiện lên 48,81% Full (+1,97%p) và TTS đạt 49,56% (+5,07%p).",
            "- Lâm Đồng đạt 47,38% Full và TTS đạt 48,73% (+1,79%p) — đây là địa bàn cần tập trung giải cứu khẩn cấp vì vẫn dưới ngưỡng 50% do vướng cụm Đà Lạt, Đơn Dương, Đức Trọng."
        ],
        insights=[
            "Khánh Hòa là hình mẫu phục hồi thành công nhất tuần qua khi tăng tới +5,78%p TTS lên 59,60%.",
            "Ninh Thuận và Bình Thuận tiếp tục là 2 bức tường thành kiên cố bảo vệ tỷ lệ GTC toàn vùng trên 67%."
        ],
        warnings=[
            "Lâm Đồng và Đắk Nông vẫn dưới mốc 50% GTC, nguyên nhân chủ yếu do các bưu cục đồi núi bị dồn ứ đơn tồn."
        ],
        actions=[
            "Áp dụng ngay cơ chế chi viện bưu tá và điều tiết tải cho cụm Lâm Đồng để đưa %GTC vượt ngưỡng 52% trong tuần W40."
        ]
    )

    # 4. GTC CA 1 SÁNG TTS
    add_speech_section(
        doc,
        sec_title="🔥 [IV. PHÂN TÍCH CHUYÊN SÂU %GTC CA 1 TIKTOK SHOP (TARGET SLA ≥ 76.0%) (W39)]",
        speech_heading="🗣️ MỔ XẺ CHUYÊN SÂU HIỆU SUẤT GIAO CA 1 SÁNG TIKTOK SHOP (TARGET SLA ≥ 76.0%):",
        paragraphs_text=[
            "Kính thưa Ban Giám Đốc, về hiệu suất Ca 1 sáng TikTok Shop (Ca 1 thuần) — chỉ số cam kết SLA khắt khe nhất với sàn:",
            "• Bức tranh toàn vùng Ca 1 sáng TTS: Tuần W39 ghi nhận bước tiến nhảy vọt khi tỷ lệ giao thành công Ca 1 thuần TTS toàn vùng đạt 75,10% (tăng mạnh +3,84%p WoW so với W38: 71,26%), tiệm cận sát nút mục tiêu chuẩn xanh SLA 76,0%!",
            "• Đánh giá 5 Tỉnh thành:",
            "- Dẫn đầu vượt chuẩn xanh: Ninh Thuận xuất sắc đạt 84,75% (+3,04%p WoW) và Bình Thuận đạt 84,64% — cả 2 tỉnh vượt xa chuẩn cam kết của sàn.",
            "- Điểm sáng bứt phá mạnh nhất: Khánh Hòa tăng vọt +7,95%p từ 67,58% lên 75,53%, áp sát ngưỡng 76%.",
            "- Hai tỉnh cần tăng tốc: Đắk Nông đạt 67,81% (+2,71%p WoW) và Lâm Đồng đạt 66,85% (+2,89%p WoW). Cả 2 tỉnh đều tăng trưởng nhưng vẫn cần siết kỷ luật xuất tuyến sáng trước 08h15 để bứt phá khỏi vùng trũng."
        ],
        insights=[
            "Tỷ lệ Ca 1 thuần TTS tăng lên 75,10% (+3,84%p WoW) cho thấy kỷ luật xuất tuyến sáng tại Khánh Hòa và duyên hải đã được thiết lập lại bài bản.",
            "Khung giờ vàng 08h30 - 11h30 quyết định 80% thành công của đơn TikTok Shop giao tại cơ quan công sở."
        ],
        warnings=[
            "Lâm Đồng và Đắk Nông vẫn dưới 68% Ca 1 sáng do địa hình đèo dốc và bưu tá chia chọn trễ giờ."
        ],
        actions=[
            "Bắt buộc 100% bưu cục Lâm Đồng và Đắk Nông phải hoàn tất chia chọn trước 08h00 và xuất tuyến trước 08h15."
        ]
    )

    # 5. GÁN VẬN HÀNH
    add_speech_section(
        doc,
        sec_title="📋 [V. TỶ LỆ GÁN VẬN HÀNH TOÀN MẠNG THEO CA 1, CA 2 & GÁN TỔNG (TARGET ≥ 90.0%) (W39)]",
        speech_heading="🗣️ KIỂM SOÁT TỶ LỆ GÁN ĐƠN GIAO: GÁN SÁNG ĐẠT CHUẨN — TỬ HUYỆT GÁN CA 2:",
        paragraphs_text=[
            "Kính thưa Ban Giám Đốc, về tỷ lệ gán đơn giao — thước đo tính kỷ luật giải phóng hàng khỏi sàn kho:",
            "• Toàn vùng tuần W39: Tỷ lệ gán tổng cải thiện tích cực: Full hàng đạt 82,41% (+1,87%p WoW so với W38: 80,54%) và TTS đạt 82,77% (+2,64%p WoW so với W38: 80,13%).",
            "• Phân tích theo ca gán:",
            "- Gán Ca 1 + Tồn: Đạt tỷ lệ rất tốt với 87,41% Full hàng và 88,17% TTS (tiệm cận chuẩn xanh 90%).",
            "- Gán Ca 2 buổi chiều: Đã có chuyển biến đáng khích lệ khi tăng từ 56,67% lên 59,10% Full hàng (+2,43%p WoW) và TTS tăng từ 53,20% lên 58,33% (+5,13%p WoW). Tuy nhiên, mức 58-59% vẫn còn cách rất xa chuẩn 90%, đồng nghĩa hơn 40% hàng KTC cập bến buổi trưa vẫn bị để lại bưu cục qua đêm!",
            "• Yêu cầu trọng tâm: Khâu Gán Ca 2 tiếp tục là tử huyệt số 1 cần giải quyết dứt điểm để bảo vệ ODR và tránh dồn ứ đơn sàn."
        ],
        insights=[
            "Gán Ca 2 tăng +5,13%p ở TTS chứng minh các bưu cục đã bắt đầu bố trí nhân sự quét hàng trưa, nhưng tỷ lệ còn thấp (58,33%).",
            "Việc gán dứt điểm hàng trưa là chìa khóa then chốt để kéo GTC tổng vượt mốc 60%."
        ],
        warnings=[
            "Hơn 40% hàng KTC trưa chưa gán kịp trong ngày làm tăng nguy cơ quá hạn SLA 24h và tạo gánh nặng tồn cho sáng hôm sau."
        ],
        actions=[
            "Áp dụng ca trực lệch giờ từ 12h30 đến 13h30 tại 100% bưu cục, quyết tâm kéo tỷ lệ gán Ca 2 lên trên 75% trong tuần W40."
        ]
    )

    # 6. ODR GIAO ĐÚNG HẸN
    add_speech_section(
        doc,
        sec_title="⏱️ [VI. PHÂN TÍCH HIỆU SUẤT %ODR (GIAO ĐÚNG HẸN SLA) TOÀN VÙNG (TARGET ≥ 92.0%) (W39)]",
        speech_heading="🗣️ PHÂN TÍCH CHỈ SỐ ĐÚNG HẸN %ODR THEO 5 TỈNH VÀ NGHỊCH LÝ ĐIỀU HÀNH 18 AM:",
        paragraphs_text=[
            "Kính thưa Ban Giám Đốc, về chỉ số cam kết chất lượng dịch vụ Giao Đúng Hẹn (%ODR):",
            "• Toàn vùng tuần W39: %ODR Full hàng đạt 90,79% (W38: 91,19%) và %ODR kênh TikTok Shop đạt 91,72% (tăng +0,24%p WoW so với W38: 91,48%). Kênh TTS bảo vệ rất tốt ngưỡng cam kết sát vạch 92%.",
            "• Xếp hạng 5 Tỉnh thành:",
            "- Ninh Thuận và Bình Thuận là lá chắn thép vững chắc nhất toàn vùng: Ninh Thuận đạt 96,43% Full và Bình Thuận đạt 96,27% Full — cả 2 đều vượt xa chuẩn xanh 92%.",
            "- Khánh Hòa giữ phong độ ổn định đạt 91,76% Full hàng (+0,89%p WoW) và TTS đạt 92,30%.",
            "- Hai tỉnh Tây Nguyên gặp khó khăn do đơn tồn tích tụ: Đắk Nông đạt 88,53% Full và Lâm Đồng đạt 84,69% Full. Đây là lý do chính kéo ODR trung bình toàn vùng xuống 90,79%."
        ],
        insights=[
            "ODR kênh TikTok Shop (91,72%) cao hơn Full hàng (90,79%) cho thấy bưu tá đã nhận thức rõ chế tài phạt của sàn TMĐT.",
            "Lâm Đồng bị tụt ODR xuống 84,69% do hàng aging tích tụ tại các bưu cục điểm nóng như Lâm Viên 2, Đơn Dương, Đức Trọng 1."
        ],
        warnings=[
            "Cần tránh tình trạng bưu tá chỉ lựa đơn mới để giao lấy ODR mà bỏ rơi các đơn hàng cũ, gây tích tụ đơn tồn đọng."
        ],
        actions=[
            "Giao chỉ tiêu xả tồn aging cho từng AM tại Lâm Đồng và Đắk Nông; bắt buộc bưu tá mang 100% đơn tuyến đi giao trong ngày."
        ]
    )

    # 7. LTC LẤY THÀNH CÔNG
    add_speech_section(
        doc,
        sec_title="🚚 [VII. PHÂN TÍCH CHỈ SỐ %LTC (LẤY THÀNH CÔNG) THEO 18 AM & 5 TỈNH (TARGET ≥ 90.0%) (W39)]",
        speech_heading="🗣️ ĐIỂM SÁNG RỰC RỠ FIRST-MILE: %LTC TIKTOK SHOP ĐẠT ĐỈNH CAO 94.58%:",
        paragraphs_text=[
            "Kính thưa Ban Giám Đốc, khâu Lấy hàng First-mile tuần W39 tiếp tục là điểm tựa vững chắc nhất của toàn mạng lưới:",
            "• Toàn vùng tuần W39: %LTC kênh TikTok Shop đạt mức rất cao 94,58% và Full hàng đạt 90,12% — cả 2 phân khúc đều bảo vệ vững chắc chuẩn xanh SLA ≥ 90,0%!",
            "• Đánh giá 5 Tỉnh thành:",
            "- Ninh Thuận quán quân toàn mạng với %LTC Full đạt 96,10% (+0,98%p WoW).",
            "- Khánh Hòa đạt 91,30% Full và Lâm Đồng đạt 90,18% Full (+0,96%p WoW).",
            "- Đắk Nông đạt 87,79% và Bình Thuận đạt 86,26% đối với Full hàng do đặc thù shop nông sản phân tán xa trung tâm.",
            "• Khâu lấy hàng First-mile hoạt động ổn định giúp giữ vững niềm tin của các shop và đối tác thương mại điện tử lớn trên toàn địa bàn."
        ],
        insights=[
            "Tỷ lệ LTC TTS đạt 94,58% khẳng định đội ngũ bưu tá lấy hàng phối hợp rất nhịp nhàng với các nhà bán lẻ và shop livestream.",
            "First-mile là mắt xích mạnh nhất trong chuỗi cung ứng của NTB hiện tại."
        ],
        warnings=[
            "Cần lưu ý kiểm tra cân đo kích thước ngay tại thời điểm lấy hàng để chặn đứng nguy cơ truy thu cước phát sinh sau này."
        ],
        actions=[
            "Trang bị bổ sung cân điện tử cầm tay cho bưu tá đi lấy hàng tại các shop nông sản và hàng cồng kềnh."
        ]
    )

    # 8. OPR TIKTOK SHOP
    add_speech_section(
        doc,
        sec_title="🌙 [VIII. PHÂN TÍCH CHỈ SỐ %OPR TIKTOK SHOP TOÀN VÙNG (TARGET KPI ≥ 80.0%) (W39)]",
        speech_heading="🗣️ ĐÁNH GIÁ CHUYÊN SÂU %OPR TỔNG TIKTOK SHOP: TOÀN VÙNG VƯỢT CHUẨN XANH:",
        paragraphs_text=[
            "Kính thưa Ban Giám Đốc, về chỉ số %OPR Tổng TikTok Shop — tỷ lệ xử lý đơn hàng và bàn giao luân chuyển đúng cam kết toàn trình (Target KPI ≥ 80,0%):",
            "• Toàn vùng tuần W39: Chỉ số OPR Tổng TTS toàn vùng duy trì ở mức cao trên 83,0%, tiếp tục giữ vững sắc xanh chuẩn KPI.",
            "• Đánh giá các tỉnh thành:",
            "- Ninh Thuận và Bình Thuận dẫn đầu với OPR trên 89-90%, xử lý nhanh gọn và không để hàng trôi ca.",
            "- Khánh Hòa duy trì mức tốt trên 85%.",
            "- Lâm Đồng đạt trên 74% và Đắk Nông đạt 72%, đã có sự cải thiện rõ rệt so với các tuần trước nhưng cần tập trung tối ưu ca đêm tại các trạm trung chuyển để không bị trễ chuyến xe KTC liên tỉnh."
        ],
        insights=[
            "OPR TTS giữ vững trên 83% giúp toàn vùng không bị sàn TikTok áp các mức phạt cảnh cáo về thời gian luân chuyển.",
            "Nút thắt ca đêm tại Hub Cam Ranh và trung chuyển Lâm Đồng đã được tháo gỡ một phần."
        ],
        warnings=[
            "Cần duy trì giám sát camera quét kiện ban đêm để tránh tình trạng đơn hàng bị bỏ quên tại góc kho."
        ],
        actions=[
            "Bố trí trưởng ca kiểm kê quét đối soát 100% trước khi xe tải KTC lăn bánh rời hub."
        ]
    )

    # 9. RỚT LUÂN CHUYỂN
    add_speech_section(
        doc,
        sec_title="🚨 [IX. PHÂN TÍCH TỶ TRỌNG RỚT ĐƠN LUÂN CHUYỂN THEO AM & TỈNH THÀNH (W39)]",
        speech_heading="🗣️ BỨT PHÁ NGOẠN MỤC: TỶ LỆ RỚT LUÂN CHUYỂN GIẢM TỪ 3.32% XUỐNG CÒN 1.52%:",
        paragraphs_text=[
            "Kính thưa Ban Giám Đốc, chuyên đề thứ 9 ghi nhận một trong những thành tích điều hành nổi bật nhất của tuần W39:",
            "• Tỷ lệ Rớt luân chuyển toàn vùng đã giảm ngoạn mục từ 3,32% ở tuần W38 xuống chỉ còn 1,52% trong tuần W39 (giảm sâu -1,81%p WoW, tương ứng giảm hơn 54% lượng đơn rớt)!",
            "• Đây là kết quả trực tiếp của việc Ban Điều Hành siết chặt quy trình đóng bao điện tử và giám sát biên bản bàn giao xe KTC liên tỉnh.",
            "• Điểm nóng rớt đơn tuần trước tại Khánh Hòa và Đắk Nông đã được giải tỏa cơ bản. Lượng đơn rớt luân chuyển toàn vùng giảm về mức an toàn dưới 120 đơn, xóa tan nguy cơ thất thoát và chậm trễ đơn hàng."
        ],
        insights=[
            "Biện pháp quét barcode bao kiện và kiểm tra chéo giữa tài xế KTC và thủ kho đã phát huy tác dụng ngay lập tức.",
            "Tỷ lệ rớt LC giảm về 1,52% giúp tiết kiệm hàng chục triệu đồng chi phí tìm kiếm đơn thất lạc."
        ],
        warnings=[
            "Tuyệt đối không chủ quan; các trạm trung chuyển đèo dốc vẫn có nguy cơ rớt hàng vào những ngày mưa bão."
        ],
        actions=[
            "Duy trì quy định tài xế và thủ kho cùng ký biên bản quét mã bao 100% trước khi xe xuất bến."
        ]
    )

    # 10. FD HOÀN TRẢ
    add_speech_section(
        doc,
        sec_title="🔄 [X. BÁO CÁO TỶ LỆ %FD (RETURN / HOÀN TRẢ) — VÙNG NAM TRUNG BỘ (W39)]",
        speech_heading="🗣️ KIỂM SOÁT TỶ LỆ HOÀN TRẢ (%FD) 7.7% TOÀN VÙNG VÀ BÓC TÁCH CHI PHÍ:",
        paragraphs_text=[
            "Kính thưa Ban Giám Đốc, về tỷ lệ hàng hoàn trả (%FD):",
            "• Toàn vùng tuần W39 ghi nhận tỷ lệ %FD ở mức 7,7%, tương đương khoảng 25.300 đơn hàng hoàn trả ngược về cho người gửi.",
            "• Bóc tách nguyên nhân:",
            "- Hơn 65% đơn hoàn trả xuất phát từ lý do 'Khách không liên lạc được' hoặc 'Khách đổi ý / hủy đơn' tại các địa bàn nông thôn xa xôi.",
            "- Một bộ phận bưu tá chưa quyết liệt liên hệ lại lần 2, lần 3 trước khi bấm hoàn, làm tỷ lệ hoàn tăng cục bộ tại một số bưu cục Đắk Nông và Lâm Đồng.",
            "• Việc kéo giảm 1% tỷ lệ FD sẽ giúp tiết kiệm hàng trăm triệu đồng chi phí vận chuyển ngược và tăng tỷ lệ giao thành công cho toàn vùng."
        ],
        insights=[
            "Tỷ lệ hoàn hàng tập trung cao ở các đơn COD giá trị thấp hoặc hàng thời trang mua theo cảm xúc trên livestream.",
            "Bưu tá có thâm niên gọi điện trước thường có tỷ lệ hoàn thấp hơn 3-4%p so với bưu tá mới."
        ],
        warnings=[
            "Hàng hoàn lưu cữu tại bưu cục quá 48h sẽ làm tăng nguy cơ thất lạc và khiếu nại từ người bán."
        ],
        actions=[
            "Quy định bắt buộc gọi tối thiểu 3 cuộc điện thoại ở các khung giờ khác nhau trước khi cập nhật trạng thái hoàn đơn."
        ]
    )

    # 11. KTC & VẬN TẢI
    add_speech_section(
        doc,
        sec_title="🚛 [XI. BÁO CÁO ĐIỀU HÀNH KTC, VẬN TẢI, %TLTĐ THÙNG XE & LEADTIME (W39)]",
        speech_heading="🗣️ TỐI ƯU HÓA VẬN TẢI KTC: NÂNG CAO TỶ LỆ LẤP ĐẦY THÙNG XE VÀ RÚT NGẮN LEADTIME:",
        paragraphs_text=[
            "Kính thưa Ban Giám Đốc, về công tác vận chuyển kết nối trung chuyển (KTC):",
            "• Tỷ lệ trọng tải lấp đầy (%TLTĐ) thùng xe tuần W39 đạt mức trung bình 52,5%, đã có sự cải thiện nhẹ so với mức 51,0% tuần trước nhờ cắt giảm bớt các chuyến xe rỗng tuyến ngắn.",
            "• Tuy nhiên, số chuyến xe chạy dưới 35% tải vẫn còn ghi nhận ở các tuyến nhánh Đắk Nông và Ninh Thuận, gây lãng phí chi phí nhiên liệu và khấu hao xe.",
            "• Về Leadtime luân chuyển: Toàn trình nội vùng đạt chuẩn 98,2% đúng giờ, đảm bảo hàng hóa cập bến bưu cục phát trước 06h30 sáng cho Ca 1 và trước 13h00 trưa cho Ca 2."
        ],
        insights=[
            "Gom chuyến linh hoạt giữa các bưu cục lân cận là giải pháp hiệu quả nhất để nâng %TLTĐ lên trên 60%.",
            "Leadtime xe KTC đúng giờ là điều kiện tiên quyết giúp bưu cục phát xuất tuyến sáng đúng 08h00."
        ],
        warnings=[
            "Chi phí xe rỗng tải là khoản lãng phí vô hình lớn nhất của khối vận tải cần triệt để cắt giảm."
        ],
        actions=[
            "Khối Vận Tải rà soát biểu đồ chạy xe, ghép tuyến các bưu cục khối lượng thấp để giảm tối thiểu 15 chuyến xe non tải trong tuần W40."
        ]
    )

    # 12. AGING & TREO LUÂN CHUYỂN
    add_speech_section(
        doc,
        sec_title="📦 [XII. ĐIỀU HÀNH XỬ LÝ HÀNG AGING TỒN ĐỌNG & TREO LUÂN CHUYỂN (W39)]",
        speech_heading="🗣️ CẬP NHẬT DỮ LIỆU THỰC TẾ: BÓC TÁCH 1.468 ĐƠN AGING LƯU KHO VÀ 4.251 ĐƠN TREO LUÂN CHUYỂN:",
        paragraphs_text=[
            "Kính thưa Ban Giám Đốc, về tình hình hàng tồn kho aging và treo luân chuyển tính đến tuần W39:",
            "• Hàng Aging lưu kho (Tổng 1.468 đơn tồn ≥ 5 ngày):",
            "- Trong đó, nhóm tồn từ 5 - 8 ngày chiếm đa số với 1.136 đơn (77,4%); nhóm tồn nguy hiểm trên 8 ngày có 332 đơn.",
            "- Địa bàn tập trung: Hai tỉnh Tây Nguyên Lâm Đồng và Đắk Nông chiếm tới trên 80% tổng lượng hàng aging toàn vùng, tập trung tại các bưu cục như Lâm Viên 2, Tân Hà, Di Linh, Quảng Tín.",
            "• Hàng Treo luân chuyển (Tổng 4.251 đơn):",
            "- Luân chuyển đúng hạn (< 24h): Có 3.735 đơn (chiếm 87,9%) — đang di chuyển bình thường theo đúng nhịp luân chuyển.",
            "- Bóc tách đơn treo quá hạn (Tổng 516 đơn, chiếm 12,1%): Treo chớm trễ 24h – 36h có 153 đơn; treo nguy hiểm 36h – 72h có 199 đơn; và treo đặc biệt nghiêm trọng trên 72h có 164 đơn.",
            "• Kế hoạch giải tỏa: Khối Vận hành đã kích hoạt chiến dịch 'Xả kho cấp tốc', đặt mục tiêu quét sạch 516 đơn treo quá hạn và giảm 50% lượng hàng aging >5 ngày ngay trong 3 ngày đầu tuần W40."
        ],
        insights=[
            "Đơn treo quá hạn chủ yếu do vướng các kiện hàng sai địa chỉ hoặc hàng đóng gói rách vỡ đang chờ xác minh.",
            "Hàng aging trên 5 ngày nếu không xử lý dứt điểm sẽ biến thành hàng mất mát và phát sinh tiền bồi thường truy thu."
        ],
        warnings=[
            "516 đơn treo quá hạn ≥24h nếu không được cập nhật trạng thái sẽ bị hệ thống tự động tính lỗi SLA toàn trình."
        ],
        actions=[
            "Thành lập tổ đặc nhiệm quét sạch 516 đơn treo quá hạn trước 17h00 ngày 30/09; quy trách nhiệm cụ thể cho từng thủ kho."
        ]
    )

    # 13. COD DÒNG TIỀN
    add_speech_section(
        doc,
        sec_title="💰 [XIII. QUẢN TRỊ DÒNG TIỀN COD, TỶ LỆ TIỀN MẶT 64% & CHUYỂN ĐỔI SỐ VIETQR (W39)]",
        speech_heading="🗣️ QUẢN TRỊ DÒNG TIỀN COD TOÀN VÙNG: BÁO ĐỘNG TỶ LỆ TIỀN MẶT VẪN Ở MỨC CAO 64%:",
        paragraphs_text=[
            "Kính thưa Ban Giám Đốc, về công tác quản trị dòng tiền thu hộ COD tuần W39:",
            "• Bức tranh dòng tiền toàn vùng: Tỷ lệ thu tiền mặt hiện chiếm tới 64,0%, trong khi thanh toán không dùng tiền mặt (VietQR / chuyển khoản) chỉ đạt 36,0%. Mặc dù tỷ lệ tiền mặt đã giảm nhẹ -2,4%p so với tuần trước, nhưng con số 64% vẫn là một rủi ro tài chính rất lớn!",
            "• Rủi ro tồn quỹ tiền mặt: Việc bưu tá giữ hàng chục tỷ đồng tiền mặt lưu động trên đường và tại két sắt bưu cục đối mặt với rủi ro mất cắp, chậm nộp và chiếm dụng vốn.",
            "• Điểm sáng chuyển đổi số: Các tuyến trung tâm Nha Trang (Khánh Hòa) và Phan Thiết (Bình Thuận) có tỷ lệ quét VietQR đạt trên 55-60%, trong khi các vùng sâu Lâm Đồng và Đắk Nông tỷ lệ tiền mặt vẫn trên 75%.",
            "• Mục tiêu W40: Đẩy mạnh hướng dẫn khách hàng quét mã VietQR trên app bưu tá, phấn đấu nâng tỷ lệ thanh toán số lên trên 45% toàn khu vực."
        ],
        insights=[
            "Thanh toán VietQR giúp tiền về ngay tài khoản công ty, xóa bỏ 100% rủi ro chiếm dụng và sai lệch tiền mặt.",
            "Khách hàng ngoại thành vẫn có thói quen dùng tiền mặt, cần khuyến khích bưu tá kiên nhẫn mời quét mã QR."
        ],
        warnings=[
            "Tỷ lệ tiền mặt 64% tiềm ẩn nguy cơ chậm nộp COD và chênh lệch sổ sách cuối ngày."
        ],
        actions=[
            "Gắn KPI tỷ lệ thanh toán VietQR tối thiểu ≥40% vào đánh giá thi đua tuần của từng AM và bưu tá."
        ]
    )

    # 14. TRUY THU
    add_speech_section(
        doc,
        sec_title="⚖️ [XIV. BÁO CÁO TRUY THU CƯỚC & LỖ HỔNG CÂN ĐO 306.9 TRIỆU ĐỒNG (W39)]",
        speech_heading="🗣️ BÁO ĐỘNG ĐỎ TRUY THU TUẦN W39: PHÁT SINH 306.9 TRIỆU ĐỒNG TRÊN 4.013 BẢN GHI:",
        paragraphs_text=[
            "Kính thưa Ban Giám Đốc, chuyên đề thứ 14 là hồi chuông cảnh tỉnh nghiêm khắc nhất về kỷ luật nghiệp vụ quầy tiếp nhận:",
            "• Quy mô truy thu tuần W39: Toàn vùng phát sinh 4.013 bản ghi truy thu (tăng đột biến +3.878 đơn) với tổng số tiền cần truy thu lên tới 306,9 triệu đồng (tăng +303,0 triệu đồng so với mức 3,9 triệu đồng rất thấp của tuần W38)!",
            "• Bóc tách các nhóm vi phạm trọng điểm:",
            "- 1. Backlog Giao Hàng: Chiếm 109,2 triệu đồng trên 742 đơn vi phạm;",
            "- 2. Backlog Luân Chuyển Trả: Chiếm 53,6 triệu đồng trên 559 đơn;",
            "- 3. Đơn hàng hư hỏng / bể vỡ: Chiếm 25,5 triệu đồng trên 254 đơn;",
            "- Cùng các khoản truy thu sai lệch kích thước cân nặng ba chiều và thao tác sai quy trình.",
            "• Top 4 AM có số tiền truy thu lớn nhất: AM Huỳnh Thị Kim Chi (58,3 triệu đồng | 177 ticket), AM Hồng Bích Nga (50,7 triệu đồng | 104 ticket), AM Lê Văn Trường (50,6 triệu đồng | 722 ticket), và AM Trần Văn Phước (27,1 triệu đồng | 706 ticket). Riêng 4 AM này đã chiếm hơn 60% tổng số tiền truy thu toàn vùng!"
        ],
        insights=[
            "Lỗ hổng bắt nguồn từ việc nhân viên tiếp nhận nể nang khách quen, không cân đo lại kiện hàng cồng kềnh và đóng gói sơ sài.",
            "Truy thu backlog cho thấy khâu cập nhật biên bản tồn kho bị chậm trễ nhiều ngày."
        ],
        warnings=[
            "Nếu không xử lý dứt điểm, khoản truy thu 306,9 triệu đồng này sẽ trực tiếp ăn mòn lợi nhuận và tạo tiền lệ xấu về kỷ luật."
        ],
        actions=[
            "Yêu cầu 4 AM (Kim Chi, Bích Nga, Văn Trường, Văn Phước) thu hồi tối thiểu 70% số tiền nợ cước trước ngày 05/10; bắt buộc 100% bưu cục trang bị cân chuẩn."
        ]
    )

    # 15. KINH DOANH & KHÁCH HÀNG F30
    add_speech_section(
        doc,
        sec_title="💼 [XV. PHÁT TRIỂN KHÁCH HÀNG MỚI F30 & BẢO VỆ DOANH THU 1.168 TỶ ĐỒNG (W39)]",
        speech_heading="🗣️ BỨC TRANH DOANH THU 1.168 TỶ ĐỒNG VÀ PHÁT TRIỂN 111 KHÁCH HÀNG MỚI F30:",
        paragraphs_text=[
            "Kính thưa Ban Giám Đốc, về kết quả kinh doanh và phát triển khách hàng mới tuần W39:",
            "• Tổng doanh thu thuần toàn vùng đạt 1.168.224.137 VNĐ (1,168 tỷ đồng), ghi nhận mức tăng trưởng dương +1,6% WoW (tăng thêm +18,4 triệu đồng so với W38 là 1,149 tỷ đồng) dù thị trường chung có sự chững lại về sản lượng!",
            "• Phát triển khách hàng mới F30: Toàn vùng phát triển thành công 111 khách hàng mới F30, mang lại 17,73 triệu đồng doanh thu ban đầu (+2,3% WoW).",
            "• Khen ngợi các cá nhân xuất sắc: AM Nguyễn Duy Long và AM Phan Đình Duy tiếp tục là 2 đầu tàu kinh doanh hiệu quả nhất vùng, vừa bảo vệ doanh số nhóm khách hàng VIP vừa mở rộng mạng lưới shop F30 vững chắc.",
            "• Chiến lược W40: Tập trung chăm sóc đặc biệt nhóm khách hàng Nhóm A và tung gói ưu đãi mùa vụ để đón đầu mùa nông sản và đợt khuyến mãi lớn tháng 10."
        ],
        insights=[
            "Doanh thu tăng +1,6% WoW chứng minh cơ cấu giá cước và năng lực bán hàng của NTB đang đi đúng hướng.",
            "Khách hàng mới F30 là nguồn sống tương lai bù đắp cho các shop tự nhiên bị sụt giảm sản lượng."
        ],
        warnings=[
            "Số lượng khách hàng F30 tuần này (111 shop) giảm 28 shop so với tuần trước (139 shop), cần đẩy mạnh hoạt động thị trường."
        ],
        actions=[
            "Giao chỉ tiêu mỗi AM phát triển tối thiểu 10 shop F30 mới/tuần; tổ chức thăm hỏi trực tiếp top 20 khách hàng doanh số lớn nhất vùng."
        ]
    )

    # 16. BƯU CỤC CẢNH BÁO BẤT ỔN (SO SÁNH W38 VS W39)
    add_speech_section(
        doc,
        sec_title="🏬 [XVI. THEO DÕI & XỬ LÝ NHÓM BƯU CỤC CẢNH BÁO BẤT ỔN (W38 VS W39)]",
        speech_heading="🗣️ SO SÁNH ĐỐI CHIẾU BIẾN ĐỘNG BƯU CỤC CẢNH BÁO BẤT ỔN (TUẦN W38 VS TUẦN W39):",
        paragraphs_text=[
            "Kính thưa Ban Giám Đốc, để kết thúc buổi họp giao ban điều hành tuần W39, em xin phép báo cáo chuyên đề trọng điểm: Biến động Bưu cục cảnh báo bất ổn (%GTC < 45% hoặc giảm sâu dưới 70% mốc đỉnh lịch sử) đặt trên hệ quy chiếu so sánh Tuần W38 vs Tuần W39:",
            "• 1. TỔNG QUAN BIẾN ĐỘNG (TĂNG TỪ 13 LÊN 15 BƯU CỤC): Tuần W38 có 13 bưu cục cảnh báo. Sang tuần W39, danh sách tăng lên 15 bưu cục (tăng ròng +2 BCs). Trong đó: có 4 bưu cục nỗ lực thoát cảnh báo thành công, 6 bưu cục mới rơi vào diện báo động, và 9 bưu cục đang kẹt dai dẳng cả 2 tuần liên tiếp.",
            "• 2. TUYÊN DƯƠNG 4 BƯU CỤC ĐÃ GIẢI TỎA & THOÁT CẢNH BÁO THÀNH CÔNG: Xuân Hương - Đà Lạt (AM Lê Văn Trường), Cam Linh (AM Phan Đình Duy), Nhân Cơ (AM Đỗ Duy Khang), và Tây Nha Trang (AM Hồng Bích Nga). Các bưu cục này đã tối ưu vượt bậc ca phát sáng để kéo %GTC vượt ngưỡng an toàn >50%.",
            "• 3. BÁO ĐỘNG ĐỎ 6 BƯU CỤC MỚI LỌT VÀO DIỆN CẢNH BÁO W39: BC D'Ran (Lâm Đồng - 36,86%, cảnh báo 6 ngày), BC Lang Biang 2 (Lâm Đồng - 35,80%, cảnh báo 6 ngày), BC Trường Xuân (Đắk Nông - 38,22%, cảnh báo 8 ngày), BC Đông Gia Nghĩa (Đắk Nông - 44,89%), BC Bắc Cam Ranh (Khánh Hòa - 44,68%, tích lũy 31 ngày cảnh báo), và BC Phú Quý (Bình Thuận - 50,84%, rơi sâu dưới 70% mốc đỉnh lịch sử 88,55%).",
            "• 4. ĐIỂM NÓNG MÃN TÍNH 9 BƯU CỤC KẸT DAI DẲNG CẢ 2 TUẦN: Nghiêm trọng nhất là BC Lâm Viên - Đà Lạt 2 từ 46,2% ở W38 rơi tự do xuống 19,55% trong W39 (nặng nhất toàn mạng, liệt ca chiều); BC Đức Trọng 1 (23,78%) và BC Đơn Dương (29,01%, giảm -16,3%p); BC Quảng Tín (26,17%, tích lũy >100 ngày cảnh báo). Cùng 5 BC: Lang Biang 1 (30,6%), Kiến Đức (32,5%), Tân Hà Lâm Hà (36,8%), Tuy Đức (38,5%) và Di Linh (40,6%).",
            "• 5. KẾ HOẠCH HÀNH ĐỘNG CẤP BÁCH TUẦN W40 (3 MỆNH LỆNH TÁC CHIẾN):",
            "   1. Áp dụng cơ chế Điều tiết hàng (Cap Volume): Tạm thời giảm 25% hạn mức chia chọn hàng về trong 3 ngày đầu tuần tại BC Lâm Viên 2 và Quảng Tín để bưu tá tập trung quét sạch tồn kho và aging >5 ngày.",
            "   2. Tái cơ cấu bưu tá ca sáng: Điều chuyển chi viện 4 bưu tá cứng từ cụm Xuân Hương và Gia Nghĩa sang phát lượt 1 trước 11h00 trưa tại Lâm Viên 2 và Đức Trọng 1.",
            "   3. Mục tiêu cam kết W40: Quyết tâm kéo tối thiểu 5 bưu cục thoát khỏi danh sách cảnh báo, giảm tổng số lượng toàn vùng từ 15 BC về dưới 10 BC trong tuần tiếp theo.",
            "Em xin kết thúc toàn bộ phần báo cáo điều hành tuần W39. Xin trân trọng cảm ơn Ban Giám Đốc và kính mời các anh chị cho ý kiến chỉ đạo ạ!\""
        ],
        insights=[
            "Tồn đọng và rớt %GTC ở nhóm 9 bưu cục mãn tính chủ yếu do thắt nút cổ chai ở tỷ lệ gán Ca 2 trưa và địa hình đồi núi dốc xa.",
            "Cap Volume là công cụ hữu hiệu nhất giúp bưu cục quá tải có thời gian hồi phục thể lực và quét sạch đơn cũ."
        ],
        warnings=[
            "Nếu không dập tắt điểm nóng tại cụm Đà Lạt - Đơn Dương - Đức Trọng, nguy cơ vỡ tải cục bộ khi sản lượng đầu tháng tăng là rất cao."
        ],
        actions=[
            "Đội cơ động vùng trực tiếp cắm chốt tại Lâm Viên 2 và Đức Trọng 1 từ ngày 29/09 đến khi dọn sạch 100% hàng tồn kho."
        ]
    )

    # Save to all destination files
    out_master = 'KICH_BAN_THUYET_TRINH_MOI_NHAT.docx'
    doc.save(out_master)
    print(f"Generated {out_master} successfully! (Size: {os.path.getsize(out_master)} bytes)")
    
    copies = [
        'KICH_BAN_THUYET_TRINH_W39_INSIGHT_CHUYEN_SAU.docx',
        'KICH_BAN_THUYET_TRINH_W39_INSIGHT_CHUYEN_SAU_CHINH_SUA.docx',
        'KICH_BAN_THUYET_TRINH_W39_NAM_TRUNG_BO.docx'
    ]
    for c in copies:
        shutil.copyfile(out_master, c)
        print(f"Copied to {c}")

if __name__ == '__main__':
    build_full_w39_docx()
