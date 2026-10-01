# -*- coding: utf-8 -*-
import os
import sys
import pandas as pd
from datetime import datetime
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_csv('scratch/sheet1_today.csv')

df['AM'] = df['AM'].str.strip()
df['Bưu Cục'] = df['Bưu Cục'].str.strip()
df['currentstatus'] = df['currentstatus'].fillna('unknown').astype(str).str.strip().str.lower()

total_orders = len(df)
delivered_count = len(df[df['currentstatus'] == 'delivered'])
delivering_count = len(df[df['currentstatus'] == 'delivering'])
storing_count = len(df[df['currentstatus'] == 'storing'])
return_count = len(df[df['currentstatus'].isin(['return', 'return_transporting'])])
other_count = total_orders - delivered_count - delivering_count - storing_count - return_count

gtc_rate = (delivered_count / total_orders * 100) if total_orders > 0 else 0
current_reward = delivered_count * 10000
potential_pending = (total_orders - delivered_count)

# AM Summary
am_stats = []
for am, grp in df.groupby('AM'):
    tot = len(grp)
    g_del = len(grp[grp['currentstatus'] == 'delivered'])
    g_pending = tot - g_del
    g_deliv = len(grp[grp['currentstatus'] == 'delivering'])
    g_store = len(grp[grp['currentstatus'] == 'storing'])
    g_ret = len(grp[grp['currentstatus'].isin(['return', 'return_transporting'])])
    r = (g_del / tot * 100) if tot > 0 else 0
    am_stats.append({
        'AM': am,
        'total': tot,
        'delivered': g_del,
        'pending': g_pending,
        'delivering': g_deliv,
        'storing': g_store,
        'return': g_ret,
        'rate': r,
        'reward': g_del * 10000
    })

am_stats.sort(key=lambda x: (x['pending'], x['total']), reverse=True)

