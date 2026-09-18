# -*- coding: utf-8 -*-

with open('scratch/report_perfect_words.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace with standard metric label
text = text.replace("• Tỷ lệ: GTC 7 ngày:", "• Tỷ lệ: GTC 7D:")
text = text.replace("• Bưu cục bất ổn: 12/85 BC (14.1%) - Nhóm 1: 11 BC | Nhóm 2: 01 BC", "• BC bất ổn: 12/85 BC (14.1%) - Nhóm 1: 11 BC | Nhóm 2: 01 BC")

# Trim Section 3
text = text.replace("1. Nhân sự (AM & HRBP): Cấm duyệt nghỉ tùy tiện (tối đa 1 ngày, cấm 2 người nghỉ cùng lúc); cắt sạch ID đã nghỉ; dứt điểm BHXH; thêm 2 thực tập sinh tuyển dụng cho Lâm Đồng & Khánh Hòa", "1. Nhân sự (AM & HRBP): Cấm duyệt nghỉ tùy tiện (tối đa 1 ngày, cấm 2 người nghỉ cùng lúc); cắt sạch ID đã nghỉ; dứt điểm BHXH; thêm 2 TTS tuyển dụng kéo data Lâm Đồng & Khánh Hòa")
text = text.replace("2. Vận hành (AM & Kho): Đẩy gán trước 10h; dọn sạch tồn lớn (Tây Nha Trang, Đức Trọng 1, Di Linh) trước mùa mưa; đơn >5 ngày tích mất đền bù; chuẩn hóa đào tạo AM & áp dụng Senior AM từ 01/10", "2. Vận hành (AM & Kho): Đẩy gán trước 10h; dọn sạch kho tồn lớn (Tây Nha Trang, Đức Trọng 1, Di Linh) trước mùa mưa; đơn >5 ngày tích mất đền bù; chuẩn hóa đào tạo AM & áp dụng Senior AM từ 01/10")

print("TWEAKED LEN:", len(text))

# Let's inspect length
with open('scratch/report_full_labels_tight.txt', 'w', encoding='utf-8') as f:
    f.write(text)
