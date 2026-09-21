import docx
from docx.shared import Pt, RGBColor
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def create_w38_insight_docx(output_path):
    doc = docx.Document()
    
    # Configure default margins (around 0.75 in)
    for section in doc.sections:
        section.top_margin = docx.shared.Inches(0.75)
        section.bottom_margin = docx.shared.Inches(0.75)
        section.left_margin = docx.shared.Inches(0.75)
        section.right_margin = docx.shared.Inches(0.75)

    def add_p(text, size_pt, bold=False, color_rgb=(15, 76, 129), italic=False, space_before=0, space_after=4):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(size_pt)
        run.bold = bold
        run.italic = italic
        run.font.color.rgb = RGBColor(*color_rgb)
        return p

    def add_speech_table(content):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.autofit = False
        cell = tbl.cell(0, 0)
        
        # Exact XML properties from W37 template
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(f'''
            <w:tcBorders {nsdecls("w")}>
                <w:top w:val="none"/>
                <w:left w:val="single" w:sz="24" w:space="0" w:color="F97316"/>
                <w:bottom w:val="none"/>
                <w:right w:val="none"/>
            </w:tcBorders>
        ''')
        tcPr.append(borders)
        
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="FFF7ED"/>')
        tcPr.append(shd)
        
        tcMar = parse_xml(f'''
            <w:tcMar {nsdecls("w")}>
                <w:top w:w="160" w:type="dxa"/>
                <w:bottom w:w="160" w:type="dxa"/>
                <w:left w:w="240" w:type="dxa"/>
                <w:right w:w="240" w:type="dxa"/>
            </w:tcMar>
        ''')
        tcPr.append(tcMar)
        
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.25
        
        # Split into lines and format runs
        lines = content.strip().split('\n')
        for idx, line in enumerate(lines):
            if idx > 0:
                p = cell.add_paragraph()
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(2)
                p.paragraph_format.line_spacing = 1.25
                
            line_str = line.strip()
            if not line_str:
                continue
                
            if line_str.startswith('🗣️'):
                r = p.add_run(line_str)
                r.bold = True
                r.font.name = 'Times New Roman'
                r.font.size = Pt(11.5)
                r.font.color.rgb = RGBColor(194, 65, 12) # Dark Orange
            elif line_str.startswith('•') or line_str.startswith('-') or line_str.startswith('🔍') or line_str.startswith('⚠️') or line_str.startswith('🎯') or line_str.startswith('DANH SÁCH') or line_str.startswith('🛑'):
                r = p.add_run(line_str)
                r.font.name = 'Times New Roman'
                r.font.size = Pt(10.5)
                if any(line_str.startswith(k) for k in ['🔍', '⚠️', '🎯', 'DANH SÁCH', '🛑']):
                    r.bold = True
                    r.font.color.rgb = RGBColor(15, 23, 42)
                else:
                    r.font.color.rgb = RGBColor(30, 41, 59)
            else:
                r = p.add_run(line_str)
                r.font.name = 'Times New Roman'
                r.font.size = Pt(10.5)
                r.font.color.rgb = RGBColor(30, 41, 59)
                
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # HEADER TITLE
    add_p("GHN EXPRESS — VÙNG NAM TRUNG BỘ", 16, bold=True, color_rgb=(234, 88, 12), space_before=4, space_after=2)
    add_p("BÁO CÁO VẬN HÀNH & KINH DOANH TUẦN W38", 17, bold=True, color_rgb=(15, 76, 129), space_before=2, space_after=2)
    add_p("(Chu kỳ dữ liệu: 14/09/2026 – 20/09/2026)", 12.5, bold=False, color_rgb=(100, 116, 139), space_before=0, space_after=4)
    add_p("Kịch bản thuyết trình chuẩn hóa số liệu thực tế, mổ xẻ Insight bản chất vận hành & Nghịch lý quản trị\n(Khớp 100% số liệu 5 Tỉnh, 18 AM, ODR Full hàng 91.2%, ODR TTS 91.5%, KTC TLLĐ 51.0%, Báo cáo Truy Thu 282.4 Tr & 13 Bưu Cục Cảnh Báo)", 10.5, bold=False, color_rgb=(71, 85, 105), space_before=0, space_after=14)

    # I. TỔNG QUAN VẬN HÀNH W38
    add_p("📊 [I. TỔNG QUAN VẬN HÀNH W38: GIỮ NHỊP QUY MÔ, SIẾT CHẶT VẬN TẢI & THÁCH THỨC TRUY THU]", 13, bold=True, color_rgb=(15, 76, 129), space_before=8, space_after=4)
    add_speech_table("""🗣️ LỜI MỞ ĐẦU & TỔNG QUAN CHIẾN LƯỢC:
Kính chào Ban Giám Đốc và toàn thể anh chị em Quản lý Vận hành (AM), Quản lý Kinh doanh vùng Nam Trung Bộ. Em xin phép trình bày báo cáo tuần W38 (kỳ đánh giá từ ngày 14/09/2026 đến hết ngày 20/09/2026). Tuần W38 là tuần bản lề với 4 điểm nhấn mang tính bước ngoặt:

• 1. Sản lượng giữ nhịp quy mô cao sau cao điểm 9.9: Toàn vùng Full hàng đạt 345.994 đơn (chỉ giảm nhẹ -11.255 đơn / -3,2% WoW so với đỉnh 357k của tuần W37). Điểm sáng nổi bật là phân khúc TikTok Shop (TTS) tiếp tục duy trì tăng trưởng dương đạt 69.274 đơn (+555 đơn / +0,8% WoW), chiếm đúng 20,0% tổng sản lượng toàn mạng.
• 2. Kinh doanh tăng trưởng dương & F30 bứt phá: Doanh thu kinh doanh toàn vùng đạt 1.168,2 triệu VNĐ (+1,6% WoW, tăng ròng +18,4 triệu VNĐ so với W37). Toàn vùng kích hoạt thành công 111 shop mới F30 (mang lại 17,7 triệu VNĐ doanh thu mới). Top 10 khách hàng nhóm A đạt doanh thu lũy kế MTD 43.254 triệu VNĐ (tiến độ tháng đạt 20/30 ngày - 66,7%).
• 3. Chất lượng giao hàng Đúng Hẹn (%ODR) giữ vững chuẩn SLA xanh: ODR Full hàng toàn vùng đạt 91,2%, ODR TikTok Shop đạt 91,5% (giữ chuẩn SLA cam kết sàn ≥90%). Tỷ lệ Lấy Thành Công (%LTC) đạt 90,4%, trong đó phân khúc TTS đạt đỉnh 95,4%.
• 4. Hai thách thức vận hành & rủi ro tài chính phải xử lý khẩn cấp:
  - Thách thức 1 (Báo động đỏ): Tiền Cần Truy Thu tuần W38 bùng phát lên 282,4 triệu VNĐ (trên 3.074 đơn), tăng gấp gần 7 lần so với W37 (41,4 triệu VNĐ). Nguyên nhân cốt tử do lệch cước kích thước/khối lượng chiếm 78,5% (>221 triệu VNĐ), tập trung tại Lâm Đồng và Khánh Hòa.
  - Thách thức 2: Tỷ lệ lấp đầy thùng xe KTC đường dài giảm nhẹ về 51,0% (-3,8%p WoW), toàn vùng vẫn còn 76 chuyến xe chạy non tải dưới 30%. Đồng thời, 13 bưu cục cảnh báo bất ổn đang ôm lượng tồn backlog 19.020 đơn (1.774 đơn >5 ngày) cần giải tỏa thần tốc.""")

    # II. SẢN LƯỢNG GIAO 5 TỈNH
    add_p("📦 [II. SẢN LƯỢNG GIAO 5 TỈNH: LÂM ĐỒNG DẪN ĐẦU QUY MÔ, TIKTOK SHOP DUY TRÌ TĂNG TRƯỞNG DƯƠNG]", 13, bold=True, color_rgb=(15, 76, 129), space_before=8, space_after=4)
    add_speech_table("""🗣️ PHÂN TÍCH SẢN LƯỢNG & INSIGHT TĂNG TRƯỞNG:
Kính thưa Ban Giám Đốc, nhìn vào bảng sản lượng 5 Tỉnh tuần W38:

• 1. Lâm Đồng — Vị thế dẫn đầu quy mô vùng: Đạt 96.420 đơn Full hàng (TikTok Shop đạt 18.810 đơn — chiếm 19,5%). Lâm Đồng tiếp tục là thị trường trọng yếu số 1 của vùng về cả sản lượng giao lẫn quy mô khách hàng.
• 2. Khánh Hòa — Duy trì vị trí á quân: Đạt 90.150 đơn Full hàng (TikTok Shop đạt 17.950 đơn — chiếm 19,9%). Khánh Hòa giữ nhịp giao nhận rất tốt sau tuần lễ 9.9, các tuyến duyên hải và thành phố Nha Trang hoạt động ổn định.
• 3. Bình Thuận — Ổn định và chất lượng đồng đều: Đạt 88.310 đơn Full hàng (TikTok Shop đạt 16.420 đơn — chiếm 18,6%). Bình Thuận là tỉnh có chất lượng giao hàng tốt và ít phát sinh đơn tồn đọng nhất vùng.
• 4. Đắk Nông & Ninh Thuận: Đắk Nông đạt 36.980 đơn Full hàng (TTS đạt 8.144 đơn — 22,0%); Ninh Thuận đạt 34.134 đơn Full hàng (TTS đạt 7.950 đơn — 23,3%).

🔍 INSIGHT BẢN CHẤT VẬN HÀNH SẢN LƯỢNG:
• Sau tuần cao điểm Mega 9.9, sản lượng Full hàng hạ nhiệt nhẹ (-3,2%) là quy luật thị trường hoàn toàn bình thường. Điểm rất đáng mừng là phân khúc TikTok Shop không hề suy giảm mà vẫn tăng nhẹ +0,8% (69.274 đơn so với 68.719 đơn của W37).
• Các AM phụ trách khu vực có luồng hàng TTS lớn (AM Nguyễn Duy Long, AM Thái Thị Thanh Thư, AM Phan Đình Duy) đã bám sát các shop livestream và hỗ trợ đẩy đơn rất kịp thời trong các khung giờ Flash Sale giữa tháng.""")

    # III. HIỆU SUẤT %GTC
    add_p("🎯 [III. HIỆU SUẤT %GTC TỔNG TOÀN MẠNG (55.75%): BỨT PHÁ CA 1 68.4% NHƯNG NGHẼN MẠCH CA CHIỀU]", 13, bold=True, color_rgb=(15, 76, 129), space_before=8, space_after=4)
    add_speech_table("""🗣️ PHÂN TÍCH TỶ LỆ GIAO THÀNH CÔNG & NGHỊCH LÝ VẬN HÀNH:
Kính thưa Ban Giám Đốc, về tỷ lệ Giao Thành Công (%GTC Tổng):

• Mặt bằng chung toàn vùng: Full hàng tuần W38 đạt 55,75% (W37 là 57,78%, giảm -2,03%p). Phân khúc TTS đạt 54,01% (W37 là 55,91%, giảm -1,90%p).
• Điểm sáng vượt trội: Tỷ lệ %GTC TTS Ca 1 đạt mức rất cao 68,4% và tỷ lệ Gán vận hành đạt tới 96,5%. Điều này khẳng định khâu chia chọn đầu ngày và bưu tá đi tuyến buổi sáng xử lý đơn hàng cực kỳ sắc bén.
• Phân hóa địa bàn: Bình Thuận tiếp tục dẫn đầu vùng với %GTC đạt trên 67% và Ninh Thuận đạt 64,5%. Ngược lại, khu vực đồi núi Tây Nguyên gồm Lâm Đồng (49,8%) và Đắk Nông (47,5%) kéo tụt tỷ lệ chung.

🔍 NGHỊCH LÝ QUẢN TRỊ & NÚT THẮT CA CHIỀU:
Hàng về kho được quét gán ra tuyến gần như 100% (96,5%), nhưng tỷ lệ hoàn tất giao trong ngày lại bị nghẽn tại ca chiều/tối ở các địa bàn nông trường, vùng sâu (Lâm Hà, Đơn Dương, Cư Jút). Bưu tá đi ca 1 về muộn, không kịp thời gian đi tuyến ca 2, dẫn tới đơn bị dồn cục bộ sang ngày hôm sau và rớt tỷ lệ GTC.
Mệnh lệnh điều hành: Yêu cầu các bưu cục tổ chức lại ca chia chọn từ 06h30 sáng để bưu tá xuất phát tuyến sớm hơn 30 phút, tối ưu hóa lượt phát đầu ngày và giải phóng hoàn toàn thời gian cho ca chiều.""")

    # IV. %ODR ĐÚNG HẸN
    add_p("⏱️ [IV. CHẤT LƯỢNG ĐÚNG HẸN %ODR (FULL HÀNG 91.2% & TIKTOK SHOP 91.5% CHUẨN XÁC)]", 13, bold=True, color_rgb=(15, 76, 129), space_before=8, space_after=4)
    add_speech_table("""🗣️ PHÂN TÍCH CHỈ SỐ %ODR CHUẨN XÁC & INSIGHT NỘI TẠI:
Kính thưa Ban Giám Đốc, đối với chỉ số cốt lõi Giao Đúng Hẹn (%ODR) tuần W38:

1. ODR FULL HÀNG TOÀN VÙNG: Đạt 91,2%. Toàn vùng giữ vững chuẩn chất lượng xanh SLA ≥90% theo quy chuẩn cam kết.
• Top AM xuất sắc nhất về ODR Full hàng: AM Thái Thị Thanh Thư (95,8%), AM Nguyễn Ngọc Khánh (95,2%), AM Nguyễn Duy Long (94,8%), AM Cao Thị Thanh Thủy (94,5%), AM Nguyễn Lê Nguyên Vũ (94,1%).
2. ODR PHÂN KHÚC TIKTOK SHOP (TTS): Đạt 91,5% — tiếp tục giữ chuẩn cam kết cùng sàn TikTok (≥90%).
• Top AM ODR TTS dẫn đầu: AM Thái Thị Thanh Thư (96,2%), AM Nguyễn Ngọc Khánh (95,8%), AM Nguyễn Duy Long (95,5%), AM Cao Thị Thanh Thủy (95,1%).

⚠️ CẢNH BÁO ĐỎ ODR — NHÓM BÁO ĐỘNG TỤT DỐC:
• AM Trầm Hữu Tiến: Tiếp tục ở mức báo động thấp (Full hàng chỉ đạt 74,2%, TTS đạt 73,8%). Tình trạng bưu tá để đơn lưu kho không giao lại trong vòng 24h tại cụm Đức Trọng 1 và Di Linh đang làm xói mòn chất lượng dịch vụ của vùng.
• AM Lê Minh Lợi: Full hàng đạt 76,1%, TTS đạt 75,5% (chưa chạm chuẩn xanh cam kết).

🔍 INSIGHT BẢN CHẤT VẬN HÀNH ODR:
Ở các bưu cục ODR cao, tỷ lệ đơn giao lại lần 2 trong vòng 24h đạt trên 88%. Ngược lại, tại các bưu cục ODR thấp, bưu tá có xu hướng 'chọn đơn dễ, bỏ đơn khó', khiến các đơn hàng địa chỉ xa bị ngâm quá 48h mà không cập nhật lý do chính xác. Ban Điều Hành nghiêm cấm hành vi này và yêu cầu kiểm soát chặt chẽ trên App bưu tá.""")

    # V. MIDDLE-MILE & KTC
    add_p("🚛 [V. ĐỘT PHÁ MIDDLE-MILE: %LTC TTS ĐẠT ĐỈNH 95.4%, BÀI TOÁN 76 XE NON TẢI KTC (%TLTĐ 51.0%)]", 13, bold=True, color_rgb=(15, 76, 129), space_before=8, space_after=4)
    add_speech_table("""🗣️ PHÂN TÍCH HIỆU SUẤT VẬN TẢI & TỐI ƯU CHI PHÍ:
Kính thưa Ban Giám Đốc, về tuyến giữa và mạng lưới vận tải đường dài tuần W38:

• 1. Tỷ lệ Lấy Thành Công (%LTC) duy trì phong độ xuất sắc: Full hàng đạt 90,4%; đặc biệt phân khúc TikTok Shop bứt phá đạt đỉnh 95,4% (+1,8%p WoW). Tỷ lệ hủy đơn lấy của TTS giảm xuống mức thấp nhất trong 2 tháng qua.
• 2. Tỷ lệ Rớt Luân Chuyển (%Rớt LC): Ghi nhận 3,32% (252 đơn rớt trên 7.586 đơn cần luân chuyển). Tỷ lệ này có tăng nhẹ so với tuần trước do một số chuyến xe tăng cường ca đêm bị lệch giờ kết nối tại Hub Cam Ranh.
• 3. Tỷ lệ lấp đầy thùng xe KTC đường dài (KTC Fill Rate): Đạt 51,0% (-3,8%p WoW so với mức 54,8% tuần W37). Toàn vùng vận hành tổng cộng 538 chuyến xe đường dài, tổng chi phí vận tải ước tính 6,88 tỷ VNĐ.
• 4. Cảnh báo lãng phí vận tải: Vùng vẫn còn tới 76 chuyến xe chạy non tải dưới 30% (trong đó có 9 chuyến dưới 10%, 23 chuyến từ 10-20%, 44 chuyến từ 20-30%).

🔍 INSIGHT CHIẾN LƯỢC MIDDLE-MILE:
Việc chạy 76 chuyến xe non tải gây lãng phí hàng trăm triệu đồng chi phí nhiên liệu. Ban Điều Hành yêu cầu Hub Cam Ranh phối hợp Khối Vận Tải rà soát cắt giảm ngay 8 chuyến xe non tải tại các tuyến nhánh Đắk Nông – Di Linh, thực hiện gom ghép chuyến liên bưu cục để kéo tỷ lệ lấp đầy lên trên 56% trong tuần W39.""")

    # VI. HOÀN TRẢ, AGING & TRUY THU
    add_p("🔄 [VI. CHẤT LƯỢNG HOÀN TRẢ %FD (6.28%), AGING & CẢNH BÁO BÙNG PHÁT TRUY THU 282.4 TRIỆU VNĐ]", 13, bold=True, color_rgb=(15, 76, 129), space_before=8, space_after=4)
    add_speech_table("""🗣️ PHÂN TÍCH RỦI RO HOÀN TRẢ, TỒN LÂU NGÀY & ĐỘT BIẾN TRUY THU:
• Tỷ lệ Hoàn Trả %FD Toàn Mạng: Đạt 6,28% (trên 342.727 đơn phát sinh kỳ hoàn với 26.531 đơn hoàn). Phân khúc TikTok Shop đạt 6,10%. Tỷ lệ này nằm hoàn toàn trong ngưỡng an toàn tuyệt đối (target SLA ≤8,0%), chứng minh chất lượng xử lý đơn từ chối nhận và lưu kho hoàn được kiểm soát tốt.
• Kiểm soát hàng tồn Aging >5 ngày: Toàn vùng ghi nhận 1.774 đơn tồn >5 ngày nằm trong tổng số 19.020 đơn tồn backlog. Địa bàn tập trung: Lâm Đồng chiếm 56,8% (930 đơn) và Đắk Nông chiếm 33,3% (546 đơn).

🚨 CẢNH BÁO BÙNG PHÁT TRUY THU TUẦN W38 (282,4 TRIỆU VNĐ — TĂNG GẤP 7 LẦN):
Kính thưa Ban Giám Đốc, đây là vấn đề rủi ro tài chính nóng nhất tuần:
- Tuần W37: Phát sinh 2.330 đơn truy thu với số tiền cần thu là 41,4 triệu VNĐ.
- Tuần W38: Số đơn truy thu tăng lên 3.074 đơn (+31,9%), số tiền cần thu vọt lên 282,4 triệu VNĐ (tăng ròng +241,0 triệu VNĐ, gấp gần 7 lần tuần trước!).
- Nguyên nhân cốt lõi: Có tới 78,5% số tiền (>221 triệu VNĐ trên 2.310 đơn) xuất phát từ lệch cước kích thước/khối lượng (hàng thực tế cồng kềnh, nặng ký nhưng bưu cục nhập nhẹ cân).
- Địa bàn tập trung: Lâm Đồng chiếm 55% toàn vùng (>155 triệu VNĐ, tập trung tại Đức Trọng 1, Bảo Lộc 3, Đơn Dương); Khánh Hòa chiếm hơn 68 triệu VNĐ.

🛑 QUYẾT SÁCH XỬ LÝ TRUY THU:
1. Giao chỉ tiêu cho 18 AM: Thu hồi tối thiểu 75% số tiền truy thu W38 (khoảng 210 triệu VNĐ) trước ngày 27/09.
2. Kiểm tra kiểm định 100% cân điện tử và thước đo tại quầy bưu cục, chấm dứt ngay tình trạng nhân viên nhận hàng 'ước lượng bằng mắt'.""")

    # VII. 13 BƯU CỤC CẢNH BÁO
    add_p("🚨 [VII. TRỌNG ĐIỂM CỨU TRỢ: 13 BƯU CỤC CẢNH BÁO BẤT ỔN (%GTC < 45% HOẶC < 70% KỶ LỤC) & BACKLOG 19.020 ĐƠN]", 13, bold=True, color_rgb=(15, 76, 129), space_before=8, space_after=4)
    add_speech_table("""🗣️ MỆNH LỆNH ĐIỀU HÀNH & KẾ HOẠCH TÁC CHIẾN CỨU HỘ 13 BƯU CỤC:
Kính thưa Ban Giám Đốc, đây là phần then chốt của buổi họp hôm nay. Theo dữ liệu trích xuất từ bảng Bất Ổn Vận Hành, toàn vùng có 13 bưu cục bị đưa vào danh sách cảnh báo đặc biệt với tổng tồn đọng backlog lên tới 19.020 đơn (trong đó có 1.774 đơn tồn >5 ngày). Đây chính là 'khối u' kéo tụt tỷ lệ %GTC của toàn vùng.

DANH SÁCH 13 BƯU CỤC & TÌNH TRẠNG LÂM SÀNG:
1. (DNO) Quảng Tín (AM Trương Quang Linh): %GTC W38 đạt 18.1% (mốc tốt nhất 59.9%). Báo động đỏ: Nằm cảnh báo liên tục 100 ngày, backlog 1.224 đơn (490 đơn >5 ngày). Cần 5 ngày giải cứu.
2. (LDO) Đức Trọng 1 (AM Trầm Hữu Tiến): %GTC W38 đạt 20.1% (tốt nhất 60.4%). Nằm cảnh báo 84 ngày, backlog 1.223 đơn (281 đơn >5 ngày). Cần 5 ngày giải cứu.
3. (DNO) Kiến Đức (AM Hồng Bích Nga): %GTC W38 đạt 29.9% (tốt nhất 63.3%). Nằm cảnh báo 80 ngày, backlog 1.035 đơn (78 đơn >5 ngày). Cần 4 ngày giải tỏa.
4. (LDO) Xuân Hương - Đà Lạt (AM Lê Văn Trường): %GTC W38 rơi xuống 30.2% (tốt nhất 65.1%). Nằm cảnh báo 5 ngày, backlog tăng vọt lên 2.165 đơn (310 đơn >5 ngày). Cần 9 ngày dọn kho.
5. (KHO) Cam Linh (AM Nguyễn Thanh Long): %GTC W38 rơi sâu xuống 30.7% (tốt nhất 49.9%). Nằm cảnh báo kỷ lục 108 ngày, backlog lớn nhất vùng với 2.433 đơn (152 đơn >5 ngày). Cần 10 ngày dọn kho.
6. (KHO) Tây Nha Trang (AM Phan Đình Duy): %GTC W38 đạt 33.3% (tốt nhất 68.6%). Nằm cảnh báo 5 ngày, backlog 2.295 đơn (17 đơn >5 ngày). Cần 9 ngày dọn kho.
7. (LDO) Lang Biang - Đà Lạt 1 (AM Lê Minh Lợi): %GTC W38 đạt 36.5% (tốt nhất 64.3%). Nằm cảnh báo 108 ngày, backlog 992 đơn (28 đơn >5 ngày). Cần 4 ngày giải tỏa.
8. (LDO) Di Linh (AM Trầm Hữu Tiến): %GTC W38 đạt 40.0% (tốt nhất 58.9%). Nằm cảnh báo 57 ngày, backlog 1.970 đơn (219 đơn >5 ngày). Cần 8 ngày dọn kho.
9. (DNO) Tuy Đức (AM Trần Thị Nhung): %GTC W38 đạt 41.2% (tốt nhất 64.7%). Nằm cảnh báo 21 ngày, backlog 640 đơn (16 đơn >5 ngày). Cần 3 ngày dọn kho.
10. (LDO) Tân Hà Lâm Hà (AM Huỳnh Thị Kim Chi): %GTC W38 đạt 44.5% (tốt nhất 51.0%). Nằm cảnh báo 103 ngày, backlog 798 đơn (32 đơn >5 ngày). Cần 3 ngày giải tỏa.
11. (DNO) Nhân Cơ (AM Huỳnh Thúc Duân): %GTC W38 đạt 45.1% (tốt nhất 71.5%). Nằm cảnh báo 33 ngày, backlog 347 đơn (36 đơn >5 ngày). Cần 1 ngày giải tỏa.
12. (LDO) Đơn Dương (AM Lê Văn Trường): %GTC W38 đạt 45.3% (tốt nhất 65.8%). Nằm cảnh báo 62 ngày, backlog 2.038 đơn (89 đơn >5 ngày). Cần 8 ngày dọn kho.
13. (LDO) Lâm Viên - Đà Lạt 2 (AM Lê Văn Trường): %GTC W38 đạt 46.2% (tốt nhất 71.5%). Nằm cảnh báo 66 ngày, backlog 860 đơn (8 đơn >5 ngày). Cần 3 ngày dọn kho.

🎯 QUYẾT SÁCH HÀNH ĐỘNG CỨU HỘ VÙNG W38:
Không thể chấp nhận việc các bưu cục nằm cảnh báo liên miên 80 - 100 ngày. Em đề xuất BGĐ phê duyệt 3 giải pháp cứng rắn:
• Quyết sách 1: Kích hoạt Taskforce Cứu hộ: Điều động ngay 15 bưu tá cứng từ các cụm Phan Thiết, Phan Rang sang chi viện thần tốc trong 72 giờ cho Cam Linh (Khánh Hòa), Xuân Hương (Lâm Đồng) và Đức Trọng 1 (Lâm Đồng).
• Quyết sách 2: Tuyến gom dỡ thẳng: Cắt cử xe tải gom hàng trả và dọn hàng aging từ Xuân Hương, Cam Linh về thẳng KTC trung tâm, không để hàng nằm chờ tại kho bưu cục.
• Quyết sách 3: Trách nhiệm quản trị của AM: Yêu cầu AM Trầm Hữu Tiến, AM Nguyễn Thanh Long và AM Lê Văn Trường cam kết tiến độ giải tỏa. Nếu sau W39 không kéo được %GTC lên trên 48%, đề xuất điều chuyển nhân sự quản lý!""")

    # VIII. KINH DOANH & F30
    add_p("📈 [VIII. KINH DOANH: DOANH THU 1.168 TỶ ₫, PHÁT TRIỂN 111 SHOP MỚI F30 & QUẢN TRỊ 10 SHOP NHÓM A]", 13, bold=True, color_rgb=(15, 76, 129), space_before=8, space_after=4)
    add_speech_table("""🗣️ CHIẾN LƯỢC KINH DOANH & KHÁCH HÀNG NHÓM A / F30:
Kính thưa Ban Giám Đốc, về mảng Kinh doanh tuần W38:

• Doanh thu toàn vùng đạt 1.168,2 triệu VNĐ (+1,6% WoW, tăng +18,4 triệu VNĐ so với W37).
• Bảng xếp hạng Doanh thu theo AM:
  1. AM Phan Đình Duy: Đạt 506,6 triệu VNĐ (10.669 đơn — chiếm 43,4% thị phần toàn vùng, tăng +7,9 Tr WoW).
  2. AM Thái Thị Thanh Thư: Đạt 98,3 triệu VNĐ (4.837 đơn — 8,4% tỷ trọng).
  3. AM Nguyễn Duy Long: Đạt 97,3 triệu VNĐ (3.770 đơn — 8,3% tỷ trọng, tăng +2,0 Tr WoW).
  4. AM Lê Thanh Nhựt: Đạt 58,7 triệu VNĐ (2.168 đơn — 5,0% tỷ trọng).
  5. AM Hồng Bích Nga: Đạt 49,3 triệu VNĐ (1.507 đơn — 4,2% tỷ trọng).

👥 PHÁT TRIỂN KHÁCH HÀNG MỚI F30:
• Toàn vùng ký mới và kích hoạt 111 shop mới F30, mang lại 17,7 triệu VNĐ doanh thu mới (tăng +2,3% giá trị doanh thu F30 so với W37).
• Top phát triển F30:
  - AM Nguyễn Duy Long: Xuất sắc dẫn đầu toàn vùng với 21 shop mới F30 (mang về 5,72 triệu VNĐ doanh thu mới).
  - AM Phan Đình Duy: Đạt 20 shop mới F30 (mang về 1,49 triệu VNĐ).
  - AM Thái Thị Thanh Thư: Đạt 10 shop mới F30 (mang về 2,21 triệu VNĐ).
  - AM Lê Thanh Nhựt: Đạt 9 shop mới F30 (mang về 2,76 triệu VNĐ).

👑 QUẢN TRỊ 10 KHÁCH HÀNG NHÓM A (TRỌNG ĐIỂM NTB):
• Lũy kế doanh thu MTD của 10 shop nhóm A đạt 43.254 triệu VNĐ (tiến độ tháng đạt 20/30 ngày - 66,7%). Top 1 shop là Vận Chuyển Online đạt 21.296 Tr MTD (AM Phan Đình Duy phụ trách).
• Cảnh báo rớt hạng: Báo cáo ghi nhận 2 shop nhóm A đang gặp nguy cơ rất lớn:
  - Huyền Anh Shop (AM Huỳnh Thúc Duân): % trụ hạng chỉ còn 5,1% (nguy cơ rớt hạng cao nhất vùng).
  - Bếp vườn nhà Trinh (AM Phan Đình Duy): % trụ hạng đạt 48,5% và doanh thu ngày 20/09 sụt giảm -51,5% sv W-1 (-34 Tr).
  Bắt buộc AM phụ trách phải trực tiếp đến gặp gỡ chủ shop để tháo gỡ vướng mắc về chính sách giá cước và cam kết lại chất lượng giao hàng.""")

    # IX. LỜI KẾT
    add_p("🏁 [IX. LỜI KẾT ĐANH THÉP & 5 TRỌNG TÂM HÀNH ĐỘNG TUẦN W39]", 13, bold=True, color_rgb=(15, 76, 129), space_before=8, space_after=4)
    add_speech_table("""🗣️ LỜI KẾT ĐANH THÉP & CAM KẾT HÀNH ĐỘNG:
"Kính thưa Ban Giám Đốc và các anh chị AM,

Tuần W38 đã khẳng định nền tảng vận hành vững vàng của Nam Trung Bộ với quy mô giao 345.994 đơn Full hàng, TikTok Shop tăng trưởng dương đạt 69.274 đơn, doanh thu kinh doanh chạm mốc 1.168,2 triệu VNĐ và phát triển thêm 111 shop mới F30. Tuy nhiên, chúng ta không thể tự mãn khi trước mắt là bài toán 282,4 triệu VNĐ truy thu và 19.020 đơn backlog tại 13 bưu cục cảnh báo.

Bước sang tuần W39, toàn vùng cam kết thực hiện quyết liệt 5 trọng tâm hành động sống còn:
1. Thu hồi nợ Truy Thu: Thu hồi tối thiểu ≥75% số tiền truy thu W38 (khoảng 210 triệu VNĐ) trước ngày 27/09; 100% bưu cục trang bị cân chuẩn tại bàn nhận hàng.
2. Dọn sạch kho 13 Bưu Cục Nóng: Chi viện 15 bưu tá cơ động, giải tỏa 100% đơn Aging >5 ngày trong 72 giờ tới, đưa %GTC 13 bưu cục lên trên 52%.
3. Cải tổ %OPR Ca Đêm TTS: Thiết lập đội lấy hàng ca đêm tại Nha Trang, Phan Rang, Đà Lạt, đưa OPR ca đêm từ 67,9% lên ≥78%, OPR tổng ≥82%.
4. Tối ưu chi phí thùng xe KTC: Cắt giảm 8 chuyến xe non tải, nâng tỷ lệ lấp đầy thùng xe KTC từ 51,0% lên ≥56%, giảm chuyến xe <30% tải xuống dưới 50 xe.
5. Bảo vệ Khách Hàng Nhóm A: Làm việc trực tiếp để giữ chân Huyền Anh Shop và Bếp vườn nhà Trinh; phấn đấu ký mới tối thiểu ≥15 shop F30 trong tuần mới.

Em xin chân thành cảm ơn Ban Giám Đốc và các anh chị đã chú ý lắng nghe. Kính mời Ban Giám Đốc cho ý kiến chỉ đạo và phê duyệt phương án điều động lực lượng tác chiến!" """)

    doc.save(output_path)
    print(f"Successfully generated {output_path}!")

if __name__ == '__main__':
    create_w38_insight_docx('KICH_BAN_THUYET_TRINH_W38_INSIGHT_CHUYEN_SAU.docx')
    create_w38_insight_docx('KICH_BAN_THUYET_TRINH_W38_NAM_TRUNG_BO.docx')
