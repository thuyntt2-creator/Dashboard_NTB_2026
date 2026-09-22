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
            "- Top AM gánh vác sản lượng giao lớn nhất vùng (xương sống mạng lưới): Quán quân sản lượng toàn vùng tuần này là AM Nguyễn Duy Long (Bình Thuận) dẫn đầu với 43.018 đơn (chiếm 12,4% toàn vùng); bám sát phía sau là AM Thái Thị Thanh Thư (32.538 đơn), AM Lê Thanh Nhựt (30.600 đơn), AM Lê Văn Trường (28.919 đơn), và AM Nguyễn Ngọc Khánh (28.325 đơn). Nhóm 5 AM đầu tàu này đang gánh vác tới 163.382 đơn, chiếm gần một nửa (47,2%) tổng sản lượng giao của toàn vùng.",
            "- Điểm sáng tăng trưởng sản lượng WoW: Toàn vùng ghi nhận duy nhất 5 AM có sản lượng tăng trưởng dương tuần này. Trong đó, dẫn đầu bứt phá là AM Thái Thị Thanh Thư tăng mạnh nhất toàn mạng +2.729 đơn Full (+9,16% WoW, đạt 32.538 đơn); tiếp theo là AM Phan Đình Duy tăng +900 đơn (+3,75% WoW, đạt 24.931 đơn); AM Nguyễn Lê Nguyên Vũ tăng +491 đơn (đạt 13.500 đơn); AM Nguyễn Thanh Long tăng +163 đơn (đạt 14.127 đơn); và AM Nguyễn Thị Tuyết Thơ tăng nhẹ +11 đơn (đạt 9.670 đơn).",
            "- Nhóm các AM suy giảm sản lượng theo nhịp thị trường: Tuần W38 ghi nhận 13/18 AM có sản lượng giảm nhẹ sau đợt cao điểm mua sắm đầu tháng. Trong đó, lượng giảm tập trung chủ yếu ở 3 AM gánh tải lớn nhất vùng là AM Nguyễn Duy Long (-2.575 đơn), AM Lê Văn Trường (-2.299 đơn), và AM Nguyễn Ngọc Khánh (-2.092 đơn) — riêng 3 AM này đã chiếm hơn 60% tổng lượng đơn sụt giảm của cả vùng (-11.255 đơn)."
        ],
        insights=[
            "Khánh Hòa bứt phá trở thành tỉnh dẫn đầu sản lượng nhờ sự tăng tốc mạnh mẽ của các tuyến nội thị Nha Trang do AM Phan Đình Duy và AM Nguyễn Ngọc Khánh phụ trách.",
            "Kênh TikTok Shop tăng trưởng dương trên diện rộng chứng minh nhu cầu mua sắm livestream tại Nam Trung Bộ không hề hạ nhiệt."
        ],
        warnings=[
            "Sức mua thị trường sau đợt cao điểm có dấu hiệu chững lại ở 13/18 cụm bưu cục, trong đó 3 AM đầu tàu (Long, Trường, Khánh) giảm gần 7.000 đơn cần theo dõi sát nhu cầu gửi hàng của các shop lớn."
        ],
        actions=[
            "Khối Vận hành phối hợp chặt chẽ cùng khối Kinh doanh đẩy mạnh tiếp cận các khách hàng doanh nghiệp, nhà vườn và shop online để kích cầu sản lượng cho tuần W39."
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
            "- Top đầu tàu xuất sắc giữ vững trận địa (%GTC trên 67%, đạt chuẩn xanh SLA): Đứng đầu toàn mạng là AM Nguyễn Ngọc Khánh đạt kỷ lục 75,1% GTC (+0,2%p WoW trên 35.925 đơn gán giao); Top 2 là AM Cao Thị Thanh Thủy đạt 71,1% GTC (+2,3%p WoW trên 23.291 đơn); Top 3 là AM Nguyễn Đỗ Minh Nghĩa đạt 70,8% GTC (+5,1%p WoW trên 11.587 đơn); Top 4 là AM Thái Thị Thanh Thư đạt 68,7% GTC (+1,8%p WoW trên 44.533 đơn); và đặc biệt đáng nể là AM Nguyễn Duy Long dù phải gánh lượng đơn gán giao cực lớn lên tới 58.928 đơn nhưng vẫn bảo vệ xuất sắc tỷ lệ 67,9% GTC. Đây là 5 trụ cột giữ vững nhịp độ vận hành cho toàn khu vực.",
            "- Nhóm nỗ lực bứt phá cải thiện tỷ lệ tốt nhất vùng: Biểu dương AM Nguyễn Hoàng Phi tuần qua đã có bước lội ngược dòng ngoạn mục nhất vùng khi tăng vọt +5,6%p từ 59,5% lên 65,2% (trên 34.940 đơn gán giao) nhờ quyết liệt rà soát lại tuyến và chia lại ca giao cho bưu tá; AM Huỳnh Thị Kim Chi cũng có sự tiến bộ rõ nét đạt 57,0% (+3,1%p WoW trên 21.270 đơn); cùng các AM giữ nhịp khá gồm AM Nguyễn Thị Tuyết Thơ (65,5%), AM Lê Thanh Nhựt (61,7%), và AM Trần Thị Nhung (56,9%).",
            "- Nhóm giằng co tiệm cận cần xốc lại kỷ luật (46% – 49%): Gồm AM Hồng Bích Nga đạt 48,4% (-3,8%p WoW trên 38.777 đơn), AM Phan Đình Duy đạt 47,6% (-5,2%p WoW trên 45.503 đơn), và AM Huỳnh Thúc Duân đạt 46,1% (-2,0%p WoW trên 9.432 đơn).",
            "- Nhóm báo động đỏ sụt giảm sâu cần quy trách nhiệm giải trình (< 42%): Nguy hiểm nhất toàn vùng là AM Lê Văn Trường tại Lâm Đồng tụt dốc thảm hại xuống 41,2% GTC (giảm sốc -6,6%p WoW). Do AM Trường có lượng đơn gán giao đánh giá GTC lớn nhất toàn mạng lên tới 61.755 đơn, nên mức rơi này trực tiếp bẻ gãy 1,5%p GTC của cả vùng! Kế tiếp là AM Nguyễn Thanh Long (36,7% GTC, giảm sốc -10,2%p) do bưu cục Cam Linh bị vỡ trận giao hàng dồn ứ đơn; AM Nguyễn Lê Nguyên Vũ (37,2% GTC); AM Lê Minh Lợi (32,1% GTC) tại bưu cục Lang Biang; và AM Trương Quang Linh rơi xuống đáy 16,8% GTC tại Quảng Tín — mức thấp nhất toàn quốc."
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
            "• Đánh giá chi tiết kỷ luật gán giao của 18 Quản lý Vận hành (AM):",
            "- Nhóm AM làm chủ ca chiều và giữ vững kỷ luật gán tổng (chuẩn xanh ≥ 90%): Toàn vùng có 7 AM đạt chuẩn xanh Gán Tổng, dẫn đầu là AM Thái Thị Thanh Thư (gán tổng 96,0%, gán Ca 2 đạt 88,5%); AM Nguyễn Ngọc Khánh (gán tổng 93,6%, Ca 2 đạt 85,3%); AM Cao Thị Thanh Thủy (gán tổng 93,0%, Ca 2 đạt 81,2%); AM Nguyễn Hoàng Phi (gán tổng 92,7%, Ca 2 đạt 80,4%); cùng AM Nguyễn Thị Tuyết Thơ (92,4%), AM Nguyễn Đỗ Minh Nghĩa (92,1%) và AM Nguyễn Duy Long (91,4%). Đặc biệt, AM Lê Minh Lợi đạt tỷ lệ gán Ca 2 tuyệt đối 100,0%.",
            "- Nhóm báo động đỏ buông lỏng hoàn toàn gán Ca 2 buổi chiều (dưới 35%): Tê liệt nặng nề nhất là AM Trương Quang Linh khi tỷ lệ gán Ca 2 chạm đáy chỉ đạt vỏn vẹn 5,5% (gán tổng thấp nhất vùng 55,5%); tiếp theo là AM Huỳnh Thúc Duân có tỷ lệ gán Ca 2 chỉ đạt 14,2% (dù gán sáng đạt 81,7%); AM Nguyễn Đỗ Minh Nghĩa gán Ca 2 chỉ đạt 22,7% (dù sáng đạt 98,6%); AM Nguyễn Lê Nguyên Vũ gán Ca 2 chỉ 22,8% (gán tổng 65,3%); AM Trần Thị Nhung gán Ca 2 chỉ đạt 31,0%; AM Hồng Bích Nga đạt 34,1% (gán tổng 71,4%); và AM Lê Văn Trường đạt 35,5% (gán tổng 61,8%). Tình trạng 'đầu voi đuôi chuột' — sáng đi tuyến rầm rộ nhưng chiều bỏ mặc hàng KTC trưa — chính là tử huyệt bẻ gãy chỉ số SLA của các AM này!"
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
        speech_heading="🗣️ ĐÁNH GIÁ CHUYÊN SÂU %OPR TỔNG TIKTOK SHOP: TOÀN VÙNG ĐẠT 83.0% (VƯỢT CHUẨN), 9 AM ĐẠT XANH & 6 AM CHƯA ĐẠT:",
        paragraphs_text=[
            "Kính thưa Ban Giám Đốc, về chỉ số %OPR Tổng TikTok Shop — tỷ lệ xử lý và xuất luân chuyển đúng cam kết toàn trình (Target KPI toàn mạng ≥ 80,0%):",
            "• Tín hiệu khởi sắc toàn vùng W38: Tổng sản lượng xử lý OPR đạt 6.534 đơn. Tỷ lệ %OPR Tổng toàn vùng đạt 83,0%, bứt phá tăng mạnh +4,8%p WoW so với tuần W37 (78,2%), chính thức đưa Nam Trung Bộ vượt qua ngưỡng chuẩn xanh 80,0%.",
            "• Phân hóa theo địa bàn 5 Tỉnh thành:",
            "- 3 Tỉnh xuất sắc đạt chuẩn KPI (≥ 80%): Dẫn đầu là Ninh Thuận đạt 90,6% (+1,1%p WoW, 1.270 đơn); Bình Thuận đạt 89,0% (+3,6%p WoW, 1.876 đơn); và Khánh Hòa bứt phá ấn tượng đạt 87,3% (+9,4%p WoW, 1.691 đơn).",
            "- 2 Tỉnh chưa đạt chuẩn: Lâm Đồng đạt 70,3% (1.436 đơn, dù tăng +4,0%p WoW nhưng vẫn dưới vạch đích gần 10%p); đặc biệt Đắk Nông báo động đỏ khi chỉ đạt vỏn vẹn 45,2% (261 đơn), thấp nhất toàn mạng.",
            "• Bóc tách chi tiết hiệu quả điều hành theo 15 Quản lý Vận hành (AM):",
            "- Nhóm 9 AM XUẤT SẮC ĐẠT CHUẨN XANH (≥ 80,0%):",
            "  1. AM Thái Thị Thanh Thư: Quán quân OPR toàn vùng đạt 93,0% (+5,1%p WoW, 917 đơn).",
            "  2. AM Cao Thị Thanh Thủy: Đạt 91,4% (+0,8%p WoW, 800 đơn).",
            "  3. AM Nguyễn Duy Long: Đạt 90,6% (+2,7%p WoW, gánh sản lượng OPR lớn nhất vùng với 1.392 đơn).",
            "  4. AM Nguyễn Lê Nguyên Vũ: Đạt 89,7% (78 đơn).",
            "  5. AM Lê Thanh Nhựt: Đạt 88,0% (+9,8%p WoW, 624 đơn).",
            "  6. AM Hồng Bích Nga: Bứt phá tăng vọt +20,5%p WoW, vươn lên đạt 86,9% (466 đơn).",
            "  7. AM Phan Đình Duy: Đạt 85,8% (+12,5%p WoW, 148 đơn).",
            "  8. AM Nguyễn Ngọc Khánh: Đạt 84,8% (330 đơn).",
            "  9. AM Nguyễn Hoàng Phi: Em xin biểu dương AM Phi tuần qua có bước nhảy vọt thần tốc nhất vùng khi tăng tới +29,9%p WoW (từ 50,4% tuần W37 nhảy vọt lên 80,4% tuần W38), chính thức đưa toàn bộ 570 đơn vượt chuẩn xanh!",
            "- Nhóm 6 AM CHƯA ĐẠT CHUẨN KPI (< 80,0%) CẦN CHẤN CHỈNH NGAY:",
            "  1. AM Nguyễn Đỗ Minh Nghĩa: Đạt 78,7% (-9,7%p WoW, 164 đơn) — suýt soát chạm vạch 80%, cần siết lại nhịp gom hàng cuối ngày.",
            "  2. AM Nguyễn Thanh Long: Đạt 69,6% (+10,1%p WoW, 56 đơn).",
            "  3. AM Huỳnh Thúc Duân: Đạt 64,2% (+13,8%p WoW, 81 đơn) — phụ trách Đắk Nông, tiến độ cải thiện còn quá chậm.",
            "  4. AM Nguyễn Thị Tuyết Thơ: Đạt 55,5% (274 đơn) — BÁO ĐỘNG ĐỎ tụt dốc sâu nhất toàn vùng khi rơi thẳng đứng -15,7%p WoW (W37 đang đạt 71,1%).",
            "  5. AM Lê Văn Trường: Đạt 54,9% (+14,8%p WoW, 459 đơn) — dù có tăng trưởng nhưng tỷ lệ đơn trễ hạn vẫn chiếm tới 45,1% sản lượng phụ trách.",
            "  6. AM Trần Thị Nhung: Chạm đáy yếu kém toàn vùng khi chỉ đạt vỏn vẹn 37,9% (174 đơn), hơn 62% lượng hàng TikTok Shop phát sinh bị trễ hạn xuất luân chuyển!"
        ],
        insights=[
            "Toàn vùng đã có bước chuyển biến rất lớn khi 9/15 AM (chiếm 60% nhân sự) và 3/5 tỉnh thành đã làm chủ chỉ số OPR vượt chuẩn 80%.",
            "Tuy nhiên, sự yếu kém tập trung nghiêm trọng ở 3 AM nhóm cuối gồm Tuyết Thơ (55,5%), Văn Trường (54,9%) và Trần Thị Nhung (37,9%) đang kéo tụt chỉ số chung của cả 2 tỉnh Lâm Đồng và Đắk Nông."
        ],
        warnings=[
            "AM Nguyễn Thị Tuyết Thơ đang có dấu hiệu buông lỏng quy trình xử lý TikTok Shop khi để tụt dốc -15,7%p WoW; nếu không can thiệp ngay trong tuần W39, nguy cơ cao các shop lớn trên địa bàn sẽ bị sàn hạn chế lưu lượng hiển thị.",
            "AM Trần Thị Nhung và AM Lê Văn Trường để tỷ lệ vi phạm SLA OPR vượt quá 45%, gây rủi ro phạt tài chính trực tiếp từ sàn TikTok."
        ],
        actions=[
            "Yêu cầu 3 AM yếu nhất (Tuyết Thơ, Văn Trường, Trần Thị Nhung) rà soát lại ngay quy trình chia chọn và quét xuất hàng tại bưu cục, chấm dứt tình trạng dồn ứ hàng không đóng bao xuất luân chuyển kịp giờ.",
            "Thiết lập KPI giám sát giờ vàng: Trước 20h30 hàng ngày, các bưu cục của 6 AM chưa đạt chuẩn bắt buộc phải hoàn thành 100% khâu đóng bao và bàn giao cho xe tải KTC luân chuyển về Hub."
        ]
    )

    # =========================================================================
    # 9. RỚT ĐƠN LUÂN CHUYỂN THEO AM & TỈNH
    # =========================================================================
    add_speech_section(
        doc,
        sec_title="🚨 [IX. PHÂN TÍCH TỶ TRỌNG RỚT ĐƠN LUÂN CHUYỂN THEO AM & TỈNH THÀNH (W38)]",
        speech_heading="🗣️ CẢNH BÁO BẤT THƯỜNG: TỶ LỆ RỚT LUÂN CHUYỂN TĂNG LÊN 3.32% VỚI 252 ĐƠN BỊ BỎ LẠI:",
        paragraphs_text=[
            "Kính thưa Ban Giám Đốc, trái ngược với nỗ lực cải thiện OPR, chỉ số rớt đơn luân chuyển tuần W38 đang gióng lên hồi chuông cảnh báo đỏ trên diện rộng:",
            "• Tổng quan toàn vùng tuần W38: Tỷ lệ rớt đơn luân chuyển toàn vùng đã tăng từ 1,80% tuần W37 lên mức 3,32% trong tuần W38 (+1,52%p WoW), tương ứng với 252 đơn hàng bị rớt lại trên tổng số 7.586 đơn cần luân chuyển trong tuần.",
            "• Đánh giá chi tiết địa bàn 5 Tỉnh thành:",
            "- Đắk Nông: BÁO ĐỘNG ĐỎ KỶ LỤC TOÀN VÙNG khi tỷ lệ rớt luân chuyển bùng phát lên tới 20,73% (tăng vọt +16,57%p WoW so với mức chỉ 4,17% của W37, với 57 đơn rớt / 275 đơn cần LC) — đồng nghĩa với việc cứ 5 đơn cần luân chuyển ra khỏi bưu cục thì có hơn 1 đơn bị bỏ rơi lại!",
            "- Khánh Hòa: Là tỉnh để xảy ra số lượng đơn rớt lớn nhất toàn mạng lưới với 102 đơn rớt (tỷ lệ 5,09%, tăng +3,34%p WoW trên 2.005 đơn cần LC) do áp lực gom hàng lớn tại các bưu cục ven vịnh và trung tâm.",
            "- Lâm Đồng: Để rớt 58 đơn (tỷ lệ 3,32%, tăng +1,28%p WoW trên 1.748 đơn cần LC).",
            "- Ninh Thuận: Rớt 16 đơn (tỷ lệ 1,14% / 1.390 đơn).",
            "- Bình Thuận: Kiểm soát luân chuyển tốt nhất khu vực ven biển với 19 đơn rớt (tỷ lệ chỉ 0,88% trên 2.168 đơn cần LC).",
            "• Điểm danh đích danh từng Quản lý Vận hành (AM) có tỷ lệ rớt cao và lượng đơn rớt lớn:",
            "- AM Huỳnh Thúc Duân (Đắk Nông): Tỷ lệ rớt luân chuyển cao kỷ lục toàn mạng lưới lên tới 20,79% (tăng sốc +20,14%p WoW so với tuần W37 chỉ 0,65%), để rớt 21 đơn trên 101 đơn cần LC.",
            "- AM Trần Thị Nhung (Đắk Nông): Tỷ lệ rớt luân chuyển đạt 19,76% (tăng vọt +13,84%p WoW so với W37 5,92%), để rớt 33 đơn trên 167 đơn cần LC.",
            "- AM Thái Thị Thanh Thư (Khánh Hòa): Tỷ lệ rớt 7,13% (tăng +4,98%p WoW so với W37 2,15%), đặc biệt đây là AM để RỚT SỐ LƯỢNG ĐƠN LỚN NHẤT TOÀN VÙNG với 79 đơn rớt / 1.108 đơn cần LC (chiếm hơn 31% tổng số đơn rớt của cả vùng Nam Trung Bộ!).",
            "- AM Hồng Bích Nga (Đắk Nông): Tỷ lệ rớt 4,49% (tăng +2,65%p WoW, để rớt 27 đơn / 601 đơn cần LC).",
            "- AM Lê Văn Trường (Lâm Đồng): Tỷ lệ rớt 4,24% (tăng +2,10%p WoW, để rớt 21 đơn / 495 đơn cần LC).",
            "- AM Nguyễn Hoàng Phi: Tỷ lệ rớt 2,84% (để rớt 19 đơn / 670 đơn cần LC).",
            "• Bóc tách danh sách Top Bưu cục điểm nóng để xảy ra rớt đơn nặng nề nhất:",
            "- Bưu cục (DNO) Đức Lập (phụ trách bởi AM Trần Thị Nhung): BÁO ĐỘNG ĐỎ TOÀN MẠNG khi một mình bưu cục này để rớt tới 32 đơn hàng (tỷ lệ rớt 27,83% trên 115 đơn cần LC) — chiếm tới 12,7% tổng đơn rớt của toàn vùng!",
            "- Bưu cục (DNO) Đông Gia Nghĩa (phụ trách bởi AM Huỳnh Thúc Duân): Để rớt 11 đơn (tỷ lệ rớt lên tới 42,31% trên 26 đơn cần LC).",
            "- Bưu cục (DNO) Bắc Gia Nghĩa (phụ trách bởi AM Huỳnh Thúc Duân): Để rớt 8 đơn (tỷ lệ rớt 20,51% trên 39 đơn cần LC).",
            "- Bưu cục (NTH) Thuận Nam (phụ trách bởi AM Nguyễn Duy Long): Để rớt 4 đơn (tỷ lệ rớt 100% / 4 đơn).",
            "- Bưu cục (DNO) Kiến Đức (phụ trách bởi AM Hồng Bích Nga): Để rớt 3 đơn (tỷ lệ rớt 42,86% / 7 đơn cần LC).",
            "- Bưu cục (DNO) ĐL Nam Gia Nghĩa 2 (phụ trách bởi AM Huỳnh Thúc Duân): Để rớt 2 đơn (tỷ lệ rớt 40,0% / 5 đơn).",
            "- Bưu cục (LDO) Lang Biang - Đà Lạt 1 (phụ trách bởi AM Lê Minh Lợi): Để rớt 2 đơn (tỷ lệ rớt 100% / 2 đơn).",
            "- Các bưu cục rớt 1 đơn nhưng tỷ lệ 100%: (DNO) Quảng Sơn (AM Trần Thị Nhung), (LDO) Đinh Văn Lâm Hà (AM Huỳnh Thị Kim Chi), (BTH) Mũi Né (AM Nguyễn Ngọc Khánh - rớt 1/5 đơn, 20%)."
        ],
        insights=[
            "Hành vi tác nghiệp cẩu thả tại bưu cục: Nhân viên kho không quét mã bao/kiện điện tử để bàn giao cho tài xế xe tải KTC theo đúng quy trình; đóng chuyến trễ giờ cắt dẫn tới việc xe tải KTC tuyến buộc phải xuất bến bỏ lại các kiện hàng nằm lăn lóc tại sàn kho.",
            "Tập trung cục bộ nguy hiểm: 3 AM gồm Thái Thị Thanh Thư (79 đơn), Trần Thị Nhung (33 đơn) và Hồng Bích Nga (27 đơn) cộng lại đã chiếm tới hơn 55% tổng lượng đơn rớt của toàn mạng."
        ],
        warnings=[
            "252 đơn rớt luân chuyển này sẽ tự động biến thành 252 đơn vi phạm ODR giao trễ hạn, kéo tụt nghiêm trọng chỉ số cam kết SLA của tỉnh Đắk Nông và Khánh Hòa."
        ],
        actions=[
            "Quy trách nhiệm trực tiếp cho AM Huỳnh Thúc Duân và AM Trần Thị Nhung: Phải trực tiếp có mặt tại Bưu cục Đức Lập, Đông Gia Nghĩa và Bắc Gia Nghĩa kiểm soát 100% giờ đóng bao và quét bàn giao điện tử với lái xe KTC trước 19h30 hàng ngày.",
            "Phạt 50.000đ/đơn rớt luân chuyển đối với Trưởng bưu cục và tài xế nếu để phát sinh đơn rớt luân chuyển không lý do chính đáng trong tuần W39."
        ]
    )

    # =========================================================================
    # 10. BÁO CÁO HOÀN TRẢ %FD (RETURN)
    # =========================================================================
    add_speech_section(
        doc,
        sec_title="🔄 [X. BÁO CÁO TỶ LỆ %FD (RETURN / HOÀN TRẢ) — VÙNG NAM TRUNG BỘ (W38)]",
        speech_heading="🗣️ PHÂN TÍCH TỶ LỆ HOÀN TRẢ (%FD) VÀ SO SÁNH BIẾN ĐỘNG WOW TẠI CÁC BƯU CỤC NÓNG:",
        paragraphs_text=[
            "Kính thưa Ban Giám Đốc, về tỷ lệ Hoàn Trả (%FD) — chỉ số trực tiếp bào mòn biên lợi nhuận của vùng:",
            "• Tổng quan toàn mạng tuần W38: Tỷ lệ %FD Full hàng toàn vùng giữ ở mức 6,73% (giảm nhẹ -0,81%p WoW so với mức 7,54% của W37). Riêng kênh TikTok Shop đạt 6,10% (giảm -0,70%p WoW). Tổng số đơn hoàn trả ghi nhận 24.518 đơn trên toàn bộ mạng lưới giao.",
            "• Phân hóa theo 5 Tỉnh thành:",
            "- Bình Thuận và Ninh Thuận kiểm soát hoàn trả tốt nhất khu vực với tỷ lệ FD chỉ lần lượt 5,82% và 6,10%.",
            "- Khánh Hòa giữ ở mức 6,65%.",
            "- Hai tỉnh Tây Nguyên tiếp tục là vùng trũng rủi ro: Lâm Đồng đạt 7,54% và Đắk Nông ghi nhận mức hoàn trả cao nhất vùng lên tới 8,12%.",
            "• So sánh biến động WoW tại Top 10 Bưu cục có tỷ lệ hoàn trả cao nhất mạng lưới:",
            "- Bưu cục (DNO) Quảng Tín (AM Trương Quang Linh): BÁO ĐỘNG ĐỎ cao nhất toàn vùng khi %FD lên tới 37,89% (770 đơn hoàn / 2.032 đơn giao), tăng mạnh +4,37%p WoW so với tuần W37 (33,52%) — cứ gần 2,5 đơn giao đi thì có 1 đơn bị trả về!",
            "- Bưu cục (LDO) Lang Biang - Đà Lạt 1 (AM Trần Tấn Lợi): %FD đạt 20,30% (625 đơn hoàn / 3.079 đơn), tăng vọt +4,03%p WoW so với W37 (16,26%).",
            "- Bưu cục (KHO) Cam Linh (AM Nguyễn Tiến Long): %FD đạt 16,96% (988 đơn hoàn / 5.825 đơn), tăng +2,01%p WoW so với W37 (14,96%).",
            "- Bưu cục (LDO) Đức Trọng 1 (AM Nguyễn Lê Nguyên Vũ): %FD đạt 14,59% (318 đơn hoàn), tăng +2,27%p WoW so với W37 (12,32%).",
            "- Bưu cục (DNO) Đông Gia Nghĩa (AM Huỳnh Thúc Duân): %FD đạt 14,51% (280 đơn hoàn), tăng +1,09%p WoW so với W37 (13,42%).",
            "- Bưu cục (DNO) Tuy Đức (AM Trần Thị Nhung): %FD đạt 12,43% (266 đơn hoàn), tăng +1,02%p WoW so với W37 (11,41%).",
            "- Bưu cục (LDO) Di Linh (AM Nguyễn Lê Nguyên Vũ): %FD bùng phát tăng đột biến +5,71%p WoW (từ 6,37% tuần W37 nhảy vọt lên 12,08% tuần W38 với 733 đơn hoàn).",
            "- Điểm sáng cải thiện: Bưu cục (DNO) Kiến Đức (AM Hồng Bích Nga) ghi nhận %FD giảm -1,83%p WoW (từ 17,36% xuống 15,53%, 343 đơn hoàn)."
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
        speech_heading="🗣️ CẬP NHẬT DỮ LIỆU MỚI: BÓC TÁCH 1.306 ĐƠN AGING LƯU KHO VÀ 4.590 ĐƠN TREO LUÂN CHUYỂN TOÀN VÙNG:",
        paragraphs_text=[
            "Kính thưa Ban Giám Đốc, theo số liệu đối soát mới nhất sáng nay về hàng tồn kho lâu ngày (Aging ≥ 5 ngày) và Treo luân chuyển trên toàn mạng lưới Nam Trung Bộ:",
            "• BỨC TRANH HÀNG AGING LƯU KHO (TỔNG 1.306 ĐƠN TỒN ≥ 5 NGÀY):",
            "- Phân bổ theo 5 Tỉnh thành: Hai tỉnh Tây Nguyên chiếm tới 82,4% tổng lượng hàng aging toàn vùng! Trong đó, Lâm Đồng là điểm nóng lớn nhất với 724 đơn (chiếm 55,4% toàn vùng); Đắk Nông chiếm 353 đơn (27,0%); Khánh Hòa chiếm 211 đơn (16,2%); trong khi Bình Thuận chỉ có 12 đơn (0,9%) và Ninh Thuận kiểm soát cực tốt chỉ có 6 đơn (0,5%).",
            "- Phân nhóm thời gian tồn đọng:",
            "  + Nhóm 5 – 8 ngày: 1.048 đơn (chiếm 80,2% tổng aging) — đây là nhóm hàng có thể giải phóng nhanh nếu bưu cục tập trung lực lượng giao dứt điểm trong 24h tới.",
            "  + Nhóm 8 – 15 ngày: 244 đơn (chiếm 18,7%) — nhóm vướng mắc địa chỉ khó hoặc đang lưu bưu cục chờ khách nhận.",
            "  + Nhóm báo động đỏ trên 15 ngày (> 15 ngày): 14 đơn (chiếm 1,1%) — nguy cơ thất thoát, bể vỡ hoặc đền bù rất cao, bắt buộc lập biên bản xử lý dứt điểm.",
            "- Top 5 AM có lượng hàng Aging đọng nhiều nhất:",
            "  1. AM Lê Văn Trường: 351 đơn (chiếm 26,9% toàn vùng, đứng đầu danh sách tồn đọng).",
            "  2. AM Hồng Bích Nga: 234 đơn (chiếm 17,9%).",
            "  3. AM Nguyễn Lê Nguyên Vũ: 224 đơn (chiếm 17,2%).",
            "  4. AM Nguyễn Thanh Long: 158 đơn (chiếm 12,1%).",
            "  5. AM Trương Quang Linh: 82 đơn (chiếm 6,3%).",
            "• BỨC TRANH TREO LUÂN CHUYỂN (TỔNG 4.590 ĐƠN TRÊN TOÀN HỆ THỐNG):",
            "- Phân bổ trạng thái luân chuyển:",
            "  + Luân chuyển đúng hạn (< 24h): 4.006 đơn (chiếm 87,3%) — đang di chuyển bình thường theo đúng nhịp luân chuyển chuẩn.",
            "  + Tổng đơn Treo luân chuyển quá hạn (> 24h): 584 đơn (chiếm 12,7% tổng luồng hàng).",
            "  + Bóc tách thời gian treo quá hạn: Chớm trễ 24h – 36h có 241 đơn (5,3%); Treo nguy hiểm 36h – 72h có 212 đơn (4,6%); Treo nghiêm trọng 72h – 120h (3 – 5 ngày) có 74 đơn (1,6%); và đặc biệt có 57 đơn treo báo động đỏ trên 5 ngày (> 120h), trong đó có 21 đơn treo trên 8 ngày chưa cập bến!",
            "- Địa bàn tập trung đơn treo luân chuyển: Lâm Đồng chiếm 1.630 đơn (35,5%); Khánh Hòa chiếm 1.370 đơn (29,8%); Đắk Nông chiếm 734 đơn (16,0%); Bình Thuận chiếm 509 đơn (11,1%) và Ninh Thuận chiếm 347 đơn (7,6%).",
            "- Top AM có lượng đơn treo luân chuyển cao nhất: AM Lê Văn Trường (596 đơn — đứng đầu toàn vùng cả về aging lẫn treo luân chuyển), AM Thái Thị Thanh Thư (427 đơn), AM Nguyễn Duy Long (393 đơn), AM Phan Đình Duy (377 đơn), và AM Trần Thị Nhung (354 đơn)."
        ],
        insights=[
            "Hàng aging và hàng treo luân chuyển có sự tương đồng rõ rệt về địa bàn: Lâm Đồng và Đắk Nông là 2 điểm nghẽn lớn nhất, phản ánh khâu kiểm soát tồn và nhịp xe gom giữa các bưu cục đồi núi về kho trung tâm chưa được chuẩn hóa.",
            "AM Lê Văn Trường đang là mắt xích nghẽn nặng nề nhất khi phụ trách tới 351 đơn aging và 596 đơn treo luân chuyển, cần có sự hỗ trợ can thiệp trực tiếp từ Giám đốc Vận hành."
        ],
        warnings=[
            "14 đơn aging > 15 ngày và 57 đơn treo luân chuyển > 5 ngày nếu không truy vết xử lý ngay trong 48h tới chắc chắn sẽ chuyển hóa thành đơn đền bù thất thoát với tổng giá trị thiệt hại ước tính trên 35 triệu đồng."
        ],
        actions=[
            "Thiết lập 'Tổ đặc nhiệm giải cứu hàng Aging' tại Lâm Đồng: Yêu cầu 4 AM (Trường, Nga, Vũ, Long) trong ngày hôm nay phải tổ chức rà soát trực tiếp 100% kho bãi, phân loại và giao dứt điểm 1.048 đơn nhóm 5–8 ngày.",
            "Đội KTC kích hoạt chiến dịch 'Xả treo luân chuyển': Truy vết toàn bộ 57 đơn treo > 5 ngày và 212 đơn treo 36–72h, xác định chính xác vị trí thất lạc tại kho trung chuyển để hoàn tất bàn giao trong ngày 23/09."
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
        speech_heading="🗣️ BÁO ĐỘNG ĐỎ TRUY THU: BÙNG NỔ 282.4 TRIỆU ĐỒNG (+241.0 TRIỆU WoW — TĂNG +582%):",
        paragraphs_text=[
            "Kính thưa Ban Giám Đốc, đây là nội dung báo động đỏ tài chính và kiểm soát thất thoát nghiêm trọng nhất của tuần W38:",
            "• Biến động bùng nổ toàn mạng: Số tiền CẦN TRUY THU THỰC TẾ tuần W38 đã bùng phát lên mức kỷ lục 282,4 triệu đồng (chính xác 282.441.700 VNĐ), tăng vọt thêm +241,0 triệu đồng (tương ứng mức tăng sốc +581,7% WoW so với con số chỉ 41,4 triệu đồng của tuần W37!). Tổng số bản ghi/ticket phạt phát sinh lên tới 3.074 ticket (tăng +744 ticket, +31,9% WoW).",
            "• Cơ cấu 4 nguyên nhân truy thu chính toàn vùng:",
            "- 1. Liên đới chiếm dụng: 107,6 triệu đồng (chiếm 38,1% tổng tiền truy thu toàn vùng).",
            "- 2. Tick mất hàng: 52,0 triệu đồng (chiếm 18,4%, tăng thêm +125 ticket vi phạm).",
            "- 3. Kiện thiếu đơn: 30,7 triệu đồng (chiếm 10,9%).",
            "- 4. Giao sai quy trình tác nghiệp: 18,4 triệu đồng (chiếm 6,5%).",
            "• Điểm danh đích danh Top 5 Quản lý Vận hành (AM) bị truy thu nặng nề nhất (Chiếm tới 84,1% tổng tiền truy thu toàn vùng):",
            "1. AM Thái Thị Thanh Thư (Khánh Hòa) — BÁO ĐỘNG ĐỎ SỐ 1: Bị truy thu lên tới 81,7 triệu đồng (81.660.686 VNĐ), tăng đột biến +79,9 triệu đồng (+4.505% WoW so với tuần W37 chỉ 1,8 triệu đồng!). Điểm danh bưu cục thủ phạm: Tập trung tới 93,2% số tiền truy thu của AM Thư nằm tại Bưu cục (KHO) Bắc Nha Trang với 76,1 triệu đồng (tăng vọt +75,0 triệu đồng WoW)!",
            "2. AM Trần Văn Phước (Đắk Nông) — BÁO ĐỘNG ĐỎ SỐ 2: Bị truy thu 49,6 triệu đồng (49.649.059 VNĐ, tăng vọt +44,6 triệu đồng, +880,5% WoW, phát sinh tới 678 ticket). Điểm danh 2 bưu cục nóng: Bưu cục (DNO) Quảng Tín bị truy thu 24,9 triệu đồng (tăng +24,6 triệu WoW với 468 ticket) và Bưu cục (DNO) Kiến Đức bị truy thu 24,2 triệu đồng (tăng +23,6 triệu WoW với 110 ticket)!",
            "3. AM Huỳnh Thị Kim Chi (Lâm Đồng) — BÁO ĐỘNG ĐỎ SỐ 3: Bị truy thu 45,1 triệu đồng (45.105.158 VNĐ, tăng +41,4 triệu đồng, +1.123% WoW). Điểm danh 2 bưu cục thủ phạm: Bưu cục (LDO) Đam Rông 3 bị truy thu 33,3 triệu đồng (tăng +30,5 triệu WoW) và Bưu cục (LDO) Tân Hà Lâm Hà bị truy thu 11,8 triệu đồng (tăng +11,8 triệu WoW)!",
            "4. AM Nguyễn Ngọc Khánh (Bình Thuận): Bị truy thu 35,2 triệu đồng (35.200.624 VNĐ, tăng +26,1 triệu đồng, +285,4% WoW). Điểm danh đơn vị nóng: Kho Chuyển Tiếp Bình Thuận bị truy thu 31,6 triệu đồng (tăng +22,8 triệu WoW với 90 ticket)!",
            "5. AM Lê Văn Trường (Lâm Đồng): Bị truy thu 25,5 triệu đồng (25.524.546 VNĐ, tăng +16,4 triệu đồng WoW). Đáng báo động đây là AM CÓ SỐ LƯỢNG TICKET PHẠT NHIỀU NHẤT TOÀN VÙNG với 805 ticket (+553 ticket WoW), trong đó tâm điểm là Bưu cục (LDO) Đơn Dương bị truy thu 16,7 triệu đồng (468 ticket, tăng +8,6 triệu WoW)!",
            "• Nhóm các AM kiểm soát truy thu tốt hơn (dưới 15 triệu đồng):",
            "- AM Phan Đình Duy: 14,9 triệu đồng (chủ yếu tại Bưu cục Tây Nha Trang 14,1 triệu).",
            "- AM Nguyễn Thanh Long: 9,3 triệu đồng (Bưu cục Cam Linh 5,3 triệu, đã giảm -600k WoW).",
            "- AM Huỳnh Thúc Duân: 5,0 triệu đồng (Bưu cục Đông Gia Nghĩa 5,0 triệu).",
            "- AM Trầm Hữu Tiến: 5,0 triệu đồng (Bưu cục Đức Trọng 1 2,6 triệu)."
        ],
        insights=[
            "Lỗ hổng buông lỏng kiểm soát cân đo và nhận hàng: Tại Bưu cục Bắc Nha Trang (76,1 Tr), Đam Rông 3 (33,3 Tr), KCT Bình Thuận (31,6 Tr), Quảng Tín (24,9 Tr), Kiến Đức (24,2 Tr) và Đơn Dương (16,7 Tr), nhân viên tiếp nhận hàng hóa bỏ qua hoàn toàn việc đo kích thước 3 chiều của thùng hàng quy đổi thể tích hoặc bao che cho shop quen gửi hàng cồng kềnh với cước hàng nhẹ.",
            "Tình trạng liên đới chiếm dụng và mất kiện hàng tăng vọt 107,6 triệu đồng cho thấy kỷ luật bàn giao ca và kiểm kê bưu cục đang bị buông lỏng nghiêm trọng."
        ],
        warnings=[
            "282,4 triệu đồng truy thu nếu không được thu hồi từ người gửi sẽ bị chế tài trừ trực tiếp vào quỹ lương và tiền thưởng của các AM và bưu cục có liên quan."
        ],
        actions=[
            "Yêu cầu 5 AM nhóm đầu (Thanh Thư, Văn Phước, Kim Chi, Ngọc Khánh, Văn Trường) lập tức xuống thanh tra trực tiếp tại 6 bưu cục điểm nóng kể trên trong vòng 24 giờ tới.",
            "Kích hoạt quy trình: 100% kiện hàng cồng kềnh thùng xốp, hàng nông sản tại Bắc Nha Trang, Đam Rông 3, Quảng Tín bắt buộc phải chụp ảnh có kèm thước đo 3 chiều tải lên hệ thống trước khi in nhãn xuất kho."
        ]
    )

    # =========================================================================
    # 15. DOANH THU & PHÁT TRIỂN SHOP MỚI (F30)
    # =========================================================================
    add_speech_section(
        doc,
        sec_title="📈 [XV. PHÂN TÍCH DOANH THU KINH DOANH & TĂNG TRƯỞNG KHÁCH HÀNG MỚI (F30) (W38)]",
        speech_heading="🗣️ TỔNG DOANH THU 1.143 TỶ ĐỒNG VÀ PHÁT TRIỂN 135 KHÁCH HÀNG MỚI F30:",
        paragraphs_text=[
            "Kính thưa Ban Giám Đốc, về kết quả hoạt động kinh doanh và phát triển thị trường của khối Thương Mại Vùng Nam Trung Bộ tuần W38:",
            "• Tổng quy mô doanh thu thuần tuần W38: Toàn vùng ghi nhận doanh thu đạt 1.142.868.830 VNĐ (1,143 tỷ đồng) trên tổng số 39.003 đơn hàng phát sinh cước giao dịch.",
            "• Điểm danh chi tiết đóng góp doanh thu và cơ cấu thị phần của từng AM:",
            "- AM Phan Đình Duy (Khánh Hòa) — QUÁN QUÂN DOANH THU TOÀN VÙNG: Tiếp tục giữ vị trí đầu tàu kinh doanh số 1 của Nam Trung Bộ khi mang về 506,6 triệu đồng (506.646.806 VNĐ), MỘT MÌNH ĐÓNG GÓP TỚI 43,4% TỔNG DOANH THU TOÀN VÙNG trên 10.613 đơn hàng, đạt mức tăng trưởng dương +7,9 triệu đồng WoW nhờ sức tiêu thụ cực mạnh của các chuỗi shop online lớn tại Nha Trang.",
            "- AM Thái Thị Thanh Thư (Khánh Hòa): Đứng thứ hai toàn vùng với doanh thu 98,3 triệu đồng (chiếm 8,4% thị phần doanh thu vùng, với 5.345 đơn hàng).",
            "- AM Nguyễn Duy Long (Bình Thuận): Đạt 97,3 triệu đồng (chiếm 8,3% doanh thu, 3.690 đơn, tăng trưởng +2,1 triệu đồng WoW).",
            "- AM Huỳnh Thúc Duân (Đắk Nông) — ĐIỂM SÁNG TĂNG TRƯỞNG BỨT PHÁ: Đạt 66,7 triệu đồng (chiếm 5,7% doanh thu, 6.175 đơn), đặc biệt đây là AM CÓ TỐC ĐỘ TĂNG TRƯỞNG DOANH THU MẠNH NHẤT TOÀN VÙNG với mức tăng vọt +15,8 triệu đồng WoW!",
            "- AM Hồng Bích Nga (Đắk Nông): Đạt 52,4 triệu đồng (chiếm 4,5% doanh thu, tăng +2,3 triệu đồng WoW).",
            "- AM Lê Thanh Nhựt (Bình Thuận): Đạt 51,0 triệu đồng (chiếm 4,4% doanh thu, 2.502 đơn).",
            "- AM Nguyễn Lê Nguyên Vũ (Lâm Đồng): Đạt 50,5 triệu đồng (chiếm 4,4% doanh thu, 2.222 đơn).",
            "- AM Trần Thị Nhung (Đắk Nông): Đạt 31,2 triệu đồng (chiếm 2,7% doanh thu).",
            "- AM Nguyễn Đỗ Minh Nghĩa (Ninh Thuận): Đạt 30,8 triệu đồng (tăng +3,3 triệu đồng WoW).",
            "- AM Lê Văn Trường (Lâm Đồng): Đạt 26,7 triệu đồng (tăng nhẹ +385k WoW).",
            "• Cảnh báo nhóm AM có doanh thu suy giảm cần đôn đốc khẩn cấp:",
            "- AM Huỳnh Thị Kim Chi (Lâm Đồng): BÁO ĐỘNG ĐỎ KINH DOANH khi doanh thu sụt giảm sâu nhất toàn vùng tới -9,2 triệu đồng WoW (chỉ còn 37,8 triệu đồng, 1.258 đơn) do bị rơi rụng các shop nông sản Lâm Hà vào tay đối thủ.",
            "- AM Lê Thanh Nhựt (Bình Thuận): Doanh thu sụt giảm -3,9 triệu đồng WoW (còn 51,0 triệu đồng).",
            "- AM Trần Thị Nhung (Đắk Nông): Doanh thu giảm -1,2 triệu đồng WoW (còn 31,2 triệu đồng).",
            "• Phong trào phát triển Khách hàng mới (F30):",
            "- Toàn vùng trong tuần W38 đã khai thác, ký kết và kích hoạt thành công 135 khách hàng mới F30, mang lại nguồn doanh thu ban đầu đạt 10,32 triệu đồng.",
            "- Bảng vàng Top AM dẫn đầu phát triển khách hàng mới F30:",
            "  1. AM Nguyễn Duy Long (Bình Thuận): Dẫn đầu toàn mạng với 20 khách hàng mới F30 (mang về 1,32 triệu đồng doanh thu).",
            "  2. AM Phan Đình Duy (Khánh Hòa): Đứng thứ hai với 17 khách hàng mới F30 (mang về 0,97 triệu đồng).",
            "  3. AM Thái Thị Thanh Thư (Khánh Hòa): Mang về 15 khách hàng mới F30 (doanh thu 1,25 triệu đồng).",
            "  4. AM Nguyễn Thanh Long: Phát triển 12 khách hàng mới F30 (doanh thu 0,69 triệu đồng).",
            "  5. AM Trần Thị Nhung: Đạt 11 khách hàng mới F30 (doanh thu 0,46 triệu đồng).",
            "  6. AM Hồng Bích Nga: Đạt 10 khách hàng mới F30 (doanh thu 0,55 triệu đồng).",
            "  7. AM Huỳnh Thúc Duân: Đạt 9 khách hàng mới F30 (doanh thu 0,78 triệu đồng)."
        ],
        insights=[
            "Cơ cấu doanh thu phụ thuộc rất lớn vào Nha Trang: Một mình AM Phan Đình Duy gánh 43,4% doanh thu vùng cho thấy tiềm năng kinh tế biển và TMĐT nội thị cực lớn, nhưng cũng đặt ra bài toán rủi ro tập trung.",
            "Điểm sáng Đắk Nông: AM Huỳnh Thúc Duân bứt phá doanh thu +15,8 triệu đồng WoW chứng minh nông sản Tây Nguyên bước vào mùa thu hoạch rộ, mở ra dư địa kinh doanh rất lớn cho các bưu cục vùng cao."
        ],
        warnings=[
            "AM Huỳnh Thị Kim Chi để tụt -9,2 triệu đồng doanh thu WoW nếu không chặn đứng đà rơi rụng khách hàng sẽ làm thủng chỉ số hoàn thành doanh thu tháng của tỉnh Lâm Đồng."
        ],
        actions=[
            "Yêu cầu AM Huỳnh Thị Kim Chi cùng chuyên viên kinh doanh Lâm Đồng tổ chức gặp gỡ trực tiếp 5 khách hàng lớn đã giảm đơn tại Lâm Hà trong ngày 23/09 để đưa ra chính sách cước giữ chân.",
            "Nhân rộng kịch bản tiếp cận khách hàng mới F30 của AM Nguyễn Duy Long (20 shop) và AM Phan Đình Duy (17 shop) cho toàn bộ 16 AM còn lại học tập."
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
            "3. Quét mã bao/kiện điện tử 100% khi bàn giao xe KTC: Xóa bỏ hoàn toàn tình trạng 252 đơn rớt luân chuyển (tỷ lệ 3,32%), đặc biệt tại Đức Lập, Đông Gia Nghĩa và Bắc Gia Nghĩa; tài xế và nhân viên kho vi phạm sẽ bị xử phạt nghiêm khắc.",
            "4. Chiến dịch thanh tra cân đo và chặn truy thu: Kiểm tra 100% kích thước ba chiều của các kiện hàng cồng kềnh tại quầy, đặc biệt tại 6 điểm nóng (Bắc Nha Trang 76,1 Tr, Đam Rông 3 33,3 Tr, KCT Bình Thuận 31,6 Tr, Quảng Tín 24,9 Tr, Kiến Đức 24,2 Tr, Đơn Dương 16,7 Tr); kéo giảm số tiền truy thu từ 282,4 triệu đồng xuống dưới 40 triệu đồng trong tuần W39.",
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
