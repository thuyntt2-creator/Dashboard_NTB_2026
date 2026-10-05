import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

# ==============================================================================
# PART 1: INDEX.HTML
# ==============================================================================
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Overview Tab fixes
html = html.replace('XU HƯỚNG CÁC CHỈ SỐ VẬN HÀNH CHÍNH (W36 – W39)', 'XU HƯỚNG CÁC CHỈ SỐ VẬN HÀNH CHÍNH (W37 – W40)')
html = html.replace('XU HƯỚNG CÁC CHỈ SỐ VẬN HÀNH CHÍNH (W36 - W39)', 'XU HƯỚNG CÁC CHỈ SỐ VẬN HÀNH CHÍNH (W37 – W40)')
html = html.replace('SẢN LƯỢNG GIAO THEO 5 TỈNH THÀNH (FULL HÀNG vs TTS — W39)', 'SẢN LƯỢNG GIAO THEO 5 TỈNH THÀNH (FULL HÀNG vs TTS — W40)')
html = html.replace('SẢN LƯỢNG GIAO THEO 5 TỈNH THÀNH (FULL HÀNG VS TTS — W39)', 'SẢN LƯỢNG GIAO THEO 5 TỈNH THÀNH (FULL HÀNG vs TTS — W40)')
html = html.replace('ĐIỂM NỔI BẬT & ĐÁNH GIÁ W39', 'ĐIỂM NỔI BẬT & ĐÁNH GIÁ W40')
html = html.replace('ĐIỂM NỔI BẬT &amp; ĐÁNH GIÁ W39', 'ĐIỂM NỔI BẬT &amp; ĐÁNH GIÁ W40')
html = html.replace('BẢNG TỔNG HỢP CÁC CHỈ SỐ VÙNG NTB (W36 – W39) — FULL HÀNG & TTS', 'BẢNG TỔNG HỢP CÁC CHỈ SỐ VÙNG NTB (W37 – W40) — FULL HÀNG & TTS')
html = html.replace('BẢNG TỔNG HỢP CÁC CHỈ SỐ VÙNG NTB (W36 – W39) — FULL HÀNG &amp; TTS', 'BẢNG TỔNG HỢP CÁC CHỈ SỐ VÙNG NTB (W37 – W40) — FULL HÀNG &amp; TTS')
html = html.replace('Dữ liệu so sánh W36 – W39 kèm đường Xu Hướng (Trend)', 'Dữ liệu so sánh W37 – W40 kèm đường Xu Hướng (Trend)')

# 2. Tab 2 Sản Lượng Table 3A / 3B headers: W36, W37, W38, W39 -> W37, W38, W39, W40
html = re.sub(
    r'<th class="num">W36</th>\s*<th class="num">W37</th>\s*<th class="num">W38</th>\s*<th class="num"[^>]*>W39</th>',
    r'<th class="num">W37</th>\n                    <th class="num">W38</th>\n                    <th class="num">W39</th>\n                    <th class="num" style="background: var(--color-amber-bg); font-weight: 800; color: #ea580c;">W40</th>',
    html
)

# 3. Tab 3 GTC:
html = html.replace('⚡ So Sánh Full vs TTS (W37)', '⚡ So Sánh Full vs TTS (W40)')
html = re.sub(
    r'<th class="num">W37</th>\s*<th class="num"[^>]*>W38</th>',
    r'<th class="num">W39</th>\n                    <th class="num" style="background: var(--color-blue-bg); font-weight: 800;">W40</th>',
    html
)
html = html.replace('<th class="num">TTS W39</th>', '<th class="num">TTS W39</th>\n                    <th class="num" style="background: var(--color-amber-bg); font-weight: 800; color: #ea580c;">TTS W40</th>')
html = html.replace('THEO DÕI BƯU CỤC TRONG NHÓM CẢNH BÁO BẤT ỔN (%GTC < 45% HOẶC < 70% LỊCH SỬ) — SO SÁNH W38 vs W39',
                    'THEO DÕI BƯU CỤC TRONG NHÓM CẢNH BÁO BẤT ỔN (%GTC < 45% HOẶC < 70% LỊCH SỬ) — SO SÁNH W39 vs W40')
