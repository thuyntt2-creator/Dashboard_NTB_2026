# -*- coding: utf-8 -*-
"""
NTB FD Analysis – Báo Cáo FD Tổng N-1 (HUB)
========================================================================
Mô tả:
  1. Tự động đọc dữ liệu N-1 từ Google Sheets (có fallback đọc trực tiếp từ Master FD sheet
     nếu sheet `RAW FD N-1 (HUB)` bị kẹt ở trạng thái 'Loading...').
  2. Lọc bỏ các bưu cục / kho không có tên AM (kho giao hàng nặng không do AM quản lý).
  3. Kiểm tra dữ liệu mới/cũ: Nếu dữ liệu trùng 100% với lần chạy trước -> Báo 'data chưa cập nhật' và bỏ qua.
     (Có hỗ trợ tham số '--force', '-f', hoặc 'force' để bắt buộc chạy lại).
  4. Tính toán & Xuất Google Sheet `Snapshot – FD N-1 (HUB)`:
     - Bảng 1: Bảng Tổng Quan Vùng NTB
     - Bảng 2: Top 10 Bưu Cục %FD cao nhất
     - Bảng 3: Báo cáo %FD theo từng AM (Sort %FD ↓)
     - Bảng 4: BẢNG TẤT CẢ BƯU CỤC QUẢN LÝ (FULL LIST)
  5. Tạo 2 ảnh báo cáo sắc nét (Top 10 BC & Xếp hạng AM) chữ to rõ ràng, tiêu đề sạch sẽ chuẩn chỉnh (không lỗi ô vuông).
  6. Gửi GỘP CẢ 2 ẢNH TRONG 1 TIN NHẮN GTalk kèm link MVĐ hoàn trả.
"""

import sys, os
sys.stdout.reconfigure(encoding='utf-8')

import json
import time
from PIL import Image
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from google.oauth2.credentials import Credentials as UserCredentials
from datetime import datetime, timedelta
import warnings
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import requests
import io
warnings.filterwarnings('ignore')

# ============================================================
#  CONFIG
# ============================================================
CREDENTIALS_PATH   = r'C:\Users\lap4all\Desktop\Backlog_Automation\credentials.json'
SPREADSHEET_ID     = '15Z-aMM6OFfiWUXd2Zwz6BFNq_Y0KWwHiVDqxkioHufM'  # Google Sheet làm việc
SOURCE_SHEET_ID   = '1odUPX5mWpUYUUQOrhX_k8kXWV7drMUdQ58DRwgSQNS8'  # Master FD raw source

# ── Telegram ──
TELEGRAM_BOT_TOKEN = '8570130113:AAGXRiUaKBknVpgtm1_i9ZA47JRjAXmB21M'
TELEGRAM_CHAT_ID   = '-5058464865'

# ── GTalk ──
GTALK_OA_TOKEN     = '2067164759497973760:RfgqBJY4QtV18udu1wMEfhmoRNI4hgBv'
GTALK_CHANNEL_ID   = '2073028116810764288'

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(BASE_DIR, 'last_hub_n1_state.json')

def get_gspread_client(spreadsheet_id=SPREADSHEET_ID):
    candidates = [
        CREDENTIALS_PATH,
        r'C:\Users\lap4all\Documents\Auto report\credentials.json',
        os.path.join(BASE_DIR, 'credentials.json'),
        'credentials.json'
    ]
    for cred_path in candidates:
        if os.path.exists(cred_path):
            try:
                creds = Credentials.from_service_account_file(cred_path, scopes=SCOPES)
                gc = gspread.authorize(creds)
                if spreadsheet_id:
                    gc.open_by_key(spreadsheet_id)
                print(f"  🔑 Authenticated with Service Account: {cred_path}")
                return gc
            except Exception as e:
                pass

    auth_user_candidates = [
        r'C:\Users\lap4all\Documents\Auto report\authorized_user.json',
        r'C:\Users\lap4all\Desktop\Backlog_Automation\authorized_user.json',
        os.path.join(BASE_DIR, 'authorized_user.json'),
        'authorized_user.json'
    ]
    for auth_user_file in auth_user_candidates:
        if os.path.exists(auth_user_file):
            try:
                creds = UserCredentials.from_authorized_user_file(auth_user_file, scopes=SCOPES)
                gc = gspread.authorize(creds)
                if spreadsheet_id:
                    gc.open_by_key(spreadsheet_id)
                print(f"  🔑 Authenticated with Authorized User: {auth_user_file}")
                return gc
            except Exception as e:
                pass

    raise PermissionError("Không thể xác thực Google Sheets API")

# ── Color Map (Google Sheets formatting) ────────────────────
CLR = {
    'darkBlue' : {'red': 0.122, 'green': 0.306, 'blue': 0.475},
    'midBlue'  : {'red': 0.180, 'green': 0.459, 'blue': 0.714},
    'lightBlue': {'red': 0.839, 'green': 0.894, 'blue': 0.941},
    'altRow'   : {'red': 0.961, 'green': 0.976, 'blue': 1.000},
    'yellow'   : {'red': 1.000, 'green': 0.949, 'blue': 0.800},
    'orange'   : {'red': 0.773, 'green': 0.353, 'blue': 0.067},
    'good'     : {'red': 0.851, 'green': 0.918, 'blue': 0.827},
    'goodFont' : {'red': 0.153, 'green': 0.392, 'blue': 0.098},
    'warn'     : {'red': 1.000, 'green': 0.949, 'blue': 0.800},
    'warnFont' : {'red': 0.600, 'green': 0.400, 'blue': 0.000},
    'bad'      : {'red': 1.000, 'green': 0.878, 'blue': 0.878},
    'badFont'  : {'red': 0.753, 'green': 0.000, 'blue': 0.000},
    'white'    : {'red': 1.000, 'green': 1.000, 'blue': 1.000},
    'black'    : {'red': 0.000, 'green': 0.000, 'blue': 0.000},
}

