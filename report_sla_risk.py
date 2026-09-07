# -*- coding: utf-8 -*-
"""
BÁO CÁO CẢNH BÁO ĐƠN CHẠM / SẮP QUÁ HẠN SLA CẦN XỬ LÝ GẤP (TRUY THU QUÁ HẠN)
- Dashboard 6 ô KPI chuẩn điều hành (Tổng tồn, Tại Hub, Chưa về Hub, Đứng yên ≥ 2 ngày cần báo GDV, Chưa gán LM, Đã xử lý xong)
- Phân bổ theo AM và Top 5 Bưu cục tồn cao nhất kèm chi tiết Đứng yên ≥ 2 ngày & Chưa gán LM
- Render ảnh HD Playwright & Gửi tin tổng hợp lên GTalk Group chính
- Tách và cập nhật tab chi tiết cho từng AM trên Google Sheet
"""

import os
import sys
import io
import json
import re
import time
import unicodedata
from datetime import datetime, timedelta
import pandas as pd
import requests
import gspread
from google.oauth2.service_account import Credentials
from google.oauth2.credentials import Credentials as UserCredentials
from playwright.sync_api import sync_playwright

# Fix encoding cho Windows Command Prompt / Task Scheduler
os.environ['PYTHONIOENCODING'] = 'utf-8'
try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
except AttributeError:
    pass

# ==============================================================================
# CẤU HÌNH HỆ THỐNG
# ==============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 🔑 Cấu hình Google Sheet
SHEET_KEY = '1YlLYFhCioAelNLaLyHg95UmH6QuasvEP50fcp-A-Yg4'
DATA_TAB_NAME = 'data'
PIVOT_TAB_NAME = 'PIVOT SLA'

SNAPSHOT_FILE = os.path.join(BASE_DIR, 'snapshot_sla_risk.json')

# 🤖 Cấu hình GTalk Bot & Kênh tổng hợp (Group Tổng)
GTALK_TOKEN = "2067164759497973760:RfgqBJY4QtV18udu1wMEfhmoRNI4hgBv"
GTALK_CHANNEL_MAIN = "2073027751071649792"

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

SLOT_COLORS = [
    {"name": "Amber",   "data_bg": "#FEF3C7", "total_bg": "#FDE68A", "header_bg": "#F59E0B", "fg": "#78350F"},
    {"name": "Emerald", "data_bg": "#D1FAE5", "total_bg": "#A7F3D0", "header_bg": "#10B981", "fg": "#065F46"},
    {"name": "Blue",    "data_bg": "#DBEAFE", "total_bg": "#BFDBFE", "header_bg": "#3B82F6", "fg": "#1E40AF"},
    {"name": "Pink",    "data_bg": "#FCE7F3", "total_bg": "#FBCFE8", "header_bg": "#EC4899", "fg": "#9D174D"},
    {"name": "Teal",    "data_bg": "#CCFBF1", "total_bg": "#99F6E4", "header_bg": "#14B8A6", "fg": "#0F766E"},
    {"name": "Purple",  "data_bg": "#F3E5F5", "total_bg": "#E1BEE7", "header_bg": "#8B5CF6", "fg": "#6B21A8"},
]

# ==============================================================================
# HÀM BỔ TRỢ
# ==============================================================================
def normalize_str(s):
    if s is None:
        return ""
    return unicodedata.normalize('NFC', str(s).strip())

def parse_datetime(dt_str):
    if not dt_str:
        return None
    dt_str = str(dt_str).strip()
    for fmt in [
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%Y %H:%M",
        "%Y-%m-%d"
    ]:
        try:
            return datetime.strptime(dt_str, fmt)
        except ValueError:
            pass
    try:
        clean_str = dt_str.split('+')[0].split('Z')[0]
        if '.' in clean_str:
            base, frac = clean_str.split('.')
            frac = (frac + '000000')[:6]
            clean_str = f"{base}.{frac}"
            return datetime.strptime(clean_str, "%Y-%m-%dT%H:%M:%S.%f")
    except Exception:
        pass
    return None

def retry_gspread(func, *args, max_retries=6, initial_delay=3, **kwargs):
    delay = initial_delay
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            err_str = str(e)
            if any(k in err_str for k in ["429", "Quota exceeded", "RESOURCE_EXHAUSTED", "LIMIT_EXCEEDED", "timed out", "TimeoutError"]):
                print(f"⚠️ Google Sheets API Quota / Timeout. Chờ {delay}s thử lại (lần {attempt+1}/{max_retries})...")
                time.sleep(delay)
                delay *= 1.5
            else:
                raise e
    return func(*args, **kwargs)

def get_gspread_client(sheet_key=None):
    cred_paths = [
        os.path.join(BASE_DIR, 'credentials.json'),
        r'C:\Users\lap4all\Documents\Auto report\credentials.json',
        r'C:\Users\lap4all\Desktop\Backlog_Automation\credentials.json',
        r'C:\Users\lap4all\Downloads\credentials.json'
    ]
    for json_file in cred_paths:
        if os.path.exists(json_file):
            try:
                creds = Credentials.from_service_account_file(json_file, scopes=SCOPES)
                gc = gspread.authorize(creds)
                if sheet_key:
                    gc.open_by_key(sheet_key)
                return gc
            except Exception:
                pass

    auth_paths = [
        os.path.join(BASE_DIR, 'authorized_user.json'),
        r'C:\Users\lap4all\Documents\Auto report\authorized_user.json',
        r'C:\Users\lap4all\Desktop\Backlog_Automation\authorized_user.json'
    ]
    for auth_user_file in auth_paths:
        if os.path.exists(auth_user_file):
            try:
                creds = UserCredentials.from_authorized_user_file(auth_user_file, scopes=SCOPES)
                gc = gspread.authorize(creds)
                if sheet_key:
                    gc.open_by_key(sheet_key)
                return gc
            except Exception:
                pass

    raise PermissionError("❌ Không thể xác thực Google Sheets. Vui lòng kiểm tra credentials.json hoặc authorized_user.json")

def find_col_idx(headers, possible_names):
    headers_lower = [normalize_str(h).lower() for h in headers]
    for name in possible_names:
        name_lower = normalize_str(name).lower()
        if name_lower in headers_lower:
            return headers_lower.index(name_lower)
    return -1

def is_unassigned_lm(lm_val):
    if not lm_val:
        return True
    val = normalize_str(lm_val).lower()
    if 'đang có chuyến' in val or 'dang co chuyen' in val:
        return False
    return True

def is_done_case(cur_st, st_vi="", raw_st="", order_type_or_action=""):
    """
    LOGIC DONE CASE (ĐÃ XỬ LÝ XONG):
    1. BẤT KỲ ĐƠN NÀO có status là delivered, returned hoặc lost (không quan tâm loại quá hạn gì) 
       -> Đều lập tức tính là DONE CASE!
    2. Đơn ban đầu là chiều giao (Loại quá hạn là "giao" / action_status có "CHƯA GTC") 
       nhưng hiện tại trạng thái đã chuyển sang luồng chuyển hoàn 
       (return, returning, return_transporting, return_sorting, waiting_to_return, chuyển hoàn, trả hàng...)
       -> Cũng tính là DONE CASE (vì bưu cục giao đã kết thúc trách nhiệm giao hàng).
    """
    c = normalize_str(cur_st).lower()
    v = normalize_str(st_vi).lower()
    r = normalize_str(raw_st).lower()
    a = normalize_str(order_type_or_action).lower()

    all_st = f"{c} {v} {r}".strip()

    # 1. Bất kể loại quá hạn gì: cứ delivered, returned hoặc lost là ĐÃ XỬ LÝ XONG (Done Case)
    if any(k in all_st for k in [
        'delivered', 'returned', 'lost',
        'giao thành công', 'giao thanh cong',
        'trả hàng thành công', 'tra hang thanh cong',
        'chuyển trả thành công', 'chuyen tra thanh cong',
        'thất lạc', 'that lac', 'hàng thất lạc', 'hang that lac'
    ]):
        return True

    # 2. Đơn ban đầu là chiều giao nhưng hiện tại đã chuyển sang luồng hoàn trả
    is_delivery = any(k in a for k in ['giao', 'chưa gtc', 'chua gtc', 'cần xử lý tiếp', 'can xu ly tiep'])
    if is_delivery:
        if any(k in all_st for k in [
            'return', 'returning', 'return_transporting', 'return_sorting', 'waiting_to_return',
            'chuyển hoàn', 'chuyen hoan', 'đang chuyển hoàn', 'dang chuyen hoan',
            'trả hàng', 'tra hang', 'đang trả hàng', 'dang tra hang', 'chuyển trả'
        ]):
            return True

    return False

