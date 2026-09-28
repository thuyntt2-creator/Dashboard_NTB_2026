import docx
import sys
sys.stdout.reconfigure(encoding='utf-8')

table9_content = """🗣️ PHÂN TÍCH TỶ LỆ HOÀN TRẢ (%FD) — PHÂN HÓA 4 AM VƯỢT TRẦN 10% & ĐIỂM NÓNG QUẢNG TÍN, LANG BIANG (W39 vs W38):

📍 1. BẢNG TỔNG QUAN TỶ LỆ HOÀN TRẢ TOÀN VÙNG (W39 vs W38):
• Toàn Vùng (Full Luồng): Tỷ lệ hoàn trả bình quân đạt 7,64% (25.993 đơn hoàn / 340.199 đơn giao xử lý kỳ hoàn), tăng nhẹ +0,10%p so với W38 (7,54%), vẫn nằm trong trần kiểm soát chung toàn mạng (≤ 8,0%).
• Riêng TikTok Shop (TTS): Tỷ lệ hoàn trả kiểm soát cực tốt ở mức 6,10% (4.191 đơn hoàn / 68.719 đơn giao TTS), giảm mạnh -0,70%p so với tuần W38 (6,80%). Hàng sàn TMĐT TikTok Shop đang được giao nhận và hạn chế hoàn trả tốt hơn luồng ngoài 1,54%p!

👤 2. BÓC TÁCH CHI TIẾT THEO AM — PHÂN ĐỊNH 3 NHÓM KIỂM SOÁT HOÀN:

🔴 NHÓM BÁO ĐỘNG ĐỎ (TỶ LỆ HOÀN TRÊN 10% — CỰC KỲ NGUY HIỂM): Gồm 4 AM:
  1. AM Trương Quang Linh: Hoàn trả kỷ lục 29,54% (605 đơn hoàn / 2.048 đơn giao, TTS hoàn 25,95%) ➔ Gần 30% hàng xuất kho bị hoàn trả! Tâm điểm là bưu cục (DNO) Quảng Tín.
  2. AM Lê Minh Lợi: Hoàn trả 25,54% (715 đơn hoàn / 2.800 đơn giao, TTS hoàn 22,53%) ➔ Hơn 1/4 lượng hàng bị hoàn về shop, tăng vọt +9,27%p WoW! Tâm điểm bưu cục (LDO) Lang Biang - Đà Lạt 1.
  3. AM Nguyễn Thanh Long (Cam Ranh): Hoàn trả 11,47% (1.730 đơn hoàn / 15.081 đơn giao), tâm điểm là bưu cục (KHO) Cam Linh rớt hoàn tới 1.144 đơn (16,50%).
  4. AM Lê Văn Trường (Lâm Đồng): Hoàn trả 10,90% (2.839 đơn hoàn / 26.043 đơn giao), tăng vọt do hai bưu cục Đơn Dương (19,32%) và Lâm Viên 2 (17,84%).

🟡 NHÓM CẦN THEO DÕI SÁT (TỶ LỆ HOÀN TỪ 8,0% - 10,0%):
  5. AM Nguyễn Lê Nguyên Vũ: Hoàn 9,26% (1.157/12.490 đơn), vướng bưu cục Đức Trọng 1 hoàn 17,24%.
  6. AM Phan Đình Duy: Hoàn 8,77% (2.027/23.121 đơn).
  7. AM Trần Thị Nhung: Hoàn 8,40% (2.054/24.457 đơn), vướng bưu cục Tuy Đức (11,47%) và Quảng Khê (10,61%).
  8. AM Huỳnh Thúc Duân: Hoàn 8,24% (409/4.966 đơn), vướng Đông Gia Nghĩa (11,28%).

🟢 NHÓM KIỂM SOÁT HOÀN TRẢ XUẤT SẮC (DƯỚI 7,5% — AN TOÀN TUYỆT ĐỐI):
  9. AM Nguyễn Hoàng Phi: Hoàn 7,32% (1.735/23.687 đơn).
  10. AM Thái Thị Thanh Thư: Hoàn 7,00% (2.379/33.977 đơn).
  11. AM Hồng Bích Nga: Hoàn 6,95% (1.418/20.398 đơn).
  12. AM Nguyễn Đỗ Minh Nghĩa: Hoàn 6,85% (539/7.865 đơn).
  13. AM Nguyễn Duy Long (Ninh Thuận): Hoàn 6,51% (2.763/42.469 đơn) — Quản lý sản lượng lớn nhất toàn vùng nhưng tỷ lệ hoàn giữ ở mức rất an toàn!
  14. AM Nguyễn Thị Tuyết Thơ: Hoàn 6,49% (580/8.934 đơn).
  15. AM Lê Thị Kim Chi: Hoàn 6,37% (763/11.979 đơn).
  16. AM Cao Thị Thanh Thủy (Bình Thuận): Hoàn 6,01% (972/16.186 đơn).
  17. AM Lê Thanh Nhựt (Bình Thuận): Hoàn 5,80% (1.700/29.325 đơn).
  18. AM Nguyễn Văn Khánh (Nha Trang): Hoàn thấp nhất toàn vùng chỉ 4,66% (1.234/26.505 đơn) ➔ Quán quân kiểm soát giao thành công và hạn chế hoàn trả!

🔍 3. INSIGHT VẬN HÀNH & TOP 10 BƯU CỤC CÓ TỶ LỆ HOÀN CAO NHẤT:
• Danh sách 10 bưu cục điểm nóng hoàn trả toàn vùng:
  1. (DNO) Quảng Tín (AM Linh): Hoàn 29,54% (605/2.048 đơn).
  2. (LDO) Lang Biang - Đà Lạt 1 (AM Lợi): Hoàn 25,54% (715/2.800 đơn).
  3. (LDO) Đơn Dương (AM Trường): Hoàn 19,32% (840/4.348 đơn).
  4. (LDO) Lâm Viên - Đà Lạt 2 (AM Trường): Hoàn 17,84% (550/3.083 đơn).
  5. (LDO) Đức Trọng 1 (AM Vũ): Hoàn 17,24% (333/1.932 đơn).
  6. (KHO) Cam Linh (AM Long Cam Ranh): Hoàn 16,50% (1.144/6.935 đơn).
  7. (DNO) Kiến Đức (AM Nga): Hoàn 12,90% (348/2.698 đơn).
  8. (DNO) Tuy Đức (AM Nhung): Hoàn 11,47% (200/1.743 đơn).
  9. (DNO) Đông Gia Nghĩa (AM Duân): Hoàn 11,28% (202/1.791 đơn).
  10. (DNO) Quảng Khê (AM Nhung): Hoàn 10,61% (161/1.517 đơn).
• Bản chất vấn đề hiện trường: 
  - Toàn bộ 10 bưu cục hoàn cao nhất đều nằm tại Đắk Nông, vùng đồi núi Lâm Đồng và huyện xa Cam Lâm/Cam Ranh.
  - Shipper tại các tuyến xa có biểu hiện nản giao, gọi điện 1 cuộc không nghe máy là bấm ngay lý do 'Khách từ chối nhận' hoặc 'Không liên lạc được 3 lần' để hợp thức hóa việc chuyển hoàn (hoàn ảo).
  - Tỷ lệ hoàn vọt lên 25% - 30% như tại Quảng Tín và Lang Biang là bất bình thường, ảnh hưởng nghiêm trọng đến uy tín của GHN với các Shop lớn và sàn TMĐT!

🎯 4. CHỈ ĐẠO HÀNH ĐỘNG & GIAO NHIỆM VỤ TÁC CHIẾN ĐÍCH DANH:
• Anh Trương Quang Linh và anh Lê Minh Lợi: Thiết lập tổ kiểm soát độc lập tại Quảng Tín và Lang Biang 1. Bắt buộc Trưởng bưu cục phải gọi điện phúc tra xác suất 100% các đơn bấm lý do hoàn trả trước khi duyệt cho hàng quay đầu KTC. Bưu tá nào bấm hoàn khống lập tức lập biên bản xử phạt và đình chỉ tuyến.
• Anh Lê Văn Trường: Xử lý dứt điểm tình trạng hoàn tăng đột biến tại Đơn Dương (19,3%) và Lâm Viên 2 (17,8%), rà soát lại chất lượng giao hàng của đội bưu tá tuyến huyện.
• Anh Nguyễn Thanh Long (Cam Ranh): Tập trung chấn chỉnh bưu cục Cam Linh (1.144 đơn hoàn), phân loại rõ lý do hoàn của nhóm hàng nông sản/hải sản và nhóm hàng thông thường để có biện pháp can thiệp sớm."""

for fn in ['KICH_BAN_THUYET_TRINH_MOI_NHAT.docx', 'KICH_BAN_THUYET_TRINH_W39_INSIGHT_CHUYEN_SAU.docx']:
    try:
        doc = docx.Document(fn)
        if len(doc.tables) > 9:
            t9 = doc.tables[9]
            t9.rows[0].cells[0].text = table9_content
            doc.save(fn)
            print(f"Updated Table 9 in {fn} successfully.")
        else:
            print(f"File {fn} has less than 10 tables.")
    except Exception as e:
        print(f"Error updating {fn}: {e}")
