import sys, os

with open('scratch/build_w38_redesigned_final.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Let's inspect Section 3 in build_w38_redesigned_final.py
old_sec3_am = '''        am_analysis_block=[
            "Kính thưa Ban Giám Đốc, nhìn vào hiệu suất %GTC của từng AM, chúng ta thấy một bức tranh phân hóa cực kỳ gay gắt:",
            "• Top 3 AM có tỷ lệ %GTC xuất sắc nhất vùng:",
            "  1. AM Nguyễn Ngọc Khánh: Đạt 75,1% GTC (+0,2%p WoW) — giữ vững vị trí số 1 toàn vùng về chất lượng giao.",
            "  2. AM Cao Thị Thanh Thủy: Đạt 71,1% GTC (+2,3%p WoW) — có sự cải thiện rất ấn tượng.",
            "  3. AM Nguyễn Đỗ Minh Nghĩa: Đạt 70,8% GTC (+5,1%p WoW — AM tăng trưởng %GTC mạnh nhất tuần qua).",
            "• Nhóm AM giữ nhịp khá (từ 56% đến 65%): AM Thái Thị Thanh Thư (64,2%), AM Nguyễn Hoàng Phi (61,5%), AM Lê Thanh Nhựt (58,7%), AM Nguyễn Duy Long (57,9%).",
            "• Nhóm 3 AM báo động đỏ — kéo tụt chỉ số của toàn vùng:",
            "  1. AM Nguyễn Thanh Long: %GTC tụt dốc thảm hại chỉ còn 36,7% (giảm sốc -10,2%p so với tuần trước), nguyên nhân chính do bưu cục Cam Linh bị nghẽn mạch.",
            "  2. AM Lê Minh Lợi: %GTC chỉ đạt 32,1% (giảm -5,0%p WoW) tại cụm bưu cục Lang Biang 1.",
            "  3. AM Trương Quang Linh: %GTC rơi xuống đáy 16,8% (-1,6%p WoW) — thấp nhất toàn quốc, bưu cục Quảng Tín gần như tê liệt giao hàng."
        ],'''

new_sec3_am = '''        am_analysis_block=[
            "Kính thưa Ban Giám Đốc, đi sâu bóc tách chi tiết hiệu suất %GTC của toàn bộ 18 AM phụ trách tuần W38 theo 4 nhóm phân hóa rõ rệt:",
            "🏆 1. NHÓM 5 AM XUẤT SẮC DẪN ĐẦU VÙNG (GTC TRÊN 67% — ĐẠT CHUẨN XANH SLA):",
            "  • Top 1 - AM Nguyễn Ngọc Khánh: Đạt 75,1% GTC (+0,2%p WoW, sản lượng 35.925 đơn) — Giữ vững vị trí số 1 toàn vùng về chất lượng giao hàng.",
            "  • Top 2 - AM Cao Thị Thanh Thủy: Đạt 71,1% GTC (+2,3%p WoW, sản lượng 23.291 đơn) — Duy trì phong độ xuất sắc liên tục 3 tuần.",
            "  • Top 3 - AM Nguyễn Đỗ Minh Nghĩa: Đạt 70,8% GTC (+5,1%p WoW, sản lượng 11.587 đơn) — Một trong những AM tăng trưởng %GTC ấn tượng nhất.",
            "  • Top 4 - AM Thái Thị Thanh Thư: Đạt 68,7% GTC (+1,8%p WoW, sản lượng 44.533 đơn) — Vừa gánh tải lớn vừa bảo vệ tỷ lệ giao thành công cao.",
            "  • Top 5 - AM Nguyễn Duy Long: Đạt 67,9% GTC (+0,1%p WoW, sản lượng khủng 58.928 đơn) — Trụ cột vững chắc nhất của khu vực Bình Thuận.",
            "📈 2. NHÓM 5 AM GIỮ NHỊP KHÁ & TĂNG TRƯỞNG TÍCH CỰC (56% – 66%):",
            "  • AM Nguyễn Thị Tuyết Thơ: Đạt 65,5% GTC (W37: 68,4%, -2,9%p, sản lượng 13.329 đơn).",
            "  • AM Nguyễn Hoàng Phi: Đạt 65,2% GTC (tăng vọt +5,6%p WoW từ 59,5%, sản lượng 34.940 đơn) ➔ AM có bước nhảy %GTC mạnh nhất toàn mạng!",
            "  • AM Lê Thanh Nhựt: Đạt 61,7% GTC (W37: 64,2%, -2,5%p, sản lượng lớn 46.621 đơn).",
            "  • AM Huỳnh Thị Kim Chi: Đạt 57,0% GTC (tăng +3,1%p WoW từ 53,8%, sản lượng 21.270 đơn).",
            "  • AM Trần Thị Nhung: Đạt 56,9% GTC (W37: 56,8%, +0,1%p, sản lượng 40.617 đơn).",
            "⚠️ 3. NHÓM 3 AM SUY GIẢM TIỆM CẬN (46% – 49% — CẦN ĐÔN ĐỐC):",
            "  • AM Hồng Bích Nga: Đạt 48,4% GTC (giảm -3,8%p WoW từ 52,2%, sản lượng 38.777 đơn tại Di Linh - Bảo Lộc).",
            "  • AM Phan Đình Duy: Đạt 47,6% GTC (giảm -5,2%p WoW từ 52,8%, sản lượng 45.503 đơn).",
            "  • AM Huỳnh Thúc Duân: Đạt 46,1% GTC (giảm -2,0%p WoW từ 48,1%, sản lượng 9.432 đơn).",
            "🚨 4. NHÓM 5 AM BÁO ĐỘNG ĐỎ — KÉO TỤT TOÀN BỘ CHỈ SỐ VÙNG (< 42%):",
            "  • AM Lê Văn Trường (Lâm Đồng): Chỉ đạt 41,2% GTC (giảm sốc -6,6%p WoW từ 47,8%). Đáng nguy hại nhất là AM Trường gánh tới 61.755 đơn — sản lượng lớn nhất toàn vùng — nên mức rơi này kéo tụt trực tiếp ~1,5%p của cả vùng!",
            "  • AM Nguyễn Lê Nguyên Vũ: Đạt 37,2% GTC (W37: 38,2%, -1,0%p, sản lượng 32.204 đơn).",
            "  • AM Nguyễn Thanh Long: Tụt dốc thảm hại chỉ còn 36,7% GTC (giảm mạnh nhất vùng -10,2%p WoW từ 46,9%, 32.049 đơn), bưu cục Cam Linh bị quá tải.",
            "  • AM Lê Minh Lợi: Chỉ đạt 32,1% GTC (giảm -5,0%p WoW từ 37,0%, 7.630 đơn) tại cụm bưu cục Lang Biang 1.",
            "  • AM Trương Quang Linh: Rơi xuống đáy 16,8% GTC (W37: 18,4%, -1,6%p, 7.457 đơn) ➔ Mức thấp nhất toàn quốc, bưu cục Quảng Tín tê liệt giao hàng."
        ],'''

if old_sec3_am in code:
    code = code.replace(old_sec3_am, new_sec3_am)
    print("Replaced Section 3 AM analysis with all 18 AMs categorized!")
else:
    print("Could not find old_sec3_am, let's inspect")

with open('scratch/build_w38_redesigned_final.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Saved updated scratch/build_w38_redesigned_final.py")
