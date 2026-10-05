# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

new_tab_13_14 = '''    # ----------------------------------------------------
    # TAB 13: BÁO CÁO COD – QUẢN TRỊ DÒNG TIỀN & QR CODE
    # ----------------------------------------------------
    {
        "id": "tab-control",
        "title": "🗣️ PHÂN TÍCH QUẢN TRỊ DÒNG TIỀN COD (77.5 TỶ) & CHUYỂN ĐỔI SỐ THANH TOÁN QR CODE (BẬT TAB 13 DASHBOARD):",
        "content": """📍 1. BẢNG 1: TỔNG QUAN DÒNG TIỀN COD TOÀN VÙNG (W39 VS W40):
• Tổng COD thu hộ toàn vùng tuần W40: 77.502,0 Triệu VNĐ (~77,5 Tỷ đồng, giảm -3.231,6 Tr ₫ / -4,0% do volume giảm nhẹ).
• Tiền mặt thu về: 31.276,0 Triệu VNĐ (chiếm tỷ lệ 40,4% tiền mặt | Giảm -1.128,7 Tr ₫).
• Chuyển khoản QR thu về: 46.226,0 Triệu VNĐ (chiếm tỷ lệ 59,6% chuyển khoản QR | Giảm -2.103,0 Tr ₫).
• Đánh giá biến động: Tỷ lệ tiền mặt tăng nhẹ +0,2%p (từ 40,1% lên 40,4%), chuyển khoản QR giảm nhẹ -0,2%p ➔ XU HƯỚNG ĐANG XẤU ĐI ⚠️!

📍 2. BẢNG 2: SO SÁNH TỶ LỆ TIỀN MẶT THEO 18 AM (TARGET TIỀN MẶT < 40.0%, QR > 60.0%):
• 🟢 TOP AM CHUYỂN ĐỔI SỐ DÒNG TIỀN XUẤT SẮC NHẤT VÙNG (QR > 70%, TIỀN MẶT RẤT THẤP):
  1. Thái Thị Thanh Thư (Khánh Hòa): Tiền mặt chỉ 4,0% (W39: 4,4%) ➔ TỶ LỆ QR ĐẠT TỚI 96,0%! (Thu hơn 9 Tỷ COD mà tiền mặt chỉ có 360 triệu, số hóa dòng tiền gần như tuyệt đối!).
  2. Cao Thị Thanh Thủy (Khánh Hòa): Tiền mặt 16,1% (giảm -3,6%p) ➔ QR đạt 83,9%!
  3. Nguyễn Duy Long (Ninh Thuận): Tiền mặt 23,4% ➔ QR đạt 76,6% (trên quy mô thu COD cực lớn).
  4. Nguyễn Ngọc Khánh (Bình Thuận): Tiền mặt 30,6% ➔ QR đạt 69,4%.
  5. Nguyễn Thanh Long (Khánh Hòa): Tiền mặt 30,7% ➔ QR đạt 69,3%.
  6. Phan Đình Duy (Khánh Hòa): Tiền mặt 34,2% ➔ QR đạt 65,8%.
• 🔴 TOP 3 AM BÁO ĐỘNG ĐỎ NGUY CƠ THẤT THOÁT TIỀN MẶT (TỶ LỆ TIỀN MẶT VƯỢT 75% — MỨC ĐỘ NGHIÊM TRỌNG):
  1. Huỳnh Thúc Duân (Đắk Nông): 81,0% Tiền mặt! (W39: 71,5%, TĂNG VỌT +9,5%p ➔ Đỉnh tiền mặt cao nhất toàn vùng!).
  2. Lê Thanh Nhựt (Bình Thuận): 80,4% Tiền mặt! (W39: 77,7%, tăng +2,7%p ➔ Duy trì ở mức rất cao qua 2 tuần).
  3. Huỳnh Thị Kim Chi (Lâm Đồng): 75,8% Tiền mặt! (W39: 68,6%, TĂNG MẠNH +7,2%p).
• 🟡 NHÓM CẦN CẢI THIỆN (TIỀN MẶT TỪ 50% – 70%):
  - Trần Thị Nhung: 64,1% TM (tăng +1,3%p)
  - Phan Nguyễn Yến Nhi: 59,2% TM (tăng +2,1%p)
  - Nguyễn Đỗ Minh Nghĩa: 58,6% TM (tăng vọt +7,2%p)
  - Trương Quang Linh: 56,3% TM (tiến bộ lớn, giảm mạnh -24,3%p từ 80,6%)

📍 3. BẢNG 3: TOP 8 BƯU CỤC ÔM TIỀN MẶT KHỦNG KHIẾP NHẤT VÙNG:
• 1. (DNO) Quảng Khê (AM Nhung): 99,1% TM (Tiền mặt: 354,5 Tr ₫)
• 2. (DNO) Bắc Gia Nghĩa (AM Duân): 97,3% TM (Tiền mặt: 371,5 Tr ₫)
• 3. (BTH) Hàm Thuận (AM Nhựt): 89,5% TM (Tiền mặt: 1.200,5 Tr ₫ — HƠN 1,2 TỶ ĐỒNG TIỀN MẶT ÔM TRONG TÚI BƯU TÁ!)
• 4. (LDO) Đam Rông 3 (AM Chi): 88,7% TM (Tiền mặt: 727,4 Tr ₫)
• 5. (BTH) Hàm Liêm (AM Nhựt): 88,1% TM (Tiền mặt: 720,1 Tr ₫)
• 6. (KHO) Cam Lâm 1 (AM Phi): 86,9% TM (Tiền mặt: 552,5 Tr ₫)
• 7. (BTH) Lương Sơn (AM Khánh): 84,4% TM (Tiền mặt: 421,8 Tr ₫)
• 8. (DNO) Đức Lập (AM Nhung): 82,3% TM (Tiền mặt: 1.358,5 Tr ₫ — HƠN 1,35 TỶ ĐỒNG TIỀN MẶT!)

🎙️ LỜI THOẠI THUYẾT TRÌNH TỰ NHIÊN (KHI BẬT TAB 13 DASHBOARD COD & QR CODE):
"Kính thưa Ban Giám Đốc và toàn thể các anh chị em AM,
Chúng ta chuyển sang Tab 13 là Báo cáo Quản trị dòng tiền COD và thanh toán QR Code:
Tuần W40 này, toàn vùng Nam Trung Bộ của chúng ta luân chuyển một dòng tiền COD cực kỳ lớn: 77,5 TỶ ĐỒNG!
Trong đó, số tiền thu về bằng chuyển khoản QR đạt 46,2 tỷ đồng (chiếm 59,6%), còn tiền mặt shipper ôm về nộp là 31,3 tỷ đồng (chiếm 40,4%).
So với tuần trước, tỷ lệ tiền mặt không những không giảm mà lại tăng nhẹ +0,2%p. Đây là tín hiệu báo động về tính kỷ luật tài chính!

Nhìn vào bức tranh toàn cảnh của 18 AM trên màn hình:
Ở chiều tích cực: Em xin biểu dương chị Thái Thị Thanh Thư ở Khánh Hòa:
Chị Thư quản lý thu hơn 9 tỷ tiền COD tại Nha Trang mà tỷ lệ tiền mặt chỉ vỏn vẹn có 4,0%, còn lại 96% khách hàng thanh toán qua mã VietQR chuyển thẳng về tài khoản công ty!
Chị Thủy ở Khánh Hòa cũng đạt tới 84% chuyển khoản QR, anh Duy Long ở Ninh Thuận đạt gần 77% QR!
Tại sao Khánh Hòa và Ninh Thuận làm được? Vì bưu tá chịu khó in mã QR dán lên gói hàng, shipper đến nơi mở sẵn app chìa mã cho khách quét, biến việc thanh toán không dùng tiền mặt thành thói quen!

NHƯNG các anh chị nhìn sang 3 AM ở nhóm báo động đỏ nghiêm trọng:
Anh Huỳnh Thúc Duân: 81,0% tiền mặt, tăng vọt gần 10%p so với tuần trước!
Anh Lê Thanh Nhựt: 80,4% tiền mặt, đứng yên ở mức nguy hiểm qua 2 tuần liền!
Chị Huỳnh Thị Kim Chi: 75,8% tiền mặt, tăng hơn 7%p!
Cứ 10 đồng tiền thu hộ của khách thì shipper của anh Duân, anh Nhựt, chị Chi đang ôm tới hơn 8 đồng tiền mặt trong người!
Nhìn xuống Bảng 3 Top bưu cục ôm tiền mặt:
Bưu cục Hàm Thuận của anh Nhựt ôm hơn 1,2 TỶ ĐỒNG tiền mặt! Bưu cục Hàm Liêm ôm 720 triệu!
Bưu cục Đức Lập của chị Nhung ôm hơn 1,35 TỶ ĐỒNG tiền mặt!
Các anh chị có biết cầm hàng tỷ đồng tiền mặt lưu động ngoài đường nguy hiểm đến mức nào không?

🔍 INSIGHT BẢN CHẤT & BÓC TRẦN NGUY CƠ HIỆN TRƯỜNG:
Tại sao tỷ lệ tiền mặt ở bưu cục anh Duân, anh Nhựt, chị Chi lại cao ngất ngưởng như vậy?
Bóc tách ra có 2 nguyên nhân cốt lõi:
1. BƯU TÁ CỐ TÌNH NÉ QUÉT QR ĐỂ CẦM TIỀN MẶT 'XOAY VÒNG ĐẢO NỢ':
Shipper thu tiền mặt của khách xong có tâm lý giữ lại trong ví cá nhân để chi tiêu riêng, rồi lấy tiền thu của ngày hôm sau bù đắp nộp về cho ngày hôm trước! Hiện tượng 'xoay vòng công nợ' này nếu bưu cục không chốt quỹ chặt chẽ từng ca thì chỉ cần shipper thua lỗ cá độ hoặc gặp biến cố là lập tức bùng nợ, biến thành chiếm dụng công nợ hàng chục triệu đồng!
2. NGỤY BIỆN 'NGƯỜI DÂN VÙNG QUÊ KHÔNG CÓ TÀI KHOẢN':
Nhiều AM đổ lỗi rằng Đắk Nông hay vùng nông thôn Bình Thuận bà con không biết chuyển khoản. Thực tế hiện nay người dân đi chợ mua rau cũng quét mã VietQR. Bưu tá lười in mã QR, lười chìa điện thoại cho khách quét vì muốn nhận tiền mặt cho tiện tay!

🎯 QUYẾT SÁCH HÀNH ĐỘNG & MỆNH LỆNH TÁC CHIẾN TUẦN W41:
1. YÊU CẦU GIẢI TRÌNH TRONG 24H: AM Huỳnh Thúc Duân và AM Huỳnh Thị Kim Chi phải gửi văn bản giải trình lý do vì sao tỷ lệ tiền mặt tăng vọt từ 7% đến 9,5%p về phòng Vận hành vùng trước 17h00 chiều mai.
2. LÀM VIỆC 1-1 VỚI AM LÊ THANH NHỰT: Phòng Tài chính - Kế toán vùng làm việc trực tiếp với anh Nhựt để kiểm tra quy trình nộp tiền tại Hàm Thuận và Hàm Liêm; trang bị ngay mã VietQR tại quầy và cấp mã bưu tá.
3. SIẾT CHẶT KỶ LUẬT THU NỘP QUỸ: 100% bưu cục phải thực hiện chốt quỹ tiền mặt 2 lần/ngày: Chốt ca trưa lúc 12h00 và chốt ca chiều lúc 18h30. Shipper không nộp hết tiền mặt về tài khoản công ty trước 19h00 sẽ bị khóa app không cho xuất bến ngày hôm sau!
4. GIAO CHỈ TIÊU TUẦN W41: Ép tỷ lệ tiền mặt của anh Duân, anh Nhựt, chị Chi từ trên 75-80% xuống dưới mốc 60%!
Bây giờ, em xin chuyển sang Tab 14 mổ xẻ Báo cáo Truy thu 2 tuần ạ!\"
    },

    # ----------------------------------------------------
    # TAB 14: BÁO CÁO TRUY THU (2 TUẦN W39 VS W40)
    # ----------------------------------------------------
    {
        "id": "tab-truythu",
        "title": "🗣️ BÁO CÁO TRUY THU 2 TUẦN: VỤ ÁN CHIẾM DỤNG TẠI BẮC CAM RANH & 419 TICKET TỒN ĐỌNG (BẬT TAB 14 DASHBOARD):",
        "content": """📍 1. BẢNG TỔNG HỢP SO SÁNH 2 TUẦN TRUY THU TOÀN VÙNG:
• Tổng số bản ghi (ticket): 2.424 bản ghi (W39: 4.076 bản ghi, giảm -1.652 đơn / -40,5%).
• Số tiền phát sinh ban đầu: 433,1 Triệu VNĐ (W39: 317,3 Tr ₫, TĂNG VỌT +115,8 Tr ₫ / +36,5% ➔ BÁO ĐỘNG ĐỎ VI PHẠM TĂNG MẠNH!).
• Số tiền điều chỉnh giảm: -246,0 Triệu VNĐ (chủ yếu là bù trừ đối soát backlog từ kỳ trước).
• Số tiền thực tế CẦN TRUY THU: 187,1 Triệu VNĐ (W39: 312,1 Tr ₫, giảm -125,0 Tr ₫ / -40,1%).

📍 2. BẢNG 1: CƠ CẤU 5 LOẠI HÌNH VI PHẠM TRỌNG ĐIỂM:
• 1. LIÊN ĐỚI CHIẾM DỤNG: 56,8 Triệu VNĐ (chỉ 4 đơn hàng nhưng số tiền cực lớn!) ➔ Tính chất đặc biệt nghiêm trọng!
• 2. TICK MẤT HÀNG: 41,2 Triệu VNĐ (53 đơn hàng).
• 3. MẤT / THIẾU / TRÁO SẢN PHẨM: 30,9 Triệu VNĐ (76 đơn hàng).
• 4. HÀNG HÓA TRỄ HẠN: 17,7 Triệu VNĐ (69 đơn hàng).
• 5. BỒI THƯỜNG COD: 11,8 Triệu VNĐ (4 đơn hàng).

📍 3. BẢNG 2: PHÂN BỔ TRUY THU THEO TỈNH THÀNH:
• Lâm Đồng: Cần thu 72,5 Tr ₫ (827 ticket | W39: 197,9 Tr ₫, giảm -63,4%).
• Khánh Hòa: Cần thu 69,3 Tr ₫ (296 ticket | W39: 38,3 Tr ₫, TĂNG MẠNH +31,1 Tr ₫ / +81,2% do vụ Bắc Cam Ranh!).
• Đắk Nông: Cần thu 28,3 Tr ₫ (774 ticket | W39: 51,3 Tr ₫, giảm -44,7%).
• Khác / Liên tỉnh: 11,4 Tr ₫ (377 ticket).
• Bình Thuận: 4,8 Tr ₫ (93 ticket).
• Ninh Thuận: 682 ngàn đồng (57 ticket ➔ Kiểm soát gần như tuyệt đối!).

📍 4. BẢNG 3: TOP 4 AM DÍNH TRUY THU NẶNG NHẤT TOÀN VÙNG:
• 🔴 1. NGUYỄN THANH LONG: 51,2 Triệu VNĐ (72 ticket | W39: 18,2 Tr ₫, TĂNG VỌT +33,0 Tr ₫ / +180,8%)
  ➔ ĐIỂM NÓNG CỰC KỲ NGHIÊM TRỌNG: Bưu cục (KHO) Bắc Cam Ranh dính 48,7 Triệu VNĐ (tăng +240,3% WoW!) — VỤ ÁN CHIẾM DỤNG TIỀN HÀNG COD!
• 🔴 2. LÊ VĂN TRƯỜNG: 26,3 Triệu VNĐ (419 TICKET TỒN ĐỌNG — SỐ LƯỢNG TICKET KHỦNG KHIẾP NHẤT TOÀN VÙNG!)
  ➔ Điểm nóng: BC Đơn Dương dính 12,8 Tr ₫ (118 ticket), BC Xuân Hương dính 8,5 Tr ₫ (166 ticket).
• 🔴 3. TRẦN VĂN PHƯỚC: 22,9 Triệu VNĐ (288 ticket | W39: 27,3 Tr ₫)
  ➔ Điểm nóng: BC Quảng Tín dính 13,0 Tr ₫ (72 ticket), BC Kiến Đức dính 9,1 Tr ₫ (196 ticket).
• 🔴 4. HUỲNH THỊ KIM CHI: 21,3 Triệu VNĐ (110 ticket | W39: 58,3 Tr ₫)
  ➔ Điểm nóng: BC Tân Hà Lâm Hà dính trọn 21,3 Tr ₫ (98 ticket).

🎙️ LỜI THOẠI THUYẾT TRÌNH TỰ NHIÊN (KHI BẬT TAB 14 DASHBOARD TRUY THU):
"Kính thưa Ban Giám Đốc và các anh chị AM,
Bước sang Tab 14 Báo cáo Truy thu, đây là con số tác động trực tiếp đến dòng tiền, uy tín pháp lý và lợi nhuận của toàn vùng:
Nhìn vào tổng thể: Tuần W40 này, số tiền cần truy thu thực tế đã giảm 40%, từ 312 triệu xuống còn 187,1 triệu đồng.
TUY NHIÊN, tôi cảnh báo toàn thể cuộc họp: Số tiền vi phạm phát sinh ban đầu lại TĂNG VỌT TỚI 36,5%, từ 317 triệu nhảy lên 433,1 triệu đồng!
Trong đó, nổi cộm lên nhóm hành vi vi phạm: 'Liên đới chiếm dụng' lên tới 56,8 triệu đồng!

Tôi yêu cầu AM Nguyễn Thanh Long ở Khánh Hòa đứng dậy giải trình trực tiếp trước Ban Giám Đốc:
Tại bưu cục Bắc Cam Ranh thuộc cụm quản lý của anh Long:
Số tiền truy thu tuần trước là 14,3 triệu, tuần này đã nhảy vọt lên 48,7 TRIỆU ĐỒNG, tăng tới hơn 240%!
Đây là vụ việc nhân sự bưu cục thu tiền hàng COD của khách nhưng không nộp về quỹ mà cố tình chiếm đoạt!
Một vụ việc có dấu hiệu vi phạm pháp luật hình sự rõ ràng xảy ra ngay trong cụm của anh!
Trưởng bưu cục Bắc Cam Ranh làm gì? AM quản lý kiểm tra giám sát kiểu gì mà để nhân sự ôm gần 50 triệu đồng tiền hàng của công ty biến mất?
Sự việc xảy ra nhiều ngày mà không có biện pháp ngăn chặn kịp thời, đẩy tỉnh Khánh Hòa tuần này tăng vọt tiền truy thu từ 38 triệu lên gần 70 triệu đồng!

Điểm nóng thứ hai là anh Lê Văn Trường ở Lâm Đồng:
Anh Trường nhìn lên màn hình giúp tôi: 419 TICKET TRUY THU TỒN ĐỌNG với số tiền 26,3 triệu đồng!
Tại sao bưu cục Đơn Dương dính 12,8 triệu, bưu cục Xuân Hương dính 8,5 triệu?
419 ticket này là 419 hồ sơ khiếu nại mất hàng, thiếu hàng, tráo hàng trôi nổi từ tuần này qua tuần khác mà anh Trường và Trưởng bưu cục không chịu đối soát, không chịu ra quyết định đền bù, để nhân sự cù nhầy không nộp tiền phạt!
Chị Huỳnh Thị Kim Chi ở Tân Hà Lâm Hà cũng đang dính trọn 21,3 triệu đồng truy thu!

🔍 INSIGHT BẢN CHẤT & GỐC RỄ NGUYÊN NHÂN:
Tại sao tiền truy thu và vi phạm lại phình to như vậy?
1. NGUYÊN NHÂN THỨ NHẤT: BUÔNG LỎNG QUẢN LÝ TÀI CHÍNH TẠI BƯU CỤC (Vụ Bắc Cam Ranh):
Trưởng bưu cục không đối soát sổ sách cuối ngày, cho phép bưu tá nợ tiền COD sang ngày hôm sau mà không có tài sản thế chấp hay cam kết. Nhân viên thấy quản lý lỏng lẻo bèn ôm tiền tiêu xài cá nhân, đến khi số tiền vượt quá khả năng chi trả là bỏ việc trốn tránh!
2. NGUYÊN NHÂN THỨ HAI: BỆNH 'NGÂM TICKET' CỦA AM VÀ ĐIỀU PHỐI (Vụ 419 ticket của anh Trường):
Khi xảy ra mất hàng hay khiếu nại, AM không quyết liệt phân định trách nhiệm bưu cục nào làm mất, shipper nào làm rơi, mà cứ để ticket trôi nổi trên hệ thống. Càng để lâu, nhân sự vi phạm đã nghỉ việc hoặc chuyển đi nơi khác, việc truy thu đền bù trở nên bế tắc!

🎯 QUYẾT SÁCH HÀNH ĐỘNG & MỆNH LỆNH TÁC CHIẾN TUẦN W41:
1. VỤ ÁN BẮC CAM RANH (48,7 TRIỆU ĐỒNG):
   - Giao đích danh AM Nguyễn Thanh Long trực tiếp phối hợp với bộ phận Pháp chế - Thanh tra vùng và Công an địa phương hoàn thiện toàn bộ hồ sơ khởi tố, truy thu dứt điểm 48,7 triệu đồng trước ngày 08/10!
   - Tạm đình chỉ chức vụ Trưởng bưu cục Bắc Cam Ranh để phục vụ công tác điều tra làm rõ trách nhiệm liên đới.
2. XỬ LÝ DỨT ĐIỂM 419 TICKET CỦA ANH TRƯỜNG & 110 TICKET CỦA CHỊ CHI:
   - Tối hậu thư 72 giờ: Anh Lê Văn Trường và chị Huỳnh Thị Kim Chi phải rà soát từng ticket. Đơn nào shipper làm mất thì khấu trừ lương tháng 9; đơn nào lỗi do bưu cục thì Trưởng bưu cục chịu trách nhiệm giải quyết dứt điểm trước ngày 10/10!
3. Phòng Tài chính vùng áp dụng cơ chế tự động phong tỏa hạn mức nợ đối với các bưu cục vi phạm.
4. MỤC TIÊU TUẦN W41: Toàn vùng Nam Trung Bộ phải kéo tổng số tiền cần truy thu từ 187 triệu xuống dưới mốc 100 triệu đồng!
Bây giờ, em xin phép chuyển sang Tab 15 xem tình hình Kinh doanh & Khách hàng F30 ạ!\"
    },'''

with open('scratch/make_final_script.py', 'r', encoding='utf-8') as f:
    content = f.read()

p1 = content.find('    # ----------------------------------------------------\n    # TAB 13: QR CODE & TIỀN MẶT')
p2 = content.find('    # ----------------------------------------------------\n    # TAB 15: KINH DOANH & KHÁCH HÀNG F30')

if p1 != -1 and p2 != -1:
    updated = content[:p1] + new_tab_13_14 + '\n\n' + content[p2:]
    with open('scratch/make_final_script.py', 'w', encoding='utf-8') as f:
        f.write(updated)
    print("SUCCESS: Updated Tab 13 (COD/QR) and Tab 14 (Truy Thu) in make_final_script.py!")
else:
    print(f"ERROR: Could not find markers (p1={p1}, p2={p2})")
