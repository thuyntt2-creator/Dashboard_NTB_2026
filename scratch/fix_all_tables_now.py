import re
import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

# 1. Update index.html using BeautifulSoup or string replacement for precise theads
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace table-overview-kpi-data thead
old_ov_thead = """              <thead>
                <tr>
                  <th style="min-width: 220px;">Chỉ Số Vận Hành</th>
                  <th class="center" style="width: 120px;">Phạm Vi</th>
                  <th class="num">W35</th>
                  <th class="num">W36</th>
                  <th class="num">W37</th>
                  <th class="num" style="background: var(--color-blue-bg); color: var(--color-blue-dark); font-weight: 800;">W38 (Kỳ N)</th>
                  <th class="num">Biến Động (Δ WoW)</th>
                  <th class="center" style="width: 130px;">Xu Hướng (Trend)</th>
                </tr>
              </thead>"""

new_ov_thead = """              <thead>
                <tr>
                  <th style="min-width: 220px;">Chỉ Số Vận Hành</th>
                  <th class="center" style="width: 120px;">Phạm Vi</th>
                  <th class="num">W37</th>
                  <th class="num">W38</th>
                  <th class="num">W39</th>
                  <th class="num" style="background: var(--color-blue-bg); color: var(--color-blue-dark); font-weight: 800;">W40 (Kỳ N)</th>
                  <th class="num">Biến Động (Δ WoW)</th>
                  <th class="center" style="width: 130px;">Xu Hướng (Trend)</th>
                </tr>
              </thead>"""

html = html.replace(old_ov_thead, new_ov_thead)

# Replace table-vol-tinh-full thead
old_vol_full_thead = """                <thead>
                  <tr>
                    <th class="center" style="width: 44px;">#</th>
                    <th>Tỉnh Thành</th>
                    <th class="num">W39</th>
                    <th class="num">W40</th>
                    <th class="num">W39</th>
                    <th class="num" style="background: var(--color-amber-bg); font-weight: 800; color: #ea580c;">W40</th>
                    <th class="num">Biến Động (Δ Đơn)</th>
                    <th class="center">Đánh Giá</th>
                  </tr>
                </thead>"""

new_vol_full_thead = """                <thead>
                  <tr>
                    <th class="center" style="width: 44px;">#</th>
                    <th>Tỉnh Thành</th>
                    <th class="num">W37</th>
                    <th class="num">W38</th>
                    <th class="num">W39</th>
                    <th class="num" style="background: var(--color-amber-bg); font-weight: 800; color: #ea580c;">W40</th>
                    <th class="num">Biến Động (Δ Đơn)</th>
                    <th class="center">Đánh Giá</th>
                  </tr>
                </thead>"""

html = html.replace(old_vol_full_thead, new_vol_full_thead)

# Replace table-vol-tinh-tts thead
old_vol_tts_thead = """                <thead>
                  <tr>
                    <th class="center" style="width: 44px;">#</th>
                    <th>Tỉnh Thành</th>
                    <th class="num">W39</th>
                    <th class="num">W40</th>
                    <th class="num">W39</th>
                    <th class="num" style="background: var(--color-amber-bg); font-weight: 800; color: #ea580c;">W40</th>
                    <th class="num">Biến Động (Δ Đơn)</th>
                    <th class="center">Đánh Giá</th>
                  </tr>
                </thead>"""

new_vol_tts_thead = """                <thead>
                  <tr>
                    <th class="center" style="width: 44px;">#</th>
                    <th>Tỉnh Thành</th>
                    <th class="num">W37</th>
                    <th class="num">W38</th>
                    <th class="num">W39</th>
                    <th class="num" style="background: var(--color-amber-bg); font-weight: 800; color: #ea580c;">W40</th>
                    <th class="num">Biến Động (Δ Đơn)</th>
                    <th class="center">Đánh Giá</th>
                  </tr>
                </thead>"""

