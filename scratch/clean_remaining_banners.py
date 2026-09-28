import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('(FULL HÀNG vs TTS — W38)', '(FULL HÀNG vs TTS — W39)')
html = html.replace('ĐIỂM NỔI BẬT & ĐÁNH GIÁ W38', 'ĐIỂM NỔI BẬT & ĐÁNH GIÁ W39')

# Volume banner
html = html.replace(
    '<h3 id="banner-volume-title">PHÂN TÍCH SẢN LƯỢNG GIAO TOÀN VÙNG, 5 TỈNH THÀNH & 18 AM (W38)</h3>',
    '<h3 id="banner-volume-title">PHÂN TÍCH SẢN LƯỢNG GIAO TOÀN VÙNG, 5 TỈNH THÀNH & 18 AM (W39)</h3>'
)
html = re.sub(
    r'• <strong>Sản lượng Toàn Mạng \(W38\):</strong>.*?(?=•|</div>|</p>)',
    '• <strong>Sản lượng Toàn Mạng (W39):</strong> Full hàng đạt <strong>328,925 đơn</strong> (giảm <strong>-14,672 đơn / -4.3% WoW</strong> so với W38: 343,597 đơn); Kênh TikTok Shop đạt <strong>72,781 đơn</strong> (+4,055 đơn / +5.9% WoW). ',
    html,
    flags=re.DOTALL
)

# OPR and KTC labels
html = html.replace('%OPR 9h–19h (W38)', '%OPR 9h–19h (W39)')
html = html.replace('%OPR 19h–9h (W38)', '%OPR 19h–9h (W39)')
html = html.replace('% Rớt LC (W38)', '% Rớt LC (W39)')
html = html.replace('W37: 54.8% → W38: 51.0% (▼ -3.8%p)', 'W38: 51.0% → W39: 47.7% (▼ -3.3%p)')
html = html.replace('Cột Xám: Tuần W37 | Cột Đỏ: Tuần W38', 'Cột Xám: Tuần W38 | Cột Đỏ: Tuần W39')
html = html.replace('Cột Xám: W37 (Tr ₫) | Cột Cam: W38 (Tr ₫)', 'Cột Xám: W38 (Tr ₫) | Cột Cam: W39 (Tr ₫)')
html = html.replace('Cột Xám: Tiền W37 | Cột Đỏ: Tiền W38', 'Cột Xám: Tiền W38 | Cột Đỏ: Tiền W39')
html = html.replace('Kỳ 7–13/9 (W37) vs Kỳ 14–20/9 (W38)', 'Kỳ 14–20/9 (W38) vs Kỳ 21–27/9 (W39)')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Remaining banners successfully cleaned and updated in index.html!")
