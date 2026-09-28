import docx
import sys
sys.stdout.reconfigure(encoding='utf-8')

table15_content = """🗣️ CHUYÊN ĐỀ THEO DÕI & XỬ LÝ BƯU CỤC CẢNH BÁO BẤT ỔN (%GTC < 45% HOẶC GIẢM SÂU) — SO SÁNH ĐỐI CHIẾU TUẦN W38 vs W39:

📍 1. TỔNG QUAN BIẾN ĐỘNG TOÀN VÙNG (W38 vs W39):
• Tổng số bưu cục cảnh báo: Tuần W38 toàn vùng có 13 bưu cục, sang tuần W39 tăng lên 15 bưu cục (tăng ròng +2 bưu cục).
• Cơ cấu biến động 3 nhóm: Có 4 bưu cục nỗ lực giải tỏa dứt điểm và thoát cảnh báo thành công, nhưng lại phát sinh 6 bưu cục mới rơi vào diện báo động, và 9 bưu cục đang kẹt dai dẳng cả 2 tuần liên tiếp.

👤 2. BÓC TÁCH CHI TIẾT 3 NHÓM BƯU CỤC BIẾN ĐỘNG THEO TUẦN (W38 vs W39):

🟢 NHÓM 1: TUYÊN DƯƠNG 4 BƯU CỤC THOÁT CẢNH BÁO THÀNH CÔNG (W38 🚨 ➔ W39 ✅):
  1. BC Xuân Hương - Đà Lạt (Lâm Đồng): %GTC tăng mạnh từ 42,1% lên 51,8% (+9,7%p) ➔ Giải tỏa sạch backlog tồn đọng, gán ca 1 đạt 94%.
  2. BC Cam Linh (Khánh Hòa): %GTC từ 36,7% nhảy vọt lên 48,5% (+11,8%p) ➔ Ổn định lại đội bưu tá tuyến Cam Ranh, thoát hiểm xuất sắc.
  3. BC Nhân Cơ (Đắk Nông): %GTC từ 43,5% vọt lên 52,3% (+8,8%p) ➔ Phục hồi nhịp xuất tuyến đúng giờ, vượt ngưỡng an toàn >50%.
  4. BC Tây Nha Trang (Khánh Hòa): %GTC từ 44,1% lên 49,6% (+5,5%p) ➔ Tối ưu giao ca sáng trước 11h00, xử lý sạch backlog luân chuyển.

🔴 NHÓM 2: BÁO ĐỘNG ĐỎ 6 BƯU CỤC MỚI RƠI VÀO DIỆN CẢNH BÁO TUẦN W39 (W38 ✅ ➔ W39 🚨):
  5. BC D'Ran (Lâm Đồng): %GTC sụt từ 48,2% xuống 36,9% (-11,3%p) ➔ Địa bàn đèo dốc sạt lở, thiếu hụt 2 bưu tá tuyến xa.
  6. BC Lang Biang 2 (Lâm Đồng): %GTC giảm từ 47,8% về 35,8% (-12,0%p) ➔ Áp lực hàng TikTok Shop đổ về vượt công suất xử lý.
  7. BC Trường Xuân (Đắk Nông): %GTC tụt từ 49,0% xuống 38,2% (-10,8%p) ➔ Tuyến giao xa, tỷ lệ không liên lạc được tăng vọt.
  8. BC Đông Gia Nghĩa (Đắk Nông): %GTC từ 47,1% tụt về 44,9% (-2,2%p) ➔ Chớm rớt dưới ngưỡng 45%, gán ca 2 rất yếu.
  9. BC Bắc Cam Ranh (Khánh Hòa): %GTC đạt 44,7% (-1,8%p), trễ hạn giao phát.
  10. BC Phú Quý (Bình Thuận): %GTC đạt 50,8%, giảm sâu so với mốc lịch sử 88,5% do phụ thuộc lịch trình tàu cao tốc biển.

⚠️ NHÓM 3: ĐIỂM NÓNG MÃN TÍNH 9 BƯU CỤC KẸT DAI DẲNG CẢ 2 TUẦN (W38 🚨 ➔ W39 🚨):
  11. BC Lâm Viên - Đà Lạt 2 (Lâm Đồng): THẢM HỌA VẬN HÀNH LỚN NHẤT MẠNG! Từ 46,2% ở W38 rơi tự do xuống 19,55% ở W39 (-26,6%p). Bưu tá tê liệt ca chiều, không xuất tuyến.
  12. BC Đức Trọng 1 (Lâm Đồng): %GTC kẹt cứng ở 23,8% (W38: 23,9%), backlog lưu cữu tồn đọng.
  13. BC Quảng Tín (Đắk Nông): %GTC đạt 26,2% (W38: 18,1%), tích lũy kỷ lục >100 ngày cảnh báo.
  14. BC Đơn Dương (Lâm Đồng): %GTC rơi tự do từ 45,3% xuống 29,0% (-16,3%p), năng suất ca chiều chạm đáy.
  15. BC Lang Biang 1 (Lâm Đồng): %GTC ở mức 30,6% (W38: 32,8%), quá tải hàng cồng kềnh.
  16. BC Kiến Đức (Đắk Nông): %GTC ở mức 32,5% (W38: 35,6%), bán kính phát rộng >25km đường đồi núi.
  17. BC Tân Hà Lâm Hà (Lâm Đồng): %GTC đạt 36,8% (W38: 38,2%), tồn đọng hàng nông sản sai quy cách.
  18. BC Tuy Đức (Đắk Nông): %GTC đạt 38,5% (W38: 41,5%), hạ tầng mạng chập chờn.
  19. BC Di Linh (Lâm Đồng): %GTC đạt 40,6% (W38: 44,2%), tỷ lệ hoàn hàng cao.

🎯 3. KẾ HOẠCH HÀNH ĐỘNG CẤP BÁCH TUẦN W40 (3 MỆNH LỆNH TÁC CHIẾN):
• Mệnh lệnh 1 - Cap Volume (Điều tiết tải): Tạm thời giảm 25% hạn mức chia chọn hàng về trong 3 ngày đầu tuần tại BC Lâm Viên 2 và Quảng Tín để bưu tá dồn 100% sức quét sạch hàng tồn kho và aging >5 ngày.
• Mệnh lệnh 2 - Chi viện Ca 1: Điều chuyển ngay 4 bưu tá cứng từ cụm Xuân Hương và Gia Nghĩa sang chi viện phát lượt 1 trước 11h00 trưa tại Lâm Viên 2 và Đức Trọng 1; nâng %GTC ca 1 sáng từ 41% lên ≥70%.
• Mệnh lệnh 3 - Cam kết KPI Vùng W40: Triển khai tổ phản ứng nhanh giám sát real-time từng giờ; quyết tâm kéo tối thiểu 5 bưu cục thoát cảnh báo trong tuần W40, đưa tổng số bưu cục bất ổn toàn vùng từ 15 về dưới 10 bưu cục!"""

for fn in ['KICH_BAN_THUYET_TRINH_MOI_NHAT.docx', 'KICH_BAN_THUYET_TRINH_W39_INSIGHT_CHUYEN_SAU.docx']:
    try:
        doc = docx.Document(fn)
        if len(doc.tables) > 15:
            t15 = doc.tables[15]
            t15.rows[0].cells[0].text = table15_content
            doc.save(fn)
            print(f"Updated Table 15 in {fn} successfully.")
        else:
            print(f"File {fn} has less than 16 tables.")
    except Exception as e:
        print(f"Error updating {fn}: {e}")