# ==============================================================================
# QUẢN LÝ SNAPSHOT LỊCH SỬ
# ==============================================================================
def load_snapshot_state(today_str):
    state = {"last_updated_date": today_str, "history": [], "daily_snapshots": {}}
    if os.path.exists(SNAPSHOT_FILE):
        try:
            with open(SNAPSHOT_FILE, "r", encoding="utf-8") as f:
                state = json.load(f)
        except Exception:
            pass

    if state.get("last_updated_date") != today_str:
        prev_date = state.get("last_updated_date")
        if prev_date and len(state.get("history", [])) > 0:
            prev_key = prev_date.replace("-", "")
            first_snap = state["history"][0]
            state["daily_snapshots"][prev_key] = {
                "totals": first_snap.get("totals", {}),
                "grandTotal": sum(first_snap.get("totals", {}).values())
            }
        state["history"] = []
        state["last_updated_date"] = today_str

    return state

def save_snapshot_state(state):
    with open(SNAPSHOT_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

# ==============================================================================
# HÀM FORMAT SHEETS
# ==============================================================================
def make_color(hex_str):
    hex_str = hex_str.lstrip('#')
    return {
        "red": int(hex_str[0:2], 16) / 255.0,
        "green": int(hex_str[2:4], 16) / 255.0,
        "blue": int(hex_str[4:6], 16) / 255.0
    }

def cell_format_request(sheet_id, start_row, end_row, start_col, end_col, format_dict):
    return {
        "repeatCell": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": start_row,
                "endRowIndex": end_row,
                "startColumnIndex": start_col,
                "endColumnIndex": end_col
            },
            "cell": {
                "userEnteredFormat": format_dict
            },
            "fields": "userEnteredFormat(" + ",".join(format_dict.keys()) + ")"
        }
    }

def unmerge_request(sheet_id):
    return {
        "unmergeCells": {
            "range": {
                "sheetId": sheet_id
            }
        }
    }

def merge_request(sheet_id, start_row, end_row, start_col, end_col):
    return {
        "mergeCells": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": start_row,
                "endRowIndex": end_row,
                "startColumnIndex": start_col,
                "endColumnIndex": end_col
            },
            "mergeType": "MERGE_ALL"
        }
    }

def row_height_request(sheet_id, start_row, end_row, height):
    return {
        "updateDimensionProperties": {
            "range": {
                "sheetId": sheet_id,
                "dimension": "ROWS",
                "startIndex": start_row,
                "endIndex": end_row
            },
            "properties": {"pixelSize": height},
            "fields": "pixelSize"
        }
    }

def col_width_request(sheet_id, start_col, end_col, width):
    return {
        "updateDimensionProperties": {
            "range": {
                "sheetId": sheet_id,
                "dimension": "COLUMNS",
                "startIndex": start_col,
                "endIndex": end_col
            },
            "properties": {"pixelSize": width},
            "fields": "pixelSize"
        }
    }

def border_request(sheet_id, start_row, end_row, start_col, end_col, color_hex="#BDC3C7"):
    color = make_color(color_hex)
    border_style = {"style": "SOLID", "color": color}
    return {
        "updateBorders": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": start_row,
                "endRowIndex": end_row,
                "startColumnIndex": start_col,
                "endColumnIndex": end_col
            },
            "top": border_style,
            "bottom": border_style,
            "left": border_style,
            "right": border_style,
            "innerHorizontal": border_style,
            "innerVertical": border_style
        }
    }

