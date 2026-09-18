# -*- coding: utf-8 -*-

with open('scratch/report_1809_ready_to_send.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Trim 100 chars
text = text.replace('• NN: Hụt 50% NV, gán chậm do phụ chở hàng to về kho, đọng 401 đơn, hoàn FD 49.0%', '• NN: Hụt 50% NV, gán chậm do phụ chở hàng to về kho, đọng 401 đơn, hoàn FD 49%')
text = text.replace('• GP: Phỏng vấn 2 ứng viên Đắk Ru, dọn nốt đơn >120h, đơn >5 ngày tích mất đền bù', '• GP: Phỏng vấn 2 ứng viên Đắk Ru, dọn nốt đơn >120h, đơn >5 ngày tích mất')
text = text.replace('• GP: Đổi AM mới kiểm kê cắt ID, siết duyệt nghỉ tối đa 1 ngày, tuyển xử lý mới', '• GP: Đổi AM mới kiểm kê cắt ID, siết duyệt nghỉ tối đa 1 ngày, tuyển xử lý mới')
text = text.replace('• NN: Thiếu 5 NV vỡ lộ trình làm Ontime rơi 28.0%, kho quanh kẹt tải đọng 263 đơn', '• NN: Thiếu 5 NV vỡ lộ trình làm Ontime rơi 28%, kho quanh kẹt tải đọng 263 đơn')
text = text.replace('• NN: 3 NV nghỉ ngang do chậm thủ tục BHXH/giấy tờ, chuyển đơn sang Quảng Tín gánh phụ', '• NN: 3 NV nghỉ ngang do chậm thủ tục BHXH/giấy tờ, chuyển đơn sang Quảng Tín phụ')
text = text.replace('• NN: Đọng 1,776 đơn (68% tải), shipper mới chưa dám ép tải kéo Ontime rớt 24.6%', '• NN: Đọng 1,776 đơn (68% tải), shipper mới chưa dám ép tải kéo Ontime rớt 24.6%')
text = text.replace('• GP: Thêm 1 NV mới & 1 chi viện nâng lên 9 NV, gán >1,200 đơn, dọn sạch tồn', '• GP: Thêm 1 NV mới & 1 chi viện nâng lên 9 NV, gán >1,200 đơn, xả sạch tồn')
text = text.replace('• GP: Dùng 2 NV chi viện xả tồn cũ, sáng chạy hàng to trưa đẩy hàng nhỏ', '• GP: Dùng 2 NV chi viện dọn tồn cũ, sáng chạy hàng to trưa đẩy hàng nhỏ')
text = text.replace('• NN: Hụt 4 NV gãy tuyến trọng điểm, bưu tá nản chí giảm năng suất, GTC N-1 về 29.4%', '• NN: Hụt 4 NV gãy tuyến trọng điểm, bưu tá giảm năng suất, GTC N-1 về 29.4%')
text = text.replace('• NN: Kho chính quá tải chia chọn đầu ngày làm trễ xuất tuyến, đọng 204 đơn cũ', '• NN: Kho chính quá tải chia chọn đầu ngày làm trễ xuất tuyến, đọng 204 đơn')
text = text.replace('• NN: Thiếu 4 NV khiến bưu tá quá tải (172 đơn/NV), dồn ứ 439 đơn tồn lớn (59% tải)', '• NN: Thiếu 4 NV bưu tá quá tải (172 đơn/NV), dồn ứ 439 đơn tồn lớn (59% tải)')
text = text.replace('• NN: 3/4 shipper mới, xe tải đến trễ (09:30) phụ dỡ hàng tới 11:30 mới giao, chiều mưa', '• NN: 3/4 shipper mới, xe tải đến trễ phụ dỡ hàng tới 11:30 mới giao, chiều mưa ngưng chạy')
text = text.replace('• GP: Cắt quyền AM cũ giao AM mới tiếp quản, kiểm kê cắt ID, chấn chỉnh luồng hàng', '• GP: Cắt quyền AM cũ giao AM mới tiếp quản, kiểm kê cắt ID, chấn chỉnh luồng hàng')
text = text.replace('• NN: NV mới chưa quen đường & hỏng xe làm Ontime rớt 54.7%, hoàn FD tăng 12.9%', '• NN: NV mới chưa thạo đường & hỏng xe làm Ontime rớt 54.7%, hoàn FD tăng 12.9%')

print("FINAL STRING LEN:", len(text))
with open('scratch/report_1809_ready_to_send.txt', 'w', encoding='utf-8') as f:
    f.write(text)
