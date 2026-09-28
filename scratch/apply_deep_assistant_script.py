import docx, sys, shutil
sys.stdout.reconfigure(encoding='utf-8')

src = 'KICH_BAN_THUYET_TRINH_MOI_NHAT.docx'
doc = docx.Document(src)

# TABLE 0: MỤC I - TỔNG QUAN ĐIỀU HÀNH VÙNG (GÓC NHÌN TRỢ LÝ GIÁM ĐỐC VÙNG)
cell0 = doc.tables[0].rows[0].cells[0]
for p in cell0.paragraphs[1:]:
    p._p.getparent().remove(p._p)

sec1 = [
    '📍 1. BẢNG CHỈ SỐ TOÀN VÙNG & 5 TỈNH THÀNH (W39 vs W38):',
    '• Khánh Hòa: 92.696 đơn (-1,0% WoW) | %GTC 58,6% (+3,6%p) | %ODR 91,8% | TTS: 18.043 đơn (+449 đơn WoW) ➔ Giữ vững ngôi vị số 1 toàn vùng!',
    '• Lâm Đồng: 88.287 đơn (-7,8% WoW, -7.440 đơn) | Đầu tàu TTS vùng (19.283 đơn, 26,5%) | %GTC 47,4% | %ODR 84,7% | Báo động tồn đọng.',
    '• Bình Thuận: 80.817 đơn (-5,5% WoW) | %GTC 67,5% | %ODR 96,3% (Top 2 vùng) | TTS bùng nổ: 18.146 đơn (+2.273 đơn WoW, +14,3%!).',
    '• Đắk Nông: 33.883 đơn (-2,8% WoW) | %GTC 48,8% (+2,0%p) | %ODR 88,5% | TTS: 9.016 đơn (+702 đơn WoW, +8,4%).',
    '• Ninh Thuận: 33.242 đơn (-2,0% WoW) | Quán quân %GTC toàn vùng (68,0%) | Quán quân %ODR toàn vùng (96,4%) | TTS: 8.293 đơn (+935 đơn WoW, +12,7%).',
    '➔ TOÀN VÙNG: 328.925 đơn Full (-4,3% WoW, -14.672 đơn) | TikTok Shop lập đỉnh 72.781 đơn (+5,9% WoW, chiếm 22,1% tỷ trọng) | %GTC Full 56,60% (+0,92%p) | %GTC TTS 57,45% (+3,55%p) | %ODR 90,79% | Rớt luân chuyển KTC giảm sâu về 1,52% (-1,81%p WoW) | Phạt truy thu phát sinh 306,9 Tr ₫ trên 4.013 đơn.',
    '',
    '🎙️ LỜI THOẠI THUYẾT TRÌNH TỔNG QUAN (VAI TRÒ TRỢ LÝ GIÁM ĐỐC VÙNG ĐÁNH GIÁ ĐIỀU HÀNH):',
    '\"Kính thưa Ban Giám Đốc cùng toàn thể các anh chị Quản lý Vận hành (AM), Trưởng bưu cục và các khối phòng ban Vùng Nam Trung Bộ.',
    '',
    'Bước vào tuần vận hành W39 (từ 21/09 đến 27/09/2026), thay mặt bộ phận điều hành vùng, em xin phép báo cáo tổng quan bức tranh tuần qua với những đánh giá cụ thể về CÁI LÀM ĐƯỢC và CÁI CHƯA LÀM ĐƯỢC của toàn mạng lưới:',
    '',
    'Về mặt số lượng, tổng sản lượng giao toàn vùng đạt 328.925 đơn Full hàng, giảm nhẹ -4,3% WoW (-14.672 đơn). Tuy nhiên, đi sâu vào cấu trúc số liệu, chúng ta nhìn thấy rõ 3 chuyển động then chốt:',
    '',
    '✅ CÁI LÀM ĐƯỢC (ĐIỂM SÁNG ĐIỀU HÀNH CẦN PHÁT HUY):',
    '1. Bứt phá dòng hàng TikTok Shop: Trong bối cảnh hàng truyền thống hạ nhiệt, kênh TikTok Shop tiếp tục tăng trưởng dương +5,9% WoW, đạt kỷ lục 72.781 đơn và nâng tỷ trọng trong cơ cấu toàn mạng lên mức cao nhất lịch sử: 22,1%. Đáng chú ý, tỷ lệ Giao thành công (%GTC) của TikTok Shop có bước nhảy vọt +3,55%p, đạt 57,45% – chính thức vượt qua tỷ lệ GTC của hàng Full (56,60%). Điều này chứng minh các giải pháp ưu tiên xử lý đơn sàn của chúng ta đã đi đúng hướng.',
    '2. Thắng lợi ở khâu vận tải KTC: Tỷ lệ rớt luân chuyển KTC giảm ngoạn mục từ 3,32% xuống còn 1,52% (-1,81%p WoW, giảm hơn 54% lượng đơn rớt luân chuyển). Việc siết chặt kỷ luật bàn giao ca KTC đã giải quyết cơ bản tình trạng đơn bị bỏ sót chuyến xe tải trục.',
    '3. Giữ vững kỷ luật cam kết SLA tại các tỉnh duyên hải: Ninh Thuận tiếp tục là ngọn cờ đầu toàn mạng với %GTC đạt 68,0% và %ODR đạt 96,4%; Bình Thuận giữ vững phong độ Top 2 với GTC 67,5% và ODR 96,3%.',
    '',
    '❌ CÁI CHƯA LÀM ĐƯỢC (NÚT THẮT NGUY HIỂM CẦN AM NHÌN RÕ VÀ HÀNH ĐỘNG):',
    '1. Bùng phát áp lực bưu cục cảnh báo: Danh sách bưu cục bất ổn tăng từ 13 lên 15 bưu cục. Trong đó, có 9 bưu cục kẹt dai dẳng cả 2 tuần và 6 bưu cục mới rơi vào diện cảnh báo, tập trung chủ yếu tại Lâm Đồng và Đắk Nông (%GTC dưới 45%). Độ vênh chất lượng giữa vùng đồng bằng (>67%) và miền núi (<48%) đang kéo lùi toàn bộ chỉ số chung của vùng.',
    '2. Báo động đỏ về tài chính truy thu: Số liệu truy thu phát sinh tăng vọt lên 306,9 triệu đồng trên 4.013 đơn. Đáng nói, hơn 162 triệu đồng (chiếm 53%) nằm ở hai lỗi vận hành cốt lõi: Backlog giao hàng (109,2 Tr ₫) và Backlog luân chuyển trả (53,6 Tr ₫), tập trung nặng nhất ở các cụm bưu cục do AM Kim Chi, AM Bích Nga, AM Văn Trường và AM Văn Phước phụ trách.',
    '',
    '🔍 INSIGHT BẢN CHẤT ĐIỀU HÀNH:',
    'Sản lượng giảm 4,3% là khoảng thời gian quý giá để toàn mạng lưới dọn dẹp hàng tồn và nâng chuẩn dịch vụ, điều này đã giúp GTC tăng nhẹ (+0,92%p Full, +3,55%p TTS). Tuy nhiên, nếu các AM không giải quyết dứt điểm các bưu cục nghẽn tải cục bộ thì nguy cơ vỡ trận trong các đợt kích cầu đầu tháng 10 là hiện hữu.',
    '',
    '🎯 MỆNH LỆNH TÁC CHIẾN TUẦN W40:',
    '1. Điều tiết ngay hạn mức tiếp nhận tải (Cap Volume) tại 15 bưu cục cảnh báo để thông luồng hàng tồn.',
    '2. 18 AM trực tiếp rà soát và đóng dứt điểm các biên bản truy thu do tồn đọng giao hàng và hoàn hàng, không để kéo dài sang tháng mới.',
    '3. Duy trì tỷ lệ rớt luân chuyển KTC dưới 2,0% và đẩy mạnh tỷ lệ thanh toán COD số qua VietQR.\"'
]
for line in sec1:
    p = cell0.add_paragraph()
    p.text = line

