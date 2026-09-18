# -*- coding: utf-8 -*-

with open('scratch/report_1809_ready_to_send.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Shave 50 chars
text = text.replace('• %GTC tổng: 58.0% (+1.8%) | %GTC TTS: 56.4% (+1.9%) | Ca 1: 71.9% (+0.9%)', '• %GTC tổng: 58.0% (+1.8%) | %GTC TTS: 56.4% (+1.9%) | Ca 1: 71.9% (+0.92%)')
text = text.replace('• GP: Phỏng vấn 2 ứng viên Đắk Ru, dọn nốt đơn >120h, đơn >5 ngày tích mất', '• GP: Phỏng vấn 2 ứng viên Đắk Ru, dọn nốt đơn >120h, đơn >5 ngày tích mất đền bù')
text = text.replace('2. Vận hành (AM & Kho): Đẩy gán trước 10h; dọn sạch tồn lớn (Tây Nha Trang, Đức Trọng 1, Di Linh) trước mùa mưa; đơn >5 ngày tích mất đền bù; chuẩn hóa đào tạo AM & áp dụng Senior AM từ 01/10', '2. Vận hành (AM & Kho): Đẩy gán trước 10h; dọn sạch tồn lớn (Tây Nha Trang, Đức Trọng 1, Di Linh) trước mùa mưa bão; đơn >5 ngày tích mất; chuẩn hóa đào tạo AM & áp dụng Senior AM từ 01/10')
text = text.replace('1. Nhân sự (AM & HRBP): Cấm duyệt nghỉ tùy tiện (tối đa 1 ngày, cấm 2 người nghỉ cùng lúc); cắt sạch ID đã nghỉ; dứt điểm BHXH; bổ sung 2 TTS tuyển dụng kéo data Lâm Đồng & Khánh Hòa', '1. Nhân sự (AM & HRBP): Cấm duyệt nghỉ tùy tiện (tối đa 1 ngày, cấm 2 người nghỉ cùng lúc); cắt sạch ID đã nghỉ; dứt điểm BHXH; thêm 2 TTS tuyển dụng kéo data Lâm Đồng & Khánh Hòa')

# Let's inspect final length
print("ULTRA PERFECT LEN:", len(text))
with open('scratch/report_1809_ready_to_send.txt', 'w', encoding='utf-8') as f:
    f.write(text)