html = html.replace(old_vol_tts_thead, new_vol_tts_thead)

# Replace table-gtc-tinh-full thead
old_gtc_full_thead = """                <thead>
                  <tr>
                    <th class="center" style="width: 44px;">#</th>
                    <th>Tỉnh / Thành Phố</th>
                    <th class="num">Sản Lượng</th>
                    <th class="num">W35</th>
                    <th class="num">W36</th>
                    <th class="num">W37</th>
                    <th class="num" style="background: var(--color-blue-bg); font-weight: 800;">%GTC W40</th>
                    <th class="num">Biến Động (Δ)</th>
                    <th class="center">Đánh Giá SLA</th>
                  </tr>
                </thead>"""

new_gtc_full_thead = """                <thead>
                  <tr>
                    <th class="center" style="width: 44px;">#</th>
                    <th>Tỉnh / Thành Phố</th>
                    <th class="num">Sản Lượng</th>
                    <th class="num">W37</th>
                    <th class="num">W38</th>
                    <th class="num">W39</th>
                    <th class="num" style="background: var(--color-blue-bg); font-weight: 800;">%GTC W40</th>
                    <th class="num">Biến Động (Δ)</th>
                    <th class="center">Đánh Giá SLA</th>
                  </tr>
                </thead>"""

html = html.replace(old_gtc_full_thead, new_gtc_full_thead)

# Replace table-gtc-tinh-tts thead
old_gtc_tts_thead = """                <thead>
                  <tr>
                    <th class="center" style="width: 44px;">#</th>
                    <th>Tỉnh / Thành Phố</th>
                    <th class="num">Sản Lượng</th>
                    <th class="num">W35</th>
                    <th class="num">W36</th>
                    <th class="num">W37</th>
                    <th class="num" style="background: var(--color-amber-bg); font-weight: 800; color: #ea580c;">%GTC W40</th>
                    <th class="num">Biến Động (Δ)</th>
                    <th class="center">Đánh Giá SLA</th>
                  </tr>
                </thead>"""

new_gtc_tts_thead = """                <thead>
                  <tr>
                    <th class="center" style="width: 44px;">#</th>
                    <th>Tỉnh / Thành Phố</th>
                    <th class="num">Sản Lượng</th>
                    <th class="num">W37</th>
                    <th class="num">W38</th>
                    <th class="num">W39</th>
                    <th class="num" style="background: var(--color-amber-bg); font-weight: 800; color: #ea580c;">%GTC W40</th>
                    <th class="num">Biến Động (Δ)</th>
                    <th class="center">Đánh Giá SLA</th>
                  </tr>
                </thead>"""

html = html.replace(old_gtc_tts_thead, new_gtc_tts_thead)

# Replace table-odr-tinh-full & tts theads
html = re.sub(
    r'<table class="bi-table" id="table-odr-tinh-full">\s*<thead>.*?</thead>',
    """<table class="bi-table" id="table-odr-tinh-full">
                <thead>
                  <tr>
                    <th class="center" style="width: 44px;">#</th>
                    <th>Tỉnh / Thành Phố</th>
                    <th class="num">Sản Lượng</th>
                    <th class="num">W37</th>
                    <th class="num">W38</th>
                    <th class="num">W39</th>
                    <th class="num" style="background: var(--color-green-bg); font-weight: 800;">%ODR W40</th>
                    <th class="num">Biến Động (Δ)</th>
                    <th class="center">Đánh Giá SLA</th>
                  </tr>
                </thead>""",
    html,
    flags=re.DOTALL
)