html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap');
    
    * {{
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }}
    
    body {{
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
        background: #f8fafc;
        color: #0f172a;
        padding: 24px;
        width: 880px;
        margin: 0 auto;
    }}
    
    .card {{
        background: #ffffff;
        border-radius: 20px;
        padding: 26px 30px;
        box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.08), 0 0 0 1px rgba(0, 0, 0, 0.04);
    }}
    
    .header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
        padding-bottom: 16px;
        border-bottom: 2px solid #f1f5f9;
    }}

    .badge {{
        display: inline-block;
        padding: 4px 10px;
        background: #fff7ed;
        color: #ea580c;
        border: 1px solid #ffedd5;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        margin-bottom: 4px;
    }}
    
    .title {{
        font-size: 22px;
        font-weight: 800;
        color: #0f172a;
        letter-spacing: -0.5px;
    }}
    
    .time-tag {{
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        padding: 6px 14px;
        border-radius: 10px;
        text-align: right;
    }}
    .time-lbl {{
        font-size: 10px;
        font-weight: 700;
        color: #64748b;
        text-transform: uppercase;
    }}
    .time-val {{
        font-size: 13px;
        font-weight: 800;
        color: #0284c7;
    }}

    /* 3 KPI BOXES */
    .kpi-row {{
        display: grid;
        grid-template-columns: 1fr 1.2fr 1fr;
        gap: 14px;
        margin-bottom: 20px;
    }}

    .kpi-box {{
        padding: 16px 18px;
        border-radius: 14px;
    }}

    .kpi-box.blue {{
        background: #f8fafc;
        border: 1.5px solid #e2e8f0;
    }}
    .kpi-box.orange {{
        background: #fff7ed;
        border: 1.5px solid #fed7aa;
    }}
    .kpi-box.green {{
        background: #f0fdf4;
        border: 1.5px solid #bbf7d0;
    }}

    .kpi-lbl {{
        font-size: 11px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.3px;
        margin-bottom: 4px;
    }}
    .kpi-box.blue .kpi-lbl {{ color: #475569; }}
    .kpi-box.orange .kpi-lbl {{ color: #9a3412; }}
    .kpi-box.green .kpi-lbl {{ color: #166534; }}

    .kpi-num {{
        font-size: 30px;
        font-weight: 800;
        line-height: 1.1;
        margin-bottom: 4px;
    }}
    .kpi-box.blue .kpi-num {{ color: #334155; }}
    .kpi-box.orange .kpi-num {{ color: #c2410c; }}
    .kpi-box.green .kpi-num {{ color: #15803d; }}

    .kpi-desc {{
        font-size: 12px;
        font-weight: 600;
    }}
    .kpi-box.blue .kpi-desc {{ color: #64748b; }}
    .kpi-box.orange .kpi-desc {{ color: #c2410c; }}
    .kpi-box.green .kpi-desc {{ color: #15803d; }}

    /* TABLE */
    .table-box {{
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        overflow: hidden;
        margin-bottom: 18px;
    }}

    table {{
        width: 100%;
        border-collapse: collapse;
        font-size: 13px;
    }}

    th {{
        background: #f8fafc;
        color: #475569;
        font-size: 11px;
        font-weight: 800;
        text-transform: uppercase;
        padding: 10px 12px;
        border-bottom: 1px solid #e2e8f0;
        text-align: left;
    }}

    td {{
        padding: 9px 12px;
        border-bottom: 1px solid #f1f5f9;
        color: #334155;
    }}

    tr:last-child td {{
        border-bottom: none;
    }}

    tr:nth-child(even) td {{
        background: #fafafa;
    }}

    .center {{ text-align: center; }}
    .right {{ text-align: right; }}

    .tag-green {{
        background: #dcfce7;
        color: #15803d;
        font-weight: 800;
        padding: 2px 7px;
        border-radius: 6px;
        display: inline-block;
    }}

    .tag-orange {{
        background: #ffedd5;
        color: #c2410c;
        font-weight: 800;
        padding: 2px 7px;
        border-radius: 6px;
        display: inline-block;
    }}

    .tag-gray {{
        background: #f1f5f9;
        color: #64748b;
        font-weight: 700;
        padding: 2px 7px;
        border-radius: 6px;
        display: inline-block;
    }}

    /* NOTICE BANNER */
    .notice {{
        background: linear-gradient(90deg, #ea580c 0%, #f97316 100%);
        color: #ffffff;
        padding: 12px 18px;
        border-radius: 10px;
        font-size: 13px;
        font-weight: 700;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}

    .notice-badge {{
        background: rgba(255, 255, 255, 0.25);
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 11px;
        text-transform: uppercase;
    }}
</style>
</head>
<body>

<div class="card">
    <div class="header">
        <div>
            <div class="badge">VÙNG NAM TRUNG BỘ</div>
            <div class="title">TIẾN ĐỘ THƯỞNG 10K/ĐƠN TTS (NGÀY 01/10)</div>
        </div>
        <div class="time-tag">
            <div class="time-lbl">Hạn chót chốt thưởng</div>
            <div class="time-val">18:00 HÔM NAY</div>
        </div>
    </div>

    <!-- 3 KPI BOXES -->
    <div class="kpi-row">
        <div class="kpi-box blue">
            <div class="kpi-lbl">TỔNG ĐƠN DANH SÁCH</div>
            <div class="kpi-num">{total_orders} <span style="font-size:16px; font-weight:700;">đơn</span></div>
            <div class="kpi-desc">Phân bổ <b>13 Quản lý AM</b></div>
        </div>
        <div class="kpi-box orange">
            <div class="kpi-lbl">CẦN XỬ LÝ GẤP TRƯỚC 15H</div>
            <div class="kpi-num">{potential_pending} <span style="font-size:16px; font-weight:700;">đơn</span></div>
            <div class="kpi-desc">Cơ hội gom thưởng: <b>+{potential_pending * 10000:,.0f}đ</b></div>
        </div>
        <div class="kpi-box green">
            <div class="kpi-lbl">ĐÃ GTC (ĐÃ ĐẠT THƯỞNG)</div>
            <div class="kpi-num">{delivered_count} <span style="font-size:16px; font-weight:700;">đơn</span></div>
            <div class="kpi-desc">Đã chốt thưởng: <b>{current_reward:,.0f}đ</b></div>
        </div>
    </div>

    <!-- AM PROGRESS TABLE -->
    <div class="table-box">
        <table>
            <thead>
                <tr>
                    <th style="width: 35px;" class="center">#</th>
                    <th>Quản lý AM</th>
                    <th class="center">Tổng số đơn</th>
                    <th class="center">Cần xử lý gấp (Push)</th>
                    <th class="center">Đã GTC (Không push)</th>
                    <th class="right">Tỷ lệ GTC</th>
                    <th class="right">Thưởng Đã Đạt</th>
                </tr>
            </thead>
            <tbody>
"""

for idx, am in enumerate(am_stats, 1):
    pend_tag = f'<span class="tag-orange">{am["pending"]} đơn</span>' if am['pending'] > 0 else '<span class="tag-gray">0</span>'
    del_tag = f'<span class="tag-green">{am["delivered"]} đơn</span>' if am['delivered'] > 0 else '<span class="tag-gray">0</span>'
    
    html_content += f"""
                <tr>
                    <td class="center" style="font-weight:700; color:#94a3b8;">{idx}</td>
                    <td style="font-weight:700; color:#0f172a;">{am['AM']}</td>
                    <td class="center" style="font-weight:700;">{am['total']}</td>
                    <td class="center">{pend_tag}</td>
                    <td class="center">{del_tag}</td>
                    <td class="right" style="font-weight:700; color:{'#15803d' if am['rate'] > 0 else '#94a3b8'};">{am['rate']:.1f}%</td>
                    <td class="right" style="font-weight:800; color:#15803d;">{am['reward']:,.0f}đ</td>
                </tr>
    """

html_content += f"""
            </tbody>
        </table>
    </div>

    <!-- NOTICE -->
    <div class="notice">
        <div>⚡ <b>Chính sách thưởng:</b> Mỗi đơn GTC trước 18h hôm nay thưởng <b>10.000đ/đơn</b>. Yêu cầu AM push xử lý trước <b>15h00</b>.</div>
        <div class="notice-badge">Hạn chót 18:00</div>
    </div>
</div>

</body>
</html>
"""

html_path = 'scratch/bao_cao_gtc_today.html'
img_path = 'scratch/bao_cao_gtc_today.png'

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 930, "height": 920})
    page.goto(f"file:///{os.path.abspath(html_path)}")
    page.wait_for_timeout(400)
    page.screenshot(path=img_path, full_page=True)
    browser.close()

print(f"Today's report image generated: {img_path}")
