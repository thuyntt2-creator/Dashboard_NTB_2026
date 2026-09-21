import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

reps = [
    (
"""                  <th class="num">W34</th>
                  <th class="num">W35</th>
                  <th class="num">W36</th>
                  <th class="num" style="background: var(--color-blue-bg); color: var(--color-blue-dark); font-weight: 800;">W37 (Kỳ N)</th>""",
"""                  <th class="num">W35</th>
                  <th class="num">W36</th>
                  <th class="num">W37</th>
                  <th class="num" style="background: var(--color-blue-bg); color: var(--color-blue-dark); font-weight: 800;">W38 (Kỳ N)</th>"""
    ),
    (
"""                    <th class="num">Full W36</th>
                    <th class="num" style="background: var(--color-blue-bg); font-weight:800;">Full W37</th>""",
"""                    <th class="num">Full W37</th>
                    <th class="num" style="background: var(--color-blue-bg); font-weight:800;">Full W38</th>"""
    ),
    (
"""                    <th class="num">TTS W36</th>
                    <th class="num" style="background: var(--color-amber-bg); font-weight:800; color:#ea580c;">TTS W37</th>""",
"""                    <th class="num">TTS W37</th>
                    <th class="num" style="background: var(--color-amber-bg); font-weight:800; color:#ea580c;">TTS W38</th>"""
    ),
    (
"""                    <th class="num">W36</th>
                    <th class="num" style="background: var(--color-blue-bg); font-weight: 800;">W37</th>""",
"""                    <th class="num">W37</th>
                    <th class="num" style="background: var(--color-blue-bg); font-weight: 800;">W38</th>"""
    ),
    (
"""                    <th class="num">Ca 1+Tồn W36</th>
                    <th class="num" style="background: var(--color-amber-bg); font-weight:800;">Ca 1+Tồn W37</th>""",
"""                    <th class="num">Ca 1+Tồn W37</th>
                    <th class="num" style="background: var(--color-amber-bg); font-weight:800;">Ca 1+Tồn W38</th>"""
    )
]

for src, tgt in reps:
    if src in html:
        html = html.replace(src, tgt)
        print("Replaced 1 table header!")
    else:
        print("Failed to find: ", src[:40])

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Finished patching last 5 theads!")
