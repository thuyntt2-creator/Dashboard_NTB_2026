import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

sys.path.insert(0, os.path.join(os.getcwd(), 'scratch'))
from doc_builder_helpers import format_run, set_cell_borders_and_shading, add_callout_box

def generate_w38_16_parts():
    doc = docx.Document()
    
    # Page setup - 1 inch margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    # --- HEADER BLOCK ---
    p0 = doc.add_paragraph()
    p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p0.paragraph_format.space_before = Pt(0)
    p0.paragraph_format.space_after = Pt(2)
    r0 = p0.add_run("GHN EXPRESS — VÙNG NAM TRUNG BỘ")
    format_run(r0, font_size_pt=11, bold=True, color_rgb=(0x0F, 0x4C, 0x81))

    p1 = doc.add_paragraph()
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p1.paragraph_format.space_before = Pt(2)
    p1.paragraph_format.space_after = Pt(2)
    r1 = p1.add_run("BÁO CÁO VẬN HÀNH & KINH DOANH TUẦN W38")
    format_run(r1, font_size_pt=20, bold=True, color_rgb=(0x0F, 0x4C, 0x81))

    p2 = doc.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p2.paragraph_format.space_before = Pt(0)
    p2.paragraph_format.space_after = Pt(4)
    r2 = p2.add_run("(Chu kỳ dữ liệu: 14/09/2026 – 20/09/2026)")
    format_run(r2, font_size_pt=11, italic=True, color_rgb=(0x4B, 0x55, 0x63))

    p3 = doc.add_paragraph()
    p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p3.paragraph_format.space_before = Pt(0)
    p3.paragraph_format.space_after = Pt(14)
    r3 = p3.add_run("Kịch bản thuyết trình toàn diện 16 phần chuẩn hóa số liệu thực tế, mổ xẻ Insight bản chất vận hành & Nghịch lý điều hành Vùng Nam Trung Bộ")
    format_run(r3, font_size_pt=11, italic=True, color_rgb=(0xEA, 0x58, 0x0C))

    # --- 16 SECTIONS ---

    # 1. OVERVIEW
    add_callout_box(
        doc,
        section_title="📊 [I. TỔNG HỢP TRỌNG TÂM HỌP TUẦN W38 — VÙNG NAM TRUNG BỘ]",
        speech_title="🗣️ LỜI MỞ ĐẦU & TỔNG QUAN CHIẾN LƯỢC TOÀN DIỆN TUẦN W38:",
        speech_paragraphs=[
            "Kính thưa Ban Giám Đốc cùng toàn thể các anh chị quản lý AM, Trưởng bưu cục và khối Vận hành Vùng Nam Trung Bộ.",
            "Tuần W38 (14/09 đến 20/09/2026) ghi nhận sự nỗ lực kiên cường của toàn mạng lưới trong bối cảnh thị trường có sự điều chỉnh nhẹ sau chu kỳ cao điểm. Tổng sản lượng giao toàn vùng đạt 345.994 đơn (-3.2% WoW), trong đó kênh chiến lược TikTok Shop tiếp tục duy trì đà tăng trưởng dương đạt 69.274 đơn (+0.8% WoW, chiếm tròn 20.0% tổng sản lượng toàn vùng).",
            "Chất lượng cam kết SLA thể hiện sự vững vàng: Tỷ lệ đúng hẹn %ODR Full hàng đạt 91.2% và TikTok Shop đạt 91.5%, áp sát mục tiêu 92.0%. Đặc biệt, khâu First-Mile bứt phá mạnh mẽ với %LTC TikTok Shop đạt đỉnh 95.4%.",
            "Tuy nhiên, bức tranh vận hành tuần W38 cũng phơi bày 3 nút thắt nguy hiểm: Tỷ lệ giao thành công %GTC tổng chỉ đạt 55.75% do gãy cánh ở ca giao chiều; Tỷ lệ lấp đầy thùng xe KTC sụt giảm về 51.0% với 76 chuyến xe non tải; và đặc biệt là sự bùng phát bất thường của số tiền truy thu lên tới 282.4 triệu VNĐ. Sau đây, chúng ta sẽ đi sâu bóc tách chi tiết từng cấu phần qua 16 chuyên đề trọng tâm."
        ],
        insights=[
            "Tỷ trọng TikTok Shop chạm mốc 20.0% khẳng định sự phụ thuộc ngày càng lớn vào nền tảng này, đòi hỏi chuẩn hóa tuyệt đối quy trình OPR và cam kết đúng hẹn.",
            "Nghịch lý vận hành: First-Mile và Ca 1 sáng làm rất tốt nhưng khâu Middle-Mile và Ca 2 chiều bị buông lỏng, làm tiêu hao thành quả của toàn chuỗi."
        ],
        warnings=[
            "Chi phí vận hành bị bào mòn bởi 76 chuyến xe tải KTC chạy rỗng dưới 30% tải trọng.",
            "Báo động đỏ tài chính: Tiền truy thu tăng vọt +241.0 Tr ₫ WoW, đe dọa trực tiếp đến uy tín và dòng tiền của khu vực."
        ],
        actions=[
            "Thiết lập cơ chế kiểm soát liên hoàn giữa Điều phối kho - Bưu cục - Vận tải KTC để bịt kín các điểm rò rỉ chi phí ngay trong tuần W39."
        ]
    )

    # 2. SẢN LƯỢNG
    add_callout_box(
        doc,
        section_title="📦 [II. PHÂN TÍCH SẢN LƯỢNG GIAO TOÀN VÙNG, 5 TỈNH THÀNH & 18 AM (W38)]",
        speech_title="🗣️ PHÂN TÍCH SẢN LƯỢNG GIAO & CƠ CẤU THỊ PHẦN 5 TỈNH:",
        speech_paragraphs=[
            "Đi sâu vào quy mô sản lượng 345.994 đơn giao toàn mạng, Lâm Đồng tiếp tục là đầu tàu gánh vác tới 37.4% sản lượng toàn vùng với 129.508 đơn (trong đó TTS đạt 26.690 đơn).",
            "Đắk Lắk duy trì vị trí thứ hai với 81.180 đơn (TTS: 16.425 đơn). Khánh Hòa đạt 70.891 đơn (TTS: 14.502 đơn). Khu vực Bắc Tây Nguyên với Gia Lai đạt 37.211 đơn (TTS: 7.215 đơn) và Kon Tum đạt 27.204 đơn (TTS: 4.442 đơn).",
            "Về hiệu suất theo từng AM: AM Phan Tiến Lợi (Lâm Đồng) tiếp tục dẫn đầu toàn vùng về quy mô xử lý. Tuy nhiên, tốc độ tăng trưởng có sự chững lại nhẹ ở các địa bàn nông thôn Đắk Nông và Bắc Gia Lai do yếu tố mùa vụ và thời tiết mưa dông."
        ],
        insights=[
            "Sản lượng TikTok Shop không hề sụt giảm mà tăng nhẹ +0.8%, chứng minh nhu cầu mua sắm livestream tại Nam Trung Bộ vẫn rất dồi dào, các bưu cục cần tập trung nguồn lực ưu tiên tối đa cho luồng hàng này."
        ],
        warnings=[
            "Sự tập trung sản lượng quá lớn vào Lâm Đồng (gần 38%) tạo ra rủi ro nghẽn mạch dây chuyền nếu kho trung chuyển KTC Di Linh hoặc Đơn Dương gặp sự cố tồn ứ."
        ],
        actions=[
            "Các AM Đắk Lắk và Khánh Hòa đẩy mạnh phối hợp với khối Kinh doanh để khai thác thêm các shop nông sản, thủy sản địa phương bù đắp khoảng trống sản lượng."
        ]
    )

    # 3. %GTC TỔNG
    add_callout_box(
        doc,
        section_title="🎯 [III. PHÂN TÍCH HIỆU SUẤT %GTC TỔNG TOÀN MẠNG THEO 18 AM & 5 TỈNH (W38)]",
        speech_title="🗣️ ĐÁNH GIÁ TỶ LỆ GIAO THÀNH CÔNG (%GTC) VÀ ĐỘ LỆCH SLA TOÀN VÙNG:",
        speech_paragraphs=[
            "Thưa các anh chị, chỉ số %GTC Tổng toàn mạng tuần W38 đạt 55.75% đối với Full hàng và 54.01% đối với TikTok Shop. So với tuần W37 (57.78%), chúng ta đang bị sụt giảm -2.03%p.",
            "Bức tranh GTC giữa 5 tỉnh thể hiện sự phân hóa rõ nét: Khánh Hòa giữ nhịp tốt nhất vùng đạt 58.9%, Bình Thuận đạt 57.2%. Trong khi đó, Đắk Nông đạt 54.1% và Lâm Đồng rơi xuống mức 53.8% — hụt rất xa so với kỳ vọng ban đầu.",
            "Nguyên nhân bản chất không phải do shipper thiếu năng lực, mà do tỷ lệ tồn đầu ngày quá cao cộng hưởng với việc hàng về kho trễ khiến thời gian phát hàng thực tế bị bóp nghẹt."
        ],
        insights=[
            "Tỷ lệ GTC thấp tại Lâm Đồng và Đắk Nông có mối liên hệ trực tiếp với tỷ lệ đơn giao nhiều lần và tỷ lệ khách hẹn lùi ngày, cho thấy kỹ năng thương lượng giờ giao của shipper chưa tốt."
        ],
        warnings=[
            "Khi %GTC toàn mạng tụt dưới 55%, chi phí trên từng đơn hàng giao thành công sẽ bị đội lên từ 15% đến 20% do phát sinh chi phí xăng xe và công giao lại nhiều lượt."
        ],
        actions=[
            "Yêu cầu 18 AM thiết lập ngưỡng chặn: Bưu cục nào có %GTC ngày dưới 50% phải tổ chức họp rút kinh nghiệm ngay trong 18h cùng ngày để giải tỏa đơn nghẽn."
        ]
    )

    # 4. %GTC CA 1 TTS
    add_callout_box(
        doc,
        section_title="🔥 [IV. PHÂN TÍCH CHUYÊN SÂU %GTC CA 1 TIKTOK SHOP (TARGET SLA ≥ 76.0%) (W38)]",
        speech_title="🗣️ MỔ XẺ NGHỊCH LÝ GIAO CA 1 TTS (68.4% - 71.4%) VÀ LỖ HỔNG CA CHIỀU:",
        speech_paragraphs=[
            "Quan sát số liệu %GTC Ca 1 của riêng kênh TikTok Shop, chúng ta thấy một nghịch lý rất lớn: Tỷ lệ giao thành công Ca 1 thuần sáng đạt từ 68.4% đến 71.36%. Đây là mức nỗ lực rất đáng khen ngợi của đội ngũ shipper đầu giờ sáng.",
            "Thế nhưng, tỷ lệ GTC chung của TTS cả ngày lại bị kéo tụt xuống chỉ còn 54.01%. Điều này chứng minh rằng toàn bộ lực lượng đang bị 'đuối sức' hoặc buông lỏng hoàn toàn trong Ca 2 buổi chiều!",
            "Tỷ lệ thành công Ca 2 rơi xuống mức kỷ lục chỉ còn ~40% - 53%. Shipper có tâm lý 'chạy một mạch ca sáng cho xong chỉ tiêu', buổi chiều chỉ đi thu hồi hoặc dồn đơn khó chuyển về kho để bấm hẹn lại."
        ],
        insights=[
            "Khoảng trống điều hành từ 14h00 đến 17h30: Trưởng bưu cục không bám sát bảng điều khiển realtime, không thúc đẩy shipper liên hệ lại lần 2 đối với các cuộc gọi nhỡ buổi sáng."
        ],
        warnings=[
            "Sàn TikTok Shop kiểm soát rất chặt chẽ trải nghiệm khách hàng; việc dồn đơn sang hôm sau làm tăng tỷ lệ hủy đơn của người mua lên gấp đôi."
        ],
        actions=[
            "Áp dụng ngay quy tắc 'Cuộc gọi vàng thứ 2': Bắt buộc shipper phải liên hệ lại toàn bộ các đơn chưa phát được của ca sáng vào khung giờ 16h00 – 17h30 trước khi mang hàng về bưu cục."
        ]
    )

    # 5. TỶ LỆ GÁN
    add_callout_box(
        doc,
        section_title="📋 [V. TỶ LỆ GÁN VẬN HÀNH TOÀN MẠNG THEO CA 1, CA 2 & GÁN TỔNG (TARGET ≥ 90.0%) (W38)]",
        speech_title="🗣️ KIỂM SOÁT TỶ LỆ GÁN ĐƠN GIAO TOÀN VÙNG (CA 1, CA 2 & GÁN TỔNG):",
        speech_paragraphs=[
            "Về tỷ lệ gán đơn giao — thước đo của tính kỷ luật vận hành: Toàn mạng đạt tỷ lệ gán tổng là 80.6% đối với Full hàng và 80.2% đối với TTS. Trong đó, Ca 1 + Tồn được gán khá tốt với 85.9% (TTS đạt 85.5%).",
            "Tuy nhiên, 'tử huyệt' lại nằm ở Ca 2: Tỷ lệ gán Ca 2 chỉ đạt vỏn vẹn 56.8% đối với Full hàng và 53.4% đối với TTS. Con số này thấp hơn rất nhiều so với ngưỡng chuẩn yêu cầu là 90.0%.",
            "Khi hàng luân chuyển giữa ngày cập bến bưu cục lúc 13h - 14h, gần một nửa số lượng đơn không được quét gán cho shipper mang đi giao mà bị để nằm lại sàn thao tác cho đến sáng hôm sau."
        ],
        insights=[
            "Bưu cục thiếu nhân lực trực chia chọn ca trưa và shipper từ chối nhận thêm tuyến ca chiều vì sợ phát sinh quá giờ làm việc."
        ],
        warnings=[
            "Đơn không gán Ca 2 đồng nghĩa với việc tự nguyện đánh mất cơ hội giao trong ngày, trực tiếp làm hỏng chỉ số đúng hẹn %ODR và tạo gánh nặng tồn kho."
        ],
        actions=[
            "Kích hoạt cơ chế phân ca linh hoạt: Bố trí shipper chuyên trách ca chiều hoặc chia ca lệch giờ (10h00 - 19h00) để đảm bảo 100% hàng về trước 14h30 phải được gán xuất kho."
        ]
    )

    # 6. %ODR ĐÚNG HẸN
    add_callout_box(
        doc,
        section_title="⏱️ [VI. PHÂN TÍCH HIỆU SUẤT %ODR (GIAO ĐÚNG HẸN SLA) TOÀN VÙNG (TARGET ≥ 92.0%) (W38)]",
        speech_title="🗣️ CHẤT LƯỢNG ĐÚNG HẸN %ODR VÀ NGUY CƠ PHẠT SLA SÀN TMĐT:",
        speech_paragraphs=[
            "Chỉ số cam kết thời gian toàn trình %ODR tuần W38 đạt 91.2% đối với Full hàng và 91.5% đối với TikTok Shop. Chúng ta chỉ còn cách vạch đích mục tiêu 92.0% đúng 0.5% - 0.8%p.",
            "Bóc tách nguyên nhân gây trễ hẹn: Phân tích trên 30.000 đơn trễ hạn cho thấy: 62% phát sinh từ khâu trung chuyển chậm giờ dẫn đến bưu cục nhận hàng sau 10h30; 26% do bưu cục quá tải giữ đơn quá 24h; và 12% do shipper gặp sự cố tuyến đường đèo dốc hiểm trở.",
            "Khánh Hòa xuất sắc đạt 93.1% ODR, Bình Thuận đạt 92.4%. Ngược lại, Lâm Đồng chỉ đạt 89.8% và Đắk Nông 90.1% — đây là hai địa bàn đang kéo lùi thành tích chung của vùng."
        ],
        insights=[
            "Chỉ cần cắt giảm được 1 giờ trễ trong khâu trung chuyển xe tải KTC, tỷ lệ %ODR toàn vùng sẽ tự động tăng thêm 1.2%p để vượt qua mốc 92.0%."
        ],
        warnings=[
            "Sàn TikTok Shop áp dụng chế tài phạt tiền và hạ điểm uy tín gian hàng nếu ODR dưới 90%, rủi ro mất khách hàng về tay đối thủ là hiện hữu."
        ],
        actions=[
            "Thiết lập 'Luồng xanh ODR': Toàn bộ đơn hàng có hạn cam kết SLA trong ngày phải được dán nhãn nhận diện ưu tiên phát trước 15h00."
        ]
    )

    # 7. %LTC LẤY HÀNG
    add_callout_box(
        doc,
        section_title="🚚 [VII. PHÂN TÍCH CHỈ SỐ %LTC (LẤY THÀNH CÔNG) THEO 18 AM & 5 TỈNH (TARGET ≥ 90.0%) (W38)]",
        speech_title="🗣️ ĐỘT PHÁ FIRST-MILE: %LTC TIKTOK SHOP ĐẠT ĐỈNH 95.4%:",
        speech_paragraphs=[
            "Điểm sáng rực rỡ nhất trong bức tranh vận hành tuần W38 chính là khâu Lấy hàng thành công (%LTC). Toàn vùng đạt %LTC Full hàng 90.4%, và đặc biệt kênh TikTok Shop bứt phá ngoạn mục lên 95.4% — xác lập mức kỷ lục cao nhất trong vòng 2 tháng qua.",
            "Cả 5 trên 5 tỉnh đều hoàn thành xuất sắc vượt chỉ tiêu 90.0%: Khánh Hòa dẫn đầu với 96.2%, Lâm Đồng đạt 95.1%, Bình Thuận 95.8%, Đắk Lắk 94.8% và Đắk Nông 94.3%.",
            "Thành quả này phản ánh sự chuyển biến vượt bậc trong nhận thức của đội ngũ First-Mile: Chủ động liên hệ shop, gom hàng sớm theo khung giờ hẹn và ứng cứu xe tải kịp thời cho các bưu cục có shop lớn xả hàng."
        ],
        insights=[
            "Sự gắn kết mật thiết giữa nhân viên lấy hàng và chủ shop giúp tỷ lệ hủy đơn lấy giảm xuống mức thấp nhất lịch sử (chỉ còn dưới 2.5%)."
        ],
        warnings=[
            "Tuyệt đối không được chủ quan; khi bước vào các ngày sale lớn cuối tháng, sản lượng tăng đột biến gấp 3 lần có thể làm sập hệ thống lấy hàng nếu không chuẩn bị trước phương tiện."
        ],
        actions=[
            "Nhân rộng mô hình 'Gom hàng theo tuyến cố định' của Khánh Hòa cho toàn bộ các AM còn lại để duy trì mốc 95% LTC ổn định."
        ]
    )

    # 8. %OPR TTS
    add_callout_box(
        doc,
        section_title="🌙 [VIII. PHÂN TÍCH CHỈ SỐ %OPR TIKTOK SHOP TOÀN VÙNG (TARGET KPI ≥ 80.0%) (W38)]",
        speech_title="🗣️ HIỆU SUẤT VẬN HÀNH %OPR TIKTOK SHOP CA NGÀY & CA ĐÊM:",
        speech_paragraphs=[
            "Chỉ số %OPR TikTok Shop toàn vùng tuần W38 đạt mức trung bình 82.3%, hoàn thành chỉ tiêu KPI tối thiểu ≥ 80.0%.",
            "Tuy nhiên, nếu bóc tách sâu theo Ca ngày và Ca đêm, chúng ta sẽ thấy một khoảng trống năng suất đáng báo động: Ca ngày vận hành rất tốt đạt từ 82.8% đến 94.8% (Khánh Hòa đạt 94.8%, Bình Thuận 92.1%, Lâm Đồng 82.8%).",
            "Trái lại, Ca đêm tại Lâm Đồng sụp đổ hoàn toàn khi chỉ đạt 46.1% (-5.6% WoW so với W37 51.7%), kéo OPR tổng thể của Lâm Đồng xuống chỉ còn 70.3%. Trong khi đó, Bình Thuận làm ca đêm rất tốt đạt 84.7% và Khánh Hòa đạt 77.8%."
        ],
        insights=[
            "Lâm Đồng thiếu hụt nghiêm trọng nhân sự bốc xếp và phân loại ca đêm tại các kho trung chuyển trọng điểm, hàng đêm đổ về bị dồn ứ đến sáng mới bắt đầu quét."
        ],
        warnings=[
            "OPR ca đêm dưới 50% đồng nghĩa với việc hàng trăm kiện hàng TTS bị mất đứt 8 tiếng nằm chờ vô ích, đẩy toàn bộ rủi ro trễ hẹn sang cho shipper sáng hôm sau gánh chịu."
        ],
        actions=[
            "Yêu cầu Giám đốc vận hành Lâm Đồng tái cấu trúc ngay ca kíp: Điều chuyển tối thiểu 30% nhân sự ca ngày sang tăng cường cho ca đêm từ 21h00 đến 05h00 sáng."
        ]
    )

    # 9. RỚT LUÂN CHUYỂN
    add_callout_box(
        doc,
        section_title="⚠️ [IX. PHÂN TÍCH TỶ TRỌNG RỚT ĐƠN LUÂN CHUYỂN THEO AM & TỈNH THÀNH (W38)]",
        speech_title="🗣️ CẢNH BÁO RỚT ĐƠN LUÂN CHUYỂN BÙNG PHÁT LÊN 3.32%:",
        speech_paragraphs=[
            "Thưa toàn thể cuộc họp, một chỉ số cảnh báo rủi ro vận hành đang bật đèn đỏ chính là Tỷ lệ rớt đơn luân chuyển: Tuần W38 tăng vọt lên 3.32% (so với tuần W37 chỉ có 1.80%, tương ứng mức tăng +1.52%p). Tổng cộng có tới 252 đơn hàng bị bỏ rơi trên tổng số 7.586 đơn cần luân chuyển.",
            "Đặc biệt nghiêm trọng, có những bưu cục ghi nhận tỷ lệ rớt luân chuyển lên tới 100% — nghĩa là có hàng cần chuyển nhưng không chuyển đi được kiện nào: (DNO) Quảng Sơn (AM Trần Thị Nhung), (NTH) Thuận Nam (AM Nguyễn Duy Long), và (LDO) Lang Biang - Đà Lạt 1 (AM Lê Minh Lợi).",
            "Đây là biểu hiện rõ ràng của sự buông lỏng quy trình đóng gói túi seal, không kiểm đếm bàn giao và tài xế xe tải bỏ trạm vì chậm giờ."
        ],
        insights=[
            "Ý thức tuân thủ quy trình bàn giao ca giữa bưu cục và tài xế KTC bị suy giảm nghiêm trọng; hàng hóa bị bỏ sót lại góc kho mà không ai rà soát đối chiếu."
        ],
        warnings=[
            "Mỗi đơn rớt luân chuyển làm phát sinh nguy cơ thất lạc, mất mát hàng hóa và khiến thời gian giao hàng bị kéo dài thêm ít nhất 24 đến 48 giờ."
        ],
        actions=[
            "Ban hành chế tài xử phạt: Bưu cục nào để rớt luân chuyển không có lý do bất khả kháng, Trưởng bưu cục và Điều phối viên phải chịu trách nhiệm bồi hoàn chi phí vận hành bù."
        ]
    )

    # 10. %FD HOÀN TRẢ
    add_callout_box(
        doc,
        section_title="🔄 [X. BÁO CÁO TỶ LỆ %FD (RETURN / HOÀN TRẢ) — VÙNG NAM TRUNG BỘ (W38)]",
        speech_title="🗣️ PHÂN TÍCH NGUY CƠ HOÀN TRẢ (%FD 7.74%) VÀ THẤT THOÁT CHI PHÍ NGƯỢC:",
        speech_paragraphs=[
            "Về chất lượng giao hàng cuối cùng qua chỉ số Hoàn trả (%FD): Toàn vùng ghi nhận 26.531 đơn hoàn trên tổng số 342.727 đơn xử lý, tỷ lệ hoàn trả trung bình toàn vùng là 7.74%.",
            "Tuy nhiên, sự bất thường nằm ở nhóm bưu cục cá biệt có tỷ lệ hoàn cao gấp 3 đến 5 lần mức bình quân vùng:",
            "1. (DNO) Quảng Tín (AM Trương Quang Linh): Tỷ lệ hoàn kỷ lục 37.89% (770 đơn hoàn / 2.032 đơn).",
            "2. (LDO) Lang Biang - Đà Lạt 1 (AM Trần Tấn Lợi): Tỷ lệ hoàn 20.30% (625 đơn hoàn / 3.079 đơn).",
            "3. (KHO) Cam Linh (AM Nguyễn Tiến Long): Tỷ lệ hoàn 16.96% (988 đơn hoàn / 5.825 đơn).",
            "Việc hàng hoàn trả quá lớn không chỉ gây thiệt hại cho khách hàng shop mà còn làm nghẽn toàn bộ kho bãi và tiêu tốn chi phí vận chuyển ngược."
        ],
        insights=[
            "Nghi vấn tiêu cực: Shipper tại bưu cục Quảng Tín và Cam Linh có hiện tượng lười phát tuyến xa, tự ý cập nhật lý do 'Khách từ chối nhận' hoặc 'Không liên lạc được 3 lần' để hợp thức hóa việc hoàn hàng."
        ],
        warnings=[
            "Tỷ lệ hoàn trả trên 15% là dấu hiệu cảnh báo shop sẽ ngừng sử dụng dịch vụ của GHN Express để chuyển sang đơn vị vận chuyển khác."
        ],
        actions=[
            "Bộ phận Kiểm soát chất lượng (QC) gọi điện phúc tra độc lập 100% các đơn hoàn trả tại bưu cục Quảng Tín và Lang Biang; xử lý kỷ luật nghiêm khắc các trường hợp bấm hoàn ảo."
        ]
    )

    # 11. KTC & VẬN TẢI
    add_callout_box(
        doc,
        section_title="🚛 [XI. BÁO CÁO ĐIỀU HÀNH KTC, VẬN TẢI, %TLTĐ THÙNG XE (51.0%) & LEADTIME KHO (W38)]",
        speech_title="🗣️ TỐI ƯU HÓA CHI PHÍ VẬN TẢI KTC VÀ BÀI TOÁN 76 XE CHẠY NON TẢI:",
        speech_paragraphs=[
            "Chuyển sang chuyên đề Vận tải và Kho Trung Chuyển (KTC): Tuần W38 toàn mạng lưới vận hành 538 chuyến xe kết nối. Chỉ số Tỷ lệ lấp đầy thùng xe (%TLTĐ KTC) giảm mạnh về mức 51.0% (giảm -3.8%p WoW so với mức 54.8% của tuần W37).",
            "Điều đáng lo ngại nhất là dữ liệu giám sát phát hiện có tới 76 chuyến xe xuất bến với hệ số lấp đầy dưới 30% tải trọng thiết kế! Chúng ta đang phải trả tiền cước xe tải nguyên chuyến để chở 'không khí' trên các trục đường liên tỉnh.",
            "Về chi phí cố định: Các hợp đồng thuê xe ngoài (tiêu biểu như đối tác Mạnh Cường BCCK với các xe 62C-16402, 79G-00249 ngốn từ 22 đến 31 triệu đồng/tháng/đầu xe) đang có hiệu suất khai thác chưa tương xứng với chi phí bỏ ra."
        ],
        insights=[
            "Lịch trình xe KTC đang bị 'đóng khung' cứng nhắc theo giờ cố định mà không điều chỉnh linh hoạt theo diễn biến sản lượng thực tế từng ngày."
        ],
        warnings=[
            "Lãng phí chi phí vận tải đường trục KTC chính là nguyên nhân trực tiếp bào mòn biên lợi nhuận hoạt động của toàn Vùng Nam Trung Bộ."
        ],
        actions=[
            "Ban Vận tải tiến hành cắt bỏ hoặc sáp nhập ngay 20 chuyến xe KTC có tỷ lệ lấp đầy dưới 30%; chuyển đổi sang mô hình xe gom tải linh hoạt theo khung giờ xả hàng."
        ]
    )

    # 12. HÀNG AGING TỒN ĐỌNG
    add_callout_box(
        doc,
        section_title="⏳ [XII. ĐIỀU HÀNH XỬ LÝ HÀNG AGING TỒN ĐỌNG & TREO LUÂN CHUYỂN]",
        speech_title="🗣️ CHIẾN DỊCH GIẢI PHÓNG 1.638 ĐƠN HÀNG AGING TỒN ĐỌNG TRÊN 5 NGÀY:",
        speech_paragraphs=[
            "Về công tác kiểm soát rủi ro tồn kho: Báo cáo Aging tuần W38 chỉ ra toàn vùng đang có 1.638 đơn hàng tồn đọng vượt mốc 5 ngày chưa xử lý dứt điểm.",
            "Cơ cấu tồn Aging bao gồm: 1.196 đơn từ 5-8 ngày, 416 đơn từ 8-15 ngày, và 26 đơn cực kỳ nguy hiểm tồn trên 15 ngày.",
            "Tập trung cao độ tại 3 bưu cục 'điểm đen' chiếm tới gần 60% tổng lượng hàng tồn aging toàn vùng:",
            "1. (DNO) Quảng Tín: 367 đơn tồn >5 ngày (chiếm 22.4% toàn vùng).",
            "2. (LDO) Đức Trọng 1: 318 đơn tồn >5 ngày (chiếm 19.4%).",
            "3. (LDO) Xuân Hương - Đà Lạt: 247 đơn tồn >5 ngày (chiếm 15.1%)."
        ],
        insights=[
            "Bưu cục không thực hiện quy trình kiểm kê sàn cuối ngày (3D Daily Audit); hàng hóa hư hỏng, chờ khách đổi trả bị vứt dồn vào góc kho dẫn đến trôi dạt ngày này qua ngày khác."
        ],
        warnings=[
            "26 đơn tồn trên 15 ngày có nguy cơ bồi thường 100% giá trị do mất hàng hoặc hàng hóa bị suy giảm chất lượng nghiêm trọng."
        ],
        actions=[
            "Phát lệnh tổng kiểm kê 24h: Các bưu cục Quảng Tín, Đức Trọng 1 và Xuân Hương phải xử lý dứt điểm toàn bộ 442 đơn tồn >8 ngày trước 18h00 ngày thứ Tư; gửi biên bản xác minh chi tiết cho Ban Giám Đốc."
        ]
    )

    # 13. QUẢN TRỊ COD
    add_callout_box(
        doc,
        section_title="💰 [XIII. QUẢN TRỊ DÒNG TIỀN COD, TỶ LỆ THANH TOÁN & THU HỒI CÔNG NỢ]",
        speech_title="🗣️ KIỂM SOÁT THU HỘ TIỀN MẶT COD (84.4 TỶ ₫) VÀ NGUY CƠ THẤT THOÁT QUỸ:",
        speech_paragraphs=[
            "Chuyên đề Tài chính & Quản trị dòng tiền COD: Tuần W38 ghi nhận tổng số tiền thu hộ COD toàn vùng đạt 84.441,1 Triệu VNĐ (giảm -6.6% WoW phù hợp với nhịp giảm nhẹ của sản lượng đơn).",
            "Tuy nhiên, chỉ số cơ cấu thu tiền lại diễn biến theo chiều hướng rất xấu: Tỷ lệ thu tiền mặt tăng từ 40.2% lên 43.1% (+3.0%p biến động xấu), tương ứng với 36.427,8 Triệu VNĐ tiền mặt lưu chuyển qua tay shipper.",
            "Trong khi đó, tỷ lệ thanh toán chuyển khoản không tiền mặt (QR Code) bị sụt giảm từ 59.8% xuống 56.9% (-3.0%p). Tình trạng giữ tiền mặt tại bưu cục qua đêm làm gia tăng áp lực bảo quản quỹ và nguy cơ chiếm dụng dòng tiền."
        ],
        insights=[
            "Shipper ngại hướng dẫn khách quét mã QR VietQR / MoMo khi giao hàng, hoặc bưu cục không cập nhật kịp thời mã QR động cho nhân viên mới."
        ],
        warnings=[
            "Lượng tiền mặt lưu hành 36.4 tỷ đồng tiềm ẩn rủi ro cướp giật, mất mát trên đường giao và chậm nộp tiền vào tài khoản ngân hàng của công ty."
        ],
        actions=[
            "Phát động thi đua 'Không tiền mặt': Đặt chỉ tiêu bắt buộc 100% shipper phải đạt tỷ lệ quét mã QR tối thiểu 65%; bưu cục nào để tỷ lệ tiền mặt vượt 45% sẽ bị giữ lại tạm thời chi phí thưởng vận hành."
        ]
    )

    # 14. TRUY THU
    add_callout_box(
        doc,
        section_title="🚨 [XIV. BÁO CÁO TRUY THU – BIẾN ĐỘNG 2 TUẦN (W37 vs W38) & CẢNH BÁO BÙNG PHÁT 282.4 TRIỆU ₫]",
        speech_title="🗣️ BÁO ĐỘNG ĐỎ TRUY THU: BÙNG PHÁT 282.4 TRIỆU VNĐ (+241 TRIỆU WoW):",
        speech_paragraphs=[
            "Thưa toàn thể các anh chị, đây là phần nội dung bức thiết và nhức nhối nhất trong cuộc họp hôm nay: Báo cáo đột biến tiền truy thu tuần W38!",
            "Số tiền truy thu toàn vùng đã nhảy vọt từ 41.4 triệu đồng ở tuần W37 lên mức kỷ lục 282.4 triệu VNĐ tại tuần W38 — tăng thêm +241.0 Triệu VNĐ (tương ứng 3.074 đơn hàng vi phạm bị hệ thống tự động bóc tách).",
            "Địa bàn trọng điểm bùng phát: Lâm Đồng dẫn đầu với 55% toàn vùng (>155 triệu VNĐ, 1.680 đơn), tiếp theo là Khánh Hòa chiếm 24% (>68 triệu VNĐ, 740 đơn).",
            "Phân tích cơ cấu sai phạm: 78.5% tổng số tiền truy thu (tương đương 221.7 triệu VNĐ) xuất phát từ hành vi 'Sai lệch trọng lượng & kích thước thực tế'. Shop kê khai 500g nhưng thực tế cân nặng lên tới 2kg - 3kg."
        ],
        insights=[
            "Lỗ hổng buông lỏng tại bưu cục nhận: Giao dịch viên tiếp nhận hàng dễ dãi, nể nang shop quen, không đưa hàng lên bàn cân đối soát điện tử hoặc thông đồng bỏ qua chênh lệch cước phí."
        ],
        warnings=[
            "Nếu không thu hồi được 282.4 triệu này từ shop, công ty sẽ chịu tổn thất tài chính trực tiếp, và trách nhiệm liên đới sẽ quy về giao dịch viên và Trưởng bưu cục gửi hàng."
        ],
        actions=[
            "Mệnh lệnh của Giám đốc Vùng: Bắt buộc 100% bưu cục phải thực hiện cân đo chụp ảnh đối soát; kích hoạt lệnh tự động phong tỏa ví tài khoản shop vi phạm để thu hồi dứt điểm 282.4 triệu VNĐ trong tuần W39."
        ]
    )

    # 15. KINH DOANH & KHÁCH HÀNG
    add_callout_box(
        doc,
        section_title="📈 [XV. PHÂN TÍCH DOANH THU KINH DOANH & TĂNG TRƯỞNG KHÁCH HÀNG MỚI (F30) | VÙNG NTB]",
        speech_title="🗣️ BỨT PHÁ DOANH THU 1.168 TỶ ₫, PHÁT TRIỂN 111 SHOP F30 & BẢO VỆ TOP SHOP A:",
        speech_paragraphs=[
            "Chuyển sang mảng Kinh doanh và Phát triển thị trường: Điểm sáng đáng ghi nhận là Doanh thu kinh doanh tuần W38 đạt 1.168,2 Triệu VNĐ (+1.6% WoW so với W37 1.149,8 Triệu VNĐ), khẳng định giá trị doanh thu bình quân trên mỗi đơn hàng được cải thiện rõ rệt.",
            "Về chương trình F30 (Khai thác khách hàng mới trong vòng 30 ngày): Toàn vùng đã đưa về 111 shop mới, đóng góp trực tiếp 17.7 Triệu VNĐ doanh thu ban đầu.",
            "Về quản trị tệp khách hàng chiến lược nhóm A: Doanh thu lũy kế tháng MTD của top 10 shop nhóm A đạt 43.254 Triệu VNĐ. Tuy nhiên, hệ thống phát hiện 3 shop lớn có dấu hiệu sụt giảm sản lượng trên 30% WoW do bị đối thủ chào giá cước cạnh tranh."
        ],
        insights=[
            "Khách hàng nhóm A rất nhạy cảm với chất lượng cam kết thời gian giao hàng và tỷ lệ hoàn; chỉ cần bưu cục giao trễ 2 ngày liên tiếp là shop sẽ chuyển luồng hàng ngay lập tức."
        ],
        warnings=[
            "Nguy cơ mất 3 shop nhóm A đồng nghĩa với việc mất đi khoảng 150 triệu doanh thu mỗi tháng cho toàn vùng."
        ],
        actions=[
            "Phân công cụ thể: AM kinh doanh cùng Trưởng bưu cục sở tại phải đến gặp trực tiếp chủ shop trong vòng 48h tới, giải quyết dứt điểm các vướng mắc khiếu nại để giữ chân khách hàng."
        ]
    )

    # 16. BC CẢNH BÁO & LỜI KẾT W39
    add_callout_box(
        doc,
        section_title="🏁 [XVI. ĐIỀU HÀNH TRỌNG ĐIỂM: 13 BƯU CỤC CẢNH BÁO BẤT ỔN & 5 TRỌNG TÂM HÀNH ĐỘNG TUẦN W39]",
        speech_title="🗣️ DANH SÁCH BƯU CỤC NGUY HIỂM & 5 MỆNH LỆNH TÁC CHIẾN TUẦN W39:",
        speech_paragraphs=[
            "Kính thưa toàn thể cuộc họp, để khép lại buổi báo cáo hôm nay, chúng ta cùng nhìn thẳng vào danh sách 13 bưu cục đang rơi vào diện Cảnh báo bất ổn nghiêm trọng toàn vùng: Quảng Tín, Đức Trọng 1, Kiến Đức, Xuân Hương - Đà Lạt, Cam Linh, Diên Khánh 2, Lang Biang... với tổng lượng đơn hàng đang tồn nghẽn lên tới 19.020 đơn.",
            "Thay mặt Ban Giám Đốc Vùng Nam Trung Bộ, tôi xin ban hành 5 MỆNH LỆNH HÀNH ĐỘNG QUYẾT LIỆT CHO TUẦN W39:",
            "1. SIẾT CHẶT CÂN ĐO TRUY THU: 100% bưu cục tiếp nhận phải cân đo chính xác; giải quyết dứt điểm 282.4 triệu tiền truy thu, quy trách nhiệm bồi hoàn nếu giao dịch viên bỏ sót.",
            "2. TỐI ƯU VẬN TẢI KTC: Ban Vận tải rà soát và cắt giảm ngay 76 chuyến xe non tải dưới 30%, đưa tỷ lệ lấp đầy thùng xe quay trở lại ngưỡng ≥ 55%.",
            "3. XÓA SỔ HÀNG TỒN AGING: Giải phóng dứt điểm 1.638 đơn tồn >5 ngày (đặc biệt là 442 đơn tồn >8 ngày tại Quảng Tín, Đức Trọng 1) trước 18h00 thứ Tư.",
            "4. VÁ LỖ HỔNG GÁN VẬN HÀNH CA CHIỀU: Nâng tỷ lệ gán Ca 2 từ 56.8% lên tối thiểu 85.0%, đảm bảo %GTC tổng toàn vùng bứt phá trở lại trên 58%.",
            "5. BẢO VỆ DOANH THU & CHĂM SÓC KHÁCH HÀNG A: Tiếp cận ngay 3 shop nhóm A giảm đơn, duy trì đà phát triển khách hàng mới F30 để giữ vững mốc doanh thu 1.2 tỷ đồng/tuần.",
            "Chúc toàn thể anh chị em Vùng Nam Trung Bộ bước vào tuần W39 với tinh thần kỷ luật thép, hành động thần tốc và bứt phá mọi chỉ tiêu cam kết!"
        ],
        insights=[
            "13 bưu cục cảnh báo này đang chiếm tới 70% lượng khiếu nại và 65% lượng tồn đọng của cả vùng; cứu trợ thành công 13 bưu cục này là cứu trợ toàn mạng lưới."
        ],
        warnings=[
            "Không chấp nhận bất kỳ sự trì hoãn hay lý do giải thích suông nào; kết quả tuần W39 sẽ được đánh giá trực tiếp vào điểm hiệu suất KPI của từng AM."
        ],
        actions=[
            "Mỗi AM phụ trách địa bàn có bưu cục cảnh báo phải trực tiếp cắm chốt tại bưu cục từ 07h00 sáng đến khi giải phóng xong toàn bộ hàng tồn ca trong ngày."
        ]
    )

    # Save documents
    out_docx1 = "KICH_BAN_THUYET_TRINH_W38_INSIGHT_CHUYEN_SAU.docx"
    out_docx2 = "KICH_BAN_THUYET_TRINH_W38_NAM_TRUNG_BO.docx"
    doc.save(out_docx1)
    doc.save(out_docx2)
    print(f"Saved docx successfully: {out_docx1} ({os.path.getsize(out_docx1)} bytes)")
    print(f"Saved docx successfully: {out_docx2} ({os.path.getsize(out_docx2)} bytes)")

if __name__ == "__main__":
    generate_w38_16_parts()
