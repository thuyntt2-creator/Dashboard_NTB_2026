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

def build_w38_natural_doc():
    doc = docx.Document()
    
    # 1 inch margins
    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)
        
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
    r3 = p3.add_run("Kịch bản thuyết trình thực tế 16 chuyên đề điều hành — Mổ xẻ số liệu thực tế, điểm nghẽn vận hành & Nhiệm vụ tuần W39")
    format_run(r3, font_size_pt=11, italic=True, color_rgb=(0xEA, 0x58, 0x0C))

    # --- 16 PARTS WITH NATURAL OPERATIONAL SPEAKING STYLE ---

    # 1. TỔNG QUAN
    add_callout_box(
        doc,
        section_title="📊 [I. TỔNG HỢP TRỌNG TÂM HỌP TUẦN W38 — VÙNG NAM TRUNG BỘ]",
        speech_title="🗣️ LỜI MỞ ĐẦU & ĐÁNH GIÁ TỔNG QUAN VẬN HÀNH TUẦN W38:",
        speech_paragraphs=[
            "Kính chào Ban Giám Đốc và toàn thể anh chị em Quản lý Vận hành (AM) vùng Nam Trung Bộ. Em xin phép báo cáo kết quả vận hành tuần W38 (từ 14/09 đến 20/09/2026). Tuần này toàn vùng có 4 điểm chính cần nhìn nhận thẳng thắn:",
            "• 1. Quy mô sản lượng: Sau tuần 9.9 bùng nổ, tuần này sản lượng giao toàn vùng hạ nhiệt nhẹ về 345.994 đơn (giảm -11.255 đơn, tương ứng -3,2% WoW). Điểm tích cực là mảng TikTok Shop vẫn giữ nhịp tăng trưởng, đạt 69.274 đơn (+0,8% WoW), chiếm tròn 20,0% tổng sản lượng của cả vùng.",
            "• 2. Chất lượng giao đúng hẹn: %ODR Full hàng đạt 91,2% và TikTok Shop đạt 91,5%. Tuy chưa đạt mốc 92% kỳ vọng nhưng vẫn giữ được ngưỡng trên 91% nhờ chặng lấy hàng (LTC) kênh TikTok tuần này làm rất tốt, đạt đỉnh 95,4%.",
            "• 3. Điểm nghẽn giao hàng Last-mile: Tỷ lệ giao thành công (%GTC Tổng) tụt xuống 55,75% (giảm -2,03%p so với W37). Vấn đề là ca sáng anh em giao đạt trên 68% - 71%, nhưng sang ca chiều thì hụt hơi rõ rệt, kéo cả ngày đi xuống.",
            "• 4. Hai rủi ro chi phí lớn phát sinh trong tuần: Thứ nhất, hiệu suất xe tải KTC giảm xuống 51,0% với 76 chuyến chạy non tải dưới 30% thùng. Thứ hai, số tiền truy thu tuần này tăng vọt lên tới 282,4 triệu đồng (tăng thêm 241 triệu so với W37), tập trung hơn một nửa tại Lâm Đồng do các bưu cục nhận hàng không kiểm soát cân nặng kích thước."
        ],
        insights=[
            "TikTok Shop chiếm 20% sản lượng toàn vùng, trở thành kênh doanh thu bắt buộc phải ưu tiên hàng đầu về tốc độ xử lý.",
            "Nghịch lý vận hành: Khâu lấy hàng và giao ca 1 làm rất đạt, nhưng khâu gom tải KTC và ca giao chiều bị hụt, làm xói mòn hiệu quả của cả chuỗi."
        ],
        warnings=[
            "76 chuyến xe tải KTC chạy non tải dưới 30% đang trực tiếp làm đội chi phí vận chuyển đường trục.",
            "Tiền truy thu 282,4 triệu đồng nếu không thu hồi kịp thời sẽ biến thành tổn thất tài chính và nợ xấu của khu vực."
        ],
        actions=[
            "Tuần W39 siết lại kỷ luật 3 khâu: Giám sát ca giao chiều, điều phối ghép chuyến xe tải KTC và kiểm soát cân đo ngay tại bàn nhận hàng bưu cục."
        ]
    )

    # 2. SẢN LƯỢNG 5 TỈNH
    add_callout_box(
        doc,
        section_title="📦 [II. PHÂN TÍCH SẢN LƯỢNG GIAO TOÀN VÙNG, 5 TỈNH THÀNH & 18 AM (W38)]",
        speech_title="🗣️ PHÂN TÍCH SẢN LƯỢNG GIAO 5 TỈNH & BIẾN ĐỘNG THEO AM:",
        speech_paragraphs=[
            "Kính thưa Ban Giám Đốc, nhìn vào số liệu sản lượng thực tế của 5 tỉnh tuần W38:",
            "• 1. Khánh Hòa — Tỉnh duy nhất giữ được đà tăng trưởng dương: Đạt 96.012 đơn (tăng +2.828 đơn so với W37 93.184 đơn, +3,0% WoW). Mảng TTS đạt 18.142 đơn. Khánh Hòa đã vượt qua Lâm Đồng để vươn lên thành địa bàn có sản lượng giao lớn nhất vùng trong tuần 38.",
            "• 2. Lâm Đồng — Giảm nhẹ sau đợt cao điểm: Đạt 95.727 đơn (W37: 99.384 đơn, giảm -3.657 đơn, -3,7% WoW). Tuy nhiên về mảng TikTok Shop, Lâm Đồng vẫn dẫn đầu toàn vùng với 19.587 đơn (tăng +942 đơn WoW).",
            "• 3. Bình Thuận: Đạt 85.489 đơn (W37: 90.964 đơn, giảm -5.475 đơn, -6,0% WoW). Mảng TTS đạt 15.873 đơn (+157 đơn WoW).",
            "• 4. Đắk Nông: Đạt 34.848 đơn (W37: 38.189 đơn, giảm -3.341 đơn, -8,7% WoW). TTS đạt 8.314 đơn (-343 đơn WoW).",
            "• 5. Ninh Thuận: Đạt 33.918 đơn (W37: 35.528 đơn, giảm -1.610 đơn, -4,5% WoW). TTS đạt 7.358 đơn (đi ngang so với tuần trước).",
            "Về phía các AM: AM Nguyễn Duy Long và AM Lê Văn Trường tiếp tục quản lý các cụm địa bàn có tải lớn nhất. Tuy nhiên tại Đắk Nông và Lâm Đồng, một số bưu cục vùng sâu bị ảnh hưởng bởi thời tiết mưa chiều, dẫn đến lượng đơn giao thành công trong ngày bị chậm lại."
        ],
        insights=[
            "Khánh Hòa giữ nhịp giao nhận rất tốt nhờ các tuyến nội thành Nha Trang và Cam Ranh khai thác đều tay, bù đắp được khoảng sụt giảm của các tỉnh Tây Nguyên.",
            "Sản lượng TikTok Shop toàn vùng không giảm mà tăng nhẹ +0,8%, khẳng định lượng khách mua hàng online vẫn rất ổn định."
        ],
        warnings=[
            "Đắk Nông có mức giảm sản lượng sâu nhất vùng (-8,7%), cần rà soát xem có tình trạng shop gửi hàng chuyển sang nhà xe địa phương hay không."
        ],
        actions=[
            "AM Đắk Nông và Bình Thuận làm việc lại với các bưu cục trực thuộc để nắm sát nguồn hàng từ các đối tác lớn, không để sót đơn."
        ]
    )

    # 3. %GTC TỔNG
    add_callout_box(
        doc,
        section_title="🎯 [III. PHÂN TÍCH HIỆU SUẤT %GTC TỔNG TOÀN MẠNG THEO 18 AM & 5 TỈNH (W38)]",
        speech_title="🗣️ ĐÁNH GIÁ TỶ LỆ GIAO THÀNH CÔNG (%GTC) VÀ ĐỘ LỆCH THEO TỈNH:",
        speech_paragraphs=[
            "Kính thưa Ban Giám Đốc, về tỷ lệ Giao Thành Công (%GTC Tổng):",
            "Tuần W38, %GTC Full hàng toàn vùng đạt 55,75% và TikTok Shop đạt 54,01%. So với tuần W37 (57,78%), toàn vùng đang bị tụt mất -2,03%p.",
            "Nhìn vào mặt bằng 5 tỉnh:",
            "• Khánh Hòa tiếp tục dẫn đầu vùng về tỷ lệ GTC, đạt 58,9%.",
            "• Bình Thuận bám sát phía sau với 57,2%.",
            "• Ba tỉnh còn lại đang kéo tụt mặt bằng chung: Ninh Thuận đạt 55,1%, Đắk Nông đạt 54,1%, và thấp nhất là Lâm Đồng chỉ đạt 53,8%.",
            "Thực tế kiểm tra tại các bưu cục cho thấy: Tỷ lệ khách hẹn giao lại chiếm tới 18% lượng đơn không phát được. Shipper gọi điện khi khách bận hoặc đi làm chưa về, nhưng buổi chiều lại không đi phát lại mà mang thẳng về kho."
        ],
        insights=[
            "Lâm Đồng là địa bàn có lượng đơn lớn nhất nhì vùng nhưng tỷ lệ GTC lại thấp nhất (53,8%), chứng tỏ khâu điều phối tuyến giao tại đây đang có vấn đề tồn đọng."
        ],
        warnings=[
            "%GTC dưới 56% đồng nghĩa với việc cứ 100 đơn xuất kho thì có tới 44 đơn phải xử lý lại, làm tăng gấp đôi chi phí giao nhận và nhân công kho."
        ],
        actions=[
            "Yêu cầu các AM có %GTC dưới 55% (đặc biệt là cụm Lâm Đồng, Đắk Nông) rà soát lại năng suất giao của từng shipper, lập danh sách các tuyến có tỷ lệ hẹn lùi cao để điều chỉnh giờ phát."
        ]
    )

    # 4. GTC CA 1 TTS
    add_callout_box(
        doc,
        section_title="🔥 [IV. PHÂN TÍCH CHUYÊN SÂU %GTC CA 1 TIKTOK SHOP (TARGET SLA ≥ 76.0%) (W38)]",
        speech_title="🗣️ MỔ XẺ CHÊNH LỆCH GIAO HÀNG GIỮA CA 1 VÀ CA 2 TIKTOK SHOP:",
        speech_paragraphs=[
            "Kính thưa Ban Giám Đốc, khi bóc tách số liệu giao hàng của riêng kênh TikTok Shop, chúng ta thấy một sự lệch pha rất rõ giữa ca sáng và ca chiều:",
            "• Ở Ca 1 sáng (hàng đi phát từ 08h00): Tỷ lệ giao thành công thuần của TTS đạt tới 71,36% (toàn mạng đạt 68,4% - 71,4%). Đây là mức giao rất tốt, chứng minh shipper đầu giờ sáng đi tuyến rất hăng hái và tập trung.",
            "• Nhưng sang Ca 2 chiều (hàng đi phát từ 14h00): Tỷ lệ thành công lập tức rơi tự do xuống chỉ còn khoảng 40% đến 53%.",
            "Chính sự sụt giảm nghiêm trọng của ca chiều đã kéo tỷ lệ GTC cả ngày của TikTok Shop xuống mức 54,01%.",
            "Nguyên nhân thực tế tại các bưu cục: Buổi sáng shipper gom hết các đơn dễ, đơn gần để phát trước cho kịp số. Đến buổi chiều gặp các đơn khó, khách hẹn giờ muộn hoặc địa chỉ xa thì anh em ngại đi lại lần hai, có tâm lý dồn hàng để sáng mai đi một thể."
        ],
        insights=[
            "Trưởng bưu cục chưa theo dõi sát tiến độ giao buổi chiều. Từ 15h30 đến 17h30 là khung giờ khách hàng đi làm về, tỷ lệ nhận hàng rất cao nhưng lại không có shipper trên tuyến."
        ],
        warnings=[
            "Đơn TikTok Shop để trôi sang ngày thứ hai rất dễ bị khách bấm hủy trên app, làm tăng tỷ lệ hoàn trả oan uổng."
        ],
        actions=[
            "Bắt buộc Trưởng bưu cục phải kiểm soát ca chiều: Yêu cầu shipper gọi lại lần 2 cho toàn bộ các đơn gọi nhỡ buổi sáng trước khi kết thúc ca làm việc lúc 18h00."
        ]
    )

    # 5. TỶ LỆ GÁN
    add_callout_box(
        doc,
        section_title="📋 [V. TỶ LỆ GÁN VẬN HÀNH TOÀN MẠNG THEO CA 1, CA 2 & GÁN TỔNG (TARGET ≥ 90.0%) (W38)]",
        speech_title="🗣️ KIỂM TRA TỶ LỆ GÁN ĐƠN XUẤT KHO VÀ ĐIỂM TỒN CA TRƯA:",
        speech_paragraphs=[
            "Kính thưa Ban Giám Đốc, tỷ lệ gán đơn giao phản ánh trực tiếp việc hàng về kho có được đưa ra đường hay không:",
            "• Gán Ca 1 + Tồn đầu ngày: Toàn vùng làm khá ổn định, đạt 85,9% đối với Full hàng và 85,5% đối với TikTok Shop.",
            "• Điểm nghẽn nằm ở Gán Ca 2: Toàn vùng chỉ đạt vỏn vẹn 56,8% với Full hàng và 53,4% với TikTok Shop (thấp hơn rất nhiều so với ngưỡng quy định là 90%).",
            "Hệ quả là tính chung cả ngày, tỷ lệ gán tổng toàn mạng chỉ đạt 80,6% (TTS đạt 80,2%). Gần 20% lượng đơn hàng về bưu cục trong ngày không được gán cho shipper mang đi giao.",
            "Thực tế tại kho: Xe KTC chuyển hàng về bưu cục tầm 12h30 - 13h30. Lúc này nhân viên bưu cục nghỉ trưa, hàng nằm trên sàn chưa kịp bắn phân loại. Đến 14h30 shipper chuẩn bị đi ca chiều thì hàng mới chưa sẵn sàng, nên anh em chỉ mang lượng đơn còn lại của ca sáng đi giao."
        ],
        insights=[
            "Khâu chia chọn ca trưa tại bưu cục đang bị đứt quãng. Hàng về nhưng không có người quét gán kịp thời trước giờ shipper xuất tuyến ca chiều."
        ],
        warnings=[
            "Đơn hàng tồn lại kho bưu cục qua đêm làm chật chội sàn thao tác, dễ lẫn lộn và trực tiếp làm giảm tỷ lệ đúng hẹn %ODR của ngày hôm sau."
        ],
        actions=[
            "Bố trí lại ca làm việc tại bưu cục: Cắt cử tối thiểu 1 nhân viên kho trực bắn hàng từ 12h30 đến 13h30, đảm bảo 100% hàng ca trưa phải sẵn sàng trên kệ trước 14h00 để gán cho shipper."
        ]
    )

    # 6. %ODR ĐÚNG HẸN
    add_callout_box(
        doc,
        section_title="⏱️ [VI. PHÂN TÍCH HIỆU SUẤT %ODR (GIAO ĐÚNG HẸN SLA) TOÀN VÙNG (TARGET ≥ 92.0%) (W38)]",
        speech_title="🗣️ CHẤT LƯỢNG ĐÚNG HẸN %ODR VÀ NGUYÊN NHÂN TRỄ TUYẾN:",
        speech_paragraphs=[
            "Kính thưa Ban Giám Đốc, về chỉ số Giao Đúng Hẹn (%ODR) theo cam kết SLA:",
            "Tuần W38 toàn vùng đạt 91,2% với Full hàng và 91,5% với TikTok Shop. Khoảng cách đến mục tiêu 92,0% chỉ còn khoảng 0,5% đến 0,8%p.",
            "Phân tích các tỉnh:",
            "• Khánh Hòa đạt tốt nhất vùng với 93,1% ODR.",
            "• Bình Thuận giữ vững 92,4%.",
            "• Ba tỉnh chưa đạt mốc 92%: Ninh Thuận đạt 91,0%, Đắk Nông đạt 90,1%, và Lâm Đồng thấp nhất vùng chỉ đạt 89,8%.",
            "Qua rà soát trên các đơn bị trễ hẹn: Hơn 60% nguyên nhân xuất phát từ việc xe tải KTC chuyển hàng về bưu cục huyện muộn hơn lịch trình (sau 10h sáng). Thời gian còn lại trong ngày không đủ để shipper chạy hết các tuyến đường đồi dốc vùng ven."
        ],
        insights=[
            "Chỉ cần bưu cục nhận được hàng sớm hơn 45 phút vào đầu giờ sáng, tỷ lệ %ODR của các tuyến huyện sẽ tự động tăng thêm từ 1,5% đến 2,0%p."
        ],
        warnings=[
            "Sàn TikTok Shop kiểm soát thời gian giao hàng rất ngặt nghèo; nếu ODR dưới 90% thì shop bán hàng sẽ bị trừ điểm vận hành và giảm lượng đơn chia sẻ cho GHN."
        ],
        actions=[
            "Ban Vận tải rà soát lại giờ xuất bến xe KTC buổi sáng; bưu cục ưu tiên chia chọn và phát trước các kiện hàng có gắn cảnh báo SLA cận giờ."
        ]
    )

    # 7. %LTC LẤY HÀNG
    add_callout_box(
        doc,
        section_title="🚚 [VII. PHÂN TÍCH CHỈ SỐ %LTC (LẤY THÀNH CÔNG) THEO 18 AM & 5 TỈNH (TARGET ≥ 90.0%) (W38)]",
        speech_title="🗣️ ĐIỂM SÁNG FIRST-MILE: %LTC TIKTOK SHOP ĐẠT ĐỈNH 95.4%:",
        speech_paragraphs=[
            "Kính thưa Ban Giám Đốc, điểm sáng và đáng khích lệ nhất của tuần W38 nằm ở khâu Lấy hàng thành công (%LTC):",
            "• Toàn vùng đạt %LTC Full hàng 90,4%, và đặc biệt kênh TikTok Shop bứt phá lên 95,4% — đây là mức cao nhất của vùng Nam Trung Bộ trong vòng 8 tuần gần đây.",
            "• Cả 5 trên 5 tỉnh đều vượt mốc chỉ tiêu 90%: Khánh Hòa dẫn đầu đạt 96,2%; Lâm Đồng đạt 95,1%; Bình Thuận đạt 95,8%; Đắk Lắk đạt 94,8%; và Đắk Nông đạt 94,3%.",
            "Kết quả này có được là nhờ anh em điều phối lấy hàng tuần qua đã liên hệ chặt chẽ với các shop lớn, chủ động hẹn giờ gom hàng trước 16h30, không để tình trạng dồn ứ đơn lấy vào cuối ngày như các tuần trước."
        ],
        insights=[
            "Mô hình hẹn giờ lấy cố định và cho xe bán tải gom trực tiếp tại các kho hàng lớn đã phát huy hiệu quả rõ rệt, giảm hẳn tình trạng shop báo hủy đơn lấy."
        ],
        warnings=[
            "Tuần tới chuẩn bị bước vào đợt sale lương về cuối tháng, sản lượng lấy có thể tăng vọt 30-40%, nếu không giữ vững nhịp này sẽ rất dễ vỡ trận lấy hàng."
        ],
        actions=[
            "Duy trì cơ chế điều xe gom hàng sớm; các AM chuẩn bị sẵn danh sách shipper dự phòng để tăng cường lấy hàng cho các shop livestream lớn."
        ]
    )

    # 8. %OPR TTS
    add_callout_box(
        doc,
        section_title="🌙 [VIII. PHÂN TÍCH CHỈ SỐ %OPR TIKTOK SHOP TOÀN VÙNG (TARGET KPI ≥ 80.0%) (W38)]",
        speech_title="🗣️ ĐÁNH GIÁ HIỆU SUẤT %OPR TIKTOK SHOP CA NGÀY VÀ CA ĐÊM:",
        speech_paragraphs=[
            "Kính thưa Ban Giám Đốc, về chỉ số xử lý đơn hàng TikTok Shop (%OPR toàn vùng):",
            "Mặt bằng chung tuần W38 đạt 82,3%, cơ bản hoàn thành mục tiêu KPI ≥ 80%. Tuy nhiên, giữa ca ngày và ca đêm đang có sự chênh lệch rất lớn:",
            "• Ca ngày: Các tỉnh làm rất tốt, đạt từ 82,8% đến 94,8% (Khánh Hòa đạt 94,8%, Bình Thuận đạt 92,1%, Lâm Đồng đạt 82,8%).",
            "• Ca đêm: Hiệu suất bị tụt sâu, đặc biệt tại Lâm Đồng ca đêm chỉ đạt 46,1% (giảm -5,6%p so với tuần trước 51,7%), kéo tỷ lệ OPR chung của cả tỉnh Lâm Đồng xuống mức 70,3%. Trong khi đó, Bình Thuận làm ca đêm đạt 84,7% và Khánh Hòa đạt 77,8%.",
            "Thực tế tại kho trung chuyển Lâm Đồng: Lực lượng bốc xếp và phân loại ban đêm mỏng, trong khi hàng đêm đổ về nhiều khiến hàng bị nằm chờ trên sàn đến tận sáng hôm sau mới được xử lý."
        ],
        insights=[
            "Ca đêm tại Lâm Đồng đang là nút thắt làm chậm dòng chảy hàng hóa; hàng về đêm nhưng không quét nhập kho kịp thời khiến shipper sáng hôm sau bị chậm giờ xuất tuyến."
        ],
        warnings=[
            "OPR ca đêm dưới 50% làm lãng phí toàn bộ thời gian vận chuyển ban đêm, biến các đơn hàng hỏa tốc thành đơn giao trễ."
        ],
        actions=[
            "Yêu cầu Quản lý vận hành Lâm Đồng điều chỉnh lại lịch trực: Tăng cường thêm nhân sự bốc xếp cho ca đêm từ 22h00 đến 04h00 sáng để giải tỏa dứt điểm hàng trước 06h00."
        ]
    )

    # 9. RỚT LUÂN CHUYỂN
    add_callout_box(
        doc,
        section_title="⚠️ [IX. PHÂN TÍCH TỶ TRỌNG RỚT ĐƠN LUÂN CHUYỂN THEO AM & TỈNH THÀNH (W38)]",
        speech_title="🗣️ CẢNH BÁO TỶ LỆ RỚT ĐƠN LUÂN CHUYỂN TĂNG VỌT LÊN 3.32%:",
        speech_paragraphs=[
            "Kính thưa Ban Giám Đốc, một chỉ số vận hành đang xấu đi rõ rệt trong tuần W38 là Tỷ lệ Rớt Đơn Luân Chuyển:",
            "• Toàn vùng tuần này tăng vọt lên 3,32% (trong khi tuần W37 chỉ có 1,80%, tăng thêm +1,52%p). Trong tổng số 7.586 đơn cần luân chuyển thì có tới 252 đơn bị rớt lại không đi được theo chuyến xe quy định.",
            "• Đáng chú ý, có 3 bưu cục ghi nhận tỷ lệ rớt luân chuyển lên tới 100%: (DNO) Quảng Sơn (AM Trần Thị Nhung), (NTH) Thuận Nam (AM Nguyễn Duy Long), và (LDO) Lang Biang - Đà Lạt 1 (AM Lê Minh Lợi).",
            "Kiểm tra thực tế: Nhân viên bưu cục đóng túi seal muộn, tài xế xe tải đến đúng giờ không kịp chờ nên phải chạy rỗng; hoặc nhân viên bưu cục bàn giao thiếu sót, để bao hàng nằm góc kho mà không quét lên xe."
        ],
        insights=[
            "Ý thức tuân thủ giờ cắt hàng (Cut-off time) tại một số bưu cục huyện đang bị buông lỏng; thiếu sự phối hợp chặt chẽ giữa nhân viên bưu cục và tài xế xe tải."
        ],
        warnings=[
            "Hàng rớt luân chuyển sẽ bị chậm ít nhất 24 giờ, làm tăng tỷ lệ khiếu nại và tiềm ẩn rủi ro thất lạc hàng hóa rất cao."
        ],
        actions=[
            "Quy định rõ trách nhiệm: Bưu cục nào để rớt hàng chuyến xe KTC mà không có lý do chính đáng, Trưởng bưu cục phải chịu trách nhiệm giải trình và xử lý kỷ luật theo quy chế."
        ]
    )

    # 10. %FD HOÀN TRẢ
    add_callout_box(
        doc,
        section_title="🔄 [X. BÁO CÁO TỶ LỆ %FD (RETURN / HOÀN TRẢ) — VÙNG NAM TRUNG BỘ (W38)]",
        speech_title="🗣️ PHÂN TÍCH TỶ LỆ HOÀN TRẢ (%FD 7.74%) VÀ TOP BƯU CỤC BẤT THƯỜNG:",
        speech_paragraphs=[
            "Kính thưa Ban Giám Đốc, về tỷ lệ hàng Hoàn trả (%FD toàn mạng):",
            "Tuần W38 ghi nhận 26.531 đơn hoàn trên tổng số 342.727 đơn xử lý, tỷ lệ hoàn trả trung bình là 7,74%. Con số này nhìn chung vẫn nằm trong ngưỡng kiểm soát cho phép (dưới 8%).",
            "Tuy nhiên, khi soi vào từng bưu cục thì có 3 điểm đen có tỷ lệ hoàn cao bất thường:",
            "• 1. (DNO) Quảng Tín (AM Trương Quang Linh): Tỷ lệ hoàn lên tới 37,89% (770 đơn hoàn trên 2.032 đơn giao). Đây là tỷ lệ cao không thể chấp nhận được.",
            "• 2. (LDO) Lang Biang - Đà Lạt 1 (AM Trần Tấn Lợi): Tỷ lệ hoàn 20,30% (625 đơn hoàn trên 3.079 đơn).",
            "• 3. (KHO) Cam Linh (AM Nguyễn Thanh Long): Tỷ lệ hoàn 16,96% (988 đơn hoàn trên 5.825 đơn).",
            "Qua kiểm tra nghiệp vụ, tại bưu cục Quảng Tín và Cam Linh có dấu hiệu shipper lười phát các tuyến xa, tự ý bấm cập nhật trạng thái 'Khách từ chối nhận' hoặc 'Không liên lạc được 3 lần' để đẩy hàng về trạng thái hoàn trả."
        ],
        insights=[
            "Việc shipper tự ý bấm hoàn ảo để xả tải cá nhân đang gây thiệt hại trực tiếp cho các shop bán hàng và làm tăng chi phí vận chuyển ngược của công ty."
        ],
        warnings=[
            "Các shop lớn bị hoàn tỷ lệ trên 20% sẽ lập tức cắt hợp đồng và chuyển sang đối thủ cạnh tranh."
        ],
        actions=[
            "Phòng Thanh tra / QC gọi điện phúc tra ngẫu nhiên 100% các đơn hoàn trả tại Quảng Tín và Cam Linh; nếu phát hiện shipper khai báo gian dối sẽ xử lý sa thải ngay lập tức."
        ]
    )

    # 11. KTC & VẬN TẢI
    add_callout_box(
        doc,
        section_title="🚛 [XI. BÁO CÁO ĐIỀU HÀNH KTC, VẬN TẢI, %TLTĐ THÙNG XE (51.0%) & LEADTIME KHO (W38)]",
        speech_title="🗣️ HIỆU QUẢ VẬN TẢI KTC VÀ XỬ LÝ 76 CHUYẾN XE CHẠY NON TẢI:",
        speech_paragraphs=[
            "Kính thưa Ban Giám Đốc, về khâu Vận tải đường dài và Kho trung chuyển KTC:",
            "Tuần W38 toàn mạng lưới chạy 538 chuyến xe KTC kết nối các kho. Chỉ số Tỷ lệ lấp đầy thùng xe (%TLTĐ KTC) giảm mạnh về mức 51,0% (giảm -3,8%p so với tuần W37 54,8%).",
            "Đáng chú ý nhất: Hệ thống phát hiện có tới 76 chuyến xe xuất bến với tỷ lệ lấp đầy thùng dưới 30%! Chúng ta đang tốn tiền dầu, tiền cước xe nguyên chuyến nhưng thực tế thùng xe chỉ chở được một phần ba tải trọng.",
            "Ngoài ra, các hợp đồng xe thuê ngoài (như đối tác Mạnh Cường với các đầu xe bưu cục chuyển phát chi phí từ 22 đến 31 triệu/tháng) cần phải đánh giá lại hiệu quả từng tuyến để xem xét cắt giảm hoặc gom tuyến cho phù hợp."
        ],
        insights=[
            "Biểu đồ chạy xe KTC hiện đang cố định theo giờ mà chưa linh hoạt theo lượng hàng thực tế của từng ngày trong tuần."
        ],
        warnings=[
            "Chạy xe non tải đường dài là khoản lãng phí chi phí lớn nhất của khối vận hành trong tuần vừa qua."
        ],
        actions=[
            "Ban Vận tải tiến hành rà soát ngay 76 chuyến xe non tải dưới 30%: Tuyến nào sản lượng thấp thì chuyển sang xe tải nhỏ hơn hoặc gộp 2 tuyến làm một để đưa tỷ lệ lấp đầy quay lại trên 55%."
        ]
    )

    # 12. HÀNG AGING TỒN ĐỌNG
    add_callout_box(
        doc,
        section_title="⏳ [XII. ĐIỀU HÀNH XỬ LÝ HÀNG AGING TỒN ĐỌNG & TREO LUÂN CHUYỂN]",
        speech_title="🗣️ XỬ LÝ 1.638 ĐƠN HÀNG TỒN AGING TRÊN 5 NGÀY TẠI CÁC BƯU CỤC:",
        speech_paragraphs=[
            "Kính thưa Ban Giám Đốc, về tình hình hàng tồn lâu ngày (Aging >5 ngày):",
            "Hiện toàn vùng còn 1.638 đơn hàng tồn trên 5 ngày chưa được giải phóng. Cụ thể:",
            "• Tồn từ 5 đến 8 ngày: 1.196 đơn.",
            "• Tồn từ 8 đến 15 ngày: 416 đơn.",
            "• Tồn nguy hiểm trên 15 ngày: 26 đơn.",
            "Số lượng hàng tồn aging này tập trung chủ yếu ở 3 bưu cục trọng điểm:",
            "1. (DNO) Quảng Tín: 367 đơn (chiếm 22,4% toàn vùng).",
            "2. (LDO) Đức Trọng 1: 318 đơn (chiếm 19,4%).",
            "3. (LDO) Xuân Hương - Đà Lạt: 247 đơn (chiếm 15,1%).",
            "Chỉ riêng 3 bưu cục này đã chiếm gần 60% tổng lượng hàng ngâm lâu của cả vùng. Hàng chủ yếu là các đơn khách hẹn nhiều lần, đơn sai số điện thoại hoặc hàng chờ xử lý đền bù nhưng không được cập nhật dứt điểm lên hệ thống."
        ],
        insights=[
            "Bưu cục thiếu thói quen kiểm kê sàn cuối ngày; hàng khó phát thường bị gạt sang một góc và để trôi nổi từ ngày này qua ngày khác."
        ],
        warnings=[
            "Hàng tồn trên 8 ngày có tỷ lệ giao thành công dưới 5% và nguy cơ mất mát, hư hỏng dẫn đến đền bù là rất cao."
        ],
        actions=[
            "Các AM phụ trách trực tiếp xuống 3 bưu cục Quảng Tín, Đức Trọng 1 và Xuân Hương: Phân loại dứt điểm 442 đơn tồn trên 8 ngày trong vòng 48 giờ tới (giao dứt điểm hoặc bấm hoàn trả theo đúng quy định)."
        ]
    )

    # 13. QUẢN TRỊ COD
    add_callout_box(
        doc,
        section_title="💰 [XIII. QUẢN TRỊ DÒNG TIỀN COD, TỶ LỆ THANH TOÁN & THU HỒI CÔNG NỢ]",
        speech_title="🗣️ KIỂM SOÁT THU TIỀN COD (84.4 TỶ ₫) VÀ NGUY CƠ TỒN QUỸ TIỀN MẶT:",
        speech_paragraphs=[
            "Kính thưa Ban Giám Đốc, về mảng Thu hộ tiền COD và Quản trị dòng tiền:",
            "Tuần W38, tổng số tiền COD toàn vùng thu hộ là 84.441,1 triệu đồng (khoảng 84,4 tỷ đồng, giảm -6,6% phù hợp với đà giảm sản lượng).",
            "Tuy nhiên, cơ cấu thu tiền lại đang biến động theo hướng không an toàn:",
            "• Tỷ lệ thu bằng Tiền mặt tăng từ 40,2% lên 43,1% (tăng +3,0%p), tương ứng hơn 36,4 tỷ đồng tiền mặt nằm trong tay shipper và két sắt bưu cục.",
            "• Ngược lại, tỷ lệ Chuyển khoản QR Code giảm từ 59,8% xuống còn 56,9% (-3,0%p).",
            "Lượng tiền mặt luân chuyển tăng thêm 3% tạo ra áp lực rất lớn cho công tác nộp tiền về tài khoản công ty cuối ngày, đồng thời làm tăng rủi ro thất thoát hoặc giữ tiền chậm nộp của shipper."
        ],
        insights=[
            "Một số shipper mới chưa hướng dẫn khách thanh toán QR qua app, hoặc bưu cục chưa in sẵn bảng mã QR cho shipper cầm theo tuyến."
        ],
        warnings=[
            "Tiền mặt tồn đọng tại bưu cục qua đêm là rủi ro an ninh rất lớn, vi phạm quy định quản lý tài chính của công ty."
        ],
        actions=[
            "Yêu cầu 100% bưu cục trang bị thẻ quét mã QR cho shipper; đặt mục tiêu kéo tỷ lệ chuyển khoản QR của vùng quay lại mức trên 60% trong tuần W39."
        ]
    )

    # 14. TRUY THU
    add_callout_box(
        doc,
        section_title="🚨 [XIV. BÁO CÁO TRUY THU – BIẾN ĐỘNG 2 TUẦN (W37 vs W38) & CẢNH BÁO BÙNG PHÁT 282.4 TRIỆU ₫]",
        speech_title="🗣️ CẢNH BÁO ĐỘT BIẾN TRUY THU: TĂNG VỌT LÊN 282.4 TRIỆU ĐỒNG (+241 TRIỆU WoW):",
        speech_paragraphs=[
            "Kính thưa Ban Giám Đốc, đây là nội dung cảnh báo nghiêm trọng nhất trong tuần W38:",
            "Số tiền truy thu toàn vùng đã tăng vọt từ 41,4 triệu đồng ở tuần W37 lên tới 282,4 triệu đồng tại tuần W38 — tức là tăng thêm tới +241,0 triệu đồng chỉ trong vòng một tuần, phát sinh trên 3.074 đơn hàng bị phát hiện sai lệch cước.",
            "Tập trung ở đâu?",
            "• Lâm Đồng chiếm tới 55% tổng tiền truy thu toàn vùng (hơn 155 triệu đồng, với 1.680 đơn).",
            "• Khánh Hòa chiếm 24% (hơn 68 triệu đồng, với 740 đơn).",
            "• Hai tỉnh này cộng lại đã chiếm gần 80% số tiền truy thu của cả vùng!",
            "Về nguyên nhân: 78,5% số tiền truy thu (hơn 221 triệu đồng) xuất phát từ lỗi 'Sai lệch trọng lượng và kích thước thực tế'. Hàng của shop gửi cồng kềnh, nặng 2-3 kg nhưng bưu cục nhận chỉ ghi nhận 500g để lấy cước rẻ."
        ],
        insights=[
            "Lỗi nằm trực tiếp ở khâu tiếp nhận hàng tại bưu cục: Giao dịch viên nể nang shop quen, không đưa hàng lên bàn cân đo hoặc cố tình bỏ qua sai số để giữ chân shop."
        ],
        warnings=[
            "Nếu hệ thống không truy thu được khoản tiền 282,4 triệu này từ shop, công ty sẽ chịu thiệt hại trực tiếp và trách nhiệm đền bù sẽ truy ngược về nhân viên nhận hàng."
        ],
        actions=[
            "Mệnh lệnh khẩn cấp: Bắt buộc 100% bưu cục gửi hàng phải đưa bưu kiện lên cân đo đúng quy chuẩn; phối hợp với bộ phận Kế toán truy thu dứt điểm số tiền chênh lệch của các shop vi phạm trong tuần W39."
        ]
    )

    # 15. KINH DOANH
    add_callout_box(
        doc,
        section_title="📈 [XV. PHÂN TÍCH DOANH THU KINH DOANH & TĂNG TRƯỞNG KHÁCH HÀNG MỚI (F30) | VÙNG NTB]",
        speech_title="🗣️ DOANH THU KINH DOANH ĐẠT 1.168 TỶ ₫, PHÁT TRIỂN SHOP MỚI F30 & TOP SHOP A:",
        speech_paragraphs=[
            "Kính thưa Ban Giám Đốc, về kết quả hoạt động Kinh doanh tuần W38:",
            "• Tổng doanh thu đạt 1.168,2 triệu đồng (tăng +1,6% WoW so với tuần trước 1.149,8 triệu đồng). Dù sản lượng tạo đơn giảm nhẹ nhưng doanh thu vẫn tăng nhờ giá trị cước bình quân trên mỗi đơn được cải thiện.",
            "• Khách hàng mới F30: Tuần qua toàn vùng mang về 111 shop mới, đóng góp 17,7 triệu đồng doanh thu ban đầu.",
            "• Quản trị khách hàng lớn nhóm A: Doanh thu lũy kế tháng MTD của top 10 shop nhóm A đạt 43.254 triệu đồng.",
            "Tuy nhiên có một rủi ro cần lưu ý: Hệ thống ghi nhận 3 khách hàng lớn trong nhóm A có sản lượng giảm trên 30% so với tuần trước. Lý do shop phản ánh là thời gian giao hàng tại một số tuyến huyện bị chậm, làm ảnh hưởng đến tỷ lệ đánh giá gian hàng của họ."
        ],
        insights=[
            "Chất lượng vận hành Last-mile đang ảnh hưởng trực tiếp đến doanh số kinh doanh; bưu cục giao trễ là shop lập tức chia sẻ đơn sang đơn vị vận chuyển khác."
        ],
        warnings=[
            "Nếu để mất 3 shop lớn này, khu vực sẽ mất đi khoảng 150 triệu đồng doanh thu mỗi tháng."
        ],
        actions=[
            "AM Kinh doanh phối hợp ngay với AM Vận hành địa bàn đến gặp trực tiếp 3 chủ shop này trong đầu tuần W39 để cam kết lại thời gian giao và giữ chân khách hàng."
        ]
    )

    # 16. BC CẢNH BÁO & KẾT LUẬN W39
    add_callout_box(
        doc,
        section_title="🏁 [XVI. ĐIỀU HÀNH TRỌNG ĐIỂM: 13 BƯU CỤC CẢNH BÁO BẤT ỔN & 5 TRỌNG TÂM HÀNH ĐỘNG TUẦN W39]",
        speech_title="🗣️ DANH SÁCH 13 BƯU CỤC CẢNH BÁO ĐỎ & 5 NHIỆM VỤ TRỌNG TÂM TUẦN W39:",
        speech_paragraphs=[
            "Kính thưa Ban Giám Đốc và các anh chị quản lý, để kết thúc buổi họp giao ban tuần W38, em xin điểm danh 13 bưu cục đang rơi vào danh sách cảnh báo bất ổn của vùng với tổng lượng hàng backlog lên tới 18.020 đơn:",
            "1. (KHO) Cam Linh: Backlog 2.433 đơn (AM Nguyễn Thanh Long)",
            "2. (KHO) Tây Nha Trang: Backlog 2.295 đơn (AM Phan Đình Duy)",
            "3. (LDO) Xuân Hương - Đà Lạt: Backlog 2.165 đơn (AM Lê Văn Trường)",
            "4. (LDO) Đơn Dương: Backlog 2.038 đơn (AM Lê Văn Trường)",
            "5. (LDO) Di Linh: Backlog 1.970 đơn (AM Trầm Hữu Tiến)",
            "6. (DNO) Quảng Tín: Backlog 1.224 đơn (AM Trương Quang Linh)",
            "7. (LDO) Đức Trọng 1: Backlog 1.223 đơn (AM Trầm Hữu Tiến)",
            "8. (DNO) Kiến Đức: Backlog 1.035 đơn (AM Hồng Bích Nga)",
            "9. (LDO) Lang Biang - Đà Lạt 1: Backlog 992 đơn (AM Lê Minh Lợi)",
            "10. (LDO) Lâm Viên - Đà Lạt 2: Backlog 860 đơn (AM Lê Văn Trường)",
            "11. (LDO) Tân Hà Lâm Hà: Backlog 798 đơn (AM Huỳnh Thị Kim Chi)",
            "12. (DNO) Tuy Đức: Backlog 640 đơn (AM Trần Thị Nhung)",
            "13. (DNO) Nhân Cơ: Backlog 347 đơn (AM Huỳnh Thúc Duân)",
            "Để giải quyết dứt điểm các tồn đọng trên, toàn vùng Nam Trung Bộ tập trung thực hiện 5 nhiệm vụ trọng tâm trong tuần W39:",
            "• Nhiệm vụ 1: Siết chặt khâu cân đo tiếp nhận tại bưu cục, xử lý dứt điểm 282,4 triệu đồng tiền truy thu, không để phát sinh sai lệch cước mới.",
            "• Nhiệm vụ 2: Tối ưu lại các tuyến xe tải KTC, cắt giảm hoặc gộp chuyến 76 xe non tải dưới 30% để đưa tỷ lệ lấp đầy quay lại trên 55%.",
            "• Nhiệm vụ 3: AM trực tiếp xuống bưu cục giải tỏa 1.638 đơn tồn Aging >5 ngày (đặc biệt tại Quảng Tín, Đức Trọng 1, Xuân Hương) trước thứ Tư.",
            "• Nhiệm vụ 4: Kiểm soát chặt ca giao chiều, nâng tỷ lệ gán Ca 2 từ 56,8% lên trên 85% để kéo tỷ lệ %GTC toàn vùng vượt mốc 58%.",
            "• Nhiệm vụ 5: Chăm sóc giữ chân 3 khách hàng nhóm A đang giảm đơn và tiếp tục mở rộng thêm các shop mới F30.",
            "Em xin cảm ơn Ban Giám Đốc và các anh chị đã lắng nghe. Kính mong nhận được ý kiến chỉ đạo của Ban Giám Đốc để toàn vùng triển khai ngay từ hôm nay!"
        ],
        insights=[
            "13 bưu cục này đang tập trung hầu hết lượng hàng tồn và rủi ro trễ hẹn của vùng; giải tỏa được 13 bưu cục này là toàn vùng sẽ đạt chuẩn SLA."
        ],
        warnings=[
            "Bưu cục nào nằm cảnh báo quá 3 tuần liên tiếp mà không có chuyển biến sẽ xem xét điều chuyển Trưởng bưu cục."
        ],
        actions=[
            "Các AM có bưu cục trong danh sách cảnh báo phải gửi cam kết tiến độ giải tỏa hàng ngày về cho Ban Giám Đốc trước 19h00."
        ]
    )

    out_docx1 = "KICH_BAN_THUYET_TRINH_W38_INSIGHT_CHUYEN_SAU.docx"
    out_docx2 = "KICH_BAN_THUYET_TRINH_W38_NAM_TRUNG_BO.docx"
    out_docx3 = "KICH_BAN_THUYET_TRINH_W38_INSIGHT_CHUYEN_SAU_CHINH_SUA.docx"
    
    doc.save(out_docx2)
    print(f"Saved: {out_docx2} ({os.path.getsize(out_docx2)} bytes)")
    
    try:
        doc.save(out_docx1)
        print(f"Saved: {out_docx1} ({os.path.getsize(out_docx1)} bytes)")
    except Exception as e:
        print(f"Warning: {out_docx1} is currently open in Word ({e}). Saving to {out_docx3}")
        doc.save(out_docx3)
        print(f"Saved: {out_docx3} ({os.path.getsize(out_docx3)} bytes)")

if __name__ == "__main__":
    build_w38_natural_doc()
