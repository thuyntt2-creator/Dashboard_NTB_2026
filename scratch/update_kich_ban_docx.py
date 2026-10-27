import docx

doc = docx.Document('KICH_BAN_THUYET_TRINH_W43_NAM_TRUNG_BO.docx')

# Find paragraph with "XII. MỆNH LỆNH"
idx_target = -1
for i, p in enumerate(doc.paragraphs):
    if 'XII. MỆNH LỆNH' in p.text or '[XII.' in p.text:
        idx_target = i
        break

section_title = "📦 [XI.B. BÁO CÁO TỒN AGING (>5 NGÀY) & TREO LUÂN CHUYỂN REALTIME]"
section_content = """🗣️ LỜI NÓI THUYẾT TRÌNH BÁO CÁO (KÈM CHỈ DẪN NHÌN MÀN HÌNH CHART TAB 12):

"Kính thưa Ban Giám đốc và toàn thể Hội nghị, 

Tiếp theo xin mời các anh chị nhìn lên Tab 12: Giám Sát Aging & Treo Luân Chuyển Realtime. Đây là hai 'ổ bệnh tiềm ẩn' nếu không kiểm soát chặt sẽ trực tiếp bóp nghẹt tỷ lệ giao đúng hạn ODR và làm bùng nổ chi phí đền bù toàn vùng:

📍 1. BÓC TÁCH TỒN AGING (>5 NGÀY TẠI BƯU CỤC): GHI NHẬN 769 ĐƠN
• Toàn vùng hiện có 769 đơn tồn trên 5 ngày. Trong đó:
  - Nhóm 5 – 8 ngày: Chiếm tới 547 đơn (71,1%). Đây là nhóm cần ưu tiên dồn lực gán giao dứt điểm trong ngày hôm nay, không để trôi qua mốc 8 ngày.
  - Nhóm 8 – 15 ngày: Ghi nhận 216 đơn (28,1%).
  - Nhóm nguy cơ đền bù (>15 ngày): Hiện toàn vùng chỉ còn vỏn vẹn 6 đơn (0,8%)! Đây là nỗ lực rất lớn của các AM trong tuần qua khi gần như xóa sổ nhóm trên 15 ngày.
• Phân bổ địa bàn: Tỉnh Lâm Đồng tiếp tục là tâm bão tồn đọng lớn nhất, giữ tới 336 đơn (chiếm 43,7% toàn vùng)! Tiếp theo là Khánh Hòa (168 đơn), Đắk Nông (105 đơn), Bình Thuận (89 đơn) và Ninh Thuận (71 đơn).

📍 2. BÓC TÁCH HÀNG TREO LUÂN CHUYỂN: 3.711 ĐƠN — ĐÚNG HẠN 90,9%
• Toàn vùng NTB đang có 3.711 đơn hàng lưu thông trên các trục đường luân chuyển:
  - Đúng hạn (<24h): Đạt 3.375 đơn (tỷ lệ 90,9%) — Mạng lưới vận tải trục kết nối liên tỉnh duy trì lưu thông tốt.
  - Bắt đầu trễ (24 – 36h): Có 144 đơn (3,9%).
  - Trễ 36 – 72h): Có 127 đơn (3,4%).
  - Trễ nặng (>72h): Có 65 đơn (1,8%) (gồm 36 đơn 72-120h và 29 đơn trên 120h).
  - Tổng đơn Treo ≥24h cần giải tỏa khẩn cấp: 336 đơn (chiếm 9,1% tổng lượng luân chuyển).

📍 3. ĐIỂM DANH TOP 5 AM ĐIỂM NÓNG TREO LUÂN CHUYỂN CẦN GIẢI TỎA GẤP:
• 1. AM Lê Hồng Phong (Đắk Nông): Nặng nhất toàn vùng với 53 đơn treo ≥24h trên tổng 198 đơn luân chuyển — tỷ lệ treo lên tới 26,8%! (Gồm 19 đơn 24-36h, 24 đơn 36-72h và 10 đơn trôi quá 72h).
• 2. AM Trần Thị Nhung (Đắk Nông): Treo 49 đơn ≥24h (13,9% tổng LC).
• 3. AM Huỳnh Thị Kim Chi (Lâm Đồng): Treo 41 đơn ≥24h (tỷ lệ treo rất cao 24,6% tổng LC).
• 4. AM Nguyễn Thanh Long (Khánh Hòa): Treo 39 đơn ≥24h (tỷ lệ treo 24,1% tổng LC).
• 5. AM Nguyễn Duy Long (Ninh Thuận): Treo 30 đơn ≥24h.

📍 4. MỆNH LỆNH ĐIỀU HÀNH VẬN TẢI & BƯU CỤC TRONG 24H:
1. KTC & Điều xe: Rà soát ngay các chuyến xe kết nối Đắk Nông và Lâm Đồng; bưu cục đích bắt buộc quét nhận kiện ngay khi xe cập bến, nghiêm cấm tình trạng xe đến nhưng bưu cục chưa quét nhận ngâm bao ảo!
2. Giải phóng dứt điểm: 4 AM Phong, Nhung, Chi, Long phải trực tiếp theo dõi, giải phóng dứt điểm 192 đơn trễ ≥36h ngay trong ngày hôm nay 27/10!\""""

if idx_target != -1:
    p_ref = doc.paragraphs[idx_target]
    p_title = p_ref.insert_paragraph_before(section_title)
    p_title.runs[0].font.bold = True
    p_title.runs[0].font.size = docx.shared.Pt(14)
    p_title.runs[0].font.color.rgb = docx.shared.RGBColor(180, 83, 9)
    
    p_body = p_ref.insert_paragraph_before(section_content)
    p_ref.insert_paragraph_before("")
    print(f"Inserted section before paragraph {idx_target}")
else:
    doc.add_paragraph(section_title)
    doc.add_paragraph(section_content)
    print("Appended section at end")

doc.save('KICH_BAN_THUYET_TRINH_W43_NAM_TRUNG_BO.docx')
print("Successfully saved KICH_BAN_THUYET_TRINH_W43_NAM_TRUNG_BO.docx")
