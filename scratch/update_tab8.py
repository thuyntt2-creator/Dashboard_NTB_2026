# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

new_tab_opr_tts = '''    # ----------------------------------------------------
    # TAB 8: %OPR TIKTOK SHOP
    # ----------------------------------------------------
    {
        "id": "tab-opr-tts",
        "title": "🗣️ PHÂN TÍCH CHUYÊN SÂU HIỆU SUẤT LẤY HÀNG %OPR TIKTOK SHOP (TARGET KPI ≥ 80.0%) (BẬT TAB 8 DASHBOARD):",
        "content": """📍 1. BẢNG 1: TỔNG QUAN %OPR TIKTOK SHOP TOÀN VÙNG & 5 TỈNH THÀNH (W40):
• TỔNG TOÀN VÙNG: 83,48% ➔ Đạt chuẩn SLA sàn ≥ 80,0% (10.526 đơn đạt chuẩn / 12.609 đơn phát sinh | Tổng đơn lỗi trễ hạn: 2.083 đơn).
  - Khung giờ Ngày (9h00 – 19h00): Đạt rất cao 91,63% (6.809 / 7.431 đơn đạt chuẩn | Chỉ lỗi 622 đơn).
  - Khung giờ Đêm (19h00 – 9h00 sáng hôm sau): Sụt giảm nghiêm trọng còn 71,73% (3.718 / 5.183 đơn đạt chuẩn | LỖI TỚI 1.465 ĐƠN, chiếm tới 70,3% tổng lượng đơn lỗi của cả vùng!).
• Xếp hạng %OPR TTS theo 5 Tỉnh thành:
  1. Ninh Thuận: 93,79% (Ngày 97,59%, Đêm 85,19% | Vol 1.676 đơn) ➔ Tỉnh quán quân xuất sắc nhất toàn vùng!
  2. Khánh Hòa: 89,23% (Ngày 94,10%, Đêm 84,57% | Vol 3.157 đơn) ➔ Rất vững vàng, cả ngày và đêm đều trên 84%.
  3. Bình Thuận: 83,45% (Ngày 88,05%, Đêm 77,37% | Vol 4.235 đơn) ➔ Đạt chuẩn tổng nhưng ca đêm còn non.
  4. Lâm Đồng: 75,54% (Ngày 89,58%, ĐÊM CHỈ ĐẠT 48,32% | Vol 2.968 đơn) ➔ KHÔNG ĐẠT KPI 80% ❌
  5. Đắk Nông: 62,80% (Ngày 97,20%, ĐÊM RƠI TỰ DO XUỐNG 7,24% | Vol 578 đơn) ➔ BÁO ĐỘNG ĐỎ KHÔNG ĐẠT KPI ❌

📍 2. BẢNG 2: DANH SÁCH CÁC AM LÀM XUẤT SẮC NHẤT (%OPR TTS ≥ 90.0% — TUYÊN DƯƠNG):
• 1. Nguyễn Thị Tuyết Thơ (Lâm Đồng): OPR Tổng 96,6% (Ngày 98,8%, Đêm 94,7% | Vol 529 đơn — chỉ lỗi 18 đơn) ➔ Quán quân OPR TTS toàn vùng!
• 2. Nguyễn Đỗ Minh Nghĩa (Lâm Đồng): OPR Tổng 95,7% (Ngày 96,9%, Đêm 89,3% | Vol 468 đơn — chỉ lỗi 20 đơn).
• 3. Phan Đình Duy (Khánh Hòa): OPR Tổng 95,1% (Ngày 99,0%, Đêm 85,6% | Vol 446 đơn — chỉ lỗi 22 đơn).
• 4. Nguyễn Duy Long (Ninh Thuận): OPR Tổng 93,8% trên khối lượng cực lớn 1.824 đơn (Ngày 97,3%, Đêm 85,6% — lỗi chỉ 113 đơn).
• 5. Nguyễn Thanh Long (Khánh Hòa): OPR Tổng 100,0% (Đêm 33/33 đơn đạt 100%).
• 6. Thái Thị Thanh Thư (Khánh Hòa): OPR Tổng 90,3% trên khối lượng 1.857 đơn (Ngày 92,2%, Đêm 88,4%).
• 7. Cao Thị Thanh Thủy (Khánh Hòa): OPR Tổng 89,8% trên 1.188 đơn (Ngày 95,3%, Đêm 85,5%).

📍 3. BẢNG 3: DANH SÁCH CÁC AM KHÔNG ĐẠT KPI (< 80.0%) VÀ LỖI CỤ THỂ TỪNG AM:
• 1. Lê Văn Trường (Lâm Đồng): OPR Tổng chỉ đạt 42,6% ➔ Thấp nhất vùng! Lỗi trôi sạch đơn đêm (Đêm đạt vỏn vẹn 11,1%).
• 2. Trần Thị Nhung (Đắk Nông): OPR Tổng chỉ đạt 40,5% ➔ Ngày 98,4% nhưng đêm chỉ đạt 12,2%, bỏ rơi 115 đơn đêm.
• 3. Hồng Bích Nga (Đắk Nông): OPR Tổng 76,3% ➔ Ngày chỉ đạt 80,2%, đêm 61,4%, lỗi trôi đều cả ngày lẫn đêm.
• 4. Huỳnh Thúc Duân (Đắk Nông): OPR Tổng 78,7% ➔ Ngày 96,7% nhưng ca đêm TÊ LIỆT 0,0% (trôi sạch 63 đơn đêm).
• 5. Lê Thanh Nhựt (Bình Thuận): OPR Tổng 78,6% ➔ Ngày 78,5%, đêm 78,6%, để rớt hơn 420 đơn do quá tải điều phối.
• 6. Huỳnh Thị Kim Chi / Lê Minh Lợi / Phan Nguyễn Yến Nhi: OPR Tổng 0,0% (phát sinh đơn đêm nhưng bỏ qua không lấy).

📍 4. BẢNG 4: MỔ XẺ ĐÍCH DANH AM NÀO KÉO TỶ TRỌNG LỖI NHIỀU NHẤT VÙNG (TRÊN TỔNG 2.083 ĐƠN LỖI):
• 🔴 ĐẦU SỎ SỐ 1 KÉO TỤT TOÀN VÙNG: AM LÊ VĂN TRƯỜNG (LÂM ĐỒNG):
  - Gây ra tới 494 ĐƠN LỖI, chiếm 23,7% TỔNG LƯỢNG ĐƠN LỖI CỦA CẢ VÙNG NAM TRUNG BỘ!
  - Riêng ban đêm anh Trường để lỗi tới 434 đơn trên 488 đơn đêm phát sinh (tỷ lệ lỗi đêm lên tới 88,9%!).
• 🔴 ĐẦU SỎ SỐ 2 KÉO TỤT TOÀN VÙNG: AM LÊ THANH NHỰT (BÌNH THUẬN):
  - Gây ra 424 ĐƠN LỖI, chiếm 20,4% TỔNG LƯỢNG ĐƠN LỖI TOÀN VÙNG! (Lỗi ngày 219 đơn, lỗi đêm 205 đơn).
  ➔ ĐẶC BIỆT CHÚ Ý: CHỈ RIÊNG 2 AM LÊ VĂN TRƯỜNG VÀ LÊ THANH NHỰT ĐÃ GÂY RA 918 ĐƠN LỖI, CHIẾM TỚI 44,1% (GẦN MỘT NỬA) TOÀN BỘ ĐƠN HÀNG TRỄ HẠN OPR TTS CỦA CẢ VÙNG!
• 🔴 ĐẦU SỎ SỐ 3: AM HỒNG BÍCH NGA (ĐẮK NÔNG): Gây ra 182 đơn lỗi (chiếm 8,7% tổng lỗi vùng; lỗi ngày 121 đơn, lỗi đêm 61 đơn).
• 🔴 ĐẦU SỎ SỐ 4: AM TRẦN THỊ NHUNG (ĐẮK NÔNG): Gây ra 116 đơn lỗi (chiếm 5,6% tổng lỗi vùng; trong đó lỗi đêm là 115 đơn trên 131 đơn phát sinh).
• 🔴 ĐẦU SỎ SỐ 5: AM HUỲNH THÚC DUÂN (ĐẮK NÔNG): Gây ra 72 đơn lỗi (chiếm 3,5% tổng lỗi vùng; trôi sạch 100% 63 đơn đêm, OPR đêm 0,0%).

🎙️ LỜI THOẠI THUYẾT TRÌNH TỰ NHIÊN (KHI BẬT TAB 8 DASHBOARD %OPR TIKTOK SHOP):
"Kính thưa Ban Giám Đốc và các anh chị AM, chuyển sang Tab 8 là chỉ số OPR TikTok Shop - Tỷ lệ lấy hàng đúng hạn cam kết của sàn:
Trước hết về con số tổng thể: Toàn vùng Nam Trung Bộ của chúng ta tuần W40 đạt 83,48%, chính thức vượt qua ngưỡng chuẩn KPI của sàn là 80,0%.
Tổng lượng đơn phát sinh là 12.609 đơn, trong đó chúng ta lấy chuẩn giờ được 10.526 đơn, và có 2.083 đơn hàng bị vi phạm trễ hẹn.
Tỉnh Ninh Thuận của anh Duy Long tiếp tục là quán quân toàn vùng với OPR đạt tới 93,79%, kế đến là Khánh Hòa 89,23%, và Bình Thuận 83,45%.
Về phía cá nhân các AM xuất sắc: Em xin tuyên dương đặc biệt chị Nguyễn Thị Tuyết Thơ ở Lâm Đồng: Chị Thơ đạt OPR đỉnh toàn vùng 96,6% trên 529 đơn hàng, cả ban ngày (98,8%) lẫn ban đêm (94,7%) đều gần như tuyệt đối!
Anh Nguyễn Đỗ Minh Nghĩa đạt 95,7%, anh Phan Đình Duy đạt 95,1%, và đặc biệt là anh Nguyễn Duy Long gánh sản lượng cực khủng hơn 1.800 đơn mà OPR vẫn giữ vững 93,8%! Chị Thư (90,3%) và chị Thủy (89,8%) cũng hoàn thành rất tốt nhiệm vụ.

TUY NHIÊN, nhìn vào mặt tối của bức tranh, tôi yêu cầu 2 tỉnh Lâm Đồng (75,54%) và Đắk Nông (62,80%) cùng các AM liên quan nhìn thẳng vào sự thật:
Toàn vùng có 2.083 đơn hàng bị trễ hẹn với sàn TikTok Shop, thì tôi hỏi các anh chị: AI LÀ NGƯỜI KÉO TỶ TRỌNG LỖI NHIỀU NHẤT?
Anh Lê Văn Trường và anh Lê Thanh Nhựt đứng dậy!
Hai anh nhìn lên màn hình giúp tôi:
Một mình anh Lê Văn Trường ở Lâm Đồng gây ra tới 494 đơn lỗi, chiếm tới 23,7% — tức là gần một phần tư tổng số đơn lỗi của toàn vùng!
Anh Lê Thanh Nhựt ở Bình Thuận gây ra 424 đơn lỗi, chiếm 20,4% tổng số đơn lỗi!
Cộng hai anh lại là 918 đơn hàng trễ hẹn, chiếm tới 44,1% — gần một nửa số lượng lỗi của cả vùng Nam Trung Bộ nằm trọn trong tay anh Trường và anh Nhựt!
Kế đến là chị Hồng Bích Nga gây ra 182 đơn lỗi (8,7%), chị Trần Thị Nhung gây ra 116 đơn lỗi (5,6%), và anh Huỳnh Thúc Duân gây ra 72 đơn lỗi (3,5%)!

🔍 INSIGHT BẢN CHẤT & BÓC TÁCH GỐC RỄ NGUYÊN NHÂN:
Tại sao anh Trường, anh Nhựt, chị Nhung, anh Duân lại để trôi đơn khủng khiếp như vậy?
Bóc tách ra có 3 nguyên nhân cốt tử:
1. LỖI THỨ NHẤT: TÊ LIỆT HOÀN TOÀN ĐƠN CA ĐÊM (Chiếm tới hơn 70% tổng lượng đơn lỗi toàn vùng - 1.465 / 2.083 đơn):
Đặc thù sàn TikTok Shop là các shop livestream bán hàng bùng nổ từ 20h00 đến 23h30 đêm! Khách đặt hàng nườm nượp, shop in đơn sẵn chờ lấy.
Nhưng bưu cục của anh Trường (Đơn Dương, Xuân Hương), bưu cục của anh Duân (Gia Nghĩa, Nhân Cơ), bưu cục chị Nhung (Cư Jút, Tuy Đức) đúng 18h00 là nhân viên dọn dẹp, 18h30 là Trưởng bưu cục khóa cửa tắt đèn đi về!
Không có ai trực đêm, không có shipper gom chuyến tối! Đơn hàng phát sinh từ 21h đêm qua nằm ngâm chết dí trên app, đến tận 9h30 - 10h00 sáng hôm sau shipper mới tới bưu cục rồi túc tắc đi lấy.
Lúc đó thuật toán của TikTok Shop nó đã tự động quét vi phạm SLA OPR trễ hơn 12 tiếng rồi! Đó là lý do vì sao OPR ban đêm của anh Duân rớt về 0,0%, anh Vũ 9,4%, anh Trường 11,1%, chị Nhung 12,2%!
2. LỖI THỨ HAI: TRỄ CHUYẾN LẤY CA 1 SÁNG:
Shipper buổi sáng đến bưu cục có thói quen chỉ lo tranh nhau bốc hàng đi giao ca 1 cho xong chuyến, bỏ quên toàn bộ các yêu cầu lấy hàng First-mile phát sinh đầu giờ sáng! Mãi đến 11h - 12h trưa đi giao về mới tạt qua shop lấy, dẫn đến 622 đơn ca ngày bị quá hạn cam kết 10h30.
3. LỖI THỨ BA: THIẾU CƠ CHẾ PHÂN LUỒNG SHOP LIVESTREAM:
AM và Trưởng bưu cục không nắm được danh sách các shop có lịch livestream cố định trên địa bàn để bố trí người gom riêng, dẫn đến việc đối xử cào bằng shop lớn với shop gửi lẻ thông thường.

🎯 QUYẾT SÁCH HÀNH ĐỘNG & MỆNH LỆNH TÁC CHIẾN TUẦN W41:
1. Giao đích danh AM Lê Văn Trường và AM Lê Thanh Nhựt: Phải giảm ngay ít nhất 70% lượng đơn lỗi trong tuần W41, đưa OPR TTS của cụm mình vượt mốc 85%!
2. Tất cả bưu cục có shop livestream phát sinh trên 30 đơn/đêm bắt buộc bố trí 1 ca trực tối đến 21h30 hoặc hợp đồng bưu tá gom chuyến chốt lúc 21h00.
3. Xuất bến ca lấy sớm lúc 07h30 sáng, toàn bộ đơn đêm phải được quét lấy và bắn trạng thái 'Đã lấy hàng' lên sàn TikTok Shop trước 08h30 sáng!
4. Giám đốc Vận hành sẽ kiểm tra đột xuất dữ liệu OPR đêm lúc 22h00 và 8h00 sáng mỗi ngày, bưu cục nào để trôi đơn đêm sẽ xử phạt trừ thẳng KPI của Trưởng bưu cục!
Bây giờ, em xin chuyển sang Tab 9 mổ xẻ tình trạng Rớt luân chuyển KTC ạ!\""""
    },'''

