# -*- coding: utf-8 -*-
import os
import sys
import pandas as pd
from datetime import datetime
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

# 1. Load Data
df = pd.read_csv('scratch/sheet1_current.csv')

# Clean AM names
df['AM'] = df['AM'].str.strip()
df['Bưu Cục'] = df['Bưu Cục'].str.strip()
df['currentstatus'] = df['currentstatus'].fillna('unknown').str.strip()

total_orders = len(df)
delivered_count = len(df[df['currentstatus'] == 'delivered'])
delivering_count = len(df[df['currentstatus'] == 'delivering'])
storing_transport = len(df[df['currentstatus'].isin(['storing', 'transporting'])])
fail_return = len(df[df['currentstatus'].isin(['return', 'delivery_fail', 'waiting_to_return', 'return_transporting'])])

gtc_rate = (delivered_count / total_orders * 100) if total_orders > 0 else 0
delivering_rate = (delivering_count / total_orders * 100) if total_orders > 0 else 0
storing_rate = (storing_transport / total_orders * 100) if total_orders > 0 else 0
return_rate = (fail_return / total_orders * 100) if total_orders > 0 else 0

current_reward = delivered_count * 10000
potential_reward = delivering_count * 10000
total_potential = (delivered_count + delivering_count) * 10000

# AM Summary
am_stats = []
for am, grp in df.groupby('AM'):
    tot = len(grp)
    g_del = len(grp[grp['currentstatus'] == 'delivered'])
    g_deli = len(grp[grp['currentstatus'] == 'delivering'])
    g_fail = len(grp[grp['currentstatus'].isin(['return', 'delivery_fail', 'waiting_to_return', 'return_transporting'])])
    g_other = tot - g_del - g_deli - g_fail
    r = (g_del / tot * 100) if tot > 0 else 0
    am_stats.append({
        'AM': am,
        'total': tot,
        'delivered': g_del,
        'delivering': g_deli,
        'fail_return': g_fail,
        'other': g_other,
        'rate': r,
        'reward': g_del * 10000,
        'potential_reward': g_deli * 10000
    })

# Sort AMs by Delivered desc, then Delivering desc, then rate desc
am_stats.sort(key=lambda x: (x['delivered'], x['delivering'], x['rate']), reverse=True)

# Post Offices with highest delivering
bc_stats = []
for (am, bc), grp in df.groupby(['AM', 'Bưu Cục']):
    tot = len(grp)
    g_del = len(grp[grp['currentstatus'] == 'delivered'])
    g_deli = len(grp[grp['currentstatus'] == 'delivering'])
    bc_stats.append({
        'AM': am,
        'bc': bc,
        'total': tot,
        'delivered': g_del,
        'delivering': g_deli,
        'fail_return': tot - g_del - g_deli
    })
bc_stats.sort(key=lambda x: (x['delivering'], x['delivered']), reverse=True)