# TABLE 1: MỤC II - SẢN LƯỢNG GIAO (BÓC TÁCH CHI TIẾT 18 AM & ĐÁNH GIÁ SÂU)
cell1 = doc.tables[1].rows[0].cells[0]
for p in cell1.paragraphs[1:]:
    p._p.getparent().remove(p._p)

sec2 = [
    '📍 1. BẢNG PHÂN BỔ SẢN LƯỢNG 5 TỈNH THÀNH (W39 vs W38):',
    '• Khánh Hòa: 92.696 đơn (giảm -919 đơn, -1,0% WoW) | TTS: 18.043 đơn (+449 đơn WoW) ➔ Giữ vững ngôi vị quán quân sản lượng toàn vùng.',
    '• Lâm Đồng: 88.287 đơn (giảm sâu -7.440 đơn, -7,8% WoW) | TTS: 19.283 đơn (-304 đơn WoW, đầu tàu TTS vùng).',
    '• Bình Thuận: 80.817 đơn (giảm -4.672 đơn, -5,5% WoW) | TTS: 18.146 đơn (+2.273 đơn WoW, +14,3% ➔ Tăng trưởng TTS mạnh nhất vùng).',
    '• Đắk Nông: 33.883 đơn (giảm -965 đơn, -2,8% WoW) | TTS: 9.016 đơn (+702 đơn WoW, +8,4%).',
    '• Ninh Thuận: 33.242 đơn (giảm -676 đơn, -2,0% WoW) | TTS: 8.293 đơn (+935 đơn WoW, +12,7%).',
    '➔ TOÀN VÙNG: 328.925 đơn Full hàng (-4,3% WoW) | TikTok Shop: 72.781 đơn (+5,9% WoW, tỷ trọng 22,1%).',
    '',
    '🎙️ LỜI THOẠI THUYẾT TRÌNH SẢN LƯỢNG (TAB II — 3 CHARTS | ĐÁNH GIÁ SÂU & GIAO VIỆC):',
    '\"Kính thưa Ban Giám Đốc cùng toàn thể các anh chị AM,',
    '',
    'Quan sát 3 biểu đồ sản lượng trên màn hình, tổng đơn toàn vùng tuần W39 đạt 328.925 đơn, giảm 14.672 đơn so với tuần trước. Khi bóc tách chi tiết tương quan giữa 5 tỉnh và 18 AM, chúng ta thấy rõ những điểm làm được rất tốt và những điểm báo động cần chấn chỉnh ngay:',
    '',
    '✅ CÁI LÀM ĐƯỢC — TUYÊN DƯƠNG 2 ĐẦU TÀU BỨT PHÁ:',
    '1. AM Thái Thị Thanh Thư (Khánh Hòa) — Quán quân tăng trưởng toàn mạng (+2.227 đơn Full, +6,8% WoW, đạt 34.765 đơn):',
    '• Đánh giá: Nhìn trên biểu đồ biến động của 18 AM, chị Thư là AM DUY NHẤT trong toàn mạng có sản lượng tăng trưởng dương tuần này (17 AM còn lại đều giảm hoặc đi ngang). Mức tăng ấn tượng này đã đưa AM Thư chính thức vượt qua AM Trường và AM Nhựt để leo lên vị trí Top 2 sản lượng toàn vùng, trực tiếp bảo vệ ngôi vị số 1 của tỉnh Khánh Hòa.',
    '• Bài học vận hành: Địa bàn nội thị có vòng quay đơn nhanh, bưu tá phát 2-3 ca trong ngày, tỷ lệ giao thành công cao đã giúp AM Thư giữ trọn nhịp tăng trưởng ngay trong giai đoạn thị trường điều chỉnh.',
    '',
    '2. AM Nguyễn Duy Long (Bình Thuận) — Cỗ máy gánh tải số 1 & Bứt phá TikTok Shop (+1.379 đơn TTS, +15,0%, đạt 10.584 đơn | Full: 42.506 đơn):',
    '• Đánh giá: AM Long tiếp tục là xương sống gánh vác tới 12,9% sản lượng của toàn mạng lưới. Đáng biểu dương nhất, anh Long là AM đầu tiên của toàn vùng Nam Trung Bộ phá mốc 10.000 đơn TikTok Shop chỉ trong 1 tuần, đóng góp chính vào mức tăng 2.273 đơn TTS của tỉnh Bình Thuận.',
    '• Bài học vận hành: Khâu lấy hàng First-mile được tổ chức rất linh hoạt theo các khung giờ chốt đơn livestream chiều tối, giúp gom trọn sản lượng đưa lên xe KTC trong đêm.',
    '',
    '❌ CÁI CHƯA LÀM ĐƯỢC — BÁO ĐỘNG ĐỎ CẦN AM NHÌN RÕ VẤN ĐỀ:',
    '1. AM Nguyễn Thanh Long (Cam Ranh) — Cú rơi TikTok Shop sâu nhất toàn mạng (-1.186 đơn TTS, -40,5% WoW, rơi từ 2.930 xuống 1.744 đơn):',
    '• Đánh giá: Bốc hơi hơn 40% sản lượng đơn sàn chỉ trong 7 ngày là điểm bất thường lớn nhất trên biểu đồ TTS tuần này, hoàn toàn ngược chiều với xu hướng tăng +5,9% của toàn vùng và đà tăng của các AM còn lại ở Khánh Hòa (+449 đơn).',
    '• Vấn đề cốt lõi: AM Long cần rà soát khẩn cấp nguồn phát sinh đơn của các shop lớn tại địa bàn Cam Ranh, làm rõ nguyên nhân đứt gãy để có giải pháp chặn đứng đà sụt giảm.',
    '',
    '2. AM Lê Văn Trường (Lâm Đồng) — Suy giảm sản lượng Full sâu nhất toàn vùng (-2.132 đơn Full, rơi từ 28.919 về 26.787 đơn):',
    '• Đánh giá: Mức giảm của AM Trường đóng góp lớn nhất vào mức sụt -7.440 đơn của tỉnh Lâm Đồng. Đáng lo ngại hơn, sự sụt giảm sản lượng này đang đi liền với nút thắt nghẽn tải tại bưu cục Lâm Viên 2 (GTC rơi về 19,55%) và khoản phạt truy thu phát sinh 50,6 triệu đồng trên 722 đơn tồn đọng.',
    '• Mối liên hệ nhân quả: Ách tắc Last-mile và giao hàng trễ tiến độ làm giảm uy tín dịch vụ, khiến lượng đơn gửi tại địa phương bị kéo lùi.',
    '',
    '⚠️ ĐIỂM CẦN LƯU Ý VỀ TỶ TRỌNG ĐƠN SÀN TẠI VÙNG NÚI:',
    '• AM Trương Quang Linh (TTS chiếm tới 34,8% tổng đơn) và AM Huỳnh Thúc Duân (chiếm 29,0% tổng đơn) đang có tỷ trọng đơn sàn cao vượt trội. Với đặc thù địa bàn đường đèo dốc Đắk Nông, 2 anh phải siết chặt thời gian xuất tuyến ca sáng trước 08h30 để bảo vệ tỷ lệ giao thành công.',
    '',
    '🎯 QUYẾT SÁCH TÁC CHIẾN TUẦN W40 — GIAO VIỆC ĐÍCH DANH:',
    '1. AM Nguyễn Thanh Long: Trong 48 giờ tới, rà soát toàn bộ danh sách khách hàng gửi đơn TTS tại Cam Ranh, làm việc trực tiếp để phục hồi sản lượng về lại mốc trên 2.500 đơn TTS/tuần.',
    '2. AM Lê Văn Trường: Tập trung dồn nhân lực giải quyết dứt điểm 722 đơn tồn đọng tại cụm Đà Lạt, thông luồng bưu cục Lâm Viên 2 để đưa sản lượng Full tuần W40 quay trở lại mốc 28.000 đơn.',
    '3. Toàn thể 18 AM: Tiếp tục ưu tiên cao nhất cho tiến độ lấy hàng và xử lý luồng đơn TikTok Shop trong ngày, đảm bảo giữ vững đà tăng trưởng trên 22% tỷ trọng toàn mạng.\"'
]
for line in sec2:
    p = cell1.add_paragraph()
    p.text = line

doc.save(src)
for c in ['KICH_BAN_THUYET_TRINH_W39_INSIGHT_CHUYEN_SAU.docx', 'KICH_BAN_THUYET_TRINH_W39_NAM_TRUNG_BO.docx']:
    shutil.copyfile(src, c)

print('Updated docx successfully!')
