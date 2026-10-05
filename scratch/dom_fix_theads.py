import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# 1. table-vol-tinh-full
tbl = soup.find('table', id='table-vol-tinh-full')
if tbl and tbl.find('thead'):
    tbl.find('thead').clear()
    thead_html = """<tr>
                    <th class="center" style="width: 44px;">#</th>
                    <th>Tỉnh Thành</th>
                    <th class="num">W37</th>
                    <th class="num">W38</th>
                    <th class="num">W39</th>
                    <th class="num" style="background: var(--color-amber-bg); font-weight: 800; color: #ea580c;">W40</th>
                    <th class="num">Biến Động (Δ Đơn)</th>
                    <th class="center">Đánh Giá</th>
                  </tr>"""
    tbl.find('thead').append(BeautifulSoup(thead_html, 'html.parser'))

# 2. table-vol-tinh-tts
tbl = soup.find('table', id='table-vol-tinh-tts')
if tbl and tbl.find('thead'):
    tbl.find('thead').clear()
    thead_html = """<tr>
                    <th class="center" style="width: 44px;">#</th>
                    <th>Tỉnh Thành</th>
                    <th class="num">W37</th>
                    <th class="num">W38</th>
                    <th class="num">W39</th>
                    <th class="num" style="background: var(--color-amber-bg); font-weight: 800; color: #ea580c;">W40</th>
                    <th class="num">Biến Động (Δ Đơn)</th>
                    <th class="num" title="Tỷ trọng sản lượng TTS đóng góp trong toàn vùng (Tổng = 100%)">% Tỷ Trọng</th>
                    <th class="center">Đánh Giá</th>
                  </tr>"""
    tbl.find('thead').append(BeautifulSoup(thead_html, 'html.parser'))

# 3. table-bc-canh-bao-overview
tbl = soup.find('table', id='table-bc-canh-bao-overview')
if tbl and tbl.find('thead'):
    tbl.find('thead').clear()
    thead_html = """<tr style="background: #1e3a8a; color: #ffffff;">
                    <th class="center" style="width: 44px; color: #ffffff;">#</th>
                    <th style="color: #ffffff;">Bưu Cục Điểm Nóng</th>
                    <th style="color: #ffffff;">Tỉnh / TP</th>
                    <th style="color: #ffffff;">AM Phụ Trách</th>
                    <th class="num" style="background: #0284c7; color: #ffffff; font-weight: 700;">%GTC W39</th>
                    <th class="num" style="background: #dc2626; color: #ffffff; font-weight: 800;">%GTC W40</th>
                    <th class="num" style="background: #ea580c; color: #ffffff; font-weight: 700;">Biến Động WoW (Δ)</th>
                    <th class="num" style="background: #475569; color: #ffffff;">Mốc Tốt Nhất</th>
                    <th class="center" style="background: #d97706; color: #ffffff; font-weight: 800;">Số Ngày Cảnh Báo (3T)</th>
                    <th class="num" style="background: #334155; color: #ffffff;">Backlog Tồn</th>
                    <th class="num" style="background: #991b1b; color: #ffffff;">Tồn &gt; 5 Ngày</th>
                    <th class="center" style="background: #0d9488; color: #ffffff;">Dự Kiến Clear</th>
                    <th class="center" style="color: #ffffff;">Tiêu Chí Cảnh Báo</th>
                  </tr>"""
    tbl.find('thead').append(BeautifulSoup(thead_html, 'html.parser'))

