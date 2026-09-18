# -*- coding: utf-8 -*-

with open('scratch/report_1809_safe_final.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Shave 150 chars
text = text.replace('• 7D: 16.9% | N-1: 19.1% | Vol: 1,921 | FD: 49.0% | ODR: 63.3%', '• 7D: 16.9% | N-1: 19.1% | Vol: 1,921 | FD: 49% | ODR: 63.3%')
text = text.replace('• 7D: 23.2% | N-1: 23.7% | Vol: 992 | FD: 17.2% | ODR: 40.0%', '• 7D: 23.2% | N-1: 23.7% | Vol: 992 | FD: 17.2% | ODR: 40%')
text = text.replace('• 7D: 26.3% | N-1: 24.1% | Vol: 2,167 | FD: 21.4% | ODR: 28.0%', '• 7D: 26.3% | N-1: 24.1% | Vol: 2,167 | FD: 21.4% | ODR: 28%')
text = text.replace('• 7D: 30.1% | N-1: 30.0% | Vol: 793 | FD: 6.0% | ODR: 24.6%', '• 7D: 30.1% | N-1: 30% | Vol: 793 | FD: 6% | ODR: 24.6%')
text = text.replace('• 7D: 35.2% | N-1: 29.4% | Vol: 1,074 | FD: 12.8% | ODR: 75.0%', '• 7D: 35.2% | N-1: 29.4% | Vol: 1,074 | FD: 12.8% | ODR: 75%')
text = text.replace('• 7D: 50.0% | N-1: 65.0% | Vol: 565 | FD: 3.7% | ODR: 70.8%', '• 7D: 50% | N-1: 65% | Vol: 565 | FD: 3.7% | ODR: 70.8%')

text = text.replace('1. Nhân sự (AM & HRBP): Cấm duyệt nghỉ phép tùy tiện (tối đa 1 ngày, cấm 2 người nghỉ cùng lúc); kiểm kê cắt sạch ID đã nghỉ; dứt điểm thủ tục BHXH; bổ sung 2 TTS tuyển dụng kéo data Lâm Đồng & Khánh Hòa', '1. Nhân sự (AM & HRBP): Cấm duyệt nghỉ tùy tiện (tối đa 1 ngày, cấm 2 người nghỉ cùng lúc); cắt sạch ID đã nghỉ; dứt điểm BHXH; bổ sung 2 TTS tuyển dụng kéo data Lâm Đồng & Khánh Hòa')
text = text.replace('2. Vận hành (AM & Kho): Đẩy tiến độ gán trước 10h; dọn sạch kho tồn lớn (Tây Nha Trang, Đức Trọng 1, Di Linh) trước mùa mưa; đơn >5 ngày tích mất đền bù; chuẩn hóa đào tạo AM và áp dụng Senior AM từ 01/10', '2. Vận hành (AM & Kho): Đẩy gán trước 10h; dọn sạch tồn lớn (Tây Nha Trang, Đức Trọng 1, Di Linh) trước mùa mưa; đơn >5 ngày tích mất đền bù; chuẩn hóa đào tạo AM & áp dụng Senior AM từ 01/10')

print("ULTRA SAFE FINAL LENGTH:", len(text))
with open('scratch/report_1809_ready_to_send.txt', 'w', encoding='utf-8') as f:
    f.write(text)
