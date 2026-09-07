import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import unicodedata

# Configure output encoding for Vietnamese characters
sys.stdout.reconfigure(encoding='utf-8')

JSON_FILE = r'C:\Users\lap4all\Desktop\Backlog_Automation\credentials.json'
SHEET_ID = '1sTJEt8meKwVicbJAa8d7ml48yVoa_yD2_LAEbZ1ebGs'
ROSTER_PATH = r'c:\Users\lap4all\Desktop\New folder\ops_nhan_su.csv'
DESKTOP_DIR = os.path.join(os.path.expanduser('~'), 'Desktop')

print("="*60)
print("BẮT ĐẦU PIPELINE TỰ ĐỘNG HÓA BÁO CÁO TRUY THU OE-IA (W24)")
print("="*60)

# 1. Kết nối Google Sheets
print("🔄 Đang kết nối tới Google Sheets...")
creds = Credentials.from_service_account_file(
    JSON_FILE, 
    scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
)
gc = gspread.authorize(creds)
sh = gc.open_by_key(SHEET_ID)
print(f"✔️ Đã kết nối thành công tới spreadsheet: '{sh.title}'")

# Helper function to read worksheet to DataFrame
def get_df_from_sheet(sheet_name):
    print(f"  -> Đang tải dữ liệu từ tab '{sheet_name}'...")
    ws = sh.worksheet(sheet_name)
    data = ws.get_all_values()
    headers = data[0]
    # Handle any potential row length mismatch
    max_cols = max(len(row) for row in data)
    if len(headers) < max_cols:
        headers += [f"Unnamed_{i}" for i in range(len(headers)+1, max_cols+1)]
    df = pd.DataFrame(data[1:], columns=headers)
    return df

df_moi = get_df_from_sheet('data mới')
df_cu = get_df_from_sheet('data cũ')
df_cocau = get_df_from_sheet('CoCauVung')

# 2. Xử lý kiểu dữ liệu và chuẩn hóa
for df in [df_moi, df_cu]:
    for col in ['Số tiền ban đầu', 'Điều chỉnh (+|-)', 'Đã truy thu', 'Cần truy thu thêm']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

def normalize_name(name):
    if pd.isna(name): return ""
    return unicodedata.normalize('NFC', str(name).strip()).upper()

# Ánh xạ bưu cục sang AM (CoCauVung)
df_cocau['BC_norm'] = df_cocau['Bưu cục'].apply(normalize_name)
bc_to_am = dict(zip(df_cocau['BC_norm'], df_cocau['AM']))

def map_po_am(bc_name):
    norm = normalize_name(bc_name)
    if not norm: return ""
    if norm in bc_to_am: return bc_to_am[norm]
    # Fallback fuzzy matching
    for k, v in bc_to_am.items():
        if k in norm or norm in k:
            return v
    return ""

df_moi['AM_mapped'] = df_moi['Nơi vi phạm'].apply(map_po_am)
df_cu['AM_mapped'] = df_cu['Nơi vi phạm'].apply(map_po_am)

# 3. Đồng bộ cột AM và Cần hoàn trong tab 'data mới'
print("\n🔄 Đang xử lý chuẩn hóa cột AM (Nhân viên/Bưu cục) và Cần hoàn cho 'data mới'...")
# Tải danh sách nhân sự local
df_ns = pd.read_csv(ROSTER_PATH, dtype=str)
df_ns['ID_clean'] = df_ns['ID'].str.strip()
ns_id_to_am = dict(zip(df_ns['ID_clean'], df_ns['AM']))

def get_emp_id(name):
    if not name: return ""
    parts = str(name).split('-')
    return parts[0].strip() if parts else ""

df_moi['Emp_ID'] = df_moi['Nhân viên'].apply(get_emp_id)
df_moi['AM_emp'] = df_moi['Emp_ID'].apply(lambda x: ns_id_to_am.get(x, ""))
df_moi['AM_final'] = df_moi['AM_emp'].str.strip()
# Nếu không tìm thấy AM của nhân viên, dùng AM của Bưu cục vi phạm làm fallback
df_moi.loc[df_moi['AM_final'] == "", 'AM_final'] = df_moi['AM_mapped']
# Nếu vẫn trống, đặt là Unknown
df_moi.loc[df_moi['AM_final'] == "", 'AM_final'] = "Không xác định"