# ==============================================================================
# QUY TRÌNH TÍNH TOÁN & CẬP NHẬT BÁO CÁO SLA
# ==============================================================================
def run_sla_risk_report():
    print(f"🚀 [BẮT ĐẦU] Báo cáo SLA & Đơn sắp quá hạn lúc: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    current_dt = datetime.now()
    current_time = current_dt.strftime("%H:%M")
    today_str = current_dt.strftime("%Y-%m-%d")
    today_display = current_dt.strftime("%d/%m/%Y")
    today_key = current_dt.strftime("%Y%m%d")

    gc_client = get_gspread_client(SHEET_KEY)
    sh = gc_client.open_by_key(SHEET_KEY)

    # 1. Đọc dữ liệu từ tab 'data'
    all_worksheets_dict = {ws.title: ws for ws in sh.worksheets()}
    
    if DATA_TAB_NAME not in all_worksheets_dict:
        print(f"❌ Không tìm thấy tab '{DATA_TAB_NAME}' trong Google Sheet: {sh.title}")
        return

    ws_data = all_worksheets_dict[DATA_TAB_NAME]
    print(f"📖 Đọc dữ liệu từ tab: '{ws_data.title}' (Sheet: '{sh.title}')...")

    raw_data = ws_data.get_all_values()
    if len(raw_data) < 2:
        print("❌ Dữ liệu bảng trống hoặc chỉ có header.")
        return

    header = raw_data[0]
    
    # Đảm bảo nhận diện linh hoạt mọi biến thể tên cột (cả bảng cũ lẫn bảng mới sau khi xóa/đổi cột)
    col_order = find_col_idx(header, ["order_code", "mã đơn hàng", "mã đơn", "madh", "ordercode"])
    col_current_status = find_col_idx(header, ["status", "current_status", "trạng thái hiện tại", "currentstatus"])
    col_status_start_en = find_col_idx(header, ["sstatus_en_startday", "current_status", "status"])
    col_status_vi = find_col_idx(header, ["status_vi", "trạng thái vi", "trạng thái tiếng việt", "sstatus_vi_startday", "trạng thái"])
    col_cur_wid = find_col_idx(header, ["current_warehouse_id", "id kho hiện tại", "id_bc_ht"])
    col_del_wid = find_col_idx(header, ["deliver_warehouse_id", "delivery_warehouse_id", "id kho giao", "id_bc_giao"])
    col_cur_wh_name = find_col_idx(header, ["khohientai", "current_warehouse_name", "kho hiện tại", "bưu cục hiện tại", "bc hiện tại"])
    col_del_wh_name = find_col_idx(header, ["khogiao", "delivery_warehouse_name", "kho giao", "bưu cục giao"])
    col_am_ht = find_col_idx(header, ["am (ht)", "am_ht", "am hiện tại", "am (kho hiện tại)"])
    col_am_dl = find_col_idx(header, ["am (dl)", "am_dl", "am giao", "am (kho giao)"])
    col_action_status = find_col_idx(header, ["action_status", "trạng thái xử lý", "hành động", "loại quá hạn", "loai qua han"])
    col_status = find_col_idx(header, ["status", "trạng thái", "currentstatus"])
    col_lm = find_col_idx(header, ["lm", "chuyến đi", "trip", "trạng thái lm"])
    col_aging = find_col_idx(header, ["aging", "thời gian tồn đọng", "thoi gian ton dong", "thời gian tồn"])
    col_updated_time = find_col_idx(header, ["status_updated_time_hcm", "thời gian cập nhật", "updated_time", "status_updated_time", "endpicktime", "ngày update", "ngay update"])

    if col_order == -1:
        print("❌ Không tìm thấy cột 'order_code' / 'MaDH' trong dữ liệu.")
        return

    # Tra cứu bổ sung từ tab 'status' nếu cột status trong data bị thiếu/trống
    st_dict = {}
    if "status" in all_worksheets_dict:
        try:
            st_rows = all_worksheets_dict["status"].get_all_values()
            if len(st_rows) > 1:
                st_dict = {r[0].strip(): r[2].strip() for r in st_rows[1:] if len(r) > 2 and r[0].strip()}
        except Exception as e:
            print(f"⚠️ Không thể đọc tab status: {e}")

    # 2. Xử lý & Phân loại đơn hàng: ACTIVE vs DONE CASE & ĐỨNG YÊN >= 2 NGÀY
    active_orders = []
    done_orders_by_am = {}
    done_orders_by_bc = {}
    status_counts_global = {}
    total_at_hub_giao = 0
    total_not_at_hub_giao = 0
    total_done_count = 0
    total_stagnant_2d = 0
    
    for row_idx, row in enumerate(raw_data[1:]):
        if len(row) <= col_order:
            continue
        order_code = normalize_str(row[col_order])
        if not order_code:
            continue

        # Lấy trạng thái hiện tại (real-time)
        cur_status = normalize_str(row[col_current_status]) if col_current_status != -1 and len(row) > col_current_status else ""
        if not cur_status and order_code in st_dict:
            cur_status = st_dict[order_code]
        if not cur_status and col_status_start_en != -1 and len(row) > col_status_start_en:
            cur_status = normalize_str(row[col_status_start_en])
        if not cur_status:
            cur_status = "Khác"

        status_vi_val = normalize_str(row[col_status_vi]) if col_status_vi != -1 and len(row) > col_status_vi else ""
        action_status_val = normalize_str(row[col_action_status]) if col_action_status != -1 and len(row) > col_action_status else ""
        status_val = normalize_str(row[col_status]) if col_status != -1 and len(row) > col_status else ""

        # Lấy AM theo kho hiện tại (AM (ht))
        am_name = normalize_str(row[col_am_ht]) if col_am_ht != -1 and len(row) > col_am_ht else ""
        if not am_name or am_name.upper() in ['#N/A', '#N-A', 'N/A', 'NONE', '', 'NULL']:
            am_name = "Chưa gán AM"

        # Lấy kho/bưu cục hiện tại & kho giao
        cur_wh = normalize_str(row[col_cur_wh_name]) if col_cur_wh_name != -1 and len(row) > col_cur_wh_name else "Không xác định"
        if not cur_wh:
            cur_wh = "Không xác định"
        del_wh = normalize_str(row[col_del_wh_name]) if col_del_wh_name != -1 and len(row) > col_del_wh_name else "Không xác định"

        # Kiểm tra nếu là DONE CASE (giao TC / trả TC / thất lạc / đơn chiều giao bị chuyển hoàn)
        if is_done_case(cur_status, status_vi_val, status_val, action_status_val):
            total_done_count += 1
            done_orders_by_am[am_name] = done_orders_by_am.get(am_name, 0) + 1
            done_orders_by_bc[cur_wh] = done_orders_by_bc.get(cur_wh, 0) + 1
            continue

        # Các đơn còn tồn (ACTIVE CASE)
        cur_wid = normalize_str(row[col_cur_wid]) if col_cur_wid != -1 and len(row) > col_cur_wid else ""
        del_wid = normalize_str(row[col_del_wid]) if col_del_wid != -1 and len(row) > col_del_wid else ""
        
        is_at_hub = False
        if cur_wid and del_wid:
            if cur_wid == del_wid:
                is_at_hub = True
        elif cur_wh and del_wh and cur_wh != "Không xác định" and del_wh != "Không xác định":
            if cur_wh.lower() == del_wh.lower():
                is_at_hub = True

        if is_at_hub:
            total_at_hub_giao += 1
        else:
            total_not_at_hub_giao += 1

        lm_val = row[col_lm] if col_lm != -1 and len(row) > col_lm else ""
        unassigned = is_unassigned_lm(lm_val)

        # Tính đơn đứng yên >= 2 ngày (>= 48 giờ)
        is_stagnant = False
        if col_aging != -1 and len(row) > col_aging:
            aging_val = normalize_str(row[col_aging]).lower()
            if any(k in aging_val for k in ['48', '72', '96', '120', '192']):
                is_stagnant = True

        if not is_stagnant and col_updated_time != -1 and len(row) > col_updated_time:
            up_time_str = row[col_updated_time]
            dt_up = parse_datetime(up_time_str)
            if dt_up:
                diff_hours = (current_dt - dt_up).total_seconds() / 3600.0
                if diff_hours >= 48:
                    is_stagnant = True

        if is_stagnant:
            total_stagnant_2d += 1

        order_obj = {
            "order_code": order_code,
            "am": am_name,
            "current_status": cur_status,
            "status_vi": status_vi_val,
            "current_wh": cur_wh,
            "is_at_hub": is_at_hub,
            "lm": lm_val,
            "is_unassigned": unassigned,
            "is_stagnant": is_stagnant,
            "raw": row
        }

        active_orders.append(order_obj)
        status_counts_global[cur_status] = status_counts_global.get(cur_status, 0) + 1

    total_active = len(active_orders)
    total_unassigned = sum(1 for o in active_orders if o['is_unassigned'])
    print(f"📊 Tổng đơn cần xử lý: {total_active:,} đơn (Tại HUB: {total_at_hub_giao:,} | Chưa về HUB: {total_not_at_hub_giao:,} | Chưa gán LM: {total_unassigned:,} | Đứng yên ≥ 2 ngày: {total_stagnant_2d:,}) | Đã xử lý xong: {total_done_count:,} đơn")

    # 3. Danh sách AM và Status columns
    all_ams_set = set(o['am'] for o in active_orders if o['am'] != "Chưa gán AM")
    for am in done_orders_by_am.keys():
        if am != "Chưa gán AM":
            all_ams_set.add(am)
    all_ams = sorted(list(all_ams_set))
    if any(o['am'] == "Chưa gán AM" for o in active_orders) or "Chưa gán AM" in done_orders_by_am:
        all_ams.append("Chưa gán AM")

    sorted_status_tuples = sorted(status_counts_global.items(), key=lambda x: x[1], reverse=True)
    status_columns = [s[0] for s in sorted_status_tuples if s[1] > 0]
    if not status_columns:
        status_columns = ["storing", "delivering", "transporting"]

    # Pivot Map theo AM
    am_pivot = {}
    for am in all_ams:
        am_pivot[am] = {s: 0 for s in status_columns}
        am_pivot[am]['total'] = 0
        am_pivot[am]['unassigned'] = 0
        am_pivot[am]['stagnant'] = 0
        am_pivot[am]['at_hub'] = 0
        am_pivot[am]['not_at_hub'] = 0
        am_pivot[am]['done'] = done_orders_by_am.get(am, 0)

    for o in active_orders:
        am = o['am']
        st = o['current_status']
        if am in am_pivot:
            if st in am_pivot[am]:
                am_pivot[am][st] += 1
            am_pivot[am]['total'] += 1
            if o['is_unassigned']:
                am_pivot[am]['unassigned'] += 1
            if o['is_stagnant']:
                am_pivot[am]['stagnant'] += 1
            if o['is_at_hub']:
                am_pivot[am]['at_hub'] += 1
            else:
                am_pivot[am]['not_at_hub'] += 1

    # Thống kê theo Bưu Cục hiện tại
    bc_pivot = {}
    for o in active_orders:
        bc = o['current_wh']
        st = o['current_status']
        am = o['am']
        if bc not in bc_pivot:
            bc_pivot[bc] = {s: 0 for s in status_columns}
            bc_pivot[bc]['am'] = am
            bc_pivot[bc]['total'] = 0
            bc_pivot[bc]['unassigned'] = 0
            bc_pivot[bc]['stagnant'] = 0
            bc_pivot[bc]['done'] = done_orders_by_bc.get(bc, 0)
        if st in bc_pivot[bc]:
            bc_pivot[bc][st] += 1
        bc_pivot[bc]['total'] += 1
        if o['is_unassigned']:
            bc_pivot[bc]['unassigned'] += 1
        if o['is_stagnant']:
            bc_pivot[bc]['stagnant'] += 1

    sorted_bcs = sorted(bc_pivot.items(), key=lambda x: x[1]['total'], reverse=True)
    top5_bcs = sorted_bcs[:5]
    top5_bc_names = [x[0] for x in top5_bcs]

    # 4. Cập nhật Snapshot mốc thời gian
    state = load_snapshot_state(today_str)
    current_am_totals = {am: am_pivot[am]['total'] for am in all_ams}
    current_bc_totals = {bc: stats['total'] for bc, stats in bc_pivot.items()}

    current_snap = {
        "time": current_time,
        "totals": current_am_totals,
        "doneTotals": {am: am_pivot[am]['done'] for am in all_ams},
        "unassignedTotals": {am: am_pivot[am]['unassigned'] for am in all_ams},
        "stagnantTotals": {am: am_pivot[am]['stagnant'] for am in all_ams},
        "bcTotals": current_bc_totals,
        "grandTotal": total_active,
        "grandDone": total_done_count,
        "totalAtHub": total_at_hub_giao,
        "totalNotAtHub": total_not_at_hub_giao,
        "grandUnassigned": total_unassigned,
        "grandStagnant": total_stagnant_2d
    }

    if len(state["history"]) == 0:
        state["history"].append(current_snap)
        state["daily_snapshots"][today_key] = {
            "totals": current_am_totals,
            "grandTotal": total_active
        }
    elif len(state["history"]) == 1:
        state["history"].append(current_snap)
    else:
        state["history"][1] = current_snap

    save_snapshot_state(state)
    history = state["history"]

    # 5. Cập nhật Sheet PIVOT SLA trên Google Sheets
    print(f"📝 Đang cập nhật Sheet '{PIVOT_TAB_NAME}'...")
    if PIVOT_TAB_NAME in all_worksheets_dict:
        ws_pivot = all_worksheets_dict[PIVOT_TAB_NAME]
    else:
        ws_pivot = retry_gspread(sh.add_worksheet, title=PIVOT_TAB_NAME, rows="150", cols="25")
        all_worksheets_dict[PIVOT_TAB_NAME] = ws_pivot
    
    retry_gspread(ws_pivot.clear)

    grid_values = []
    requests_format = [unmerge_request(ws_pivot.id)]

    # Header Row 1: Tiêu đề lớn
    headers_t1 = ['AM (Kho hiện tại)'] + status_columns + ['Tổng còn tồn (Chưa gán LM)', 'Đứng yên ≥ 2 ngày', 'Đã xử lý xong (Done)']
    for i, snap in enumerate(history):
        headers_t1.append(f"Mốc {snap['time']}")
        if i > 0:
            headers_t1.append("Tăng/Giảm (+/-)")

    num_cols = len(headers_t1)
    grid_values.append([f"BÁO CÁO ĐƠN CHẠM / SẮP QUÁ HẠN SLA CẦN XỬ LÝ GẤP — MỐC {current_time} NGÀY {today_str}"] + [''] * (num_cols - 1))
    requests_format.append(merge_request(ws_pivot.id, 0, 1, 0, num_cols))
    requests_format.append(cell_format_request(ws_pivot.id, 0, 1, 0, num_cols, {
        "backgroundColor": make_color("#1E3A8A"),
        "textFormat": {"bold": True, "fontSize": 12, "fontFamily": "Arial", "foregroundColor": make_color("#FFFFFF")},
        "horizontalAlignment": "CENTER",
        "verticalAlignment": "MIDDLE"
    }))
    requests_format.append(row_height_request(ws_pivot.id, 0, 1, 35))

    # Header Row 2: Các cột
    grid_values.append(headers_t1)
    requests_format.append(cell_format_request(ws_pivot.id, 1, 2, 0, len(headers_t1), {
        "backgroundColor": make_color("#2563EB"),
        "textFormat": {"bold": True, "fontSize": 10, "fontFamily": "Arial", "foregroundColor": make_color("#FFFFFF")},
        "horizontalAlignment": "CENTER",
        "verticalAlignment": "MIDDLE"
    }))
    requests_format.append(row_height_request(ws_pivot.id, 1, 2, 28))

    # Dữ liệu Table 1: Theo AM
    sorted_ams = sorted(all_ams, key=lambda x: am_pivot[x]['total'], reverse=True)
    t1_start_row = 2

    for r_idx, am in enumerate(sorted_ams):
        row_idx = t1_start_row + r_idx
        tot = am_pivot[am]['total']
        unas = am_pivot[am]['unassigned']
        stag = am_pivot[am]['stagnant']
        done = am_pivot[am]['done']
        unas_str = f" ({unas} chưa gán)" if unas > 0 else ""
        row = [am]
        for st in status_columns:
            row.append(am_pivot[am][st])
        row.append(f"{tot}{unas_str}")
        row.append(stag)
        row.append(done)

        for h_idx, snap in enumerate(history):
            snap_val = snap["totals"].get(am, 0)
            row.append(snap_val)
            if h_idx > 0:
                prev_val = history[h_idx - 1]["totals"].get(am, 0)
                diff = snap_val - prev_val
                row.append("—" if diff == 0 else f"+ {diff}" if diff > 0 else f"- {abs(diff)}")

        grid_values.append(row)
        bg = "#F8FAFC" if r_idx % 2 == 0 else "#FFFFFF"
        requests_format.append(cell_format_request(ws_pivot.id, row_idx, row_idx+1, 0, 1, {
            "backgroundColor": make_color("#E0E7FF"),
            "textFormat": {"bold": True, "fontSize": 9, "fontFamily": "Arial"},
            "horizontalAlignment": "LEFT",
            "verticalAlignment": "MIDDLE"
        }))
        requests_format.append(cell_format_request(ws_pivot.id, row_idx, row_idx+1, 1, len(headers_t1), {
            "backgroundColor": make_color(bg),
            "textFormat": {"fontSize": 9, "fontFamily": "Arial"},
            "horizontalAlignment": "CENTER",
            "verticalAlignment": "MIDDLE"
        }))
        requests_format.append(row_height_request(ws_pivot.id, row_idx, row_idx+1, 24))

    # Row Tổng Table 1
    t1_total_idx = t1_start_row + len(sorted_ams)
    total_row = ['TỔNG CỘNG']
    for st in status_columns:
        total_row.append(sum(am_pivot[am][st] for am in all_ams))
    total_row.append(f"{total_active} ({total_unassigned} chưa gán)")
    total_row.append(total_stagnant_2d)
    total_row.append(total_done_count)
    
    for h_idx, snap in enumerate(history):
        t_sum = sum(snap["totals"].get(am, 0) for am in all_ams)
        total_row.append(t_sum)
        if h_idx > 0:
            prev_t_sum = sum(history[h_idx - 1]["totals"].get(am, 0) for am in all_ams)
            diff = t_sum - prev_t_sum
            total_row.append("—" if diff == 0 else f"+ {diff}" if diff > 0 else f"- {abs(diff)}")

    grid_values.append(total_row)
    requests_format.append(cell_format_request(ws_pivot.id, t1_total_idx, t1_total_idx+1, 0, len(headers_t1), {
        "backgroundColor": make_color("#FEF08A"),
        "textFormat": {"bold": True, "fontSize": 10, "fontFamily": "Arial", "foregroundColor": make_color("#854D0E")},
        "horizontalAlignment": "CENTER",
        "verticalAlignment": "MIDDLE"
    }))
    requests_format.append(border_request(ws_pivot.id, 1, t1_total_idx+1, 0, len(headers_t1)))

    grid_values.append([''] * len(headers_t1))
    grid_values.append([''] * len(headers_t1))

    # Table 2: Top 5 Bưu Cục Tồn Đơn Sắp Quá Hạn
    t2_start_row = t1_total_idx + 3
    grid_values.append([f"TOP 5 BƯU CỤC (KHO HIỆN TẠI) CẦN XỬ LÝ GẤP NHẤT"] + [''] * (len(headers_t1) - 1))
    requests_format.append(merge_request(ws_pivot.id, t2_start_row, t2_start_row+1, 0, len(headers_t1)))
    requests_format.append(cell_format_request(ws_pivot.id, t2_start_row, t2_start_row+1, 0, len(headers_t1), {
        "backgroundColor": make_color("#DC2626"),
        "textFormat": {"bold": True, "fontSize": 11, "fontFamily": "Arial", "foregroundColor": make_color("#FFFFFF")},
        "horizontalAlignment": "CENTER",
        "verticalAlignment": "MIDDLE"
    }))
    requests_format.append(row_height_request(ws_pivot.id, t2_start_row, t2_start_row+1, 30))

    t2_headers = ['Bưu cục (Kho hiện tại)'] + status_columns + ['Tổng còn tồn (Chưa gán LM)', 'Đứng yên ≥ 2 ngày', 'Đã xử lý xong (Done)']
    for i, snap in enumerate(history):
        t2_headers.append(f"Mốc {snap['time']}")
        if i > 0:
            t2_headers.append("Tăng/Giảm (+/-)")

    grid_values.append(t2_headers)
    requests_format.append(cell_format_request(ws_pivot.id, t2_start_row+1, t2_start_row+2, 0, len(headers_t1), {
        "backgroundColor": make_color("#991B1B"),
        "textFormat": {"bold": True, "fontSize": 10, "fontFamily": "Arial", "foregroundColor": make_color("#FFFFFF")},
        "horizontalAlignment": "CENTER",
        "verticalAlignment": "MIDDLE"
    }))

    for r_idx, bc_name in enumerate(top5_bc_names):
        row_idx = t2_start_row + 2 + r_idx
        stats = bc_pivot[bc_name]
        tot = stats['total']
        unas = stats['unassigned']
        stag = stats['stagnant']
        done = stats['done']
        unas_str = f" ({unas} chưa gán)" if unas > 0 else ""
        row = [f"{bc_name} (AM: {stats['am']})"]
        for st in status_columns:
            row.append(stats[st])
        row.append(f"{tot}{unas_str}")
        row.append(stag)
        row.append(done)

        for h_idx, snap in enumerate(history):
            snap_val = snap["bcTotals"].get(bc_name, 0)
            row.append(snap_val)
            if h_idx > 0:
                prev_val = history[h_idx - 1]["bcTotals"].get(bc_name, 0)
                diff = snap_val - prev_val
                row.append("—" if diff == 0 else f"+ {diff}" if diff > 0 else f"- {abs(diff)}")

        grid_values.append(row)
        bg = "#FEF2F2" if r_idx % 2 == 0 else "#FFFFFF"
        requests_format.append(cell_format_request(ws_pivot.id, row_idx, row_idx+1, 0, 1, {
            "backgroundColor": make_color("#FEE2E2"),
            "textFormat": {"bold": True, "fontSize": 9, "fontFamily": "Arial"},
            "horizontalAlignment": "LEFT",
            "verticalAlignment": "MIDDLE"
        }))
        requests_format.append(cell_format_request(ws_pivot.id, row_idx, row_idx+1, 1, len(headers_t1), {
            "backgroundColor": make_color(bg),
            "textFormat": {"fontSize": 9, "fontFamily": "Arial"},
            "horizontalAlignment": "CENTER",
            "verticalAlignment": "MIDDLE"
        }))
        requests_format.append(row_height_request(ws_pivot.id, row_idx, row_idx+1, 24))

    t2_end_row = t2_start_row + 2 + len(top5_bc_names)
    requests_format.append(border_request(ws_pivot.id, t2_start_row+1, t2_end_row, 0, len(headers_t1)))

    col_widths = {0: 300, 1: 90, 2: 90, 3: 90, 4: 90, 5: 90, 6: 150, 7: 150, 8: 120}
    for c_idx, w in col_widths.items():
        requests_format.append(col_width_request(ws_pivot.id, c_idx, c_idx+1, w))

    max_cols = max(len(r) for r in grid_values)
    clean_grid = [r + [''] * (max_cols - len(r)) for r in grid_values]
    end_col_letter = gspread.utils.rowcol_to_a1(1, max_cols).split("1")[0]
    
    retry_gspread(ws_pivot.update, range_name=f"A1:{end_col_letter}{len(clean_grid)}", values=clean_grid, value_input_option="USER_ENTERED")
    retry_gspread(sh.batch_update, {"requests": requests_format})
    print("✔️ Đã cập nhật xong Sheet PIVOT SLA.")

    # 6. TÁCH SHEET CHI TIẾT THEO TỪNG AM (chỉ đưa các đơn ACTIVE cần xử lý)
    print("📂 Đang tách / cập nhật sheet chi tiết cho từng AM...")
    am_orders_map = {}
    for o in active_orders:
        am = o['am']
        if am not in am_orders_map:
            am_orders_map[am] = []
        am_orders_map[am].append(o['raw'])

    am_links = {}
    am_format_reqs = []
    
    for am in all_ams:
        am_rows = am_orders_map.get(am, [])
        tab_name = am
        if tab_name == "Chưa gán AM" and "#N-A" in all_worksheets_dict:
            tab_name = "#N-A"
        elif tab_name == "Chưa gán AM" and "#N/A" in all_worksheets_dict:
            tab_name = "#N/A"

        if tab_name in all_worksheets_dict:
            ws_am = all_worksheets_dict[tab_name]
            retry_gspread(ws_am.clear)
        else:
            ws_am = retry_gspread(sh.add_worksheet, title=tab_name, rows=str(max(100, len(am_rows) + 50)), cols=str(len(header) + 2))
            all_worksheets_dict[tab_name] = ws_am

        retry_gspread(ws_am.update, range_name=f"A1", values=[header] + am_rows)
        am_links[am] = f"https://docs.google.com/spreadsheets/d/{SHEET_KEY}/edit#gid={ws_am.id}"

        am_format_reqs.extend([
            cell_format_request(ws_am.id, 0, 1, 0, len(header), {
                "backgroundColor": make_color("#1E3A8A"),
                "textFormat": {"bold": True, "fontSize": 10, "fontFamily": "Arial", "foregroundColor": make_color("#FFFFFF")},
                "horizontalAlignment": "CENTER",
                "verticalAlignment": "MIDDLE"
            }),
            row_height_request(ws_am.id, 0, 1, 28)
        ])
        time.sleep(0.1)

    if am_format_reqs:
        retry_gspread(sh.batch_update, {"requests": am_format_reqs})
    print("✔️ Đã hoàn tất cập nhật sheet cho toàn bộ AM.")

    # 7. Render HTML & Chụp ảnh bảng bằng Playwright gửi Group Tổng
    render_and_push_gtalk(
        am_pivot, all_ams, status_columns, history, 
        top5_bc_names, bc_pivot, current_time, today_str, 
        total_active, total_done_count, total_at_hub_giao, total_not_at_hub_giao, total_unassigned, total_stagnant_2d, am_links, state
    )

# ==============================================================================
# RENDER HTML & GỬI BÁO CÁO GTALK TỔNG HỢP (GROUP TỔNG)
# ==============================================================================
def render_and_push_gtalk(am_pivot, all_ams, status_columns, history, top5_bc_names, bc_pivot, current_time, today_str, total_active, total_done, total_at_hub, total_not_at_hub, total_unassigned, total_stagnant, am_links, state):
    print("📸 Render giao diện HTML và chụp ảnh Playwright...")

    extra_headers_html = ""
    for i, snap in enumerate(history):
        color_info = SLOT_COLORS[i % len(SLOT_COLORS)]
        extra_headers_html += f'<th style="background: {color_info["header_bg"]} !important; color: #FFFFFF; text-align: center;">Mốc {snap["time"]}</th>'
        if i > 0:
            extra_headers_html += f'<th style="background: {color_info["header_bg"]} !important; color: #FFFFFF; text-align: center;">+/-</th>'

    def make_delta_badge(delta_val):
        if delta_val == 0:
            return '<span class="delta-none">—</span>'
        if delta_val > 0:
            return f'<span class="delta-badge delta-red">▲ +{delta_val:,}</span>'
        return f'<span class="delta-badge delta-green">▼ -{abs(delta_val):,}</span>'

    def format_cell_qty(val):
        if val == 0:
            return "<td class='zero-val'>-</td>"
        elif val >= 50:
            return f"<td><span class='qty-badge qty-high'>{val:,}</span></td>"
        elif val >= 15:
            return f"<td><span class='qty-badge qty-med'>{val:,}</span></td>"
        elif val >= 5:
            return f"<td><span class='qty-badge qty-low'>{val:,}</span></td>"
        return f"<td><span class='qty-badge qty-minimal'>{val:,}</span></td>"

    sorted_ams = sorted(all_ams, key=lambda x: am_pivot[x]['total'], reverse=True)
    
    t1_rows = ""
    for am in sorted_ams:
        tot = am_pivot[am]['total']
        unas = am_pivot[am]['unassigned']
        stag = am_pivot[am]['stagnant']
        done = am_pivot[am]['done']
        unas_html = f"<div class='sub-unas'>({unas:,} chưa gán)</div>" if unas > 0 else ""
        stag_html = f"<span class='qty-badge qty-stag'>⚠️ {stag:,}</span>" if stag > 0 else "<span class='zero-val'>-</span>"
        done_html = f"<span class='qty-badge qty-done'>+{done:,}</span>" if done > 0 else "<span class='zero-val'>-</span>"
        
        t1_rows += f"<tr><td class='left-align bold-text'>{am}</td>"
        for st in status_columns:
            val = am_pivot[am][st]
            t1_rows += format_cell_qty(val)
        
        tot_bg_cls = "tot-high" if tot >= 50 else "tot-med" if tot >= 15 else "tot-low"
        t1_rows += f"<td class='total-col bold-text {tot_bg_cls}'>{tot:,}{unas_html}</td>"
        t1_rows += f"<td class='stag-col'>{stag_html}</td>"
        t1_rows += f"<td class='done-col'>{done_html}</td>"

        for h_idx, snap in enumerate(history):
            color_info = SLOT_COLORS[h_idx % len(SLOT_COLORS)]
            snap_val = snap["totals"].get(am, 0)
            t1_rows += f"<td class='bold-text' style='background-color: {color_info['data_bg']} !important;'>{snap_val:,}</td>" if snap_val > 0 else f"<td class='zero-val' style='background-color: {color_info['data_bg']} !important;'>-</td>"
            if h_idx > 0:
                prev_val = history[h_idx - 1]["totals"].get(am, 0)
                diff = snap_val - prev_val
                bg_diff = "#FFCDD2" if diff > 0 else "#C8E6C9" if diff < 0 else color_info['data_bg']
                t1_rows += f"<td style='background-color: {bg_diff} !important;'>{make_delta_badge(diff)}</td>"
        t1_rows += "</tr>"

    t1_total_row = "<tr class='total-row'><td class='left-align'>TỔNG CỘNG</td>"
    for st in status_columns:
        st_sum = sum(am_pivot[am][st] for am in all_ams)
        t1_total_row += f"<td>{st_sum:,}</td>" if st_sum > 0 else "<td class='zero-val'>-</td>"
    t1_total_row += f"<td>{total_active:,}<div class='sub-unas' style='color:#78350F;'>({total_unassigned:,} chưa gán)</div></td>"
    t1_total_row += f"<td style='background-color: #fee2e2 !important; color: #991b1b; font-weight: 800;'>⚠️ {total_stagnant:,}</td>"
    t1_total_row += f"<td style='background-color: #bbf7d0 !important; color: #166534; font-weight: 800;'>+{total_done:,}</td>"

    for h_idx, snap in enumerate(history):
        color_info = SLOT_COLORS[h_idx % len(SLOT_COLORS)]
        t_sum = sum(snap["totals"].get(am, 0) for am in all_ams)
        t1_total_row += f"<td style='background-color: {color_info['total_bg']} !important; font-weight: 800;'>{t_sum:,}</td>"
        if h_idx > 0:
            prev_t_sum = sum(history[h_idx - 1]["totals"].get(am, 0) for am in all_ams)
            diff = t_sum - prev_t_sum
            bg_diff = "#FFCDD2" if diff > 0 else "#C8E6C9" if diff < 0 else color_info['total_bg']
            t1_total_row += f"<td style='background-color: {bg_diff} !important;'>{make_delta_badge(diff)}</td>"
    t1_total_row += "</tr>"

    t2_rows = ""
    for bc_name in top5_bc_names:
        stats = bc_pivot[bc_name]
        tot = stats['total']
        unas = stats['unassigned']
        stag = stats['stagnant']
        done = stats['done']
        unas_html = f"<div class='sub-unas'>({unas:,} chưa gán)</div>" if unas > 0 else ""
        stag_html = f"<span class='qty-badge qty-stag'>⚠️ {stag:,}</span>" if stag > 0 else "<span class='zero-val'>-</span>"
        done_html = f"<span class='qty-badge qty-done'>+{done:,}</span>" if done > 0 else "<span class='zero-val'>-</span>"
        
        t2_rows += f"<tr><td class='left-align bold-text'>{bc_name} <span class='am-badge'>AM: {stats['am']}</span></td>"
        for st in status_columns:
            val = stats[st]
            t2_rows += format_cell_qty(val)
        
        tot_bg_cls = "tot-high" if tot >= 50 else "tot-med" if tot >= 15 else "tot-low"
        t2_rows += f"<td class='total-col bold-text {tot_bg_cls}'>{tot:,}{unas_html}</td>"
        t2_rows += f"<td class='stag-col'>{stag_html}</td>"
        t2_rows += f"<td class='done-col'>{done_html}</td>"

        for h_idx, snap in enumerate(history):
            color_info = SLOT_COLORS[h_idx % len(SLOT_COLORS)]
            snap_val = snap["bcTotals"].get(bc_name, 0)
            t2_rows += f"<td class='bold-text' style='background-color: {color_info['data_bg']} !important;'>{snap_val:,}</td>" if snap_val > 0 else f"<td class='zero-val' style='background-color: {color_info['data_bg']} !important;'>-</td>"
            if h_idx > 0:
                prev_val = history[h_idx - 1]["bcTotals"].get(bc_name, 0)
                diff = snap_val - prev_val
                bg_diff = "#FFCDD2" if diff > 0 else "#C8E6C9" if diff < 0 else color_info['data_bg']
                t2_rows += f"<td style='background-color: {bg_diff} !important;'>{make_delta_badge(diff)}</td>"
        t2_rows += "</tr>"

    html_content = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
    body {{
        font-family: 'Inter', sans-serif;
        background: #0f172a;
        margin: 0;
        padding: 30px;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 25px;
    }}
    #capture-container {{
        background: #ffffff;
        padding: 32px;
        border-radius: 20px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
        max-width: 1850px;
        width: 100%;
        box-sizing: border-box;
    }}
    .header-box {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 2.5px solid #e2e8f0;
        padding-bottom: 18px;
        margin-bottom: 22px;
    }}
    .header-box h2 {{
        margin: 0;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 26px;
        background: linear-gradient(90deg, #b91c1c 0%, #dc2626 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    .time-badge {{
        font-size: 14px;
        color: #475569;
        font-weight: 700;
        background: #f1f5f9;
        padding: 8px 18px;
        border-radius: 30px;
        border: 1.5px solid #cbd5e1;
    }}
    
    /* 6 Ô THỐNG KÊ DASHBOARD */
    .kpi-cards-grid {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 16px;
        margin-bottom: 28px;
    }}
    .card {{
        background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 16px 14px;
        text-align: center;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.04);
        display: flex;
        flex-direction: column;
        justify-content: center;
    }}
    .card.c-red {{
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
        border: 1.5px solid #fca5a5;
    }}
    .card.c-blue {{
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        border: 1.5px solid #bfdbfe;
    }}
    .card.c-amber {{
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        border: 1.5px solid #fde68a;
    }}
    .card.c-green {{
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border: 1.5px solid #86efac;
    }}
    .card.c-purple {{
        background: linear-gradient(135deg, #faf5ff 0%, #f3e8ff 100%);
        border: 1.5px solid #d8b4fe;
    }}
    .card.c-rose {{
        background: linear-gradient(135deg, #fff1f2 0%, #ffe4e6 100%);
        border: 1.5px solid #fda4af;
    }}
    
    .card-title {{
        font-size: 14px;
        font-weight: 800;
        text-transform: uppercase;
        margin-bottom: 6px;
        letter-spacing: 0.3px;
    }}
    .card.c-red .card-title {{ color: #991b1b; }}
    .card.c-blue .card-title {{ color: #1e40af; }}
    .card.c-amber .card-title {{ color: #92400e; }}
    .card.c-green .card-title {{ color: #166534; }}
    .card.c-purple .card-title {{ color: #6b21a8; }}
    .card.c-rose .card-title {{ color: #be123c; }}
    
    .card-val {{
        font-size: 34px;
        font-weight: 900;
        line-height: 1.1;
    }}
    .card.c-red .card-val {{ color: #b91c1c; }}
    .card.c-blue .card-val {{ color: #1d4ed8; }}
    .card.c-amber .card-val {{ color: #b45309; }}
    .card.c-green .card-val {{ color: #15803d; }}
    .card.c-purple .card-val {{ color: #7e22ce; }}
    .card.c-rose .card-val {{ color: #e11d48; }}
    
    .card-sub {{
        font-size: 13px;
        font-weight: 600;
        color: #64748b;
        margin-top: 5px;
    }}
    
    .table-section {{
        margin-bottom: 28px;
    }}
    .table-title {{
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 21px;
        font-weight: 800;
        color: #1e3a8a;
        margin-bottom: 14px;
        text-transform: uppercase;
        border-left: 6px solid #2563eb;
        padding-left: 12px;
    }}
    .table-title.danger-title {{
        color: #b91c1c;
        border-left-color: #dc2626;
    }}
    table {{
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        border-radius: 12px;
        overflow: hidden;
        border: 1.5px solid #cbd5e1;
    }}
    th {{
        font-family: 'Plus Jakarta Sans', sans-serif;
        background: linear-gradient(180deg, #1e40af 0%, #1e3a8a 100%);
        color: #ffffff;
        font-weight: 800;
        font-size: 15px;
        text-transform: uppercase;
        padding: 14px 10px;
        text-align: center;
    }}
    th.danger-th {{
        background: linear-gradient(180deg, #b91c1c 0%, #991b1b 100%);
    }}
    th.stag-th {{
        background: linear-gradient(180deg, #be123c 0%, #9f1239 100%);
    }}
    th.done-th {{
        background: linear-gradient(180deg, #16a34a 0%, #15803d 100%);
    }}
    td {{
        padding: 11px 10px;
        font-size: 17px;
        color: #334155;
        border-bottom: 1px solid #e2e8f0;
        font-weight: 600;
        text-align: center;
        background-color: #ffffff;
    }}
    tr:nth-child(even) td {{ background-color: #f8fafc; }}
    .left-align {{ text-align: left; padding-left: 18px; font-size: 16px; }}
    .bold-text {{ font-weight: 800; color: #0f172a; }}
    
    /* CONDITIONAL FORMATTING BADGES */
    .qty-badge {{
        display: inline-block;
        padding: 4px 12px;
        border-radius: 7px;
        font-weight: 800;
        font-size: 17px;
        min-width: 28px;
    }}
    .qty-high {{
        background: #fee2e2;
        color: #b91c1c;
        border: 1.5px solid #fca5a5;
        font-weight: 800;
    }}
    .qty-med {{
        background: #fef3c7;
        color: #b45309;
        border: 1.5px solid #fde68a;
    }}
    .qty-low {{
        background: #eff6ff;
        color: #1d4ed8;
        border: 1.5px solid #bfdbfe;
    }}
    .qty-minimal {{
        background: #f1f5f9;
        color: #475569;
    }}
    .qty-stag {{
        background: #ffe4e6;
        color: #be123c;
        border: 1.5px solid #fda4af;
        font-weight: 900;
    }}
    .qty-done {{
        background: #dcfce7;
        color: #15803d;
        border: 1.5px solid #86efac;
        font-weight: 800;
    }}
    
    .total-col {{
        font-size: 19px;
        font-weight: 800;
    }}
    .tot-high {{ background-color: #fee2e2 !important; color: #991b1b; }}
    .tot-med {{ background-color: #fef3c7 !important; color: #92400e; }}
    .tot-low {{ background-color: #eff6ff !important; color: #1e40af; }}
    
    .stag-col {{
        background-color: #fff1f2 !important;
    }}
    .done-col {{
        background-color: #f0fdf4 !important;
        font-size: 18px;
    }}
    
    .sub-unas {{ font-size: 13px; color: #dc2626; font-weight: 800; margin-top: 3px; }}
    .am-badge {{
        background: #e2e8f0;
        color: #334155;
        font-size: 13px;
        padding: 3px 8px;
        border-radius: 5px;
        margin-left: 8px;
        font-weight: 700;
    }}
    .zero-val {{ color: #94a3b8; font-weight: 400; font-size: 16px; }}
    .delta-badge {{
        display: inline-flex;
        padding: 4px 10px;
        border-radius: 7px;
        font-size: 16px;
        font-weight: 800;
    }}
    .delta-red {{ background-color: #fee2e2; color: #dc2626; }}
    .delta-green {{ background-color: #dcfce7; color: #16a34a; }}
    .delta-none {{ color: #94a3b8; }}
    .total-row td {{
        background: #fef08a !important;
        color: #854d0e;
        font-weight: 900;
        font-size: 20px;
        border-top: 2.5px solid #eab308;
    }}
</style>
</head>
<body>
<div id="capture-container">
    <div class="header-box">
        <h2>⚠️ Báo cáo Đơn Chạm / Sắp Quá Hạn SLA Cần Xử Lý Gấp</h2>
        <div class="time-badge">Mốc: {current_time} | Ngày: {today_str}</div>
    </div>

    <!-- 6 Ô THỐNG KÊ DASHBOARD -->
    <div class="kpi-cards-grid">
        <div class="card c-red">
            <div class="card-title">1. Tổng Còn Tồn Cần Xử Lý</div>
            <div class="card-val">{total_active:,}</div>
            <div class="card-sub">(Cộng mục 2 & mục 3)</div>
        </div>
        <div class="card c-blue">
            <div class="card-title">2. Tổng Đơn Tại HUB Giao</div>
            <div class="card-val">{total_at_hub:,}</div>
            <div class="card-sub">{round(total_at_hub/total_active*100, 1) if total_active > 0 else 0}% đơn tồn | Đã tới bưu cục đích</div>
        </div>
        <div class="card c-amber">
            <div class="card-title">3. Tổng Đơn Chưa Về Đến HUB Giao</div>
            <div class="card-val">{total_not_at_hub:,}</div>
            <div class="card-sub">{round(total_not_at_hub/total_active*100, 1) if total_active > 0 else 0}% đơn tồn | Đang trung chuyển</div>
        </div>
        <div class="card c-rose">
            <div class="card-title">4. Đứng Yên ≥ 2 Ngày</div>
            <div class="card-val">{total_stagnant:,}</div>
            <div class="card-sub">{round(total_stagnant/total_active*100, 1) if total_active > 0 else 0}% đơn tồn | Cần GDV can thiệp</div>
        </div>
        <div class="card c-purple">
            <div class="card-title">5. Chưa Gán Chuyến Đi</div>
            <div class="card-val">{total_unassigned:,}</div>
            <div class="card-sub">{round(total_unassigned/total_active*100, 1) if total_active > 0 else 0}% trên tổng đơn tồn</div>
        </div>
        <div class="card c-green">
            <div class="card-title">6. Đã Xử Lý Xong (Done Case)</div>
            <div class="card-val">+{total_done:,}</div>
            <div class="card-sub">Đã GTC / Chuyển hoàn / Thất lạc</div>
        </div>
    </div>

    <div class="table-section">
        <div class="table-title">1. Phân bổ theo AM (Kho hiện tại) & Nhóm trạng thái</div>
        <table>
            <thead>
                <tr>
                    <th class="left-align">AM (Kho hiện tại)</th>
                    {''.join([f'<th>{st}</th>' for st in status_columns])}
                    <th>Tổng còn tồn (Chưa gán LM)</th>
                    <th class="stag-th">Đứng yên ≥ 2 ngày</th>
                    <th class="done-th">Đã xử lý xong (Done)</th>
                    {extra_headers_html}
                </tr>
            </thead>
            <tbody>
                {t1_rows}
                {t1_total_row}
            </tbody>
        </table>
    </div>

    <div class="table-section">
        <div class="table-title danger-title">2. Top 5 Bưu Cục (Kho hiện tại) Tồn nhiều nhất</div>
        <table>
            <thead>
                <tr>
                    <th class="left-align danger-th">Bưu Cục Hiện Tại</th>
                    {''.join([f'<th class="danger-th">{st}</th>' for st in status_columns])}
                    <th class="danger-th">Tổng còn tồn (Chưa gán LM)</th>
                    <th class="stag-th">Đứng yên ≥ 2 ngày</th>
                    <th class="done-th">Đã xử lý xong (Done)</th>
                    {extra_headers_html}
                </tr>
            </thead>
            <tbody>
                {t2_rows}
            </tbody>
        </table>
    </div>
</div>
</body>
</html>
"""

    temp_html_path = os.path.join(BASE_DIR, "temp_table_sla_risk.html")
    output_image_path = os.path.join(BASE_DIR, "table_sla_risk.png")

    with open(temp_html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_viewport_size({"width": 1850, "height": 1300})
        page.goto(f"file:///{temp_html_path.replace('\\', '/')}")
        page.wait_for_timeout(1000)
        container = page.locator("#capture-container")
        container.screenshot(path=output_image_path)
        browser.close()

    try:
        os.remove(temp_html_path)
    except Exception:
        pass

    # 8. Gửi ảnh và tóm tắt thông báo lên GTalk chính
    print("📡 Đang gửi ảnh và tóm tắt thông báo sang GTalk group chính...")
    
    comparison_label = f"mốc {history[0]['time']}" if len(history) > 1 else "đầu ngày"
    prev_grand_total = history[0]['grandTotal'] if len(history) > 1 else total_active
    diff_total = total_active - prev_grand_total
    
    diff_str = ""
    if len(history) > 1:
        if diff_total < 0:
            diff_str = f" (📉 <b>Đã giảm {abs(diff_total):,} đơn tồn</b> ~ {round(abs(diff_total)/prev_grand_total*100, 1)}%)"
        elif diff_total > 0:
            diff_str = f" (📈 <b>Tồn tăng thêm +{diff_total:,} đơn</b> ~ +{round(diff_total/prev_grand_total*100, 1)}%)"
        else:
            diff_str = " (➖ Không đổi)"

    caption = f"🚨 <b>BÁO CÁO ĐƠN CHẠM / SẮP QUÁ HẠN SLA CẦN XỬ LÝ GẤP</b>\n"
    caption += f"⏱️ <b>Mốc cập nhật:</b> {current_time} ngày {today_str}\n"
    caption += f"<b>Tổng còn tồn cần xử lý:</b> <b>{total_active:,}</b> đơn{diff_str}\n"
    caption += f"  ├ <b>Đã tại HUB giao:</b> <b>{total_at_hub:,}</b> đơn ({round(total_at_hub/total_active*100, 1) if total_active > 0 else 0}%)\n"
    caption += f"  └ <b>Chưa về đến HUB giao:</b> <b>{total_not_at_hub:,}</b> đơn ({round(total_not_at_hub/total_active*100, 1) if total_active > 0 else 0}%)\n"
    caption += f"<b>Đứng yên ≥ 2 ngày:</b> <b>{total_stagnant:,}</b> đơn ({round(total_stagnant/total_active*100, 1) if total_active > 0 else 0}%)\n"
    caption += f"<b>Chưa gán chuyến đi:</b> <b>{total_unassigned:,}</b> đơn ({round(total_unassigned/total_active*100, 1) if total_active > 0 else 0}%)\n"
    caption += f"<b>Đã xử lý xong (Done case):</b> <b>+{total_done:,}</b> đơn\n"
    caption += f"🔗 <b>Link tra cứu tổng hợp:</b> <a href=\"https://docs.google.com/spreadsheets/d/{SHEET_KEY}/edit#gid=0\">Click vào đây để xem</a>"

    file_size = os.path.getsize(output_image_path)
    file_name = os.path.basename(output_image_path)
    with open(output_image_path, 'rb') as f:
        file_bytes = f.read()

    init_payload = {
        "ChannelId": GTALK_CHANNEL_MAIN,
        "FileName": file_name,
        "FileSize": str(file_size),
        "MimeType": "image/png",
        "Metadata": json.dumps({"width": 1850, "height": 1300}),
        "oaToken": GTALK_TOKEN
    }

    try:
        resp_init = requests.post("https://mbff.ghn.vn/api/gtalk/initiate-upload", json=init_payload, timeout=20)
        if resp_init.status_code == 200:
            init_data = resp_init.json()
            if init_data.get("errorCode") == "success":
                presigned_url = init_data["data"]["PresignedURL"]
                upload_id = init_data["data"]["UploadId"]

                resp_put = requests.put(presigned_url, data=file_bytes, headers={"Content-Type": "image/png"}, timeout=30)
                if resp_put.status_code == 200:
                    resp_comp = requests.post("https://mbff.ghn.vn/api/gtalk/complete-upload", json={"oaToken": GTALK_TOKEN, "UploadId": upload_id}, timeout=20)
                    if resp_comp.status_code == 200:
                        comp_data = resp_comp.json()
                        if comp_data.get("errorCode") == "success":
                            file_id = comp_data["data"]["Id"]
                            send_payload = {
                                "channelId": GTALK_CHANNEL_MAIN,
                                "clientMsgId": str(int(time.time() * 1000)),
                                "content": {
                                    "parseMode": "HTML",
                                    "attachment": {
                                        "caption": caption,
                                        "items": [{"image": {"fileId": file_id, "width": 1850, "height": 1300}}]
                                    }
                                },
                                "oaToken": GTALK_TOKEN
                            }
                            r_send = requests.post("https://mbff.ghn.vn/api/gtalk/send-message", json=send_payload, timeout=20)
                            if r_send.status_code == 200 and r_send.json().get("errorCode") == "success":
                                print("   ✅ Đã gửi báo cáo SLA sang GTalk group chính thành công!")
                            else:
                                print(f"   ❌ Gửi tin nhắn GTalk lỗi: {r_send.text}")
    except Exception as e:
        print(f"❌ Lỗi gửi GTalk: {e}")

def main():
    if "--clear" in sys.argv:
        if os.path.exists(SNAPSHOT_FILE):
            try:
                os.remove(SNAPSHOT_FILE)
                print(f"🧹 Đã xóa file snapshot cũ: {SNAPSHOT_FILE}")
            except Exception as e:
                print(f"❌ Lỗi khi xóa snapshot: {e}")

    try:
        run_sla_risk_report()
    except Exception as e:
        print(f"❌ Lỗi thực thi báo cáo SLA: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
