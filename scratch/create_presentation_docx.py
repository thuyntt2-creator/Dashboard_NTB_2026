import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=180, right=180):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def create_callout_box(doc, title, text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.8)
    
    set_cell_background(cell, "FFF7ED") # Soft warm orange/cream
    set_cell_margins(cell, top=160, bottom=160, left=240, right=200)
    
    # Left border orange, others none
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="none"/>
            <w:left w:val="single" w:sz="36" w:space="0" w:color="F26522"/>
            <w:bottom w:val="none"/>
            <w:right w:val="none"/>
        </w:tcBorders>
    ''')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    run_t = p.add_run(title)
    run_t.bold = True
    run_t.font.name = 'Arial'
    run_t.font.size = Pt(10.5)
    run_t.font.color.rgb = RGBColor(217, 78, 14) # Orange dark
    
    p2 = cell.add_paragraph()
    p2.paragraph_format.space_before = Pt(2)
    p2.paragraph_format.space_after = Pt(2)
    p2.paragraph_format.line_spacing = 1.2
    run_b = p2.add_run(text)
    run_b.italic = True
    run_b.font.name = 'Arial'
    run_b.font.size = Pt(10)
    run_b.font.color.rgb = RGBColor(30, 41, 59) # Slate navy
    
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

def style_table(tbl, col_widths, headers, rows_data, header_bg="1E293B", header_fg="FFFFFF"):
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    
    # Header
    hdr_cells = tbl.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].width = Inches(col_widths[i])
        set_cell_background(hdr_cells[i], header_bg)
        set_cell_margins(hdr_cells[i], top=120, bottom=120, left=140, right=140)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if i == 0 or 'STT' in h or '%' in h else (WD_ALIGN_PARAGRAPH.RIGHT if 'đơn' in h or 'Tr' in h or 'VNĐ' in h else WD_ALIGN_PARAGRAPH.LEFT)
        r = p.add_run(h)
        r.bold = True
        r.font.name = 'Arial'
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)
        
    # Rows
    for r_idx, r_data in enumerate(rows_data):
        row = tbl.add_row()
        cells = row.cells
        bg_color = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(r_data):
            cells[c_idx].width = Inches(col_widths[c_idx])
            set_cell_background(cells[c_idx], bg_color)
            set_cell_margins(cells[c_idx], top=100, bottom=100, left=140, right=140)
            p = cells[c_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx == 0 or '%' in headers[c_idx] or 'STT' in headers[c_idx] else (WD_ALIGN_PARAGRAPH.RIGHT if any(w in headers[c_idx] for w in ['đơn', 'Tr', 'VNĐ', 'Cần Thu', 'Doanh Thu', 'Volume']) else WD_ALIGN_PARAGRAPH.LEFT)
            r = p.add_run(str(val))
            r.font.name = 'Arial'
            r.font.size = Pt(9)
            if c_idx == 1 or 'TỔNG' in str(val) or 'Top' in str(val):
                r.bold = True
            if '▲' in str(val):
                r.font.color.rgb = RGBColor(5, 150, 105)
                r.bold = True
            elif '▼' in str(val) or '🚨' in str(val):
                r.font.color.rgb = RGBColor(220, 38, 38)
                r.bold = True

doc = docx.Document()

# Page setup (A4, 0.7 inch margins)
sections = doc.sections
for s in sections:
    s.page_width = Inches(8.27)
    s.page_height = Inches(11.69)
    s.top_margin = Inches(0.7)
    s.bottom_margin = Inches(0.7)
    s.left_margin = Inches(0.75)
    s.right_margin = Inches(0.75)

# HEADER TITLE
p_brand = doc.add_paragraph()
p_brand.paragraph_format.space_before = Pt(0)
p_brand.paragraph_format.space_after = Pt(2)
run_brand = p_brand.add_run("GIAOHANGNHANH (GHN EXPRESS) — KHỐI VẬN HÀNH & KINH DOANH VÙNG NAM TRUNG BỘ")
run_brand.bold = True
run_brand.font.name = 'Arial'
run_brand.font.size = Pt(9.5)
run_brand.font.color.rgb = RGBColor(242, 101, 34) # GHN Orange

p_title = doc.add_paragraph()
p_title.paragraph_format.space_before = Pt(4)
p_title.paragraph_format.space_after = Pt(2)
run_title = p_title.add_run("KỊCH BẢN THUYẾT TRÌNH BÁO CÁO HỌP TUẦN W38")
run_title.bold = True
run_title.font.name = 'Arial'
run_title.font.size = Pt(18)
run_title.font.color.rgb = RGBColor(15, 23, 42) # Deep Navy

p_sub = doc.add_paragraph()
p_sub.paragraph_format.space_before = Pt(0)
p_sub.paragraph_format.space_after = Pt(14)
run_sub = p_sub.add_run("Kỳ đánh giá: Tuần W38 từ 14/09/2026 đến hết 20/09/2026 · So sánh cùng kỳ Tuần W37")
run_sub.italic = True
run_sub.font.name = 'Arial'
run_sub.font.size = Pt(10)
run_sub.font.color.rgb = RGBColor(100, 116, 139)

# 0. TỔNG QUAN CHIẾN LƯỢC
h0 = doc.add_paragraph()
h0.paragraph_format.space_before = Pt(10)
h0.paragraph_format.space_after = Pt(6)
r_h0 = h0.add_run("🧭 TỔNG QUAN CHIẾN LƯỢC VÙNG W38")
r_h0.bold = True
r_h0.font.name = 'Arial'
r_h0.font.size = Pt(13)
r_h0.font.color.rgb = RGBColor(15, 23, 42)

create_callout_box(
    doc,
    "🗣️ LỜI THOẠI MỞ ĐẦU DÀNH CHO NGƯỜI BÁO CÁO (TRÌNH BÀY TRƯỚC BAN GIÁM ĐỐC):",
    '"Kính chào Ban Giám Đốc, các Giám đốc Khối và toàn thể các anh chị Quản lý Vận hành (AM), Quản lý Kinh doanh vùng Nam Trung Bộ. Hôm nay, em xin đại diện Ban Điều Hành Vùng trình bày Báo cáo tổng kết tuần W38 (kỳ từ ngày 14/09 đến hết ngày 20/09/2026).\n\n'
    'Thưa Ban Giám Đốc, nhìn lại tuần W38, có thể gói gọn trong nhận định: \'Quy mô giữ nhịp vững chắc, kinh doanh tăng trưởng dương, chất lượng ODR đạt chuẩn xanh cam kết; tuy nhiên cần siết chặt ngay kỷ luật cân đo đầu vào trước đợt bùng phát truy thu và giải tỏa dứt điểm 13 bưu cục cảnh báo\'.\n\n'
    '• Sản lượng Full hàng đạt 345.994 đơn, trong đó phân khúc trọng điểm TikTok Shop tăng trưởng đạt 69.274 đơn (+0.8%), chiếm 20% tổng tải toàn vùng.\n'
    '• Kinh doanh bứt phá: Doanh thu vùng tăng trưởng dương đạt 1.168,2 triệu VNĐ (+1.6%). Toàn vùng kích hoạt 111 shop mới F30 (17.7 Tr ₫ doanh thu mới). 10 shop nhóm A đạt 43.254 triệu VNĐ MTD.\n'
    '• Chất lượng vận hành giữ chuẩn: ODR Full hàng đạt 91.2%, ODR TTS đạt 91.5%. %LTC lấy hàng TTS đạt đỉnh 95.4%.\n'
    '• Hai điểm nóng cần xử lý gấp: Tiền cần truy thu tăng vọt lên 282.4 triệu VNĐ (3.074 đơn) do lệch cước kích thước/khối lượng, và hiệu suất thùng xe KTC giảm còn 51.0% (76 chuyến non tải <30%)."'
)

# BẢNG TỔNG HỢP KPI W38
doc.add_paragraph().paragraph_format.space_after = Pt(2)
p_tbl_lbl = doc.add_paragraph()
p_tbl_lbl.paragraph_format.space_before = Pt(4)
p_tbl_lbl.paragraph_format.space_after = Pt(4)
r_lbl = p_tbl_lbl.add_run("BẢNG 1: TỔNG HỢP CÁC CHỈ TIÊU KPI CHÍNH VÙNG NAM TRUNG BỘ (W38 vs W37)")
r_lbl.bold = True
r_lbl.font.size = Pt(10)
r_lbl.font.color.rgb = RGBColor(30, 58, 138)

t_kpi = doc.add_table(rows=1, cols=5)
style_table(
    t_kpi,
    [1.8, 1.3, 1.3, 1.2, 1.2],
    ["Chỉ Tiêu KPI", "Kỳ Này (W38)", "Kỳ Trước (W37)", "Biến Động (Δ)", "Đánh Giá"],
    [
        ["Doanh Thu Kinh Doanh", "1,168.2 Tr ₫", "1,149.8 Tr ₫", "▲ +18.4 Tr (+1.6%)", "Tăng trưởng tốt"],
        ["Sản Lượng Full Hàng", "345,994 đơn", "357,249 đơn", "▼ -11,255 đ (-3.2%)", "Hạ nhiệt sau 9.9"],
        ["Sản Lượng TikTok Shop", "69,274 đơn", "68,719 đơn", "▲ +555 đ (+0.8%)", "Chiếm 20% vùng"],
        ["%ODR Full Hàng", "91.2%", "93.9%", "▼ -2.7%p", "Đạt chuẩn SLA xanh"],
        ["%ODR TikTok Shop", "91.5%", "92.8%", "▼ -1.3%p", "Đạt chuẩn SLA sàn"],
        ["%GTC Tổng Toàn Vùng", "55.75%", "57.78%", "▼ -2.03%p", "Cần cải thiện ca 2"],
        ["%GTC TTS Ca 1", "68.4%", "69.1%", "▼ -0.7%p", "Phát sáng rất tốt"],
        ["% Gán Vận Hành", "96.5%", "96.8%", "▼ -0.3%p", "Chuẩn SLA phân bổ"],
        ["%LTC Lấy Thành Công", "90.4%", "90.3%", "▲ +0.1%p", "Ổn định"],
        ["%LTC TikTok Shop", "95.4%", "93.6%", "▲ +1.8%p", "Đỉnh cao 2 tháng"],
        ["%OPR TikTok Shop", "78.10%", "78.05%", "▲ +0.05%p", "Ca ngày 87.8%"],
        ["% TLLĐ Thùng Xe KTC", "51.0%", "54.8%", "▼ -3.8%p", "76 chuyến <30%"],
        ["Tiền Cần Truy Thu", "282.4 Tr ₫", "41.4 Tr ₫", "▲ +241.0 Tr (3,074 đ)", "🚨 Báo động đỏ"],
        ["Khách Hàng Mới F30", "111 Shop", "139 Shop", "▼ -28 shop", "17.7 Tr doanh thu"]
    ]
)
doc.add_paragraph().paragraph_format.space_after = Pt(12)

# 1. SẢN LƯỢNG 5 TỈNH
h1 = doc.add_paragraph()
h1.paragraph_format.space_before = Pt(10)
h1.paragraph_format.space_after = Pt(4)
r_h1 = h1.add_run("📦 I. SẢN LƯỢNG GIAO 5 TỈNH THÀNH (FULL HÀNG vs TIKTOK SHOP)")
r_h1.bold = True
r_h1.font.size = Pt(12)
r_h1.font.color.rgb = RGBColor(15, 23, 42)

create_callout_box(
    doc,
    "🗣️ LỜI THOẠI TRÌNH BÀY — PHÂN TÍCH SẢN LƯỢNG ĐỊA BÀN:",
    '"Kính thưa Ban Giám Đốc, nhìn vào cơ cấu sản lượng 5 tỉnh thành tuần W38:\n'
    '• Lâm Đồng tiếp tục giữ vững vị trí anh cả về quy mô vùng với 96.420 đơn Full hàng (TTS đạt 18.810 đơn).\n'
    '• Khánh Hòa đứng thứ hai với 90.150 đơn (TTS đạt 17.950 đơn), giữ vững sản lượng ổn định sau chiến dịch 9.9.\n'
    '• Bình Thuận đạt 88.310 đơn (TTS đạt 16.420 đơn), địa bàn duy trì phong độ giao hàng ổn định nhất vùng.\n'
    '• Đắk Nông đạt 36.980 đơn và Ninh Thuận đạt 34.134 đơn.\n\n'
    'Insight: Sau tuần cao điểm 9.9, sản lượng Full hàng hạ nhiệt nhẹ (-3.2%) là quy luật thị trường hoàn toàn bình thường. Tuy nhiên, phân khúc TikTok Shop vẫn giữ được đà tăng trưởng (+0.8% lên 69.274 đơn). Các AM Duy Long, Thanh Thư, Đình Duy đã tận dụng rất tốt các khung giờ Flash Sale giữa tháng để duy trì tải."'
)

t_vol = doc.add_table(rows=1, cols=5)
style_table(
    t_vol,
    [1.8, 1.4, 1.4, 1.1, 1.1],
    ["Tỉnh / Thành Phố", "Full Hàng W38", "TikTok Shop W38", "Tỷ Trọng TTS", "Đặc Điểm Địa Bàn"],
    [
        ["Lâm Đồng", "96,420 đơn", "18,810 đơn", "19.5%", "Địa bàn lớn nhất vùng"],
        ["Khánh Hòa", "90,150 đơn", "17,950 đơn", "19.9%", "Khu vực ven biển, du lịch"],
        ["Bình Thuận", "88,310 đơn", "16,420 đơn", "18.6%", "Chất lượng ổn định nhất"],
        ["Đắk Nông", "36,980 đơn", "8,144 đơn", "22.0%", "Địa hình dốc, nông trường"],
        ["Ninh Thuận", "34,134 đơn", "7,950 đơn", "23.3%", "Top 1 ODR & OPR toàn vùng"],
        ["TỔNG TOÀN VÙNG", "345,994 đơn", "69,274 đơn", "20.0%", "TTS chiếm 1/5 sản lượng"]
    ]
)
doc.add_paragraph().paragraph_format.space_after = Pt(12)

# 2. %GTC & GÁN
h2 = doc.add_paragraph()
h2.paragraph_format.space_before = Pt(10)
h2.paragraph_format.space_after = Pt(4)
r_h2 = h2.add_run("🎯 II. HIỆU SUẤT GIAO THÀNH CÔNG (%GTC) & TỶ LỆ GÁN VẬN HÀNH")
r_h2.bold = True
r_h2.font.size = Pt(12)
r_h2.font.color.rgb = RGBColor(15, 23, 42)

create_callout_box(
    doc,
    "🗣️ LỜI THOẠI TRÌNH BÀY — NGHỊCH LÝ GÁN CAO NHƯNG GTC NGHẼN CA CHIỀU:",
    '"Thưa Ban Giám Đốc, về tỷ lệ Giao Thành Công: %GTC Tổng toàn vùng đạt 55.75% Full hàng và 54.01% TTS. Điểm sáng nổi bật là %GTC TTS Ca 1 đạt rất cao 68.4% và tỷ lệ Gán vận hành đạt 96.5%.\n\n'
    'Tuy nhiên, nghịch lý nằm ở chỗ: Hàng về kho được gán ra tuyến ngay lập tức (96.5%), nhưng tỷ lệ hoàn tất giao trong ngày lại bị nghẽn tại ca chiều/tối ở các địa bàn nông trường, vùng sâu (Lâm Hà, Đơn Dương, Cư Jút). Bưu tá không kịp đi tuyến ca 2, dẫn tới hàng bị trôi sang hôm sau. Ban Điều Hành yêu cầu các bưu cục tổ chức lại ca chia chọn từ 06h30 sáng để bưu tá xuất phát tuyến sớm hơn 30 phút, giải tỏa triệt để áp lực ca chiều."'
)

# 3. %ODR ĐÚNG HẸN
h3 = doc.add_paragraph()
h3.paragraph_format.space_before = Pt(10)
h3.paragraph_format.space_after = Pt(4)
r_h3 = h3.add_run("⏱️ III. CHẤT LƯỢNG GIAO ĐÚNG HẸN %ODR (FULL HÀNG 91.2% & TIKTOK SHOP 91.5%)")
r_h3.bold = True
r_h3.font.size = Pt(12)
r_h3.font.color.rgb = RGBColor(15, 23, 42)

create_callout_box(
    doc,
    "🗣️ LỜI THOẠI TRÌNH BÀY — CHỈ SỐ ĐÚNG HẸN %ODR & CẢNH BÁO BÁO ĐỘNG ĐỎ:",
    '"Kính thưa Ban Giám Đốc, chỉ số Đúng Hẹn (%ODR) tuần W38 tiếp tục giữ vững màu xanh tiêu chuẩn: Full hàng đạt 91.2% và TikTok Shop đạt 91.5%. Toàn vùng đã hoàn thành tốt cam kết chất lượng với sàn và đối tác lớn.\n\n'
    '• Top AM dẫn đầu: AM Thái Thị Thanh Thư (95.8%), AM Nguyễn Ngọc Khánh (95.2%), AM Nguyễn Duy Long (94.8%), AM Cao Thị Thanh Thủy (94.5%).\n'
    '• Nhóm báo động đỏ cần chấn chỉnh ngay: AM Trầm Hữu Tiến (74.2%) và AM Lê Minh Lợi (76.1%). Tình trạng bưu tá để đơn tồn không giao lại trong 24h tại cụm Đức Trọng 1 và Di Linh đang trực tiếp làm xói mòn chất lượng vùng. Yêu cầu 2 AM phải có báo cáo giải trình và phương án xử lý trước thứ Tư."'
)

# 4. TRUY THU
h4 = doc.add_paragraph()
h4.paragraph_format.space_before = Pt(10)
h4.paragraph_format.space_after = Pt(4)
r_h4 = h4.add_run("💰 IV. BÁO CÁO TRUY THU 2 TUẦN: BÙNG PHÁT 282.4 TRIỆU VNĐ (GẤP 7 LẦN W37)")
r_h4.bold = True
r_h4.font.size = Pt(12)
r_h4.font.color.rgb = RGBColor(220, 38, 38) # Red alert

create_callout_box(
    doc,
    "🗣️ LỜI THOẠI TRÌNH BÀY — TRỌNG TÂM CẢNH BÁO TÀI CHÍNH TRUY THU:",
    '"Kính thưa Ban Giám Đốc, đây là nội dung khẩn cấp nhất tuần này: Số tiền truy thu tuần W38 bùng phát lên 282.4 triệu VNĐ trên 3.074 đơn, tăng gấp gần 7 lần so với tuần W37 (41.4 triệu VNĐ).\n\n'
    '• Nguyên nhân cốt tử: Có tới 78.5% số tiền (hơn 221 triệu VNĐ) xuất phát từ việc lệch cước kích thước và khối lượng (khách khai báo nhẹ nhưng hàng thực tế cồng kềnh, nặng ký). Điều này phản ánh sự buông lỏng khâu cân đo tại quầy bưu cục.\n'
    '• Địa bàn tập trung: Lâm Đồng chiếm tới 55% toàn vùng (hơn 155 triệu VNĐ, điểm nóng tại Đức Trọng 1, Bảo Lộc 3, Đơn Dương), tiếp đến là Khánh Hòa (hơn 68 triệu VNĐ).\n\n'
    'Kế hoạch thu hồi dứt điểm: Ban Điều Hành giao chỉ tiêu cho 18 AM phải thu hồi tối thiểu 75% số tiền truy thu W38 (tương đương 210 triệu VNĐ) trước ngày 27/09. Đồng thời, 100% bưu cục phải kiểm định lại cân điện tử và đo đạc nghiêm ngặt ngay tại thời điểm nhận hàng."'
)

t_tt = doc.add_table(rows=1, cols=5)
style_table(
    t_tt,
    [2.2, 1.2, 1.2, 1.1, 1.1],
    ["Phân Loại Truy Thu", "Tiền Thu W38", "Tiền Thu W37", "Số Đơn W38", "Tỷ Trọng"],
    [
        ["Lệch cước kích thước / khối lượng", "221.7 Tr ₫", "31.2 Tr ₫", "2,310 đơn", "78.5%"],
        ["Sai mã phân loại & cước phụ phí", "40.1 Tr ₫", "6.8 Tr ₫", "492 đơn", "14.2%"],
        ["Truy thu hoàn hàng sai quy trình", "20.6 Tr ₫", "3.4 Tr ₫", "272 đơn", "7.3%"],
        ["TỔNG CỘNG TRUY THU", "282.4 Tr ₫", "41.4 Tr ₫", "3,074 đơn", "100.0%"]
    ],
    header_bg="991B1B"
)
doc.add_paragraph().paragraph_format.space_after = Pt(12)

# 5. KINH DOANH & F30
h5 = doc.add_paragraph()
h5.paragraph_format.space_before = Pt(10)
h5.paragraph_format.space_after = Pt(4)
r_h5 = h5.add_run("📈 V. KINH DOANH & KHÁCH HÀNG MỚI F30: DOANH THU 1.168 TỶ ₫")
r_h5.bold = True
r_h5.font.size = Pt(12)
r_h5.font.color.rgb = RGBColor(15, 23, 42)

create_callout_box(
    doc,
    "🗣️ LỜI THOẠI TRÌNH BÀY — KẾT QUẢ KINH DOANH, SHOP F30 & 10 SHOP NHÓM A:",
    '"Về kết quả kinh doanh tuần W38: Tổng doanh thu toàn vùng đạt 1.168,2 triệu VNĐ (+1.6% WoW). Dẫn đầu vùng tiếp tục là anh Phan Đình Duy đạt 506.6 triệu VNĐ (chiếm 43.4% thị phần), chị Thái Thị Thanh Thư (98.3 Tr), anh Nguyễn Duy Long (97.3 Tr), anh Lê Thanh Nhựt (58.7 Tr).\n\n'
    '• Về khách hàng mới F30: Toàn vùng phát triển thành công 111 shop mới, mang lại 17.7 triệu VNĐ doanh thu mới. Anh Nguyễn Duy Long dẫn đầu xuất sắc với 21 shop F30 (mang về 5.72 triệu VNĐ), anh Phan Đình Duy đạt 20 shop, chị Thanh Thư đạt 10 shop.\n\n'
    '• Về 10 khách hàng nhóm A: Lũy kế MTD đạt 43.254 triệu VNĐ (tiến độ tháng đạt 20/30 ngày - 66.7%). Top 1 shop là Vận Chuyển Online đạt 21.296 Tr MTD. Tuy nhiên, có 2 shop cần AM can thiệp gấp: Huyền Anh Shop (AM Huỳnh Thúc Duân) % trụ hạng chỉ còn 5.1%, và Bếp vườn nhà Trinh (AM Phan Đình Duy) trụ hạng 48.5%. Yêu cầu 2 AM phải trực tiếp gặp gỡ đối tác để bảo vệ sản lượng."'
)

t_kd = doc.add_table(rows=1, cols=5)
style_table(
    t_kd,
    [1.8, 1.2, 1.4, 1.2, 1.2],
    ["AM Phụ Trách", "Sản Lượng W38", "Doanh Thu W38", "Tỷ Trọng", "Shop Mới F30"],
    [
        ["Phan Đình Duy", "10,669 đơn", "506.6 Tr ₫", "43.4%", "20 shop (1.49 Tr)"],
        ["Thái Thị Thanh Thư", "4,837 đơn", "98.3 Tr ₫", "8.4%", "10 shop (2.21 Tr)"],
        ["Nguyễn Duy Long", "3,770 đơn", "97.3 Tr ₫", "8.3%", "21 shop (5.72 Tr) 🥇"],
        ["Lê Thanh Nhựt", "2,168 đơn", "58.7 Tr ₫", "5.0%", "9 shop (2.76 Tr)"],
        ["Hồng Bích Nga", "1,507 đơn", "49.3 Tr ₫", "4.2%", "7 shop (0.54 Tr)"],
        ["Huỳnh Thúc Duân", "5,076 đơn", "46.7 Tr ₫", "4.0%", "1 shop (0.08 Tr)"],
        ["Huỳnh Thị Kim Chi", "892 đơn", "44.9 Tr ₫", "3.8%", "8 shop (0.67 Tr)"],
        ["Trần Thị Nhung", "985 đơn", "30.4 Tr ₫", "2.6%", "6 shop (0.85 Tr)"],
        ["Nguyễn Hoàng Phi", "843 đơn", "28.5 Tr ₫", "2.4%", "4 shop (0.16 Tr)"]
    ]
)
doc.add_paragraph().paragraph_format.space_after = Pt(12)

# 6. NGHỊ QUYẾT HÀNH ĐỘNG W39
h6 = doc.add_paragraph()
h6.paragraph_format.space_before = Pt(10)
h6.paragraph_format.space_after = Pt(4)
r_h6 = h6.add_run("📋 VI. NGHỊ QUYẾT HÀNH ĐỘNG TUẦN W39 (5 TRỌNG TÂM CỐT LÕI)")
r_h6.bold = True
r_h6.font.size = Pt(12)
r_h6.font.color.rgb = RGBColor(15, 23, 42)

t_res = doc.add_table(rows=1, cols=5)
style_table(
    t_res,
    [0.6, 2.2, 1.8, 1.4, 0.8],
    ["STT", "Mục Tiêu Trọng Tâm", "Chỉ Tiêu Cam Kết SLA", "Đầu Mối Chịu Trách Nhiệm", "Hạn Chót"],
    [
        ["1", "Thu hồi nợ Truy Thu W38", "Thu hồi tối thiểu ≥75% (210 Tr ₫); trang bị 100% cân chuẩn", "Toàn bộ 18 AM & Trưởng Bưu Cục", "27/09"],
        ["2", "Dập tắt tồn kho 13 BC nóng", "Giải tỏa 100% đơn Aging >5 ngày; đưa %GTC lên ≥52%", "Đội cơ động vùng & AM phụ trách", "24/09"],
        ["3", "Cải tổ OPR Ca Đêm TTS", "Nâng OPR ca đêm từ 67.9% lên ≥78%; OPR tổng ≥82%", "AM Duy Long, Đình Duy, Thanh Thư", "25/09"],
        ["4", "Tối ưu chi phí xe KTC", "Nâng %TLTĐ từ 51.0% lên ≥56%; giảm chuyến non tải <50 xe", "Khối Vận Tải & Hub Cam Ranh", "26/09"],
        ["5", "Bảo vệ KH Nhóm A & F30", "Cứu vãn Huyền Anh Shop, Bếp nhà Trinh; tăng ≥15 shop F30", "Khối Kinh Doanh & AM Account", "27/09"]
    ],
    header_bg="0F172A"
)

doc.add_paragraph().paragraph_format.space_after = Pt(12)
p_end = doc.add_paragraph()
p_end.paragraph_format.space_before = Pt(6)
r_end = p_end.add_run('🗣️ LỜI KẾT THUYẾT TRÌNH:\n"Thưa Ban Giám Đốc và toàn thể các anh chị, mục tiêu của vùng Nam Trung Bộ trong tuần W39 là vừa duy trì đà tăng trưởng doanh thu, vừa lập lại trật tự kỷ luật kho bãi và thu hồi dứt điểm các khoản lệch cước truy thu. Khối Vận hành và Kinh doanh xin cam kết hoàn thành vượt mức các mục tiêu trên. Em xin trân trọng cảm ơn Ban Giám Đốc và kính mời các anh chị đóng góp ý kiến chỉ đạo!"')
r_end.italic = True
r_end.bold = True
r_end.font.size = Pt(10)
r_end.font.color.rgb = RGBColor(15, 23, 42)

doc.save('KICH_BAN_THUYET_TRINH_W38_NAM_TRUNG_BO.docx')
print("Successfully generated KICH_BAN_THUYET_TRINH_W38_NAM_TRUNG_BO.docx!")
