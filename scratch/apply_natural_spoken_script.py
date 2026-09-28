import docx, sys, shutil
sys.stdout.reconfigure(encoding='utf-8')

src = 'KICH_BAN_THUYET_TRINH_MOI_NHAT.docx'
doc = docx.Document(src)

# TABLE 0: MỤC I - GIỌNG ĐIỆU NÓI TỰ NHIÊN, THỰC TẾ (BÁM SÁT DASHBOARD TAB 1)
cell0 = doc.tables[0].rows[0].cells[0]
for p in cell0.paragraphs[1:]:
    p._p.getparent().remove(p._p)

sec1 = [
    '📍 1. BẢNG 10 CHỈ SỐ NHANH TRÊN MÀN HÌNH DASHBOARD (W39 vs W38):',
    '• 1. Sản Lượng Full Hàng: 328.925 đơn (-14.672 đơn / -4,3% so với W38).',
    '• 2. Sản Lượng TikTok Shop: 72.781 đơn (+4.055 đơn / +5,9%) ➔ Đạt đỉnh 22,1% tỷ trọng toàn vùng.',
    '• 3. %GTC Full Hàng: 56,60% (+0,92%p so với W38).',
    '• 4. %GTC TikTok Shop: 57,45% (+3,55%p) ➔ Lần đầu tiên vượt %GTC hàng Full.',
    '• 5. %ODR (Đúng Hẹn): 90,79% (giảm nhẹ -0,40%p, giữ sát mốc 92%).',
    '• 6. %LTC (Lấy Hàng): 90,12% (riêng TTS đạt 94,58%).',
    '• 7. %Rớt Luân Chuyển KTC: 1,52% (giảm hơn một nửa so với 3,32% tuần trước).',
    '• 8. %FD (Hoàn Trả): 7,64% (ở ngưỡng an toàn).',
    '• 9. Tổng Tiền Cần Truy Thu: 174,7 Tr ₫ (chi tiết phân loại 306,9 Tr ₫ / 4.013 đơn).',
    '• 10. Tỷ Lệ Tiền Mặt COD: 40,1% (giảm 3,0%p, tỷ lệ thanh toán chuyển khoản/QR tăng lên gần 60%).',
    '',
    '🎙️ LỜI THOẠI THUYẾT TRÌNH TỰ NHIÊN (KHI BẬT TAB 1 DASHBOARD TỔNG QUAN):',
    '\"Dạ em chào Ban Giám Đốc, chào các anh chị AM và các phòng ban.',
    '',
    'Mở đầu buổi họp giao ban tuần W39, mọi người cùng nhìn lên màn hình Dashboard Tổng quan giúp em. Tuần này với 10 thẻ KPI và 2 biểu đồ xu hướng 4 tuần, em xin tóm tắt nhanh những điểm làm được và chưa làm được của vùng mình:',
    '',
    'Về mặt sản lượng, tuần này toàn vùng đi được gần 329 ngàn đơn Full hàng, giảm nhẹ khoảng 4% so với tuần trước. Tuy nhiên, nhìn sâu vào các chỉ số vận hành thì có 3 điểm sáng rất rõ ràng:',
    '',
    'Thứ nhất là ở kênh TikTok Shop: Mọi người nhìn cái thẻ màu xanh này, đơn TikTok tuần này chạm đỉnh gần 73 ngàn đơn, tăng gần 6% và chiếm tới hơn 22% sản lượng toàn vùng mình rồi. Đơn sàn đang gánh số rất tốt cho mình trong lúc hàng truyền thống giảm. Đặc biệt là tỷ lệ giao thành công của TikTok tuần này kéo lên được hơn 57%, tăng hơn 3.5% và lần đầu tiên vượt luôn cả hàng Full. Khâu lấy hàng First-mile thì các anh chị bưu cục vẫn giữ phong độ tốt, trên 94%.',
    '',
    'Điểm sáng thứ hai là ở khâu vận chuyển KTC: Tuần này anh em làm rất tốt nha. Tỷ lệ rớt luân chuyển tuần trước tới 3.3% thì tuần này rớt xuống còn 1.5%, tức là giảm hơn một nửa lượng đơn bị rớt. Các bưu cục với kho trung chuyển đã phối hợp bàn giao ca rất khớp, không còn bị rớt hàng nhiều như tuần trước nữa.',
    '',
    'Tuy nhiên, nhìn qua 2 cái thẻ bên phải, mình vẫn còn 2 vấn đề lớn phải xử lý ngay:',
    '',
    'Thứ nhất là GTC tổng cả vùng vẫn mới ngấp nghé 56.6%, chưa qua được cái mốc 60% Sếp giao. Chủ yếu là anh em vẫn còn bị đuối ở ca chiều và đơn tồn từ hôm trước dồn qua.',
    '',
    'Thứ hai là thẻ truy thu tuần này nhảy lên con số khá lớn, hơn 300 triệu phát sinh. Đa phần là do lỗi để đơn tồn quá hạn giao với hoàn hàng chậm. Cái này xíu nữa tới phần chi tiết em sẽ đi sâu xem đang nằm ở những bưu cục nào để các anh chị xử lý dứt điểm.',
    '',
    'Trọng tâm tuần W40 của mình là: Kéo GTC tiệm cận 60%, giữ tỷ lệ rớt KTC dưới 1.8% và giải tỏa các bưu cục đang bị nghẽn.',
    '',
    'Dạ, bây giờ em xin phép bấm chuyển qua Tab 2 để mình coi kỹ hơn về sản lượng từng tỉnh với từng anh chị AM nha.\"'
]
for line in sec1:
    p = cell0.add_paragraph()
    p.text = line

