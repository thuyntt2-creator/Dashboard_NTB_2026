"""
push_charts_kinhdoanh.py
========================
Đọc 2 bảng "V. KINH DOANH" + "Doanh thu khách hàng mới" từ 1 tab Google Sheet,
tự dọn data (bỏ dòng combo nhiều AM, sort giảm dần) rồi:
  1. Viết data đã dọn vào tab "ChartData_PYTHON" (để chart trỏ vào)
  2. Tạo 5 chart trực tiếp trên Google Sheet bằng Sheets API:
     - Tổng Volume & Doanh thu toàn vùng theo tuần (combo, 2 trục)
     - Volume theo AM - tuần gần nhất vs tuần trước
     - Doanh thu theo AM - tuần gần nhất vs tuần trước
     - Doanh thu khách hàng mới toàn vùng theo tuần
     - Doanh thu khách hàng mới theo AM - tuần gần nhất vs tuần trước

CÀI ĐẶT TRƯỚC KHI CHẠY:
    pip install gspread --break-system-packages

CẤU HÌNH (sửa SPREADSHEET_ID và SOURCE_SHEET_NAME):
    SPREADSHEET_ID    : ID của Google Sheet (lấy từ URL .../d/<ID>/edit)
    SOURCE_SHEET_NAME : tên tab chứa 2 bảng "V. KINH DOANH" / "Doanh thu khách hàng mới"

Chạy:
    python push_charts_kinhdoanh.py
"""

import os
import sys
import gspread

# Configure output encoding for Vietnamese characters
sys.stdout.reconfigure(encoding='utf-8')

# ============================ CONFIG - SỬA Ở ĐÂY ============================
FOLDER_PATH = r'C:\Users\lap4all\Desktop\Backlog_Automation'
JSON_FILE = os.path.join(FOLDER_PATH, 'credentials.json')

SPREADSHEET_ID = "1PpWUoCYMiaZjoTpCg_U-cSX84jcqP5qX4NyJXmd_I1k"
SOURCE_SHEET_NAME = "Kinh doanh"
CHART_DATA_SHEET_NAME = "ChartData_PYTHON"
# =============================================================================


# ---------------------------------------------------------------------------
# 1) Đọc + parse data nguồn
# ---------------------------------------------------------------------------
def find_table(values, marker_col0, marker_col1_prefix, start_row=0):
    """Tìm header row: cột A == marker_col0, cột B bắt đầu bằng marker_col1_prefix.
    Trả về (header_idx, data_rows) với data_rows là list row cho tới khi gặp 'Grand Total'."""
    for i in range(start_row, len(values)):
        row = values[i]
        if len(row) >= 2 and row[0].strip() == marker_col0 and row[1].strip().startswith(marker_col1_prefix):
            header = row
            data = []
            for j in range(i + 1, len(values)):
                r = values[j]
                if not r or not r[0].strip():
                    continue
                data.append(r)
                if r[0].strip() == "Grand Total":
                    break
            return i, header, data
    raise ValueError(f"Không tìm thấy bảng có header A='{marker_col0}', B bắt đầu '{marker_col1_prefix}'")


def to_num(s):
    """Convert giá trị string từ Google Sheets (get_all_values) sang float.
    Hỗ trợ số có dấu phẩy ngăn cách hàng nghìn kiểu '8,349,430'."""
    if s is None or str(s).strip() == "":
        return 0.0
    s = str(s).strip().replace(",", "")
    try:
        return float(s)
    except ValueError:
        return 0.0


def parse_kinh_doanh(values):
    """Bảng V. KINH DOANH: AM | Vol21 DT21 | Vol22 DT22 | Vol23 DT23 | Vol24 DT24"""
    _, header, rows = find_table(values, "AM", "Volume")
    weeks = ["Tuần 21", "Tuần 22", "Tuần 23", "Tuần 24"]
    out = []
    for r in rows:
        am_raw = r[0].strip()
        vol = [to_num(r[1 + 2 * i]) for i in range(4)]
        dt = [to_num(r[2 + 2 * i]) for i in range(4)]
        out.append({"am_raw": am_raw, "vol": vol, "dt": dt})
    return weeks, out