# Build HTML
html_template = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    * {{
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }}
    
    body {{
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        background: #0b1120;
        color: #f1f5f9;
        padding: 30px;
        width: 1080px;
        margin: 0 auto;
    }}
    
    .card-container {{
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 32px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5), 0 0 40px rgba(249, 115, 22, 0.08);
        position: relative;
        overflow: hidden;
    }}

    .card-container::before {{
        content: '';
        position: absolute;
        top: -150px;
        right: -150px;
        width: 350px;
        height: 350px;
        background: radial-gradient(circle, rgba(249, 115, 22, 0.15) 0%, transparent 70%);
        pointer-events: none;
    }}

    .card-container::after {{
        content: '';
        position: absolute;
        bottom: -150px;
        left: -150px;
        width: 350px;
        height: 350px;
        background: radial-gradient(circle, rgba(16, 185, 129, 0.12) 0%, transparent 70%);
        pointer-events: none;
    }}
    
    .header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        padding-bottom: 24px;
        margin-bottom: 28px;
    }}
    
    .header-left {{
        display: flex;
        flex-direction: column;
        gap: 6px;
    }}
    
    .badge {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 14px;
        background: rgba(249, 115, 22, 0.15);
        color: #fb923c;
        border: 1px solid rgba(249, 115, 22, 0.3);
        border-radius: 9999px;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        width: fit-content;
    }}

    .pulse-dot {{
        width: 8px;
        height: 8px;
        background: #f97316;
        border-radius: 50%;
        box-shadow: 0 0 10px #f97316;
    }}
    
    .title {{
        font-size: 26px;
        font-weight: 800;
        background: linear-gradient(to right, #ffffff, #cbd5e1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.5px;
    }}
    
    .subtitle {{
        font-size: 14px;
        color: #94a3b8;
        font-weight: 500;
    }}

    .header-right {{
        text-align: right;
    }}

    .timestamp-box {{
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 10px 18px;
        border-radius: 14px;
        display: inline-block;
    }}

    .timestamp-label {{
        font-size: 11px;
        text-transform: uppercase;
        color: #64748b;
        font-weight: 700;
        letter-spacing: 0.5px;
    }}

    .timestamp-val {{
        font-size: 15px;
        font-weight: 700;
        color: #38bdf8;
    }}

    /* KPI METRICS */
    .kpi-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin-bottom: 28px;
    }}

    .kpi-card {{
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 18px;
        padding: 18px;
        position: relative;
        overflow: hidden;
    }}

    .kpi-card.green {{
        border-color: rgba(16, 185, 129, 0.3);
        background: linear-gradient(145deg, rgba(16, 185, 129, 0.1) 0%, rgba(15, 23, 42, 0.6) 100%);
    }}

    .kpi-card.orange {{
        border-color: rgba(249, 115, 22, 0.35);
        background: linear-gradient(145deg, rgba(249, 115, 22, 0.12) 0%, rgba(15, 23, 42, 0.6) 100%);
    }}

    .kpi-card.blue {{
        border-color: rgba(56, 189, 248, 0.3);
        background: linear-gradient(145deg, rgba(56, 189, 248, 0.1) 0%, rgba(15, 23, 42, 0.6) 100%);
    }}

    .kpi-label {{
        font-size: 12px;
        font-weight: 700;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}

    .kpi-val {{
        font-size: 32px;
        font-weight: 800;
        line-height: 1.1;
        margin-bottom: 6px;
    }}

    .kpi-val.green {{ color: #10b981; }}
    .kpi-val.orange {{ color: #fb923c; }}
    .kpi-val.blue {{ color: #38bdf8; }}
    .kpi-val.slate {{ color: #cbd5e1; }}

    .kpi-sub {{
        font-size: 12px;
        color: #64748b;
        font-weight: 600;
    }}

    .kpi-sub span {{
        color: #f1f5f9;
        font-weight: 700;
    }}

    /* PROGRESS BAR */
    .progress-section {{
        background: rgba(15, 23, 42, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 16px;
        padding: 16px 20px;
        margin-bottom: 28px;
    }}

    .progress-header {{
        display: flex;
        justify-content: space-between;
        font-size: 13px;
        font-weight: 700;
        margin-bottom: 10px;
    }}

    .progress-bar {{
        height: 14px;
        background: #1e293b;
        border-radius: 9999px;
        overflow: hidden;
        display: flex;
        margin-bottom: 10px;
    }}

    .prog-del {{ background: #10b981; width: {gtc_rate:.1f}%; }}
    .prog-deli {{ background: #f97316; width: {delivering_rate:.1f}%; }}
    .prog-store {{ background: #0284c7; width: {storing_rate:.1f}%; }}
    .prog-fail {{ background: #ef4444; width: {return_rate:.1f}%; }}

    .legend-row {{
        display: flex;
        gap: 20px;
        font-size: 12px;
        font-weight: 600;
    }}

    .legend-item {{
        display: flex;
        align-items: center;
        gap: 6px;
    }}

    .dot {{
        width: 10px;
        height: 10px;
        border-radius: 3px;
    }}
    .dot.green {{ background: #10b981; }}
    .dot.orange {{ background: #f97316; }}
    .dot.blue {{ background: #0284c7; }}
    .dot.red {{ background: #ef4444; }}

    /* TABLES */
    .table-title {{
        font-size: 15px;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }}

    .table-container {{
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        margin-bottom: 26px;
        border-radius: 14px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }}

    .table-container th {{
        background: #1e293b;
        color: #94a3b8;
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        padding: 12px 14px;
        text-align: left;
    }}

    .table-container th.center, .table-container td.center {{
        text-align: center;
    }}

    .table-container th.right, .table-container td.right {{
        text-align: right;
    }}

    .table-container td {{
        background: rgba(15, 23, 42, 0.7);
        border-top: 1px solid rgba(255, 255, 255, 0.04);
        padding: 12px 14px;
        font-size: 13px;
        color: #e2e8f0;
    }}

    .table-container tr:hover td {{
        background: rgba(30, 41, 59, 0.7);
    }}

    .am-name {{
        font-weight: 700;
        color: #f8fafc;
    }}

    .badge-pill {{
        display: inline-block;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 700;
    }}
    .badge-pill.green {{ background: rgba(16, 185, 129, 0.2); color: #34d399; }}
    .badge-pill.orange {{ background: rgba(249, 115, 22, 0.2); color: #fb923c; }}
    .badge-pill.slate {{ background: rgba(148, 163, 184, 0.15); color: #94a3b8; }}

    .rate-bar-bg {{
        width: 90px;
        height: 6px;
        background: #334155;
        border-radius: 9999px;
        display: inline-block;
        vertical-align: middle;
        margin-right: 8px;
        overflow: hidden;
    }}
    .rate-bar-fill {{
        height: 100%;
        background: linear-gradient(90deg, #10b981, #34d399);
        border-radius: 9999px;
    }}

    /* FOOTER */
    .footer {{
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        padding-top: 18px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 12px;
        color: #64748b;
    }}

    .footer-highlight {{
        color: #fb923c;
        font-weight: 700;
    }}
</style>
</head>
<body>

<div class="card-container">
    <!-- Header -->
    <div class="header">
        <div class="header-left">
            <div class="badge">
                <div class="pulse-dot"></div>
                CHƯƠNG TRÌNH THƯỞNG 10K/ĐƠN TTS
            </div>
            <div class="title">BÁO CÁO TIẾN ĐỘ XỬ LÝ & TỶ LỆ GIAO THÀNH CÔNG</div>
            <div class="subtitle">Đánh giá tiến độ xử lý 72 đơn TTS quá hạn theo AM & Bưu cục - Vùng Nam Trung Bộ</div>
        </div>
        <div class="header-right">
            <div class="timestamp-box">
                <div class="timestamp-label">Cập nhật lúc</div>
                <div class="timestamp-val">{datetime.now().strftime('%H:%M - %d/%m/%Y')}</div>
            </div>
        </div>
    </div>

    <!-- KPI Grid -->
    <div class="kpi-grid">
        <div class="kpi-card blue">
            <div class="kpi-label">Tổng đơn push hồi sáng</div>
            <div class="kpi-val blue">{total_orders}</div>
            <div class="kpi-sub">Phân bổ <span>9 AM</span> (18 bưu cục)</div>
        </div>
        <div class="kpi-card green">
            <div class="kpi-label">Đã Giao Thành Công (GTC)</div>
            <div class="kpi-val green">{delivered_count} <span style="font-size: 18px; font-weight: 700;">({gtc_rate:.1f}%)</span></div>
            <div class="kpi-sub">Thưởng đạt: <span style="color:#10b981; font-weight:800;">{current_reward:,.0f}đ</span></div>
        </div>
        <div class="kpi-card orange">
            <div class="kpi-label">Đang Đi Giao (Delivering)</div>
            <div class="kpi-val orange">{delivering_count} <span style="font-size: 18px; font-weight: 700;">({delivering_rate:.1f}%)</span></div>
            <div class="kpi-sub">Tiềm năng thưởng thêm: <span style="color:#fb923c; font-weight:800;">+{potential_reward:,.0f}đ</span></div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Tồn kho / Trả / Chuyển hoàn</div>
            <div class="kpi-val slate">{storing_transport + fail_return} <span style="font-size: 18px; font-weight: 700;">({((storing_transport + fail_return)/total_orders*100):.1f}%)</span></div>
            <div class="kpi-sub">Hoàn: <span>{fail_return}</span> | Lưu kho: <span>{storing_transport}</span></div>
        </div>
    </div>

    <!-- Progress Breakdown Bar -->
    <div class="progress-section">
        <div class="progress-header">
            <span>CƠ CẤU TRẠNG THÁI HIỆN TẠI TRƯỚC MỐC 18H</span>
            <span style="color: #fb923c;">Mục tiêu: Đẩy toàn bộ {delivering_count} đơn đang giao thành GTC trước 18h00!</span>
        </div>
        <div class="progress-bar">
            <div class="prog-del"></div>
            <div class="prog-deli"></div>
            <div class="prog-store"></div>
            <div class="prog-fail"></div>
        </div>
        <div class="legend-row">
            <div class="legend-item"><div class="dot green"></div> Đã GTC: {delivered_count} ({gtc_rate:.1f}%)</div>
            <div class="legend-item"><div class="dot orange"></div> Đang giao (Push gấp): {delivering_count} ({delivering_rate:.1f}%)</div>
            <div class="legend-item"><div class="dot blue"></div> Lưu kho/Luân chuyển: {storing_transport} ({storing_rate:.1f}%)</div>
            <div class="legend-item"><div class="dot red"></div> Trả / Giao thất bại: {fail_return} ({return_rate:.1f}%)</div>
        </div>
    </div>

    <!-- Table 1: AM Ranking -->
    <div class="table-title">
        <span>🏆 BẢNG THEO DÕI TIẾN ĐỘ THEO TỪNG QUẢN LÝ AM</span>
    </div>
    <table class="table-container">
        <thead>
            <tr>
                <th style="width: 50px;" class="center">#</th>
                <th>Quản lý AM</th>
                <th class="center">Tổng đơn</th>
                <th class="center">Đã GTC (Thưởng 10k)</th>
                <th class="center">Đang Đi Giao</th>
                <th class="center">Thất bại / Hoàn</th>
                <th class="right">Tỷ lệ GTC</th>
                <th class="right">Thưởng Hiện Tại</th>
            </tr>
        </thead>
        <tbody>
"""

for idx, am in enumerate(am_stats, 1):
    html_template += f"""
            <tr>
                <td class="center" style="font-weight: 700; color: #64748b;">{idx}</td>
                <td class="am-name">{am['AM']}</td>
                <td class="center" style="font-weight: 700;">{am['total']}</td>
                <td class="center"><span class="badge-pill green">{am['delivered']}</span></td>
                <td class="center"><span class="badge-pill orange">{am['delivering']}</span></td>
                <td class="center"><span class="badge-pill slate">{am['fail_return'] + am['other']}</span></td>
                <td class="right">
                    <div class="rate-bar-bg"><div class="rate-bar-fill" style="width: {am['rate']}%;"></div></div>
                    <span style="font-weight: 700; color: #34d399;">{am['rate']:.1f}%</span>
                </td>
                <td class="right" style="font-weight: 800; color: #10b981;">{am['reward']:,.0f}đ</td>
            </tr>
    """

html_template += """
        </tbody>
    </table>

    <!-- Table 2: Top post offices with pending deliveries -->
    <div class="table-title">
        <span>⚡ TOP BƯU CỤC CẦN ĐÔN ĐỐC GẤP TRƯỚC 18H (CÒN ĐƠN ĐANG ĐI GIAO)</span>
    </div>
    <table class="table-container" style="margin-bottom: 10px;">
        <thead>
            <tr>
                <th>Bưu Cục</th>
                <th>AM Phụ Trách</th>
                <th class="center">Tổng đơn</th>
                <th class="center">Đang Đi Giao (Cần GTC)</th>
                <th class="center">Đã GTC</th>
                <th class="right">Tiềm năng thưởng thêm</th>
            </tr>
        </thead>
        <tbody>
"""

# Filter only BCs that have delivering orders > 0
top_delivering_bcs = [b for b in bc_stats if b['delivering'] > 0]
for b in top_delivering_bcs:
    html_template += f"""
            <tr>
                <td style="font-weight: 700; color: #f1f5f9;">{b['bc']}</td>
                <td style="color: #94a3b8;">{b['AM']}</td>
                <td class="center" style="font-weight: 700;">{b['total']}</td>
                <td class="center"><span class="badge-pill orange" style="font-size: 13px;">{b['delivering']} đơn</span></td>
                <td class="center"><span class="badge-pill green">{b['delivered']} đơn</span></td>
                <td class="right" style="font-weight: 800; color: #fb923c;">+{b['delivering'] * 10000:,.0f}đ</td>
            </tr>
    """

html_template += f"""
        </tbody>
    </table>

    <!-- Footer -->
    <div class="footer">
        <div>Hệ thống giám sát vận hành NTB - Tự động trích xuất từ Google Sheet</div>
        <div>Mỗi đơn GTC trước 18h00 được thưởng <span class="footer-highlight">10.000đ/đơn</span>. Hạn chót chốt thưởng: <span class="footer-highlight">18:00 Hôm nay</span>.</div>
    </div>
</div>

</body>
</html>
"""

# Save HTML
html_file = os.path.join(os.getcwd(), 'scratch/bao_cao_gtc_15h.html')
img_file = os.path.join(os.getcwd(), 'scratch/bao_cao_gtc_15h.png')

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html_template)

print(f"HTML saved to {html_file}")

# Render to Image using Playwright
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1140, "height": 1200})
    page.goto(f"file:///{os.path.abspath(html_file)}")
    page.wait_for_timeout(500)
    page.screenshot(path=img_file, full_page=True)
    browser.close()

print(f"Image successfully generated: {img_file}")