def rgb(clr_key):
    return CLR[clr_key]

def cell_data(value, bg=None, bold=False, fg=None, fmt=None, halign='LEFT'):
    d = {'userEnteredValue': {}}
    if isinstance(value, str):
        d['userEnteredValue']['stringValue'] = value
    elif isinstance(value, (int, float)):
        d['userEnteredValue']['numberValue'] = value
    else:
        d['userEnteredValue']['stringValue'] = str(value) if value is not None else ''

    fmt_obj = {
        'textFormat': {
            'bold': bold,
            'foregroundColor': rgb(fg) if fg else rgb('black'),
            'fontFamily': 'Arial',
            'fontSize': 9,
        },
        'horizontalAlignment': halign,
        'verticalAlignment': 'MIDDLE',
    }
    if bg:
        fmt_obj['backgroundColor'] = rgb(bg)
    if fmt:
        fmt_obj['numberFormat'] = {'type': 'NUMBER', 'pattern': fmt}

    d['userEnteredFormat'] = fmt_obj
    return d

def fd_cell(val, alt=False):
    bg_alt = 'altRow' if alt else None
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return cell_data('', bg=bg_alt, halign='CENTER')
    v = round(val / 100, 4)
    if val <= 4.5:
        return cell_data(v, bg='good', fg='goodFont', fmt='0.0%', halign='CENTER')
    elif val < 6.0:
        return cell_data(v, bg='warn', fg='warnFont', fmt='0.0%', halign='CENTER')
    else:
        return cell_data(v, bg='bad',  fg='badFont',  fmt='0.0%', halign='CENTER')

def batch_update_sheet(sh, rows_data):
    max_cols = max(len(r) for r in rows_data)
    for r in rows_data:
        while len(r) < max_cols:
            r.append(cell_data(''))

    body = {
        'requests': [{
            'updateCells': {
                'rows': [{'values': row} for row in rows_data],
                'fields': 'userEnteredValue,userEnteredFormat',
                'start': {'sheetId': sh.id, 'rowIndex': 0, 'columnIndex': 0}
            }
        }]
    }
    sh.spreadsheet.batch_update(body)

def set_col_widths(sh, widths):
    max_cols = 50
    widths = widths[:max_cols]
    requests = []
    for i, w in enumerate(widths):
        requests.append({
            'updateDimensionProperties': {
                'range': {
                    'sheetId': sh.id,
                    'dimension': 'COLUMNS',
                    'startIndex': i,
                    'endIndex': i+1,
                },
                'properties': {'pixelSize': w},
                'fields': 'pixelSize'
            }
        })
    try:
        sh.spreadsheet.batch_update({'requests': requests})
    except Exception as e:
        print(f'  ⚠️ Không set được column widths: {e}')

def ensure_sheet(spreadsheet, name):
    try:
        return spreadsheet.worksheet(name)
    except gspread.WorksheetNotFound:
        return spreadsheet.add_worksheet(title=name, rows=500, cols=50)

# ============================================================
#  DATA STATE CHECKING (DUPLICATE DATA PROTECTION)
# ============================================================
def check_data_updated(overview, force=False):
    current_sig = f"{overview['Total_don']:.0f}_{overview['Don_return']:.0f}_{overview['Total_bcu']}_{overview['Total_am']}"
    if not force and os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                last_state = json.load(f)
                if last_state.get('sig') == current_sig:
                    return False, current_sig
        except Exception:
            pass
    return True, current_sig

