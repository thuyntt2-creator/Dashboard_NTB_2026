import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace static thead headers for each table

replacements = [
    # 1. table-vol-tinh-full (Screenshot 1)
    (
        r'(<table class="bi-table" id="table-vol-tinh-full">[\s\S]*?<thead>[\s\S]*?)<th>W34</th>\s*<th>W35</th>\s*<th>W36</th>\s*<th>W37</th>',
        r'\1<th>W35</th>\n                  <th>W36</th>\n                  <th>W37</th>\n                  <th>W38</th>'
    ),
    # 2. table-vol-tinh-tts (Screenshot 1)
    (
        r'(<table class="bi-table" id="table-vol-tinh-tts">[\s\S]*?<thead>[\s\S]*?)<th>W34</th>\s*<th>W35</th>\s*<th>W36</th>\s*<th>W37</th>',
        r'\1<th>W35</th>\n                  <th>W36</th>\n                  <th>W37</th>\n                  <th>W38</th>'
    ),
    # 3. table-gtc-tinh-full (Screenshot 2)
    (
        r'(<table class="bi-table" id="table-gtc-tinh-full">[\s\S]*?<thead>[\s\S]*?)<th>W34</th>\s*<th>W35</th>\s*<th>W36</th>\s*<th[^>]*>%GTC W37</th>',
        r'\1<th>W35</th>\n                  <th>W36</th>\n                  <th>W37</th>\n                  <th class="num" style="background: var(--color-blue-bg); font-weight:800; font-size:13.5px;">%GTC W38</th>'
    ),
    # 4. table-gtc-tinh-tts (Screenshot 2)
    (
        r'(<table class="bi-table" id="table-gtc-tinh-tts">[\s\S]*?<thead>[\s\S]*?)<th>W34</th>\s*<th>W35</th>\s*<th>W36</th>\s*<th[^>]*>%GTC W37</th>',
        r'\1<th>W35</th>\n                  <th>W36</th>\n                  <th>W37</th>\n                  <th class="num" style="background: var(--color-amber-bg); color:#ea580c; font-weight:800; font-size:13.5px;">%GTC W38</th>'
    ),
    # 5. table-gtc-tts-ca1-detailed (Screenshot 3)
    (
        r'(<table class="bi-table" id="table-gtc-tts-ca1-detailed">[\s\S]*?<thead>[\s\S]*?)<th>%GTC TTS Ca 1 \(W36\)</th>\s*<th[^>]*>%GTC TTS Ca 1 \(W37\)</th>',
        r'\1<th>%GTC TTS Ca 1 (W37)</th>\n                  <th class="num" style="background: var(--color-amber-bg); color:#ea580c; font-weight:800;">%GTC TTS Ca 1 (W38)</th>'
    ),
    # 6. table-gan-overview-region (Screenshot 4)
    (
        r'(<table class="bi-table" id="table-gan-overview-region">[\s\S]*?<thead>[\s\S]*?)<th>W34</th>\s*<th>W35</th>\s*<th>W36</th>\s*<th>W37</th>\s*<th>Δ W37/W36</th>',
        r'\1<th>W35</th>\n                  <th>W36</th>\n                  <th>W37</th>\n                  <th>W38</th>\n                  <th>Δ W38/W37</th>'
    ),
    # 7. table-odr-tinh-full (Screenshot 5)
    (
        r'(<table class="bi-table" id="table-odr-tinh-full">[\s\S]*?<thead>[\s\S]*?)<th>W34</th>\s*<th>W35</th>\s*<th>W36</th>\s*<th[^>]*>%ODR W37</th>',
        r'\1<th>W35</th>\n                  <th>W36</th>\n                  <th>W37</th>\n                  <th class="num" style="background: var(--color-blue-bg); font-weight:800; font-size:13.5px;">%ODR W38</th>'
    ),
    # 8. table-odr-tinh-tts (Screenshot 5)
    (
        r'(<table class="bi-table" id="table-odr-tinh-tts">[\s\S]*?<thead>[\s\S]*?)<th>W34</th>\s*<th>W35</th>\s*<th>W36</th>\s*<th[^>]*>%ODR W37</th>',
        r'\1<th>W35</th>\n                  <th>W36</th>\n                  <th>W37</th>\n                  <th class="num" style="background: var(--color-amber-bg); color:#ea580c; font-weight:800; font-size:13.5px;">%ODR W38</th>'
    ),
    # 9. table-overview-kpi-data
    (
        r'(<table class="bi-table" id="table-overview-kpi-data">[\s\S]*?<thead>[\s\S]*?)<th>W34</th>\s*<th>W35</th>\s*<th>W36</th>\s*<th[^>]*>W37 \(Kỳ N\)</th>',
        r'\1<th>W35</th>\n                  <th>W36</th>\n                  <th>W37</th>\n                  <th class="num" style="background: var(--color-blue-bg); font-weight:800; color: var(--color-primary);">W38 (Kỳ N)</th>'
    ),
    # 10. table-ltc-detailed & table-ltc-tinh-detailed
    (
        r'(<table class="bi-table" id="table-ltc-detailed">[\s\S]*?<thead>[\s\S]*?)<th>W34</th>\s*<th>W35</th>\s*<th>W36</th>\s*<th[^>]*>%LTC W37</th>',
        r'\1<th>W35</th>\n                  <th>W36</th>\n                  <th>W37</th>\n                  <th class="num" style="background: var(--color-blue-bg); font-weight:800;">%LTC W38</th>'
    ),
    (
        r'(<table class="bi-table" id="table-ltc-tinh-detailed">[\s\S]*?<thead>[\s\S]*?)<th>W34</th>\s*<th>W35</th>\s*<th>W36</th>\s*<th[^>]*>%LTC W37</th>',
        r'\1<th>W35</th>\n                  <th>W36</th>\n                  <th>W37</th>\n                  <th class="num" style="background: var(--color-blue-bg); font-weight:800;">%LTC W38</th>'
    ),
    # 11. table-rot-am-detailed & table-rot-tinh-detailed (Tab 9)
    (
        r'(<table class="bi-table" id="table-rot-am-detailed">[\s\S]*?<thead>[\s\S]*?)<th>% Rớt W36</th>\s*<th[^>]*>% Rớt W37</th>',
        r'\1<th>% Rớt W37</th>\n                  <th class="num" style="background: var(--color-red-bg); font-weight:800; color:#b91c1c;">% Rớt W38</th>'
    ),
    (
        r'(<table class="bi-table" id="table-rot-tinh-detailed">[\s\S]*?<thead>[\s\S]*?)<th>% Rớt W36</th>\s*<th[^>]*>% Rớt W37</th>',
        r'\1<th>% Rớt W37</th>\n                  <th class="num" style="background: var(--color-red-bg); font-weight:800; color:#b91c1c;">% Rớt W38</th>'
    ),
    # 12. table-rot-lc-top-bc
    (
        r'(<table class="bi-table" id="table-rot-lc-top-bc">[\s\S]*?<thead>[\s\S]*?<th[^>]*>)% Rớt LC \(W37\)(</th>)',
        r'\1% Rớt LC (W38)\2'
    ),
    # 13. table-vol-full-detailed & table-vol-tts-detailed
    (
        r'(<table class="bi-table" id="table-vol-full-detailed">[\s\S]*?<thead>[\s\S]*?)<th>Full W36</th>\s*<th[^>]*>Full W37</th>',
        r'\1<th>Full W37</th>\n                  <th class="num" style="background: var(--color-blue-bg); font-weight:800; font-size:13.5px;">Full W38</th>'
    ),
    (
        r'(<table class="bi-table" id="table-vol-tts-detailed">[\s\S]*?<thead>[\s\S]*?)<th>TTS W36</th>\s*<th[^>]*>TTS W37</th>',
        r'\1<th>TTS W37</th>\n                  <th class="num" style="background: var(--color-amber-bg); color:#ea580c; font-weight:800; font-size:13.5px;">TTS W38</th>'
    ),
    # 14. table-gtc-full-detailed & table-gtc-tts-detailed
    (
        r'(<table class="bi-table" id="table-gtc-full-detailed">[\s\S]*?<thead>[\s\S]*?)<th>W36</th>\s*<th[^>]*>W37</th>',
        r'\1<th>W37</th>\n                  <th class="num" style="background: var(--color-blue-bg); font-weight:800; font-size:13.5px;">W38</th>'
    ),
    (
        r'(<table class="bi-table" id="table-gtc-tts-detailed">[\s\S]*?<thead>[\s\S]*?)<th>TTS W36</th>\s*<th[^>]*>TTS W37</th>',
        r'\1<th>TTS W37</th>\n                  <th class="num" style="background: var(--color-amber-bg); color:#ea580c; font-weight:800; font-size:13.5px;">TTS W38</th>'
    ),
    # 15. table-odr-full-detailed & table-odr-tts-detailed
    (
        r'(<table class="bi-table" id="table-odr-full-detailed">[\s\S]*?<thead>[\s\S]*?)<th>W36</th>\s*<th[^>]*>W37</th>',
        r'\1<th>W37</th>\n                  <th class="num" style="background: var(--color-blue-bg); font-weight:800; font-size:13.5px;">W38</th>'
    ),
    (
        r'(<table class="bi-table" id="table-odr-tts-detailed">[\s\S]*?<thead>[\s\S]*?)<th>TTS W36</th>\s*<th[^>]*>TTS W37</th>',
        r'\1<th>TTS W37</th>\n                  <th class="num" style="background: var(--color-amber-bg); color:#ea580c; font-weight:800; font-size:13.5px;">TTS W38</th>'
    ),
    # 16. table-gan-ca1-detailed & table-gan-ca2-detailed
    (
        r'(<table class="bi-table" id="table-gan-ca1-detailed">[\s\S]*?<thead>[\s\S]*?)<th>Ca 1\+Tồn W36</th>\s*<th[^>]*>Ca 1\+Tồn W37</th>',
        r'\1<th>Ca 1+Tồn W37</th>\n                  <th class="num" style="background: var(--color-blue-bg); font-weight:800;">Ca 1+Tồn W38</th>'
    ),
    (
        r'(<table class="bi-table" id="table-gan-ca2-detailed">[\s\S]*?<thead>[\s\S]*?)<th>Tổng W36</th>\s*<th[^>]*>Gán Tổng W37</th>',
        r'\1<th>Tổng W37</th>\n                  <th class="num" style="background: var(--color-blue-bg); font-weight:800;">Gán Tổng W38</th>'
    ),
    # 17. table-opr-day-detailed & table-opr-night-detailed & table-opr-tts-data
    (
        r'(<table class="bi-table" id="table-opr-day-detailed">[\s\S]*?<thead>[\s\S]*?)<th>W36</th>\s*<th[^>]*>%OPR W37</th>',
        r'\1<th>W37</th>\n                  <th class="num" style="background: var(--color-amber-bg); font-weight:800; color:#ea580c;">%OPR W38</th>'
    ),
    (
        r'(<table class="bi-table" id="table-opr-night-detailed">[\s\S]*?<thead>[\s\S]*?)<th>W36</th>\s*<th[^>]*>%OPR W37</th>',
        r'\1<th>W37</th>\n                  <th class="num" style="background: var(--color-amber-bg); font-weight:800; color:#ea580c;">%OPR W38</th>'
    ),
    (
        r'(<table class="bi-table" id="table-opr-tts-data">[\s\S]*?<thead>[\s\S]*?)%OPR 9h–19h \(W36\)([\s\S]*?)%OPR 9h–19h \(W37\)([\s\S]*?)%OPR 19h–9h \(W36\)([\s\S]*?)%OPR 19h–9h \(W37\)',
        r'\1%OPR 9h–19h (W37)\2%OPR 9h–19h (W38)\3%OPR 19h–9h (W37)\4%OPR 19h–9h (W38)'
    ),
    # 18. table-fd-am-detailed
    (
        r'(<table class="bi-table" id="table-fd-am-detailed">[\s\S]*?<thead>[\s\S]*?)<th>Full W36</th>\s*<th>Full W37</th>([\s\S]*?)<th>TTS W36</th>\s*<th>TTS W37</th>',
        r'\1<th>Full W37</th>\n                  <th>Full W38</th>\2<th>TTS W37</th>\n                  <th>TTS W38</th>'
    ),
    # 19. table-kd-churn-top10
    (
        r'(<table class="bi-table" id="table-kd-churn-top10">[\s\S]*?<thead>[\s\S]*?)<th>Kỳ Trước \(W36\)</th>\s*<th>Kỳ Này \(W37\)</th>',
        r'\1<th>Kỳ Trước (W37)</th>\n                  <th>Kỳ Này (W38)</th>'
    ),
    # 20. table-bc-canh-bao-overview & table-bc-canh-bao & table-bc-canhbao-tab
    (
        r'<th>%GTC W36</th>\s*<th>%GTC W37</th>',
        r'<th>%GTC W37</th>\n                  <th>%GTC W38</th>'
    )
]

