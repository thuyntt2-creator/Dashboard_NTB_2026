import re, sys

path = r"c:\Users\lap4all\Desktop\New folder\scratch\generate_professional_w38_script.py"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. New Section X: BÁO CÁO HOÀN TRẢ %FD
sec_10_new = '''    # =========================================================================
    # 10. BÁO CÁO HOÀN TRẢ %FD (RETURN)
    # =========================================================================
    add_speech_section(
        doc,
        sec_title="🔄 [X. BÁO CÁO TỶ LỆ %FD (RETURN / HOÀN TRẢ) — VÙNG NAM TRUNG BỘ (W38)]",
        speech_heading="🗣️ PHÂN TÍCH TỶ LỆ HOÀN TRẢ (%FD) VÀ BÓC TÁCH CHI TIẾT 18 AM & 10 BƯU CỤC NÓNG:",
        paragraphs_text=[
            "Kính thưa Ban Giám Đốc, về tỷ lệ Hoàn Trả (%FD) — chỉ số trực tiếp bào mòn biên lợi nhuận của vùng:",
            "• Tổng quan toàn mạng tuần W38: Tỷ lệ %FD Full hàng toàn vùng đạt mức 6,73% (giảm nhẹ -0,81%p WoW so với mức 7,54% của tuần W37). Riêng kênh TikTok Shop đạt 6,10% (giảm -0,70%p WoW). Toàn mạng lưới ghi nhận 24.518 đơn hoàn trả trên tổng số 364.298 đơn giao.",
            "• Phân hóa theo 5 Tỉnh thành:",
            "- Bình Thuận và Ninh Thuận kiểm soát hoàn trả tốt nhất khu vực với tỷ lệ %FD Full lần lượt là 5,82% và 6,10%.",
            "- Khánh Hòa giữ ở mức 6,65%.",
            "- Lâm Đồng ở mức 7,54%.",
            "- Đắk Nông ghi nhận mức hoàn trả cao nhất toàn vùng lên tới 8,12%.",
            "• Điểm danh đích danh các Quản lý Vận hành (AM) có tỷ lệ hoàn trả %FD cao nhất mạng lưới:",
            "1. AM Trương Quang Linh (Đắk Nông) — BÁO ĐỘNG ĐỎ KỶ LỤC SỐ 1: Tỷ lệ hoàn trả %FD Full cao nhất toàn mạng lên tới 37,89% (770 đơn hoàn / 2.032 đơn giao, kênh TTS hoàn 33,33%) — cứ hơn 2,5 đơn giao đi thì có gần 1 đơn bị trả về!",
            "2. AM Trần Tấn Lợi (Lâm Đồng) — BÁO ĐỘNG ĐỎ SỐ 2: Tỷ lệ %FD Full đạt tới 20,30% (625 đơn hoàn / 3.079 đơn giao, TTS hoàn 17,94%).",
            "3. AM Nguyễn Tiến Long (Khánh Hòa): %FD Full đạt 11,51% (1.530 đơn hoàn / 13.293 đơn, TTS hoàn 10,19%).",
            "4. AM Huỳnh Thúc Duân (Đắk Nông): %FD Full đạt 10,20% (493 đơn hoàn / 4.831 đơn).",
            "5. AM Nguyễn Lê Nguyên Vũ (Lâm Đồng): %FD Full đạt 9,82% (1.308 đơn hoàn / 13.322 đơn).",
            "6. AM Trần Thị Nhung (Đắk Nông): %FD Full đạt 9,36%, đặc biệt đây là AM CÓ SỐ LƯỢNG ĐƠN HOÀN KHỔNG LỒ NHẤT NHÓM NGUY CƠ với 2.392 đơn hoàn / 25.557 đơn giao!",
            "7. AM Phan Đình Duy (Khánh Hòa): %FD Full đạt 9,15% với 2.186 đơn hoàn / 23.887 đơn giao.",
            "8. AM Lê Văn Trường (Lâm Đồng): %FD Full đạt 8,13% với 2.273 đơn hoàn / 27.971 đơn giao.",
            "9. AM Nguyễn Hoàng Phi (Khánh Hòa): %FD Full đạt 8,07% với 2.003 đơn hoàn / 24.827 đơn giao.",
            "• So sánh biến động WoW tại Top 10 Bưu cục điểm nóng có tỷ lệ hoàn trả cao nhất toàn vùng:",
            "- Bưu cục (DNO) Quảng Tín (AM Trương Quang Linh): BÁO ĐỘNG ĐỎ CAO NHẤT TOÀN QUỐC khi %FD lên tới 37,89% (770 đơn hoàn / 2.032 đơn giao), tăng vọt +4,37%p WoW so với tuần W37 (33,52%)!",
            "- Bưu cục (LDO) Lang Biang - Đà Lạt 1 (AM Trần Tấn Lợi): %FD đạt 20,30% (625 đơn hoàn / 3.079 đơn), tăng mạnh +4,03%p WoW so với W37 (16,26%).",
            "- Bưu cục (KHO) Cam Linh (AM Nguyễn Tiến Long): %FD đạt 16,96%, là BƯU CỤC CÓ SỐ ĐƠN HOÀN LỚN NHẤT TOÀN VÙNG với 988 đơn hoàn / 5.825 đơn, tăng +2,01%p WoW so với W37 (14,96%).",
            "- Bưu cục (DNO) Kiến Đức (AM Hồng Bích Nga): %FD đạt 15,53% (343 đơn hoàn / 2.209 đơn), mặc dù đã giảm -1,83%p WoW nhưng vẫn nằm trong top nguy cơ.",
            "- Bưu cục (LDO) Đức Trọng 1 (AM Nguyễn Lê Nguyên Vũ): %FD đạt 14,59% (318 đơn hoàn / 2.179 đơn), tăng +2,27%p WoW so với W37 (12,32%).",
            "- Bưu cục (DNO) Đông Gia Nghĩa (AM Huỳnh Thúc Duân): %FD đạt 14,51% (280 đơn hoàn / 1.930 đơn), tăng +1,09%p WoW so với W37 (13,42%).",
            "- Bưu cục (DNO) Tuy Đức (AM Trần Thị Nhung): %FD đạt 12,43% (266 đơn hoàn / 2.140 đơn), tăng +1,02%p WoW so với W37 (11,41%).",
            "- Bưu cục (LDO) Di Linh (AM Nguyễn Lê Nguyên Vũ): %FD BÙNG PHÁT TĂNG ĐỘT BIẾN +5,71%p WoW (từ 6,37% tuần W37 nhảy vọt lên 12,08% tuần W38 với 733 đơn hoàn / 6.068 đơn)! Cơ sở này cần kiểm tra ngay hiện tượng bưu tá ép hoàn hàng loạt.",
            "- Bưu cục (DNO) Trường Xuân (AM Trần Thị Nhung): %FD đạt 11,71% (219 đơn hoàn / 1.870 đơn), tăng +1,98%p WoW.",
            "- Bưu cục (DNO) Quảng Sơn (AM Trần Thị Nhung): %FD đạt 11,08% (215 đơn hoàn / 1.941 đơn), tăng +1,99%p WoW."
        ],
        insights=[
            "Nguyên nhân gốc rễ: Tại các khu vực nông thôn và đồi dốc Đắk Nông và Lâm Đồng, bưu tá ngại đi giao lại lần 2 đối với các địa chỉ xa, vội vàng cập nhật trạng thái 'Khách không nhận' hoặc 'Không liên lạc được' để ép đơn chuyển hoàn.",
            "Thiếu quy trình xác minh hoàn độc lập: Tổ CSKH bưu cục không gọi điện phúc tra lại người mua trước khi duyệt hoàn đơn, dẫn tới tình trạng đơn hàng bị chuyển hoàn oan uổng."
        ],
        warnings=[
            "Mỗi đơn hàng hoàn trả khiến GHN mất 100% doanh thu cước giao đồng thời tốn thêm chi phí vận chuyển ngược chiều và xử lý bồi hoàn.",
            "Tỷ lệ hoàn trả 37,89% tại Quảng Tín và 20,30% tại Lang Biang đang đe dọa trực tiếp uy tín hợp tác giữa GHN và các sàn TMĐT."
        ],
        actions=[
            "Kích hoạt quy trình 'Chặn hoàn 3 lớp' tại Quảng Tín, Lang Biang, Cam Linh, Di Linh: Bắt buộc bưu tá phải có tối thiểu 3 cuộc gọi thành công và 1 tin nhắn định danh trước khi đề xuất hoàn.",
            "Tổ CSKH bưu cục phải thực hiện 100% cuộc gọi xác minh độc lập với người nhận trước khi bấm duyệt lệnh chuyển hoàn về kho trung tâm."
        ]
    )'''

