# -*- coding: utf-8 -*-
"""
Tạo kịch bản thuyết trình W36 dạng .docx
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from docx import Document
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import copy

doc = Document()

# ===================== STYLES =====================
style_normal = doc.styles['Normal']
style_normal.font.name = 'Times New Roman'
style_normal.font.size = Pt(12)

# Page margins
section = doc.sections[0]
section.top_margin = Cm(2)
section.bottom_margin = Cm(2)
section.left_margin = Cm(2.5)
section.right_margin = Cm(2.5)

def add_heading(doc, text, level=1, color=None):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = True
    if level == 1:
        run.font.size = Pt(16)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    elif level == 2:
        run.font.size = Pt(13)
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    else:
        run.font.size = Pt(12)
    if color:
        run.font.color.rgb = RGBColor(*color)
    run.font.name = 'Times New Roman'
    return p

def add_body(doc, text, bold_parts=None, indent=False):
    p = doc.add_paragraph()
    if indent:
        p.paragraph_format.left_indent = Cm(1)
    # Handle basic text
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(11.5)
    return p

def add_bullet(doc, text, indent_level=1):
    p = doc.add_paragraph(style='List Bullet')
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(11.5)
    return p

def add_divider(doc):
    p = doc.add_paragraph('─' * 80)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.runs[0].font.color.rgb = RGBColor(150, 150, 150)
    p.runs[0].font.size = Pt(9)
    return p

def add_section_title(doc, emoji, title, color=(30, 80, 160)):
    add_divider(doc)
    p = doc.add_paragraph()
    run = p.add_run(f'{emoji}  {title}')
    run.bold = True
    run.font.size = Pt(13)
    run.font.color.rgb = RGBColor(*color)
    run.font.name = 'Times New Roman'
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    return p

def add_speech(doc, text):
    """Thêm lời thuyết trình dạng box / italic"""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(1.2)
    p.paragraph_format.right_indent = Cm(0.5)
    run = p.add_run('🗣️  ')
    run.font.size = Pt(11.5)
    run2 = p.add_run(text)
    run2.font.name = 'Times New Roman'
    run2.font.size = Pt(11.5)
    run2.italic = True
    return p

def add_action(doc, text, who=''):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(1.2)
    r1 = p.add_run('📌 ACTION: ')
    r1.bold = True
    r1.font.color.rgb = RGBColor(180, 20, 20)
    r1.font.size = Pt(11.5)
    r1.font.name = 'Times New Roman'
    r2 = p.add_run(text)
    r2.font.size = Pt(11.5)
    r2.font.name = 'Times New Roman'
    if who:
        r3 = p.add_run(f' → [{who}]')
        r3.bold = True
        r3.font.size = Pt(11.5)
        r3.font.name = 'Times New Roman'
    return p

# ===================== TRANG BÌA =====================
doc.add_paragraph()
add_heading(doc, 'GHN EXPRESS — VÙNG NAM TRUNG BỘ', 1, color=(200, 50, 30))
add_heading(doc, 'BÁO CÁO VẬN HÀNH & KINH DOANH TUẦN W36', 1, color=(30, 60, 140))
add_heading(doc, '(31/08/2026 – 06/09/2026)', 1)
doc.add_paragraph()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('Kịch bản thuyết trình chi tiết từng AM & Phân tích tương quan thuần số liệu thực tế\n(Bổ sung mục %FD Hoàn Trả, KTC & Vận Tải – Lần đầu có trong báo cáo tuần)')
r.italic = True
r.font.size = Pt(11)
r.font.name = 'Times New Roman'
doc.add_page_break()

# ===================== I. TỔNG QUAN VẬN HÀNH =====================
add_section_title(doc, '📊', 'I. TỔNG QUAN VẬN HÀNH — CÁC CHỈ SỐ CHÍNH TUẦN W36')

add_speech(doc,
    '"Kính thưa Quý anh/chị, tuần W36 (31/08–06/09/2026) vùng Nam Trung Bộ ghi nhận một số diễn biến đáng chú ý:\n'
    '• Sản lượng full hàng đạt 307.837 đơn, giảm 11.149 đơn (-3,5%) so với W35; TTS đạt 63.122 đơn, giảm 9.759 đơn (-13,4%).\n'
    '• GTC tổng duy trì ổn định ở mức 58,1% (full) – 56,9% (TTS), nhưng Ca2 giảm đáng kể -2,9%p (full) và -3,2%p (TTS).\n'
    '• Điểm sáng: ODR cải thiện lên 92,9% (+0,7%p). Tỷ lệ Gán vận hành toàn vùng tăng lên 83,5% (+1,4%p).\n'
    '• Điểm cần theo dõi: %LTC giảm -0,6%p (full) và -1,9%p (TTS). %Rớt LC tăng lên 2,2% (+0,7%p). FD toàn vùng 7,5% (full) – 6,8% (TTS)."\n'
)

add_body(doc, '📍 BẢNG TỔNG HỢP CÁC CHỈ SỐ KPI TUẦN W36 VS W35:')
kpi_table = doc.add_table(rows=11, cols=4)
kpi_table.style = 'Table Grid'
headers = ['Chỉ Số', 'W35', 'W36', 'Δ']
for i, h in enumerate(headers):
    cell = kpi_table.rows[0].cells[i]
    cell.text = h
    cell.paragraphs[0].runs[0].bold = True
    cell.paragraphs[0].runs[0].font.size = Pt(10)
    cell.paragraphs[0].runs[0].font.name = 'Times New Roman'

rows_data = [
    ('Sản Lượng Full Hàng', '318.986 đ', '307.837 đ', '▼ -11.149 (-3,5%)'),
    ('Sản Lượng TTS', '72.881 đ', '63.122 đ', '▼ -9.759 (-13,4%)'),
    ('%GTC Full (Ca1+Ca2+Tồn)', '58,2%', '58,1%', '▼ -0,03%p'),
    ('%GTC Full (Ca1+Tồn)', '59,7%', '60,5%', '▲ +0,8%p'),
    ('%GTC Full (Ca2)', '51,2%', '48,4%', '▼ -2,9%p'),
    ('%ODR Full Hàng', '92,2%', '92,9%', '▲ +0,7%p'),
    ('%LTC Full Hàng', '91,1%', '90,5%', '▼ -0,6%p'),
    ('%Gán Vận Hành (Full)', '82,1%', '83,5%', '▲ +1,4%p'),
    ('%FD Hoàn Trả (Full)', '~7,6%*', '7,5%', '≈ ổn định'),
    ('%Rớt Luân Chuyển', '1,6%', '2,2%', '▲ +0,7%p ⚠️'),
]
for row_i, (c1, c2, c3, c4) in enumerate(rows_data):
    row = kpi_table.rows[row_i + 1]
    for ci, txt in enumerate([c1, c2, c3, c4]):
        cell = row.cells[ci]
        cell.text = txt
        cell.paragraphs[0].runs[0].font.size = Pt(10)
        cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
doc.add_paragraph()

# ===================== SẢN LƯỢNG THEO TỈNH =====================
add_section_title(doc, '📍', 'II.1 SẢN LƯỢNG THEO TỈNH')
add_speech(doc,
    '"Về phân bổ sản lượng theo tỉnh: Khánh Hòa vẫn chiếm tỷ trọng lớn nhất vùng. '
    'Tuần W36 ghi nhận sản lượng toàn vùng giảm, chủ yếu do TTS giảm đột biến -13,4% — '
    'cần rà soát các khu vực TTS sụt mạnh đặc biệt là Lâm Đồng và Đắk Nông."'
)

# ===================== SẢN LƯỢNG THEO AM =====================
add_section_title(doc, '👤', 'II.2 SẢN LƯỢNG THEO AM')
add_speech(doc,
    '"Nhìn vào bảng sản lượng theo AM: W36 ghi nhận sự phân hóa rõ rệt. '
    'Đề nghị từng AM báo cáo nguyên nhân sụt giảm sản lượng so với W35, '
    'đặc biệt các AM có sản lượng TTS giảm mạnh."'
)

# ===================== GTC =====================
add_section_title(doc, '📊', 'II.3 GTC TỔNG & PHÂN THEO AM (Full Hàng + TTS)')
add_speech(doc,
    '"Về %GTC tuần W36:\n'
    '• GTC full hàng tổng (Ca1+Ca2+Tồn) đạt 58,1% — gần như không đổi so với W35 (58,2%).\n'
    '• Ca1+Tồn cải thiện lên 60,5% (+0,8%p) — đây là tín hiệu tích cực.\n'
    '• Tuy nhiên Ca2 giảm mạnh xuống 48,4% (▼2,9%p) — cần tập trung cải thiện Ca2.\n'
    '• AM cải thiện GTC mạnh nhất: Nguyễn Thanh Long (+10,2%), Hồng Bích Nga (+4,5%), Lê Văn Trường (+3,5%).\n'
    '• AM giảm GTC mạnh nhất: Huỳnh Thúc Duân (-6,2%), Nguyễn Ngọc Khánh (-5,0%), Phan Đình Duy (-5,2%).\n'
    '→ Đề nghị các AM Huỳnh Thúc Duân, Nguyễn Ngọc Khánh, Phan Đình Duy báo cáo nguyên nhân và cam kết cải thiện."'
)
add_action(doc, 'AM Huỳnh Thúc Duân, Nguyễn Ngọc Khánh, Phan Đình Duy báo cáo nguyên nhân GTC giảm & kế hoạch cải thiện W37.', 'Trước họp W37')

# ===================== GTC CA1 TTS =====================
add_section_title(doc, '⭐', 'II.4 GTC CA1 TTS — CHỈ SỐ CÔNG TY QUAN TÂM')
add_speech(doc,
    '"GTC Ca1 TTS tuần W36:\n'
    '• GTC Ca1 thuần TTS đạt 74,8% — giảm -1,0%p so với W35 (75,8%). Đây là chỉ số Công ty theo dõi sát nhất.\n'
    '• GTC Ca1+Tồn TTS đạt 89,0% (+2,1%p) — cải thiện tốt.\n'
    '→ Cần tiếp tục push Ca1 thuần TTS về mốc ≥75% trong W37."'
)

# ===================== GÁN =====================
add_section_title(doc, '📋', 'II.5 TỶ LỆ GÁN VẬN HÀNH')
add_speech(doc,
    '"Tỷ lệ Gán tuần W36:\n'
    '• Full hàng – Tổng (Ca1+Ca2+Tồn): 83,5% (▲+1,4%p) — cải thiện tích cực.\n'
    '• Full hàng – Ca1+Tồn: 89,3% (▲+2,8%p) — rất tốt.\n'
    '• Full hàng – Ca2: 60,2% (▼-2,2%p) — cần chú ý.\n'
    '• TTS tổng: 83,4% (▲+1,1%p).\n'
    '→ Nhìn chung tỷ lệ Gán đang đi đúng hướng, duy trì và cải thiện trong W37."'
)

# ===================== ODR =====================
add_section_title(doc, '⏱️', 'II.6 ODR — TỶ LỆ GIAO ĐÚNG HẸN SLA')
add_speech(doc,
    '"ODR full hàng W36 đạt 92,9% — cải thiện +0,7%p so với W35 (92,2%). Đây là tín hiệu đáng mừng.\n'
    '• Tất cả các tỉnh đều cải thiện: Đắk Nông +2,9% (lên 89,1%), Lâm Đồng +0,9% (89,5%), Bình Thuận +0,6% (96,4%).\n'
    '• Khánh Hòa và Ninh Thuận giảm nhẹ -0,5% và -0,2% nhưng vẫn ở mức cao.\n'
    '• Theo AM cải thiện tốt nhất: Trương Quang Linh (+20,3% lên 60,4%), Lê Minh Lợi (+12,5% lên 71,0%).\n'
    '• AM cần chú ý: Trầm Hữu Tiến giảm -3,9% xuống 75,6% — thấp nhất vùng (sau anh Linh và anh Lợi).\n'
    '→ Đề nghị anh Trầm Hữu Tiến báo cáo kế hoạch đẩy ODR lên ≥80% trong W37."'
)
add_action(doc, 'AM Trầm Hữu Tiến: Kế hoạch cải thiện ODR lên ≥80% trong W37.', 'Trước họp W37')

# ===================== LTC =====================
add_section_title(doc, '📦', 'II.7 CHỈ SỐ %LTC — LẤY THÀNH CÔNG')
add_speech(doc,
    '"LTC full hàng W36 đạt 90,5% — giảm -0,6%p so với W35 (91,1%). Mức giảm chưa đáng lo nhưng cần theo dõi.\n'
    '• AM cải thiện tốt: Nguyễn Lê Nguyên Vũ (+4,6% lên 96,4%), Trương Quang Linh (+2,6%), Lê Văn Trường (+2,0%).\n'
    '• AM cần chú ý:\n'
    '  – Nguyễn Ngọc Khánh giảm mạnh nhất: -11,1% xuống 80,0%\n'
    '  – Nguyễn Thị Tuyết Thơ: -6,8% xuống 85,5%\n'
    '  – Huỳnh Thúc Duân: -3,6% xuống 89,9%\n'
    '  – Nguyễn Hoàng Phi: -3,3% xuống 89,6%\n'
    '→ Đặc biệt anh Khánh cần báo cáo nguyên nhân LTC giảm đột biến -11%."'
)
add_action(doc, 'AM Nguyễn Ngọc Khánh, Nguyễn Thị Tuyết Thơ: Báo cáo nguyên nhân LTC giảm mạnh & cam kết kế hoạch W37.', 'Trước họp W37')

# ===================== OPR TTS =====================
add_section_title(doc, '⏰', 'II.8 OPR TTS THEO KHUNG GIỜ')
add_speech(doc,
    '"OPR TTS theo khung giờ tuần W36: Tiếp tục theo dõi việc push đơn Ca1 và tỷ lệ hoàn thành Ca2.\n'
    '• Nhìn chung OPR TTS vẫn còn nhiều dư địa cải thiện ở khung giờ Ca1 sáng sớm.\n'
    '→ Yêu cầu các AM phối hợp với bưu cục để đảm bảo tỷ lệ phát Ca1 đạt ≥75% trong W37."'
)

# ===================== RỚT LC =====================
add_section_title(doc, '🚛', 'II.9 RỚT LUÂN CHUYỂN — %RỚT LC TOÀN VÙNG')
add_speech(doc,
    '"Rớt luân chuyển tuần W36 tăng lên 2,2% — tăng +0,7%p so với W35 (1,6%). Đây là mức tăng đáng lo ngại.\n'
    '• AM có rớt LC cao nhất: Lê Minh Lợi (100% — cần xác minh nguyên nhân cụ thể).\n'
    '• Trần Thị Nhung: 24,8%; Huỳnh Thúc Duân: 15,3%; Trầm Hữu Tiến: 6,7%; Hồng Bích Nga: 5,8%.\n'
    '→ Toàn bộ các AM có rớt LC trên 3% cần có giải trình ngay trong buổi họp này."'
)
add_action(doc, 'AM Lê Minh Lợi, Trần Thị Nhung, Huỳnh Thúc Duân: Báo cáo nguyên nhân rớt LC cao & kế hoạch xử lý.', 'Ngay trong họp')

# ===================== FD — MỤC MỚI =====================
add_section_title(doc, '🔄', 'II.10 %FD HOÀN TRẢ — BÁO CÁO LẦN ĐẦU TRONG HỌP TUẦN', color=(140, 30, 100))
add_speech(doc,
    '"Tuần này, ban đầu lần đầu tiên chúng ta đưa chỉ số FD Hoàn Trả vào báo cáo họp tuần chính thức.\n\n'
    'FD (Failed Delivery) là tỷ lệ đơn hàng hoàn trả — thể hiện chất lượng giao hàng lần đầu.\n\n'
    '• FD Full hàng toàn vùng W36: 7,5% (304.308 đơn giao / 22.954 đơn hoàn trả).\n'
    '• FD TTS toàn vùng W36: 6,8% (64.220 đơn / 4.365 đơn hoàn trả).\n\n'
    'TOP 5 BƯU CỤC FD CAO NHẤT TUẦN W36:\n'
    '  1. (DNO) Kiến Đức — AM Hồng Bích Nga: FD 43,7% — 1.422/3.254 đơn hoàn\n'
    '  2. (DNO) Quảng Tín — AM Trương Quang Linh: FD 28,8% — 573/1.988 đơn hoàn\n'
    '  3. (LDO) Lang Biang-Đà Lạt 1 — AM Lê Minh Lợi: FD 17,5% — 490/2.795 đơn hoàn\n'
    '  4. (KHO) Cam Linh — AM Nguyễn Thanh Long: FD 15,8% — 910/5.779 đơn hoàn\n'
    '  5. (DNO) Tuy Đức — AM Trần Thị Nhung: FD 13,3% — 236/1.781 đơn hoàn\n\n'
    '→ Đặc biệt BC Kiến Đức FD 43,7% là mức nghiêm trọng. Đề nghị AM Hồng Bích Nga và AM Trương Quang Linh báo cáo nguyên nhân và kế hoạch giảm FD trong W37."'
)
add_action(doc, 'AM Hồng Bích Nga (BC Kiến Đức), AM Trương Quang Linh (BC Quảng Tín): Báo cáo nguyên nhân FD cao & kế hoạch can thiệp W37.', 'Trước họp W37')
add_action(doc, 'Toàn bộ AM rà soát Top 3 bưu cục FD cao nhất trong khu vực của mình và lên kế hoạch cải thiện.', 'Trước họp W37')

# ===================== AGING =====================
add_section_title(doc, '⚠️', 'II.11 AGING TỒN KHO & HÀNG TREO LUÂN CHUYỂN')
add_speech(doc,
    '"Aging và hàng treo luân chuyển tuần W36:\n'
    '• Backlog luân chuyển toàn vùng hiện tại: 16.207 đơn — trong đó có 381 đơn treo trên 36h chưa đóng kiện (tập trung tại KTC Khánh Hòa, AM Nguyễn Tiến Lực).\n'
    '• Cần xử lý khẩn 381 đơn treo >36h ngay sau buổi họp.\n'
    '→ AM Nguyễn Tiến Lực báo cáo tình trạng và cam kết xử lý dứt điểm trong ngày."'
)
add_action(doc, 'AM Nguyễn Tiến Lực: Xử lý dứt điểm 381 đơn treo >36h tại KTC Khánh Hòa trong ngày hôm nay.', 'Ngay trong họp')

# ===================== KTC & VẬN TẢI — MỤC MỚI =====================
add_section_title(doc, '🚚', 'II.12 KTC & VẬN TẢI — BÁO CÁO LẦN ĐẦU TRONG HỌP TUẦN', color=(10, 100, 60))
add_speech(doc,
    '"Đây là lần đầu tiên chỉ số KTC và Vận Tải được báo cáo chính thức trong họp tuần vùng. '
    'Mục này bao gồm 3 phần: Backlog KTC, Leadtime, và Tỷ Lệ Lấp Đầy Xe (TLLĐ).\n\n'
    '【A】 BACKLOG KTC — ĐƠN TREO LUÂN CHUYỂN:\n'
    '• Tổng backlog luân chuyển toàn vùng: 16.207 đơn (phần lớn 0-6h: 12.309 đơn, chiếm 76%).\n'
    '• Đáng lo: 381 đơn treo trên 36h tại KTC Khánh Hòa — 100% thuộc AM Nguyễn Tiến Lực.\n'
    '• 5 KTC/KCT đang hoạt động: KTC Khánh Hòa (6.510đ), KCT Bình Thuận (3.634đ), KCT Bảo Lộc-LĐ (2.730đ), KCT Đức Trọng-LĐ (2.099đ), KCT Đắk Nông (1.234đ).\n\n'
    '【B】 LEADTIME KTC/KCT:\n'
    '• Thời gian nhận xuất trung bình toàn vùng: 3,31h (P50: 2,24h — P95: 7,09h).\n'
    '• Tỷ lệ tồn >12h: 2,1% (662 đơn); Tồn >24h: 0,1% (46 đơn) — nằm trong ngưỡng kiểm soát.\n'
    '• Lưu ý: KCT Đắk Nông có tỷ lệ tồn >12h cao nhất: 12,4% (405/3.272 đơn) → VI PHẠM SLA.\n\n'
    '【C】 TỶ LỆ LẤP ĐẦY XE (TLLĐ) — W35 VS W36:\n'
    '• TLLĐ bình quân toàn vùng W36: 48,1% — giảm -3,7%p so với W35 (51,8%).\n'
    '• Số chuyến W36: 516 chuyến (giảm 22 chuyến vs W35).\n'
    '• Số chuyến dưới 30% TLLĐ: 112/516 chuyến (21,7%) — cao hơn W35 (93/538 = 17,3%).\n'
    '• KCT Đắk Nông thấp nhất: 30,7% (▼-7,4%p vs W35).\n'
    '• KCT Đức Trọng giảm: 49,1% (▼-4,4%p).\n'
    '• Nguyên nhân chính chuyến <30% TLLĐ: Sản lượng bưu cục/hàng lấy về thấp (35%), Lộ trình ghé nhiều điểm ít hàng (12%), Chủ động giữ hàng ghép điểm (9%).\n\n'
    '→ Cần tập trung tối ưu lộ trình ghép điểm để nâng TLLĐ lên ≥52% trong W37."'
)
add_action(doc, 'AM Trương Quang Linh (KCT Đắk Nông): Rà soát và đề xuất giải pháp nâng TLLĐ KCT Đắk Nông lên ≥38% W37.', 'Trước họp W37')
add_action(doc, 'AM Nguyễn Minh Hoàng (KCT Đức Trọng): Xử lý 12,4% đơn tồn >12h tại KCT Đắk Nông.', 'Ngay trong ngày')
add_action(doc, 'Toàn bộ KTC/KCT: Rà soát và tối ưu các chuyến <30% TLLĐ bằng ghép điểm hoặc điều chỉnh lộ trình.', 'W37')

# ===================== COD TIỀN MẶT =====================
add_section_title(doc, '💳', 'III. KIỂM SOÁT — COD TIỀN MẶT (TỶ LỆ THANH TOÁN QR)')
add_speech(doc,
    '"Tỷ lệ COD tiền mặt toàn vùng W36 đạt 39,6% — tăng +1,1%p so với W35. '
    'Chỉ tiêu toàn công ty là ≤35%. Vùng NTB vẫn đang trên ngưỡng mục tiêu.\n'
    '→ Tiếp tục yêu cầu bưu tá đẩy mạnh thanh toán QR, mục tiêu ≤37% trong W37."'
)
add_action(doc, 'Tất cả AM: Tăng cường đào tạo bưu tá push QR, mục tiêu COD TM ≤37% tuần W37.', 'W37')

# ===================== TRUY THU =====================
add_section_title(doc, '🛡️', 'IV. TRUY THU VÀ PHẠT TICKET OE-IA')
add_speech(doc,
    '"Tổng truy thu toàn vùng W36 còn 174,6 triệu đồng — giảm -21,2 triệu so với W35. '
    'Đây là xu hướng tích cực, tuy nhiên vẫn còn ở mức cao.\n'
    '→ Đề nghị các AM theo dõi sát từng ticket và push xử lý trong tuần W37."'
)
add_action(doc, 'Tất cả AM: Rà soát ticket OE-IA còn tồn, phối hợp xử lý giảm truy thu xuống <150M trong W37.', 'Trước họp W37')

# ===================== KINH DOANH =====================
add_section_title(doc, '📈', 'V. KINH DOANH & KHÁCH HÀNG MỚI F30')
add_speech(doc,
    '"Về mảng kinh doanh tuần W36:\n'
    '• Sản lượng TTS giảm mạnh -13,4% (-9.759 đơn) — đây là tín hiệu cảnh báo về việc giữ chân khách hàng TikTok Shop.\n'
    '• Danh sách KH không lên đơn hoặc giảm so với cùng kỳ tuần trước đang được theo dõi — tập trung vào Top 10 KH có vol lớn đang rời bỏ để can thiệp kịp thời.\n'
    '• F30 (khách hàng mới): Dữ liệu đang được tổng hợp — các AM báo cáo số KH mới khai thác được trong tuần W36.\n'
    '→ Ưu tiên giữ chân các KH TTS đang giảm đơn; AM kinh doanh tăng tốc phát triển F30 trong W37."'
)
add_action(doc, 'AM Kinh Doanh: Báo cáo Top 10 KH lớn giảm đơn TTS và kế hoạch chăm sóc/giữ chân cụ thể.', 'Ngay trong họp')
add_action(doc, 'Tất cả AM: Báo cáo số KH F30 mới đã khai thác được trong W36.', 'Ngay trong họp')

# ===================== ACTION PLAN W37 =====================
add_section_title(doc, '🎯', 'VI. TỔNG HỢP GÓP Ý & ACTION PLAN TUẦN W37', color=(150, 40, 10))
add_speech(doc,
    '"Để chuẩn bị tốt cho tuần W37, toàn vùng NTB cần tập trung vào các mục tiêu trọng tâm sau:"'
)

actions_w37 = [
    ('Sản Lượng', 'Đẩy sản lượng phục hồi về ≥320.000 đơn full; TTS ≥70.000 đơn. Tập trung giữ chân KH TTS đang giảm.'),
    ('GTC Ca2', 'Các AM có GTC giảm (Huỳnh Thúc Duân, Nguyễn Ngọc Khánh, Phan Đình Duy) lên kế hoạch cụ thể cải thiện Ca2 ≥50%.'),
    ('ODR', 'AM Trầm Hữu Tiến cam kết đẩy ODR lên ≥80%. Mục tiêu toàn vùng ≥93,5%.'),
    ('LTC', 'AM Nguyễn Ngọc Khánh, Nguyễn Thị Tuyết Thơ giải trình và cam kết đẩy LTC lên ≥90% W37.'),
    ('FD Hoàn Trả', 'BC Kiến Đức (FD 43,7%) — AM Hồng Bích Nga lên phương án can thiệp khẩn. Mục tiêu FD toàn vùng ≤7%.'),
    ('Rớt LC', 'Xử lý 381 đơn treo >36h tại KTC Khánh Hòa ngay. Mục tiêu %Rớt LC toàn vùng ≤1,5%.'),
    ('TLLĐ Xe', 'Tối ưu lộ trình, ghép điểm để nâng TLLĐ lên ≥52%. Đặc biệt KCT Đắk Nông cần đạt ≥38%.'),
    ('KTC Đắk Nông', 'Xử lý 12,4% đơn tồn >12h (405 đơn) ngay trong ngày.'),
    ('COD TM', 'Đẩy QR xuống ≤37% trong W37 bằng đào tạo bưu tá.'),
    ('Truy Thu', 'Xử lý ticket OE-IA, giảm tổng truy thu xuống <150M.'),
]

for i, (cat, action) in enumerate(actions_w37, 1):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.5)
    r1 = p.add_run(f'{i}. [{cat}] ')
    r1.bold = True
    r1.font.size = Pt(11.5)
    r1.font.name = 'Times New Roman'
    r1.font.color.rgb = RGBColor(30, 80, 160)
    r2 = p.add_run(action)
    r2.font.size = Pt(11.5)
    r2.font.name = 'Times New Roman'

doc.add_paragraph()
add_divider(doc)
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('— GHN NTB – Báo Cáo Tuần W36 | Ngày 07/09/2026 —')
r.italic = True
r.font.size = Pt(10)
r.font.name = 'Times New Roman'
r.font.color.rgb = RGBColor(120, 120, 120)

# ===================== LƯU FILE =====================
output_path = r'C:\Users\lap4all\Desktop\New folder\KICH_BAN_THUYET_TRINH_W36_NTB.docx'
doc.save(output_path)
print(f'✅ Saved: {output_path}')
