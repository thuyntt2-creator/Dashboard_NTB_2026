import docx, sys, shutil
sys.stdout.reconfigure(encoding='utf-8')

src = 'KICH_BAN_THUYET_TRINH_MOI_NHAT.docx'
doc = docx.Document(src)

# TABLE 5: MỤC VI - CHẤT LƯỢNG ĐÚNG HẸN %ODR W39 CHUẨN XÁC 100%
cell5 = doc.tables[5].rows[0].cells[0]
for p in cell5.paragraphs[1:]:
    p._p.getparent().remove(p._p)

cell5.paragraphs[0].text = "🗣️ CHẤT LƯỢNG ĐÚNG HẸN %ODR THEO TỈNH VÀ ĐỘ PHÂN HÓA 18 AM (TARGET SLA ≥ 92.0%) W39 vs W38:"

sec6 = [
    '📍 1. BẢNG CHỈ SỐ %ODR 5 TỈNH THÀNH (W39 vs W38):',
    '• Top 1 - Ninh Thuận: Full W39 đạt 96,43% (-0,11%p) | TTS W39 đạt 96,42% ➔ Giữ vững ngôi vị quán quân toàn vùng, vượt xa chuẩn SLA ≥92%!',
    '• Top 2 - Bình Thuận: Full W39 đạt 96,27% (+0,14%p) | TTS W39 đạt 96,30% ➔ Ổn định vững chắc Top 2, chuẩn xanh toàn diện.',
    '• Top 3 - Khánh Hòa: Full W39 đạt 91,76% (+0,89%p) | TTS W39 đạt 92,20% ➔ Cải thiện rất tốt, phân khúc TTS chính thức vượt chuẩn 92%.',
    '• Top 4 - Đắk Nông: Full W39 đạt 88,53% (-1,42%p) | TTS W39 đạt 89,10% ➔ Rơi xuống dưới 90%, chưa đạt cam kết.',
    '• Top 5 - Lâm Đồng: Full W39 đạt 84,69% (-1,95%p) | TTS W39 đạt 85,20% ➔ Báo động đỏ: Thấp nhất toàn vùng, giảm sâu gần 2.0%p.',
    '➔ TOÀN VÙNG W39: %ODR Full hàng đạt 90,79% (-0,40%p WoW) | TikTok Shop đạt 91,72% (+0,23%p WoW) ➔ Tiệm cận sát nút vạch đích cam kết SLA 92.0%.',
    '',
    '🎙️ LỜI THOẠI THUYẾT TRÌNH %ODR (KHI BẬT TAB 6: GIAO ĐÚNG HẸN):',
    '\"Dạ tiếp theo em xin phép chuyển qua Tab 6 là chỉ số Giao đúng hẹn %ODR (chuẩn SLA của công ty yêu cầu phải đạt từ 92% trở lên):',
    '',
    'Nhìn vào tỷ lệ toàn vùng tuần này, mình đạt 90.8% ở hàng Full và 91.7% ở TikTok Shop. Như vậy là cả 2 phân khúc đều đang bám rất sát mốc chuẩn 92% của công ty, riêng TikTok Shop chỉ còn cách vạch đích chưa đầy 0.3%p.',
    '',
    'Đầu tiên, nhìn vào bảng 5 tỉnh:',
    '• Tuyên dương 2 tỉnh duyên hải là Ninh Thuận (96.4%) và Bình Thuận (96.3%): Cả 2 tỉnh tiếp tục bảo vệ vững chắc chuẩn SLA xanh, giao phát rất đúng cam kết với khách hàng.',
    '• Khánh Hòa tuần này có cải thiện thêm gần 1%p, đưa tỷ lệ giao đúng hẹn lên 91.8%, riêng TikTok Shop của Khánh Hòa đã vượt qua mốc 92%.',
    '• Tuy nhiên, báo động đỏ lại rơi vào 2 tỉnh miền núi là Đắk Nông (88.5%) và Lâm Đồng (84.7%): Cả 2 tỉnh này đều bị sụt giảm từ 1.5% đến gần 2% so với tuần trước, đặc biệt Lâm Đồng đang cách chuẩn SLA của công ty tới hơn 7%p.',
    '',
    'Bóc tách chi tiết theo 18 AM bên dưới:',
    '',
    'Nhóm AM giữ chuẩn SLA xuất sắc trên 95%:',
    '• Dẫn đầu toàn mạng tiếp tục là anh Nguyễn Ngọc Khánh ở Khánh Hòa (đạt 97.3% Full và 97.8% TTS).',
    '• Chị Cao Thị Thanh Thủy đạt 97.4%, anh Nguyễn Duy Long đạt 96.6% Full và 97.4% TTS, anh Nguyễn Hoàng Phi đạt 95.4%, và anh Nguyễn Đỗ Minh Nghĩa đạt gần 94%.',
    '• Điểm sáng tiến bộ nhất tuần này là anh Phan Đình Duy ở Lâm Đồng: Tuần này anh Duy có bước bứt phá rất tốt, kéo ODR tăng tới 4.1%p (từ 87.7% lên 91.8%), TTS của anh Duy đạt hơn 93%.',
    '',
    'Ngược lại, em xin phép điểm danh các điểm nóng rớt hẹn giao:',
    '• Chỗ anh Lê Văn Trường ở Lâm Đồng: ODR TikTok Shop của anh Trường tuần này bị tụt sâu từ 82.4% xuống chỉ còn 76.8% (rớt mất 5.7%p). Bưu cục giao trễ hẹn nhiều ngày đã ảnh hưởng nghiêm trọng đến điểm vận hành của các shop.',
    '• Chỗ anh Nguyễn Thanh Long ở Cam Ranh: ODR TikTok Shop cũng bị rớt từ 82.6% xuống còn 77.6% (giảm gần 5%p), tỷ lệ đơn trễ hẹn tăng vọt.',
    '• Và tại Đắk Nông, anh Trương Quang Linh (ODR Full chỉ đạt 73.3%, giảm 6.5%p) và anh Lê Minh Lợi (ODR TTS rớt xuống 41.5%) là 2 mắt xích rớt SLA nặng nhất vùng.',
    '',
    '🎯 Về nhiệm vụ tác chiến cho chỉ số ODR tuần W40:',
    '• Em đề nghị anh Trường, anh Long Cam Ranh, anh Linh và anh Lợi: Kiểm soát chặt chẽ các đơn hàng cận giờ SLA (đặc biệt là đơn hàng sàn TikTok Shop), ưu tiên bưu tá phát dứt điểm trong ngày, tuyệt đối không để đơn bị trôi date giao hẹn sang ngày thứ 2, thứ 3.',
    '• Quyết tâm toàn vùng tuần W40 đưa %ODR của cả Full hàng và TikTok Shop vượt mốc 92.0% SLA cam kết.\"'
]

for line in sec6:
    p = cell5.add_paragraph()
    p.text = line

doc.save(src)
for c in ['KICH_BAN_THUYET_TRINH_W39_INSIGHT_CHUYEN_SAU.docx', 'KICH_BAN_THUYET_TRINH_W39_NAM_TRUNG_BO.docx']:
    shutil.copyfile(src, c)

print('Updated Table 5 (ODR) with exact W39 data successfully!')
