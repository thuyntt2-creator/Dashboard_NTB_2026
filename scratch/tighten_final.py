# -*- coding: utf-8 -*-

with open('scratch/report_1809_strict.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's see where we can trim 350 chars cleanly:
replacements = [
    ("• Sản lượng: 79,707 đơn (+2.4% | +1,831 đơn)", "• Sản lượng: 79,707 đơn (+2.4% | +1,831)"),
    ("• %GTC tổng: 58.0% (+1.8%) | %GTC TTS: 56.4% (+1.9%) | Ca 1: 71.92% (+0.92%)", "• %GTC tổng: 58.0% (+1.8%) | %GTC TTS: 56.4% (+1.9%) | Ca 1: 71.9% (+0.9%)"),
    ("• %FD: 9.1% (▲ 2.27%) | %ODR TTS: 93.1% (+1.5%) | %OPR: 85.47% (+8.36%)", "• %FD: 9.1% (▲ 2.27%) | %ODR: 93.1% (+1.5%) | %OPR: 85.5% (+8.4%)"),
    ("• BC bất ổn: 12/85 BC (14.1%) - Nhóm 1: 11 BC | Nhóm 2: 01 BC", "• BC bất ổn: 12/85 BC (14.1%) - N1: 11 BC | N2: 01 BC"),
    ("1. Nhân sự & Kỷ luật (AM & HRBP): Chấm dứt duyệt nghỉ phép tùy tiện (tối đa 1 ngày, cấm 2 người nghỉ cùng lúc); kiểm kê cắt sạch ID đã nghỉ; dứt điểm thủ tục BHXH/giấy tờ; bổ sung 2 thực tập sinh tuyển dụng cho Lâm Đồng & Khánh Hòa", "1. Nhân sự (AM & HRBP): Cấm duyệt nghỉ phép tùy tiện (tối đa 1 ngày, cấm 2 người nghỉ cùng lúc); kiểm kê cắt sạch ID đã nghỉ; dứt điểm thủ tục BHXH; bổ sung 2 TTS tuyển dụng kéo data Lâm Đồng & Khánh Hòa"),
    ("2. Vận hành & Xả tồn (AM & Kho): Đẩy tiến độ gán trước 10h; dọn sạch kho tồn lớn (Tây Nha Trang, Đức Trọng 1, Di Linh) trước mùa mưa bão; đơn >5 ngày tích mất đền bù dứt điểm; chuẩn hóa năng lực 12-13 AM mới và áp dụng Senior AM từ 01/10", "2. Vận hành (AM & Kho): Đẩy tiến độ gán trước 10h; dọn sạch kho tồn lớn (Tây Nha Trang, Đức Trọng 1, Di Linh) trước mùa mưa; đơn >5 ngày tích mất đền bù; chuẩn hóa đào tạo AM và áp dụng Senior AM từ 01/10"),
    ("• NN: Hụt 50% NV, gán chậm do phụ chở hàng to về kho, đọng 401 đơn, FD vọt 49.0%", "• NN: Hụt 50% NV, gán chậm do phụ chở hàng to về kho, đọng 401 đơn, hoàn FD 49.0%"),
    ("• GP: Phỏng vấn 2 ứng viên Đắk Ru, dọn nốt đơn >120h, đơn >5 ngày tích mất đền bù", "• GP: Phỏng vấn 2 ứng viên Đắk Ru, dọn nốt đơn >120h, đơn >5 ngày tích mất đền bù"),
    ("• GP: Đổi AM mới kiểm kê cắt ID, siết duyệt nghỉ tối đa 1 ngày, phỏng vấn xử lý mới", "• GP: Đổi AM mới kiểm kê cắt ID, siết duyệt nghỉ tối đa 1 ngày, tuyển xử lý mới"),
    ("• GP: Tái cấu trúc tuyến theo cụm gỡ Ontime, siết duyệt nghỉ, HRBP dồn lực tuyển 5 NV", "• GP: Tái cấu trúc tuyến gỡ Ontime, siết duyệt nghỉ, HRBP dồn lực tuyển bù 5 NV"),
    ("• GP: Kiểm kê cắt sạch ID đã nghỉ, bổ sung 1 NV mới gán 60 đơn, dứt điểm hồ sơ BHXH", "• GP: Kiểm kê cắt sạch ID đã nghỉ, bổ sung 1 NV mới gán 60 đơn, xử lý hồ sơ BHXH"),
    ("• GP: Thêm 1 NV mới & 1 chi viện Diên An lên 9 người, gán >1,200 đơn, dọn sạch tồn", "• GP: Thêm 1 NV mới & 1 chi viện nâng lên 9 NV, gán >1,200 đơn, dọn sạch tồn"),
    ("• GP: Dùng 2 NV chi viện dọn sạch tồn cũ, sáng chạy hàng to trưa đẩy hàng nhỏ", "• GP: Dùng 2 NV chi viện xả tồn cũ, sáng chạy hàng to trưa đẩy hàng nhỏ"),
    ("• GP: Chấn chỉnh kỷ luật dẹp lơ là lướt app, phối hợp cụm san sẻ tuyến, tuyển bù 2 NV", "• GP: Dẹp lơ là lướt app tại kho, phối hợp cụm san sẻ tuyến, tuyển bù 2 NV"),
    ("• GP: Kích hoạt 2 kho vệ tinh D'Ran & Thạnh Mỹ từ Thứ 2, AM thúc gán xong trước 12h", "• GP: Kích hoạt 2 kho D'Ran & Thạnh Mỹ từ Thứ 2, AM thúc gán xong trước 12h"),
    ("• GP: Thuê xe ngoài giảm tải chặn trần 110 đơn/NV, tập trung xả 439 đơn tồn cũ", "• GP: Thuê xe ngoài giảm tải trần 110 đơn/NV, tập trung xả 439 đơn tồn cũ"),
    ("• GP: Cắt trách nhiệm AM cũ giao AM mới tiếp quản, kiểm kê cắt ID, chấn chỉnh luồng hàng", "• GP: Cắt quyền AM cũ giao AM mới tiếp quản, kiểm kê cắt ID, chấn chỉnh luồng hàng"),
    ("• GP: Bố trí bưu tá cứng kèm cặp hỗ trợ, AM gọi phúc tra đơn hoàn FD, siết kỷ luật giao", "• GP: Bố trí bưu tá cứng kèm cặp, AM gọi phúc tra đơn hoàn FD, siết kỷ luật giao"),
    ("• GP: Xuất toàn bộ 138 đơn tồn đi giao ngay Ca 1, AM giám sát chặt hành trình giao hàng", "• GP: Xuất toàn bộ 138 đơn tồn đi giao Ca 1, AM giám sát hành trình giao hàng"),
]

for old, new in replacements:
    text = text.replace(old, new)

# Also let's tighten NN lines
text = text.replace('• NN: Duyệt nghỉ tùy tiện (>20 ngày), tối qua treo chuyến, xử lý kém làm đọng 209 đơn', '• NN: Duyệt nghỉ tùy tiện (>20 ngày), tối qua treo chuyến, xử lý kém, đọng 209 đơn')
text = text.replace('• NN: Thiếu 5 NV vỡ lộ trình làm Ontime tụt 28.0%, kho quanh kẹt tải đọng 263 đơn', '• NN: Thiếu 5 NV vỡ lộ trình làm Ontime rơi 28.0%, kho quanh kẹt tải đọng 263 đơn')
text = text.replace('• NN: 3 NV nghỉ ngang do chậm thủ tục BHXH/giấy tờ, chuyển đơn sang Quảng Tín hỗ trợ', '• NN: 3 NV nghỉ ngang do chậm thủ tục BHXH/giấy tờ, chuyển đơn sang Quảng Tín gánh phụ')
text = text.replace('• NN: Đọng 1,776 đơn (68% tải), shipper mới chưa dám ép tải làm Ontime rớt 24.6%', '• NN: Đọng 1,776 đơn (68% tải), shipper mới chưa dám ép tải kéo Ontime rớt 24.6%')
text = text.replace('• NN: Tuyến đồi dốc kèm hàng to làm chậm giao, thiếu 2 NV khiến 218 đơn cũ chưa xả hết', '• NN: Tuyến dốc kèm hàng to làm chậm giao, thiếu 2 NV làm 218 đơn cũ chưa xả hết')
text = text.replace('• NN: Hụt 4 NV gãy tuyến trọng điểm, bưu tá nản chí giảm năng suất làm GTC N-1 về 29.4%', '• NN: Hụt 4 NV gãy tuyến trọng điểm, bưu tá nản chí giảm năng suất, GTC N-1 về 29.4%')
text = text.replace('• NN: Kho chính quá tải chia chọn đầu ngày làm bưu tá trễ xuất tuyến, đọng 204 đơn cũ', '• NN: Kho chính quá tải chia chọn đầu ngày làm trễ xuất tuyến, đọng 204 đơn cũ')
text = text.replace('• NN: Thiếu 4 NV khiến bưu tá quá tải cực hạn (172 đơn/NV), dồn ứ 439 đơn tồn lớn', '• NN: Thiếu 4 NV khiến bưu tá quá tải (172 đơn/NV), dồn ứ 439 đơn tồn lớn (59% tải)')
text = text.replace('• NN: 3/4 shipper mới, xe tải đến trễ (09:30) phụ dỡ hàng tới 11:30 mới đi giao, chiều mưa', '• NN: 3/4 shipper mới, xe tải đến trễ (09:30) phụ dỡ hàng tới 11:30 mới giao, chiều mưa')
text = text.replace('• NN: NV mới chưa quen đường & hỏng xe làm Ontime tụt về 54.7%, hoàn FD tăng 12.9%', '• NN: NV mới chưa quen đường & hỏng xe làm Ontime rớt 54.7%, hoàn FD tăng 12.9%')
text = text.replace('• NN: Tồn kho còn 138 đơn sau mưa bão chưa được ưu tiên xử lý dứt điểm trước khi nhận đơn mới', '• NN: Tồn 138 đơn sau mưa bão chưa ưu tiên xử lý dứt điểm trước khi nhận đơn mới')

print("FINAL TIGHTENED LENGTH:", len(text))
with open('scratch/report_1809_safe_final.txt', 'w', encoding='utf-8') as f:
    f.write(text)
