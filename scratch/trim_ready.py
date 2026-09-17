# -*- coding: utf-8 -*-

with open('scratch/safe_report_tight.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Trim some small filler words
text = text.replace('• NN: Hụt 50% NV, ngập hàng to, sợ truy thu né hàng cũ làm đọng 401 đơn, FD 42.6%', '• NN: Hụt 50% NV, ngập hàng to, sợ truy thu né hàng cũ làm đọng 401 đơn, hoàn FD 42.6%')
text = text.replace('• GP: Bàn giao hàng vật lý tận tay tại kho, cấm gán ảo trên app (Đức Trọng 1, Di Linh); trần tải 110 đơn/NV', '1. Bàn giao hàng vật lý tận tay tại kho, cấm gán ảo trên app (Đức Trọng 1, Di Linh); trần tải 110 đơn/NV')
text = text.replace('2. HRBP dồn lực tuyển bù định biên tại điểm nóng (Cam Linh 5 NV, Tây Nha Trang 6 NV, Đức Trọng 1 3 NV); chính sách kích thích giữ chân BC bất ổn', '2. HRBP dồn lực tuyển bù định biên điểm nóng (Cam Linh 5 NV, Tây Nha Trang 6 NV, Đức Trọng 1 3 NV); ra chính sách kích thích giữ chân nhân sự')

# Let's check length
print("Final Len:", len(text))
with open('scratch/final_ready.txt', 'w', encoding='utf-8') as f:
    f.write(text)