html = re.sub(
    r'<table class="bi-table" id="table-odr-tinh-tts">\s*<thead>.*?</thead>',
    """<table class="bi-table" id="table-odr-tinh-tts">
                <thead>
                  <tr>
                    <th class="center" style="width: 44px;">#</th>
                    <th>Tỉnh / Thành Phố</th>
                    <th class="num">Sản Lượng</th>
                    <th class="num">W37</th>
                    <th class="num">W38</th>
                    <th class="num">W39</th>
                    <th class="num" style="background: var(--color-amber-bg); font-weight: 800; color: #ea580c;">%ODR W40</th>
                    <th class="num">Biến Động (Δ)</th>
                    <th class="center">Đánh Giá SLA</th>
                  </tr>
                </thead>""",
    html,
    flags=re.DOTALL
)

# Replace table-ltc-detailed & tinh
html = re.sub(
    r'<table class="bi-table" id="table-ltc-detailed">\s*<thead>.*?</thead>',
    """<table class="bi-table" id="table-ltc-detailed">
                <thead>
                  <tr>
                    <th class="center" style="width: 44px;">#</th>
                    <th>AM Phụ Trách</th>
                    <th class="num">Sản Lượng</th>
                    <th class="num">W37</th>
                    <th class="num">W38</th>
                    <th class="num">W39</th>
                    <th class="num" style="background: var(--color-blue-bg); font-weight:800;">%LTC W40</th>
                    <th class="num">Biến Động (Δ)</th>
                    <th class="center">Đánh Giá SLA</th>
                  </tr>
                </thead>""",
    html,
    flags=re.DOTALL
)

html = re.sub(
    r'<table class="bi-table" id="table-ltc-tinh-detailed">\s*<thead>.*?</thead>',
    """<table class="bi-table" id="table-ltc-tinh-detailed">
                <thead>
                  <tr>
                    <th class="center" style="width: 44px;">#</th>
                    <th>Tỉnh / Thành Phố</th>
                    <th class="num">Sản Lượng</th>
                    <th class="num">W37</th>
                    <th class="num">W38</th>
                    <th class="num">W39</th>
                    <th class="num" style="background: var(--color-blue-bg); font-weight:800;">%LTC W40</th>
                    <th class="num">Biến Động (Δ)</th>
                    <th class="center">Đánh Giá SLA</th>
                  </tr>
                </thead>""",
    html,
    flags=re.DOTALL
)

# Replace table-opr-day-detailed & night
html = re.sub(
    r'<table class="bi-table" id="table-opr-day-detailed">\s*<thead>.*?</thead>',
    """<table class="bi-table" id="table-opr-day-detailed">
                <thead>
                  <tr>
                    <th class="center" style="width: 44px;">#</th>
                    <th>AM Phụ Trách</th>
                    <th class="num">Đơn Ngày</th>
                    <th class="num">W39</th>
                    <th class="num" style="background: var(--color-blue-bg); font-weight:800;">%OPR W40</th>
                    <th class="num">Biến Động (Δ)</th>
                    <th class="center">Đánh Giá KPI</th>
                  </tr>
                </thead>""",
    html,
    flags=re.DOTALL
)

html = re.sub(
    r'<table class="bi-table" id="table-opr-night-detailed">\s*<thead>.*?</thead>',
    """<table class="bi-table" id="table-opr-night-detailed">
                <thead>
                  <tr>
                    <th class="center" style="width: 44px;">#</th>
                    <th>AM Phụ Trách</th>
                    <th class="num">Đơn Đêm</th>
                    <th class="num">W39</th>
                    <th class="num" style="background: var(--color-amber-bg); font-weight:800; color:#ea580c;">%OPR W40</th>
                    <th class="num">Biến Động (Δ)</th>
                    <th class="center">Đánh Giá SLA</th>
                  </tr>
                </thead>""",
    html,
    flags=re.DOTALL
)

