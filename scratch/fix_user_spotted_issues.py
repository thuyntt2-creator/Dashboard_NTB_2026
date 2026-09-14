import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

# ==============================================================================
# 1. FIX INDEX.HTML
# ==============================================================================
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix table-gtc-tts-detailed (Screenshot 1)
# Replace the duplicate TTS W37 headers
old_gtc_tts_thead = """                    <th class="num">TTS W37</th>
                    <th class="num" style="background: var(--color-amber-bg); font-weight: 800; color: #ea580c;">TTS W37</th>"""

new_gtc_tts_thead = """                    <th class="num">TTS W36</th>
                    <th class="num" style="background: var(--color-amber-bg); font-weight: 800; color: #ea580c;">TTS W37</th>"""

if old_gtc_tts_thead in html:
    html = html.replace(old_gtc_tts_thead, new_gtc_tts_thead)
    print("✓ Fixed table-gtc-tts-detailed thead in index.html (TTS W36 vs TTS W37)")
else:
    print("⚠ Could not find exact old_gtc_tts_thead in index.html")

# Fix table-odr-tts-detailed (Screenshot 3 & 4)
# Replace the duplicate TTS W37 headers
old_odr_tts_thead = """                    <th class="num">TTS W37</th>
                    <th class="num" style="background: var(--color-amber-bg); font-weight: 800; color: #ea580c;">TTS W37</th>"""

new_odr_tts_thead = """                    <th class="num">TTS W36</th>
                    <th class="num" style="background: var(--color-amber-bg); font-weight: 800; color: #ea580c;">TTS W37</th>"""

if old_odr_tts_thead in html:
    html = html.replace(old_odr_tts_thead, new_odr_tts_thead)
    print("✓ Fixed table-odr-tts-detailed thead in index.html (TTS W36 vs TTS W37)")

# Fix table-gan-ca1-detailed
html = html.replace(
    '<th class="num">W35</th>\n                    <th class="num" style="background: var(--color-blue-bg); font-weight:800;">Ca 1+Tồn W37</th>',
    '<th class="num">W36</th>\n                    <th class="num" style="background: var(--color-blue-bg); font-weight:800;">Ca 1+Tồn W37</th>'
)

