import sys

sys.stdout.reconfigure(encoding='utf-8')

# 1. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix table-gan-ca1-detailed header
html = html.replace(
    '<th class="num">W35</th>\n                    <th class="num" style="background: var(--color-amber-bg); font-weight:800;">Ca 1+Tồn W37</th>',
    '<th class="num">Ca 1+Tồn W36</th>\n                    <th class="num" style="background: var(--color-amber-bg); font-weight:800;">Ca 1+Tồn W37</th>'
)

# Fix table-odr-tinh-tts header
html = html.replace(
    '<th class="num">W33</th>\n                    <th class="num">W34</th>\n                    <th class="num">W35</th>\n                    <th class="num" style="background: var(--color-amber-bg); font-weight: 800; color: #ea580c;">%ODR W37</th>',
    '<th class="num">W34</th>\n                    <th class="num">W35</th>\n                    <th class="num">W36</th>\n                    <th class="num" style="background: var(--color-amber-bg); font-weight: 800; color: #ea580c;">%ODR W37</th>'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("✓ index.html updated")

# 2. Update updateDynamicWeekLabels() in app.js
with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

# Enhance updateDynamicWeekLabels to explicitly handle all these headers dynamically
old_dyn_block = """    const thGtcTtsPrev = document.querySelector('#table-gtc-tts-detailed thead th:nth-child(4)');
    const thGtcTtsCurr = document.querySelector('#table-gtc-tts-detailed thead th:nth-child(5)');
    if (thGtcTtsPrev) thGtcTtsPrev.textContent = `TTS ${prevW}`;
    if (thGtcTtsCurr) thGtcTtsCurr.textContent = `TTS ${currW}`;

    const thOdrTtsPrev = document.querySelector('#table-odr-tts-detailed thead th:nth-child(4)');
    const thOdrTtsCurr = document.querySelector('#table-odr-tts-detailed thead th:nth-child(5)');
    if (thOdrTtsPrev) thOdrTtsPrev.textContent = `TTS ${prevW}`;
    if (thOdrTtsCurr) thOdrTtsCurr.textContent = `TTS ${currW}`;"""

new_dyn_block = """    const thGtcTtsPrev = document.querySelector('#table-gtc-tts-detailed thead th:nth-child(4)');
    const thGtcTtsCurr = document.querySelector('#table-gtc-tts-detailed thead th:nth-child(5)');
    if (thGtcTtsPrev) thGtcTtsPrev.textContent = `TTS ${prevW}`;
    if (thGtcTtsCurr) thGtcTtsCurr.textContent = `TTS ${currW}`;

    const thOdrTtsPrev = document.querySelector('#table-odr-tts-detailed thead th:nth-child(4)');
    const thOdrTtsCurr = document.querySelector('#table-odr-tts-detailed thead th:nth-child(5)');
    if (thOdrTtsPrev) thOdrTtsPrev.textContent = `TTS ${prevW}`;
    if (thOdrTtsCurr) thOdrTtsCurr.textContent = `TTS ${currW}`;

    const thGanCa1Prev = document.querySelector('#table-gan-ca1-detailed thead th:nth-child(4)');
    const thGanCa1Curr = document.querySelector('#table-gan-ca1-detailed thead th:nth-child(5)');
    if (thGanCa1Prev) thGanCa1Prev.textContent = `Ca 1+Tồn ${prevW}`;
    if (thGanCa1Curr) thGanCa1Curr.textContent = `Ca 1+Tồn ${currW}`;

    const thGanCa2Prev = document.querySelector('#table-gan-ca2-detailed thead th:nth-child(4)');
    const thGanCa2Curr = document.querySelector('#table-gan-ca2-detailed thead th:nth-child(5)');
    if (thGanCa2Prev) thGanCa2Prev.textContent = `Tổng ${prevW}`;
    if (thGanCa2Curr) thGanCa2Curr.textContent = `Gán Tổng ${currW}`;"""

if old_dyn_block in app_js:
    app_js = app_js.replace(old_dyn_block, new_dyn_block)
    print("✓ Enhanced updateDynamicWeekLabels with Gan Ca1 & Ca2 table headers")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)
print("✓ app.js updated")
