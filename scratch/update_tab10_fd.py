# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

new_tab_fd = '''    # ----------------------------------------------------
    # TAB 10: %FD HOÀN TRẢ (FAIL DELIVERY / RETURN RATE)
    # ----------------------------------------------------
    {
        "id": "tab-fd",
        "title": "🗣️ PHÂN TÍCH CHUYÊN SÂU TỶ LỆ HOÀN TRẢ %FD (RETURN RATE) & BÓC TRẦN CHIÊU TRÒ XẢ TỒN (BẬT TAB 10 DASHBOARD):",
        "content": """📍 1. BẢNG TỔNG QUAN TỶ LỆ HOÀN TRẢ TOÀN VÙNG (W40):
• TỔNG TOÀN VÙNG: 7,77% (W39: 7,54%, tăng nhẹ +0,23%p | 24.498 đơn return / 315.328 đơn phát sinh; 86 bưu cục).
  - Phân khúc Full hàng: 7,77% (Hoàn trả 24.498 đơn).
  - Phân khúc TikTok Shop (TTS): Kiểm soát tốt hơn ở mức 6,10% (Hoàn trả 4.410 đơn / 72.253 đơn phát sinh).
• Đánh giá thiệt hại: 24.498 đơn hoàn trả đồng nghĩa với việc chúng ta tốn chi phí vận chuyển 2 chiều đi - về, mất trắng doanh thu cước, và tạo ra làn sóng khiếu nại gay gắt từ các chủ shop!

📍 2. BẢNG 1: XẾP HẠNG 18 AM THEO %FD TỶ LỆ HOÀN TRẢ:
• 🟢 TOP 6 AM KIỂM SOÁT HOÀN TRẢ TỐT NHẤT VÙNG (%FD THẤP < 7.0% — TUYÊN DƯƠNG):
  1. Lê Thanh Nhựt (Bình Thuận): 5,63% (TTS: 4,97% | Vol 29.660 đơn — chỉ hoàn 1.670 đơn) ➔ Quán quân giữ hàng và giao thành công toàn vùng!
  2. Cao Thị Thanh Thủy (Khánh Hòa): 5,98% (TTS: 5,27% | Vol 16.493 đơn — hoàn 987 đơn).
  3. Nguyễn Đỗ Minh Nghĩa (Lâm Đồng): 5,99% (TTS: 5,26% | Vol 7.825 đơn — hoàn 469 đơn) ➔ Điểm sáng hiếm hoi tại Lâm Đồng.
  4. Nguyễn Duy Long (Ninh Thuận): 6,51% (TTS: 5,76% | Gánh sản lượng khủng 42.208 đơn mà chỉ hoàn 2.748 đơn).
  5. Nguyễn Thị Tuyết Thơ (Lâm Đồng): 6,82% (TTS: 6,01% | Vol 9.453 đơn — hoàn 645 đơn).
  6. Lê Thị Kim Chi (Lâm Đồng): 7,11% (TTS: 6,26% | Vol 11.900 đơn — hoàn 846 đơn).
• 🔴 TOP 3 AM BÁO ĐỘNG ĐỎ CỰC NẶNG (%FD TRÊN 20% — GẤP GẦN 3 LẦN MỨC BÌNH QUÂN VÙNG!):
  1. Trương Quang Linh (Đắk Nông): 22,95% (TTS: 20,19% | Vol 1.656 đơn — hoàn tới 380 đơn!) ➔ Tỷ lệ hoàn trả cao nhất toàn vùng!
  2. Lê Minh Lợi (Lâm Đồng): 21,04% (TTS: 18,52% | Vol 2.110 đơn — hoàn 444 đơn!).
  3. Phan Nguyễn Yến Nhi (Lâm Đồng): 20,99% (TTS: 18,59% | Vol 3.111 đơn — hoàn tới 653 đơn!).

📍 3. BẢNG 2: TOP 10 BƯU CỤC ĐIỂM NÓNG CÓ TỶ LỆ HOÀN TRẢ CAO NHẤT VÙNG:
• 1. (DNO) Quảng Tín: 22,95% (Hoàn 380 / 1.656 đơn) | AM Trương Quang Linh
• 2. (LDO) Lang Biang - Đà Lạt 1: 21,04% (Hoàn 444 / 2.110 đơn | Tăng +4,78%p WoW) | AM Lê Minh Lợi (Cảnh báo đỏ 108 ngày!)
• 3. (LDO) Đơn Dương: 20,99% (Hoàn 653 / 3.111 đơn | TĂNG ĐỘT BIẾN +11,00%p WoW!) | AM Phan Nguyễn Yến Nhi
• 4. (LDO) Đức Trọng 1: 20,53% (Hoàn 334 / 1.627 đơn | TĂNG MẠNH +8,21%p WoW!) | AM Nguyễn Lê Nguyên Vũ
• 5. (DNO) Kiến Đức: 16,71% (Hoàn 320 / 1.915 đơn) | AM Hồng Bích Nga
• 6. (KHO) Cam Linh: 15,33% (Hoàn 579 / 3.776 đơn) | AM Nguyễn Thanh Long
• 7. (DNO) Đông Gia Nghĩa: 13,72% (Hoàn 275 / 2.004 đơn) | AM Huỳnh Thúc Duân
• 8. (DNO) Tuy Đức: 13,43% (Hoàn 202 / 1.504 đơn | Tăng +2,02%p) | AM Trần Thị Nhung
• 9. (KHO) Nha Trang: 13,17% (Hoàn 696 / 5.283 đơn | Tăng vọt +5,16%p) | AM Phan Đình Duy
• 10. (KHO) Tây Nha Trang: 12,80% (Hoàn 463 / 3.616 đơn) | AM Phan Đình Duy

🎙️ LỜI THOẠI THUYẾT TRÌNH TỰ NHIÊN (KHI BẬT TAB 10 DASHBOARD %FD HOÀN TRẢ):
"Kính thưa Ban Giám Đốc và toàn thể các anh chị AM,
Bước sang Tab 10 là chỉ số %FD - Tỷ lệ đơn hàng hoàn trả về người gửi:
Trong tất cả các chỉ số vận hành Last-mile, đây là con số gây lãng phí và bào mòn lợi nhuận khủng khiếp nhất: Một đơn hàng giao thất bại phải hoàn trả đồng nghĩa với việc chúng ta tốn gấp đôi chi phí vận tải 2 chiều, mất trắng toàn bộ doanh thu, và khiến chủ shop ức chế quay lưng bỏ sang đối thủ!
Bình quân tuần W40 toàn vùng chúng ta ghi nhận tỷ lệ hoàn trả là 7,77% với gần 24.500 đơn hàng bị trả về.
Trước hết, em xin biểu dương nhóm 6 AM kiểm soát hoàn trả cực kỳ xuất sắc:
Anh Lê Thanh Nhựt ở Bình Thuận: %FD chỉ 5,63% trên quy mô gần 30 ngàn đơn!
Chị Cao Thị Thanh Thủy ở Khánh Hòa chỉ 5,98%, anh Minh Nghĩa ở Lâm Đồng chỉ 5,99%, và anh Nguyễn Duy Long gánh hơn 42 ngàn đơn mà tỷ lệ hoàn chỉ 6,51%!
Anh em làm tuyến rất khéo, bưu tá kiên trì liên hệ khách, hỗ trợ giao lại ngoài giờ nên giữ được tỷ lệ giao thành công rất cao.

TUY NHIÊN, tôi yêu cầu 4 AM: Trương Quang Linh, Lê Minh Lợi, Phan Nguyễn Yến Nhi và Nguyễn Lê Nguyên Vũ nhìn thẳng lên màn hình Bảng 2 giúp tôi:
Các anh chị giải thích thế nào khi tỷ lệ hoàn trả tại 4 bưu cục của các anh chị VƯỢT QUA MỐC 20% — CAO GẤP GẦN 3 LẦN MỨC BÌNH QUÂN VÙNG?
Bưu cục Quảng Tín của anh Linh: 22,95%! Cứ 4 đơn giao thì trả về gần 1 đơn!
Bưu cục Lang Biang - Đà Lạt 1 của anh Lợi: 21,04%, tăng thêm gần 5%p so với tuần trước!
Bưu cục Đơn Dương của chị Yến Nhi: 20,99% với 653 đơn bị trả về, TĂNG SỐC TỚI 11%p CHỈ TRONG 1 TUẦN!
Và bưu cục Đức Trọng 1 của anh Vũ: 20,53%, tăng vọt hơn 8%p!

🔍 INSIGHT BẢN CHẤT & BÓC TRẦN CHIÊU TRÒ HIỆN TRƯỜNG:
Tại sao tỷ lệ hoàn trả ở 4 bưu cục này lại tăng vọt bất thường như vậy?
Qua kiểm tra dữ liệu đối soát thực tế, tôi chỉ ra 3 nguyên nhân cốt tử:
1. NGUYÊN NHÂN THỨ NHẤT: CHIÊU TRÒ 'BẤM HOÀN TRẢ KHỐNG ĐỂ XẢ TỒN BƯU CỤC':
Bưu cục Đơn Dương và Đức Trọng 1 tuần vừa qua dính lượng hàng tồn Aging quá lớn (hơn 1.200 đơn backlog). Trưởng bưu cục bị dí KPI tồn kho, bị nhắc nhở giải tỏa, bèn chọn con đường tắt tiêu cực: Cho nhân viên và bưu tá đồng loạt quét duyệt hoàn trả hàng loạt đơn tồn lưu cữu với lý do 'Khách từ chối nhận' để đẩy hàng lên xe tải KTC trả về kho trung tâm nhằm 'làm sạch kho' trên hệ thống!
Đây là hành vi đối phó số liệu cực kỳ nghiêm trọng, biến áp lực tồn kho của bưu cục thành thiệt hại tiền cước và mất uy tín của công ty!
2. NGUYÊN NHÂN THỨ HAI: HỆ LỤY CỦA GIAO TRỄ ODR VÙNG NÚI:
Như chúng ta vừa mổ xẻ ở Tab 6, ODR hàng TikTok Shop tại Lang Biang của anh Lợi chỉ có 14%, tại Quảng Tín của anh Linh chỉ có 42%. Khách hàng đặt mua món đồ trên mạng, hẹn 2 ngày giao nhưng shipper ngâm tới ngày thứ 5 mới mang tới. Lúc đó khách hàng họ đã đi mua ngoài chợ hoặc không còn nhu cầu nữa, nên họ từ chối nhận hàng thẳng thừng! Giao trễ chính là nguyên nhân trực tiếp đẻ ra hoàn trả!
3. NGUYÊN NHÂN THỨ BA: SHIPPER NÉ TUYẾN ĐỒI NÚI ĐƯỜNG ĐẤT SÌNH LẦY:
Tuyến sâu Đơn Dương, Lang Biang, Quảng Tín vào mùa mưa đường đất trơn trượt, dốc đứng. Bưu tá đứng ở ngoài đường nhựa nhá máy 1 tiếng rồi cúp ngay, khách chưa kịp bắt máy đã bấm 'Không liên lạc được', sau 3 lần là tự động hoàn về kho!

🎯 QUYẾT SÁCH HÀNH ĐỘNG & MỆNH LỆNH TÁC CHIẾN TUẦN W41:
1. THIẾT LẬP NGAY QUY TRÌNH 3 BƯỚC PHÊ DUYỆT HOÀN TRẢ TẠI 4 BƯU CỤC ĐIỂM NÓNG:
   - Bước 1: Shipper bấm đề xuất hoàn trả phải có lịch sử cuộc gọi tối thiểu 3 lần vào 3 khung giờ khác nhau (Sáng - Trưa - Chiều).
   - Bước 2: Nhân viên CS bưu cục hoặc Trưởng bưu cục bắt buộc phải trực tiếp gọi điện lại cho người nhận xác nhận đúng lý do khách từ chối trước khi bấm duyệt hoàn trên hệ thống.
   - Bước 3: Nghiêm cấm tuyệt đối Trưởng bưu cục tự ý duyệt hoàn hàng loạt để xả tồn! Phòng Vận hành vùng sẽ audit ngẫu nhiên 100 cuộc gọi hoàn trả tại Đơn Dương và Quảng Tín. Nếu phát hiện bấm hoàn khống, lập biên bản kỷ luật sa thải nhân sự vi phạm!
2. Bố trí chuyến giao bù ca chiều tối đối với các đơn khách hẹn lùi ngày, tận dụng khung giờ khách ở nhà để cứu vãn đơn hàng.
3. GIAO CHỈ TIÊU TUẦN W41: Anh Linh, anh Lợi, chị Nhi, anh Vũ bắt buộc phải kéo tỷ lệ %FD của Quảng Tín, Lang Biang, Đơn Dương, Đức Trọng 1 từ trên 20% xuống dưới mốc 12%!
Bây giờ, em xin phép chuyển sang Tab 11 xem Báo cáo điều hành KTC & Vận tải đường trục ạ!\""""
    },'''

with open('scratch/make_final_script.py', 'r', encoding='utf-8') as f:
    content = f.read()

p1 = content.find('    # ----------------------------------------------------\n    # TAB 10: %FD HOÀN TRẢ')
p2 = content.find('    # ----------------------------------------------------\n    # TAB 11: KTC & VẬN TẢI')

if p1 != -1 and p2 != -1:
    updated = content[:p1] + new_tab_fd + '\n\n' + content[p2:]
    with open('scratch/make_final_script.py', 'w', encoding='utf-8') as f:
        f.write(updated)
    print("SUCCESS: Updated Tab 10 FD in make_final_script.py!")
else:
    print(f"ERROR: Could not find markers (p1={p1}, p2={p2})")