# 4. table-bc-canh-bao (under Tab 3)
tbl = soup.find('table', id='table-bc-canh-bao')
if tbl and tbl.find('thead'):
    tbl.find('thead').clear()
    thead_html = """<tr style="background: #1e3a8a; color: #ffffff;">
                    <th class="center" style="width: 44px; color: #ffffff;">#</th>
                    <th style="color: #ffffff;">Bưu Cục Điểm Nóng</th>
                    <th style="color: #ffffff;">Tỉnh / TP</th>
                    <th style="color: #ffffff;">AM Phụ Trách</th>
                    <th class="num" style="background: #0284c7; color: #ffffff; font-weight: 700;">%GTC W39</th>
                    <th class="num" style="background: #dc2626; color: #ffffff; font-weight: 800;">%GTC W40</th>
                    <th class="num" style="background: #ea580c; color: #ffffff; font-weight: 700;">Biến Động WoW (Δ)</th>
                    <th class="num" style="background: #475569; color: #ffffff;">Mốc Tốt Nhất</th>
                    <th class="center" style="background: #d97706; color: #ffffff; font-weight: 800;">Số Ngày Cảnh Báo (3T)</th>
                    <th class="num" style="background: #334155; color: #ffffff;">Backlog Tồn</th>
                    <th class="num" style="background: #991b1b; color: #ffffff;">Tồn &gt; 5 Ngày</th>
                    <th class="center" style="background: #0d9488; color: #ffffff;">Dự Kiến Clear</th>
                    <th class="center" style="color: #ffffff;">Tiêu Chí Cảnh Báo</th>
                  </tr>"""
    tbl.find('thead').append(BeautifulSoup(thead_html, 'html.parser'))

# 5. table-bc-canhbao-tab (Tab 16)
tbl = soup.find('table', id='table-bc-canhbao-tab')
if tbl and tbl.find('thead'):
    tbl.find('thead').clear()
    thead_html = """<tr style="background: #1e3a8a; color: #ffffff;">
                    <th class="center" style="width: 44px; color: #ffffff;">#</th>
                    <th style="color: #ffffff;">Bưu Cục Điểm Nóng</th>
                    <th style="color: #ffffff;">Tỉnh / TP</th>
                    <th style="color: #ffffff;">AM Phụ Trách</th>
                    <th class="num" style="background: #0284c7; color: #ffffff; font-weight: 700;">%GTC W39</th>
                    <th class="num" style="background: #dc2626; color: #ffffff; font-weight: 800;">%GTC W40</th>
                    <th class="num" style="background: #ea580c; color: #ffffff; font-weight: 700;">Biến Động WoW (Δ)</th>
                    <th class="num" style="background: #475569; color: #ffffff;">Mốc Tốt Nhất</th>
                    <th class="center" style="background: #d97706; color: #ffffff; font-weight: 800;">Số Ngày Cảnh Báo (3T)</th>
                    <th class="num" style="background: #334155; color: #ffffff;">Backlog Tồn</th>
                    <th class="num" style="background: #991b1b; color: #ffffff;">Tồn &gt; 5 Ngày</th>
                    <th class="center" style="background: #0d9488; color: #ffffff;">Dự Kiến Clear</th>
                    <th class="center" style="color: #ffffff;">Tiêu Chí Cảnh Báo</th>
                  </tr>"""
    tbl.find('thead').append(BeautifulSoup(thead_html, 'html.parser'))

# 6. table-gan-overview-region
tbl = soup.find('table', id='table-gan-overview-region')
if tbl and tbl.find('thead'):
    tbl.find('thead').clear()
    thead_html = """<tr style="background: #1e3a8a; color: #ffffff;">
                    <th style="color: #ffffff;">Chỉ tiêu</th>
                    <th class="num" style="color: #ffffff;">W37</th>
                    <th class="num" style="color: #ffffff;">W38</th>
                    <th class="num" style="color: #ffffff;">W39</th>
                    <th class="num" style="color: #ffffff; background: rgba(255,255,255,0.2); font-weight:800;">W40</th>
                    <th class="num" style="color: #ffffff;">Δ W40/W39</th>
                  </tr>"""
    tbl.find('thead').append(BeautifulSoup(thead_html, 'html.parser'))

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(str(soup))

print("DOM-based thead replacement done successfully!")
