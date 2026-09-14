import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Tab 8 OPR
html = html.replace("so với W35: 76.1%", "so với W36: 76.1%")

# Tab 10 FD fallback cards
html = html.replace("W35: 318,986 đ (▼ -4.6%)", "W36: 357,249 đ (+1.9%)")
html = html.replace("W35: 64,311 đ (▼ -0.1%)", "W36: 63,122 đ (+8.9%)")

# Tab 12 Truy thu
html = html.replace("Tổng quan toàn vùng W36:", "Tổng quan toàn vùng W37:")

# Tab 5 banner
html = html.replace("Chart Xu Hướng 4 Tuần W33-W36", "Chart Xu Hướng 4 Tuần W34-W37")

# Tab 14
html = html.replace("Kỳ 23–29/8: 1,073.2 triệu", "Kỳ 30/8–5/9: 1,073.2 triệu")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✓ Cleaned up remaining static texts in index.html")