html = html.replace('THEO DÕI BƯU CỤC TRONG NHÓM CẢNH BÁO BẤT ỔN (%GTC &lt; 45% HOẶC &lt; 70% LỊCH SỬ) — SO SÁNH W38 vs W39',
                    'THEO DÕI BƯU CỤC TRONG NHÓM CẢNH BÁO BẤT ỔN (%GTC &lt; 45% HOẶC &lt; 70% LỊCH SỬ) — SO SÁNH W39 vs W40')

# 4. Tab 4 GTC Ca 1 TTS:
html = html.replace('<th class="num">%GTC TTS Ca 1 (W37)</th>\n                  <th class="num" style="background: var(--color-amber-bg); font-weight:800; color:#c2410c;">%GTC TTS Ca 1 (W38)</th>',
                    '<th class="num">%GTC TTS Ca 1 (W39)</th>\n                  <th class="num" style="background: var(--color-amber-bg); font-weight:800; color:#c2410c;">%GTC TTS Ca 1 (W40)</th>')

# 5. Tab 5 %Gán:
html = html.replace('<span class="badge-tag badge-tag-purple">W34 ➔ W37</span>', '<span class="badge-tag badge-tag-purple">W37 ➔ W40</span>')
html = html.replace('<th class="num" style="color: #ffffff;">W36</th>\n                    <th class="num" style="color: #ffffff;">W37</th>\n                    <th class="num" style="color: #ffffff; background: rgba(255,255,255,0.2); font-weight:800;">W38</th>\n                    <th class="num" style="color: #ffffff;">Δ W38/W37</th>',
                    '<th class="num" style="color: #ffffff;">W37</th>\n                    <th class="num" style="color: #ffffff;">W38</th>\n                    <th class="num" style="color: #ffffff;">W39</th>\n                    <th class="num" style="color: #ffffff; background: rgba(255,255,255,0.2); font-weight:800;">W40</th>\n                    <th class="num" style="color: #ffffff;">Δ W40/W39</th>')
html = html.replace('Ca 1+Tồn W37', 'Ca 1+Tồn W39')
html = html.replace('Ca 1+Tồn W38', 'Ca 1+Tồn W40')
html = html.replace('Tổng W37', 'Tổng W39')
html = html.replace('Gán Tổng W38', 'Gán Tổng W40')

# 6. Tab 6 ODR:
html = html.replace('⚡ So Sánh Full vs TTS (W37)', '⚡ So Sánh Full vs TTS (W40)')

# 7. Tab 8 OPR:
html = html.replace('<th class="num">W38</th>\n                    <th class="num" style="background: var(--color-blue-bg); font-weight:800;">%OPR W39</th>',
                    '<th class="num">W39</th>\n                    <th class="num" style="background: var(--color-blue-bg); font-weight:800;">%OPR W40</th>')
html = html.replace('<th class="num">W38</th>\n                    <th class="num" style="background: var(--color-amber-bg); font-weight:800; color:#ea580c;">%OPR W39</th>',
                    '<th class="num">W39</th>\n                    <th class="num" style="background: var(--color-amber-bg); font-weight:800; color:#ea580c;">%OPR W40</th>')
html = html.replace('%OPR 9h–19h (W37)', '%OPR 9h–19h (W39)')
html = html.replace('%OPR 9h–19h (W39)', '%OPR 9h–19h (W40)')
html = html.replace('%OPR 19h–9h (W37)', '%OPR 19h–9h (W39)')
html = html.replace('%OPR 19h–9h (W39)', '%OPR 19h–9h (W40)')

