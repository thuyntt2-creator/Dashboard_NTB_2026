import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

direct_replacements = [
    # 1. table-vol-tinh-full
    (
"""                    <th class="num">W34</th>
                    <th class="num">W35</th>
                    <th class="num">W36</th>
                    <th class="num" style="background: var(--color-blue-bg); font-weight: 800;">W37</th>""",
"""                    <th class="num">W35</th>
                    <th class="num">W36</th>
                    <th class="num">W37</th>
                    <th class="num" style="background: var(--color-blue-bg); font-weight: 800;">W38</th>"""
    ),
    # 2. table-vol-tinh-tts
    (
"""                    <th class="num">W34</th>
                    <th class="num">W35</th>
                    <th class="num">W36</th>
                    <th class="num" style="background: var(--color-amber-bg); font-weight: 800; color: #ea580c;">W37</th>""",
"""                    <th class="num">W35</th>
                    <th class="num">W36</th>
                    <th class="num">W37</th>
                    <th class="num" style="background: var(--color-amber-bg); font-weight: 800; color: #ea580c;">W38</th>"""
    ),
    # 3. table-gtc-tinh-full
    (
"""                    <th class="num">W34</th>
                    <th class="num">W35</th>
                    <th class="num">W36</th>
                    <th class="num" style="background: var(--color-blue-bg); font-weight: 800;">%GTC W37</th>""",
"""                    <th class="num">W35</th>
                    <th class="num">W36</th>
                    <th class="num">W37</th>
                    <th class="num" style="background: var(--color-blue-bg); font-weight: 800;">%GTC W38</th>"""
    ),
    # 4. table-gtc-tinh-tts
    (
"""                    <th class="num">W34</th>
                    <th class="num">W35</th>
                    <th class="num">W36</th>
                    <th class="num" style="background: var(--color-amber-bg); font-weight: 800; color: #ea580c;">%GTC W37</th>""",
"""                    <th class="num">W35</th>
                    <th class="num">W36</th>
                    <th class="num">W37</th>
                    <th class="num" style="background: var(--color-amber-bg); font-weight: 800; color: #ea580c;">%GTC W38</th>"""
    ),
    # 5. table-gtc-tts-ca1-detailed
    (
"""                  <th class="num">%GTC TTS Ca 1 (W36)</th>
                  <th class="num" style="background: var(--color-amber-bg); font-weight:800; color:#c2410c;">%GTC TTS Ca 1 (W37)</th>""",
"""                  <th class="num">%GTC TTS Ca 1 (W37)</th>
                  <th class="num" style="background: var(--color-amber-bg); font-weight:800; color:#c2410c;">%GTC TTS Ca 1 (W38)</th>"""
    ),
    # 6. table-gan-overview-region
    (
"""                    <th class="num" style="color: #ffffff;">W34</th>
                    <th class="num" style="color: #ffffff;">W35</th>
                    <th class="num" style="color: #ffffff;">W36</th>
                    <th class="num" style="color: #ffffff; background: rgba(255,255,255,0.2); font-weight:800;">W37</th>
                    <th class="num" style="color: #ffffff;">Δ W37/W36</th>""",
"""                    <th class="num" style="color: #ffffff;">W35</th>
                    <th class="num" style="color: #ffffff;">W36</th>
                    <th class="num" style="color: #ffffff;">W37</th>
                    <th class="num" style="color: #ffffff; background: rgba(255,255,255,0.2); font-weight:800;">W38</th>
                    <th class="num" style="color: #ffffff;">Δ W38/W37</th>"""
    ),
    # 7. table-odr-tinh-full
    (
"""                    <th class="num">W34</th>
                    <th class="num">W35</th>
                    <th class="num">W36</th>
                    <th class="num" style="background: var(--color-green-bg); font-weight: 800;">%ODR W37</th>""",
"""                    <th class="num">W35</th>
                    <th class="num">W36</th>
                    <th class="num">W37</th>
                    <th class="num" style="background: var(--color-green-bg); font-weight: 800;">%ODR W38</th>"""
    ),
    # 8. table-odr-tinh-tts
    (
"""                    <th class="num">W34</th>
                    <th class="num">W35</th>
                    <th class="num">W36</th>
                    <th class="num" style="background: var(--color-amber-bg); font-weight: 800; color: #ea580c;">%ODR W37</th>""",
"""                    <th class="num">W35</th>
                    <th class="num">W36</th>
                    <th class="num">W37</th>
                    <th class="num" style="background: var(--color-amber-bg); font-weight: 800; color: #ea580c;">%ODR W38</th>"""
    ),
    # 9. table-rot-am-detailed
    (
"""                    <th class="num">% Rớt W36</th>
                    <th class="num" style="background: var(--color-red-bg); font-weight:800; color:#b91c1c;">% Rớt W37</th>""",
"""                    <th class="num">% Rớt W37</th>
                    <th class="num" style="background: var(--color-red-bg); font-weight:800; color:#b91c1c;">% Rớt W38</th>"""
    ),
    # 10. table-rot-tinh-detailed (there are two occurrences of % Rớt W36 / % Rớt W37, handled by replace)
    # 11. table-vol-full-detailed
    (
"""                    <th class="num">Full W36</th>
                    <th class="num" style="background: var(--color-blue-bg); font-weight: 800;">Full W37</th>""",
"""                    <th class="num">Full W37</th>
                    <th class="num" style="background: var(--color-blue-bg); font-weight: 800;">Full W38</th>"""
    ),
    # 12. table-vol-tts-detailed
    (
"""                    <th class="num">TTS W36</th>
                    <th class="num" style="background: var(--color-amber-bg); font-weight: 800; color: #ea580c;">TTS W37</th>""",
"""                    <th class="num">TTS W37</th>
                    <th class="num" style="background: var(--color-amber-bg); font-weight: 800; color: #ea580c;">TTS W38</th>"""
    ),
    # 13. table-gtc-full-detailed
    (
"""                    <th class="num">W36</th>
                    <th class="num" style="background: var(--color-blue-bg); font-weight:800;">W37</th>""",
"""                    <th class="num">W37</th>
                    <th class="num" style="background: var(--color-blue-bg); font-weight:800;">W38</th>"""
    ),
    # 14. table-gtc-tts-detailed
    (
"""                    <th class="num">TTS W36</th>
                    <th class="num" style="background: var(--color-amber-bg); font-weight: 800; color: #ea580c;">TTS W37</th>""",
"""                    <th class="num">TTS W37</th>
                    <th class="num" style="background: var(--color-amber-bg); font-weight: 800; color: #ea580c;">TTS W38</th>"""
    ),
    # 15. table-odr-full-detailed
    (
"""                    <th class="num">W36</th>
                    <th class="num" style="background: var(--color-green-bg); font-weight:800;">W37</th>""",
"""                    <th class="num">W37</th>
                    <th class="num" style="background: var(--color-green-bg); font-weight:800;">W38</th>"""
    ),
    # 16. table-odr-tts-detailed
    (
"""                    <th class="num">TTS W36</th>
                    <th class="num" style="background: var(--color-amber-bg); font-weight: 800; color: #ea580c;">TTS W37</th>""",
"""                    <th class="num">TTS W37</th>
                    <th class="num" style="background: var(--color-amber-bg); font-weight: 800; color: #ea580c;">TTS W38</th>"""
    ),
    # 17. table-gan-ca1-detailed
    (
"""                    <th class="num">Ca 1+Tồn W36</th>
                    <th class="num" style="background: var(--color-green-bg); font-weight:800; color:#166534;">Ca 1+Tồn W37</th>""",
"""                    <th class="num">Ca 1+Tồn W37</th>
                    <th class="num" style="background: var(--color-green-bg); font-weight:800; color:#166534;">Ca 1+Tồn W38</th>"""
    ),
    # 18. table-gan-ca2-detailed
    (
"""                    <th class="num">Tổng W36</th>
                    <th class="num" style="background: var(--color-purple-bg); font-weight:800; color:#7e22ce;">Gán Tổng W37</th>""",
"""                    <th class="num">Tổng W37</th>
                    <th class="num" style="background: var(--color-purple-bg); font-weight:800; color:#7e22ce;">Gán Tổng W38</th>"""
    ),
    # 19. table-ltc-detailed & table-ltc-tinh-detailed
    (
"""                    <th class="num">W34</th>
                    <th class="num">W35</th>
                    <th class="num">W36</th>
                    <th class="num" style="background: var(--color-blue-bg); font-weight:800;">%LTC W37</th>""",
"""                    <th class="num">W35</th>
                    <th class="num">W36</th>
                    <th class="num">W37</th>
                    <th class="num" style="background: var(--color-blue-bg); font-weight:800;">%LTC W38</th>"""
    ),
    # 20. table-opr-day-detailed
    (
"""                    <th class="num">Đơn Ngày</th>
                    <th class="num">W36</th>
                    <th class="num" style="background: var(--color-blue-bg); font-weight:800;">%OPR W37</th>""",
"""                    <th class="num">Đơn Ngày</th>
                    <th class="num">W37</th>
                    <th class="num" style="background: var(--color-blue-bg); font-weight:800;">%OPR W38</th>"""
    ),
    # 21. table-opr-night-detailed
    (
"""                    <th class="num">Đơn Đêm</th>
                    <th class="num">W36</th>
                    <th class="num" style="background: var(--color-amber-bg); font-weight:800; color:#ea580c;">%OPR W37</th>""",
"""                    <th class="num">Đơn Đêm</th>
                    <th class="num">W37</th>
                    <th class="num" style="background: var(--color-amber-bg); font-weight:800; color:#ea580c;">%OPR W38</th>"""
    ),
    # 22. table-fd-am-detailed
    (
"""                  <th class="num">Full W36</th>
                  <th class="num" style="background: var(--color-blue-bg); font-weight:800;">Full W37</th>
                  <th class="num">Biến Động (Δ)</th>
                  <th class="num">Vol TTS</th>
                  <th class="num">TTS W36</th>
                  <th class="num" style="background: var(--color-amber-bg); font-weight:800; color:#ea580c;">TTS W37</th>""",
"""                  <th class="num">Full W37</th>
                  <th class="num" style="background: var(--color-blue-bg); font-weight:800;">Full W38</th>
                  <th class="num">Biến Động (Δ)</th>
                  <th class="num">Vol TTS</th>
                  <th class="num">TTS W37</th>
                  <th class="num" style="background: var(--color-amber-bg); font-weight:800; color:#ea580c;">TTS W38</th>"""
    ),
    # 23. table-kd-churn-top10
    (
"""                  <th class="num" style="color:#ffffff;">Kỳ Trước (W36)</th>
                  <th class="num" style="background: #ef4444; color:#ffffff; font-weight:800;">Kỳ Này (W37)</th>""",
"""                  <th class="num" style="color:#ffffff;">Kỳ Trước (W37)</th>
                  <th class="num" style="background: #ef4444; color:#ffffff; font-weight:800;">Kỳ Này (W38)</th>"""
    ),
    # 24. table-bc-canhbao-tab & table-bc-canh-bao-overview & table-bc-canh-bao
    (
"""                  <th class="num" style="background: #0284c7; color: #ffffff; font-weight: 700;">%GTC W36</th>
                  <th class="num" style="background: #dc2626; color: #ffffff; font-weight: 800;">%GTC W37</th>""",
"""                  <th class="num" style="background: #0284c7; color: #ffffff; font-weight: 700;">%GTC W37</th>
                  <th class="num" style="background: #dc2626; color: #ffffff; font-weight: 800;">%GTC W38</th>"""
    ),
    (
"""                    <th class="num" style="background: #0284c7; color: #ffffff; font-weight: 700;">%GTC W36</th>
                    <th class="num" style="background: #dc2626; color: #ffffff; font-weight: 800;">%GTC W37</th>""",
"""                    <th class="num" style="background: #0284c7; color: #ffffff; font-weight: 700;">%GTC W37</th>
                    <th class="num" style="background: #dc2626; color: #ffffff; font-weight: 800;">%GTC W38</th>"""
    ),
    # 25. table-overview-kpi-data
    (
"""                    <th class="num">W34</th>
                    <th class="num">W35</th>
                    <th class="num">W36</th>
                    <th class="num" style="background: var(--color-blue-bg); font-weight:800; color: var(--color-primary);">W37 (Kỳ N)</th>""",
"""                    <th class="num">W35</th>
                    <th class="num">W36</th>
                    <th class="num">W37</th>
                    <th class="num" style="background: var(--color-blue-bg); font-weight:800; color: var(--color-primary);">W38 (Kỳ N)</th>"""
    )
]

for src, tgt in direct_replacements:
    if src in html:
        html = html.replace(src, tgt)
        print(f"Replaced: {src[:40]}...")
    else:
        print(f"NOT FOUND: {src[:40]}...")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("SUCCESS: Directly patched index.html headers!")