# 2. New Section XIII: QUẢN TRỊ DÒNG TIỀN COD & THU TIỀN MẶT
sec_13_new = '''    # =========================================================================
    # 13. QUẢN TRỊ DÒNG TIỀN COD & THU HỒI CÔNG NỢ
    # =========================================================================
    add_speech_section(
        doc,
        sec_title="💰 [XIII. QUẢN TRỊ DÒNG TIỀN COD, TỶ LỆ THANH TOÁN & THU HỒI CÔNG NỢ (W38)]",
        speech_heading="🗣️ QUẢN TRỊ COD 84.4 TỶ ĐỒNG: BÁO ĐỘNG TỶ LỆ TIỀN MẶT TĂNG LÊN 43.1% (36.4 TỶ TIỀN MẶT):",
        paragraphs_text=[
            "Kính thưa Ban Giám Đốc, về công tác quản trị an toàn tài chính, dòng tiền thu hộ (COD) và rủi ro thu tiền mặt tuần W38:",
            "• Tổng quy mô dòng tiền COD toàn vùng tuần W38: Toàn mạng Nam Trung Bộ phát sinh tổng số tiền COD thu hộ đạt 84.441,1 triệu đồng (84,4 tỷ đồng), giảm nhẹ -6,6% WoW so với tuần W37 (90.413,7 triệu đồng).",
            "• Biến động cơ cấu hình thức thanh toán — BÁO ĐỘNG TĂNG TỶ LỆ TIỀN MẶT:",
            "- Thu Tiền mặt: Đạt 36.427,8 triệu đồng (36,4 tỷ đồng), tăng thêm +115,0 triệu đồng (+0,3% WoW).",
            "- Chuyển khoản qua QR Code (VietQR): Đạt 48.013,4 triệu đồng (48,0 tỷ đồng), giảm sâu -6.087,5 triệu đồng (-11,3% WoW).",
            "- Tỷ lệ Tiền mặt (% TM) toàn vùng đã TĂNG XẤU từ 40,2% (tuần W37) lên mức 43,1% trong tuần W38 (+3,0%p WoW, tương ứng tăng +7,4% về tỷ trọng tiền mặt). Tỷ lệ chuyển khoản QR giảm tương ứng từ 59,8% xuống 56,9%.",
            "• Điểm danh đích danh Top Quản lý Vận hành (AM) có tỷ lệ tiền mặt cao báo động đỏ (> 70% tiền mặt):",
            "1. AM Lê Thanh Nhựt (Bình Thuận) — BÁO ĐỘNG ĐỎ SỐ 1: Tỷ lệ tiền mặt cao nhất toàn mạng lưới lên tới 78,9% (tăng +3,3%p WoW so với W37: 75,6%) — bưu tá thu tiền mặt gần như 8/10 đơn hàng!",
            "2. AM Huỳnh Thúc Duân (Đắk Nông): Tỷ lệ tiền mặt lên tới 77,7% (W37: 78,8%).",
            "3. AM Trần Văn Phước (Đắk Nông) — BÙNG PHÁT NGUY HIỂM: Tỷ lệ tiền mặt nhảy vọt đột biến +15,3%p WoW (từ 60,9% tuần W37 bùng lên 76,3% tuần W38!) — cảnh báo nguy cơ bưu tá ôm giữ tiền mặt cực lớn.",
            "4. AM Huỳnh Thị Kim Chi (Lâm Đồng): Tỷ lệ tiền mặt duy trì ở mức rất cao 73,9% (W37: 76,2%).",
            "5. AM Trần Thị Nhung (Đắk Nông): Tỷ lệ tiền mặt 70,5% (W37: 71,6%).",
            "6. AM Trầm Hữu Tiến (Lâm Đồng): Tỷ lệ tiền mặt 66,5% (tăng +5,7%p WoW so với W37: 60,9%).",
            "7. AM Nguyễn Đỗ Minh Nghĩa (Ninh Thuận): Tỷ lệ tiền mặt 65,8%.",
            "8. AM Lê Minh Đại: Tỷ lệ tiền mặt 54,7%.",
            "• Điểm sáng kiểm soát chuyển khoản QR xuất sắc (tỷ lệ tiền mặt cực thấp):",
            "- AM Thái Thị Thanh Thư (Khánh Hòa): Quán quân chuyển đổi số toàn vùng với tỷ lệ tiền mặt chỉ 5,6% (chuyển khoản QR chiếm tới 94,4%!).",
            "- AM Cao Thị Thanh Thủy: Tỷ lệ tiền mặt chỉ 17,2% (QR chiếm 82,8%).",
            "- AM Nguyễn Duy Long: Tỷ lệ tiền mặt chỉ 24,6% (QR chiếm 75,4%).",
            "• Bóc tách Top Bưu cục điểm nóng tỷ lệ tiền mặt cao kỷ lục và số tiền mặt thu giữ lớn nhất:",
            "- Bưu cục (DNO) Quảng Khê (AM Trần Thị Nhung): Tỷ lệ tiền mặt CHẠM TRẦN 100,0% (423,8 triệu đồng tiền mặt) — 100% người nhận trả tiền mặt, không một đơn nào quét mã VietQR!",
            "- Bưu cục (LDO) Hòa Ninh (AM Hồng Bích Nga): Tỷ lệ tiền mặt 99,9%, thu giữ 752,7 triệu đồng tiền mặt.",
            "- Bưu cục (DNO) Bắc Gia Nghĩa (AM Huỳnh Thúc Duân): Tỷ lệ tiền mặt 95,7% (424,3 triệu đồng).",
            "- Bưu cục (KHO) Vạn Ninh (AM Phan Đình Duy): Tỷ lệ tiền mặt 93,3% (tăng vọt +21,6%p WoW, thu giữ 823,7 triệu đồng tiền mặt).",
            "- Bưu cục (BTH) Hàm Thuận (AM Lê Thanh Nhựt): Tỷ lệ tiền mặt 91,3%, thu giữ số tiền mặt khổng lồ lên tới 1.264,7 triệu đồng (1,26 tỷ đồng)!",
            "- Bưu cục (KHO) CK Diên Điền (AM Phan Đình Duy): Tỷ lệ tiền mặt nhảy vọt bất thường +77,9%p WoW (từ 13,2% tuần W37 nhảy lên 91,1% tuần W38 với 722,8 triệu đồng tiền mặt)! Cần kiểm tra ngay xem hệ thống app bưu tá có bị lỗi in mã QR hay không.",
            "- Bưu cục (BTH) Đồng Kho (AM Lê Thanh Nhựt): Tỷ lệ tiền mặt 87,5%, thu giữ 1.229,3 triệu đồng (1,23 tỷ đồng) tiền mặt!",
            "- Bưu cục (BTH) Lương Sơn (AM Nguyễn Ngọc Khánh): Tỷ lệ tiền mặt 87,0% (tăng +12,6%p WoW, 511,6 triệu tiền mặt).",
            "- Bưu cục (DNO) Đức Lập (AM Trần Thị Nhung): Tỷ lệ tiền mặt 85,9%, là BƯU CỤC THU GIỮ SỐ TIỀN MẶT LỚN NHẤT TOÀN MẠNG LƯỚI LÊN TỚI 1.703,0 TRIỆU ĐỒNG (1,70 TỶ ĐỒNG)!",
            "- Bưu cục (BTH) Hàm Liêm (AM Lê Thanh Nhựt): Tỷ lệ tiền mặt 85,7% (tăng +8,4%p WoW, 796,7 triệu tiền mặt).",
            "- Bưu cục (LDO) Đam Rông 3 (AM Huỳnh Thị Kim Chi): Tỷ lệ tiền mặt 83,5% (762,6 triệu tiền mặt).",
            "- Bưu cục (LDO) Đinh Văn Lâm Hà (AM Huỳnh Thị Kim Chi): Tỷ lệ tiền mặt 80,7% (923,8 triệu tiền mặt).",
            "- Bưu cục (KHO) Diên Khánh 2 (AM Nguyễn Hoàng Phi): Tỷ lệ tiền mặt 80,3% (946,9 triệu tiền mặt).",
            "- Bưu cục (DNO) Kiến Đức (AM Trần Văn Phước): Tỷ lệ tiền mặt 79,4% (tăng +20,3%p WoW, 525,9 triệu tiền mặt)."
        ],
        insights=[
            "Thói quen và sự lười hướng dẫn của bưu tá: Tại các bưu cục đồi núi và nông thôn Bình Thuận, Đắk Nông, Lâm Đồng, bưu tá ngại đưa mã QR cho khách quét mà chủ động thu tiền mặt để tiện tiêu dùng hoặc làm tròn tiền, dẫn tới tỷ lệ tiền mặt tại Hàm Thuận (91,3%), Đồng Kho (87,5%), Đức Lập (85,9%) vượt ngưỡng 85%.",
            "Bất thường công nghệ tại CK Diên Điền: Việc tỷ lệ tiền mặt nhảy vọt +77,9%p WoW (từ 13,2% lên 91,1%) là dấu hiệu bất thường về quy trình tác nghiệp hoặc lỗi hiển thị mã QR trên app giao hàng."
        ],
        warnings=[
            "Tổng số tiền mặt thu giữ lên tới 36,4 tỷ đồng, đặc biệt tại Đức Lập (1,70 tỷ), Hàm Thuận (1,26 tỷ), Đồng Kho (1,23 tỷ) tiềm ẩn rủi ro cực lớn về an toàn tài chính, nguy cơ chiếm dụng dòng tiền, rơi rớt hoặc trộm cắp.",
            "Chậm nộp tiền mặt COD ngân hàng làm gián đoạn dòng tiền đối soát trả cho các chủ shop lớn, khiến shop khiếu nại và có thể ngưng hợp tác với GHN."
        ],
        actions=[
            "Thiết lập kỷ luật khóa sổ tiền mặt: Bắt buộc 100% bưu tá tại Đức Lập, Hàm Thuận, Đồng Kho, Vạn Ninh phải nộp toàn bộ tiền mặt COD thu được trong ngày về tài khoản công ty trước 18h30 hàng ngày; nghiêm cấm giữ tiền qua đêm.",
            "Kích hoạt chiến dịch thi đua 'Quét VietQR nhận quà': Gắn KPI tỷ lệ tiền mặt cho các AM có tỷ lệ tiền mặt trên 70% (Lê Thanh Nhựt, Huỳnh Thúc Duân, Trần Văn Phước, Huỳnh Thị Kim Chi, Trần Thị Nhung); yêu cầu giảm tỷ lệ tiền mặt xuống dưới 55% trong tuần W39.",
            "Kiểm tra kỹ thuật khẩn cấp tại Bưu cục CK Diên Điền để xác minh nguyên nhân tỷ lệ tiền mặt tăng vọt +77,9%p."
        ]
    )'''

# Replace Section X
pattern_sec10 = r'    # =========================================================================\s+# 10\. BÁO CÁO HOÀN TRẢ %FD \(RETURN\)\s+# =========================================================================.*?actions=\[\s+"[^"]+",\s+"[^"]+"\s+\]\s+\)'
content = re.sub(pattern_sec10, sec_10_new, content, flags=re.DOTALL)

# Replace Section XIII
pattern_sec13 = r'    # =========================================================================\s+# 13\. QUẢN TRỊ DÒNG TIỀN COD & THU HỒI CÔNG NỢ\s+# =========================================================================.*?actions=\[\s+"[^"]+",\s+"[^"]+"\s+\]\s+\)'
content = re.sub(pattern_sec13, sec_13_new, content, flags=re.DOTALL)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated Sections X and XIII in scratch/generate_professional_w38_script.py successfully!")
