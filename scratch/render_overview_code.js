function renderOverviewTab() {
    const ov = D.overview || {};
    const tilesEl = document.getElementById('overview-kpi-tiles');
    const latestWeek = D.meta?.latest_week || 'W37';
    const prevWeek = D.meta?.prev_week || 'W36';
    
    if (tilesEl) {
      const cardMap = {};
      (ov.cards || []).forEach(c => cardMap[c.id] = c);

      const trendMap = {};
      (ov.kpis_trend || []).forEach(t => trendMap[t.indicator] = t);

      // 1. Sản lượng Full & TTS
      const volCard = cardMap['vol_full'] || {};
      const volTtsCard = cardMap['vol_tts'] || {};
      const volVal = volCard.val || 307837;
      const volDiff = volCard.diff !== undefined ? volCard.diff : -11149;
      const volTtsVal = volTtsCard.val || 63122;
      const volTtsDiff = volTtsCard.diff !== undefined ? volTtsCard.diff : -9759;
      const volDiffPct = volCard.diff_pct !== undefined ? volCard.diff_pct : -0.035;
      const volTtsDiffPct = volTtsCard.diff_pct !== undefined ? volTtsCard.diff_pct : -0.134;

      // 2. GTC Tổng
      const gtcCard = cardMap['gtc_full'] || {};
      const gtcTtsCard = cardMap['gtc_tts'] || {};
      const gtcVal = gtcCard.val !== undefined ? gtcCard.val : 0.5778;
      const gtcDiff = gtcCard.diff !== undefined ? gtcCard.diff : -0.0036;
      const gtcTtsVal = gtcTtsCard.val !== undefined ? gtcTtsCard.val : 0.5591;
      const gtcTtsDiff = gtcTtsCard.diff !== undefined ? gtcTtsCard.diff : -0.0104;

      // 3. GTC Ca 1 TTS
      const gtcCa1Trend = trendMap['%GTC TTS (Ca1 thuần)'] || trendMap['%GTC Full hàng (Ca1 thuần)'] || {};
      const gtcCa1Val = gtcCa1Trend[latestWeek.toLowerCase()] !== undefined ? gtcCa1Trend[latestWeek.toLowerCase()] : 0.7307;
      const gtcCa1Diff = gtcCa1Trend.diff !== undefined ? gtcCa1Trend.diff : -0.0171;

      // 4. Gán vận hành
      const ganOverview = D.gan?.overview || [];
      const ganFullRow = ganOverview.find(r => r.indicator && r.indicator.includes('Full hàng – Tổng')) || {};
      const ganTtsRow = ganOverview.find(r => r.indicator && r.indicator.includes('TTS – Tổng')) || {};
      const ganVal = ganFullRow[latestWeek.toLowerCase()] !== undefined ? ganFullRow[latestWeek.toLowerCase()] : (ganFullRow.w37 || ganFullRow.w36 || 0.8355);
      const ganDiff = ganFullRow.diff !== undefined ? ganFullRow.diff : 0.0144;
      const ganTtsVal = ganTtsRow[latestWeek.toLowerCase()] !== undefined ? ganTtsRow[latestWeek.toLowerCase()] : (ganTtsRow.w37 || ganTtsRow.w36 || 0.8343);
      const ganTtsDiff = ganTtsRow.diff !== undefined ? ganTtsRow.diff : 0.0142;

                  // 5. ODR
      const odrOverview = D.odr?.overview || [];
      const odrFullRow = odrOverview.find(r => r.label === 'Full hàng') || {};
      const odrTtsRow = odrOverview.find(r => r.label === 'TTS') || {};
      const odrCard = cardMap['odr_full'] || {};
      const odrTrendFull = trendMap['%ODR Full hàng'] || {};
      const odrTrendTts = trendMap['%ODR TTS'] || {};
      const odrVal = odrCard.val !== undefined ? odrCard.val : (odrFullRow[latestWeek.toLowerCase()] !== undefined ? odrFullRow[latestWeek.toLowerCase()] : 0.9124);
      const odrDiff = odrCard.diff !== undefined ? odrCard.diff : (odrTrendFull.diff !== undefined ? odrTrendFull.diff : -0.0210);
      const odrTtsVal = odrTrendTts[latestWeek.toLowerCase()] !== undefined ? odrTrendTts[latestWeek.toLowerCase()] : (odrTtsRow[latestWeek.toLowerCase()] !== undefined ? odrTtsRow[latestWeek.toLowerCase()] : 0.9154);
      const odrTtsDiff = odrTrendTts.diff !== undefined ? odrTrendTts.diff : (odrTtsRow.diff !== undefined ? odrTtsRow.diff : -0.0131);

      // 6. LTC
      const ltcCard = cardMap['ltc_full'] || {};
      const ltcTrendTts = trendMap['%LTC TTS'] || {};
      const ltcVal = ltcCard.val !== undefined ? ltcCard.val : 0.9029;
      const ltcDiff = ltcCard.diff !== undefined ? ltcCard.diff : -0.0021;
      const ltcTtsVal = ltcTrendTts[latestWeek.toLowerCase()] !== undefined ? ltcTrendTts[latestWeek.toLowerCase()] : 0.9355;
      const ltcTtsDiff = ltcTrendTts.diff !== undefined ? ltcTrendTts.diff : -0.0064;

      // 7. Rớt LC
      const rotCard = cardMap['rot_lc'] || {};
      const rotVal = rotCard.val !== undefined ? rotCard.val : 0.0225;
      const rotDiff = rotCard.diff !== undefined ? rotCard.diff : 0.0068;

      // 8. COD Tiền mặt & Thanh toán QR
      const codCard = cardMap['cod_tm'] || {};
      const codReportMetrics = D.cod_report?.metrics || [];
      const codTmRow = codReportMetrics.find(m => m.chi_so && m.chi_so.includes('Tiền mặt (% TM)')) || {};
      const codCkRow = codReportMetrics.find(m => m.chi_so && m.chi_so.includes('Chuyển khoản (% CK)')) || {};
      const codTotRow = codReportMetrics.find(m => m.chi_so && m.chi_so.includes('Tổng COD')) || {};
      
      let codVal = 0.371;
      let codPrev = 0.401;
      let codDiff = -0.030;
      let codDigitalVal = 0.629;
      let codTotStr = '82.6 Tỷ';

      if (codTmRow.curr) {
        codVal = parseFloat(codTmRow.curr.replace('%', '')) / 100;
        if (codTmRow.prev) codPrev = parseFloat(codTmRow.prev.replace('%', '')) / 100;
        codDiff = codVal - codPrev;
        codDigitalVal = 1 - codVal;
      } else if (codCard.val !== undefined) {
        codVal = codCard.val;
        codDiff = codCard.diff !== undefined ? codCard.diff : -0.030;
        codPrev = codVal - codDiff;
        codDigitalVal = 1 - codVal;
      } else if (D.cod_payment?.overview?.rate_cash !== undefined) {
        codVal = D.cod_payment.overview.rate_cash;
        codDiff = D.cod_payment.overview.diff_cash || -0.024;
        codPrev = codVal - codDiff;
        codDigitalVal = 1 - codVal;
      }
      if (codTotRow.curr) {
        const numTot = parseFloat(codTotRow.curr.replace(/,/g, ''));
        if (!isNaN(numTot)) codTotStr = (numTot / 1000).toFixed(1) + ' Tỷ';
      }

      // 9. FD Hoàn Trả (Failed Delivery)
      const fdData = D.fd || {};
      const fdSum = fdData.summary || {};
      const fdRateFull = fdSum.rate_full !== undefined ? fdSum.rate_full : 0.0673;
      const fdRateFullPrev = fdSum.rate_full_prev !== undefined ? fdSum.rate_full_prev : 0.0754;
      const fdRateTts = fdSum.rate_tts !== undefined ? fdSum.rate_tts : 0.0610;
      const fdRateTtsPrev = fdSum.rate_tts_prev !== undefined ? fdSum.rate_tts_prev : 0.0680;
      const fdRetFull = fdSum.ret_full || 24518;
      const fdDiffFull = fdSum.diff_full !== undefined ? fdSum.diff_full : (fdRateFull - fdRateFullPrev);
      const fdDiffTts = fdSum.diff_tts !== undefined ? fdSum.diff_tts : (fdRateTts - fdRateTtsPrev);

      // 10. TLTĐ (Tỷ Lệ Lấp Đầy Thùng/Xe KTC)
      const ktcData = D.ktc || {};
      const ktcWeekly = ktcData.fill_rate?.weekly?.total || {};
      const tltdVal = (ktcWeekly.tld_curr !== undefined ? ktcWeekly.tld_curr : (ktcWeekly['tld_' + latestWeek.toLowerCase()] || 51.0)) / 100;
      const tltdPrev = (ktcWeekly.tld_prev !== undefined ? ktcWeekly.tld_prev : (ktcWeekly['tld_' + prevWeek.toLowerCase()] || 54.8)) / 100;
      const tltdDiff = ktcWeekly.diff_tld !== undefined ? (ktcWeekly.diff_tld / 100) : (tltdVal - tltdPrev);
      const tltdUnder30 = ktcWeekly.under_30 !== undefined ? ktcWeekly.under_30 : 76;

      const pairedCards = [
        {
          id: 'vol_pair',
          title: `Sản Lượng Giao (${latestWeek})`,
          mainVal: fNum(volVal),
          mainUnit: `đơn Full (${volDiff >= 0 ? '▲ +' : '▼ '}${fNum(volDiff)} đ)`,
          subVal: `TTS: ${fNum(volTtsVal)} đ (${volTtsDiff >= 0 ? '▲ +' : '▼ '}${fNum(volTtsDiff)} đ / ${fPct(volTtsDiffPct)})`,
          diff: volDiffPct,
          isHigherBetter: true,
          colorCls: 'kpi-blue',
          icon: 'package'
        },
        {
          id: 'gtc_pair',
          title: `%GTC Tổng (${latestWeek})`,
          mainVal: fPct(gtcVal),
          mainUnit: `Full Hàng (${gtcDiff >= 0 ? '▲ +' : '▼ '}${(Math.abs(gtcDiff)*100).toFixed(1)}%p)`,
          subVal: `TTS: ${fPct(gtcTtsVal)} (${gtcTtsDiff >= 0 ? '▲ +' : '▼ '}${(Math.abs(gtcTtsDiff)*100).toFixed(1)}%p)`,
          diff: gtcDiff,
          isHigherBetter: true,
          colorCls: 'kpi-amber',
          icon: 'check-circle-2'
        },
        {
          id: 'gtc_ca1_pair',
          title: `%GTC TTS Ca 1 (${latestWeek})`,
          mainVal: fPct(gtcCa1Val),
          mainUnit: 'TikTok Shop',
          subVal: 'Target ≥ 76.0%',
          diff: gtcCa1Diff,
          isHigherBetter: true,
          colorCls: 'kpi-purple',
          icon: 'award'
        },
        {
          id: 'gan_pair',
          title: `Tỷ Lệ Gán Vận Hành (${latestWeek})`,
          mainVal: fPct(ganVal),
          mainUnit: `Full Hàng (${ganDiff >= 0 ? '▲ +' : '▼ '}${(Math.abs(ganDiff)*100).toFixed(1)}%p)`,
          subVal: `Ca 1+Tồn: 89.1% · Ca 2: 57.7% | TTS: ${fPct(ganTtsVal)}`, 
          diff: ganDiff,
          isHigherBetter: true,
          colorCls: 'kpi-purple',
          icon: 'user-check'
        },
        {
          id: 'odr_pair',
          title: `%ODR (Giao Đúng Hẹn SLA - ${latestWeek})`,
          mainVal: fPct(odrVal),
          mainUnit: `Full Hàng (${odrDiff >= 0 ? '▲ +' : '▼ '}${(Math.abs(odrDiff)*100).toFixed(1)}%p)`,
          subVal: `TTS: ${fPct(odrTtsVal)} (${odrTtsDiff >= 0 ? '▲ +' : '▼ '}${(Math.abs(odrTtsDiff)*100).toFixed(1)}%p)`,
          diff: odrDiff,
          isHigherBetter: true,
          colorCls: (odrVal >= 0.92) ? 'kpi-green' : 'kpi-red',
          icon: 'clock'
        },
        {
          id: 'ltc_pair',
          title: `%LTC (Lấy Thành Công - ${latestWeek})`,
          mainVal: fPct(ltcVal),
          mainUnit: `Full Hàng (${ltcDiff >= 0 ? '▲ +' : '▼ '}${(Math.abs(ltcDiff)*100).toFixed(1)}%p)`,
          subVal: `TTS: ${fPct(ltcTtsVal)} (${ltcTtsDiff >= 0 ? '▲ +' : '▼ '}${(Math.abs(ltcTtsDiff)*100).toFixed(1)}%p) | Target ≥ 90.0%`,
          diff: ltcDiff,
          isHigherBetter: true,
          colorCls: 'kpi-green',
          icon: 'archive'
        },
        {
          id: 'rot_lc',
          title: `%Rớt Luân Chuyển (${latestWeek})`,
          mainVal: fPct(rotVal),
          mainUnit: 'Toàn Vùng',
          subVal: `${prevWeek}: ${fPct(rotVal - rotDiff)} (${rotDiff >= 0 ? 'Tăng +' : 'Giảm '}${(Math.abs(rotDiff)*100).toFixed(2)}%p)`,
          diff: rotDiff,
          isHigherBetter: false,
          colorCls: 'kpi-red',
          icon: 'truck'
        },
        {
          id: 'fd_pair',
          title: `%FD Hoàn Trả (${latestWeek})`,
          mainVal: fPct(fdRateFull),
          mainUnit: `Full Hàng (${prevWeek}: ${fPct(fdRateFullPrev)} | ▼ ${(Math.abs(fdDiffFull)*100).toFixed(1)}%p)`,
          subVal: `TTS: ${fPct(fdRateTts)} (${prevWeek}: ${fPct(fdRateTtsPrev)} | ▼ ${(Math.abs(fdDiffTts)*100).toFixed(1)}%p) · ${fNum(fdRetFull)} đ hoàn`,
          diff: fdDiffFull,
          isHigherBetter: false,
          colorCls: 'kpi-purple',
          icon: 'rotate-ccw'
        },
        {
          id: 'opr_pair',
          title: `%OPR TikTok Shop (${latestWeek})`,
          mainVal: '82.2%',
          mainUnit: 'Toàn Vùng (Target ≥ 80.0%)',
          subVal: '☀️ Ngày: 93.5% · 🌙 Đêm: 64.3% 🚨',
          diff: -0.009,
          isHigherBetter: true,
          colorCls: 'kpi-amber',
          icon: 'shopping-bag'
        }
      ];

      tilesEl.innerHTML = pairedCards.map(c => `
        <div class="kpi-tile ${c.colorCls}">
          <div class="kpi-tile-header">
            <span>${c.title}</span>
            <div class="kpi-tile-icon"><i data-lucide="${c.icon}"></i></div>
          </div>
          <div class="kpi-tile-value">
            ${c.mainVal}
            <small>${c.mainUnit}</small>
          </div>
          <div class="kpi-tile-meta">
            <span style="font-size: 11.5px; color: var(--text-muted);">${c.subVal}</span>
            ${renderDeltaBadge(c.diff, c.isHigherBetter !== undefined ? c.isHigherBetter : true, true)}
          </div>
        </div>
      `).join('');

      if (window.lucide) {
        lucide.createIcons();
      }
    }

    // Insights Box
    const insEl = document.getElementById('overview-insights-container');
    if (insEl && ov.insights) {
      insEl.innerHTML = ov.insights.map(item => {
        const title = item.title || (item.text ? item.text.substring(0, 45) + '...' : 'Điểm Nổi Bật');
        const desc = item.desc || item.text || '';
        const isGood = item.type === 'good' || item.type === 'positive' || item.type === 'highlight';
        const isBad = item.type === 'bad' || item.type === 'danger';
        const itemCls = isGood ? 'insight-good' : (isBad ? 'insight-bad' : 'insight-warn');
        const iconName = isGood ? 'check-circle' : (isBad ? 'alert-triangle' : 'info');

        return `
          <div class="insight-item ${itemCls}">
            <div class="insight-icon">
              <i data-lucide="${iconName}"></i>
            </div>
            <div>
              <div class="insight-title">${title}</div>
              <div class="insight-desc">${desc}</div>
            </div>
          </div>
        `;
      }).join('');
    }

    // 4-Week KPI Matrix Table
    const tblBody = document.querySelector('#table-overview-kpi-data tbody');
    if (tblBody && ov.kpis_trend) {
      const groups = [
        {
          name: '1. Sản Lượng Giao (Volume)',
          icon: 'package',
          items: ov.kpis_trend.filter(r => r.indicator.includes('Sản lượng'))
        },
        {
          name: '2. Hiệu Suất Giao Thành Công (%GTC)',
          icon: 'check-circle-2',
          items: ov.kpis_trend.filter(r => r.indicator.includes('%GTC'))
        },
        {
          name: '3. Chất Lượng Vận Hành SLA (%ODR & %LTC)',
          icon: 'clock',
          items: ov.kpis_trend.filter(r => r.indicator.includes('ODR') || r.indicator.includes('LTC'))
        },
        {
          name: '4. Vận Tải & Kiểm Soát Rủi Ro',
          icon: 'truck',
          items: ov.kpis_trend.filter(r => r.indicator.includes('Rớt') || r.indicator.includes('COD'))
        }
      ];

      let html = '';
      groups.forEach(grp => {
        if (grp.items.length === 0) return;
        html += `
          <tr class="tr-category-header">
            <td colspan="8">
              <span class="category-pill"><i data-lucide="${grp.icon}"></i> ${grp.name}</span>
            </td>
          </tr>
        `;

        grp.items.forEach(row => {
          const isPct = row.type === 'percent';
          const wKeys = (D.meta?.weeks || ['W34', 'W35', 'W36', 'W37']).map(w => w.toLowerCase());
          const val1 = row[wKeys[0]] !== undefined ? row[wKeys[0]] : (row.w34 || 0);
          const val2 = row[wKeys[1]] !== undefined ? row[wKeys[1]] : (row.w35 || 0);
          const val3 = row[wKeys[2]] !== undefined ? row[wKeys[2]] : (row.w36 || 0);
          const val4 = row[wKeys[3]] !== undefined ? row[wKeys[3]] : (row.w37 !== undefined ? row.w37 : (row.vol || 0));

          const w_col1 = isPct ? fPct(val1) : fNum(val1);
          const w_col2 = isPct ? fPct(val2) : fNum(val2);
          const w_col3 = isPct ? fPct(val3) : fNum(val3);
          const w_col4 = isPct ? fPct(val4) : fNum(val4);

          const isHigherBetter = !row.indicator.includes('Rớt') && !row.indicator.includes('COD');
          const diffBadge = renderDeltaBadge(row.diff, isHigherBetter, isPct);

          const isTts = row.indicator.includes('TTS');
          const scopeTag = isTts
            ? '<span class="tag-scope-tts">⚡ TTS</span>'
            : '<span class="tag-scope-full">📦 Full Hàng</span>';

          let heatType = '';
          if (row.indicator.includes('GTC')) heatType = 'gtc';
          else if (row.indicator.includes('ODR')) heatType = 'odr';
          else if (row.indicator.includes('LTC')) heatType = 'ltc';
          else if (row.indicator.includes('Rớt')) heatType = 'rot_lc';
          else if (row.indicator.includes('COD')) heatType = 'cod_tm';

          const heatClassW = heatType ? getHeatmapClass(val4, heatType) : '';
          const trendVisual = renderMicroTrendVisual(val1, val2, val3, val4, isHigherBetter, isPct);

          html += `
            <tr>
              <td class="bold" style="font-size: 13px;">${row.indicator}</td>
              <td class="center">${scopeTag}</td>
              <td class="num">${w_col1}</td>
              <td class="num">${w_col2}</td>
              <td class="num">${w_col3}</td>
              <td class="num bold ${heatClassW}">${w_col4}</td>
              <td class="num">${diffBadge}</td>
              <td class="center">${trendVisual}</td>
            </tr>
          `;
        });
      });

      tblBody.innerHTML = html;
    }
  }