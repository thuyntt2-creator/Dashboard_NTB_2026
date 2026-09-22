import re

path = r"c:\Users\lap4all\Desktop\New folder\scratch\generate_professional_w38_script.py"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. New Section IX
sec_9_new = '''    # =========================================================================
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
    )'''

# 2. New Section XIV
sec_14_new = '''    # =========================================================================
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
    )'''

# 3. New Section XV
sec_15_new = '''    # =========================================================================
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
    )'''

# Replace Section IX
pattern_sec9 = r'    # =========================================================================\s+# 9\. RỚT ĐƠN LUÂN CHUYỂN THEO AM & TỈNH\s+# =========================================================================.*?actions=\[\s+"[^"]+",\s+"[^"]+"\s+\]\s+\)'
content = re.sub(pattern_sec9, sec_9_new, content, flags=re.DOTALL)

# Replace Section XIV
pattern_sec14 = r'    # =========================================================================\s+# 14\. BÁO CÁO TRUY THU \(BIẾN ĐỘNG 2 TUẦN W37 vs W38\)\s+# =========================================================================.*?actions=\[\s+"[^"]+",\s+"[^"]+"\s+\]\s+\)'
content = re.sub(pattern_sec14, sec_14_new, content, flags=re.DOTALL)

# Replace Section XV
pattern_sec15 = r'    # =========================================================================\s+# 15\. DOANH THU & PHÁT TRIỂN SHOP MỚI \(F30\)\s+# =========================================================================.*?actions=\[\s+"[^"]+",\s+"[^"]+"\s+\]\s+\)'
content = re.sub(pattern_sec15, sec_15_new, content, flags=re.DOTALL)

# Update Section XVI references
content = content.replace("1.417 đơn rớt luân chuyển;", "252 đơn rớt luân chuyển (tỷ lệ 3,32%), đặc biệt tại Đức Lập, Đông Gia Nghĩa và Bắc Gia Nghĩa;")
content = content.replace("kéo giảm số tiền truy thu từ 282,4 triệu đồng xuống dưới 40 triệu đồng trong tuần W39.", "đặc biệt tại 6 điểm nóng (Bắc Nha Trang 76,1 Tr, Đam Rông 3 33,3 Tr, KCT Bình Thuận 31,6 Tr, Quảng Tín 24,9 Tr, Kiến Đức 24,2 Tr, Đơn Dương 16,7 Tr); kéo giảm số tiền truy thu từ 282,4 triệu đồng xuống dưới 40 triệu đồng trong tuần W39.")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated scratch/generate_professional_w38_script.py successfully!")