def parse_khach_hang_moi(values):
    """Bảng Doanh thu khách hàng mới: AM | Tuần21 | Tuần22 | Tuần23 | Tuần24 | So với W23"""
    _, header, rows = find_table(values, "AM", "Tuần")
    out = []
    for r in rows:
        am = r[0].strip()
        vals = [to_num(r[1 + i]) for i in range(4)]
        out.append({"am": am, "vals": vals})
    return out


# ---------------------------------------------------------------------------
# 2) Dọn data cho chart (bỏ combo nhiều AM, sort giảm dần theo tuần gần nhất)
# ---------------------------------------------------------------------------
def clean_kd(rows):
    clean = [r for r in rows if r["am_raw"] != "Grand Total" and "," not in r["am_raw"]]
    for r in clean:
        r["am"] = r["am_raw"].split("-", 1)[1] if "-" in r["am_raw"] else r["am_raw"]
    clean.sort(key=lambda r: r["vol"][-1], reverse=True)
    return clean


def clean_khm(rows):
    clean = [r for r in rows if r["am"] != "Grand Total"]
    clean.sort(key=lambda r: r["vals"][-1], reverse=True)
    return clean


# ---------------------------------------------------------------------------
# 3) Viết bảng "ChartData_PYTHON" + tạo chart
# ---------------------------------------------------------------------------
def a1(col, row):
    """col, row 0-indexed -> A1 notation."""
    letters = ""
    c = col + 1
    while c:
        c, rem = divmod(c - 1, 26)
        letters = chr(65 + rem) + letters
    return f"{letters}{row + 1}"


def grid_range(sheet_id, start_row, end_row, start_col, end_col):
    return {"sheetId": sheet_id, "startRowIndex": start_row, "endRowIndex": end_row,
            "startColumnIndex": start_col, "endColumnIndex": end_col}


