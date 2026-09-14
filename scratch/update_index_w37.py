import os
import re
import time

index_path = 'index.html'
with open(index_path, 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Cache busters
ts = int(time.time())
c = re.sub(r'<script src="data\.js(\?[^"]*)?"></script>', f'<script src="data.js?v={ts}"></script>', c)
c = re.sub(r'<script src="app\.js(\?[^"]*)?"></script>', f'<script src="app.js?v={ts}"></script>', c)

# 2. filter-week
c = re.sub(
    r'<select id="filter-week"[^>]*>[\s\S]*?</select>',
    '''<select id="filter-week" class="bi-select" title="Chọn tuần báo cáo">
            <option value="W37" selected>Tuần W37 (Hiện tại)</option>
            <option value="W36">Tuần W36 (Tuần trước)</option>
            <option value="W35">Tuần W35</option>
            <option value="W34">Tuần W34</option>
          </select>''',
    c
)

# 3. Titles & headings
replacements = [
    ("HỌP TUẦN W36", "HỌP TUẦN W37"),
    ("W33 – W36", "W34 – W37"),
    ("W33 ➔ W36", "W34 ➔ W37"),
    ("T30 → T36", "T31 → T37"),
    ("T30 ➔ T36", "T31 ➔ T37"),
    ("Full Hàng vs TTS — W36", "Full Hàng vs TTS — W37"),
    ("ĐÁNH GIÁ W36", "ĐÁNH GIÁ W37"),
    ("CỘT W35 vs W36", "CỘT W36 vs W37"),
    ("W35 vs W36", "W36 vs W37"),
    ("Full W35", "Full W36"),
    ("Full W36", "Full W37"),
    ("TTS W35", "TTS W36"),
    ("TTS W36", "TTS W37"),
    ("Tổng W35", "Tổng W36"),
    ("Ca 1+Tồn W36", "Ca 1+Tồn W37"),
    ("Gán Tổng (W36)", "Gán Tổng (W37)"),
    ("%GTC W36", "%GTC W37"),
    ("%ODR W36", "%ODR W37"),
    ("%LTC W36", "%LTC W37"),
    ("%OPR W36", "%OPR W37"),
    ("%OPR 9h–19h (W35)", "%OPR 9h–19h (W36)"),
    ("%OPR 9h–19h (W36)", "%OPR 9h–19h (W37)"),
    ("%OPR 19h–9h (W35)", "%OPR 19h–9h (W36)"),
    ("%OPR 19h–9h (W36)", "%OPR 19h–9h (W37)"),
    ("% Rớt W35", "% Rớt W36"),
    ("% Rớt W36", "% Rớt W37"),
    ("% Rớt LC (W36)", "% Rớt LC (W37)"),
    ("Cao Nhất (W36)", "Cao Nhất (W37)"),
    ("TRỤC NAM TRUNG BỘ (W36)", "TRỤC NAM TRUNG BỘ (W37)"),
    ("VÙNG NAM TRUNG BỘ (W36)", "VÙNG NAM TRUNG BỘ (W37)"),
    ("đơn W36", "đơn W37"),
    ("TLLĐ Xe Bình Quân (W36)", "TLLĐ Xe Bình Quân (W37)"),
    ("Tuần W36 (Lũy Kế 7 Ngày)", "Tuần W37 (Lũy Kế 7 Ngày)"),
    ("Toàn Vùng W36 (30/8–5/9)", "Toàn Vùng W37 (6–12/9)"),
    ("Tổng Doanh Thu Kỳ Này (W36)", "Tổng Doanh Thu Kỳ Này (W37)"),
    ("Kỳ 23–29/8 (W35) vs Kỳ 30/8–5/9 (W36)", "Kỳ 30/8–5/9 (W36) vs Kỳ 6–12/9 (W37)"),
]

for old_str, new_str in replacements:
    c = c.replace(old_str, new_str)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(c)

print("Successfully updated index.html with all W37 headings, table column headers, filter options and cache busters!")