with open('scratch/make_final_script.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to replace Tab 8
pattern = r'    # -+\s+# TAB 8: %OPR TIKTOK SHOP\s+# -+\s+\{\s+"id": "tab-opr-tts",.*?"id": "tab-rot-lc",'
match = re.search(pattern, content, re.DOTALL)
if match:
    replacement = new_tab_opr_tts + '\n\n    # ----------------------------------------------------\n    # TAB 9: RỚT LUÂN CHUYỂN KTC\n    # ----------------------------------------------------\n    {\n        "id": "tab-rot-lc",'
    updated_content = content[:match.start()] + replacement + content[match.end():]
    with open('scratch/make_final_script.py', 'w', encoding='utf-8') as f:
        f.write(updated_content)
    print("SUCCESS: make_final_script.py updated with rich Tab 8!")
else:
    print("WARNING: Pattern not matched directly, using string find.")
    p1 = content.find('    # ----------------------------------------------------\n    # TAB 8: %OPR TIKTOK SHOP')
    p2 = content.find('    # ----------------------------------------------------\n    # TAB 9: RỚT LUÂN CHUYỂN KTC')
    if p1 != -1 and p2 != -1:
        updated_content = content[:p1] + new_tab_opr_tts + '\n\n' + content[p2:]
        with open('scratch/make_final_script.py', 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print("SUCCESS: make_final_script.py updated using string slice!")
    else:
        print("ERROR: Could not find anchor positions.")
