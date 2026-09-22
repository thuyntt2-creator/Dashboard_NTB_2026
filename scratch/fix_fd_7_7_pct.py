import re

path = r"c:\Users\lap4all\Desktop\New folder\scratch\generate_professional_w38_script.py"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Corrected Section X: %FD 7.74% (7.7%)
sec_10_corrected = '''    # =========================================================================
    # 10. BÁO CÁO HOÀN TRẢ %FD (RETURN)
    # =========================================================================
    add_speech_section(
        doc,
        sec_title="🔄 [X. BÁO CÁO TỶ LỆ %FD (RETURN / HOÀN TRẢ) — VÙNG NAM TRUNG BỘ (W38)]",
        speech_heading="🗣️ PHÂN TÍCH TỶ LỆ HOÀN TRẢ (%FD) 7.7% TOÀN VÙNG (26.531 ĐƠN RETURN) VÀ BÓC TÁCH CHI TIẾT 18 AM & 10 BƯU CỤC NÓNG:",
        paragraphs_text=[
            "Kính thưa Ban Giám Đốc, về tỷ lệ Hoàn Trả (%FD) — chỉ số trực tiếp bào mòn biên lợi nhuận của toàn vùng:",
            "• Tổng quan toàn mạng tuần W38: Theo số liệu đối soát chính thức từ Sheet 12_FD, tỷ lệ %FD Full hàng toàn vùng Nam Trung Bộ đạt mức 7,74% (làm tròn 7,7%). Toàn bộ 84 bưu cục do 18 Quản lý Vận hành (AM) phụ trách ghi nhận tổng cộng 26.531 đơn Return (chuyển trả) trên tổng số 342.727 đơn có gán giao trong tuần.",
            "• Phân hóa theo 5 Tỉnh thành:",
            "- Bình Thuận & Ninh Thuận: Kiểm soát hoàn trả tốt nhất khu vực với tỷ lệ %FD chỉ từ 4,8% – 6,0% nhờ sự điều hành chặt chẽ của AM Nguyễn Văn Khánh (4,77%), AM Nguyễn Đỗ Minh Nghĩa (5,68%) và AM Lê Thanh Nhựt (5,96%).",
            "- Khánh Hòa: Nằm ở mức trung bình 6,65% – 6,88%.",
            "- Lâm Đồng & Đắk Nông: Tiếp tục là 2 vùng trũng rủi ro hoàn trả cao nhất mạng lưới, trong đó Đắk Nông ghi nhận tỷ lệ hoàn trả bình quân vượt ngưỡng 8,12% do tập trung nhiều bưu cục đồi núi có tỷ lệ hoàn trả trên 11%.",
            "• Bảng xếp hạng chi tiết tỷ lệ hoàn trả %FD của 18 Quản lý Vận hành (AM) (xếp từ cao xuống thấp):",
            "1. AM Trương Quang Linh (Đắk Nông) — BÁO ĐỘNG ĐỎ KỶ LỤC SỐ 1: Tỷ lệ hoàn trả %FD Full cao nhất toàn mạng lên tới 37,89% (770 đơn hoàn / 2.032 đơn giao, kênh TTS hoàn 33,33%) — cứ hơn 2,5 đơn giao đi thì có gần 1 đơn bị trả về!",
            "2. AM Trần Tấn Lợi (Lâm Đồng) — BÁO ĐỘNG ĐỎ SỐ 2: Tỷ lệ %FD Full đạt tới 20,30% (625 đơn hoàn / 3.079 đơn giao, TTS hoàn 17,94%).",
            "3. AM Nguyễn Tiến Long (Khánh Hòa): %FD đạt 11,51% (1.530 đơn hoàn / 13.293 đơn giao, TTS hoàn 10,19%).",
            "4. AM Huỳnh Thúc Duân (Đắk Nông): %FD đạt 10,20% (493 đơn hoàn / 4.831 đơn).",
            "5. AM Nguyễn Lê Nguyên Vũ (Lâm Đồng): %FD đạt 9,82% (1.308 đơn hoàn / 13.322 đơn).",
            "6. AM Trần Thị Nhung (Đắk Nông): %FD đạt 9,36%, đặc biệt đây là AM CÓ SỐ LƯỢNG ĐƠN HOÀN KHỔNG LỒ NHẤT NHÓM NGUY CƠ với 2.392 đơn hoàn / 25.557 đơn giao!",
            "7. AM Phan Đình Duy (Khánh Hòa): %FD đạt 9,15% với 2.186 đơn hoàn / 23.887 đơn giao.",
            "8. AM Lê Văn Trường (Lâm Đồng): %FD đạt 8,13% với 2.273 đơn hoàn / 27.971 đơn giao.",
            "9. AM Nguyễn Hoàng Phi (Khánh Hòa): %FD đạt 8,07% với 2.003 đơn hoàn / 24.827 đơn giao.",
            "10. AM Hồng Bích Nga (Đắk Nông): %FD đạt 7,08% (1.433 đơn hoàn / 20.237 đơn).",
            "11. AM Lê Thị Kim Chi (Lâm Đồng): %FD đạt 6,97% (911 đơn hoàn / 13.070 đơn).",
            "12. AM Nguyễn Thị Tuyết Thơ: %FD đạt 6,95% (653 đơn hoàn / 9.394 đơn).",
            "13. AM Thái Thị Thanh Thư: %FD đạt 6,88% (2.262 đơn hoàn / 32.870 đơn).",
            "14. AM Nguyễn Duy Long (Bình Thuận): %FD đạt 6,84% (2.941 đơn hoàn / 42.981 đơn).",
            "15. AM Cao Thị Thanh Thủy: %FD đạt 6,09% (1.075 đơn hoàn / 17.643 đơn).",
            "16. AM Lê Thanh Nhựt: %FD đạt 5,96% (1.828 đơn hoàn / 30.659 đơn).",
            "17. AM Nguyễn Đỗ Minh Nghĩa: %FD đạt 5,68% (495 đơn hoàn / 8.714 đơn).",
            "18. AM Nguyễn Văn Khánh: %FD kiểm soát tốt nhất toàn mạng chỉ 4,77% (1.353 đơn hoàn / 28.360 đơn).",
            "• So sánh biến động WoW tại Top 10 Bưu cục điểm nóng có tỷ lệ hoàn trả cao nhất toàn vùng:",
            "- Bưu cục (DNO) Quảng Tín (AM Trương Quang Linh): BÁO ĐỘNG ĐỎ CAO NHẤT TOÀN QUỐC khi %FD lên tới 37,89% (770 đơn hoàn / 2.032 đơn giao), tăng vọt +4,37%p WoW so với tuần W37 (33,52%)!",
            "- Bưu cục (LDO) Lang Biang - Đà Lạt 1 (AM Trần Tấn Lợi): %FD đạt 20,30% (625 đơn hoàn / 3.079 đơn), tăng mạnh +4,03%p WoW so với W37 (16,26%).",
            "- Bưu cục (KHO) Cam Linh (AM Nguyễn Tiến Long): %FD đạt 16,96%, là BƯU CỤC CÓ SỐ ĐƠN HOÀN LỚN NHẤT TOÀN VÙNG với 988 đơn hoàn / 5.825 đơn, tăng +2,01%p WoW so với W37 (14,96%).",
            "- Bưu cục (DNO) Kiến Đức (AM Hồng Bích Nga): %FD đạt 15,53% (343 đơn hoàn / 2.209 đơn), mặc dù đã giảm -1,83%p WoW nhưng vẫn nằm trong top nguy cơ cao.",
            "- Bưu cục (LDO) Đức Trọng 1 (AM Nguyễn Lê Nguyên Vũ): %FD đạt 14,59% (318 đơn hoàn / 2.179 đơn), tăng +2,27%p WoW so với W37 (12,32%).",
            "- Bưu cục (DNO) Đông Gia Nghĩa (AM Huỳnh Thúc Duân): %FD đạt 14,51% (280 đơn hoàn / 1.930 đơn), tăng +1,09%p WoW so với W37 (13,42%).",
            "- Bưu cục (DNO) Tuy Đức (AM Trần Thị Nhung): %FD đạt 12,43% (266 đơn hoàn / 2.140 đơn), tăng +1,02%p WoW so với W37 (11,41%).",
            "- Bưu cục (LDO) Di Linh (AM Nguyễn Lê Nguyên Vũ): %FD BÙNG PHÁT TĂNG ĐỘT BIẾN +5,71%p WoW (từ 6,37% tuần W37 nhảy vọt lên 12,08% tuần W38 với 733 đơn hoàn / 6.068 đơn)! Cần kiểm tra ngay hiện tượng bưu tá ép hoàn hàng loạt.",
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

pattern_sec10 = r'    # =========================================================================\s+# 10\. BÁO CÁO HOÀN TRẢ %FD \(RETURN\)\s+# =========================================================================.*?actions=\[\s+"[^"]+",\s+"[^"]+"\s+\]\s+\)'
content = re.sub(pattern_sec10, sec_10_corrected, content, flags=re.DOTALL)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated Section X with exact 7.74% (7.7%) and 26,531 orders in generate_professional_w38_script.py!")
