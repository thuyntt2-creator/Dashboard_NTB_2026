import io
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def fd_color(val):
    if val is None or pd.isna(val): return '#FFFFFF'
    if val <= 4.5: return '#D9EAD3'
    elif val < 6.0: return '#FFF2CC'
    else: return '#FFE0E0'

def fd_textcolor(val):
    if val is None or pd.isna(val): return '#000000'
    if val <= 4.5: return '#274E13'
    elif val < 6.0: return '#7F6000'
    else: return '#C00000'

def delta_text_and_colors(diff):
    if diff is None or pd.isna(diff) or abs(diff) < 0.005:
        return "-", '#FFFFFF', '#000000'
    elif diff > 0:
        txt = f"▲ +{diff:.2f}%"
        bg = '#FFE0E0' if diff >= 2.0 else '#FFFFFF'
        fg = '#C00000'
        return txt, bg, fg
    else:
        txt = f"▼ {diff:.2f}%"
        bg = '#D9EAD3' if diff <= -2.0 else '#FFFFFF'
        fg = '#274E13'
        return txt, bg, fg

def render_image_top10(overview, top10_bc):
    fig_h = 10.5
    fig = plt.figure(figsize=(17, fig_h), dpi=200)

    date_n = overview.get('Date_N', '')
    date_n1 = overview.get('Date_N1', '')
    diff_vung = overview.get('FD_pct_diff', 0.0)
    diff_vung_str = f"▲ +{diff_vung:.2f}%" if diff_vung > 0 else (f"▼ {diff_vung:.2f}%" if diff_vung < 0 else "-")

    title_main = f"BÁO CÁO %FD HUB NGÀY {date_n} (vs N-1: {date_n1}) – VÙNG NTB"
    subtitle = f"(Total Đơn: {overview['Total_don']:,.0f}  |  Đơn Return: {overview['Don_return']:,.0f}  |  %FD Tổng Vùng: {overview['FD_pct']:.2f}% [{diff_vung_str} vs N-1])"

    fig.suptitle(f"{title_main}\n{subtitle}", fontsize=21, fontweight='bold', color='#1F4E79', y=0.96)

    ax = fig.add_axes([0.02, 0.04, 0.96, 0.81])
    ax.axis('off')
    ax.set_title('TOP 10 BƯU CỤC CÓ %FD CAO NHẤT', fontsize=19, fontweight='bold', loc='left', pad=16, color='#1F4E79')

    labels = ['STT', 'Tên Bưu Cục', 'AM Phụ Trách', 'Total Đơn', 'Đơn Return', '%FD (N)', f'%FD (N-1)\n{date_n1}', 'vs N-1', 'Tỷ Trọng\nReturn']
    col_w = [0.05, 0.25, 0.16, 0.09, 0.09, 0.09, 0.09, 0.09, 0.09]

    cell_text = [labels]
    cell_color = [['#1F4E79'] * len(labels)]
    text_color = [['white'] * len(labels)]

    for idx, r in top10_bc.iterrows():
        alt = (idx % 2 == 1)
        base_bg = '#F5F9FF' if alt else '#FFFFFF'
        
        d_txt, d_bg, d_fg = delta_text_and_colors(r.get('vs_N1'))
        if d_bg == '#FFFFFF' and alt:
            d_bg = '#F5F9FF'

        fd_n1_val = r.get('%FD_N1')
        fd_n1_str = f"{fd_n1_val:.2f}%" if pd.notna(fd_n1_val) else "-"

        texts = [
            str(idx + 1),
            str(r['BC']),
            str(r['AM']),
            f"{r['Total']:,.0f}",
            f"{r['Return']:,.0f}",
            f"{r['%FD_N']:.2f}%",
            fd_n1_str,
            d_txt,
            f"{r['Tỷ trọng return']:.2f}%"
        ]
        colors = [
            base_bg, base_bg, base_bg, base_bg, base_bg,
            fd_color(r['%FD_N']),
            base_bg,
            d_bg,
            '#FFE69C'
        ]
        tcolors = [
            '#000000', '#000000', '#000000', '#000000', '#000000',
            fd_textcolor(r['%FD_N']),
            '#000000',
            d_fg,
            '#000000'
        ]
        cell_text.append(texts)
        cell_color.append(colors)
        text_color.append(tcolors)

    tbl = ax.table(cellText=cell_text, cellColours=cell_color, cellLoc='center', loc='upper left', colWidths=col_w, bbox=[0, 0, 1, 1])
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(14)

    for (r, c), cell in tbl.get_celld().items():
        cell.set_edgecolor('#BFBFBF')
        cell.set_linewidth(1.2)
        cell.set_text_props(color=text_color[r][c])
        if r == 0:
            cell.set_text_props(weight='bold', color='white', fontsize=15)
        if c == 1:
            cell.set_text_props(ha='left', weight='bold' if r > 0 else 'bold')
            cell._loc = 'left'
        elif c == 2:
            cell.set_text_props(ha='left')
            cell._loc = 'left'

    out_path = 'scratch/test_top10_preview.png'
    plt.savefig(out_path, format='png', bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"Rendered {out_path}")

