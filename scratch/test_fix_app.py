# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

# Let's inspect renderAgingCustomerChart
start_marker = "function renderAgingCustomerChart() {"
end_marker = "function renderAgingChart() {"

p1 = app_js.find(start_marker)
p2 = app_js.find(end_marker)

print(f"p1={p1}, p2={p2}")

# Let's replace the broken renderAgingCustomerChart with a clean stub or proper implementation first
stub = """function renderAgingCustomerChart() {
    const ctx = document.getElementById('chart-aging-customer');
    if (!ctx) return;
    if (charts.agingCustomer) charts.agingCustomer.destroy();

    const seg = state.agingSegment || 'aging';
    const isAging = seg === 'aging';
    const isTreo = seg === 'treo_lc';

    const custTitle = document.getElementById('aging-cust-title');
    const custBadge = document.getElementById('aging-cust-badge');
    const custSummary = document.getElementById('aging-cust-summary-grid');

    if (isAging && D.aging) {
      const custData = D.aging.by_customer || [];
      const top1 = custData[0] || { customer: 'SME', vol: 619, pct: 80.8 };

      if (custTitle) custTitle.textContent = 'PHÂN TÍCH TỒN ĐỌNG CẢ VÙNG THEO KHÁCH HÀNG (AGING >5 NGÀY)';
      if (custBadge) {
        custBadge.className = 'badge-tag badge-tag-red';
        custBadge.textContent = `🚨 ${top1.customer} Tồn Nhiều Nhất (${top1.pct}% - ${fNum(top1.vol)} đơn)`;
      }

      let sme = { vol: 0, d58: 0, d815: 0, gt15: 0, top_am: '', top_bc: '', pct: 0 };
      let tts = { vol: 0, d58: 0, d815: 0, gt15: 0, top_am: '', top_bc: '', pct: 0 };
      let shp = { vol: 0, d58: 0, d815: 0, gt15: 0, top_am: '', top_bc: '', pct: 0 };

      custData.forEach(c => {
        const name = (c.customer || '').toUpperCase();
        if (name.includes('SME')) {
          sme.vol += c.vol || 0;
          sme.d58 += c.d_5_8 || 0;
          sme.d815 += c.d_8_15 || 0;
          sme.gt15 += c.gt_15 || 0;
          if (!sme.top_am) sme.top_am = c.top_am;
          if (!sme.top_bc) sme.top_bc = c.top_bc;
        } else if (name.includes('TTS')) {
          tts.vol += c.vol || 0;
          tts.d58 += c.d_5_8 || 0;
          tts.d815 += c.d_8_15 || 0;
          tts.gt15 += c.gt_15 || 0;
          if (!tts.top_am) tts.top_am = c.top_am;
          if (!tts.top_bc) tts.top_bc = c.top_bc;
        } else if (name.includes('SHOPEE')) {
          shp.vol += c.vol || 0;
          shp.d58 += c.d_5_8 || 0;
          shp.d815 += c.d_8_15 || 0;
          shp.gt15 += c.gt_15 || 0;
          if (!shp.top_am) shp.top_am = c.top_am;
          if (!shp.top_bc) shp.top_bc = c.top_bc;
        }
      });
      const totAg = D.aging.total || 766;
      sme.pct = (sme.vol / totAg * 100).toFixed(1);
      tts.pct = (tts.vol / totAg * 100).toFixed(1);
      shp.pct = (shp.vol / totAg * 100).toFixed(1);

      const labels = [
        `1. SME (${fNum(sme.vol)} đ - ${sme.pct}%)`,
        `2. TikTok Shop (${fNum(tts.vol)} đ - ${tts.pct}%)`,
        `3. Shopee (${fNum(shp.vol)} đ - ${shp.pct}%)`
      ];

      charts.agingCustomer = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [
            {
              label: '5 – 8 ngày',
              data: [sme.d58, tts.d58, shp.d58],
              backgroundColor: '#3b82f6',
              borderRadius: 3
            },
            {
              label: '8 – 15 ngày',
              data: [sme.d815, tts.d815, shp.d815],
              backgroundColor: '#f59e0b',
              borderRadius: 3
            },
            {
              label: 'Trên 15 ngày',
              data: [sme.gt15, tts.gt15, shp.gt15],
              backgroundColor: '#dc2626',
              borderRadius: 3
            }
          ]
        },
        options: {
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              stacked: true,
              grid: { color: 'rgba(0,0,0,0.05)' },
              ticks: { font: { size: 10 } }
            },
            y: {
              stacked: true,
              grid: { display: false },
              ticks: { font: { size: 11, weight: 'bold' }, color: 'var(--text-main)' }
            }
          },
          plugins: {
            legend: {
              position: 'top',
              labels: { boxWidth: 10, font: { size: 10 }, padding: 6 }
            },
            tooltip: {
              callbacks: {
                afterBody: function(context) {
                  const idx = context[0].dataIndex;
                  if (idx === 0) return `Top AM: ${sme.top_am}\\nTop BC: ${sme.top_bc}\\n(Nắm 100% số đơn tồn >15N của cả vùng)`;
                  if (idx === 1) return `Top AM: ${tts.top_am}\\nTop BC: ${tts.top_bc}\\n(81/89 đơn ở mức 5-8N, 0 đơn >15N)`;
                  if (idx === 2) return `Top AM: ${shp.top_am}\\nTop BC: ${shp.top_bc}\\n(Gồm 16 đơn hàng Bulky cồng kềnh)`;
                }
              }
            }
          }
        }
      });

      if (custSummary) {
        custSummary.innerHTML = `
          <div style="padding: 6px 10px; background: rgba(239, 68, 68, 0.08); border: 1.5px solid #ef4444; border-radius: 6px;">
            <div style="font-size: 10.5px; font-weight: 800; color: #b91c1c;">👑 TOP 1: SME (${sme.pct}%)</div>
            <div style="font-size: 14px; font-weight: 900; color: #dc2626; line-height: 1.2;">${fNum(sme.vol)} <small style="font-size: 10px;">đơn tồn</small></div>
            <div style="font-size: 10px; color: var(--text-muted); margin-top: 2px;">Giữ <strong>100%</strong> đơn &gt;15N (${sme.gt15} đ). AM: ${sme.top_am || 'Lê Minh Đại'}</div>
          </div>
          <div style="padding: 6px 10px; background: rgba(59, 130, 246, 0.08); border: 1.5px solid #3b82f6; border-radius: 6px;">
            <div style="font-size: 10.5px; font-weight: 800; color: #1d4ed8;">TOP 2: TIKTOK SHOP (${tts.pct}%)</div>
            <div style="font-size: 14px; font-weight: 900; color: #2563eb; line-height: 1.2;">${fNum(tts.vol)} <small style="font-size: 10px;">đơn tồn</small></div>
            <div style="font-size: 10px; color: var(--text-muted); margin-top: 2px;">91% là 5–8N (${tts.d58} đ). AM: ${tts.top_am || 'Nguyễn Duy Long'}</div>
          </div>
          <div style="padding: 6px 10px; background: rgba(249, 115, 22, 0.08); border: 1.5px solid #f97316; border-radius: 6px;">
            <div style="font-size: 10.5px; font-weight: 800; color: #c2410c;">TOP 3: SHOPEE (${shp.pct}%)</div>
            <div style="font-size: 14px; font-weight: 900; color: #ea580c; line-height: 1.2;">${fNum(shp.vol)} <small style="font-size: 10px;">đơn tồn</small></div>
            <div style="font-size: 10px; color: var(--text-muted); margin-top: 2px;">16 đ Bulky (28%). AM: ${shp.top_am || 'Nguyễn Duy Long'}</div>
          </div>
        `;
      }
    } else if (isTreo && D.treo_lc) {
      const custData = D.treo_lc.by_customer || [];
      const top1 = custData[0] || { customer: 'SME / Khác (OTHER)', vol: 2178, pct: 57.5 };
      const shpCust = custData.find(c => (c.customer || '').includes('Shopee')) || {};

      if (custTitle) custTitle.textContent = 'PHÂN TÍCH TREO LUÂN CHUYỂN CẢ VÙNG THEO KHÁCH HÀNG';
      if (custBadge) {
        custBadge.className = 'badge-tag badge-tag-amber';
        custBadge.textContent = `🚨 ${top1.customer} Tồn Nhiều Nhất (${top1.pct}%) | Shopee Treo Cao Nhất (${shpCust.rate_treo_24 || '24.9'}%)`;
      }

      const labels = custData.map((c, idx) => `${idx + 1}. ${c.customer} (${fNum(c.vol)} đ - ${c.pct}%)`);
      const dataU24 = custData.map(c => c.u_24 || 0);
      const data24_36 = custData.map(c => c.h_24_36 || 0);
      const data36_plus = custData.map(c => (c.treo_24 || 0) - (c.h_24_36 || 0));

      charts.agingCustomer = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [
            {
              label: '< 24h (Đúng hạn)',
              data: dataU24,
              backgroundColor: '#10b981',
              borderRadius: 3
            },
            {
              label: '24 – 36h (Bắt đầu trễ)',
              data: data24_36,
              backgroundColor: '#f59e0b',
              borderRadius: 3
            },
            {
              label: '≥ 36h (Trễ nặng)',
              data: data36_plus,
              backgroundColor: '#dc2626',
              borderRadius: 3
            }
          ]
        },
        options: {
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              stacked: true,
              grid: { color: 'rgba(0,0,0,0.05)' },
              ticks: { font: { size: 10 } }
            },
            y: {
              stacked: true,
              grid: { display: false },
              ticks: { font: { size: 11, weight: 'bold' }, color: 'var(--text-main)' }
            }
          },
          plugins: {
            legend: {
              position: 'top',
              labels: { boxWidth: 10, font: { size: 10 }, padding: 6 }
            },
            tooltip: {
              callbacks: {
                afterBody: function(context) {
                  const idx = context[0].dataIndex;
                  const item = custData[idx] || {};
                  return `Treo ≥24h: ${fNum(item.treo_24)} đơn (${item.rate_treo_24}%)\\nChiếm ${item.pct}% tổng đơn treo cả vùng\\nTop AM: ${item.top_am || ''} (${fNum(item.top_am_vol)} đ)\\nTop BC: ${item.top_bc || ''}`;
                }
              }
            }
          }
        }
      });

      if (custSummary) {
        const other = custData[0] || {};
        const shopee = custData[1] || {};
        const tts = custData[2] || {};
        custSummary.innerHTML = `
          <div style="padding: 6px 10px; background: rgba(59, 130, 246, 0.08); border: 1.5px solid #3b82f6; border-radius: 6px;">
            <div style="font-size: 10.5px; font-weight: 800; color: #1d4ed8;">👑 TOP 1: OTHER / SME (${other.pct || '57.5'}%)</div>
            <div style="font-size: 14px; font-weight: 900; color: #2563eb; line-height: 1.2;">${fNum(other.vol || 2178)} <small style="font-size: 10px;">đơn LC</small></div>
            <div style="font-size: 10px; color: var(--text-muted); margin-top: 2px;">Treo ≥24h: <strong>${fNum(other.treo_24 || 356)} đ (${other.rate_treo_24 || '16.3'}%)</strong>. AM: ${other.top_am || 'Nguyễn Duy Long'}</div>
          </div>
          <div style="padding: 6px 10px; background: rgba(239, 68, 68, 0.08); border: 1.5px solid #ef4444; border-radius: 6px;">
            <div style="font-size: 10.5px; font-weight: 800; color: #b91c1c;">🚨 SHOPEE: TREO CAO NHẤT (${shopee.rate_treo_24 || '24.9'}%)</div>
            <div style="font-size: 14px; font-weight: 900; color: #dc2626; line-height: 1.2;">${fNum(shopee.treo_24 || 254)} / ${fNum(shopee.vol || 1019)} <small style="font-size: 10px;">treo</small></div>
            <div style="font-size: 10px; color: var(--text-muted); margin-top: 2px;">Chiếm <strong>${shopee.pct || '26.9'}%</strong> tổng treo cả vùng! AM: ${shopee.top_am || 'Trần Văn Phước'}</div>
          </div>
          <div style="padding: 6px 10px; background: rgba(16, 185, 129, 0.08); border: 1.5px solid #10b981; border-radius: 6px;">
            <div style="font-size: 10.5px; font-weight: 800; color: #047857;">TIKTOK SHOP (${tts.pct || '15.6'}%)</div>
            <div style="font-size: 14px; font-weight: 900; color: #059669; line-height: 1.2;">${fNum(tts.vol || 591)} <small style="font-size: 10px;">đơn LC</small></div>
            <div style="font-size: 10px; color: var(--text-muted); margin-top: 2px;">Treo ≥24h: <strong>${fNum(tts.treo_24 || 78)} đ (${tts.rate_treo_24 || '13.2'}%)</strong>. AM: ${tts.top_am || 'Nguyễn Duy Long'}</div>
          </div>
        `;
      }
    }
  }

  """

test_code = app_js[:p1] + stub + app_js[p2:]

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    res = page.evaluate("""(code) => {
        try {
            new Function(code);
            return { ok: true };
        } catch (e) {
            return { ok: false, msg: e.message, stack: e.stack };
        }
    }""", test_code)
    print("Testing with replaced function:", res)
    browser.close()
