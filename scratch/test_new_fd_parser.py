import csv
import re
import os
import json

def parse_fd_csv_new(file_path='ops_fd.csv', am_filter=None, prov_filter=None, po_filter=None):
    if not os.path.exists(file_path):
        return {"error": "Không tìm thấy file ops_fd.csv"}

    def clean_num(val):
        if val is None or val == '':
            return 0
        s = str(val).strip().replace(',', '')
        try:
            return int(float(s)) if float(s).is_integer() else float(s)
        except:
            return 0

    def clean_pct(val):
        if val is None or val == '':
            return 0.0
        s = str(val).strip().replace('%', '').replace(',', '.')
        try:
            return float(s)
        except:
            return 0.0

    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        lines = list(reader)

    if not lines:
        return {"error": "File ops_fd.csv trống"}

    # 1. Parse Title & Date if any
    title = ""
    date_str = "N-1"
    if len(lines) > 0 and len(lines[0]) > 0:
        title = lines[0][0].strip()
        m = re.search(r'\(N-1\)|N-1|\d{2}/\d{2}/\d{4}', title)
        if m:
            date_str = m.group(0)

    # 2. Parse Channel Breakdown from Header (Rows 1-3)
    channel_breakdown = []
    # Row 1 has channel names starting from col index 10
    # Row 2 has subheaders: 'Tổng đơn có gán giao', '%Trả hàng'
    # Row 3 has values starting from col index 10
    if len(lines) >= 3:
        r1 = lines[0]
        r2 = lines[1]
        r3 = lines[2]
        
        # Scan through columns in r1
        c = 0
        while c < max(len(r1), len(r3)):
            ch_name = r1[c].strip() if c < len(r1) else ""
            if ch_name and ch_name not in ['BÁO CÁO %FD HUB (N-1) – VÙNG NTB', '1. BẢNG TỔNG QUAN VÙNG NTB (N-1)']:
                # Found a channel
                total_orders = clean_num(r3[c]) if c < len(r3) else 0
                ret_rate = clean_pct(r3[c+1]) if (c+1) < len(r3) else 0.0
                channel_breakdown.append({
                    "channel": ch_name,
                    "total_orders": total_orders,
                    "return_rate": ret_rate
                })
                c += 2
            else:
                c += 1

    # 3. Parse Sections
    summary_metrics = {}
    top_10_pos = []
    am_rankings = []
    all_pos = []

    current_section = None

    for line in lines:
        if not line or not any(str(cell).strip() for cell in line):
            continue

        first_cell = line[0].strip() if len(line) > 0 else ""

        if "1. BẢNG TỔNG QUAN" in first_cell:
            current_section = "summary"
            continue
        elif "2. TOP 10 BƯU CỤC" in first_cell:
            current_section = "top10"
            continue
        elif "3. XẾP HẠNG %FD THEO CÁC AM" in first_cell:
            current_section = "am_ranking"
            continue
        elif "4. DANH SÁCH TẤT CẢ BƯU CỤC" in first_cell:
            current_section = "all_pos"
            continue

        # Skip table headers
        if first_cell in ['Chỉ Số Tổng Quan', 'STT'] or 'Tên Bưu Cục' in line or 'AM Phụ Trách' in line:
            continue

        if current_section == "summary":
            # Cols: Chỉ Số Tổng Quan, Giá Trị, Ghi Chú
            metric_name = first_cell
            val_str = line[1].strip() if len(line) > 1 else ""
            note = line[2].strip() if len(line) > 2 else ""
            if "Tổng Đơn Có Gán Giao" in metric_name:
                summary_metrics["total_orders"] = clean_num(val_str)
                summary_metrics["total_orders_note"] = note
            elif "Tổng Đơn Return" in metric_name:
                summary_metrics["return_orders"] = clean_num(val_str)
                summary_metrics["return_orders_note"] = note
            elif "%FD Tổng Vùng" in metric_name:
                summary_metrics["fd_rate"] = clean_pct(val_str)
                summary_metrics["fd_rate_note"] = note
            elif "Số Bưu Cục Quản Lý" in metric_name:
                summary_metrics["po_count"] = clean_num(val_str)
                summary_metrics["po_count_note"] = note

        elif current_section == "top10":
            # Cols: STT, Tên Bưu Cục, AM Phụ Trách, Total Đơn, Đơn Return, %FD (Return), Tỷ Trọng Return
            if len(line) >= 7 and first_cell.isdigit():
                top_10_pos.append({
                    "stt": int(first_cell),
                    "post_office": line[1].strip(),
                    "am": line[2].strip(),
                    "total_orders": clean_num(line[3]),
                    "return_orders": clean_num(line[4]),
                    "fd_rate": clean_pct(line[5]),
                    "return_share": clean_pct(line[6])
                })

        elif current_section == "am_ranking":
            # Cols: STT, AM Phụ Trách, Total Đơn, Đơn Return, %FD (Return), Tỷ Trọng Return, Tỷ Trọng Sản Lượng
            if len(line) >= 7 and first_cell.isdigit():
                am_rankings.append({
                    "stt": int(first_cell),
                    "am": line[1].strip(),
                    "total_orders": clean_num(line[2]),
                    "return_orders": clean_num(line[3]),
                    "fd_rate": clean_pct(line[4]),
                    "return_share": clean_pct(line[5]),
                    "volume_share": clean_pct(line[6]) if len(line) > 6 else 0.0
                })

        elif current_section == "all_pos":
            # Cols: STT, Tên Bưu Cục, AM Phụ Trách, Total Đơn, Đơn Return, %FD (Return), Tỷ Trọng Return
            if len(line) >= 7 and first_cell.isdigit():
                all_pos.append({
                    "stt": int(first_cell),
                    "post_office": line[1].strip(),
                    "am": line[2].strip(),
                    "total_orders": clean_num(line[3]),
                    "return_orders": clean_num(line[4]),
                    "fd_rate": clean_pct(line[5]),
                    "return_share": clean_pct(line[6])
                })

    # Summary fallback calculation if not found in table
    if "total_orders" not in summary_metrics and all_pos:
        tot = sum(p["total_orders"] for p in all_pos)
        ret = sum(p["return_orders"] for p in all_pos)
        summary_metrics["total_orders"] = tot
        summary_metrics["return_orders"] = ret
        summary_metrics["fd_rate"] = round(ret / tot * 100, 2) if tot > 0 else 0.0
        summary_metrics["po_count"] = len(all_pos)

    # Filter logic if AM / Post office is selected
    filtered_pos = all_pos
    filtered_am_rankings = am_rankings
    filtered_top10 = top_10_pos

    if am_filter:
        am_filter_lower = am_filter.lower().strip()
        filtered_pos = [p for p in filtered_pos if am_filter_lower in p["am"].lower()]
        filtered_am_rankings = [a for a in filtered_am_rankings if am_filter_lower in a["am"].lower()]
        filtered_top10 = [p for p in filtered_pos[:10]]

    if po_filter:
        po_filter_lower = po_filter.lower().strip()
        filtered_pos = [p for p in filtered_pos if po_filter_lower in p["post_office"].lower()]

    # Extract unique AMs for dropdown filter
    unique_ams = sorted(list(set(p["am"] for p in all_pos if p["am"])))

    return {
        "title": title or "BÁO CÁO %FD HUB (N-1) – VÙNG NTB",
        "date": date_str,
        "summary": summary_metrics,
        "channels": channel_breakdown,
        "top10": filtered_top10,
        "am_rankings": filtered_am_rankings,
        "all_pos": filtered_pos,
        "unique_ams": unique_ams,
        # backward compatibility keys in case anything calls kpi/po/am/province
        "kpi": {
            "fd_n": summary_metrics.get("fd_rate", 0.0),
            "fd_n1": summary_metrics.get("fd_rate", 0.0),
            "vs_n1": 0.0,
            "fd_n7": 0.0,
            "vs_n7": 0.0
        },
        "po": [
            {
                "post_office": p["post_office"],
                "am": p["am"],
                "fd_n": p["fd_rate"],
                "fd_n1": p["fd_rate"],
                "vs_n1": 0.0,
                "fd_n7": 0.0,
                "vs_n7": 0.0,
                "vol_giao": p["total_orders"],
                "vol_tra": p["return_orders"],
                "ty_trong_tra": p["return_share"]
            }
            for p in filtered_pos
        ],
        "am": [
            {
                "am": a["am"],
                "fd_n": a["fd_rate"],
                "fd_n1": a["fd_rate"],
                "vs_n1": 0.0,
                "fd_n7": 0.0,
                "vs_n7": 0.0,
                "vol_tra": a["return_orders"],
                "ty_trong_tra": a["return_share"]
            }
            for a in filtered_am_rankings
        ]
    }

if __name__ == '__main__':
    res = parse_fd_csv_new('ops_fd.csv')
    print("Parsed result keys:", res.keys())
    print("Summary:", res["summary"])
    print("Channels:", res["channels"])
    print(f"Top 10 count: {len(res['top10'])}")
    print("Sample top 10:", res["top10"][:3])
    print(f"AM rankings count: {len(res['am_rankings'])}")
    print("Sample AM ranking:", res["am_rankings"][:3])
    print(f"All POs count: {len(res['all_pos'])}")
    print("Sample All POs:", res["all_pos"][:3])
    print("Unique AMs:", res["unique_ams"])
