import re

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Executive Callout Banner
old_exec = """            <h3>TỔNG HỢP TRỌNG TÂM HỌP TUẦN W37 — VÙNG NAM TRUNG BỘ</h3>
            <p>
              • <strong>Sản lượng Giao Full Hàng:</strong> Đạt <strong>307,837 đơn</strong> (Tuần W36 kết thúc 06/09/2026, giảm -11,149 đơn / -3.5% WoW so với W35).<br>
              • <strong>Sản lượng TikTok Shop (TTS):</strong> Đạt <strong>63,122 đơn</strong> (giảm <strong>-9,759 đơn / -13.4% WoW</strong> so với W35), chiếm 20.5% tổng sản lượng toàn vùng.<br>
              • <strong>Chất lượng vận hành:</strong> %ODR toàn vùng đạt <strong>92.9%</strong> (tăng <strong>+0.7% WoW</strong> so với W35, giữ vững chuẩn ≥92%), %LTC đạt <strong>90.5%</strong>. Tỷ lệ Rớt LC tăng lên <strong>2.3%</strong> (tăng <strong>+0.7% WoW</strong> so với W35 1.57%, cần kiểm soát). Tỷ lệ %FD Hoàn Trả <strong>7.5%</strong>, %TLTĐ Lấp Đầy Thùng Xe <strong>48.1%</strong>.<br>
              • <strong>Điểm nổi bật:</strong> AM Nguyễn Thanh Long bứt phá %GTC mạnh nhất vùng (+10.2% WoW). Tỉnh Đắk Nông cần tập trung nâng cao %ODR (89.1%).
            </p>"""

new_exec = """            <h3>TỔNG HỢP TRỌNG TÂM HỌP TUẦN W37 — VÙNG NAM TRUNG BỘ</h3>
            <p>
              • <strong>Sản lượng Giao Full Hàng:</strong> Đạt <strong>357,249 đơn</strong> (Tuần W37 kết thúc 13/09/2026, tăng <strong>+49,412 đơn / +16.1% WoW</strong> so với W36).<br>
              • <strong>Sản lượng TikTok Shop (TTS):</strong> Đạt <strong>68,719 đơn</strong> (tăng <strong>+5,597 đơn / +8.9% WoW</strong> so với W36), chiếm 19.2% tổng sản lượng toàn vùng.<br>
              • <strong>Chất lượng vận hành:</strong> %ODR toàn vùng đạt <strong>93.3%</strong> (tăng <strong>+0.5% WoW</strong> so với W36, đạt chuẩn ≥92%), %LTC đạt <strong>90.3%</strong>. Tỷ lệ Rớt LC giảm mạnh xuống <strong>1.80%</strong> (giảm <strong>-0.45% WoW</strong> so với 2.25% W36). Tỷ lệ %FD Hoàn Trả <strong>6.73%</strong>, %TLTĐ Lấp Đầy Xe KTC <strong>54.8%</strong> (+6.7% WoW).<br>
              • <strong>Điểm nổi bật:</strong> AM Huỳnh Thúc Duân bứt phá %GTC mạnh nhất vùng (+6.4% WoW). AM Nguyễn Thanh Long cần rà soát %GTC (-10.3% WoW). Tỉnh Lâm Đồng có %ODR thấp nhất (90.2%).
            </p>"""

if old_exec in c:
    c = c.replace(old_exec, new_exec)
    print("Replaced Executive Callout Banner!")
else:
    print("old_exec not found exactly, searching via regex...")
    pattern = r'<h3>TỔNG HỢP TRỌNG TÂM HỌP TUẦN W3[67][^<]*</h3>\s*<p>[\s\S]*?</p>'
    c = re.sub(pattern, new_exec, c)
    print("Replaced via regex!")