# Fix table-odr-tinh-tts (was W33 W34 W35 %ODR W37)
html = html.replace(
    '<th class="num">W33</th>\n                    <th class="num">W34</th>\n                    <th class="num">W35</th>\n                    <th class="num" style="background: var(--color-amber-bg); font-weight: 800;">%ODR W37</th>',
    '<th class="num">W34</th>\n                    <th class="num">W35</th>\n                    <th class="num">W36</th>\n                    <th class="num" style="background: var(--color-amber-bg); font-weight: 800;">%ODR W37</th>'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("✓ index.html updated successfully")

# ==============================================================================
# 2. FIX APP.JS
# ==============================================================================
with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

# Fix Screenshot 2: renderGanOverviewChart datasets (W32, W33, W34, W35 -> W34, W35, W36, W37)
old_gan_chart = """    charts.ganOverviewBar = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [
          {
            type: 'bar',
            label: 'W32',
            data: overview.map(d => Number((d.w32 * 100).toFixed(1))),
            backgroundColor: '#cbd5e1',
            borderRadius: 3,
            datalabels: { display: false }
          },
          {
            type: 'bar',
            label: 'W33',
            data: overview.map(d => Number((d.w33 * 100).toFixed(1))),
            backgroundColor: '#94a3b8',
            borderRadius: 3,
            datalabels: { display: false }
          },
          {
            type: 'bar',
            label: 'W34',
            data: overview.map(d => Number((d.w34 * 100).toFixed(1))),
            backgroundColor: '#60a5fa',
            borderRadius: 3,
            datalabels: { display: false }
          },
          {
            type: 'bar',
            label: 'W35',
            data: overview.map(d => Number((d.w35 * 100).toFixed(1))),
            backgroundColor: overview.map(d => d.w35 >= 0.80 ? '#10b981' : '#f59e0b'),
            borderRadius: 4,
            datalabels: {
              display: true,
              align: 'top',
              anchor: 'end',
              color: '#0f172a',
              font: { size: 10.5, weight: '800' },
              formatter: v => v + '%'
            }
          }
        ]
      },"""

new_gan_chart = """    const weeks = D.meta?.weeks || ['W34', 'W35', 'W36', 'W37'];
    const w1 = weeks[0].toLowerCase();
    const w2 = weeks[1].toLowerCase();
    const w3 = weeks[2].toLowerCase();
    const w4 = weeks[3].toLowerCase();

    charts.ganOverviewBar = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [
          {
            type: 'bar',
            label: weeks[0],
            data: overview.map(d => Number(((d[w1] !== undefined ? d[w1] : (d.w34 || 0)) * 100).toFixed(1))),
            backgroundColor: '#cbd5e1',
            borderRadius: 3,
            datalabels: { display: false }
          },
          {
            type: 'bar',
            label: weeks[1],
            data: overview.map(d => Number(((d[w2] !== undefined ? d[w2] : (d.w35 || 0)) * 100).toFixed(1))),
            backgroundColor: '#94a3b8',
            borderRadius: 3,
            datalabels: { display: false }
          },
          {
            type: 'bar',
            label: weeks[2],
            data: overview.map(d => Number(((d[w3] !== undefined ? d[w3] : (d.w36 || 0)) * 100).toFixed(1))),
            backgroundColor: '#60a5fa',
            borderRadius: 3,
            datalabels: { display: false }
          },
          {
            type: 'bar',
            label: weeks[3],
            data: overview.map(d => Number(((d[w4] !== undefined ? d[w4] : (d.w37 || 0)) * 100).toFixed(1))),
            backgroundColor: overview.map(d => (d[w4] !== undefined ? d[w4] : (d.w37 || 0)) >= 0.80 ? '#10b981' : '#f59e0b'),
            borderRadius: 4,
            datalabels: {
              display: true,
              align: 'top',
              anchor: 'end',
              color: '#0f172a',
              font: { size: 10.5, weight: '800' },
              formatter: v => v + '%'
            }
          }
        ]
      },"""

if old_gan_chart in app_js:
    app_js = app_js.replace(old_gan_chart, new_gan_chart)
    print("✓ Fixed renderGanOverviewChart datasets in app.js (W34, W35, W36, W37)")
else:
    print("⚠ Could not find exact old_gan_chart in app.js")

# Fix tblBodyTinhTTS in renderVolumeTab
old_tinh_tts_v = """        const v1 = row.w36 !== undefined ? row.w33 : row.w32;
        const v2 = row.w36 !== undefined ? row.w34 : row.w33;
        const v3 = row.w36 !== undefined ? row.w35 : row.w34;
        const v4 = row.w36 !== undefined ? (row.w36 || row.vol) : (row.w35 || row.vol);"""

new_tinh_tts_v = """        const wKeys = (D.meta?.weeks || ['W34', 'W35', 'W36', 'W37']).map(w => w.toLowerCase());
        const v1 = row[wKeys[0]] !== undefined ? row[wKeys[0]] : (row.w34 || 0);
        const v2 = row[wKeys[1]] !== undefined ? row[wKeys[1]] : (row.w35 || 0);
        const v3 = row[wKeys[2]] !== undefined ? row[wKeys[2]] : (row.w36 || 0);
        const v4 = row[wKeys[3]] !== undefined ? row[wKeys[3]] : (row.w37 !== undefined ? row.w37 : (row.vol || 0));"""

if old_tinh_tts_v in app_js:
    app_js = app_js.replace(old_tinh_tts_v, new_tinh_tts_v)
    print("✓ Fixed tblBodyTinhTTS 4-week mapping in app.js")

# Update updateDynamicWeekLabels() to ensure TTS headers in GTC and ODR are strictly TTS ${prevW} and TTS ${currW}
old_dyn_target = """    const thGtcTtsPrev = document.querySelector('#table-gtc-tts-detailed thead th:nth-child(4)');
    const thGtcTtsCurr = document.querySelector('#table-gtc-tts-detailed thead th:nth-child(5)');
    if (thGtcTtsPrev) thGtcTtsPrev.textContent = prevW;
    if (thGtcTtsCurr) thGtcTtsCurr.textContent = currW;"""

new_dyn_target = """    const thGtcTtsPrev = document.querySelector('#table-gtc-tts-detailed thead th:nth-child(4)');
    const thGtcTtsCurr = document.querySelector('#table-gtc-tts-detailed thead th:nth-child(5)');
    if (thGtcTtsPrev) thGtcTtsPrev.textContent = `TTS ${prevW}`;
    if (thGtcTtsCurr) thGtcTtsCurr.textContent = `TTS ${currW}`;

    const thOdrTtsPrev = document.querySelector('#table-odr-tts-detailed thead th:nth-child(4)');
    const thOdrTtsCurr = document.querySelector('#table-odr-tts-detailed thead th:nth-child(5)');
    if (thOdrTtsPrev) thOdrTtsPrev.textContent = `TTS ${prevW}`;
    if (thOdrTtsCurr) thOdrTtsCurr.textContent = `TTS ${currW}`;"""

if old_dyn_target in app_js:
    app_js = app_js.replace(old_dyn_target, new_dyn_target)
    print("✓ Fixed updateDynamicWeekLabels for GTC TTS and ODR TTS headers")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)
print("✓ app.js updated successfully")
