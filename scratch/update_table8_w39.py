import docx
import sys
sys.stdout.reconfigure(encoding='utf-8')

table8_content = """🗣️ TỶ LỆ RỚT LUÂN CHUYỂN KTC — ĐIỂM NÓNG BÁO ĐỘNG TẠI CÁT TIÊN & PHÂN ĐỊNH AM ĐẠT / KHÔNG ĐẠT KPI (TARGET RỚT LUÂN CHUYỂN ≤ 2,00%) W39 vs W38:

📍 1. BẢNG TỔNG QUAN RỚT LUÂN CHUYỂN KTC TOÀN VÙNG & 5 TỈNH THÀNH (W39 vs W38):
• Top 1 - Bình Thuận: Tỷ lệ rớt chỉ 0,16% (-0,72%p so với 0,88% W38) | Tổng 3.041 đơn luân chuyển ➔ Quán quân toàn vùng, kiểm soát xe tải KTC xuất sắc nhất.
• Top 2 - Khánh Hòa: Tỷ lệ rớt chỉ 0,53% (-4,55%p so với 5,09% W38) | Tổng 3.556 đơn luân chuyển ➔ Bứt phá giảm rớt hàng ngoạn mục, kéo tỷ lệ về mức rất an toàn.
• Top 3 - Ninh Thuận: Tỷ lệ rớt 2,40% (+1,26%p so với 1,14% W38) | Tổng 1.624 đơn luân chuyển ➔ Vượt ngưỡng an toàn 2,0%, rớt chủ yếu ở Phước Dinh (36 đơn).
• Top 4 - Lâm Đồng: Tỷ lệ rớt 3,76% (+0,44%p so với 3,32% W38) | Tổng 2.339 đơn luân chuyển ➔ Tỉnh có tỷ lệ rớt cao thứ nhì, vướng nặng tại bưu cục Cát Tiên và Ninh Gia.
• Top 5 - Đắk Nông: Tỷ lệ rớt 3,83% (-16,90%p so với 20,73% W38) | Tổng 392 đơn luân chuyển ➔ Bước chuyển biến tích cực khi giảm từ mức đỉnh điểm 20,73% xuống 3,83%, nhưng vẫn chưa đạt trần 2,0%.
➔ TOÀN VÙNG W39: Tỷ lệ rớt luân chuyển giảm mạnh từ 3,32% xuống 1,52% (-1,81%p WoW, giảm hơn một nửa!). Tổng lượng đơn cần luân chuyển toàn vùng là 10.952 đơn, số đơn bị rớt giảm từ 252 đơn xuống chỉ còn 166 đơn (giảm được 86 đơn rớt, tương đương giảm -34,1%). Vùng đã hoàn thành xuất sắc cam kết đưa tỷ lệ rớt toàn vùng về dưới ngưỡng 2,00%!

👤 2. BÓC TÁCH CHI TIẾT HIỆU SUẤT THEO AM — PHÂN ĐỊNH ĐẠT & KHÔNG ĐẠT KPI (TARGET RỚT LUÂN CHUYỂN ≤ 2,00%):

🟢 NHÓM ĐẠT KPI (≤ 2,00% — KIỂM SOÁT VẬN HÀNH XUẤT SẮC / CẢI THIỆN MẠNH): Gồm 9 AM:
  1. AM Cao Thị Thanh Thủy (Bình Thuận): Rớt 0,00% (0/934 đơn rớt) — Đạt chuẩn tuyệt đối 100%, không để rớt bất kỳ kiện hàng nào lên xe KTC!
  2. AM Phan Đình Duy: Rớt 0,00% (0/387 đơn rớt) — Hoàn hảo 0,00%, cải thiện triệt để từ 2,84% tuần trước (-2,84%p).
  3. AM Huỳnh Thị Kim Chi: Rớt 0,00% (0/4 đơn rớt).
  4. AM Lê Thanh Nhựt (Bình Thuận): Rớt 0,07% (chỉ rớt duy nhất 1 đơn / 1.432 đơn cần luân chuyển) — Tỷ lệ gần như tuyệt đối, giảm từ 1,72% (-1,65%p).
  5. AM Nguyễn Hoàng Phi (Khánh Hòa): Rớt 0,23% (chỉ rớt 2 đơn / 852 đơn) — Giảm mạnh từ 2,84% (-2,60%p).
  6. AM Trần Thị Nhung (Đắk Nông): Rớt 0,58% (chỉ rớt 1 đơn / 172 đơn) — Cú lội ngược dòng ngoạn mục nhất vùng, tuần W38 rớt 19,76% thì tuần này giảm sâu -19,18%p!
  7. AM Thái Thị Thanh Thư (Khánh Hòa): Rớt 0,63% (rớt 14 đơn / 2.205 đơn luân chuyển) — Giảm sâu từ 7,13% tuần trước (-6,50%p).
  8. AM Nguyễn Ngọc Khánh (Khánh Hòa): Rớt 0,74% (chỉ rớt 4 đơn / 543 đơn) — Giảm từ 1,83% (-1,10%p).
  9. AM Lê Văn Trường (Lâm Đồng): Rớt 1,25% (rớt 7 đơn / 560 đơn) — Đạt chuẩn dưới 2%, giảm từ 4,24% (-2,99%p), số đơn rớt tập trung tại Lâm Viên 2 (7 đơn).

🔴 NHÓM KHÔNG ĐẠT KPI (> 2,00% — ĐIỂM NÓNG BÁO ĐỘNG ĐỎ CẦN CHẤN CHỈNH NGAY): Gồm 8 AM:
  1. AM Nguyễn Đỗ Minh Nghĩa (Khánh Hòa/Lâm Đồng): Tỷ lệ rớt 12,09% (rớt tới 48 đơn / 397 đơn cần luân chuyển). Tuần W38 chỉ rớt 0,40%, tuần này tăng vọt +11,69%p! ĐIỂM NÓNG BÁO ĐỘNG ĐỎ CỦA TOÀN VÙNG! Riêng một mình bưu cục (LDO) Cát Tiên rớt tới 48/134 đơn (tỷ lệ rớt 35,8%), chiếm gần 30% tổng số đơn rớt của cả vùng Nam Trung Bộ!
  2. AM Huỳnh Thúc Duân (Đắk Nông): Tỷ lệ rớt 5,83% (12 đơn rớt / 206 đơn). Mặc dù đã giảm từ 20,79%, nhưng vẫn cao gần gấp 3 lần trần 2,0%. Trọng tâm tại bưu cục (DNO) Nhân Cơ rớt 9/45 đơn (20,0%).
  3. AM Nguyễn Thị Tuyết Thơ (Lâm Đồng): Tỷ lệ rớt 2,87% (10 đơn rớt / 349 đơn), tăng +0,72%p từ 2,15%. Điểm nghẽn tại bưu cục (LDO) Ninh Gia rớt 7/22 đơn (31,8%).
  4. AM Nguyễn Thanh Long (Cam Ranh): Tỷ lệ rớt 2,68% (3 đơn rớt / 112 đơn), tăng từ 0,00%. Điểm nghẽn tại bưu cục (KHO) Cam Lâm 2 rớt 3/9 đơn (33,3%).
  5. AM Hồng Bích Nga (Đắk Nông): Tỷ lệ rớt 2,33% (20 đơn rớt / 858 đơn). Đã giảm từ 4,49% (-2,16%p), nhưng vẫn vướng bưu cục (DNO) Kiến Đức rớt 2/14 đơn (14,3%) và một số kho vệ tinh.
  6. AM Nguyễn Duy Long (Ninh Thuận): Tỷ lệ rớt 2,22% (39 đơn rớt / 1.756 đơn), tăng +1,20%p từ 1,02%. Do sản lượng luân chuyển toàn tỉnh rất lớn, điểm nóng rớt nặng tại bưu cục (NTH) Phước Dinh rớt tới 36/699 đơn (5,2%) và Thuận Nam rớt 1/2 đơn (50%).
  7. AM Nguyễn Lê Nguyên Vũ: Tỷ lệ rớt 2,17% (4 đơn rớt / 184 đơn), giảm nhẹ từ 2,60% nhưng vẫn nhỉnh hơn ngưỡng 2,0%.
  8. AM Lê Minh Lợi: Tỷ lệ 100% do tuần này chỉ phát sinh đúng 1 đơn cần luân chuyển tại bưu cục (LDO) Lang Biang - Đà Lạt 1 và đơn này bị rớt lại kho.

🔍 3. INSIGHT VẬN HÀNH & TOP 10 BƯU CỤC RỚT HÀNG CAO NHẤT VÙNG:
• Bảng xếp hạng các bưu cục có tỷ lệ rớt cao nhất tuần W39:
  1. Lang Biang - Đà Lạt 1 (AM Lợi): 1/1 đơn (100%)
  2. Thuận Nam (AM Long Ninh Thuận): 1/2 đơn (50%)
  3. Cát Tiên (AM Nghĩa): 48/134 đơn (35,8%) — Ổ rớt hàng lớn nhất toàn vùng!
  4. Cam Lâm 2 (AM Long Cam Ranh): 3/9 đơn (33,3%)
  5. Ninh Gia (AM Thơ): 7/22 đơn (31,8%)
  6. Nhân Cơ (AM Duân): 9/45 đơn (20,0%)
  7. Kiến Đức (AM Nga): 2/14 đơn (14,3%)
  8. Bảo An (AM Long Ninh Thuận): 1/8 đơn (12,5%)
  9. Lâm Viên - Đà Lạt 2 (AM Trường): 7/106 đơn (6,6%)
  10. Phước Dinh (AM Long Ninh Thuận): 36/699 đơn (5,2%)
• Bản chất nguyên nhân hiện trường: Rớt đơn luân chuyển KTC hoàn toàn là lỗi chủ quan của khâu vận hành bưu cục, gồm 2 nguyên nhân cốt lõi:
  + Một là đóng bao muộn, trễ giờ cắt chuyển (Cut-off time), xe tải KTC theo lịch trình chuẩn không thể chờ đợi nên buộc phải xuất bến.
  + Hai là bưu tá gom hàng ca chiều về kho phân loại trễ hoặc bao hàng đã đóng seal nhưng nhân viên kho để sót trong góc, không kiểm tra quét mã seal bàn giao lên xe tải. Mỗi kiện hàng rớt luân chuyển KTC khiến thời gian giao đến khách bị chậm thêm từ 24h đến 48h, nguy cơ phát sinh khiếu nại bồi hoàn rất cao!

🎯 4. CHỈ ĐẠO HÀNH ĐỘNG & GIAO NHIỆM VỤ ĐÍCH DANH:
• Anh Nghĩa (AM phụ trách bưu cục Cát Tiên): Yêu cầu Trưởng bưu cục Cát Tiên lập biên bản giải trình sự cố ngay trong hôm nay: Vì sao để rớt tới 48 đơn hàng (chiếm 35,8% sản lượng luân chuyển của kho)? Nếu do lỗi đóng bao trễ hay bỏ sót bao, xử lý trách nhiệm cá nhân trực tiếp. Không để tái diễn tình trạng này sang W40!
• Anh Long (Ninh Thuận): Kiểm tra ngay quy trình bàn giao tại bưu cục Phước Dinh (rớt 36 đơn). Yêu cầu Trưởng bưu cục Phước Dinh rà soát lại giờ xe tải KTC ghé kho và thiết lập chốt kiểm đếm 100% bao hàng trước khi xe lăn bánh.
• Anh Duân, chị Thơ, anh Long (Cam Ranh): Chấn chỉnh tại các bưu cục Nhân Cơ (9 đơn), Ninh Gia (7 đơn), Cam Lâm 2 (3 đơn). Yêu cầu đóng bao, kẹp seal và gom hàng xong trước giờ xe KTC đến tối thiểu 20 phút.
• Khen ngợi & nhân rộng quy trình: Biểu dương chị Thủy (0% rớt / 934 đơn), anh Duy (0% / 387 đơn), anh Nhựt (0,07% / 1.432 đơn) và chị Nhung (giảm từ 19,8% xuống 0,6%). Đề nghị các AM học tập cách bưu cục Bình Thuận kiểm soát bàn giao KTC để toàn vùng duy trì bền vững tỷ lệ rớt dưới 1,5%!"""

for fn in ['KICH_BAN_THUYET_TRINH_MOI_NHAT.docx', 'KICH_BAN_THUYET_TRINH_W39_INSIGHT_CHUYEN_SAU.docx']:
    try:
        doc = docx.Document(fn)
        if len(doc.tables) > 8:
            t8 = doc.tables[8]
            t8.rows[0].cells[0].text = table8_content
            doc.save(fn)
            print(f"Updated Table 8 in {fn} successfully.")
        else:
            print(f"File {fn} has less than 9 tables.")
    except Exception as e:
        print(f"Error updating {fn}: {e}")