def main():
    gc = gspread.service_account(filename=JSON_FILE)
    sh = gc.open_by_key(SPREADSHEET_ID)
    src = sh.worksheet(SOURCE_SHEET_NAME)
    values = src.get_all_values()

    weeks, kd_rows = parse_kinh_doanh(values)
    khm_rows = parse_khach_hang_moi(values)

    kd_clean = clean_kd(kd_rows)
    khm_clean = clean_khm(khm_rows)

    # Grand total cho chart trend (lấy từ data gốc, không lọc)
    gt_kd = next(r for r in kd_rows if r["am_raw"] == "Grand Total")
    gt_khm = next(r for r in khm_rows if r["am"] == "Grand Total")

    # tạo / clear sheet ChartData_PYTHON
    try:
        cd = sh.worksheet(CHART_DATA_SHEET_NAME)
        cd.clear()
        # xoá chart cũ trên sheet này (nếu có) để khỏi bị trùng
        cd_meta = sh.fetch_sheet_metadata()
        for s in cd_meta["sheets"]:
            if s["properties"]["sheetId"] == cd.id:
                for ch in s.get("charts", []):
                    sh.batch_update({"requests": [{"deleteEmbeddedObject": {"objectId": ch["chartId"]}}]})
    except gspread.WorksheetNotFound:
        cd = sh.add_worksheet(title=CHART_DATA_SHEET_NAME, rows=200, cols=30)

    cd_id = cd.id
    requests = []

    # ---- Table A: trend tổng (cho chart 1 + 4) ----
    table_a = [["Tuần", "Volume", "Doanh thu", "Doanh thu KH mới"]]
    for i, wk in enumerate(weeks):
        table_a.append([wk, gt_kd["vol"][i], gt_kd["dt"][i], gt_khm["vals"][i]])
    cd.update(range_name=a1(0, 0) + ":" + a1(3, len(table_a) - 1), values=table_a)
    a_start_row, a_end_row = 1, 1 + 4  # data rows (excl header), 0-indexed exclusive end

    # ---- Table B: Volume theo AM (cho chart 2) ----
    table_b = [["AM", f"Volume {weeks[-2]}", f"Volume {weeks[-1]}"]]
    for r in kd_clean:
        table_b.append([r["am"], r["vol"][-2], r["vol"][-1]])
    b_col0 = 6  # cột G
    cd.update(range_name=a1(b_col0, 0) + ":" + a1(b_col0 + 2, len(table_b) - 1), values=table_b)
    b_start_row, b_end_row = 1, len(table_b)

    # ---- Table C: Doanh thu theo AM (cho chart 3) ----
    table_c = [["AM", f"Doanh thu {weeks[-2]}", f"Doanh thu {weeks[-1]}"]]
    for r in kd_clean:
        table_c.append([r["am"], r["dt"][-2], r["dt"][-1]])
    c_col0 = 10  # cột K
    cd.update(range_name=a1(c_col0, 0) + ":" + a1(c_col0 + 2, len(table_c) - 1), values=table_c)
    c_start_row, c_end_row = 1, len(table_c)

    # ---- Table D: Doanh thu khách hàng mới theo AM (cho chart 5) ----
    table_d = [["AM", "Tuần 23", "Tuần 24"]]
    for r in khm_clean:
        table_d.append([r["am"], r["vals"][-2], r["vals"][-1]])
    d_col0 = 14  # cột O
    cd.update(range_name=a1(d_col0, 0) + ":" + a1(d_col0 + 2, len(table_d) - 1), values=table_d)
    d_start_row, d_end_row = 1, len(table_d)

    # Định dạng các cột số để chart tự động thừa kế định dạng, tránh lỗi hiển thị khoa học (dính chữ "e")
    print("🔄 Đang định dạng các cột số trong 'ChartData_PYTHON'...")
    try:
        cd.format("B2:D10", {"numberFormat": {"type": "NUMBER", "pattern": "#,##0"}})
        cd.format("H2:I100", {"numberFormat": {"type": "NUMBER", "pattern": "#,##0"}})
        cd.format("L2:M100", {"numberFormat": {"type": "NUMBER", "pattern": "#,##0"}})
        cd.format("P2:Q100", {"numberFormat": {"type": "NUMBER", "pattern": "#,##0"}})
        print("✔️ Định dạng số thành công!")
    except Exception as fe:
        print(f"⚠️ Cảnh báo định dạng số: {fe}")

    # ================= CHART 1: Combo - Tổng Volume & Doanh thu theo tuần =================
    requests.append({
        "addChart": {
            "chart": {
                "spec": {
                    "title": "Tổng Volume & Doanh thu toàn vùng theo tuần",
                    "basicChart": {
                        "chartType": "LINE",
                        "legendPosition": "BOTTOM_LEGEND",
                        "axis": [
                            {"position": "BOTTOM_AXIS", "title": "Tuần"},
                            {"position": "LEFT_AXIS", "title": "Volume"},
                            {"position": "RIGHT_AXIS", "title": "Doanh thu (VNĐ)"},
                        ],
                        "domains": [{"domain": {"sourceRange": {
                            "sources": [grid_range(cd_id, a_start_row, a_end_row, 0, 1)]}}}],
                        "series": [
                            {"series": {"sourceRange": {"sources": [grid_range(cd_id, a_start_row, a_end_row, 1, 2)]}},
                             "targetAxis": "LEFT_AXIS"},
                            {"series": {"sourceRange": {"sources": [grid_range(cd_id, a_start_row, a_end_row, 2, 3)]}},
                             "targetAxis": "RIGHT_AXIS"},
                        ],
                        "headerCount": 0,
                    },
                },
                "position": {"overlayPosition": {
                    "anchorCell": {"sheetId": cd_id, "rowIndex": 7, "columnIndex": 0},
                    "widthPixels": 700, "heightPixels": 380}},
            }
        }
    })

    # ================= CHART 2: Volume theo AM =================
    requests.append({
        "addChart": {
            "chart": {
                "spec": {
                    "title": f"Volume theo AM - {weeks[-2]} vs {weeks[-1]}",
                    "basicChart": {
                        "chartType": "COLUMN",
                        "legendPosition": "BOTTOM_LEGEND",
                        "axis": [
                            {"position": "BOTTOM_AXIS", "title": "AM"},
                            {"position": "LEFT_AXIS", "title": "Volume"},
                        ],
                        "domains": [{"domain": {"sourceRange": {
                            "sources": [grid_range(cd_id, b_start_row, b_end_row, b_col0, b_col0 + 1)]}}}],
                        "series": [
                            {"series": {"sourceRange": {"sources": [grid_range(cd_id, b_start_row, b_end_row, b_col0 + 1, b_col0 + 2)]}}},
                            {"series": {"sourceRange": {"sources": [grid_range(cd_id, b_start_row, b_end_row, b_col0 + 2, b_col0 + 3)]}}},
                        ],
                        "headerCount": 0,
                    },
                },
                "position": {"overlayPosition": {
                    "anchorCell": {"sheetId": cd_id, "rowIndex": 28, "columnIndex": 0},
                    "widthPixels": 900, "heightPixels": 420}},
            }
        }
    })

    # ================= CHART 3: Doanh thu theo AM =================
    requests.append({
        "addChart": {
            "chart": {
                "spec": {
                    "title": f"Doanh thu theo AM - {weeks[-2]} vs {weeks[-1]}",
                    "basicChart": {
                        "chartType": "COLUMN",
                        "legendPosition": "BOTTOM_LEGEND",
                        "axis": [
                            {"position": "BOTTOM_AXIS", "title": "AM"},
                            {"position": "LEFT_AXIS", "title": "Doanh thu (VNĐ)"},
                        ],
                        "domains": [{"domain": {"sourceRange": {
                            "sources": [grid_range(cd_id, c_start_row, c_end_row, c_col0, c_col0 + 1)]}}}],
                        "series": [
                            {"series": {"sourceRange": {"sources": [grid_range(cd_id, c_start_row, c_end_row, c_col0 + 1, c_col0 + 2)]}}},
                            {"series": {"sourceRange": {"sources": [grid_range(cd_id, c_start_row, c_end_row, c_col0 + 2, c_col0 + 3)]}}},
                        ],
                        "headerCount": 0,
                    },
                },
                "position": {"overlayPosition": {
                    "anchorCell": {"sheetId": cd_id, "rowIndex": 28, "columnIndex": 11},
                    "widthPixels": 900, "heightPixels": 420}},
            }
        }
    })

    # ================= CHART 4: Doanh thu khách hàng mới theo tuần =================
    requests.append({
        "addChart": {
            "chart": {
                "spec": {
                    "title": "Doanh thu khách hàng mới toàn vùng theo tuần",
                    "basicChart": {
                        "chartType": "LINE",
                        "legendPosition": "BOTTOM_LEGEND",
                        "axis": [
                            {"position": "BOTTOM_AXIS", "title": "Tuần"},
                            {"position": "LEFT_AXIS", "title": "Doanh thu (VNĐ)"},
                        ],
                        "domains": [{"domain": {"sourceRange": {
                            "sources": [grid_range(cd_id, a_start_row, a_end_row, 0, 1)]}}}],
                        "series": [
                            {"series": {"sourceRange": {"sources": [grid_range(cd_id, a_start_row, a_end_row, 3, 4)]}}},
                        ],
                        "headerCount": 0,
                    },
                },
                "position": {"overlayPosition": {
                    "anchorCell": {"sheetId": cd_id, "rowIndex": 7, "columnIndex": 9},
                    "widthPixels": 700, "heightPixels": 380}},
            }
        }
    })

    # ================= CHART 5: Doanh thu khách hàng mới theo AM =================
    requests.append({
        "addChart": {
            "chart": {
                "spec": {
                    "title": f"Doanh thu khách hàng mới theo AM - {weeks[-2]} vs {weeks[-1]}",
                    "basicChart": {
                        "chartType": "COLUMN",
                        "legendPosition": "BOTTOM_LEGEND",
                        "axis": [
                            {"position": "BOTTOM_AXIS", "title": "AM"},
                            {"position": "LEFT_AXIS", "title": "Doanh thu (VNĐ)"},
                        ],
                        "domains": [{"domain": {"sourceRange": {
                            "sources": [grid_range(cd_id, d_start_row, d_end_row, d_col0, d_col0 + 1)]}}}],
                        "series": [
                            {"series": {"sourceRange": {"sources": [grid_range(cd_id, d_start_row, d_end_row, d_col0 + 1, d_col0 + 2)]}}},
                            {"series": {"sourceRange": {"sources": [grid_range(cd_id, d_start_row, d_end_row, d_col0 + 2, d_col0 + 3)]}}},
                        ],
                        "headerCount": 0,
                    },
                },
                "position": {"overlayPosition": {
                    "anchorCell": {"sheetId": cd_id, "rowIndex": 53, "columnIndex": 0},
                    "widthPixels": 900, "heightPixels": 420}},
            }
        }
    })

    sh.batch_update({"requests": requests})
    print(f"Done. Mở tab '{CHART_DATA_SHEET_NAME}' trong Google Sheet để xem 5 chart.")


if __name__ == "__main__":
    main()