# Replace table-opr-tts-data
html = re.sub(
    r'<table class="bi-table" id="table-opr-tts-data">\s*<thead>.*?</thead>',
    """<table class="bi-table" id="table-opr-tts-data">
              <thead>
                <tr>
                  <th class="center" style="width: 50px;">#</th>
                  <th>AM Phụ Trách</th>
                  <th class="num">Đơn Ngày (9h–19h)</th>
                  <th class="num">%OPR 9h–19h (W39)</th>
                  <th class="num" style="background: var(--color-blue-bg); font-weight:800;">%OPR 9h–19h (W40)</th>
                  <th class="num">Δ Ngày</th>
                  <th class="num">Đơn Đêm (19h–9h)</th>
                  <th class="num">%OPR 19h–9h (W39)</th>
                  <th class="num" style="background: var(--color-amber-bg); font-weight:800;">%OPR 19h–9h (W40)</th>
                  <th class="num">Δ Đêm</th>
                  <th class="num" style="font-weight: 800;">Tổng Đơn TTS</th>
                  <th class="num" style="background: rgba(239, 68, 68, 0.08); font-weight:800; color:#b91c1c;">Đơn Trễ OPR</th>
                  <th class="num" style="background: var(--color-amber-bg); font-weight:800; color:#ea580c;" title="Tỷ trọng đóng góp vào tổng đơn rớt/trễ OPR toàn vùng (Tổng = 100%)">% Tỷ Trọng Rớt</th>
                </tr>
              </thead>""",
    html,
    flags=re.DOTALL
)

# Replace table-truythu-by-loai
html = re.sub(
    r'<table class="bi-table" id="table-truythu-by-loai">\s*<thead>.*?</thead>',
    """<table class="bi-table" id="table-truythu-by-loai">
                  <thead>
                    <tr style="background: #1e3a8a; color: #ffffff;">
                      <th class="center" style="width: 44px; color:#ffffff;">#</th>
                      <th style="color:#ffffff;">Loại Truy Thu</th>
                      <th class="num" id="th-tt-loai-dp" style="color:#ffffff;">Đơn W39</th>
                      <th class="num" id="th-tt-loai-dc" style="background: #0284c7; color:#ffffff; font-weight:800;">Đơn W40</th>
                      <th class="num" style="color:#ffffff;">Biến Động Đơn</th>
                      <th class="num" id="th-tt-loai-cp" style="color:#ffffff;">Cần Thu W39 (Tr ₫)</th>
                      <th class="num" id="th-tt-loai-cc" style="background: #dc2626; color:#ffffff; font-weight:800;">Cần Thu W40 (Tr ₫)</th>
                      <th class="num" style="color:#ffffff;">Biến Động (Tr ₫)</th>
                      <th class="num" style="color:#ffffff;">% Biến Động</th>
                      <th class="center" style="color:#ffffff;">Đánh Giá</th>
                    </tr>
                  </thead>""",
    html,
    flags=re.DOTALL
)

# Replace table-truythu-by-province
html = re.sub(
    r'<table class="bi-table" id="table-truythu-by-province">\s*<thead>.*?</thead>',
    """<table class="bi-table" id="table-truythu-by-province">
                <thead>
                  <tr style="background: #1e3a8a; color: #ffffff;">
                    <th class="center" style="width: 44px; color:#ffffff;">#</th>
                    <th style="color:#ffffff;">Tỉnh / Thành Phố</th>
                    <th class="num" style="color:#ffffff;">Đơn Tuần W39</th>
                    <th class="num" style="background: #0284c7; color:#ffffff; font-weight:800;">Đơn Tuần W40</th>
                    <th class="num" style="color:#ffffff;">Biến Động Đơn</th>
                    <th class="num" style="color:#ffffff;">Cần Thu W39 (Tr ₫)</th>
                    <th class="num" style="background: #dc2626; color:#ffffff; font-weight:800;">Cần Thu W40 (Tr ₫)</th>
                    <th class="num" style="color:#ffffff;">Biến Động Tiền (Tr ₫)</th>
                  </tr>
                </thead>""",
    html,
    flags=re.DOTALL
)

