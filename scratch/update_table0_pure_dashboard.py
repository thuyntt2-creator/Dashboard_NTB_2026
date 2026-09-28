import docx, sys, shutil
sys.stdout.reconfigure(encoding='utf-8')

src = 'KICH_BAN_THUYET_TRINH_MOI_NHAT.docx'
doc = docx.Document(src)

# TABLE 0: MỤC I - BÁM SÁT 100% DASHBOARD TỔNG QUAN (KHÔNG CÓ TỈNH)
cell0 = doc.tables[0].rows[0].cells[0]
for p in cell0.paragraphs[1:]:
    p._p.getparent().remove(p._p)

sec1 = [
    '📍 1. BẢNG 10 CHỈ SỐ KPI TOÀN VÙNG TRÊN DASHBOARD (W39 vs W38):',
    '• 1. Sản Lượng Full Hàng: 328.925 đơn (-14.672 đơn / -4,3% WoW so với W38: 343.597 đơn).',
    '• 2. Sản Lượng TikTok Shop (TTS): 72.781 đơn (+4.055 đơn / +5,9% WoW) ➔ Lập đỉnh kỷ lục 22,1% tỷ trọng toàn vùng.',
    '• 3. %GTC Full Hàng: 56,60% (+0,92%p WoW so với W38: 55,68%).',
    '• 4. %GTC TikTok Shop: 57,45% (+3,55%p WoW so với W38: 53,89%) ➔ Lần đầu tiên vượt %GTC Full hàng!',
    '• 5. %ODR Giao Đúng Hẹn: 90,79% (-0,40%p WoW) ➔ Duy trì sát ngưỡng chuẩn cam kết 92%.',
    '• 6. %LTC Lấy Hàng Thành Công: 90,12% (-0,23%p WoW, riêng TTS đạt 94,58%).',
    '• 7. %Rớt Luân Chuyển KTC: 1,52% (-1,81%p WoW) ➔ Giảm hơn 54% lượng đơn rớt (tuần W38 là 3,32%).',
    '• 8. %FD Tỷ Lệ Hoàn Trả: 7,64% ➔ Kiểm soát trong ngưỡng cho phép.',
    '• 9. Tổng Tiền Cần Truy Thu: 174,7 Tr ₫ (chi tiết phân loại 306,9 Tr ₫ trên 4.013 đơn tồn đọng).',
    '• 10. Tỷ Lệ Tiền Mặt COD: 40,1% (-3,0%p WoW) ➔ Tỷ lệ thanh toán số/QR tăng lên 59,9%.',
    '',
    '🎙️ LỜI THOẠI THUYẾT TRÌNH TỔNG QUAN (BÁM SÁT DASHBOARD TAB 1):',
    '\"Kính thưa Ban Giám Đốc cùng toàn thể 18 anh chị Quản lý Vận hành (AM) và các khối phòng ban,',
    '',
    'Mở đầu buổi họp giao ban tuần W39, nhìn vào màn hình Dashboard Tổng quan với 10 thẻ KPI và 2 biểu đồ xu hướng 4 tuần, thay mặt bộ phận điều hành vùng, em xin báo cáo tổng kết những gì chúng ta ĐÃ LÀM ĐƯỢC và CHƯA LÀM ĐƯỢC trong tuần vừa qua:',
    '',
    '✅ CÁI LÀM ĐƯỢC (3 ĐIỂM SÁNG NỔI BẬT TRÊN DASHBOARD):',
    '1. Bứt phá kỷ lục TikTok Shop: Trên biểu đồ xu hướng sản lượng, trong khi Full hàng giảm -4,3% (đạt 328.925 đơn) do hàng B2C hạ nhiệt, thì TikTok Shop lại đi ngược chiều tăng vọt +5,9% WoW, chính thức xác lập đỉnh mới 72.781 đơn và chiếm tới 22,1% tổng sản lượng toàn vùng. Điều này cho thấy dòng hàng TMĐT đang là trụ cột giữ nhịp tăng trưởng cho Nam Trung Bộ.',
    '2. Chất lượng giao hàng sàn vượt trội: Trên biểu đồ chất lượng, %GTC của TikTok Shop tuần này nhảy vọt +3,55%p lên 57,45%, chính thức vượt qua tỷ lệ GTC của hàng Full (56,60%). Khâu lấy hàng First-mile TTS tiếp tục duy trì phong độ rất cao với %LTC đạt 94,6%.',
    '3. Thắng lợi ở khâu vận tải KTC: Tỷ lệ rớt luân chuyển giảm sâu kỷ lục từ 3,32% xuống còn 1,52% (-1,81%p WoW, giảm hơn một nửa lượng đơn rớt). Đây là kết quả của việc siết chặt kỷ luật giao nhận xe tải trục tại các bưu cục và kho trung chuyển.',
    '',
    '❌ CÁI CHƯA LÀM ĐƯỢC (2 ĐIỂM NGHẼN BÁO ĐỘNG TRÊN DASHBOARD):',
    '1. Chỉ số GTC tổng vẫn chưa chạm ngưỡng mục tiêu 60%: Mặc dù có cải thiện (+0,92%p), nhưng mức 56,60% cho thấy áp lực giao hàng ca chiều và xử lý tồn kho tại nhiều bưu cục vẫn chưa đạt yêu cầu.',
    '2. Chi phí truy thu và tồn đọng cao: Thẻ truy thu ghi nhận số tiền phát sinh lớn, chủ yếu bắt nguồn từ 2 lỗi vận hành: đơn tồn đọng giao hàng quá hạn và tồn đọng luân chuyển hàng trả về.',
    '',
    '🎯 TRỌNG TÂM ĐIỀU HÀNH TUẦN W40:',
    'Toàn mạng lưới tập trung: Đẩy %GTC toàn vùng tiệm cận mốc 60%, duy trì tỷ lệ rớt KTC dưới 1,8%, và giải quyết triệt để các bưu cục nghẽn tải. Sau đây, em xin chuyển sang Tab 2 để bóc tách chi tiết theo từng Tỉnh và từng AM.\"'
]
for line in sec1:
    p = cell0.add_paragraph()
    p.text = line

doc.save(src)
for c in ['KICH_BAN_THUYET_TRINH_W39_INSIGHT_CHUYEN_SAU.docx', 'KICH_BAN_THUYET_TRINH_W39_NAM_TRUNG_BO.docx']:
    shutil.copyfile(src, c)

print('Updated Table 0 successfully without provinces!')