# 8. Tab 9 Rót LC:
html = html.replace('<th class="num">% Rớt W37</th>\n                    <th class="num" style="background: var(--color-red-bg); font-weight:800; color:#b91c1c;">% Rớt W39</th>',
                    '<th class="num">% Rớt W39</th>\n                    <th class="num" style="background: var(--color-red-bg); font-weight:800; color:#b91c1c;">% Rớt W40</th>')

# 9. Tab 10 FD:
html = html.replace('304,308 <small>đơn W37</small>', '311,503 <small>đơn W40</small>')
html = html.replace('W37: 357,249 đ (-4.1%)', 'W39: 331,313 đ (-6.0%)')
html = html.replace('64,220 <small>đơn W37</small>', '72,253 <small>đơn W40</small>')
html = html.replace('W37: 68,719 đ (+0.8%)', 'W39: 73,443 đ (-1.6%)')
html = html.replace('<th class="num">Full W37</th>\n                  <th class="num" style="background: var(--color-blue-bg); font-weight:800;">Full W39</th>',
                    '<th class="num">Full W39</th>\n                  <th class="num" style="background: var(--color-blue-bg); font-weight:800;">Full W40</th>')
html = html.replace('<th class="num">TTS W37</th>\n                  <th class="num" style="background: var(--color-amber-bg); font-weight:800; color:#ea580c;">TTS W39</th>',
                    '<th class="num">TTS W39</th>\n                  <th class="num" style="background: var(--color-amber-bg); font-weight:800; color:#ea580c;">TTS W40</th>')
html = html.replace('<th class="num">FD W37</th>\n                  <th class="num" style="background: var(--color-red-bg); font-weight:800; color:#b91c1c;">FD W39</th>',
                    '<th class="num">FD W39</th>\n                  <th class="num" style="background: var(--color-red-bg); font-weight:800; color:#b91c1c;">FD W40</th>')

# 10. Tab 11 KTC:
html = html.replace('Tuần W39 đạt <strong>47.7%</strong>', 'Tuần W40 đạt <strong>48.2%</strong>')
html = html.replace('TLLĐ Xe Bình Quân (W37)', 'TLLĐ Xe Bình Quân (W40)')
html = html.replace('📅 Tuần W37 (Lũy Kế 7 Ngày)', '📅 Tuần W40 (Lũy Kế 7 Ngày)')

# 11. Tab 14 Truy Thu:
html = html.replace('id="th-tt-loai-dp">Đơn W37</th>', 'id="th-tt-loai-dp">Đơn W39</th>')
html = html.replace('id="th-tt-loai-dc">Đơn W39</th>', 'id="th-tt-loai-dc">Đơn W40</th>')
html = html.replace('id="th-tt-loai-cp">Cần Thu W37 (Tr ₫)</th>', 'id="th-tt-loai-cp">Cần Thu W39 (Tr ₫)</th>')
html = html.replace('id="th-tt-loai-cc">Cần Thu W39 (Tr ₫)</th>', 'id="th-tt-loai-cc">Cần Thu W40 (Tr ₫)</th>')
html = html.replace('Đơn Tuần W37', 'Đơn Tuần W39')
html = html.replace('Đơn Tuần W39', 'Đơn Tuần W40')
html = html.replace('Cần Thu W37 (Tr ₫)', 'Cần Thu W39 (Tr ₫)')
html = html.replace('Cần Thu W39 (Tr ₫)', 'Cần Thu W40 (Tr ₫)')
html = html.replace('Ticket W37', 'Ticket W39')
html = html.replace('Ticket W39', 'Ticket W40')

# 12. Tab 15 Kinh Doanh:
html = html.replace('TOP 10 KHÁCH HÀNG CÓ SẢN LƯỢNG GIẢM / RỜI BỎ LỚN NHẤT (W37)',
                    'TOP 10 KHÁCH HÀNG CÓ SẢN LƯỢNG GIẢM / RỜI BỎ LỚN NHẤT (W40)')
html = html.replace('Kỳ Trước (W37)', 'Kỳ Trước (W39)')
html = html.replace('Kỳ Này (W39)', 'Kỳ Này (W40)')

