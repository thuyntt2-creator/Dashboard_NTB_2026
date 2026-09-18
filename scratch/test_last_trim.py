# -*- coding: utf-8 -*-

with open('scratch/sub_4k_confirmed.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Shave 135 chars:
text = text.replace('• Nguyên nhân: Hụt 50% NV, gán chậm do phụ chở hàng to, đọng 401 đơn', '• Nguyên nhân: Hụt 50% NV, gán chậm do chở hàng to, đọng 401 đơn')
text = text.replace('• Giải pháp: Phỏng vấn 2 ứng viên Đắk Ru, xả nốt tồn, đơn >5 ngày tích mất', '• Giải pháp: Phỏng vấn 2 ứng viên Đắk Ru, xả nốt tồn, đơn >5 ngày tích mất')
text = text.replace('• Nguyên nhân: Duyệt nghỉ tùy tiện (>20 ngày), tối treo chuyến, đọng 209 đơn', '• Nguyên nhân: Duyệt nghỉ tùy tiện (>20 ngày), treo chuyến, đọng 209 đơn')
text = text.replace('• Giải pháp: Đổi AM mới cắm kho cắt ID, siết duyệt nghỉ 1 ngày, tuyển xử lý mới', '• Giải pháp: Đổi AM mới kiểm kê cắt ID, siết duyệt nghỉ, tuyển xử lý mới')
text = text.replace('• Nguyên nhân: Thiếu 5 NV vỡ lộ trình làm Ontime tụt 28%, kho quanh kẹt tải', '• Nguyên nhân: Thiếu 5 NV vỡ lộ trình làm Ontime tụt 28%, kho quanh kẹt tải')
text = text.replace('• Giải pháp: Tái cấu trúc tuyến theo cụm gỡ Ontime, siết nghỉ phép, tuyển 5 NV', '• Giải pháp: Tái cấu trúc tuyến gỡ Ontime, siết nghỉ phép, tuyển bù 5 NV')
text = text.replace('• Nguyên nhân: 3 NV nghỉ ngang do chậm hồ sơ BHXH, chuyển đơn sang Quảng Tín phụ', '• Nguyên nhân: 3 NV nghỉ ngang do chậm BHXH, chuyển đơn sang Quảng Tín phụ')
text = text.replace('• Giải pháp: Kiểm kê cắt sạch ID đã nghỉ, thêm 1 NV gán 60 đơn, dứt điểm BHXH', '• Giải pháp: Kiểm kê cắt sạch ID đã nghỉ, thêm 1 NV gán 60 đơn, dứt điểm BHXH')
text = text.replace('• Nguyên nhân: Đọng 1,776 đơn (68% tải), bưu tá mới chưa dám ép tải kéo Ontime rớt', '• Nguyên nhân: Đọng 1,776 đơn (68% tải), bưu tá mới chưa dám ép tải làm rớt Ontime')
text = text.replace('• Giải pháp: Thêm 1 NV mới & 1 chi viện lên 9 người, gán >1,200 đơn, dọn sạch tồn', '• Giải pháp: Thêm 1 NV mới & 1 chi viện lên 9 người, gán >1,200 đơn, xả sạch tồn')
text = text.replace('• Nguyên nhân: Tuyến dốc kèm hàng to làm chậm giao, thiếu 2 NV làm đọng 218 đơn cũ', '• Nguyên nhân: Tuyến dốc kèm hàng to làm chậm giao, thiếu 2 NV đọng 218 đơn cũ')
text = text.replace('• Giải pháp: Duy trì 2 NV chi viện dọn tồn cũ, sáng chạy hàng to trưa đẩy hàng nhỏ', '• Giải pháp: Duy trì 2 NV chi viện dọn tồn, sáng chạy hàng to trưa đẩy hàng nhỏ')
text = text.replace('• Nguyên nhân: Hụt 4 NV gãy tuyến trọng điểm, bưu tá nản giảm năng suất, GTC rớt', '• Nguyên nhân: Hụt 4 NV gãy tuyến trọng điểm, bưu tá nản giảm năng suất, GTC rớt')
text = text.replace('• Giải pháp: Dẹp lơ là lướt app tại kho, phối hợp cụm san sẻ tuyến, tuyển bù 2 NV', '• Giải pháp: Dẹp lơ là lướt app tại kho, phối hợp cụm san sẻ tuyến, tuyển bù 2 NV')
text = text.replace('• Nguyên nhân: Kho chính quá tải chia chọn đầu ngày làm trễ xuất tuyến, đọng 204 đơn', '• Nguyên nhân: Kho chính quá tải chia chọn làm trễ xuất tuyến, đọng 204 đơn')
text = text.replace('• Giải pháp: Kích hoạt 2 kho vệ tinh D\'Ran & Thạnh Mỹ từ Thứ 2, thúc gán xong sớm', '• Giải pháp: Kích hoạt 2 kho D\'Ran & Thạnh Mỹ từ Thứ 2, thúc gán xong sớm')
text = text.replace('• Nguyên nhân: Thiếu 4 NV khiến bưu tá quá tải (172 đơn/NV), dồn ứ 439 đơn tồn lớn', '• Nguyên nhân: Thiếu 4 NV bưu tá quá tải (172 đơn/NV), dồn ứ 439 đơn tồn lớn')
text = text.replace('• Giải pháp: Thuê xe ngoài giảm tải trần 110 đơn/NV, tập trung xả sạch 439 đơn tồn', '• Giải pháp: Thuê xe ngoài giảm tải trần 110 đơn/NV, xả sạch 439 đơn tồn')
text = text.replace('• Nguyên nhân: 3/4 shipper mới, xe tải đến trễ phụ dỡ hàng tới 11:30 mới đi giao, chiều mưa', '• Nguyên nhân: 3/4 shipper mới, xe tải trễ dỡ hàng tới 11:30 mới đi giao, chiều mưa')
text = text.replace('• Giải pháp: Cắt quyền AM cũ giao AM mới tiếp quản, kiểm kê cắt ID, chấn chỉnh luồng hàng', '• Giải pháp: Cắt quyền AM cũ giao AM mới tiếp quản, kiểm kê cắt ID, chấn chỉnh luồng hàng')
text = text.replace('• Nguyên nhân: NV mới chưa quen đường & hỏng xe làm Ontime tụt 54.7%, hoàn FD tăng', '• Nguyên nhân: NV mới chưa thạo đường & hỏng xe làm Ontime tụt 54.7%, hoàn FD tăng')
text = text.replace('• Giải pháp: Bố trí bưu tá cứng kèm cặp hỗ trợ, AM gọi phúc tra đơn hoàn FD, siết kỷ luật', '• Giải pháp: Bố trí bưu tá cứng kèm cặp, AM gọi phúc tra đơn hoàn FD, siết kỷ luật')

# Section 3
text = text.replace('1. Nhân sự (AM & HRBP): Cấm duyệt nghỉ tùy tiện (tối đa 1 ngày, cấm 2 người nghỉ cùng lúc); cắt sạch ID đã nghỉ; dứt điểm BHXH; thêm 2 TTS tuyển dụng kéo data Lâm Đồng & Khánh Hòa', '1. Nhân sự (AM & HRBP): Cấm duyệt nghỉ tùy tiện (tối đa 1 ngày, cấm 2 người nghỉ cùng lúc); cắt sạch ID đã nghỉ; dứt điểm BHXH; thêm 2 TTS tuyển kéo data Lâm Đồng & Khánh Hòa')
text = text.replace('2. Vận hành (AM & Kho): Đẩy gán trước 10h; dọn sạch kho tồn lớn (Tây Nha Trang, Đức Trọng 1, Di Linh) trước mùa mưa; đơn >5 ngày tích mất đền bù; chuẩn hóa đào tạo AM & áp dụng Senior AM từ 01/10', '2. Vận hành (AM & Kho): Đẩy gán trước 10h; dọn sạch tồn lớn (Tây Nha Trang, Đức Trọng 1, Di Linh) trước mùa mưa; đơn >5 ngày tích mất; chuẩn hóa đào tạo AM & áp dụng Senior AM từ 01/10')

print("FINAL CHECK EXACT LEN:", len(text))
with open('scratch/report_1809_under_4000_perfect.txt', 'w', encoding='utf-8') as f:
    f.write(text)