# 2. San luong banner
old_sl = """• <strong>Sản lượng Toàn Mạng (W36):</strong> Full hàng đạt <strong>307.837 đơn</strong> (giảm <strong>-11.149 đơn / -3,5% WoW</strong> so với W35). Phân khúc TikTok Shop (TTS) đạt <strong>63.122 đơn</strong> (giảm <strong>-9.759 đơn / -13,4% WoW</strong>), chiếm tỷ trọng <strong>20,5%</strong> tổng sản lượng vùng.<br>
              • <strong>Theo 5 Tỉnh:</strong> Cả 5 tỉnh đều ghi nhận biến động tuần W36 — Bình Thuận (97.7k đơn), Lâm Đồng (82.7k đơn), Khánh Hòa (70.2k đơn), Ninh Thuận (36.1k đơn), Đắk Nông (21.1k đơn).<br>
              • <strong>Biến động AM:</strong> AM Nguyễn Lê Nguyên Vũ dẫn đầu tăng trưởng đơn (+347 đơn Full), tiếp sau là Hồng Bích Nga (+201 đơn Full)."""

new_sl = """• <strong>Sản lượng Toàn Mạng (W37):</strong> Full hàng đạt <strong>357,249 đơn</strong> (tăng <strong>+49,412 đơn / +16.1% WoW</strong> so với W36). Phân khúc TikTok Shop (TTS) đạt <strong>68,719 đơn</strong> (tăng <strong>+5,597 đơn / +8.9% WoW</strong>), chiếm tỷ trọng <strong>19.2%</strong> tổng sản lượng vùng.<br>
              • <strong>Theo 5 Tỉnh:</strong> Cả 5 tỉnh đều tăng trưởng sản lượng tuần W37 — Bình Thuận (107.5k đơn), Khánh Hòa (89.1k đơn), Lâm Đồng (92.5k đơn), Ninh Thuận (42.4k đơn), Đắk Nông (25.7k đơn).<br>
              • <strong>Biến động AM:</strong> AM Thái Thị Thanh Thư dẫn đầu tăng trưởng (+6,990 đơn Full), tiếp theo là Nguyễn Duy Long (+6,938 đơn), Lê Văn Trường (+5,814 đơn)."""

if old_sl in c:
    c = c.replace(old_sl, new_sl)
    print("Replaced San Luong Banner!")
else:
    c = re.sub(r'• <strong>Sản lượng Toàn Mạng \(W3[67]\):</strong>[\s\S]*?• <strong>Biến động AM:</strong>[^<]*', new_sl, c)
    print("Replaced San Luong Banner via regex!")

c = c.replace("Full: 307.8k đơn | TTS: 63.1k đơn", "Full: 357.2k đơn | TTS: 68.7k đơn")
c = c.replace("Full: ▼ -11,149 đ (-3.5%) | TTS: ▼ -9,759 đ (-13.4%)", "Full: ▲ +49,412 đ (+16.1%) | TTS: ▲ +5,597 đ (+8.9%)")

# 3. Rot LC banner
old_rot = "• <strong>Tổng đơn rớt toàn vùng W36:</strong> Đạt <strong>196 đơn rớt</strong> / 8.705 đơn cần LC (Tỷ lệ rớt: <strong>2.25%</strong>, tăng <strong>+0.68% WoW</strong> so với 1.57% W35, vượt trần an toàn ≤1.0%)."
new_rot = "• <strong>Tổng đơn rớt toàn vùng W37:</strong> Tỷ lệ rớt đạt <strong>1.80%</strong> (giảm <strong>-0.45% WoW</strong> so với 2.25% W36, xu hướng cải thiện tích cực)."
c = c.replace(old_rot, new_rot)
c = c.replace("<h3>PHÂN TÍCH TỶ TRỌNG RỚT ĐƠN LUÂN CHUYỂN THEO AM & TỈNH THÀNH (W36)</h3>", "<h3>PHÂN TÍCH TỶ TRỌNG RỚT ĐƠN LUÂN CHUYỂN THEO AM & TỈNH THÀNH (W37)</h3>")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("index.html updated successfully!")