# TABLE 1: MỤC II - GIỌNG ĐIỆU NÓI TỰ NHIÊN (BÁM SÁT TAB 2 - 3 CHARTS)
cell1 = doc.tables[1].rows[0].cells[0]
for p in cell1.paragraphs[1:]:
    p._p.getparent().remove(p._p)

sec2 = [
    '📍 1. SỐ LIỆU NHANH 5 TỈNH THÀNH (W39 vs W38):',
    '• Khánh Hòa (92.7k đơn, -1,0%) | Lâm Đồng (88.3k đơn, -7,8%) | Bình Thuận (80.8k đơn, -5,5%) | Đắk Nông (33.9k đơn, -2,8%) | Ninh Thuận (33.2k đơn, -2,0%).',
    '• Toàn vùng: Full 328.925 đơn (-4,3%) | TikTok Shop 72.781 đơn (+5,9%, tỷ trọng 22,1%).',
    '',
    '🎙️ LỜI THOẠI THUYẾT TRÌNH TỰ NHIÊN (KHI BẬT TAB 2 SẢN LƯỢNG — 3 BIỂU ĐỒ):',
    '\"Dạ qua tới Tab Sản Lượng, trên màn hình mọi người thấy có 3 cái biểu đồ:',
    '',
    'Đầu tiên nhìn vô biểu đồ 5 tỉnh ở trên, tuần này hàng truyền thống thì tỉnh nào cũng giảm nhẹ, nhưng TikTok Shop lại tăng trưởng ở 4 trên 5 tỉnh, kéo tải rất tốt cho Bình Thuận (tăng 14%), Ninh Thuận (tăng 13%) với Đắk Nông (tăng hơn 8%).',
    '',
    'Nhìn xuống biểu đồ chi tiết từng AM bên dưới, em muốn highlight 2 anh chị làm rất xuất sắc tuần này:',
    '',
    'Đầu tiên là chị Thư ở Khánh Hòa: Tuần này cả vùng mình 18 AM ai cũng giảm hoặc đi ngang, duy nhất chỉ có chị Thư là tăng trưởng dương được hơn 2.200 đơn Full, kéo sản lượng lên gần 35 ngàn đơn. Nhờ vậy chị Thư chính thức vượt qua anh Trường với anh Nhựt để leo lên Top 2 sản lượng của vùng, và giữ cho Khánh Hòa đứng vững vị trí số 1 của tỉnh.',
    '',
    'Người thứ hai là anh Long Bình Thuận: Anh Long thì tuần nào cũng là đầu tàu gánh tải lớn nhất vùng mình rồi, hơn 42 ngàn đơn, một mình anh gánh gần 13% số của cả vùng. Đặc biệt tuần này anh Long là AM đầu tiên của Nam Trung Bộ vượt qua mốc 10 ngàn đơn TikTok Shop trong một tuần, tăng thêm gần 1.400 đơn sàn.',
    '',
    'Tuy nhiên, nhìn sang phía các AM bị hụt sản lượng, có 2 điểm nóng em xin phép lưu ý với các anh chị:',
    '',
    'Chỗ thứ nhất là anh Long Cam Ranh: Tuần này đơn TikTok Shop của anh Long bị rớt hơn 40%, mất gần 1.200 đơn sàn so với tuần trước, từ gần 3.000 đơn rớt xuống còn 1.700 đơn. Trong khi cả vùng mình đơn TikTok đang tăng mà riêng Cam Ranh lại rớt sâu như vậy, thì chỗ này anh Long phải kiểm tra lại liền xem nguồn đơn của các shop lớn khu vực mình đang bị vướng cái gì nha.',
    '',
    'Chỗ thứ hai là anh Trường Lâm Đồng: Tuần này anh Trường giảm hơn 2.100 đơn Full, kéo số của Lâm Đồng giảm sâu nhất vùng. Nhìn qua các bảng khác thì thấy cụm của anh Trường đang bị nghẽn ở bưu cục Lâm Viên 2, GTC rớt xuống dưới 20% và đang dính hơn 700 đơn tồn. Khi giao hàng chậm trễ thì khách gửi người ta sẽ giảm đơn liền, nên anh Trường phải ưu tiên dồn người dọn sạch cái bưu cục này trong mấy ngày đầu tuần giúp em.',
    '',
    'Ngoài ra, chỗ anh Linh với anh Duân ở Đắk Nông: Hai anh lưu ý là tỷ trọng đơn TikTok ở khu mình rất cao, chiếm tới ba mươi mấy phần trăm sản lượng. Địa bàn đồi núi xa xôi, nếu bưu tá mà không đi giao sớm từ đầu giờ sáng thì tỷ lệ giao thành công chắc chắn sẽ bị rớt.',
    '',
    'Dạ tóm lại ở phần sản lượng, tuần tới em nhờ anh Long Cam Ranh rà soát lại nguồn đơn TTS, anh Trường dọn sạch hàng tồn Lâm Viên, còn các anh chị khác tiếp tục ưu tiên lấy và đẩy nhanh đơn TikTok Shop trong ngày.',
    '',
    'Em xin phép chuyển qua Tab tiếp theo là phần Giao thành công (GTC) ạ.\"'
]
for line in sec2:
    p = cell1.add_paragraph()
    p.text = line

doc.save(src)
for c in ['KICH_BAN_THUYET_TRINH_W39_INSIGHT_CHUYEN_SAU.docx', 'KICH_BAN_THUYET_TRINH_W39_NAM_TRUNG_BO.docx']:
    shutil.copyfile(src, c)

print('Updated docx with natural conversational spoken tone successfully!')