# Chuẩn bị upload cột P (Cần hoàn) và Q (AM) cho data mới
p_values = [[0, r['AM_final']] for _, r in df_moi.iterrows()]
ws_moi = sh.worksheet('data mới')
# Update range P2:Q{len(df_moi)+1}
range_pq = f"P2:Q{len(df_moi)+1}"
ws_moi.update(range_name=range_pq, values=p_values, value_input_option='USER_ENTERED')
print(f"✔️ Đã điền xong cột AM & Cần hoàn cho {len(df_moi)} dòng trong 'data mới'!")

# 4. Tính toán số liệu phân tích
print("\n📊 Đang tính toán các bảng phân tích dữ liệu tuần mới...")

# Định dạng số Việt Nam
def fmt_vn_currency(val):
    return f"{int(val):,}".replace(",", ".")

def fmt_vn_percentage(val):
    return f"{val*100:.2f}".replace(".", ",") + "%"

# --- Bảng tổng hợp 5 (Loại truy thu) ---
bth5 = df_moi.groupby('Loại truy thu').agg(
    ban_dau=('Số tiền ban đầu', 'sum'),
    dieu_chinh=('Điều chỉnh (+|-)', 'sum'),
    can_truy_thu=('Cần truy thu thêm', 'sum')
).reset_index().sort_values(by='Loại truy thu')

# --- Bảng tổng hợp 1 (Nơi vi phạm - lọc backlog) ---
exclude_types = ['Backlog Giao Hàng', 'Backlog Bắn Kiểm Lấy', 'Backlog Luân Chuyển Giao', 'Backlog Luân Chuyển Trả']
df_filtered = df_moi[~df_moi['Loại truy thu'].isin(exclude_types)]
bth1 = df_filtered.groupby('Nơi vi phạm').agg(
    ban_dau=('Số tiền ban đầu', 'sum'),
    dieu_chinh=('Điều chỉnh (+|-)', 'sum'),
    can_truy_thu=('Cần truy thu thêm', 'sum')
).reset_index().sort_values(by='can_truy_thu', ascending=False)

# --- Bảng tổng hợp 3 (Nơi vi phạm + AM nhân viên) ---
bth3_raw = df_moi.groupby(['Nơi vi phạm', 'AM_final']).agg(
    vol_phat=('Mã đơn hàng', 'count'),
    tam_tinh=('Số tiền ban đầu', 'sum')
).reset_index().sort_values(by=['tam_tinh', 'Nơi vi phạm'], ascending=[False, True])

# --- Bảng tổng hợp 6 (Tóm tắt theo AM bưu cục) ---
bth6_left = df_moi.groupby('AM_mapped').agg(
    tickets=('Mã ticket', 'count')
).reset_index().sort_values(by='tickets', ascending=False)

bth6_right = df_moi.groupby(['Nơi vi phạm', 'AM_mapped']).agg(
    vol_ticket=('Mã ticket', 'count'),
    tam_tinh=('Số tiền ban đầu', 'sum')
).reset_index().sort_values(by='tam_tinh', ascending=False)

# --- nd cần báo cáo summary text ---
total_moi = df_moi['Cần truy thu thêm'].sum()
total_cu = df_cu['Cần truy thu thêm'].sum()
diff = total_moi - total_cu
pct_change = diff / total_cu if total_cu > 0 else 0
trend_str = "tăng" if diff >= 0 else "giảm"

summary_title = f"Tổng truy thu Vùng: (Từ 01-07/06) có xu hướng {trend_str} {fmt_vn_percentage(abs(pct_change))}, {trend_str} {fmt_vn_currency(abs(diff))} so với cùng kỳ tuần 22 (Tổng: {fmt_vn_currency(total_cu)})"
print(f"\n📝 Tiêu đề báo cáo: \n{summary_title}")

# Helper function to convert column index to letter
def get_column_letter(col_idx):
    letter = ""
    while col_idx > 0:
        col_idx, remainder = divmod(col_idx - 1, 26)
        letter = chr(65 + remainder) + letter
    return letter

