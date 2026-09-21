import re, sys, os

# Let's inspect build_w38_redesigned_final.py and replace the province_block and speech in Section 3
with open('scratch/build_w38_redesigned_final.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace Section 3 province block and text
old_sec3 = '''        province_block=[
            "• Top 1 - Khánh Hòa: 58,9% GTC (dẫn đầu vùng, duy trì trên mốc 58%).",
            "• Top 2 - Bình Thuận: 57,2% GTC (ổn định vị trí thứ 2).",
            "• Top 3 - Ninh Thuận: 55,1% GTC.",
            "• Top 4 - Đắk Nông: 54,1% GTC.",
            "• Top 5 - Lâm Đồng: 53,8% GTC (thấp nhất vùng, kéo lùi mặt bằng chung).",
            "➔ TOÀN VÙNG: %GTC Full hàng đạt 55,75% (giảm -2,03%p so với W37 57,78%) | TikTok Shop đạt 54,01%."
        ],'''

new_sec3 = '''        province_block=[
            "• Top 1 - Bình Thuận: Full W38 đạt 69,2% (W37: 69,7%, -0,5%p) | TTS W38 đạt 68,1% (W37: 68,7%, -0,6%p) ➔ Dẫn đầu toàn vùng, vững vàng đạt chuẩn SLA xanh!",
            "• Top 2 - Ninh Thuận: Full W38 đạt 65,7% (W37: 65,7%, +0,0%p) | TTS W38 đạt 63,1% (W37: 62,7%, +0,4%p) ➔ Vững vàng đạt chuẩn SLA xanh!",
            "• Top 3 - Khánh Hòa: Full W38 đạt 55,3% (W37: 57,6%, -2,3%p) | TTS W38 đạt 54,2% (W37: 57,5%, -3,3%p) ➔ Mức tiệm cận, có dấu hiệu suy giảm sâu ở kênh TTS (-3,3%p).",
            "• Top 4 - Lâm Đồng: Full W38 đạt 48,0% (W37: 50,9%, -2,9%p) | TTS W38 đạt 46,9% (W37: 49,2%, -2,3%p) ➔ Báo động: Rơi xuống dưới 50%, sụt giảm mạnh nhất vùng (-2,9%p)!",
            "• Top 5 - Đắk Nông: Full W38 đạt 46,8% (W37: 48,6%, -1,8%p) | TTS W38 đạt 44,5% (W37: 45,6%, -1,1%p) ➔ Thấp nhất toàn vùng, cảnh báo đỏ cả Full hàng và TikTok Shop.",
            "➔ TOÀN VÙNG W38: %GTC Full hàng đạt 55,75% (giảm -2,02%p WoW so với W37 57,78%) | TikTok Shop đạt 54,01% (giảm -1,90%p WoW so với W37 55,91%)."
        ],'''

assert old_sec3 in code, "old_sec3 not found in build_w38_redesigned_final.py"
code = code.replace(old_sec3, new_sec3)

# Also check Section 6 (%ODR) province block
old_sec6 = '''        province_block=[
            "• Top 1 - Khánh Hòa: 93,1% ODR (Vượt chuẩn SLA xanh ≥92%).",
            "• Top 2 - Bình Thuận: 92,4% ODR (Vượt chuẩn SLA xanh ≥92%).",
            "• Top 3 - Ninh Thuận: 91,0% ODR (Cận kề chuẩn SLA).",
            "• Top 4 - Đắk Nông: 90,1% ODR.",
            "• Top 5 - Lâm Đồng: 89,8% ODR (Dưới chuẩn SLA, kéo tụt mặt bằng vùng).",
            "➔ TOÀN VÙNG: Full hàng đạt 91,2% | TikTok Shop đạt 91,5% (Cách vạch đích 92% chỉ 0,5% - 0,8%p)."
        ],'''

new_sec6 = '''        province_block=[
            "• Top 1 - Ninh Thuận: Full W38 đạt 96,5% (+0,5%p WoW) | TTS W38 đạt 96,6% (+0,7%p WoW) ➔ Dẫn đầu toàn vùng, vượt xa chuẩn SLA ≥92.0%!",
            "• Top 2 - Bình Thuận: Full W38 đạt 96,2% (-0,2%p WoW) | TTS W38 đạt 95,9% (-0,4%p WoW) ➔ Vững vàng trong nhóm xuất sắc xanh.",
            "• Top 3 - Khánh Hòa: Full W38 đạt 94,6% (+0,4%p WoW) | TTS W38 đạt 93,7% (-0,7%p WoW) ➔ Đạt chuẩn xanh SLA an toàn.",
            "• Top 4 - Đắk Nông: Full W38 đạt 90,5% (+1,4%p WoW) | TTS W38 đạt 90,3% (+1,7%p WoW) ➔ Cải thiện tốt nhưng vẫn chưa chạm chuẩn SLA ≥92.0%.",
            "• Top 5 - Lâm Đồng: Full W38 đạt 90,2% (+0,7%p WoW) | TTS W38 đạt 88,9% (+1,1%p WoW) ➔ Thấp nhất vùng, TTS dưới 90% cần tập trung kéo lên.",
            "➔ TOÀN VÙNG W38: %ODR Full hàng đạt 91,24% (cách chuẩn 92% chỉ 0,76%p) | TikTok Shop đạt 91,54% (cách chuẩn 92% chỉ 0,46%p)."
        ],'''

if old_sec6 in code:
    code = code.replace(old_sec6, new_sec6)
    print("Replaced Section 6 ODR province block")

# Also check Section 7 (%LTC) province block
old_sec7 = '''        province_block=[
            "• Top 1 - Khánh Hòa: 96,2% LTC TikTok Shop | 91,5% Full hàng.",
            "• Top 2 - Bình Thuận: 95,8% LTC TikTok Shop | 91,0% Full hàng.",
            "• Top 3 - Lâm Đồng: 95,1% LTC TikTok Shop | 90,2% Full hàng.",
            "• Top 4 - Đắk Lắk: 94,8% LTC TikTok Shop | 89,9% Full hàng.",
            "• Top 5 - Đắk Nông: 94,3% LTC TikTok Shop | 88,5% Full hàng.",
            "➔ TOÀN VÙNG: %LTC Full hàng đạt 90,4% | TikTok Shop bứt phá 95,4% (Đỉnh 2 tháng, cả 5/5 tỉnh đều vượt mốc 94%)."
        ],'''

new_sec7 = '''        province_block=[
            "• Top 1 - Ninh Thuận: Full W38 đạt 95,1% | TTS W38 bứt phá 98,6% (+1,2%p WoW) ➔ Tỷ lệ lấy hàng cao nhất toàn vùng!",
            "• Top 2 - Khánh Hòa: Full W38 đạt 91,3% | TTS W38 đạt đỉnh 98,4% (+2,0%p WoW).",
            "• Top 3 - Bình Thuận: Full W38 đạt 89,1% (+1,9%p WoW) | TTS W38 đạt 93,9%.",
            "• Top 4 - Lâm Đồng: Full W38 đạt 89,2% (+0,1%p WoW) | TTS W38 tăng vọt 92,4% (+7,3%p WoW).",
            "• Top 5 - Đắk Nông: Full W38 đạt 88,7% | TTS W38 đạt 90,1% (+0,3%p WoW).",
            "➔ TOÀN VÙNG W38: %LTC Full hàng đạt 90,36% (+0,06%p WoW) | TikTok Shop bứt phá ngoạn mục đạt 95,43% (+1,88%p WoW, đỉnh 2 tháng!)."
        ],'''

if old_sec7 in code:
    code = code.replace(old_sec7, new_sec7)
    print("Replaced Section 7 LTC province block")

# Also check Section 9 (Rót LC) province block
old_sec9 = '''        province_block=[
            "• Đắk Nông: Tỷ lệ rớt 20,73% (57 đơn rớt / 275 đơn cần luân chuyển) ➔ Tỷ lệ rớt kỷ lục, gấp 6 lần bình quân vùng!",
            "• Khánh Hòa: Tỷ lệ rớt 5,09% (102 đơn rớt / 2.005 đơn) ➔ Số lượng đơn rớt lớn nhất vùng.",
            "• Lâm Đồng: Tỷ lệ rớt 3,32% (58 đơn rớt / 1.748 đơn).",
            "• Ninh Thuận: Tỷ lệ rớt 1,14% (16 đơn rớt / 1.399 đơn).",
            "• Bình Thuận: Tỷ lệ rớt 0,88% (19 đơn rớt / 2.159 đơn) ➔ Tỉnh giữ kỷ luật luân chuyển tốt nhất vùng.",
            "➔ TOÀN VÙNG: Tỷ lệ rớt W38 là 3,32% (tổng 252 đơn rớt / 7.586 đơn cần LC, tăng +1,52%p so với W37 1,80%)."
        ],'''

new_sec9 = '''        province_block=[
            "• Đắk Nông: Tỷ lệ rớt 20,73% (57 đơn rớt / 275 đơn cần luân chuyển) ➔ Tỷ lệ rớt kỷ lục, gấp 6 lần bình quân toàn vùng!",
            "• Khánh Hòa: Tỷ lệ rớt 5,09% (102 đơn rớt / 2.005 đơn cần luân chuyển) ➔ Tỉnh có số lượng đơn rớt tuyệt đối lớn nhất vùng.",
            "• Lâm Đồng: Tỷ lệ rớt 3,32% (58 đơn rớt / 1.748 đơn cần luân chuyển).",
            "• Ninh Thuận: Tỷ lệ rớt 1,14% (16 đơn rớt / 1.399 đơn cần luân chuyển, cải thiện -1,89%p WoW).",
            "• Bình Thuận: Tỷ lệ rớt 0,88% (19 đơn rớt / 2.159 đơn cần luân chuyển) ➔ Tỉnh kiểm soát luân chuyển xuất sắc nhất vùng (<1%).",
            "➔ TOÀN VÙNG W38: Tỷ lệ rớt luân chuyển đạt 3,32% (252 đơn rớt / 7.586 đơn cần LC, tăng +1,52%p WoW so với W37: 1,80%)."
        ],'''

if old_sec9 in code:
    code = code.replace(old_sec9, new_sec9)
    print("Replaced Section 9 Rot LC province block")

# Also check Section 3 am_analysis_block speech to make sure speech reflects Binh Thuan & Ninh Thuan leading!
old_speech_sec3 = '''            "Lâm Đồng có sản lượng lớn nhưng %GTC chỉ đạt 53,8%, lỗi tập trung ở các AM phụ trách địa bàn huyện đồi dốc."'''
new_speech_sec3 = '''            "Bình Thuận (69,2%) và Ninh Thuận (65,7%) tiếp tục là 2 điểm tựa vững chắc nhất vùng về tỷ lệ giao thành công; trong khi Lâm Đồng (48,0%) và Đắk Nông (46,8%) rơi xuống dưới 50%, đang kéo lùi toàn bộ thành quả của vùng."'''
if old_speech_sec3 in code:
    code = code.replace(old_speech_sec3, new_speech_sec3)

with open('scratch/build_w38_redesigned_final.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated scratch/build_w38_redesigned_final.py successfully!")