# 13. Tab 16 Bưu Cục Cảnh Báo:
html = html.replace('%GTC W37', '%GTC W39')
html = html.replace('%GTC W39', '%GTC W40')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Part 1: index.html fully updated!")

# ==============================================================================
# PART 2: APP.JS DYNAMIC ENHANCEMENT
# ==============================================================================
with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

# Make sure updateWeekLabels updates ALL banner titles and card headers dynamically
target_func_start = '    // 1b. Executive Overview Callout Banner'
replacement_func_chunk = """    // 1b. Executive Overview Callout Banner
    const ovBannerTitle = document.getElementById('banner-overview-title');
    if (ovBannerTitle) {
      ovBannerTitle.textContent = `TỔNG HỢP TRỌNG TÂM HỌP TUẦN ${currW} — VÙNG NAM TRUNG BỘ`;
    }

    const ovBannerSummary = document.getElementById('banner-overview-summary');
    if (ovBannerSummary && D.overview && D.overview.cards) {
      const cards = D.overview.cards;
      const getCard = (id) => cards.find(c => c.id === id) || {};
      const volFull = getCard('vol_full');
      const volTts = getCard('vol_tts');
      const gtcFull = getCard('gtc_full');
      const gtcTts = getCard('gtc_tts');
      const odrFull = getCard('odr_full');
      const ltcFull = getCard('ltc_full');
      const rotLc = getCard('rot_lc');
      const fdRate = D.fd?.summary?.rate_full ? (D.fd.summary.rate_full * 100).toFixed(2) + '%' : '7.77%';
      const ttsShare = volFull.val && volTts.val ? ((volTts.val / volFull.val) * 100).toFixed(1) + '%' : '23.2%';
      
      const volFullDiff = volFull.diff !== undefined ? (volFull.diff > 0 ? `+${volFull.diff.toLocaleString('vi-VN')}` : `${volFull.diff.toLocaleString('vi-VN')}`) : '';
      const volFullPct = volFull.diff_pct !== undefined ? (volFull.diff_pct > 0 ? `+${(volFull.diff_pct * 100).toFixed(1)}%` : `${(volFull.diff_pct * 100).toFixed(1)}%`) : '';
      const volTtsDiff = volTts.diff !== undefined ? (volTts.diff > 0 ? `+${volTts.diff.toLocaleString('vi-VN')}` : `${volTts.diff.toLocaleString('vi-VN')}`) : '';
      const volTtsPct = volTts.diff_pct !== undefined ? (volTts.diff_pct > 0 ? `+${(volTts.diff_pct * 100).toFixed(1)}%` : `${(volTts.diff_pct * 100).toFixed(1)}%`) : '';

      ovBannerSummary.innerHTML = `
        • <strong>Sản lượng Giao Full Hàng:</strong> Đạt <strong>${(volFull.val || 311503).toLocaleString('vi-VN')} đơn</strong> (Tuần ${currW} (${dateRange}), ${volFullDiff} đơn / ${volFullPct} WoW so với ${prevW}).<br>
        • <strong>Sản lượng TikTok Shop (TTS):</strong> Đạt <strong>${(volTts.val || 72253).toLocaleString('vi-VN')} đơn</strong> (${volTtsDiff} đơn / ${volTtsPct} WoW so với ${prevW}), chiếm ${ttsShare} tổng sản lượng toàn vùng.<br>
        • <strong>Chất lượng vận hành bứt phá:</strong> %ODR Full đạt <strong>${odrFull.val ? (odrFull.val * 100).toFixed(1) + '%' : '93.1%'}</strong>, %LTC đạt <strong>${ltcFull.val ? (ltcFull.val * 100).toFixed(1) + '%' : '91.4%'}</strong>. Tỷ lệ Rớt LC <strong>${rotLc.val ? (rotLc.val * 100).toFixed(2) + '%' : '1.69%'}</strong>. Tỷ lệ %FD Hoàn Trả <strong>${fdRate}</strong>.<br>
        • <strong>Chỉ số %GTC:</strong> Full hàng đạt <strong>${gtcFull.val ? (gtcFull.val * 100).toFixed(1) + '%' : '60.9%'}</strong>, TTS đạt <strong>${gtcTts.val ? (gtcTts.val * 100).toFixed(1) + '%' : '63.4%'}</strong> — Hoàn thành xuất sắc mục tiêu GTC ≥ 60%!
      `;
    }

    const ovBannerActions = document.querySelector('#tab-overview .exec-banner-actions span');
    if (ovBannerActions) {
      ovBannerActions.innerHTML = `<i data-lucide="target"></i> Mục tiêu ${currW}: GTC ≥ 60% (Đạt 60.9%)`;
    }"""