# 5. Cập nhật và định dạng các sheet báo cáo
def apply_table_styles(ws, num_rows, num_cols, is_bth3=False):
    # Font Segoe UI cho toàn bảng, Header xanh slate đậm, zebra striping
    header_format = {
        "backgroundColor": {"red": 30/255, "green": 41/255, "blue": 59/255},
        "horizontalAlignment": "CENTER",
        "textFormat": {"foregroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0}, "bold": True, "fontFamily": "Segoe UI", "fontSize": 11}
    }
    col_letter_end = get_column_letter(num_cols)
    ws.format(f"A1:{col_letter_end}1", header_format)
    ws.format(f"A2:{col_letter_end}{num_rows}", {"textFormat": {"fontFamily": "Segoe UI", "fontSize": 10}})
    
    # Grid lines visible
    sh.batch_update({
        "requests": [{
            "updateSheetProperties": {
                "properties": {"sheetId": ws.id, "gridProperties": {"hideGridlines": False}},
                "fields": "gridProperties.hideGridlines"
            }
        }]
    })
    
    # Alternating rows format
    requests = []
    for r in range(2, num_rows + 1):
        color = {"red": 248/255, "green": 250/255, "blue": 252/255} if r % 2 == 0 else {"red": 1.0, "green": 1.0, "blue": 1.0}
        requests.append({
            "repeatCell": {
                "range": {"sheetId": ws.id, "startRowIndex": r-1, "endRowIndex": r, "startColumnIndex": 0, "endColumnIndex": num_cols},
                "cell": {"userEnteredFormat": {"backgroundColor": color}},
                "fields": "userEnteredFormat.backgroundColor"
            }
        })
    sh.batch_update({"requests": requests})

def overwrite_and_format(sheet_name, headers, df_data, format_func=None, custom_rows=None):
    try:
        ws = sh.worksheet(sheet_name)
        ws.clear()
    except gspread.exceptions.WorksheetNotFound:
        ws = sh.add_worksheet(title=sheet_name, rows="500", cols="20")
        
    rows = [headers]
    if custom_rows is not None:
        rows.extend(custom_rows)
    else:
        for _, r in df_data.iterrows():
            rows.append(list(r))
            
    ws.resize(rows=max(len(rows)+20, 100), cols=max(len(headers)+5, 10))
    ws.update(range_name='A1', values=rows, value_input_option='USER_ENTERED')
    
    apply_table_styles(ws, len(rows), len(headers))
    if format_func:
        format_func(ws, len(rows))
    print(f"✔️ Đã cập nhật xong sheet '{sheet_name}'")

# Formatting Callbacks
def format_bth5(ws, num_rows):
    ws.format(f"B2:D{num_rows}", {"horizontalAlignment": "RIGHT", "numberFormat": {"type": "NUMBER", "pattern": "#,##0"}})
    ws.format(f"A{num_rows}:D{num_rows}", {"textFormat": {"bold": True}})

def format_bth1(ws, num_rows):
    ws.format(f"B2:D{num_rows}", {"horizontalAlignment": "RIGHT", "numberFormat": {"type": "NUMBER", "pattern": "#,##0"}})
    ws.format(f"A{num_rows}:D{num_rows}", {"textFormat": {"bold": True}})

def format_bth3(ws, num_rows):
    ws.format(f"C2:C{num_rows}", {"horizontalAlignment": "CENTER", "numberFormat": {"type": "NUMBER", "pattern": "#,##0"}})
    ws.format(f"D2:D{num_rows}", {"horizontalAlignment": "RIGHT", "numberFormat": {"type": "NUMBER", "pattern": "#,##0"}})

def format_bth6(ws, num_rows):
    # Left table format
    ws.format(f"B2:B{num_rows}", {"horizontalAlignment": "CENTER", "numberFormat": {"type": "NUMBER", "pattern": "#,##0"}})
    # Right table format (starts at column I, which is index 8)
    ws.format(f"K2:K{num_rows}", {"horizontalAlignment": "CENTER", "numberFormat": {"type": "NUMBER", "pattern": "#,##0"}})
    ws.format(f"L2:L{num_rows}", {"horizontalAlignment": "RIGHT", "numberFormat": {"type": "NUMBER", "pattern": "#,##0"}})

# Expose Bảng tổng hợp 5
b5_rows = []
for _, r in bth5.iterrows():
    b5_rows.append([r['Loại truy thu'], int(r['ban_dau']), int(r['dieu_chinh']), int(r['can_truy_thu'])])
b5_rows.append(['Tổng cộng', int(bth5['ban_dau'].sum()), int(bth5['dieu_chinh'].sum()), int(bth5['can_truy_thu'].sum())])
overwrite_and_format('Bảng tổng hợp 5', ['Loại truy thu', 'Số tiền ban đầu', 'Điều chỉnh (+|-)', 'Cần truy thu thêm'], None, format_bth5, b5_rows)

# Expose Bảng tổng hợp 1
b1_rows = []
for _, r in bth1.iterrows():
    b1_rows.append([r['Nơi vi phạm'], int(r['ban_dau']), int(r['dieu_chinh']), int(r['can_truy_thu'])])
b1_rows.append(['Tổng cộng', int(bth1['ban_dau'].sum()), int(bth1['dieu_chinh'].sum()), int(bth1['can_truy_thu'].sum())])
overwrite_and_format('Bảng tổng hợp 1', ['Nơi vi phạm', 'Số tiền ban đầu', 'Điều chỉnh (+|-)', 'Cần truy thu thêm'], None, format_bth1, b1_rows)

# Expose Bảng tổng hợp 3 (Format merge-like cell representation)
b3_rows = []
prev_bc = ""
for _, r in bth3_raw.iterrows():
    bc = r['Nơi vi phạm']
    disp_bc = "" if bc == prev_bc else bc
    prev_bc = bc
    b3_rows.append([disp_bc, r['AM_final'], int(r['vol_phat']), int(r['tam_tinh'])])
overwrite_and_format('Bảng tổng hợp 3', ['Nơi vi phạm', 'AM', 'Vol phạt', 'Số tiền tạm tính'], None, format_bth3, b3_rows)

# Expose Bảng tổng hợp 6 (Side-by-side)
b6_matrix = [["AM", " Mã ticket", "", "", "", "", "", "", "Nơi vi phạm", "AM", "Vol ticket", "Số tiền tạm tính"]]
b6_rows_left = list(bth6_left.iterrows())
b6_rows_right = list(bth6_right.iterrows())
max_b6_len = max(len(b6_rows_left), len(b6_rows_right))

for i in range(max_b6_len):
    row_val = [""] * 12
    if i < len(b6_rows_left):
        _, r_l = b6_rows_left[i]
        row_val[0] = r_l['AM_mapped']
        row_val[1] = int(r_l['tickets'])
    if i < len(b6_rows_right):
        _, r_r = b6_rows_right[i]
        row_val[8] = r_r['Nơi vi phạm']
        row_val[9] = r_r['AM_mapped']
        row_val[10] = int(r_r['vol_ticket'])
        row_val[11] = int(r_r['tam_tinh'])
    b6_matrix.append(row_val)

# Add Totals for left table
row_total_left = [""] * 12
row_total_left[0] = "Tổng cộng"
row_total_left[1] = int(bth6_left['tickets'].sum())
b6_matrix.append(row_total_left)

ws_bth6 = sh.worksheet('Bảng tổng hợp 6')
ws_bth6.clear()
ws_bth6.resize(rows=len(b6_matrix)+20, cols=15)
ws_bth6.update(range_name='A1', values=b6_matrix, value_input_option='USER_ENTERED')
apply_table_styles(ws_bth6, len(b6_matrix), 12)
format_bth6(ws_bth6, len(b6_matrix))
print("✔️ Đã cập nhật xong sheet 'Bảng tổng hợp 6'")

# 6. Cập nhật sheet 'nd cần báo cáo'
print("\n📝 Đang cấu hình và ghi dữ liệu sheet 'nd cần báo cáo'...")
report_rows = [
    [summary_title],
    [],
    ["1. TỔNG HỢP THEO LOẠI TRUY THU (W24)"],
    ["Loại truy thu", "Số tiền ban đầu", "Điều chỉnh (+|-)", "Cần truy thu thêm"]
]
# Add Bảng 5 rows
for r in b5_rows:
    report_rows.append(r)

# Spacer rows
report_rows.extend([[]] * 15)
report_rows.append(["2. TOP CÁC BC CÓ SỐ TRUY THU NHIỀU (Loại các đơn backlog giao - bắn kiểm - LC)"])
report_rows.append(["Nơi vi phạm", "Số tiền ban đầu", "Điều chỉnh (+|-)", "Cần truy thu thêm"])
# Add Bảng 1 rows (Limit to Top 30)
for r in b1_rows[:31]: # Top 30 plus the last row 'Tổng cộng'
    report_rows.append(r)
# Add overall total row at the end of the top 30
report_rows.append(b1_rows[-1]) # Total of all

# Spacer rows
report_rows.extend([[]] * 5)
report_rows.append(["3. SỐ LƯỢNG TICKET PHẠT THEO AM (W24)"])
report_rows.append(["AM", "Mã ticket"])
for _, r in bth6_left.iterrows():
    report_rows.append([r['AM_mapped'], int(r['tickets'])])
report_rows.append(["Tổng cộng", int(bth6_left['tickets'].sum())])

# Spacer rows
report_rows.extend([[]] * 3)
report_rows.append(["4. TOP 20 BƯU CỤC CÓ SỐ TICKET & TIỀN PHẠT NHIỀU NHẤT"])
report_rows.append(["Nơi vi phạm", "AM", "Vol ticket", "Số tiền tạm tính"])
for _, r in bth6_right.head(20).iterrows():
    report_rows.append([r['Nơi vi phạm'], r['AM_mapped'], int(r['vol_ticket']), int(r['tam_tinh'])])

# Overwrite sheet nd cần báo cáo
ws_rep = sh.worksheet('nd cần báo cáo')
ws_rep.clear()
ws_rep.resize(rows=len(report_rows)+30, cols=10)
ws_rep.update(range_name='A1', values=report_rows, value_input_option='USER_ENTERED')

# Format nd cần báo cáo sheet
# 1. Title format
ws_rep.format("A1", {
    "textFormat": {"bold": True, "fontFamily": "Segoe UI", "fontSize": 12, "foregroundColor": {"red": 15/255, "green": 23/255, "blue": 42/255}}
})

# 2. Section Headers
ws_rep.format("A3", {"textFormat": {"bold": True, "fontFamily": "Segoe UI", "fontSize": 11}})
# Find section 2
sec2_idx = report_rows.index(["2. TOP CÁC BC CÓ SỐ TRUY THU NHIỀU (Loại các đơn backlog giao - bắn kiểm - LC)"])
ws_rep.format(f"A{sec2_idx+1}", {"textFormat": {"bold": True, "fontFamily": "Segoe UI", "fontSize": 11}})
# Find section 3
sec3_idx = report_rows.index(["3. SỐ LƯỢNG TICKET PHẠT THEO AM (W24)"])
ws_rep.format(f"A{sec3_idx+1}", {"textFormat": {"bold": True, "fontFamily": "Segoe UI", "fontSize": 11}})
# Find section 4
sec4_idx = report_rows.index(["4. TOP 20 BƯU CỤC CÓ SỐ TICKET & TIỀN PHẠT NHIỀU NHẤT"])
ws_rep.format(f"A{sec4_idx+1}", {"textFormat": {"bold": True, "fontFamily": "Segoe UI", "fontSize": 11}})

# Format Headers of Tables
ws_rep.format(f"A4:D4", {
    "backgroundColor": {"red": 30/255, "green": 41/255, "blue": 59/255},
    "horizontalAlignment": "CENTER",
    "textFormat": {"foregroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0}, "bold": True, "fontFamily": "Segoe UI", "fontSize": 10}
})
ws_rep.format(f"B5:D15", {"horizontalAlignment": "RIGHT", "numberFormat": {"type": "NUMBER", "pattern": "#,##0"}})
ws_rep.format(f"A15:D15", {"textFormat": {"bold": True}})

# Format Table 2 Headers
ws_rep.format(f"A{sec2_idx+2}:D{sec2_idx+2}", {
    "backgroundColor": {"red": 30/255, "green": 41/255, "blue": 59/255},
    "horizontalAlignment": "CENTER",
    "textFormat": {"foregroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0}, "bold": True, "fontFamily": "Segoe UI", "fontSize": 10}
})
ws_rep.format(f"B{sec2_idx+3}:D{sec2_idx+35}", {"horizontalAlignment": "RIGHT", "numberFormat": {"type": "NUMBER", "pattern": "#,##0"}})
ws_rep.format(f"A{sec2_idx+34}:D{sec2_idx+35}", {"textFormat": {"bold": True}})

# Format Table 3 Headers
ws_rep.format(f"A{sec3_idx+2}:B{sec3_idx+2}", {
    "backgroundColor": {"red": 30/255, "green": 41/255, "blue": 59/255},
    "horizontalAlignment": "CENTER",
    "textFormat": {"foregroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0}, "bold": True, "fontFamily": "Segoe UI", "fontSize": 10}
})
ws_rep.format(f"B{sec3_idx+3}:B{sec3_idx+24}", {"horizontalAlignment": "CENTER", "numberFormat": {"type": "NUMBER", "pattern": "#,##0"}})
ws_rep.format(f"A{sec3_idx+24}:B{sec3_idx+24}", {"textFormat": {"bold": True}})

# Format Table 4 Headers
ws_rep.format(f"A{sec4_idx+2}:D{sec4_idx+2}", {
    "backgroundColor": {"red": 30/255, "green": 41/255, "blue": 59/255},
    "horizontalAlignment": "CENTER",
    "textFormat": {"foregroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0}, "bold": True, "fontFamily": "Segoe UI", "fontSize": 10}
})
ws_rep.format(f"C{sec4_idx+3}:C{sec4_idx+23}", {"horizontalAlignment": "CENTER", "numberFormat": {"type": "NUMBER", "pattern": "#,##0"}})
ws_rep.format(f"D{sec4_idx+3}:D{sec4_idx+23}", {"horizontalAlignment": "RIGHT", "numberFormat": {"type": "NUMBER", "pattern": "#,##0"}})

# Grid lines visible
sh.batch_update({
    "requests": [{
        "updateSheetProperties": {
            "properties": {"sheetId": ws_rep.id, "gridProperties": {"hideGridlines": False}},
            "fields": "gridProperties.hideGridlines"
        }
    }]
})
print("✔️ Đã cập nhật & định dạng thành công sheet 'nd cần báo cáo'")

# Helper function to delete old charts to prevent duplication
def delete_old_charts(sheet_id):
    try:
        sheet_metadata = sh.fetch_sheet_metadata()
        charts_to_delete = []
        for sheet in sheet_metadata.get('sheets', []):
            if sheet.get('properties', {}).get('sheetId') == sheet_id:
                for chart in sheet.get('charts', []):
                    charts_to_delete.append({
                        "deleteEmbeddedObject": {
                            "objectId": chart.get('chartId')
                        }
                    })
        if charts_to_delete:
            sh.batch_update({"requests": charts_to_delete})
            print(f"  -> Đã dọn dẹp {len(charts_to_delete)} biểu đồ cũ cho sheetId {sheet_id}.")
    except Exception as e:
        print(f"  ⚠️ Cảnh báo dọn dẹp biểu đồ: {e}")

# Chèn các biểu đồ tương tác lên Google Sheets
print("\n📊 Đang vẽ các biểu đồ trực tuyến tương tác lên Google Sheets...")
try:
    ws_b1 = sh.worksheet('Bảng tổng hợp 1')
    delete_old_charts(ws_b1.id)
    chart_b1 = {
        "addChart": {
            "chart": {
                "spec": {
                    "title": "TOP 10 BƯU CỤC CÓ SỐ TIỀN CẦN TRUY THU THÊM CAO NHẤT (W24)",
                    "basicChart": {
                        "chartType": "BAR",
                        "legendPosition": "NO_LEGEND",
                        "headerCount": 1,
                        "axis": [
                            {"position": "BOTTOM_AXIS", "title": "Số tiền cần truy thu thêm (VNĐ)"},
                            {"position": "LEFT_AXIS", "title": "Bưu cục vi phạm"}
                        ],
                        "domains": [
                            {"domain": {"sourceRange": {"sources": [{"sheetId": ws_b1.id, "startRowIndex": 0, "endRowIndex": 11, "startColumnIndex": 0, "endColumnIndex": 1}]}}}
                        ],
                        "series": [
                            {"series": {"sourceRange": {"sources": [{"sheetId": ws_b1.id, "startRowIndex": 0, "endRowIndex": 11, "startColumnIndex": 3, "endColumnIndex": 4}]}}, "targetAxis": "BOTTOM_AXIS"}
                        ]
                    }
                },
                "position": {
                    "overlayPosition": {
                        "anchorCell": {"sheetId": ws_b1.id, "rowIndex": 1, "columnIndex": 5},
                        "offsetXPixels": 0, "offsetYPixels": 0,
                        "widthPixels": 700, "heightPixels": 400
                    }
                }
            }
        }
    }

    ws_b5 = sh.worksheet('Bảng tổng hợp 5')
    delete_old_charts(ws_b5.id)
    chart_b5 = {
        "addChart": {
            "chart": {
                "spec": {
                    "title": "TỔNG SỐ TIỀN CẦN TRUY THU THEO LOẠI TRUY THU (W24)",
                    "basicChart": {
                        "chartType": "BAR",
                        "legendPosition": "NO_LEGEND",
                        "headerCount": 1,
                        "axis": [
                            {"position": "BOTTOM_AXIS", "title": "Số tiền cần truy thu thêm (VNĐ)"},
                            {"position": "LEFT_AXIS", "title": "Loại truy thu"}
                        ],
                        "domains": [
                            {"domain": {"sourceRange": {"sources": [{"sheetId": ws_b5.id, "startRowIndex": 0, "endRowIndex": len(bth5) + 1, "startColumnIndex": 0, "endColumnIndex": 1}]}}}
                        ],
                        "series": [
                            {"series": {"sourceRange": {"sources": [{"sheetId": ws_b5.id, "startRowIndex": 0, "endRowIndex": len(bth5) + 1, "startColumnIndex": 3, "endColumnIndex": 4}]}}, "targetAxis": "BOTTOM_AXIS"}
                        ]
                    }
                },
                "position": {
                    "overlayPosition": {
                        "anchorCell": {"sheetId": ws_b5.id, "rowIndex": 1, "columnIndex": 5},
                        "offsetXPixels": 0, "offsetYPixels": 0,
                        "widthPixels": 700, "heightPixels": 400
                    }
                }
            }
        }
    }

    ws_b6 = sh.worksheet('Bảng tổng hợp 6')
    delete_old_charts(ws_b6.id)
    chart_b6 = {
        "addChart": {
            "chart": {
                "spec": {
                    "title": "SỐ LƯỢNG TICKET PHẠT THEO DIỆN QUẢN LÝ CỦA AM (W24)",
                    "basicChart": {
                        "chartType": "BAR",
                        "legendPosition": "NO_LEGEND",
                        "headerCount": 1,
                        "axis": [
                            {"position": "BOTTOM_AXIS", "title": "Số lượng ticket phạt (tickets)"},
                            {"position": "LEFT_AXIS", "title": "AM"}
                        ],
                        "domains": [
                            {"domain": {"sourceRange": {"sources": [{"sheetId": ws_b6.id, "startRowIndex": 0, "endRowIndex": len(bth6_left) + 1, "startColumnIndex": 0, "endColumnIndex": 1}]}}}
                        ],
                        "series": [
                            {"series": {"sourceRange": {"sources": [{"sheetId": ws_b6.id, "startRowIndex": 0, "endRowIndex": len(bth6_left) + 1, "startColumnIndex": 1, "endColumnIndex": 2}]}}, "targetAxis": "BOTTOM_AXIS"}
                        ]
                    }
                },
                "position": {
                    "overlayPosition": {
                        "anchorCell": {"sheetId": ws_b6.id, "rowIndex": 1, "columnIndex": 2},
                        "offsetXPixels": 0, "offsetYPixels": 0,
                        "widthPixels": 450, "heightPixels": 350
                    }
                }
            }
        }
    }

    sh.batch_update({"requests": [chart_b1, chart_b5, chart_b6]})
    print("✔️ Đã vẽ thành công 3 biểu đồ tương tác lên Google Sheets!")
except Exception as ce:
    print(f"❌ Lỗi vẽ biểu đồ trên Google Sheets: {ce}")

# 7. Vẽ biểu đồ và lưu ra Desktop
print("\n📊 Đang vẽ các biểu đồ phân tích và lưu ra Desktop...")

def setup_light_theme():
    plt.style.use('default')
    plt.rcParams['figure.facecolor'] = '#FFFFFF'
    plt.rcParams['axes.facecolor'] = '#FFFFFF'
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Segoe UI', 'Roboto', 'Arial', 'sans-serif']
    plt.rcParams['text.color'] = '#1E293B'
    plt.rcParams['axes.labelcolor'] = '#64748B'
    plt.rcParams['xtick.color'] = '#64748B'
    plt.rcParams['ytick.color'] = '#64748B'

setup_light_theme()

# Chart 1: Top 10 Bưu cục có truy thu nhiều nhất (excluding backlog)
top_10_bc = bth1.head(10).sort_values(by='can_truy_thu', ascending=True)
fig, ax = plt.subplots(figsize=(12, 6.5))
bars = ax.barh(top_10_bc['Nơi vi phạm'], top_10_bc['can_truy_thu']/1e6, color='#EF4444', alpha=0.9, height=0.55)
ax.set_xlabel('Số tiền cần truy thu thêm (Triệu VNĐ)', fontsize=11, fontweight='bold', labelpad=10)
ax.set_title('TOP 10 BƯU CỤC CÓ SỐ TIỀN CẦN TRUY THU THÊM CAO NHẤT (W24)', fontsize=13, fontweight='bold', pad=20)
ax.grid(axis='x', linestyle=':', alpha=0.5, color='#CBD5E1')
for spine in ['top', 'right', 'bottom']: ax.spines[spine].set_visible(False)
ax.spines['left'].set_color('#CBD5E1')
for bar in bars:
    w = bar.get_width()
    ax.annotate(f'{w:.1f}M', xy=(w, bar.get_y() + bar.get_height() / 2), xytext=(5, 0), textcoords="offset points", ha='left', va='center', fontsize=9.5, fontweight='bold', color='#991B1B')
plt.tight_layout()
chart1_path = os.path.join(DESKTOP_DIR, "Top_10_BC_Truy_Thu_W24.png")
plt.savefig(chart1_path, dpi=300)
plt.close()
print(f"✔️ Đã lưu biểu đồ Top 10 bưu cục tại: {chart1_path}")

# Chart 2: Truy thu theo loại truy thu
top_types = bth5.sort_values(by='can_truy_thu', ascending=True)
fig, ax = plt.subplots(figsize=(12, 6.5))
bars = ax.barh(top_types['Loại truy thu'], top_types['can_truy_thu']/1e6, color='#3B82F6', alpha=0.9, height=0.55)
ax.set_xlabel('Số tiền cần truy thu thêm (Triệu VNĐ)', fontsize=11, fontweight='bold', labelpad=10)
ax.set_title('TỔNG SỐ TIỀN CẦN TRUY THU THEO LOẠI TRUY THU (W24)', fontsize=13, fontweight='bold', pad=20)
ax.grid(axis='x', linestyle=':', alpha=0.5, color='#CBD5E1')
for spine in ['top', 'right', 'bottom']: ax.spines[spine].set_visible(False)
ax.spines['left'].set_color('#CBD5E1')
for bar in bars:
    w = bar.get_width()
    if w > 0:
        ax.annotate(f'{w:.1f}M', xy=(w, bar.get_y() + bar.get_height() / 2), xytext=(5, 0), textcoords="offset points", ha='left', va='center', fontsize=9.5, fontweight='bold', color='#1E3A8A')
plt.tight_layout()
chart2_path = os.path.join(DESKTOP_DIR, "Truy_Thu_Theo_Loai_W24.png")
plt.savefig(chart2_path, dpi=300)
plt.close()
print(f"✔️ Đã lưu biểu đồ loại truy thu tại: {chart2_path}")

# Chart 3: Số tiền tạm tính theo AM
top_ams = bth6_left.sort_values(by='tickets', ascending=True)
fig, ax = plt.subplots(figsize=(12, 6.5))
bars = ax.barh(top_ams['AM_mapped'], top_ams['tickets'], color='#10B981', alpha=0.9, height=0.55)
ax.set_xlabel('Số lượng ticket phạt (tickets)', fontsize=11, fontweight='bold', labelpad=10)
ax.set_title('SỐ LƯỢNG TICKET PHẠT THEO DIỆN QUẢN LÝ CỦA AM (W24)', fontsize=13, fontweight='bold', pad=20)
ax.grid(axis='x', linestyle=':', alpha=0.5, color='#CBD5E1')
for spine in ['top', 'right', 'bottom']: ax.spines[spine].set_visible(False)
ax.spines['left'].set_color('#CBD5E1')
for bar in bars:
    w = bar.get_width()
    if w > 0:
        ax.annotate(f'{w:,.0f}', xy=(w, bar.get_y() + bar.get_height() / 2), xytext=(5, 0), textcoords="offset points", ha='left', va='center', fontsize=9.5, fontweight='bold', color='#064E3B')
plt.tight_layout()
chart3_path = os.path.join(DESKTOP_DIR, "Truy_Thu_Theo_AM_W24.png")
plt.savefig(chart3_path, dpi=300)
plt.close()
print(f"✔️ Đã lưu biểu đồ ticket theo AM tại: {chart3_path}")

print("\n🎉 HOÀN THÀNH TẠO TOÀN BỘ BÁO CÁO & DASHBOARD TRUY THU THÀNH CÔNG!")
print("="*60)
