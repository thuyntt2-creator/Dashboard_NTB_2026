import re

path = r"c:\Users\lap4all\Desktop\New folder\scratch\generate_professional_w38_script.py"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# New Section XIII based on freshly updated Google Sheets data
sec_13_fresh = '''    # =========================================================================
    # 13. QUẢN TRỊ DÒNG TIỀN COD & THU HỒI CÔNG NỢ
    # =========================================================================
    add_speech_section(
        doc,
        sec_title="💰 [XIII. QUẢN TRỊ DÒNG TIỀN COD, TỶ LỆ THANH TOÁN & THU HỒI CÔNG NỢ (W38)]",
        speech_heading="🗣️ CẬP NHẬT MỚI: QUẢN TRỊ COD 84.4 TỶ ĐỒNG — BÁO ĐỘNG TỶ LỆ TIỀN MẶT TĂNG LÊN 43.1% (36.4 TỶ TIỀN MẶT):",
        paragraphs_text=[
            "Kính thưa Ban Giám Đốc, về công tác quản trị an toàn tài chính, dòng tiền thu hộ (COD) và kiểm soát bưu tá thu giữ tiền mặt tuần W38 theo dữ liệu đối soát mới nhất vừa cập nhật:",
            "• Tổng quy mô dòng tiền COD toàn vùng tuần W38: Toàn mạng Nam Trung Bộ phát sinh tổng số tiền COD thu hộ đạt 84.441,1 triệu đồng (84,4 tỷ đồng), giảm nhẹ -6,6% WoW so với tuần W37 (90.413,7 triệu đồng).",
            "• Biến động cơ cấu hình thức thanh toán — BÁO ĐỘNG TĂNG TỶ LỆ TIỀN MẶT:",
            "- Thu Tiền mặt: Đạt 36.427,8 triệu đồng (36,4 tỷ đồng), tăng thêm +115,0 triệu đồng (+0,3% WoW).",
            "- Chuyển khoản qua QR Code (VietQR): Đạt 48.013,4 triệu đồng (48,0 tỷ đồng), giảm sâu -6.087,5 triệu đồng (-11,3% WoW).",
            "- Tỷ lệ Tiền mặt (% TM) toàn vùng đã TĂNG XẤU từ 40,2% (tuần W37) lên mức 43,1% trong tuần W38 (+3,0%p WoW, tương ứng tăng +7,4% về tỷ trọng tiền mặt). Tỷ lệ chuyển khoản QR giảm tương ứng từ 59,8% xuống 56,9%.",
            "• Điểm danh đích danh Top Quản lý Vận hành (AM) có tỷ lệ tiền mặt cao báo động đỏ (> 70% tiền mặt):",
            "1. AM Lê Thanh Nhựt (Bình Thuận) — BÁO ĐỘNG ĐỎ SỐ 1: Tỷ lệ tiền mặt cao nhất toàn mạng lưới lên tới 78,9% (tăng +3,3%p WoW so với W37: 75,6%) — bưu tá thu tiền mặt gần như 8/10 đơn hàng!",
            "2. AM Huỳnh Thúc Duân (Đắk Nông): Tỷ lệ tiền mặt lên tới 76,5% (tăng +0,7%p WoW so với W37: 75,8%).",
            "3. AM Trương Quang Linh (Đắk Nông) — BÙNG PHÁT NGUY HIỂM: Tỷ lệ tiền mặt nhảy vọt đột biến +12,8%p WoW (từ 61,4% tuần W37 bùng lên 74,2% tuần W38!) — cảnh báo nguy cơ bưu tá ôm giữ tiền mặt cực lớn.",
            "4. AM Huỳnh Thị Kim Chi (Lâm Đồng): Tỷ lệ tiền mặt duy trì ở mức rất cao 73,9% (W37: 76,2%).",
            "5. AM Trần Thị Nhung (Đắk Nông): Tỷ lệ tiền mặt 70,5% (W37: 71,6%).",
            "6. AM Nguyễn Đỗ Minh Nghĩa (Ninh Thuận): Tỷ lệ tiền mặt 53,6% (tăng +4,4%p WoW so với W37: 49,1%).",
            "• Điểm sáng kiểm soát chuyển khoản QR xuất sắc (tỷ lệ tiền mặt cực thấp):",
            "- AM Thái Thị Thanh Thư (Khánh Hòa): Quán quân chuyển đổi số toàn vùng với tỷ lệ tiền mặt chỉ 5,6% (chuyển khoản QR chiếm tới 94,4%!).",
            "- AM Cao Thị Thanh Thủy: Tỷ lệ tiền mặt chỉ 17,2% (QR chiếm 82,8%).",
            "- AM Nguyễn Duy Long (Bình Thuận): Tỷ lệ tiền mặt chỉ 24,6% (QR chiếm 75,4%).",
            "- AM Nguyễn Ngọc Khánh: Tỷ lệ tiền mặt 30,6%.",
            "- AM Nguyễn Thanh Long: Tỷ lệ tiền mặt 32,4%.",
            "- AM Lê Minh Lợi: Tỷ lệ tiền mặt 37,0%.",
            "• Bóc tách Top Bưu cục điểm nóng tỷ lệ tiền mặt cao kỷ lục và số tiền mặt thu giữ lớn nhất:",
            "- Bưu cục (DNO) Quảng Khê (AM Trần Thị Nhung): Tỷ lệ tiền mặt CHẠM TRẦN 100,0% (thu giữ 423,8 triệu đồng tiền mặt) — 100% người nhận trả tiền mặt, không một đơn nào quét mã VietQR!",
            "- Bưu cục (LDO) Hòa Ninh (AM Hồng Bích Nga): Tỷ lệ tiền mặt 99,9%, thu giữ 752,7 triệu đồng tiền mặt.",
            "- Bưu cục (DNO) Bắc Gia Nghĩa (AM Huỳnh Thúc Duân): Tỷ lệ tiền mặt 95,7% (thu giữ 424,3 triệu đồng).",
            "- Bưu cục (KHO) Vạn Ninh (AM Phan Đình Duy): Tỷ lệ tiền mặt 93,3% (tăng vọt +21,6%p WoW, thu giữ 823,7 triệu đồng tiền mặt).",
            "- Bưu cục (BTH) Hàm Thuận (AM Lê Thanh Nhựt): Tỷ lệ tiền mặt 91,3%, thu giữ số tiền mặt khổng lồ lên tới 1.264,7 triệu đồng (1,26 tỷ đồng)!",
            "- Bưu cục (KHO) CK Diên Điền (AM Phan Đình Duy): Tỷ lệ tiền mặt nhảy vọt bất thường +77,9%p WoW (từ 13,2% tuần W37 nhảy lên 91,1% tuần W38 với 722,8 triệu đồng tiền mặt)! Cần kiểm tra ngay xem hệ thống app bưu tá có bị lỗi tạo mã QR hay không.",
            "- Bưu cục (BTH) Đồng Kho (AM Lê Thanh Nhựt): Tỷ lệ tiền mặt 87,5%, thu giữ 1.229,3 triệu đồng (1,23 tỷ đồng) tiền mặt!",
            "- Bưu cục (BTH) Lương Sơn (AM Nguyễn Ngọc Khánh): Tỷ lệ tiền mặt 87,0% (tăng +12,6%p WoW, thu giữ 511,6 triệu đồng).",
            "- Bưu cục (DNO) Đức Lập (AM Trần Thị Nhung): Tỷ lệ tiền mặt 85,9%, là BƯU CỤC THU GIỮ SỐ TIỀN MẶT LỚN NHẤT TOÀN MẠNG LƯỚI LÊN TỚI 1.703,0 TRIỆU ĐỒNG (1,70 TỶ ĐỒNG)!",
            "- Bưu cục (BTH) Hàm Liêm (AM Lê Thanh Nhựt): Tỷ lệ tiền mặt 85,7% (tăng +8,4%p WoW, thu giữ 796,7 triệu đồng).",
            "- Bưu cục (KHO) Cam Lâm 1 (AM Nguyễn Hoàng Phi): Tỷ lệ tiền mặt 84,1% (tăng +6,1%p, 550,7 triệu đồng).",
            "- Bưu cục (LDO) Đam Rông 3 (AM Huỳnh Thị Kim Chi): %TM 83,5% (thu giữ 762,6 triệu đồng).",
            "- Bưu cục (LDO) Đinh Văn Lâm Hà (AM Huỳnh Thị Kim Chi): %TM 80,7% (thu giữ 923,8 triệu đồng).",
            "- Bưu cục (KHO) Diên Khánh 2 (AM Nguyễn Hoàng Phi): %TM 80,3% (thu giữ 946,9 triệu đồng).",
            "- Bưu cục (LDO) Cát Tiên (AM Nguyễn Đỗ Minh Nghĩa): %TM 79,9% (thu giữ 456,9 triệu đồng).",
            "- Bưu cục (DNO) Kiến Đức (AM Hồng Bích Nga): %TM 79,4% (tăng +20,3%p WoW, thu giữ 525,9 triệu đồng).",
            "- Bưu cục (DNO) Krông Nô (AM Trần Thị Nhung): %TM 77,3% (thu giữ 744,2 triệu đồng).",
            "- Bưu cục (DNO) Quảng Tín (AM Trương Quang Linh): %TM 74,2% (tăng +12,8%p WoW, thu giữ 347,0 triệu đồng).",
            "- Bưu cục (DNO) Tuy Đức (AM Trần Thị Nhung): %TM 73,7% (thu giữ 385,9 triệu đồng).",
            "- Bưu cục (DNO) Nhân Cơ (AM Huỳnh Thúc Duân): %TM 73,0% (thu giữ 253,5 triệu đồng)."
        ],
        insights=[
            "Thói quen và sự lười hướng dẫn của bưu tá: Tại các bưu cục đồi núi và nông thôn Bình Thuận, Đắk Nông, Lâm Đồng, bưu tá ngại đưa mã QR cho khách quét mà chủ động thu tiền mặt để tiện tiêu dùng hoặc làm tròn tiền, dẫn tới tỷ lệ tiền mặt tại Hàm Thuận (91,3%), Đồng Kho (87,5%), Đức Lập (85,9%) vượt ngưỡng 85%.",
            "Bất thường công nghệ tại CK Diên Điền: Việc tỷ lệ tiền mặt nhảy vọt +77,9%p WoW (từ 13,2% lên 91,1%) là dấu hiệu bất thường về quy trình tác nghiệp hoặc lỗi hiển thị mã QR trên app giao hàng.",
            "Tập trung rủi ro cao tại 6 AM: 6 AM gồm Lê Thanh Nhựt, Huỳnh Thúc Duân, Trương Quang Linh, Huỳnh Thị Kim Chi, Trần Thị Nhung và Nguyễn Đỗ Minh Nghĩa đang là những địa bàn có tỷ lệ tiền mặt vượt chuẩn, phát sinh yêu cầu hành động xử lý trong 24h - 3 ngày."
        ],
        warnings=[
            "Tổng số tiền mặt thu giữ lên tới 36,4 tỷ đồng, đặc biệt tại Đức Lập (1,70 tỷ), Hàm Thuận (1,26 tỷ), Đồng Kho (1,23 tỷ) tiềm ẩn rủi ro cực lớn về an toàn tài chính, nguy cơ chiếm dụng dòng tiền, rơi rớt hoặc trộm cắp.",
            "Chậm nộp tiền mặt COD ngân hàng làm gián đoạn dòng tiền đối soát trả cho các chủ shop lớn, khiến shop khiếu nại và có thể ngưng hợp tác với GHN."
        ],
        actions=[
            "Thiết lập kỷ luật khóa sổ tiền mặt: Bắt buộc 100% bưu tá tại Đức Lập, Hàm Thuận, Đồng Kho, Vạn Ninh phải nộp toàn bộ tiền mặt COD thu được trong ngày về tài khoản công ty trước 18h30 hàng ngày; nghiêm cấm giữ tiền qua đêm.",
            "Kích hoạt chiến dịch thi đua 'Quét VietQR nhận quà': Gắn KPI tỷ lệ tiền mặt cho các AM có tỷ lệ tiền mặt trên 70% (Lê Thanh Nhựt, Huỳnh Thúc Duân, Trương Quang Linh, Huỳnh Thị Kim Chi, Trần Thị Nhung); yêu cầu giảm tỷ lệ tiền mặt xuống dưới 55% trong tuần W39.",
            "Kiểm tra kỹ thuật khẩn cấp tại Bưu cục CK Diên Điền để xác minh nguyên nhân tỷ lệ tiền mặt tăng vọt +77,9%p."
        ]
    )'''

pattern_sec13 = r'    # =========================================================================\s+# 13\. QUẢN TRỊ DÒNG TIỀN COD & THU HỒI CÔNG NỢ\s+# =========================================================================.*?actions=\[\s+"[^"]+",\s+"[^"]+",?\s+"?[^"]*"?\s+\]\s+\)'
content = re.sub(pattern_sec13, sec_13_fresh, content, flags=re.DOTALL)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated Section XIII with fresh Google Sheet COD data in generate_professional_w38_script.py!")