# Replace in app.js
app_js = re.sub(
    r'    // 1b\. Executive Overview Callout Banner.*?ovBannerActions\.innerHTML = `.*?`;\s*}',
    replacement_func_chunk,
    app_js,
    flags=re.DOTALL
)

# Now check dynamic card titles at section 15 in app.js:
section15_old = """    // 15. Dynamic Card Titles and Headers with regex replacement
    document.querySelectorAll('.report-card-title, .exec-banner-text h2, .exec-banner-text h3').forEach(el => {
      if (el.textContent.includes('SO SÁNH TỶ LỆ GÁN 18 AM:')) {
        el.textContent = `SO SÁNH TỶ LỆ GÁN 18 AM: % GÁN CA 1+TỒN vs % GÁN CA 2 vs % GÁN TỔNG (${currW})`;
      } else if (el.textContent.includes('% RỚT LUÂN CHUYỂN THEO 18 AM PHỤ TRÁCH')) {
        el.textContent = `% RỚT LUÂN CHUYỂN THEO 18 AM PHỤ TRÁCH (${currW})`;
      } else if (el.textContent.includes('DANH SÁCH TOP 20 BƯU CỤC CÓ TỶ LỆ RỚT LUÂN CHUYỂN CAO NHẤT')) {
        el.textContent = `DANH SÁCH TOP 20 BƯU CỤC CÓ TỶ LỆ RỚT LUÂN CHUYỂN CAO NHẤT (${currW})`;
      } else if (el.textContent.includes('BẢNG 2: TOP BƯU CỤC CÓ TỶ LỆ %FD CAO NHẤT')) {
        el.textContent = `BẢNG 2: TOP BƯU CỤC CÓ TỶ LỆ %FD CAO NHẤT (${currW})`;
      } else if (el.textContent.includes('TOP 10 KHÁCH HÀNG CÓ SẢN LƯỢNG GIẢM / RỜI BỎ LỚN NHẤT')) {
        el.textContent = `TOP 10 KHÁCH HÀNG CÓ SẢN LƯỢNG GIẢM / RỜI BỎ LỚN NHẤT (${currW})`;
      }
    });"""

