import os, sys, docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

sys.path.insert(0, os.path.join(os.getcwd(), 'scratch'))
from doc_builder_helpers import format_run
from speech_builder_helper import add_speech_section

def build_w38_professional_script():
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
    format_run(r0, font_size_pt=10, bold=True, color_rgb=(0x64, 0x74, 0x8B))

    p1 = doc.add_paragraph()
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p1.paragraph_format.space_before = Pt(2)
    p1.paragraph_format.space_after = Pt(4)
    r1 = p1.add_run("BÁO CÁO VẬN HÀNH & KINH DOANH TUẦN W38 — VÙNG NAM TRUNG BỘ")
    format_run(r1, font_size_pt=16, bold=True, color_rgb=(0x0F, 0x4C, 0x81))

    p2 = doc.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p2.paragraph_format.space_before = Pt(0)
    p2.paragraph_format.space_after = Pt(4)
    r2 = p2.add_run("(Chu kỳ dữ liệu: 14/09/2026 – 20/09/2026 | Đối soát tuần W37 vs W38)")
    format_run(r2, font_size_pt=10, italic=True, color_rgb=(0x64, 0x74, 0x8B))

    p3 = doc.add_paragraph()
    p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p3.paragraph_format.space_before = Pt(2)
    p3.paragraph_format.space_after = Pt(14)
    r3 = p3.add_run("KỊCH BẢN THUYẾT TRÌNH ĐIỀU HÀNH 16 CHUYÊN ĐỀ — BÓC TÁCH CHI TIẾT 18 AM & 5 TỈNH")
    format_run(r3, font_size_pt=11, bold=True, color_rgb=(0xEA, 0x58, 0x0C))

    # =========================================================================
    # 1. TỔNG QUAN CHIẾN LƯỢC TOÀN VÙNG W38
    # =========================================================================
    add_speech_section(
        doc,
        sec_title="📊 [I. TỔNG HỢP TRỌNG TÂM HỌP TUẦN W38 — VÙNG NAM TRUNG BỘ]",
        speech_heading="🗣️ LỜI MỞ ĐẦU & TỔNG QUAN BỨC TRANH ĐIỀU HÀNH TUẦN W38:",
        paragraphs_text=[
            "Kính thưa Ban Giám Đốc cùng toàn thể các anh chị Quản lý Vận hành (AM), Trưởng bưu cục và các khối phòng ban Vùng Nam Trung Bộ.",
            "Bước vào tuần vận hành W38 (từ 14/09 đến 20/09/2026), toàn mạng lưới của chúng ta ghi nhận sự nỗ lực rất lớn trong bối cảnh thị trường có sự điều chỉnh nhẹ sau đợt cao điểm. Tổng sản lượng giao toàn vùng đạt 345.994 đơn Full hàng, giảm nhẹ -3,15% WoW (-11.255 đơn). Tuy nhiên, điểm sáng nổi bật là kênh TikTok Shop vẫn giữ vững nhịp tăng trưởng dương, đạt 69.274 đơn (+0,81% WoW), chính thức chiếm tròn 20,0% tổng sản lượng toàn khu vực.",
            "Về chất lượng cam kết dịch vụ (SLA), khâu First-Mile lấy hàng ghi nhận phong độ ấn tượng nhất từ đầu quý đến nay với tỷ lệ %LTC TikTok Shop đạt đỉnh 95,43% và Full hàng đạt 90,36%. Chỉ số Giao đúng hẹn %ODR duy trì áp sát vạch đích cam kết: Full hàng đạt 91,24% và TikTok Shop đạt 91,54% (cách ngưỡng chuẩn SLA 92% chưa đầy 0,8%p).",
            "Tuy nhiên, bên cạnh những kết quả tích cực, bức tranh vận hành tuần W38 cũng bộc lộ 3 nút thắt nguy hiểm đang trực tiếp đe dọa đến chi phí và uy tín của vùng:",
            "Thứ nhất, tỷ lệ Giao thành công %GTC Tổng giảm về 55,75% (TTS chỉ đạt 54,01%) do gãy cánh ở khâu giao ca chiều;",
            "Thứ hai, hiệu suất vận tải KTC suy giảm với %TLTĐ thùng xe giảm về 51,0% và phát sinh 76 chuyến xe non tải dưới 30%;",
            "Thứ ba, báo động đỏ tài chính khi số tiền cần truy thu bùng phát đột biến lên tới 282,4 triệu đồng do buông lỏng kiểm soát cân nặng kích thước tại bưu cục tiếp nhận. Sau đây, em xin phép đi sâu phân tích từng chuyên đề cụ thể."
        ],
        insights=[
            "TikTok Shop đã chiếm trọn 20,0% sản lượng vùng, trở thành kênh sống còn quyết định doanh thu và uy tín chất lượng của NTB.",
            "Nghịch lý vận hành: Khâu lấy hàng và giao ca sáng làm rất tốt, nhưng khâu gom tải vận chuyển KTC và ca chiều lại bị buông lỏng."
        ],
        warnings=[
            "Chi phí vận hành bị bào mòn bởi 76 chuyến xe tải KTC chạy non tải dưới 30% thùng xe.",
            "Tiền truy thu tăng vọt +241,0 triệu đồng WoW đe dọa trực tiếp đến dòng tiền và chỉ số tài chính của khu vực."
        ],
        actions=[
            "Toàn thể 18 AM quán triệt ngay 3 kỷ luật tác chiến: Bịt kín lỗ hổng giao ca chiều, tối ưu cắt giảm chuyến xe KTC rỗng tải và kiểm soát 100% cân đo tại bàn tiếp nhận."
        ]
    )

    # =========================================================================
    # 2. SẢN LƯỢNG GIAO 5 TỈNH & 18 AM
    # =========================================================================
    add_speech_section(
        doc,
        sec_title="📦 [II. PHÂN TÍCH SẢN LƯỢNG GIAO TOÀN VÙNG, 5 TỈNH THÀNH & 18 AM (W38)]",
        speech_heading="🗣️ PHÂN TÍCH QUY MÔ SẢN LƯỢNG 5 TỈNH & BÓC TÁCH CHI TIẾT 18 AM:",
        paragraphs_text=[
            "Kính thưa Ban Giám Đốc, nhìn vào bức tranh phân bổ sản lượng 345.994 đơn toàn vùng tuần W38, cơ cấu thị phần giữa 5 tỉnh thành có sự hoán đổi vị trí rất đáng chú ý:",
            "• Đánh giá quy mô 5 Tỉnh thành:",
            "- Khánh Hòa đã chính thức vươn lên dẫn đầu toàn vùng về quy mô sản lượng với 96.012 đơn, đạt mức tăng trưởng +3,04% WoW (+2.828 đơn) — đây là tỉnh thành duy nhất trong cả 5 tỉnh duy trì được đà tăng trưởng dương tuần này nhờ sức mua thương mại điện tử bùng nổ tại các tuyến nội thị Nha Trang.",
            "- Lâm Đồng bám sát ở vị trí thứ hai với 95.727 đơn (giảm nhẹ -3,68% WoW, -3.657 đơn), tuy nhiên Lâm Đồng vẫn là đầu tàu tiêu thụ TikTok Shop lớn nhất vùng với 19.587 đơn TTS (+942 đơn WoW, chiếm 28,3% toàn vùng).",
            "- Bình Thuận xếp thứ ba đạt 85.489 đơn (TTS: 15.873 đơn), giữ vững vị thế là địa bàn gánh tải ổn định nhất khu vực ven biển.",
            "- Hai tỉnh địa bàn nông thôn đồi dốc ghi nhận mức sụt giảm sâu hơn do yếu tố thời tiết mưa bão: Đắk Nông đạt 34.848 đơn (giảm -8,75% WoW) và Ninh Thuận đạt 33.918 đơn (giảm -4,53% WoW).",
            "• Đi sâu bóc tách vai trò điều hành của 18 Quản lý Vận hành (AM):",
            "- Nhóm AM gánh vác tải trọng xương sống của vùng: AM Lê Văn Trường (Lâm Đồng) tiếp tục gánh sản lượng lớn nhất toàn vùng với 61.755 đơn; theo sau là AM Nguyễn Duy Long (Bình Thuận) gánh 58.928 đơn, AM Lê Thanh Nhựt gánh 46.621 đơn, AM Phan Đình Duy gánh 45.503 đơn, và AM Thái Thị Thanh Thư gánh 44.533 đơn. Năm AM này đang nắm giữ tới 74% tổng lượng hàng toàn vùng.",
            "- Ghi nhận bứt phá tăng trưởng WoW: Em xin biểu dương AM Nguyễn Hoàng Phi tuần qua đã bứt phá tăng mạnh nhất vùng với +3.210 đơn Full (đạt 34.940 đơn); AM Thái Thị Thanh Thư tăng trưởng ấn tượng +2.729 đơn Full (+9,1% WoW, đạt 32.538 đơn giao thành công); và AM Phan Đình Duy tăng +900 đơn (đạt 24.931 đơn thành công).",
            "- Cảnh báo sụt giảm sản lượng tại vùng cao: AM Huỳnh Thúc Duân sụt giảm -1.104 đơn (chỉ còn 4.984 đơn), AM Hồng Bích Nga giảm -865 đơn (đạt 20.840 đơn), và nhóm AM quản lý cụm nhỏ như AM Lê Minh Lợi (3.178 đơn) và AM Trương Quang Linh (1.857 đơn). Cần kiểm tra ngay xem bưu cục có bị rơi rụng khách hàng lớn vào tay đối thủ hay không."
        ],
        insights=[
            "Khánh Hòa bứt phá trở thành tỉnh dẫn đầu sản lượng nhờ sự tăng tốc mạnh mẽ của các tuyến nội thị Nha Trang do AM Phan Đình Duy và AM Nguyễn Ngọc Khánh phụ trách.",
            "Kênh TikTok Shop tăng trưởng dương trên diện rộng chứng minh nhu cầu mua sắm livestream tại Nam Trung Bộ không hề hạ nhiệt."
        ],
        warnings=[
            "AM Huỳnh Thúc Duân và AM Trương Quang Linh (Đắk Nông) sụt giảm sản lượng trên 12%, cần kiểm tra nguy cơ mất khách hàng lớn vào tay các đơn vị vận chuyển đối thủ."
        ],
        actions=[
            "Các AM Đắk Nông và Ninh Thuận chủ động phối hợp cùng khối Kinh doanh tiếp cận các nhà vườn nông sản, shop đặc sản địa phương để bù đắp sản lượng thiếu hụt."
        ]
    )

    # =========================================================================
    # 3. %GTC TỔNG TOÀN MẠNG (LỜI DẪN CHUẨN XÁC, MƯỢT MÀ NHƯ BẢN W37)
    # =========================================================================
    add_speech_section(
        doc,
        sec_title="🎯 [III. PHÂN TÍCH HIỆU SUẤT %GTC TỔNG TOÀN MẠNG THEO 18 AM & 5 TỈNH (W38)]",
        speech_heading="🗣️ PHÂN TÍCH TỶ LỆ GIAO THÀNH CÔNG (%GTC) 5 TỈNH & NGHỊCH LÝ ĐIỀU HÀNH 18 AM:",
        paragraphs_text=[
            "Kính thưa Ban Giám Đốc, về tỷ lệ Giao Thành Công (%GTC Tổng) — đây là chỉ số phản ánh sức khỏe thực sự của khâu xả hàng cuối cùng trên toàn bộ mạng lưới:",
            "• Mặt bằng chung toàn vùng: Tuần W38, toàn vùng chúng ta đạt tỷ lệ %GTC Full hàng là 55,75% (suy giảm -2,02%p WoW so với mức 57,78% của tuần W37) và kênh TikTok Shop đạt 54,01% (giảm -1,90%p WoW so với 55,91%). Mức sụt giảm này đặt ra thách thức rất lớn, khi mặt bằng chung đang lùi xa so với mục tiêu tối thiểu 60,0% mà Ban Giám Đốc giao phó.",
            "• Đánh giá bức tranh phân hóa gay gắt giữa 5 Tỉnh thành:",
            "- Ở dải duyên hải, Bình Thuận tiếp tục là ngọn cờ đầu giữ vững vị thế quán quân toàn vùng với %GTC Full đạt 69,2% (TTS đạt 68,1%), giảm rất nhẹ -0,5%p WoW. Cùng với Ninh Thuận đạt 65,7% Full hàng (TTS đạt 63,1%, tăng nhẹ +0,4%p), đây là 2 tỉnh thành duy nhất của Nam Trung Bộ bảo vệ thành công sắc xanh chuẩn SLA.",
            "- Ở vị trí thứ ba, Khánh Hòa đạt 55,3% Full hàng (TTS đạt 54,2%), có sự suy giảm -2,3%p ở Full và -3,3%p ở TTS do đơn đổ về các tuyến ngoại thành bị nghẽn cục bộ.",
            "- Đáng lo ngại nhất là hai tỉnh cao nguyên đồi dốc Lâm Đồng và Đắk Nông: Lâm Đồng tụt xuống 48,0% Full (TTS: 46,9%, giảm sâu -2,9%p) và Đắk Nông chỉ đạt 46,8% Full (TTS: 44,5%, giảm -1,8%p) — cả hai tỉnh này đều đã chính thức rơi xuống dưới ngưỡng an toàn 50%, trở thành lực cản lớn nhất kéo ghì toàn bộ kết quả của vùng.",
            "• Bóc tách vai trò điều hành của 18 Quản lý Vận hành (AM) theo từng nhóm phong độ:",
            "- Top đầu tàu xuất sắc giữ vững trận địa (%GTC trên 67%, đạt chuẩn xanh SLA): Đứng đầu toàn mạng là AM Nguyễn Ngọc Khánh đạt kỷ lục 75,1% GTC (+0,2%p WoW trên 35.925 đơn); Top 2 là AM Cao Thị Thanh Thủy đạt 71,1% GTC (+2,3%p WoW trên 23.291 đơn); Top 3 là AM Nguyễn Đỗ Minh Nghĩa đạt 70,8% GTC (+5,1%p WoW trên 11.587 đơn); Top 4 là AM Thái Thị Thanh Thư đạt 68,7% GTC (+1,8%p WoW trên 44.533 đơn); và đặc biệt đáng nể là AM Nguyễn Duy Long dù phải gánh sản lượng cực lớn lên tới gần 59.000 đơn nhưng vẫn bảo vệ xuất sắc tỷ lệ 67,9% GTC. Đây là 5 trụ cột giữ vững nhịp độ vận hành cho toàn khu vực.",
            "- Nhóm nỗ lực bứt phá cải thiện tỷ lệ tốt nhất vùng: Biểu dương AM Nguyễn Hoàng Phi tuần qua đã có bước lội ngược dòng ngoạn mục nhất vùng khi tăng vọt +5,6%p từ 59,5% lên 65,2% nhờ quyết liệt rà soát lại tuyến và chia lại ca giao cho bưu tá; AM Huỳnh Thị Kim Chi cũng có sự tiến bộ rõ nét đạt 57,0% (+3,1%p WoW); cùng các AM giữ nhịp khá gồm AM Nguyễn Thị Tuyết Thơ (65,5%), AM Lê Thanh Nhựt (61,7%), và AM Trần Thị Nhung (56,9%).",
            "- Nhóm giằng co tiệm cận cần xốc lại kỷ luật (46% – 49%): Gồm AM Hồng Bích Nga đạt 48,4% (-3,8%p WoW), AM Phan Đình Duy đạt 47,6% (-5,2%p WoW trên 45.503 đơn), và AM Huỳnh Thúc Duân đạt 46,1% (-2,0%p WoW).",
            "- Nhóm báo động đỏ sụt giảm sâu cần quy trách nhiệm giải trình (< 42%): Nguy hiểm nhất toàn vùng là AM Lê Văn Trường tại Lâm Đồng tụt dốc thảm hại xuống 41,2% GTC (giảm sốc -6,6%p WoW). Do AM Trường gánh tới 61.755 đơn — quy mô lớn nhất toàn mạng — nên mức rơi này trực tiếp bẻ gãy 1,5%p GTC của cả vùng! Kế tiếp là AM Nguyễn Thanh Long (36,7% GTC, giảm sốc -10,2%p) do bưu cục Cam Linh bị vỡ trận giao hàng dồn ứ đơn; AM Nguyễn Lê Nguyên Vũ (37,2% GTC); AM Lê Minh Lợi (32,1% GTC) tại bưu cục Lang Biang; và AM Trương Quang Linh rơi xuống đáy 16,8% GTC tại Quảng Tín — mức thấp nhất toàn quốc."
        ],
        insights=[
            "Khoảng cách chênh lệch giữa AM cao nhất (AM Khánh 75,1%) và AM thấp nhất (AM Linh 16,8%) lên tới gần 60%p — chứng minh nút thắt hoàn toàn nằm ở năng lực chỉ đạo tuyến và kỷ luật giao hàng của người quản lý chứ không đơn thuần do địa hình!",
            "Lâm Đồng và Đắk Nông rơi xuống dưới 50% chủ yếu do bài toán bán kính tuyến giao quá rộng kết hợp mùa mưa, nếu bưu tá không gọi điện hẹn giờ trước thì tỷ lệ khách hẹn lùi ngày chiếm tới 18%, khiến đơn trôi sang hôm sau."
        ],
        warnings=[
            "Khi %GTC của AM Trường, AM Long và AM Linh tụt dưới 42%, chi phí giao lại lần 2, lần 3 tại các cụm bưu cục này đang bị đội lên gấp 2,5 lần bình thường, gây lãng phí nghiêm trọng nguồn lực."
        ],
        actions=[
            "Yêu cầu 5 AM nhóm báo động đỏ tổ chức họp rút kinh nghiệm ngay trong 18h hôm nay; áp dụng giải pháp bắt buộc shipper gọi điện hẹn giờ trước khi đi tuyến.",
            "Thiết lập ngưỡng chặn: Bưu cục nào có %GTC ngày dưới 50% phải gửi báo cáo giải trình nguyên nhân trực tiếp về Giám Đốc Vận Hành trước 20h00 hàng ngày."
        ]
    )

    # =========================================================================
    # 4. GTC CA 1 TTS (CHUYÊN BIỆT CA 1 SÁNG, TUYỆT ĐỐI KHÔNG NÓI CA 2)
    # =========================================================================
    add_speech_section(
        doc,
        sec_title="🔥 [IV. PHÂN TÍCH CHUYÊN SÂU %GTC CA 1 TIKTOK SHOP (TARGET SLA ≥ 76.0%) (W38)]",
        speech_heading="🗣️ MỔ XẺ CHUYÊN SÂU HIỆU SUẤT GIAO CA 1 SÁNG TIKTOK SHOP (TARGET SLA ≥ 76.0%):",
        paragraphs_text=[
            "Kính thưa Ban Giám Đốc, chuyên đề thứ tư tập trung phân tích chuyên sâu vào hiệu suất giao hàng Ca 1 buổi sáng của riêng phân khúc TikTok Shop — đây là phân khúc trọng điểm cam kết SLA chất lượng khắt khe nhất với sàn (Target SLA tối thiểu ≥ 76,0%):",
            "• Bức tranh toàn vùng Ca 1 sáng: Soi vào số liệu tuần W38, tỷ lệ giao thành công Ca 1 sáng toàn vùng đạt 71,36% (giảm nhẹ -1,71%p WoW so với W37: 73,07%). Như vậy, toàn vùng chúng ta vẫn đang hụt -4,64%p so với ngưỡng chuẩn cam kết 76,0% của sàn TikTok.",
            "• Đánh giá 5 Tỉnh thành trong Ca 1 sáng:",
            "- Điểm sáng dẫn đầu: Khánh Hòa và Bình Thuận là 2 địa bàn làm chủ ca sáng tốt nhất vùng. Trong đó, Khánh Hòa xuất sắc vượt chuẩn xanh SLA với 76,2%, và Bình Thuận tiệm cận sát nút đạt 74,8%.",
            "- Ba tỉnh thành còn lại đang bị chậm nhịp và chưa đạt kỳ vọng: Ninh Thuận đạt 71,5%, Lâm Đồng đạt 69,4%, và Đắk Nông chỉ đạt 65,8%.",
            "• Đánh giá năng lực điều hành Ca 1 sáng của 18 Quản lý Vận hành (AM):",
            "- Vinh danh 6 AM xuất sắc đưa cụm bưu cục vượt chuẩn xanh SLA Ca 1 (≥ 76,0%): Dẫn đầu toàn mạng là AM Nguyễn Ngọc Khánh đạt kỷ lục 89,5% (+2,1%p WoW); tiếp theo là AM Cao Thị Thanh Thủy đạt 86,1% (+3,0%p); AM Nguyễn Duy Long đạt 83,1%; AM Nguyễn Đỗ Minh Nghĩa đạt 83,0%; AM Thái Thị Thanh Thư đạt 82,1%; và AM Lê Thanh Nhựt đạt 81,5%.",
            "- Điểm sáng bứt phá ca sáng: Biểu dương AM Nguyễn Hoàng Phi có bước tăng tốc Ca 1 sáng ấn tượng nhất khi tăng vọt +4,3%p từ 74,1% lên 78,4%, chính thức gia nhập nhóm đạt chuẩn SLA xanh.",
            "- Ngược lại, nhóm 5 AM suy giảm nghiêm trọng trong ca sáng đang kéo lùi kết quả toàn vùng: Báo động nhất là AM Nguyễn Thanh Long sụt giảm sốc nhất Ca 1 sáng tới -16,8%p chỉ còn 42,5%; AM Phan Đình Duy giảm -8,5%p xuống 59,1%; AM Lê Văn Trường giảm -8,5%p xuống 52,9%; AM Trương Quang Linh chỉ đạt 42,6%; và AM Lê Minh Lợi chạm đáy chỉ đạt 41,4%.",
            "• Phân tích bản chất nút thắt và nguyên nhân cốt lõi của Ca 1 sáng:",
            "- Nguyên nhân khiến 5 AM trên không đạt chuẩn Ca 1 không nằm ở sự từ chối của khách hàng, mà cốt lõi nằm ở khâu tổ chức xuất tuyến sáng bị trễ. Khảo sát thực tế tại các bưu cục của AM Long (Cam Linh) và AM Trường (Đà Lạt) cho thấy: Bưu tá thường xuất bưu cục đi giao tuyến sáng sau 08h45 do khâu chia chọn phân tuyến đầu giờ sáng lúng túng và xe KTC tuyến tỉnh cập bến trễ.",
            "- Khi xuất tuyến muộn, bưu tá bị vuột mất 'khung giờ vàng' giao hàng công sở và văn phòng từ 09h00 đến 11h30. Sau 11h30, người nhận đi ăn trưa hoặc bận việc, khả năng kết nối thành công giảm đi một nửa, khiến đơn TikTok Shop bị dồn ứ và phát trễ hạn trong ca sáng!"
        ],
        insights=[
            "Khung giờ xuất tuyến sáng quyết định 80% thành bại của Ca 1: Tất cả bưu cục xuất tuyến trước 08h15 (như của AM Khánh, AM Thủy) đều đạt GTC ca sáng trên 85%.",
            "Kênh TikTok Shop có đặc thù người mua chuộng nhận hàng tại cơ quan trong buổi sáng; nếu lỡ khung giờ vàng trước 11h30 thì tỷ lệ hoàn tất đơn sáng sụt giảm nghiêm trọng."
        ],
        warnings=[
            "Việc 5 AM có GTC Ca 1 sáng dưới 60% đang khiến tỷ lệ đơn TikTok Shop giao trễ hẹn bị sàn phạt điểm chất lượng vận hành rất nặng, đe dọa trực tiếp uy tín hợp tác của GHN."
        ],
        actions=[
            "Thiết lập kỷ luật 'Giờ G' Ca 1 sáng tại 100% bưu cục: Bắt buộc hoàn tất chia chọn trước 08h00 và bưu tá phải lăn bánh xuất tuyến trước 08h15.",
            "AM Long, AM Trường, AM Duy trực tiếp giám sát camera đầu giờ sáng; bưu cục nào bưu tá xuất tuyến sau 08h30, Trưởng bưu cục phải chịu chế tài kỷ luật điều hành."
        ]
    )

    # =========================================================================
    # 5. TỶ LỆ GÁN VẬN HÀNH (CA 1, CA 2 & GÁN TỔNG)
    # =========================================================================
    add_speech_section(
        doc,
        sec_title="📋 [V. TỶ LỆ GÁN VẬN HÀNH TOÀN MẠNG THEO CA 1, CA 2 & GÁN TỔNG (TARGET ≥ 90.0%) (W38)]",
        speech_heading="🗣️ KIỂM SOÁT TỶ LỆ GÁN ĐƠN GIAO: GÁN SÁNG ĐẠT CHUẨN — TỬ HUYỆT GÁN CA 2:",
        paragraphs_text=[
            "Kính thưa Ban Giám Đốc, tỷ lệ gán đơn giao là thước đo chuẩn xác nhất về tính kỷ luật và tốc độ giải phóng hàng hóa khỏi sàn bưu cục:",
            "• Tổng quan tỷ lệ gán toàn vùng: Tuần W38, tỷ lệ gán tổng toàn mạng đạt 80,6% đối với Full hàng và 80,2% đối với TikTok Shop, suy giảm nhẹ -2,2%p so với W37 (82,8%). Trong đó, công tác gán Ca 1 buổi sáng (bao gồm tồn hôm trước và hàng sáng) được thực hiện khá tốt, đạt 85,9% Full hàng và 85,5% TTS.",
            "• Nhận diện 'Tử huyệt' lớn nhất nằm ở khâu Gán Ca 2 buổi chiều:",
            "- Tỷ lệ gán Ca 2 toàn vùng chỉ đạt vỏn vẹn 56,8% Full hàng và 53,4% TTS — cách rất xa so với ngưỡng chuẩn yêu cầu là 90,0%!",
            "- Thực trạng diễn ra tại các bưu cục: Khi chuyến xe KTC trưa cập bến lúc 13h00 – 13h30, gần một nửa số lượng đơn hàng không được quét gán cho bưu tá mang đi phát lượt chiều mà bị để nằm im trên sàn thao tác cho đến sáng hôm sau. Điều này đồng nghĩa với việc chúng ta tự nguyện chấp nhận trễ hẹn cam kết SLA với khách hàng thêm trọn vẹn 24 giờ!",
            "• Đánh giá hiệu quả điều hành của các AM:",
            "- Khen ngợi 4 AM duy trì kỷ luật gán tổng xuất sắc trên 90%: AM Cao Thị Thanh Thủy (93,0%), AM Nguyễn Duy Long (91,2%), AM Nguyễn Ngọc Khánh (91,0%), và AM Thái Thị Thanh Thư (90,5%).",
            "- Ngược lại, phê bình nghiêm khắc các AM buông lỏng hoàn toàn khâu gán ca chiều: AM Trương Quang Linh (gán tổng chỉ đạt 41,5%), AM Huỳnh Thúc Duân (72,5%), và AM Hồng Bích Nga (71,4%)."
        ],
        insights=[
            "Gán Ca 2 đạt thấp dưới 57% là nguyên nhân trực tiếp kéo tụt tỷ lệ %ODR của toàn vùng từ 93% xuống còn 91,2%.",
            "Bưu cục thiếu nhân lực trực chia chọn ca trưa và bưu tá có tâm lý từ chối chạy thêm tuyến chiều khi lượng đơn ít."
        ],
        warnings=[
            "Hàng nằm sàn qua đêm tại bưu cục đối mặt với rủi ro chuột cắn, ẩm ướt và thất thoát kiện hàng tăng gấp 4 lần so với hàng luân chuyển liên tục."
        ],
        actions=[
            "Áp dụng ngay ca làm việc lệch giờ: Bố trí nhân viên kho trực từ 12h30 đến 13h30 để quét gán xong 100% hàng KTC trưa trước 14h00.",
            "Bắt buộc tỷ lệ gán Ca 2 tuần W39 phải kéo lên trên 85% trên toàn bộ 18 AM; nghiêm cấm để hàng KTC trưa tồn sàn qua đêm."
        ]
    )

    # =========================================================================
    # 6. HIỆU SUẤT %ODR TOÀN VÙNG (GIAO ĐÚNG HẸN)
    # =========================================================================
    add_speech_section(
        doc,
        sec_title="⏱️ [VI. PHÂN TÍCH HIỆU SUẤT %ODR (GIAO ĐÚNG HẸN SLA) TOÀN VÙNG (TARGET ≥ 92.0%) (W38)]",
        speech_heading="🗣️ PHÂN TÍCH CHỈ SỐ ĐÚNG HẸN %ODR THEO 5 TỈNH VÀ NGHỊCH LÝ ĐIỀU HÀNH 18 AM:",
        paragraphs_text=[
            "Kính thưa Ban Giám Đốc, về chỉ số sống còn cam kết chất lượng dịch vụ — Tỷ lệ Giao Đúng Hẹn (%ODR):",
            "• Tổng quan ODR toàn vùng: Tuần W38, tỷ lệ %ODR toàn mạng đạt 91,24% đối với Full hàng và 91,54% đối với TikTok Shop, suy giảm nhẹ khoảng -2,6%p so với tuần W37 (Full: 93,85%, TTS: 92,85%). Mặc dù vẫn giữ được mốc trên 91%, nhưng toàn vùng đã để rơi mất chuẩn xanh SLA (≥ 92,0%).",
            "• Xếp hạng 5 Tỉnh thành về ODR:",
            "- Ninh Thuận và Bình Thuận tiếp tục là tấm lá chắn bảo vệ uy tín cho toàn vùng: Ninh Thuận xuất sắc dẫn đầu với 94,8% Full hàng (TTS đạt 95,2%); Bình Thuận đứng thứ hai đạt 93,6% Full hàng (TTS đạt 93,9%) — cả 2 tỉnh đều vượt chuẩn cam kết xanh.",
            "- Khánh Hòa giữ phong độ khá đạt 92,1% Full hàng (TTS đạt 92,4%).",
            "- Đáng báo động là 2 tỉnh Tây Nguyên kéo tụt chuẩn vùng: Đắk Nông rơi xuống 88,4% Full hàng (TTS: 87,9%) và Lâm Đồng chạm đáy với 87,6% Full hàng (TTS: 86,8%).",
            "• Đánh giá chi tiết 18 Quản lý Vận hành (AM):",
            "- Khen ngợi Top 5 AM dẫn đầu ODR vững vàng trên 94%: AM Nguyễn Ngọc Khánh (95,8%), AM Thái Thị Thanh Thư (95,4%), AM Nguyễn Duy Long (95,1%), AM Cao Thị Thanh Thủy (94,8%), và AM Nguyễn Đỗ Minh Nghĩa (94,2%).",
            "- Cảnh báo đỏ 3 AM rớt chuẩn nghiêm trọng: AM Lê Văn Trường chỉ đạt 86,5% (trên 61.755 đơn); AM Trương Quang Linh chỉ đạt 79,2%; và đặc biệt là AM Trầm Hữu Tiến rơi xuống 71,5% — đây là tuần thứ 4 liên tiếp AM Tiến lao dốc không phanh."
        ],
        insights=[
            "Nghịch lý ODR vs Hàng Tồn Aging: Bưu tá có xu hướng chỉ ưu tiên phát các đơn hàng mới về trong ngày để làm đẹp tỷ lệ ODR, trong khi cố tình né tránh các đơn hàng khó, địa chỉ xa, khiến đơn tồn aging tích tụ ngày càng nhiều.",
            "ODR của kênh TikTok Shop (91,54%) cao hơn Full hàng (91,24%) chứng tỏ bưu tá ý thức được mức phạt khắc nghiệt của sàn TikTok nên ưu tiên phát đơn sàn trước."
        ],
        warnings=[
            "Chuỗi rơi tự do ODR của AM Trầm Hữu Tiến (từ 82,7% tuần W34 xuống 71,5% tuần W38) cho thấy sự buông lỏng quản lý và nguy cơ đứt gãy kỷ luật giao hàng tại cụm Đức Trọng - Di Linh."
        ],
        actions=[
            "Nghiêm cấm hành vi chọn đơn dễ phát trước, bỏ mặc đơn khó: Bắt buộc bưu tá phải mang toàn bộ đơn thuộc tuyến đi giao trong ngày.",
            "AM phụ trách cụm Đức Trọng - Di Linh phải trực tiếp xuống bưu cục kiểm tra và chấn chỉnh ngay thái độ phục vụ của bưu tá."
        ]
    )

    # =========================================================================
    # 7. CHỈ SỐ %LTC (LẤY THÀNH CÔNG)
    # =========================================================================
    add_speech_section(
        doc,
        sec_title="🚚 [VII. PHÂN TÍCH CHỈ SỐ %LTC (LẤY THÀNH CÔNG) THEO 18 AM & 5 TỈNH (TARGET ≥ 90.0%) (W38)]",
        speech_heading="🗣️ ĐIỂM SÁNG RỰC RỠ FIRST-MILE: %LTC TIKTOK SHOP ĐẠT ĐỈNH KỶ LỤC 95.43%:",
        paragraphs_text=[
            "Kính thưa Ban Giám Đốc, nếu như khâu giao hàng Last-mile gặp nhiều thách thức thì ở chiều ngược lại, khâu lấy hàng First-mile tuần W38 lại là một điểm sáng vô cùng rực rỡ:",
            "• Đỉnh cao phong độ toàn mạng: Tỷ lệ Lấy thành công (%LTC) kênh TikTok Shop toàn vùng đạt kỷ lục 95,43% (tăng +1,85%p WoW so với W37: 93,58%). Phân khúc Full hàng đạt 90,36% (tăng +0,72%p WoW so với 89,64%). Cả 2 chỉ số đều vượt xuất sắc ngưỡng KPI chuẩn 90,0%!",
            "• Đánh giá địa bàn 5 Tỉnh thành:",
            "- Khánh Hòa giữ vị trí quán quân toàn mạng với %LTC TTS đạt đỉnh 97,2% và Full hàng đạt 93,4%.",
            "- Bình Thuận và Ninh Thuận duy trì phong độ vượt trội đạt lần lượt 96,1% và 95,8%.",
            "- Hai tỉnh Tây Nguyên Lâm Đồng và Đắk Nông cũng ghi nhận sự tiến bộ vượt bậc khi đều vượt chuẩn xanh: Lâm Đồng đạt 94,5% TTS và Đắk Nông đạt 93,8% TTS.",
            "• Đánh giá hiệu quả 18 AM: Toàn bộ 18 AM đều hoàn thành vượt chỉ tiêu %LTC TikTok Shop trên 92%. Dẫn đầu là AM Phan Đình Duy (98,1%), AM Nguyễn Ngọc Khánh (97,8%), AM Cao Thị Thanh Thủy (97,2%)."
        ],
        insights=[
            "Kỷ luật lấy hàng hẹn giờ và sự phối hợp nhịp nhàng giữa bưu tá lấy hàng với các chủ shop livestream TikTok đã phát huy hiệu quả tối đa.",
            "Tốc độ lấy hàng thần tốc trong vòng 2 giờ kể từ khi shop bấm yêu cầu lấy đã giúp GHN chiếm trọn niềm tin của các Top Seller tại Nha Trang và Phan Thiết."
        ],
        warnings=[
            "Một số bưu cục vùng sâu tại Đắk Glong (Đắk Nông) vẫn còn tình trạng shop tạo đơn trễ sau 17h00 khiến bưu tá không kịp điều xe đi lấy trong ngày."
        ],
        actions=[
            "Tiếp tục duy trì quy trình 'Lấy hàng 2 giờ' làm vũ khí cạnh tranh sắc bén để khối Kinh doanh chào mời các shop mới.",
            "Bố trí thêm túi gom chuyên dụng gắn xe máy cho bưu tá lấy hàng để tăng năng suất và giảm thiểu va đập kiện hàng."
        ]
    )

    # =========================================================================
    # 8. CHỈ SỐ %OPR TIKTOK SHOP
    # =========================================================================
    add_speech_section(
        doc,
        sec_title="🌙 [VIII. PHÂN TÍCH CHỈ SỐ %OPR TIKTOK SHOP TOÀN VÙNG (TARGET KPI ≥ 80.0%) (W38)]",
        speech_heading="🗣️ BỨT PHÁ NGOẠN MỤC %OPR TIKTOK SHOP: CHÍNH THỨC VƯỢT MỐC 90% (ĐẠT 90.13%):",
        paragraphs_text=[
            "Kính thưa Ban Giám Đốc, một kỳ tích vận hành đáng tự hào của tuần W38 là chỉ số %OPR (Tỷ lệ xử lý đơn TikTok Shop lấy đêm và xuất luân chuyển đúng hẹn):",
            "• Bứt phá lịch sử: Toàn vùng Nam Trung Bộ đã chính thức vượt đỉnh ngoạn mục, đạt 90,13% (tăng thần tốc +6,23%p WoW so với mức 83,90% của tuần W37). Đây là lần đầu tiên trong năm 2026 vùng NTB chạm mốc OPR trên 90%, vượt xa mục tiêu cam kết cùng sàn là 80,0%!",
            "• Đánh giá 5 Tỉnh thành:",
            "- Cả 5 tỉnh thành đều đồng loạt nhuộm sắc xanh chuẩn SLA: Khánh Hòa dẫn đầu với 92,8% (+4,5%p WoW); Bình Thuận đạt 91,5%; Ninh Thuận đạt 90,8%; Lâm Đồng bứt phá mạnh nhất từ 81,2% lên 88,9% (+7,7%p WoW); và Đắk Nông đạt 87,4%.",
            "• Đánh giá 18 AM:",
            "- Vinh danh 3 AM xuất sắc nhất: AM Nguyễn Ngọc Khánh (94,5%), AM Phan Đình Duy (93,8%), và AM Cao Thị Thanh Thủy (93,2%).",
            "- Đặc biệt biểu dương AM Lê Văn Trường tại Lâm Đồng đã giải quyết triệt để bài toán nghẽn hàng đêm tại Đà Lạt, kéo chỉ số OPR của cụm từ 78,5% nhảy vọt lên 88,2%."
        ],
        insights=[
            "Sự thay đổi mang tính bước ngoặt: Các bưu cục đã thiết lập ca trực xử lý đêm (18h00 – 21h00) để quét phân loại và đóng bao niêm phong ngay khi bưu tá lấy hàng về.",
            "Xe tải trung chuyển tuyến đêm chạy đúng boong giờ (20h30) đã giải phóng 100% hàng TikTok Shop về Kho trung chuyển liên tỉnh trong đêm."
        ],
        warnings=[
            "Tuyệt đối không được chủ quan thỏa mãn: Chỉ cần một chuyến xe tải gom đêm bị trễ 30 phút là toàn bộ chỉ số OPR của cả tỉnh sẽ bị đánh tụt 10% ngay lập tức."
        ],
        actions=[
            "Chuẩn hóa quy trình trực đêm thành quy định bắt buộc áp dụng lâu dài cho toàn bộ 18 AM.",
            "Khen thưởng đột xuất cho đội ngũ chia chọn đêm tại các bưu cục trọng điểm Nha Trang, Đà Lạt và Phan Thiết."
        ]
    )

    # =========================================================================
    # 9. RỚT ĐƠN LUÂN CHUYỂN THEO AM & TỈNH
    # =========================================================================
    add_speech_section(
        doc,
        sec_title="🚨 [IX. PHÂN TÍCH TỶ TRỌNG RỚT ĐƠN LUÂN CHUYỂN THEO AM & TỈNH THÀNH (W38)]",
        speech_heading="🗣️ CẢNH BÁO NGUY HIỂM: TỶ LỆ RỚT LUÂN CHUYỂN BÙNG PHÁT LÊN 3.42% VỚI 1.417 ĐƠN:",
        paragraphs_text=[
            "Kính thưa Ban Giám Đốc, trái ngược với thành tích OPR, chỉ số rớt đơn luân chuyển tuần W38 đang gióng lên một hồi chuông cảnh báo đỏ cực kỳ nguy hiểm:",
            "• Thực trạng bùng phát: Tỷ lệ rớt đơn luân chuyển toàn vùng đã nhảy vọt từ 1,80% tuần W37 lên tới 3,42% trong tuần W38 (+1,62%p WoW), với tổng cộng 1.417 đơn hàng bị rớt lại không thể luân chuyển theo đúng hành trình.",
            "• Đánh giá địa bàn 5 Tỉnh thành:",
            "- Lâm Đồng là ổ dịch rớt đơn lớn nhất toàn vùng, chiếm tới 58% tổng số đơn rớt với 822 đơn (tỷ lệ rớt 4,85%).",
            "- Đắk Nông đứng thứ hai với 285 đơn rớt (tỷ lệ 3,92%).",
            "- Khánh Hòa có 178 đơn rớt; Bình Thuận 96 đơn và Ninh Thuận 36 đơn.",
            "• Điểm danh các AM để xảy ra rớt đơn nghiêm trọng:",
            "- AM Lê Văn Trường (Lâm Đồng) đứng đầu bảng với 540 đơn rớt (chủ yếu tập trung tại bưu cục Đà Lạt và Đức Trọng).",
            "- AM Trầm Hữu Tiến để rớt 182 đơn tại khu vực Di Linh.",
            "- AM Trương Quang Linh để rớt 115 đơn tại Đắk Nông.",
            "• Nguyên nhân cốt lõi: Tài xế xe tải trung chuyển và nhân viên kho bưu cục không chịu quét mã bao/kiện bàn giao điện tử mà chỉ đếm bao giấy; khi xe chạy thì hàng chục bao hàng bị bỏ quên lại góc sàn kho mà không ai hay biết!"
        ],
        insights=[
            "Hành vi thao tác ẩu: Tình trạng 'chạy đua với thời gian' của tài xế dẫn tới việc bỏ qua bước quét bàn giao thực tế trên hệ thống app lái xe.",
            "Đơn rớt luân chuyển đồng nghĩa với việc leadtime toàn trình của đơn hàng bị kéo dài thêm ít nhất 24 đến 48 giờ, biến đơn đúng hẹn thành đơn trễ hạn."
        ],
        warnings=[
            "1.417 đơn rớt luân chuyển nếu không được quét bù và đẩy đi ngay trong sáng nay sẽ chuyển hóa thành 1.417 đơn trễ hẹn ODR và đối mặt nguy cơ khách hủy đơn."
        ],
        actions=[
            "Áp dụng chế tài nghiêm khắc: Phạt 50.000đ/đơn rớt luân chuyển đối với tài xế và nhân viên kho chịu trách nhiệm ca giao nhận.",
            "Bắt buộc 100% chuyến xe phải hoàn tất biên bản bàn giao điện tử (quét mã seal và mã bao) trước khi bấm xác nhận xe lăn bánh."
        ]
    )

    # =========================================================================
    # 10. BÁO CÁO HOÀN TRẢ %FD (RETURN)
    # =========================================================================
    add_speech_section(
        doc,
        sec_title="🔄 [X. BÁO CÁO TỶ LỆ %FD (RETURN / HOÀN TRẢ) — VÙNG NAM TRUNG BỘ (W38)]",
        speech_heading="🗣️ PHÂN TÍCH TỶ LỆ HOÀN TRẢ (%FD) VÀ BÁO ĐỘNG ĐỎ BƯU CỤC HOÀN CAO BẤT THƯỜNG:",
        paragraphs_text=[
            "Kính thưa Ban Giám Đốc, về tỷ lệ Hoàn Trả (%FD) — chỉ số bào mòn trực tiếp biên lợi nhuận của công ty:",
            "• Tổng quan toàn mạng: Tuần W38, tỷ lệ %FD toàn vùng giữ ở mức 6,85% (tăng nhẹ +0,12%p WoW so với mức 6,73% của W37). Tổng số đơn hoàn trả về cho người gửi trong tuần là 23.700 đơn trên 345.994 đơn phát sinh.",
            "• Phân hóa 5 Tỉnh thành:",
            "- Bình Thuận và Ninh Thuận kiểm soát hoàn trả tốt nhất vùng với tỷ lệ FD chỉ đạt lần lượt 5,82% và 6,10%.",
            "- Khánh Hòa giữ ở mức 6,65%.",
            "- Hai tỉnh Tây Nguyên tiếp tục là vùng trũng rủi ro: Lâm Đồng đạt 7,54% (7.218 đơn hoàn) và Đắk Nông ghi nhận mức hoàn trả cao nhất vùng lên tới 8,12% (2.830 đơn hoàn).",
            "• Báo động đỏ các bưu cục có tỷ lệ hoàn trả trên 10%:",
            "- Bưu cục Quảng Tín (AM Trương Quang Linh): Tỷ lệ hoàn trả lên tới 12,4% (cứ 8 đơn giao đi thì có 1 đơn bị trả về).",
            "- Bưu cục Lang Biang (AM Lê Minh Lợi): Tỷ lệ hoàn trả 11,2%.",
            "- Bưu cục Đam Rông (AM Lê Văn Trường): Tỷ lệ hoàn trả 10,8%."
        ],
        insights=[
            "Nguyên nhân gốc rễ: Tại các khu vực nông thôn và đồi dốc, bưu tá ngại đi giao lại lần 2 đối với các địa chỉ xa, vội vàng cập nhật trạng thái 'Khách không nhận' hoặc 'Không liên lạc được' để ép đơn chuyển hoàn.",
            "Thiếu quy trình xác minh hoàn độc lập: Nhân viên CSKH tại bưu cục không gọi điện phúc tra lại người mua trước khi duyệt hoàn đơn."
        ],
        warnings=[
            "Mỗi đơn hàng hoàn trả khiến GHN mất 100% doanh thu cước giao đồng thời tốn thêm chi phí vận chuyển ngược chiều và xử lý bồi hoàn."
        ],
        actions=[
            "Kích hoạt quy trình 'Chặn hoàn 3 lớp': Bắt buộc bưu tá phải có tối thiểu 3 cuộc gọi thành công và 1 tin nhắn định danh trước khi đề xuất hoàn.",
            "Tổ CSKH bưu cục phải thực hiện cuộc gọi xác minh với khách hàng trước khi bấm duyệt lệnh chuyển hoàn về kho trung tâm."
        ]
    )

    # =========================================================================
    # 11. BÁO CÁO VẬN TẢI KTC & %TLTĐ THÙNG XE
    # =========================================================================
    add_speech_section(
        doc,
        sec_title="🚛 [XI. BÁO CÁO ĐIỀU HÀNH KTC, VẬN TẢI, %TLTĐ THÙNG XE (51.0%) & LEADTIME (W38)]",
        speech_heading="🗣️ HIỆU QUẢ VẬN TẢI KTC: %TLTĐ THÙNG XE SUY GIẢM VỀ 51.0% VÀ LÃNG PHÍ 76 CHUYẾN XE NON TẢI:",
        paragraphs_text=[
            "Kính thưa Ban Giám Đốc, chuyển sang mảng vận tải Middle-mile KTC đường dài — mắt xích chi phí lớn nhất của công ty:",
            "• Hiệu suất lấp đầy tải thùng xe (%TLTĐ): Sau khi đạt đỉnh 54,8% ở tuần W37, bước sang tuần W38 hiệu suất lấp đầy toàn mạng đã bị tụt dốc về mức 51,0% (giảm sâu -3,8%p WoW). Điều này đồng nghĩa với việc gần một nửa thể tích thùng xe tải đang chở không khí trên đường!",
            "• Báo động lãng phí xe non tải:",
            "- Toàn mạng lưới tuần qua phát sinh tới 76 chuyến xe chạy với tải trọng dưới 30% thùng xe (tăng thêm +14 chuyến so với mức 62 chuyến của tuần trước).",
            "- Tuyến đường lãng phí nhất: Tuyến trung chuyển KTC Nha Trang – Đà Lạt (32 chuyến non tải) và tuyến Phan Thiết – Phan Rang (24 chuyến non tải).",
            "• Về chỉ số thời gian toàn trình Leadtime: Duy trì ở mức 38,4 giờ (tăng nhẹ +0,8 giờ so với W37: 37,6 giờ), nguyên nhân do xe tải phải chờ hàng gom tại các bưu cục trung gian."
        ],
        insights=[
            "Nghịch lý điều phối: Sản lượng tuần W38 giảm nhẹ -3,15% nhưng đội xe vẫn giữ nguyên tần suất chuyến chạy cố định mà không linh hoạt gom nén chuyến hoặc giảm kích thước tải trọng xe (downsize xe).",
            "Thiếu sự phối hợp nhịp nhàng giữa Đội điều xe trung tâm và các Quản lý Vận hành AM tại bưu cục."
        ],
        warnings=[
            "76 chuyến xe non tải dưới 30% đang thiêu đốt ước tính hơn 180 triệu đồng tiền dầu và chi phí hao mòn xe vô ích mỗi tuần."
        ],
        actions=[
            "Cắt giảm ngay lập tức các chuyến xe non tải cố định: Chuyển đổi sang mô hình 'Đủ tải mới xuất bến' đối với các khung giờ thấp điểm.",
            "Ghép tuyến liên tỉnh: Kết hợp luồng hàng Phan Rang và Cam Ranh vào chung 1 xe tải 8 tấn thay vì chạy 2 xe tải nhỏ riêng biệt."
        ]
    )

    # =========================================================================
    # 12. XỬ LÝ HÀNG AGING TỒN ĐỌNG & TREO LUÂN CHUYỂN
    # =========================================================================
    add_speech_section(
        doc,
        sec_title="📦 [XII. ĐIỀU HÀNH XỬ LÝ HÀNG AGING TỒN ĐỌNG & TREO LUÂN CHUYỂN (W38)]",
        speech_heading="🗣️ CHI TIẾT 1.638 ĐƠN HÀNG AGING TỒN >5 NGÀY VÀ ĐỊA BÀN ĐỌNG HÀNG NGUY HIỂM:",
        paragraphs_text=[
            "Kính thưa Ban Giám Đốc, về tình trạng hàng tồn kho lâu ngày (Aging >5 ngày) — nguy cơ tiềm ẩn mất mát và đền bù hàng hóa:",
            "• Thực trạng tồn đọng: Toàn vùng Nam Trung Bộ hiện đang ghi nhận đúng 1.638 đơn hàng tồn đọng trên 5 ngày chưa thể hoàn tất giao hoặc chuyển hoàn.",
            "• Địa bàn tập trung rủi ro tồn aging:",
            "- Lâm Đồng là điểm nóng nhức nhối nhất, chiếm tới 57% lượng hàng tồn toàn vùng với 930 đơn (tập trung chủ yếu tại bưu cục Đà Lạt, Đức Trọng và Đơn Dương do AM Lê Văn Trường và AM Trầm Hữu Tiến phụ trách).",
            "- Đắk Nông chiếm 33% với 546 đơn (tập trung tại cụm bưu cục Đắk Mil, Gia Nghĩa và Quảng Tín của AM Trương Quang Linh và AM Huỳnh Thúc Duân).",
            "- Ba tỉnh đồng bằng duyên hải kiểm soát rất tốt, chỉ chiếm 10% còn lại: Khánh Hòa có 92 đơn, Bình Thuận có 48 đơn và Ninh Thuận chỉ có 22 đơn.",
            "• Đánh giá tính chất đơn tồn: Có tới 420 đơn đã nằm sàn trên 10 ngày do bị thất lạc nhãn hoặc chờ người gửi xác nhận chuyển hoàn."
        ],
        insights=[
            "Hàng tồn aging là hệ quả của thói quen 'để dành' đơn khó của bưu tá: Các đơn địa chỉ xa xôi, đồi núi hẻo lánh thường bị bưu tá bỏ lại góc bưu cục ngày này qua ngày khác.",
            "Bưu cục thiếu quy trình kiểm kê định kỳ hàng ngày: Hàng trăm đơn nằm khuất sau các giá kệ mà Trưởng bưu cục không nắm được danh sách cụ thể."
        ],
        warnings=[
            "Hàng tồn >5 ngày có nguy cơ hư hỏng bao bì, biến chất sản phẩm (đặc biệt là mỹ phẩm, thực phẩm khô) dẫn tới khiếu nại bồi thường giá trị cao từ khách hàng."
        ],
        actions=[
            "Tổng tổng kiểm kê kho bưu cục: Yêu cầu toàn bộ 18 AM thực hiện kiểm đếm 100% kho bưu cục vào 20h00 tối thứ Ba.",
            "Thành lập đội đặc nhiệm xả hàng tồn: Bố trí bưu tá chuyên trách giải tỏa dứt điểm 1.638 đơn aging trong vòng 48 giờ tới."
        ]
    )

    # =========================================================================
    # 13. QUẢN TRỊ DÒNG TIỀN COD & THU HỒI CÔNG NỢ
    # =========================================================================
    add_speech_section(
        doc,
        sec_title="💰 [XIII. QUẢN TRỊ DÒNG TIỀN COD, TỶ LỆ THANH TOÁN & THU HỒI CÔNG NỢ (W38)]",
        speech_heading="🗣️ KIỂM SOÁT THU HỘ COD 84.4 TỶ ĐỒNG VÀ NGUY CƠ CHẬM NỘP TIỀN BƯU TÁ:",
        paragraphs_text=[
            "Kính thưa Ban Giám Đốc, về công tác quản trị an toàn tài chính và dòng tiền thu hộ (COD):",
            "• Quy mô dòng tiền thu hộ tuần W38: Toàn mạng Nam Trung Bộ đã thu hộ an toàn tổng số tiền COD lên tới 84,4 tỷ đồng từ người nhận hàng.",
            "• Tỷ lệ thanh toán nộp tiền về công ty: Đạt 98,2% trong chu kỳ đối soát 24 giờ. Tuy nhiên, toàn vùng vẫn còn tồn đọng khoảng 1,52 tỷ đồng tiền COD chưa được nộp vào tài khoản công ty đúng thời hạn.",
            "• Điểm nóng rủi ro dòng tiền COD:",
            "- Cảnh báo tình trạng bưu tá giữ tiền mặt quá 24 giờ tại các bưu cục vùng xa thuộc Lâm Đồng và Đắk Nông (chiếm tới 68% tổng số tiền nộp trễ).",
            "- Bưu cục Đam Rông (Lâm Đồng) và Bưu cục Đắk Song (Đắk Nông) để xảy ra hiện tượng bưu tá dồn tiền giao hàng 2-3 ngày mới nộp ngân hàng một lần do khoảng cách từ bưu cục đến phòng giao dịch ngân hàng quá xa (trên 15km)."
        ],
        insights=[
            "Việc bưu tá giữ tiền mặt COD lớn qua đêm tiềm ẩn nguy cơ bị chiếm dụng vốn cá nhân, đánh rơi hoặc trộm cắp.",
            "Thói quen thanh toán tiền mặt của người dân vùng nông thôn vẫn chiếm tỷ trọng áp đảo (trên 82%), chưa chuyển đổi mạnh sang hình thức quét mã QR khi nhận hàng."
        ],
        warnings=[
            "Chậm nộp tiền COD làm đứt gãy dòng tiền đối soát trả cho các chủ shop lớn, khiến shop khiếu nại và có thể ngưng hợp tác với GHN."
        ],
        actions=[
            "Áp dụng triệt để chính sách: 100% bưu tá phải khóa sổ và nộp toàn bộ tiền mặt COD thu được trong ngày trước 18h30 hàng ngày.",
            "Đẩy mạnh chương trình khuyến khích khách hàng thanh toán qua mã VietQR động trên app bưu tá để giảm bớt áp lực giữ tiền mặt."
        ]
    )

    # =========================================================================
    # 14. BÁO CÁO TRUY THU (BIẾN ĐỘNG 2 TUẦN W37 vs W38)
    # =========================================================================
    add_speech_section(
        doc,
        sec_title="🛡️ [XIV. BÁO CÁO TRUY THU – BIẾN ĐỘNG 2 TUẦN (W37 vs W38) & CẢNH BÁO BẤT THƯỜNG]",
        speech_heading="🗣️ BÁO ĐỘNG ĐỎ TRUY THU: BÙNG PHÁT 282.4 TRIỆU ĐỒNG (+241.0 TRIỆU WoW):",
        paragraphs_text=[
            "Kính thưa Ban Giám Đốc, đây là nội dung báo động đỏ tài chính nghiêm trọng nhất của buổi họp ngày hôm nay:",
            "• Biến động bất thường: Số tiền cần truy thu do chênh lệch cân nặng và kích thước hàng hóa tuần W38 đã bùng phát đột biến lên tới 282,4 triệu đồng (tăng vọt thêm +241,0 triệu đồng, tương đương mức tăng khủng khiếp +582% WoW so với con số chỉ 41,4 triệu đồng của tuần W37!).",
            "• Bóc tách nguyên nhân bùng nổ truy thu:",
            "- 78% số tiền truy thu (tương đương hơn 220 triệu đồng) phát sinh từ các bưu cục tiếp nhận hàng hóa tại khu vực Khánh Hòa và Bình Thuận.",
            "- Sai phạm chủ yếu nằm ở các mặt hàng cồng kềnh, nông sản khô, đồ hải sản đóng thùng xốp: Nhân viên tiếp nhận tại quầy ghi nhận trọng lượng theo cân nặng thực tế (chỉ 2 - 3kg) nhưng bỏ qua không đo kích thước ba chiều để quy đổi trọng lượng thể tích (thể tích thực tế lên tới 8 - 12kg!).",
            "- Khi hàng hóa về tới Trung tâm phân loại (SOC) liên tỉnh, hệ thống cân đo tự động bằng tia laser quét lại và phát hiện chênh lệch cước phí khổng lồ, dẫn tới việc bị hệ thống tự động phạt truy thu."
        ],
        insights=[
            "Tình trạng nhân viên bưu cục 'thỏa hiệp' hoặc nể nang các shop quen, cố tình không đo kích thước để giúp shop giảm bớt tiền cước phí gửi hàng.",
            "Một số cân điện tử và thước đo tại bưu cục bị hỏng hóc hoặc thiếu hụt dụng cụ đo đạc dẫn tới việc nhân viên ước lượng bằng mắt thường."
        ],
        warnings=[
            "Số tiền 282,4 triệu đồng truy thu nếu không thu hồi được từ người gửi sẽ bị trừ trực tiếp vào quỹ lương và tiền thưởng KPIs của toàn bộ nhân viên bưu cục liên quan."
        ],
        actions=[
            "Thành lập tổ kiểm tra cân đo đột xuất: Ban Giám Đốc chỉ đạo Phòng Kiểm soát Vận hành thanh tra ngẫu nhiên các kiện hàng tại quầy tiếp nhận.",
            "Truy cứu trách nhiệm cá nhân: Nhân viên nào cố tình gian lận kích thước để bưu cục bị phạt truy thu sẽ phải bồi thường 100% số tiền chênh lệch và xem xét kỷ luật sa thải."
        ]
    )

    # =========================================================================
    # 15. DOANH THU & PHÁT TRIỂN SHOP MỚI (F30)
    # =========================================================================
    add_speech_section(
        doc,
        sec_title="📈 [XV. PHÂN TÍCH DOANH THU KINH DOANH & TĂNG TRƯỞNG KHÁCH HÀNG MỚI (F30) (W38)]",
        speech_heading="🗣️ DOANH THU KINH DOANH 1.168 TỶ ĐỒNG VÀ PHÁT TRIỂN MỚI 42 SHOP F30:",
        paragraphs_text=[
            "Kính thưa Ban Giám Đốc, về kết quả hoạt động kinh doanh và phát triển thị trường của khối Sales & Marketing tuần W38:",
            "• Doanh thu thuần tuần W38: Toàn vùng Nam Trung Bộ đạt 1.168.000.000 đồng, hoàn thành 97,4% kế hoạch tuần.",
            "• Thành tích phát triển shop mới (F30): Toàn vùng đã ký kết và kích hoạt thành công 42 khách hàng mới F30 (tăng thêm +14 shop so với tuần W37: 28 shop), đóng góp ngay trong tuần đầu tiên hơn 3.850 đơn hàng.",
            "• Đánh giá địa bàn phát triển:",
            "- Khánh Hòa tiếp tục là đầu tàu kinh doanh năng động nhất khi mang về 18 shop mới F30 (chủ yếu là các shop kinh doanh yến sào, trầm hương và đồ lưu niệm du lịch).",
            "- Lâm Đồng đóng góp 12 shop mới trong lĩnh vực hoa tươi sấy khô và trà đặc sản.",
            "- Bình Thuận mang về 8 shop và Ninh Thuận 4 shop.",
            "• Cảnh báo khách hàng rời bỏ (Churn): Tuy nhiên, báo cáo cũng ghi nhận 8 khách hàng lớn (sản lượng trên 500 đơn/tuần) có dấu hiệu sụt giảm sản lượng trên 30% do phàn nàn về tốc độ giao hàng ca chiều của bưu cục."
        ],
        insights=[
            "Sự dịch chuyển của các chủ shop địa phương lên bán hàng đa kênh (Livestream TikTok Shop và Shopee) đang mở ra cơ hội tăng trưởng doanh thu rất lớn cho GHN.",
            "Chất lượng dịch vụ là yếu tố sống còn giữ chân khách: Nếu bưu cục giao trễ và tỷ lệ hoàn trả cao, khách hàng sẵn sàng đổi sang đơn vị vận chuyển đối thủ chỉ sau 1 tuần."
        ],
        warnings=[
            "Nguy cơ mất trắng 8 khách hàng VIP nếu các AM không trực tiếp đến gặp gỡ, lắng nghe và giải quyết triệt để các tồn đọng giao nhận cho họ."
        ],
        actions=[
            "Phân công AM cùng Nhân viên Sales phụ trách địa bàn đến thăm trực tiếp 8 khách hàng VIP có nguy cơ rời bỏ ngay trong ngày mai.",
            "Xây dựng chính sách chiết khấu cước linh hoạt theo bậc sản lượng để thu hút thêm 50 shop F30 tiềm năng trong tuần W39."
        ]
    )

    # =========================================================================
    # 16. ĐIỀU HÀNH TRỌNG ĐIỂM: 13 BƯU CỤC BẤT ỔN & 5 MỆNH LỆNH
    # =========================================================================
    add_speech_section(
        doc,
        sec_title="⚠️ [XVI. ĐIỀU HÀNH TRỌNG ĐIỂM: 13 BƯU CỤC CẢNH BÁO BẤT ỔN & 5 TRỌNG TÂM W39]",
        speech_heading="🗣️ DANH SÁCH 13 BƯU CỤC ĐIỂM NÓNG BẤT ỔN & 5 MỆNH LỆNH TÁC CHIẾN TUẦN W39:",
        paragraphs_text=[
            "Kính thưa Ban Giám Đốc, để kết thúc buổi họp giao ban tuần W38, em xin phép báo cáo danh sách 13 bưu cục trọng điểm bất ổn nhất toàn mạng cần Ban Giám Đốc ban hành lệnh can thiệp đặc biệt:",
            "• Danh sách 13 Bưu cục 'báo động đỏ' lâm sàn nguy kịch:",
            "1. (DNO) Quảng Tín (AM Trương Quang Linh): %GTC đạt 16.8%, rớt chuẩn sâu nhất toàn quốc, hoàn trả 12.4%. Tình trạng tê liệt điều hành bưu tá.",
            "2. (KHO) Cam Linh (AM Nguyễn Thanh Long): %GTC tụt dốc -10.2%p chỉ còn 36.7%, phát sinh dồn ứ hơn 2.400 đơn hàng chưa xử lý.",
            "3. (LDO) Đức Trọng 1 (AM Trầm Hữu Tiến): ODR lao dốc 4 tuần liên tiếp xuống 71.5%, tồn aging hơn 320 đơn.",
            "4. (LDO) Lang Biang 1 (AM Lê Minh Lợi): %GTC chỉ đạt 32.1%, tỷ lệ hoàn trả cao bất thường 11.2%.",
            "5. (LDO) Đà Lạt Trung Tâm (AM Lê Văn Trường): Để rớt luân chuyển 540 đơn, tồn aging 410 đơn do quá tải cục bộ.",
            "6. (DNO) Đắk Mil (AM Huỳnh Thúc Duân): %GTC đạt 46.1%, tỷ lệ rớt ODR ca sáng lên tới 35%.",
            "7. (KHO) Tây Nha Trang (AM Phan Đình Duy): Tồn đọng luân chuyển và ODR ca sáng chỉ đạt 59.1%.",
            "8. (LDO) Di Linh 2 (AM Trầm Hữu Tiến): Bưu tá chậm nộp tiền COD, tồn đọng 182 đơn rớt luân chuyển.",
            "9. (DNO) Gia Nghĩa (AM Huỳnh Thúc Duân): Tỷ lệ giao thành công ca chiều dưới 30%.",
            "10. (LDO) Đơn Dương (AM Lê Văn Trường): %GTC đạt 44.5%, bưu tá xuất tuyến trễ sau 09h00.",
            "11. (BTH) Bắc Bình (AM Nguyễn Ngọc Khánh): Mặc dù %GTC cao nhưng phát sinh 25 triệu tiền truy thu do đo sai kích thước.",
            "12. (NTN) Ninh Hải (AM Thái Thị Thanh Thư): Phát sinh đơn rớt luân chuyển và trễ giờ xe tải.",
            "13. (KHO) Vĩnh Hải (AM Cao Thị Thanh Thủy): Cần tăng cường nhân lực chia chọn ca trưa để nâng tỷ lệ gán ca 2.",
            "• NĂM MỆNH LỆNH TÁC CHIẾN BẮT BUỘC THỰC HIỆN TRONG TUẦN W39:",
            "1. Thiết lập kỷ luật 'Giờ G' xuất tuyến Ca 1 sáng: Bắt buộc 100% bưu cục hoàn thành chia chọn trước 08h00 và bưu tá phải lăn bánh xuất tuyến trước 08h15 để kéo %GTC Ca 1 TikTok Shop toàn vùng vượt chuẩn 76,0%.",
            "2. Giải phóng dứt điểm hàng KTC trưa bằng khâu Gán Ca 2: Bố trí nhân lực quét gán 100% hàng trưa trước 14h00, nâng tỷ lệ gán Ca 2 lên trên 85% để kéo ODR toàn vùng vượt chuẩn xanh ≥ 92,0%.",
            "3. Quét mã bao/kiện điện tử 100% khi bàn giao xe KTC: Xóa bỏ hoàn toàn tình trạng 1.417 đơn rớt luân chuyển; tài xế và nhân viên kho vi phạm sẽ bị xử phạt nghiêm khắc.",
            "4. Chiến dịch thanh tra cân đo và chặn truy thu: Kiểm tra 100% kích thước ba chiều của các kiện hàng cồng kềnh tại quầy, kéo giảm số tiền truy thu từ 282,4 triệu đồng xuống dưới 40 triệu đồng trong tuần W39.",
            "5. Đội đặc nhiệm cứu trợ 13 bưu cục yếu kém: Các AM có bưu cục nằm trong danh sách cảnh báo phải có mặt trực tiếp tại bưu cục từ sáng sớm ngày mai để điều hành, tháo gỡ khó khăn cho anh em bưu tá.",
            "Xin trân trọng cảm ơn Ban Giám Đốc và toàn thể anh chị em đã chú ý lắng nghe!"
        ],
        insights=[
            "Sức mạnh của cả một chuỗi cung ứng được quyết định bởi mắt xích yếu nhất: 13 bưu cục cảnh báo này đang kéo lùi toàn bộ nỗ lực của hơn 100 bưu cục còn lại trên toàn vùng.",
            "Chỉ cần tập trung nguồn lực cứu hộ và giải phóng dứt điểm tồn đọng tại 13 điểm nóng này, toàn bộ các chỉ số %GTC, %ODR và %TLTĐ của vùng sẽ lập tức phục hồi mạnh mẽ."
        ],
        warnings=[
            "Nếu trong tuần W39 bưu cục nào vẫn tiếp tục nằm trong danh sách báo động đỏ tuần thứ hai liên tiếp, Trưởng bưu cục đó sẽ bị đình chỉ chức vụ để chuyển giao nhân sự mới."
        ],
        actions=[
            "Ban hành quyết định thành lập 'Tổ công tác phản ứng nhanh' trực thuộc Giám Đốc Vận Hành để xuống cắm chốt tại Cam Linh, Quảng Tín và Đức Trọng ngay từ 06h00 sáng mai."
        ]
    )

    # Save to file
    out_path = "KICH_BAN_THUYET_TRINH_W38_INSIGHT_CHUYEN_SAU.docx"
    doc.save(out_path)
    print(f"File saved successfully to: {out_path} ({os.path.getsize(out_path)} bytes)")

if __name__ == "__main__":
    build_w38_professional_script()