def save_data_state(sig):
    try:
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump({'sig': sig, 'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, f, indent=2)
    except Exception as e:
        print(f"⚠️ Không lưu được state file: {e}")

# ============================================================
#  DATA PROCESSING WITH FALLBACK
# ============================================================
def load_cocau_am(spreadsheet):
    """Lấy mapping Bưu cục -> AM từ CoCauVung"""
    try:
        ws = spreadsheet.worksheet('CoCauVung')
        data = ws.get_all_values()
        if len(data) >= 2:
            df = pd.DataFrame(data[1:], columns=data[0])
            bc_col = df.iloc[:, 1].astype(str).str.strip()
            am_col = df.iloc[:, 3].astype(str).str.strip()
            return dict(zip(bc_col, am_col))
    except Exception as e:
        print(f"  ⚠️ Không đọc được CoCauVung: {e}")
    return {}

def load_and_process_hub_n1(gc, spreadsheet):
    ws_name = 'RAW FD N-1 (HUB)'
    print(f"📖 Đang kiểm tra sheet: '{ws_name}'...")
    ws = spreadsheet.worksheet(ws_name)
    
    data = ws.get_all_values()
    is_loading = (len(data) < 10) or ('loading' in str(data[0][0]).lower())

    bc_to_am = load_cocau_am(spreadsheet)

    parsed_rows = []

    if not is_loading:
        print(f"  ✅ Đã đọc dữ liệu trực tiếp từ sheet '{ws_name}' ({len(data)} dòng)")
        header = data[0]
        col_id_idx, col_name_idx, col_total_idx, col_ret_idx, col_am_idx = None, None, None, None, None

        for idx, cname in enumerate(header):
            cn = str(cname).strip().lower()
            if 'id bưu cục' in cn or cn == 'id': col_id_idx = idx
            elif 'tên bưu cục' in cn or cn == 'bưu cục': col_name_idx = idx
            elif 'total đơn' in cn or cn == 'total': col_total_idx = idx
            elif 'return' in cn or 'trả' in cn: col_ret_idx = idx
            elif cn == 'am': col_am_idx = idx

        if col_id_idx is None: col_id_idx = 2
        if col_name_idx is None: col_name_idx = 3
        if col_total_idx is None: col_total_idx = 5
        if col_ret_idx is None: col_ret_idx = 6
        if col_am_idx is None: col_am_idx = 7

        if col_total_idx == col_ret_idx:
            raise ValueError(f"Lỗi: Cột Total đơn và Đơn return bị trùng index ({col_total_idx})! Header={header}")

        print(f"  Col mapping: ID={col_id_idx}, BC={col_name_idx}, Total={col_total_idx}, Return={col_ret_idx}, AM={col_am_idx}")

        for row in data[1:]:
            if len(row) <= max(col_name_idx, col_am_idx, col_total_idx, col_ret_idx):
                continue
            bc_id   = str(row[col_id_idx]).strip() if col_id_idx < len(row) else ''
            bc_name = str(row[col_name_idx]).strip() if col_name_idx < len(row) else ''
            am_name = str(row[col_am_idx]).strip() if col_am_idx < len(row) else ''

            if not am_name and bc_name in bc_to_am:
                am_name = bc_to_am[bc_name]

            tot_str = str(row[col_total_idx]).replace(',', '').strip() if col_total_idx < len(row) else '0'
            ret_str = str(row[col_ret_idx]).replace(',', '').strip() if col_ret_idx < len(row) else '0'

            try: tot_val = float(tot_str) if tot_str else 0.0
            except: tot_val = 0.0

            try: ret_val = float(ret_str) if ret_str else 0.0
            except: ret_val = 0.0

            parsed_rows.append({
                'ID': bc_id,
                'BC': bc_name,
                'AM': am_name,
                'Total': tot_val,
                'Return': ret_val
            })
    else:
        print(f"  ⚠️ Sheet '{ws_name}' đang ở trạng thái Loading / IMPORTRANGE...")
        print(f"  🔄 Đang kích hoạt Fallback: Đọc trực tiếp từ Master FD ({SOURCE_SHEET_ID})...")
        sh_source = gc.open_by_key(SOURCE_SHEET_ID)
        ws_fd = sh_source.worksheet('FD')
        data_fd = ws_fd.get_all_values()
        
        df_fd = pd.DataFrame(data_fd[1:], columns=data_fd[0])
        col_map = {str(c).strip().lower(): c for c in df_fd.columns}
        
        region_col = next((col_map[k] for k in col_map if 'region' in k), df_fd.columns[1])
        id_col     = next((col_map[k] for k in col_map if 'id' in k), df_fd.columns[2])
        bc_col     = next((col_map[k] for k in col_map if 'tên bưu cục' in k or 'bưu cục' in k), df_fd.columns[3])
        date_col   = next((col_map[k] for k in col_map if 'date' in k or 'ngày' in k), df_fd.columns[0])
        tot_col    = next((col_map[k] for k in col_map if 'total' in k), df_fd.columns[5])
        ret_col    = next((col_map[k] for k in col_map if 'return' in k or 'trả' in k), df_fd.columns[6])

        df_ntb = df_fd[df_fd[region_col] == 'NTB'].copy()
        df_ntb = df_ntb[~df_ntb[bc_col].astype(str).str.lower().str.contains('kho giao hàng', na=False)]
        
        if date_col in df_ntb.columns and not df_ntb.empty:
            dates = df_ntb[date_col].dropna().unique()
            if len(dates) > 1:
                try:
                    df_ntb['dt_parsed'] = pd.to_datetime(df_ntb[date_col], errors='coerce')
                    latest_dt = df_ntb['dt_parsed'].max()
                    df_ntb = df_ntb[df_ntb['dt_parsed'] == latest_dt].copy()
                except Exception:
                    df_ntb = df_ntb[df_ntb[date_col] == dates[-1]].copy()

        for _, row in df_ntb.iterrows():
            bc_name = str(row[bc_col]).strip()
            am_name = bc_to_am.get(bc_name, '')

            tot_str = str(row[tot_col]).replace(',', '').strip()
            ret_str = str(row[ret_col]).replace(',', '').strip()

            try: tot_val = float(tot_str) if tot_str else 0.0
            except: tot_val = 0.0

            try: ret_val = float(ret_str) if ret_str else 0.0
            except: ret_val = 0.0

            parsed_rows.append({
                'ID': str(row[id_col]).strip(),
                'BC': bc_name,
                'AM': am_name,
                'Total': tot_val,
                'Return': ret_val
            })

    df = pd.DataFrame(parsed_rows)

    # Filter: CHỈ LẤY BƯU CỤC CÓ AM (loại bỏ kho giao hàng nặng không có AM)
    df_valid = df[df['AM'] != ''].copy()
    print(f"   - Tổng dòng raw: {len(df)}")
    print(f"   - Dòng có AM (hợp lệ): {len(df_valid)}")
    print(f"   - Dòng không có AM (đã loại bỏ): {len(df) - len(df_valid)}")

    # 1. Aggregation by Bưu cục
    bc_df = df_valid.groupby(['ID', 'BC', 'AM']).agg({
        'Total': 'sum',
        'Return': 'sum'
    }).reset_index()

    tot_don_ntb = bc_df['Total'].sum()
    tot_ret_ntb = bc_df['Return'].sum()
    fd_ntb = (tot_ret_ntb / tot_don_ntb * 100) if tot_don_ntb > 0 else 0.0

    bc_df['%FD'] = (bc_df['Return'] / bc_df['Total'] * 100).round(2)
    bc_df['Tỷ trọng return'] = (bc_df['Return'] / tot_ret_ntb * 100).round(2) if tot_ret_ntb > 0 else 0.0
    bc_df['Tỷ trọng sản lượng'] = (bc_df['Total'] / tot_don_ntb * 100).round(2) if tot_don_ntb > 0 else 0.0

    # Tất cả Bưu Cục (Sort %FD ↓)
    all_bc_df = bc_df.sort_values('%FD', ascending=False).reset_index(drop=True)
    # Top 10 Bưu Cục
    top10_bc = all_bc_df.head(10).copy()

    # 2. Aggregation by AM
    am_df = df_valid.groupby('AM').agg({
        'Total': 'sum',
        'Return': 'sum'
    }).reset_index()
    am_df['%FD'] = (am_df['Return'] / am_df['Total'] * 100).round(2)
    am_df['Tỷ trọng return'] = (am_df['Return'] / tot_ret_ntb * 100).round(2) if tot_ret_ntb > 0 else 0.0
    am_df['Tỷ trọng sản lượng'] = (am_df['Total'] / tot_don_ntb * 100).round(2) if tot_don_ntb > 0 else 0.0
    am_df = am_df.sort_values('%FD', ascending=False).reset_index(drop=True)

    overview = {
        'Total_don': tot_don_ntb,
        'Don_return': tot_ret_ntb,
        'FD_pct': fd_ntb,
        'Total_bcu': len(bc_df),
        'Total_am': len(am_df)
    }

    return overview, top10_bc, am_df, all_bc_df

# ============================================================
#  WRITE SNAPSHOT TO GOOGLE SHEETS
# ============================================================
def write_hub_n1_snapshot(sh, overview, top10_bc, am_df, all_bc_df):
    print(f'📝 Đang ghi dữ liệu vào sheet: {sh.title}...')
    sh.clear()

    rows_data = []

    # ── Header Banner ──
    rows_data.append([
        cell_data('BÁO CÁO %FD HUB (N-1) – VÙNG NTB', bg='darkBlue', bold=True, fg='white', halign='LEFT'),
        *[cell_data('', bg='darkBlue')] * 6
    ])
    rows_data.append([cell_data('')] * 7)

    # ── Bảng 1: Tổng Quan Vùng ──
    rows_data.append([
        cell_data('1. BẢNG TỔNG QUAN VÙNG NTB (N-1)', bg='lightBlue', bold=True, halign='LEFT'),
        *[cell_data('', bg='lightBlue')] * 6
    ])
    rows_data.append([
        cell_data('Chỉ Số Tổng Quan', bg='midBlue', bold=True, fg='white', halign='CENTER'),
        cell_data('Giá Trị',          bg='midBlue', bold=True, fg='white', halign='CENTER'),
        cell_data('Ghi Chú',          bg='midBlue', bold=True, fg='white', halign='CENTER'),
        *[cell_data('')] * 4
    ])

    rows_data.append([
        cell_data('Tổng Đơn Có Gán Giao (Total)', bg='altRow', bold=True, halign='LEFT'),
        cell_data(round(overview['Total_don']), bg='altRow', bold=True, fmt='#,##0', halign='CENTER'),
        cell_data('Tổng đơn từ các bưu cục có quản lý AM', bg='altRow', halign='LEFT'),
    ])
    rows_data.append([
        cell_data('Tổng Đơn Return (Chuyển Trả)', halign='LEFT'),
        cell_data(round(overview['Don_return']), bold=True, fmt='#,##0', halign='CENTER'),
        cell_data('Tổng đơn bị trả về', halign='LEFT'),
    ])
    rows_data.append([
        cell_data('%FD Tổng Vùng NTB', bg='yellow', bold=True, halign='LEFT'),
        cell_data(round(overview['FD_pct'] / 100, 4), bg='yellow', bold=True, fmt='0.00%', halign='CENTER'),
        cell_data('Tỷ lệ đơn trả = Đơn return / Total đơn', bg='yellow', halign='LEFT'),
    ])
    rows_data.append([
        cell_data('Số Bưu Cục Quản Lý', bg='altRow', halign='LEFT'),
        cell_data(overview['Total_bcu'], bg='altRow', fmt='#,##0', halign='CENTER'),
        cell_data(f"Tổng số {overview['Total_am']} AM phụ trách", bg='altRow', halign='LEFT'),
    ])

    rows_data.append([cell_data('')] * 7)

    # ── Bảng 2: Top 10 Bưu Cục %FD Cao Nhất ──
    rows_data.append([
        cell_data('2. TOP 10 BƯU CỤC CÓ %FD CAO NHẤT (N-1)', bg='lightBlue', bold=True, halign='LEFT'),
        *[cell_data('', bg='lightBlue')] * 6
    ])
    rows_data.append([
        cell_data('STT',              bg='midBlue', bold=True, fg='white', halign='CENTER'),
        cell_data('Tên Bưu Cục',      bg='midBlue', bold=True, fg='white', halign='CENTER'),
        cell_data('AM Phụ Trách',     bg='midBlue', bold=True, fg='white', halign='CENTER'),
        cell_data('Total Đơn',        bg='midBlue', bold=True, fg='white', halign='CENTER'),
        cell_data('Đơn Return',       bg='midBlue', bold=True, fg='white', halign='CENTER'),
        cell_data('%FD (Return)',     bg='midBlue', bold=True, fg='white', halign='CENTER'),
        cell_data('Tỷ Trọng Return',  bg='orange',  bold=True, fg='white', halign='CENTER'),
    ])

    for i, r in top10_bc.iterrows():
        alt = i % 2 == 1
        bg = 'altRow' if alt else None
        rows_data.append([
            cell_data(i + 1, bg=bg, halign='CENTER'),
            cell_data(r['BC'], bg=bg, bold=True, halign='LEFT'),
            cell_data(r['AM'], bg=bg, halign='LEFT'),
            cell_data(round(r['Total']), bg=bg, fmt='#,##0', halign='CENTER'),
            cell_data(round(r['Return']), bg=bg, fmt='#,##0', halign='CENTER'),
            fd_cell(r['%FD'], alt=alt),
            cell_data(round(r['Tỷ trọng return'] / 100, 4), bg='yellow', fmt='0.00%', halign='CENTER'),
        ])

    rows_data.append([cell_data('')] * 7)

    # ── Bảng 3: %FD Theo AM ──
    rows_data.append([
        cell_data('3. XẾP HẠNG %FD THEO CÁC AM (SORT %FD ↓)', bg='lightBlue', bold=True, halign='LEFT'),
        *[cell_data('', bg='lightBlue')] * 6
    ])
    rows_data.append([
        cell_data('STT',                 bg='midBlue', bold=True, fg='white', halign='CENTER'),
        cell_data('AM Phụ Trách',        bg='midBlue', bold=True, fg='white', halign='CENTER'),
        cell_data('Total Đơn',           bg='midBlue', bold=True, fg='white', halign='CENTER'),
        cell_data('Đơn Return',          bg='midBlue', bold=True, fg='white', halign='CENTER'),
        cell_data('%FD (Return)',        bg='midBlue', bold=True, fg='white', halign='CENTER'),
        cell_data('Tỷ Trọng Return',     bg='orange',  bold=True, fg='white', halign='CENTER'),
        cell_data('Tỷ Trọng Sản Lượng',  bg='orange',  bold=True, fg='white', halign='CENTER'),
    ])

    for i, r in am_df.iterrows():
        alt = i % 2 == 1
        bg = 'altRow' if alt else None
        rows_data.append([
            cell_data(i + 1, bg=bg, halign='CENTER'),
            cell_data(r['AM'], bg=bg, bold=True, halign='LEFT'),
            cell_data(round(r['Total']), bg=bg, fmt='#,##0', halign='CENTER'),
            cell_data(round(r['Return']), bg=bg, fmt='#,##0', halign='CENTER'),
            fd_cell(r['%FD'], alt=alt),
            cell_data(round(r['Tỷ trọng return'] / 100, 4), bg='yellow', fmt='0.00%', halign='CENTER'),
            cell_data(round(r['Tỷ trọng sản lượng'] / 100, 4), bg=bg, fmt='0.00%', halign='CENTER'),
        ])

    rows_data.append([cell_data('')] * 7)

    # ── Bảng 4: BẢNG FULL TẤT CẢ BƯU CỤC ──
    rows_data.append([
        cell_data('4. DANH SÁCH TẤT CẢ BƯU CỤC (SORT %FD ↓)', bg='lightBlue', bold=True, halign='LEFT'),
        *[cell_data('', bg='lightBlue')] * 6
    ])
    rows_data.append([
        cell_data('STT',              bg='midBlue', bold=True, fg='white', halign='CENTER'),
        cell_data('Tên Bưu Cục',      bg='midBlue', bold=True, fg='white', halign='CENTER'),
        cell_data('AM Phụ Trách',     bg='midBlue', bold=True, fg='white', halign='CENTER'),
        cell_data('Total Đơn',        bg='midBlue', bold=True, fg='white', halign='CENTER'),
        cell_data('Đơn Return',       bg='midBlue', bold=True, fg='white', halign='CENTER'),
        cell_data('%FD (Return)',     bg='midBlue', bold=True, fg='white', halign='CENTER'),
        cell_data('Tỷ Trọng Return',  bg='orange',  bold=True, fg='white', halign='CENTER'),
    ])

    for i, r in all_bc_df.iterrows():
        alt = i % 2 == 1
        bg = 'altRow' if alt else None
        rows_data.append([
            cell_data(i + 1, bg=bg, halign='CENTER'),
            cell_data(r['BC'], bg=bg, bold=True, halign='LEFT'),
            cell_data(r['AM'], bg=bg, halign='LEFT'),
            cell_data(round(r['Total']), bg=bg, fmt='#,##0', halign='CENTER'),
            cell_data(round(r['Return']), bg=bg, fmt='#,##0', halign='CENTER'),
            fd_cell(r['%FD'], alt=alt),
            cell_data(round(r['Tỷ trọng return'] / 100, 4), bg='yellow', fmt='0.00%', halign='CENTER'),
        ])

    batch_update_sheet(sh, rows_data)
    set_col_widths(sh, [50, 320, 220, 120, 120, 120, 140])
    print('  ✅ Đã ghi thành công vào Google Sheet!')

# ============================================================
#  MATPLOTLIB REPORT IMAGE GENERATION (NO EMOJIS FOR CLEAN TITLES)
# ============================================================
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

def render_image_top10(overview, top10_bc, date_str=""):
    """Ảnh 1: Top 10 Bưu Cục %FD Cao Nhất (Tiêu đề sạch, chữ to rõ)"""
    print("🎨 Đang vẽ Ảnh 1 (Top 10 Bưu Cục)...")
    fig_h = 10.5
    fig = plt.figure(figsize=(16, fig_h), dpi=200)

    title_date = f" {date_str}" if date_str else " (N-1)"
    fig.suptitle(f'BÁO CÁO %FD HUB{title_date} – VÙNG NTB\n(Total Đơn: {overview["Total_don"]:,.0f}  |  Đơn Return: {overview["Don_return"]:,.0f}  |  %FD Tổng Vùng: {overview["FD_pct"]:.2f}%)',
                 fontsize=22, fontweight='bold', color='#1F4E79', y=0.95)

    ax = fig.add_axes([0.03, 0.05, 0.94, 0.78])
    ax.axis('off')
    ax.set_title('TOP 10 BƯU CỤC CÓ %FD CAO NHẤT', fontsize=20, fontweight='bold', loc='left', pad=18, color='#1F4E79')

    cols = ['STT', 'BC', 'AM', 'Total', 'Return', '%FD', 'Tỷ trọng return']
    labels = ['STT', 'Tên Bưu Cục', 'AM Phụ Trách', 'Total Đơn', 'Đơn Return', '%FD', 'Tỷ Trọng Return']
    col_w = [0.06, 0.34, 0.22, 0.11, 0.11, 0.10, 0.12]

    cell_text = [labels]
    cell_color = [['#1F4E79'] * len(cols)]
    text_color = [['white'] * len(cols)]

    for idx, r in top10_bc.iterrows():
        texts = [
            str(idx + 1),
            str(r['BC']),
            str(r['AM']),
            f"{r['Total']:,.0f}",
            f"{r['Return']:,.0f}",
            f"{r['%FD']:.2f}%",
            f"{r['Tỷ trọng return']:.2f}%"
        ]
        colors = [
            '#F5F9FF' if idx % 2 == 1 else '#FFFFFF',
            '#F5F9FF' if idx % 2 == 1 else '#FFFFFF',
            '#F5F9FF' if idx % 2 == 1 else '#FFFFFF',
            '#F5F9FF' if idx % 2 == 1 else '#FFFFFF',
            '#F5F9FF' if idx % 2 == 1 else '#FFFFFF',
            fd_color(r['%FD']),
            '#FFE69C'
        ]
        tcolors = [
            '#000000', '#000000', '#000000', '#000000', '#000000',
            fd_textcolor(r['%FD']), '#000000'
        ]
        cell_text.append(texts)
        cell_color.append(colors)
        text_color.append(tcolors)

    tbl = ax.table(cellText=cell_text, cellColours=cell_color, cellLoc='center', loc='upper left', colWidths=col_w, bbox=[0, 0, 1, 1])
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(16)

    for (r, c), cell in tbl.get_celld().items():
        cell.set_edgecolor('#BFBFBF')
        cell.set_linewidth(1.2)
        cell.set_text_props(color=text_color[r][c])
        if r == 0:
            cell.set_text_props(weight='bold', color='white', fontsize=17)
        if c == 1:
            cell.set_text_props(ha='left', weight='bold' if r > 0 else 'bold')
            cell._loc = 'left'
        elif c == 2:
            cell.set_text_props(ha='left')
            cell._loc = 'left'

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', facecolor='white')
    plt.close(fig)
    buf.seek(0)
    return buf

def render_image_am(overview, am_df, date_str=""):
    """Ảnh 2: Xếp hạng %FD theo AM (Tiêu đề sạch, chữ to rõ)"""
    print("🎨 Đang vẽ Ảnh 2 (Xếp Hạng AM)...")
    n_am = len(am_df)
    fig_h = max(11, n_am * 0.65 + 3.0)
    fig = plt.figure(figsize=(16, fig_h), dpi=200)

    title_date = f" {date_str}" if date_str else " (N-1)"
    fig.suptitle(f'BÁO CÁO %FD HUB{title_date} – VÙNG NTB\n(Total Đơn: {overview["Total_don"]:,.0f}  |  Đơn Return: {overview["Don_return"]:,.0f}  |  %FD Tổng Vùng: {overview["FD_pct"]:.2f}%)',
                 fontsize=22, fontweight='bold', color='#1F4E79', y=0.96)

    ax = fig.add_axes([0.03, 0.04, 0.94, 0.82])
    ax.axis('off')
    ax.set_title('XẾP HẠNG %FD THEO CÁC AM', fontsize=20, fontweight='bold', loc='left', pad=18, color='#1F4E79')

    cols = ['STT', 'AM', 'Total', 'Return', '%FD', 'Tỷ trọng return', 'Tỷ trọng sản lượng']
    labels = ['STT', 'AM Phụ Trách', 'Total Đơn', 'Đơn Return', '%FD (Return)', 'Tỷ Trọng Return', 'Tỷ Trọng Sản Lượng']
    col_w = [0.06, 0.28, 0.13, 0.13, 0.13, 0.14, 0.15]

    cell_text = [labels]
    cell_color = [['#1F4E79'] * len(cols)]
    text_color = [['white'] * len(cols)]

    for idx, r in am_df.iterrows():
        texts = [
            str(idx + 1),
            str(r['AM']),
            f"{r['Total']:,.0f}",
            f"{r['Return']:,.0f}",
            f"{r['%FD']:.2f}%",
            f"{r['Tỷ trọng return']:.2f}%",
            f"{r['Tỷ trọng sản lượng']:.2f}%"
        ]
        colors = [
            '#F5F9FF' if idx % 2 == 1 else '#FFFFFF',
            '#F5F9FF' if idx % 2 == 1 else '#FFFFFF',
            '#F5F9FF' if idx % 2 == 1 else '#FFFFFF',
            '#F5F9FF' if idx % 2 == 1 else '#FFFFFF',
            fd_color(r['%FD']),
            '#FFE69C',
            '#F5F9FF' if idx % 2 == 1 else '#FFFFFF'
        ]
        tcolors = [
            '#000000', '#000000', '#000000', '#000000',
            fd_textcolor(r['%FD']), '#000000', '#000000'
        ]
        cell_text.append(texts)
        cell_color.append(colors)
        text_color.append(tcolors)

    tbl = ax.table(cellText=cell_text, cellColours=cell_color, cellLoc='center', loc='upper left', colWidths=col_w, bbox=[0, 0, 1, 1])
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(15)

    for (r, c), cell in tbl.get_celld().items():
        cell.set_edgecolor('#BFBFBF')
        cell.set_linewidth(1.2)
        cell.set_text_props(color=text_color[r][c])
        if r == 0:
            cell.set_text_props(weight='bold', color='white', fontsize=16)
        if c == 1:
            cell.set_text_props(ha='left', weight='bold' if r > 0 else 'bold')
            cell._loc = 'left'

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', facecolor='white')
    plt.close(fig)
    buf.seek(0)
    return buf

# ============================================================
#  TELEGRAM & GTALK NOTIFIERS
# ============================================================
def send_telegram_photo(image_buf, caption):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto'
    files = {'photo': ('report.png', image_buf, 'image/png')}
    data  = {'chat_id': TELEGRAM_CHAT_ID, 'caption': caption}
    try:
        resp = requests.post(url, files=files, data=data, timeout=60)
        if resp.status_code == 200:
            print(f'  ✅ Đã gửi Telegram thành công!')
        else:
            print(f'  ⚠️ Lỗi gửi Telegram ({resp.status_code}): {resp.text[:200]}')
    except Exception as e:
        print(f'  ⚠️ Lỗi kết nối Telegram: {e}')

def upload_file_to_gtalk(image_buf, filename="report.png"):
    """Helper upload 1 file ảnh lên GTalk S3 và trả về Id, width, height"""
    try:
        image_buf.seek(0)
        img = Image.open(image_buf)
        width, height = img.size
        file_size = len(image_buf.getvalue())
        image_buf.seek(0)
    except Exception as e:
        print(f"❌ Lỗi đọc ảnh ({filename}): {e}")
        return None

    headers = {"Content-Type": "application/json"}
    initiate_url = "https://mbff.ghn.vn/api/gtalk/initiate-upload"
    payload_init = {
        "ChannelId": GTALK_CHANNEL_ID,
        "FileName": filename,
        "FileSize": str(file_size),
        "MimeType": "image/png",
        "Metadata": f'{{"width": {width}, "height": {height}}}',
        "oaToken": GTALK_OA_TOKEN
    }
    try:
        res_init = requests.post(initiate_url, json=payload_init, headers=headers, timeout=20, verify=False)
        if res_init.status_code != 200 or res_init.json().get("errorCode") != "success":
            print(f"❌ Lỗi initiate upload GTalk ({filename})")
            return None
        presigned_url = res_init.json()["data"]["PresignedURL"]
        upload_id = res_init.json()["data"]["UploadId"]
    except Exception as e:
        print(f"❌ Lỗi initiate upload GTalk ({filename}): {e}")
        return None

    try:
        image_buf.seek(0)
        res_put = requests.put(presigned_url, data=image_buf, headers={"Content-Type": "image/png"}, timeout=60, verify=False)
        if res_put.status_code != 200:
            print(f"❌ Lỗi PUT lên S3 HTTP {res_put.status_code}")
            return None
    except Exception as e:
        print(f"❌ Lỗi upload S3 ({filename}): {e}")
        return None

    complete_url = "https://mbff.ghn.vn/api/gtalk/complete-upload"
    payload_complete = {"oaToken": GTALK_OA_TOKEN, "UploadId": upload_id}
    try:
        res_comp = requests.post(complete_url, json=payload_complete, headers=headers, timeout=20, verify=False)
        if res_comp.status_code != 200 or res_comp.json().get("errorCode") != "success":
            print(f"❌ Lỗi complete upload GTalk ({filename})")
            return None
        file_id = res_comp.json()["data"]["Id"]
        return {"file_id": file_id, "width": width, "height": height}
    except Exception as e:
        print(f"❌ Lỗi complete upload GTalk ({filename}): {e}")
        return None

def send_photos_gtalk_multi(image_bufs, filenames, caption=""):
    """Gửi nhiều ảnh TRONG CÙNG 1 TIN NHẮN GTalk"""
    if not GTALK_OA_TOKEN or not GTALK_CHANNEL_ID:
        print("⚠️ Bỏ qua GTalk (thiếu Token / Channel ID)")
        return False

    print(f"📡 Đang gộp và gửi {len(image_bufs)} ảnh trong CÙNG 1 TIN NHẮN GTalk...")
    items = []
    for buf, fname in zip(image_bufs, filenames):
        info = upload_file_to_gtalk(buf, fname)
        if info:
            items.append({
                "image": {
                    "fileId": info["file_id"],
                    "width": info["width"],
                    "height": info["height"]
                }
            })

    if not items:
        print("❌ Không upload được ảnh nào lên GTalk!")
        return False

    send_url = "https://mbff.ghn.vn/api/gtalk/send-message"
    client_msg_id = str(int(time.time() * 1000))
    payload_send = {
        "channelId": GTALK_CHANNEL_ID,
        "clientMsgId": client_msg_id,
        "content": {
            "parseMode": "HTML",
            "attachment": {
                "caption": caption,
                "items": items
            }
        },
        "oaToken": GTALK_OA_TOKEN
    }
    headers = {"Content-Type": "application/json"}
    try:
        res_send = requests.post(send_url, json=payload_send, headers=headers, timeout=20, verify=False)
        if res_send.status_code == 200 and res_send.json().get("errorCode") == "success":
            print(f"  ✅ Đã gửi thành công 1 tin nhắn chứa {len(items)} ảnh sang GTalk!")
            return True
        else:
            print(f"  ❌ Lỗi gửi tin nhắn GTalk: {res_send.text}")
    except Exception as e:
        print(f"  ❌ Lỗi kết nối GTalk: {e}")
    return False

# ============================================================
#  MAIN EXECUTION
# ============================================================
def main():
    # Nhận diện tham số force (--force, -f, force) linh hoạt
    args_lower = [arg.lower() for arg in sys.argv[1:]]
    force_run = any(f in args_lower for f in ['--force', '-f', 'force'])

    print("🚀 BẮT ĐẦU PHÂN TÍCH RAW FD N-1 (HUB)...")
    if force_run:
        print("⚡ Chế độ FORCE RUN được kích hoạt: Bắt buộc ghi lại dữ liệu và gửi báo cáo!")

    gc = get_gspread_client(SPREADSHEET_ID)
    spreadsheet = gc.open_by_key(SPREADSHEET_ID)
    print(f"✅ Đã kết nối Google Sheet: '{spreadsheet.title}'")

    # Load & Process Data
    overview, top10_bc, am_df, all_bc_df = load_and_process_hub_n1(gc, spreadsheet)

    # Check data updated
    is_new_data, sig = check_data_updated(overview, force=force_run)
    if not is_new_data:
        print("\n" + "="*60)
        print("⚠️ THÔNG BÁO: Dữ liệu raw N-1 chưa cập nhật mới (giống 100% lần chạy trước).")
        print("   -> Bỏ qua ghi Sheet và không gửi báo cáo GTalk.")
        print("   (Mẹo: Dùng tham số '--force', '-f' hoặc 'force' để bắt buộc gửi báo cáo).")
        print("="*60 + "\n")
        return

    # Print Summary to Console
    print("\n" + "="*60)
    print("📊 BÁO CÁO KẾT QUẢ TỔNG QUAN N-1")
    print("="*60)
    print(f" • Tổng đơn có gán giao:  {overview['Total_don']:,.0f}")
    print(f" • Tổng đơn return:       {overview['Don_return']:,.0f}")
    print(f" • %FD Tổng Vùng NTB:      {overview['FD_pct']:.2f}%")
    print(f" • Số bưu cục quản lý:    {overview['Total_bcu']}")
    print(f" • Số AM phụ trách:       {overview['Total_am']}")
    print("="*60 + "\n")

    # Ensure Sheet & Write Results
    target_sheet_name = 'Snapshot – FD N-1 (HUB)'
    snap_sh = ensure_sheet(spreadsheet, target_sheet_name)
    write_hub_n1_snapshot(snap_sh, overview, top10_bc, am_df, all_bc_df)

    # Render Images & Send Reports
    try:
        date_n1_str = (datetime.now() - timedelta(days=1)).strftime('%d/%m/%Y')
        mvd_link = "https://docs.google.com/spreadsheets/d/15Z-aMM6OFfiWUXd2Zwz6BFNq_Y0KWwHiVDqxkioHufM/edit?gid=704022680#gid=704022680"
        caption = (
            f"<b>BÁO CÁO %FD HUB {date_n1_str} – VÙNG NTB</b>\n\n"
            f"Tổng đơn giao: {overview['Total_don']:,.0f}\n"
            f"Đơn return: {overview['Don_return']:,.0f}\n"
            f"%FD Tổng Vùng: {overview['FD_pct']:.2f}%\n\n"
            f"🔗 Chi tiết link MVĐ hoàn trả theo AM:\n"
            f"{mvd_link}"
        )

        # Render 2 Images
        buf_top10 = render_image_top10(overview, top10_bc, date_n1_str)
        buf_am    = render_image_am(overview, am_df, date_n1_str)

        # Send Telegram (if configured)
        buf_top10.seek(0)
        send_telegram_photo(buf_top10, caption)

        # Send 1 SINGLE GTalk message with BOTH images
        buf_top10.seek(0)
        buf_am.seek(0)
        send_photos_gtalk_multi(
            [buf_top10, buf_am],
            ["report_top10.png", "report_am_ranking.png"],
            caption=caption
        )

        # Save data state
        save_data_state(sig)

    except Exception as e:
        print(f"⚠️ Lỗi tạo/gửi ảnh báo cáo: {e}")

    print("\n🎉 RẤT HOÀN HẢO! ĐÃ XỬ LÝ XONG!")

if __name__ == '__main__':
    main()