section15_new = """    // 15. Dynamic Card Titles and Headers with comprehensive week synchronization
    document.querySelectorAll('.report-card-title, .exec-banner-text h2, .exec-banner-text h3, .exec-banner-text h4').forEach(el => {
      let t = el.textContent;
      if (t.includes('XU HƯỚNG CÁC CHỈ SỐ VẬN HÀNH CHÍNH')) {
        el.innerHTML = `<i data-lucide="activity" style="color: var(--color-green);"></i> XU HƯỚNG CÁC CHỈ SỐ VẬN HÀNH CHÍNH (${w1} – ${currW})`;
      } else if (t.includes('SẢN LƯỢNG GIAO THEO 5 TỈNH THÀNH')) {
        el.innerHTML = `<i data-lucide="bar-chart-2" style="color: var(--ghn-navy);"></i> SẢN LƯỢNG GIAO THEO 5 TỈNH THÀNH (FULL HÀNG vs TTS — ${currW})`;
      } else if (t.includes('ĐIỂM NỔI BẬT & ĐÁNH GIÁ') || t.includes('ĐIỂM NỔI BẬT &amp; ĐÁNH GIÁ')) {
        el.innerHTML = `<i data-lucide="sparkles" style="color: var(--color-amber);"></i> ĐIỂM NỔI BẬT & ĐÁNH GIÁ ${currW}`;
      } else if (t.includes('BẢNG TỔNG HỢP CÁC CHỈ SỐ VÙNG NTB')) {
        el.innerHTML = `<i data-lucide="table" style="color: var(--color-blue);"></i> BẢNG TỔNG HỢP CÁC CHỈ SỐ VÙNG NTB (${w1} – ${currW}) — FULL HÀNG & TTS`;
      } else if (t.includes('TỔNG QUAN VÙNG NTB — TỶ LỆ % GÁN')) {
        el.innerHTML = `<i data-lucide="layout-grid" style="color: var(--ghn-orange);"></i> TỔNG QUAN VÙNG NTB — TỶ LỆ % GÁN (4 TUẦN ${w1} – ${currW})`;
      } else if (t.includes('PHÂN TÍCH SẢN LƯỢNG GIAO TOÀN VÙNG, 5 TỈNH THÀNH')) {
        el.textContent = `PHÂN TÍCH SẢN LƯỢNG GIAO TOÀN VÙNG, 5 TỈNH THÀNH & 18 AM (${currW})`;
      } else if (t.includes('PHÂN TÍCH HIỆU SUẤT %GTC TỔNG TOÀN MẠNG')) {
        el.textContent = `PHÂN TÍCH HIỆU SUẤT %GTC TỔNG TOÀN MẠNG THEO 18 AM & 5 TỈNH (${currW})`;
      } else if (t.includes('PHÂN TÍCH CHUYÊN SÂU %GTC CA 1 TIKTOK SHOP')) {
        el.textContent = `PHÂN TÍCH CHUYÊN SÂU %GTC CA 1 TIKTOK SHOP (TARGET SLA ≥ 76.0%) (${currW})`;
      } else if (t.includes('SO SÁNH TỶ LỆ GÁN 18 AM:')) {
        el.textContent = `SO SÁNH TỶ LỆ GÁN 18 AM: % GÁN CA 1+TỒN vs % GÁN CA 2 vs % GÁN TỔNG (${currW})`;
      } else if (t.includes('% RỚT LUÂN CHUYỂN THEO 18 AM PHỤ TRÁCH')) {
        el.textContent = `% RỚT LUÂN CHUYỂN THEO 18 AM PHỤ TRÁCH (${currW})`;
      } else if (t.includes('DANH SÁCH TOP 20 BƯU CỤC CÓ TỶ LỆ RỚT LUÂN CHUYỂN CAO NHẤT')) {
        el.textContent = `DANH SÁCH TOP 20 BƯU CỤC CÓ TỶ LỆ RỚT LUÂN CHUYỂN CAO NHẤT (${currW})`;
      } else if (t.includes('BÁO CÁO TỶ LỆ %FD (RETURN / HOÀN TRẢ)')) {
        el.textContent = `BÁO CÁO TỶ LỆ %FD (RETURN / HOÀN TRẢ) — VÙNG NAM TRUNG BỘ (${currW})`;
      } else if (t.includes('BẢNG 2: TOP BƯU CỤC CÓ TỶ LỆ %FD CAO NHẤT')) {
        el.textContent = `BẢNG 2: TOP BƯU CỤC CÓ TỶ LỆ %FD CAO NHẤT (${currW})`;
      } else if (t.includes('TOP 10 KHÁCH HÀNG CÓ SẢN LƯỢNG GIẢM / RỜI BỎ LỚN NHẤT')) {
        el.textContent = `TOP 10 KHÁCH HÀNG CÓ SẢN LƯỢNG GIẢM / RỜI BỎ LỚN NHẤT (${currW})`;
      }
    });

    // Dynamic banner badges and subtitles
    const volBadge = document.getElementById('banner-volume-badge');
    if (volBadge && D.overview?.cards) {
      const vFull = D.overview.cards.find(c => c.id === 'vol_full')?.val || 311503;
      const vTts = D.overview.cards.find(c => c.id === 'vol_tts')?.val || 72253;
      volBadge.textContent = `Full: ${(vFull / 1000).toFixed(1)}k đơn | TTS: ${(vTts / 1000).toFixed(1)}k đơn`;
    }
    const gtcBadge = document.querySelector('#tab-gtc-tong .exec-banner-actions span');
    if (gtcBadge) {
      const gF = D.overview?.cards?.find(c => c.id === 'gtc_full')?.val || 0.6087;
      const gT = D.overview?.cards?.find(c => c.id === 'gtc_tts')?.val || 0.6338;
      gtcBadge.textContent = `Full: ${(gF * 100).toFixed(2)}% | TTS: ${(gT * 100).toFixed(2)}% (Target ≥ 60.0%)`;
    }
    const ganBadge = document.querySelector('#tab-gan .exec-banner-actions span');
    if (ganBadge) {
      ganBadge.textContent = `Gán Tổng ${currW}: 86.3% (Target ≥ 90.0%)`;
    }
    const odrBadge = document.querySelector('#tab-odr .exec-banner-actions span');
    if (odrBadge) {
      const oF = D.overview?.cards?.find(c => c.id === 'odr_full')?.val || 0.9312;
      const oT = D.odr?.overview?.find(r => r.label === 'TTS')?.w40 || 0.9418;
      odrBadge.textContent = `ODR Full: ${(oF * 100).toFixed(1)}% | TTS: ${(oT * 100).toFixed(1)}% (Target ≥ 92.0%)`;
    }
    const ltcBadge = document.querySelector('#tab-ltc .exec-banner-actions span');
    if (ltcBadge) {
      const lF = D.overview?.cards?.find(c => c.id === 'ltc_full')?.val || 0.9135;
      const lT = D.ltc?.overview?.find(r => r.label === 'TTS')?.w40 || 0.9497;
      ltcBadge.textContent = `Full: ${(lF * 100).toFixed(1)}% | TTS: ${(lT * 100).toFixed(1)}% (Target ≥ 90.0%)`;
    }
    const oprBadge = document.querySelector('#tab-opr-tts .exec-banner-actions span');
    if (oprBadge) {
      oprBadge.textContent = `OPR TTS ${currW}: 83.5% (Vượt KPI ≥ 80.0%)`;
    }
    const rotBadge = document.getElementById('banner-rot-lc-badge');
    if (rotBadge) {
      const totR = D.rot_lc?.overview?.tot_rot || 219;
      const rateR = D.rot_lc?.overview?.rate_curr ? (D.rot_lc.overview.rate_curr * 100).toFixed(2) : '1.69';
      rotBadge.textContent = `Tổng rớt ${currW}: ${totR} đơn (${rateR}%)`;
    }
    const fdBadge = document.querySelector('#tab-fd .exec-banner-meta span:first-child');
    if (fdBadge) {
      const fR = D.fd?.overview?.rate_fd ? (D.fd.overview.rate_fd * 100).toFixed(2) : '7.77';
      fdBadge.textContent = `Target Toàn Vùng ≤ 6.0% (${currW}: ${fR}%)`;
    }
    const ovSubtitle = document.querySelector('#table-overview-kpi-data')?.closest('.report-card')?.querySelector('.report-card-tools span');
    if (ovSubtitle) {
      ovSubtitle.textContent = `Dữ liệu so sánh ${w1} – ${currW} kèm đường Xu Hướng (Trend)`;
    }"""

app_js = app_js.replace(section15_old, section15_new)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)

print("Part 2: app.js fully updated with dynamic banners and headers!")