# Replace table-truythu-top-bc-giao
html = re.sub(
    r'<table class="bi-table" id="table-truythu-top-bc-giao">\s*<thead>.*?</thead>',
    """<table class="bi-table" id="table-truythu-top-bc-giao">
                <thead>
                  <tr style="background: #1e3a8a; color: #ffffff;">
                    <th class="center" style="width: 44px; color:#ffffff;">#</th>
                    <th style="color:#ffffff;">Bưu Cục Giao</th>
                    <th style="color:#ffffff;">AM Phụ Trách</th>
                    <th style="color:#ffffff;">Tỉnh / TP</th>
                    <th class="num" style="color:#ffffff;">Đơn W39</th>
                    <th class="num" style="background: #0284c7; color:#ffffff; font-weight:800;">Đơn W40</th>
                    <th class="num" style="color:#ffffff;">Biến Động Đơn</th>
                    <th class="num" style="color:#ffffff;">Cần Thu W39 (Tr ₫)</th>
                    <th class="num" style="background: #dc2626; color:#ffffff; font-weight:900;">Cần Thu W40 (Tr ₫)</th>
                    <th class="num" style="color:#ffffff;">Biến Động (Tr ₫)</th>
                    <th class="num" style="color:#ffffff;">% Biến Động</th>
                  </tr>
                </thead>""",
    html,
    flags=re.DOTALL
)

# Replace table-truythu-top-am
html = re.sub(
    r'<table class="bi-table" id="table-truythu-top-am">\s*<thead>.*?</thead>',
    """<table class="bi-table" id="table-truythu-top-am">
                <thead>
                  <tr style="background: #1e3a8a; color: #ffffff;">
                    <th class="center" style="width: 44px; color:#ffffff;">#</th>
                    <th style="color:#ffffff;">AM Phụ Trách</th>
                    <th class="num" style="color:#ffffff;">Ticket W39</th>
                    <th class="num" style="background: #0284c7; color:#ffffff; font-weight:800;">Ticket W40</th>
                    <th class="num" style="color:#ffffff;">Biến Động Ticket</th>
                    <th class="num" style="color:#ffffff;">Cần Thu W39 (Tr ₫)</th>
                    <th class="num" style="background: #dc2626; color:#ffffff; font-weight:900;">Cần Thu W40 (Tr ₫)</th>
                    <th class="num" style="color:#ffffff;">Biến Động (Tr ₫)</th>
                    <th class="num" style="color:#ffffff;">% Biến Động</th>
                    <th class="center" style="color:#ffffff;">Mức Độ</th>
                    <th style="color:#ffffff;">Bưu Cục Trọng Điểm</th>
                  </tr>
                </thead>""",
    html,
    flags=re.DOTALL
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Exact theads updated in index.html!")

# 2. Update app.js
with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

# Fix table-overview-kpi-data querySelector typo
app_js = app_js.replace(
    "const thOv4 = document.querySelector('#table-overview-kpi thead th:nth-child(6)');",
    "const thOv4 = document.querySelector('#table-overview-kpi-data thead th:nth-child(6), #table-overview-kpi thead th:nth-child(6)');"
)
app_js = app_js.replace(
    "const thOv3 = document.querySelector('#table-overview-kpi thead th:nth-child(5)');",
    "const thOv3 = document.querySelector('#table-overview-kpi-data thead th:nth-child(5), #table-overview-kpi thead th:nth-child(5)');"
)
app_js = app_js.replace(
    "const thOv2 = document.querySelector('#table-overview-kpi thead th:nth-child(4)');",
    "const thOv2 = document.querySelector('#table-overview-kpi-data thead th:nth-child(4), #table-overview-kpi thead th:nth-child(4)');"
)
app_js = app_js.replace(
    "const thOv1 = document.querySelector('#table-overview-kpi thead th:nth-child(3)');",
    "const thOv1 = document.querySelector('#table-overview-kpi-data thead th:nth-child(3), #table-overview-kpi thead th:nth-child(3)');"
)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)

print("Table overview selector typo fixed in app.js!")
