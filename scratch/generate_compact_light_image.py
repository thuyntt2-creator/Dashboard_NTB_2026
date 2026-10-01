# -*- coding: utf-8 -*-
import os
import sys
import pandas as pd
from datetime import datetime
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

# 1. Load Data
df = pd.read_csv('scratch/sheet1_current.csv')

df['AM'] = df['AM'].str.strip()
df['Bưu Cục'] = df['Bưu Cục'].str.strip()
df['currentstatus'] = df['currentstatus'].fillna('unknown').str.strip()

total_orders = len(df)
delivered_count = len(df[df['currentstatus'] == 'delivered'])
delivering_count = len(df[df['currentstatus'] == 'delivering'])
return_count = len(df[df['currentstatus'].isin(['return', 'return_transporting'])])
other_count = total_orders - delivered_count - delivering_count - return_count

gtc_rate = (delivered_count / total_orders * 100) if total_orders > 0 else 0
delivering_rate = (delivering_count / total_orders * 100) if total_orders > 0 else 0

current_reward = delivered_count * 10000
potential_reward = delivering_count * 10000

# AM Summary
am_stats = []
for am, grp in df.groupby('AM'):
    tot = len(grp)
    g_del = len(grp[grp['currentstatus'] == 'delivered'])
    g_deli = len(grp[grp['currentstatus'] == 'delivering'])
    g_ret = len(grp[grp['currentstatus'].isin(['return', 'return_transporting'])])
    g_other = tot - g_del - g_deli - g_ret
    r = (g_del / tot * 100) if tot > 0 else 0
    am_stats.append({
        'AM': am,
        'total': tot,
        'delivered': g_del,
        'delivering': g_deli,
        'return_other': g_ret + g_other,
        'rate': r,
        'reward': g_del * 10000,
        'potential': g_deli * 10000
    })

# Sắp xếp AM: Ưu tiên AM có đơn đang giao nhiều nhất để push, sau đó đến đã GTC
am_stats.sort(key=lambda x: (x['delivering'], x['delivered'], x['rate']), reverse=True)

