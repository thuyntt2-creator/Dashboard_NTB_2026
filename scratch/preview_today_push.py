# -*- coding: utf-8 -*-
import os
import sys
import unicodedata
from collections import defaultdict
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_csv('scratch/sheet1_today.csv')

def normalize_str(s):
    if not s or pd.isna(s):
        return ""
    return unicodedata.normalize("NFC", str(s)).strip()

orders_by_am = defaultdict(lambda: {'total': 0, 'delivered_count': 0, 'pending_by_bc': defaultdict(list)})

for _, r in df.iterrows():
    am = normalize_str(r.get('AM'))
    bc = normalize_str(r.get('Bưu Cục'))
    madh = normalize_str(r.get('MaDH'))
    status = normalize_str(r.get('currentstatus')).lower()

    if not madh or not am:
        continue

    orders_by_am[am]['total'] += 1
    if status == 'delivered':
        orders_by_am[am]['delivered_count'] += 1
    else:
        orders_by_am[am]['pending_by_bc'][bc].append(madh)

def format_am_message(am_name, data):
    total = data['total']
    delivered_count = data['delivered_count']
    pending_by_bc = data['pending_by_bc']
    pending_total = sum(len(mads) for mads in pending_by_bc.values())
    bcs_count = len(pending_by_bc)

    lines = [
        f"📢 <b>[THÔNG BÁO] XỬ LÝ ĐƠN TTS TRƯỚC 15H</b>",
        f"AM: <b>{am_name}</b>"
    ]

    if delivered_count > 0:
        lines.append(f"Tổng cộng: <b>{total} đơn</b> (Đã GTC: <b>{delivered_count} đơn</b> | Cần xử lý gấp: <b>{pending_total} đơn</b>)")
    else:
        lines.append(f"Tổng cộng: <b>{total} đơn</b> cần xử lý gấp ({bcs_count} bưu cục)")

    lines.extend([
        f"",
        f"Chính sách thưởng:",
        f"- Mỗi đơn GTC trước 18h HÔM NAY sẽ được THƯỞNG 10.000đ/đơn!",
        f"- Yêu cầu: AM đôn đốc Bưu cục xử lý gấp trước 15h00 hôm nay.",
        f"",
        f"Danh sách đơn hàng cần xử lý theo bưu cục:"
    ])

    if pending_total == 0:
        lines.append("\n<i>(Toàn bộ đơn của AM đã được Giao Thành Công!)</i>")
    else:
        for idx, (bc, mads) in enumerate(pending_by_bc.items(), 1):
            lines.append(f"\nBưu cục: <b>{bc}</b> (<b>{len(mads)}</b> đơn):")
            for m_idx, madh in enumerate(mads, 1):
                lines.append(f"  {m_idx}. <code>{madh}</code>")

    return "\n".join(lines)

if __name__ == '__main__':
    for am, d in sorted(orders_by_am.items(), key=lambda x: x[1]['total'], reverse=True):
        print(f"\n{'='*70}")
        print(f"AM: {am} | Tổng: {d['total']} | Đã GTC: {d['delivered_count']} | Cần push: {sum(len(v) for v in d['pending_by_bc'].values())}")
        print(f"{'='*70}")
        print(format_am_message(am, d))