for pattern, repl in replacements:
    new_html = re.sub(pattern, repl, html)
    if new_html != html:
        html = new_html
        print(f"Applied replacement: {pattern[:60]}...")
    else:
        print(f"No match for: {pattern[:60]}...")

# 21. Titles and banners
html = html.replace(
    'TỔNG QUAN VÙNG NTB — TỶ LỆ % GÁN (4 TUẦN W34 – W37)',
    'TỔNG QUAN VÙNG NTB — TỶ LỆ % GÁN (4 TUẦN W35 – W38)'
)

html = html.replace(
    'PHÂN TÍCH TỶ TRỌNG RỚT ĐƠN LUÂN CHUYỂN THEO AM & TỈNH THÀNH (W37)',
    'PHÂN TÍCH TỶ TRỌNG RỚT ĐƠN LUÂN CHUYỂN THEO AM & TỈNH THÀNH (W38)'
)

html = html.replace(
    'Tổng đơn rớt toàn vùng W37: Tỷ lệ rớt đạt 1.80% (giảm -0.45%p WoW',
    'Tổng đơn rớt toàn vùng W38: Tỷ lệ rớt đạt 3.32% (tăng +1.52%p WoW so với 1.80% ở W37, tổng 252 đơn rớt / 7,586 đơn cần LC'
)

html = html.replace(
    'Tổng rớt: 196 đơn',
    'Tổng rớt: 252 đơn'
)

html = html.replace(
    '% RỚT LUÂN CHUYỂN THEO 18 AM PHỤ TRÁCH (W37)',
    '% RỚT LUÂN CHUYỂN THEO 18 AM PHỤ TRÁCH (W38)'
)

html = html.replace(
    'DANH SÁCH TOP 20 BƯU CỤC CÓ TỶ LỆ RỚT LUÂN CHUYỂN CAO NHẤT (W37)',
    'DANH SÁCH TOP 20 BƯU CỤC CÓ TỶ LỆ RỚT LUÂN CHUYỂN CAO NHẤT (W38)'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("SUCCESS: index.html updated with W38 headers!")