# HTML Template - Sáng sủa, thanh lịch, gọn gàng
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
        background: #f1f5f9;
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
        grid-template-columns: 1.1fr 1.2fr 0.9fr;
        gap: 14px;
        margin-bottom: 20px;
    }}

    .kpi-box {{
        padding: 16px 18px;
        border-radius: 14px;
        position: relative;
    }}

    .kpi-box.green {{
        background: #f0fdf4;
        border: 1.5px solid #bbf7d0;
    }}
    .kpi-box.orange {{
        background: #fff7ed;
        border: 1.5px solid #fed7aa;
    }}
    .kpi-box.blue {{
        background: #f8fafc;
        border: 1.5px solid #e2e8f0;
    }}

    .kpi-lbl {{
        font-size: 11px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.3px;
        margin-bottom: 4px;
    }}
    .kpi-box.green .kpi-lbl {{ color: #166534; }}
    .kpi-box.orange .kpi-lbl {{ color: #9a3412; }}
    .kpi-box.blue .kpi-lbl {{ color: #475569; }}

    .kpi-num {{
        font-size: 30px;
        font-weight: 800;
        line-height: 1.1;
        margin-bottom: 4px;
    }}
    .kpi-box.green .kpi-num {{ color: #15803d; }}
    .kpi-box.orange .kpi-num {{ color: #c2410c; }}
    .kpi-box.blue .kpi-num {{ color: #334155; }}

    .kpi-desc {{
        font-size: 12px;
        font-weight: 600;
    }}
    .kpi-box.green .kpi-desc {{ color: #15803d; }}
    .kpi-box.orange .kpi-desc {{ color: #c2410c; }}
    .kpi-box.blue .kpi-desc {{ color: #64748b; }}

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
        padding: 10px 12px;
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
        padding: 3px 8px;
        border-radius: 6px;
        display: inline-block;
    }}

    .tag-orange {{
        background: #ffedd5;
        color: #c2410c;
        font-weight: 800;
        padding: 3px 8px;
        border-radius: 6px;
        display: inline-block;
    }}

    .tag-gray {{
        background: #f1f5f9;
        color: #64748b;
        font-weight: 700;
        padding: 3px 8px;
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
            <div class="title">TIẾN ĐỘ THƯỞNG 10K/ĐƠN TTS (CẬP NHẬT 15H35)</div>
        </div>
        <div class="time-tag">
            <div class="time-lbl">Hạn chót chốt thưởng</div>
            <div class="time-val">18:00 HÔM NAY</div>
        </div>
    </div>

    <!-- 3 KPI BOXES -->
    <div class="kpi-row">
        <div class="kpi-box green">
            <div class="kpi-lbl">ĐÃ GIAO THÀNH CÔNG (GTC)</div>
            <div class="kpi-num">{delivered_count} <span style="font-size:16px; font-weight:700;">đơn</span></div>
            <div class="kpi-desc">Tiền thưởng đã đạt: <b>{current_reward:,.0f}đ</b></div>
        </div>
        <div class="kpi-box orange">
            <div class="kpi-lbl">ĐANG ĐI GIAO (DELIVERING)</div>
            <div class="kpi-num">{delivering_count} <span style="font-size:16px; font-weight:700;">đơn</span></div>
            <div class="kpi-desc">Cơ hội gom thêm: <b>+{potential_reward:,.0f}đ</b></div>
        </div>
        <div class="kpi-box blue">
            <div class="kpi-lbl">ĐÃ XỬ LÝ HOÀN / TỒN KHÁC</div>
            <div class="kpi-num">{return_count + other_count} <span style="font-size:16px; font-weight:700;">đơn</span></div>
            <div class="kpi-desc">Đã xử lý hoàn: <b>{return_count} đơn</b></div>
        </div>
    </div>

    <!-- AM PROGRESS TABLE -->
    <div class="table-box">
        <table>
            <thead>
                <tr>
                    <th style="width: 40px;" class="center">#</th>
                    <th>Quản lý AM</th>
                    <th class="center">Tổng đơn</th>
                    <th class="center">Đang đi giao (Push gấp)</th>
                    <th class="center">Đã GTC (Thưởng 10k)</th>
                    <th class="right">Tỷ lệ GTC</th>
                    <th class="right">Thưởng Hiện Tại</th>
                </tr>
            </thead>
            <tbody>
"""

for idx, am in enumerate(am_stats, 1):
    deliv_tag = f'<span class="tag-orange">{am["delivering"]} đơn</span>' if am['delivering'] > 0 else '<span class="tag-gray">0</span>'
    del_tag = f'<span class="tag-green">{am["delivered"]} đơn</span>' if am['delivered'] > 0 else '<span class="tag-gray">0</span>'
    
    html_content += f"""
                <tr>
                    <td class="center" style="font-weight:700; color:#94a3b8;">{idx}</td>
                    <td style="font-weight:700; color:#0f172a;">{am['AM']}</td>
                    <td class="center" style="font-weight:700;">{am['total']}</td>
                    <td class="center">{deliv_tag}</td>
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
        <div>⚡ <b>Mục tiêu:</b> AM đôn đốc Bưu cục giao dứt điểm <b>{delivering_count} đơn đang đi giao</b> trước 18h00 để nhận trọn thưởng 10.000đ/đơn!</div>
        <div class="notice-badge">Hạn chót 18:00</div>
    </div>
</div>

</body>
</html>
"""

html_path = 'scratch/bao_cao_gtc_compact.html'
img_path = 'scratch/bao_cao_gtc_compact.png'

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 930, "height": 800})
    page.goto(f"file:///{os.path.abspath(html_path)}")
    page.wait_for_timeout(400)
    page.screenshot(path=img_path, full_page=True)
    browser.close()

print(f"Compact light image generated: {img_path}")