def render_image_am(overview, am_df):
    n_am = len(am_df)
    fig_h = max(11, n_am * 0.62 + 3.0)
    fig = plt.figure(figsize=(17, fig_h), dpi=200)

    date_n = overview.get('Date_N', '')
    date_n1 = overview.get('Date_N1', '')
    diff_vung = overview.get('FD_pct_diff', 0.0)
    diff_vung_str = f"▲ +{diff_vung:.2f}%" if diff_vung > 0 else (f"▼ {diff_vung:.2f}%" if diff_vung < 0 else "-")

    title_main = f"BÁO CÁO %FD HUB NGÀY {date_n} (vs N-1: {date_n1}) – VÙNG NTB"
    subtitle = f"(Total Đơn: {overview['Total_don']:,.0f}  |  Đơn Return: {overview['Don_return']:,.0f}  |  %FD Tổng Vùng: {overview['FD_pct']:.2f}% [{diff_vung_str} vs N-1])"

    fig.suptitle(f"{title_main}\n{subtitle}", fontsize=21, fontweight='bold', color='#1F4E79', y=0.96)

    ax = fig.add_axes([0.02, 0.03, 0.96, 0.83])
    ax.axis('off')
    ax.set_title('XẾP HẠNG %FD THEO CÁC AM', fontsize=19, fontweight='bold', loc='left', pad=16, color='#1F4E79')

    labels = ['STT', 'AM Phụ Trách', 'Total Đơn', 'Đơn Return', '%FD (N)', f'%FD (N-1)\n{date_n1}', 'vs N-1', 'Tỷ Trọng\nReturn', 'Tỷ Trọng\nSản Lượng']
    col_w = [0.05, 0.22, 0.09, 0.09, 0.09, 0.09, 0.09, 0.14, 0.14]

    cell_text = [labels]
    cell_color = [['#1F4E79'] * len(labels)]
    text_color = [['white'] * len(labels)]

    for idx, r in am_df.iterrows():
        alt = (idx % 2 == 1)
        base_bg = '#F5F9FF' if alt else '#FFFFFF'
        
        d_txt, d_bg, d_fg = delta_text_and_colors(r.get('vs_N1'))
        if d_bg == '#FFFFFF' and alt:
            d_bg = '#F5F9FF'

        fd_n1_val = r.get('%FD_N1')
        fd_n1_str = f"{fd_n1_val:.2f}%" if pd.notna(fd_n1_val) else "-"

        texts = [
            str(idx + 1),
            str(r['AM']),
            f"{r['Total']:,.0f}",
            f"{r['Return']:,.0f}",
            f"{r['%FD_N']:.2f}%",
            fd_n1_str,
            d_txt,
            f"{r['Tỷ trọng return']:.2f}%",
            f"{r['Tỷ trọng sản lượng']:.2f}%"
        ]
        colors = [
            base_bg, base_bg, base_bg, base_bg,
            fd_color(r['%FD_N']),
            base_bg,
            d_bg,
            '#FFE69C',
            base_bg
        ]
        tcolors = [
            '#000000', '#000000', '#000000', '#000000',
            fd_textcolor(r['%FD_N']),
            '#000000',
            d_fg,
            '#000000',
            '#000000'
        ]
        cell_text.append(texts)
        cell_color.append(colors)
        text_color.append(tcolors)

    tbl = ax.table(cellText=cell_text, cellColours=cell_color, cellLoc='center', loc='upper left', colWidths=col_w, bbox=[0, 0, 1, 1])
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(14)

    for (r, c), cell in tbl.get_celld().items():
        cell.set_edgecolor('#BFBFBF')
        cell.set_linewidth(1.2)
        cell.set_text_props(color=text_color[r][c])
        if r == 0:
            cell.set_text_props(weight='bold', color='white', fontsize=15)
        if c == 1:
            cell.set_text_props(ha='left', weight='bold' if r > 0 else 'bold')
            cell._loc = 'left'

    out_path = 'scratch/test_am_preview.png'
    plt.savefig(out_path, format='png', bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"Rendered {out_path}")

# Run with test data from test_new_logic
import test_new_logic as tnl
overview = {
    'Date_N': tnl.date_N.strftime('%d/%m/%Y'),
    'Date_N1': tnl.date_N1.strftime('%d/%m/%Y'),
    'Total_don': tnl.tot_don_N,
    'Don_return': tnl.tot_ret_N,
    'FD_pct': tnl.fd_N,
    'FD_pct_diff': tnl.fd_N - tnl.fd_N1,
}
render_image_top10(overview, tnl.top10_bc)
render_image_am(overview, tnl.am_merged)
