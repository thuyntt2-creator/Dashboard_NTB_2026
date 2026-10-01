code = '''"""
╔══════════════════════════════════════════════════════════════╗
║         SCRIPT BÁO CÁO PIVOT & XUẤT NHẬP KTC + GTALK         ║
║  Chế độ: NONE LT (Không đọc/xử lý Leadtime từ tab raw)       ║
║  Đọc tab "PIVOT" & "Xuất Nhập KTC" → Tạo 2 ảnh → gửi GTalk   ║
╚══════════════════════════════════════════════════════════════╝
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import requests
import os
import io
import sys
import time
import json
from datetime import datetime, timedelta
import gspread
import urllib3
from google.oauth2.service_account import Credentials
from google.oauth2.credentials import Credentials as UserCredentials

# Tắt cảnh báo SSL InsecureRequestWarning khi verify=False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Fix encoding cho Task Scheduler/Command Prompt trên Windows
os.environ['PYTHONIOENCODING'] = 'utf-8'
try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
except AttributeError:
    pass

# ============================================================
# ⚙️  CẤU HÌNH SHEET & GTALK
# ============================================================
SHEET_ID_BACKLOG  = '1CbXJb_-HqGGcOep8R6Zf6qBn8gGi_8EyLkr8ebhEdzI'

SHEET_PIVOT       = 'PIVOT'
SHEET_XUAT_NHAP   = 'Xuất Nhập KTC'

# Bật gửi GTalk thật khi chạy script
ENABLE_SEND_GTALK = True

# Cấu hình GTalk của Thủy
GTALK_CHANNEL     = '2090872805929144320'
GTALK_TOKEN       = '2077276776281051136:8hMHvBBU8qXKps3mLPzgKBucPLSQPg3Y'

FOLDER_PATH       = r'C:\\Users\\lap4all\\Desktop\\Backlog_Automation'
OUTPUT_DIR        = '.'
SCOPES            = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
]
# ============================================================

ORANGE='#F26522'; BLUE='#0072BC'; BLUE2='#1F4E79'; WHITE='#FFFFFF'
YELLOW_BG='#FFF2CC'; YELLOW_TXT='#7F6000'
RED_BG='#FFCCCC';    RED_TXT='#C00000'
GREEN_BG='#E2EFDA';  GREEN_TXT='#375623'
GRAY='#F5F5F5';      ALT='#EEF4FB'
TONG_BG='#FFC000';   TONG_TXT='#7F3F00'

TODAY = datetime.today().strftime('%d/%m/%Y')

def find_file(filename):
    search_paths = [
        FOLDER_PATH,
        r'C:\\Users\\lap4all\\Documents\\Auto report',
        os.getcwd()
    ]
    for p in search_paths:
        full = os.path.join(p, filename)
        if os.path.exists(full):
            return full
    return None

def get_gspread_client(sheet_key=None):
    auth_user = find_file('authorized_user.json')
    if auth_user:
        try:
            creds = UserCredentials.from_authorized_user_file(auth_user, scopes=SCOPES)
            gc = gspread.authorize(creds)
            if sheet_key:
                gc.open_by_key(sheet_key)
            print(f"🔐 Kết nối Google Sheets qua OAuth User ({os.path.basename(auth_user)}) thành công!")
            return gc
        except Exception as e:
            print(f"⚠️ OAuth User ({auth_user}) lỗi: {e}")

    cred_file = find_file('credentials.json')
    if cred_file:
        try:
            creds = Credentials.from_service_account_file(cred_file, scopes=SCOPES)
            gc = gspread.authorize(creds)
            if sheet_key:
                gc.open_by_key(sheet_key)
            print(f"🔐 Kết nối Google Sheets qua Service Account ({os.path.basename(cred_file)}) thành công!")
            return gc
        except Exception as e:
            print(f"⚠️ Service Account ({cred_file}) lỗi: {e}")

    raise PermissionError("Không thể tìm thấy file authorized_user.json hoặc credentials.json hợp lệ.")


# ============================================================
# BƯỚC 1: LOAD DATA (CHỈ LẤY PIVOT VÀ XUẤT NHẬP)
# ============================================================
def load_data():
    print(f"🔄 Kết nối Google Sheets...")

    gc = get_gspread_client(SHEET_ID_BACKLOG)
    sh_backlog = gc.open_by_key(SHEET_ID_BACKLOG)

    print(f"📥 Đang tải tab '{SHEET_PIVOT}'...")
    df_pivot_raw = pd.DataFrame(sh_backlog.worksheet(SHEET_PIVOT).get_all_values())

    print(f"📥 Đang tải tab '{SHEET_XUAT_NHAP}'...")
    xn_raw = sh_backlog.worksheet(SHEET_XUAT_NHAP).get_all_values()
    df_xuat_nhap = pd.DataFrame(xn_raw[1:], columns=xn_raw[0]) if xn_raw else pd.DataFrame()
    if not df_xuat_nhap.empty and 'ngay' in df_xuat_nhap.columns:
        df_xuat_nhap = df_xuat_nhap[['ngay','type','warehouseid','volumedonhang','warehouse_name']].copy()
        for col in ['volumedonhang']:
            if col in df_xuat_nhap.columns:
                df_xuat_nhap[col] = pd.to_numeric(df_xuat_nhap[col], errors='coerce').fillna(0)

    print(f"✅ Đã tải: PIVOT ({len(df_pivot_raw)} dòng) | Xuất nhập ({len(df_xuat_nhap)} dòng)")
    return gc, df_pivot_raw, df_xuat_nhap


# ============================================================
# BƯỚC 2: TẠO ẢNH PIVOT
# ============================================================
def to_str(val):
    if val is None: return ''
    if isinstance(val, float) and np.isnan(val): return ''
    return str(val).strip()

def short_kho(name):
    return str(name).replace('Kho Trung Chuyển ','KTC ').replace('Kho Chuyển Tiếp ','KCT ')

def draw_block(ax, title, col_headers, rows, x0, y0, col_widths, row_h=0.055,
               title_color=BLUE2, is_tong_last=True, table3=False):
    total_w = sum(col_widths)
    th = 0.046

    ax.add_patch(FancyBboxPatch((x0, y0-th), total_w, th,
        boxstyle='square,pad=0', facecolor=title_color, edgecolor='none', transform=ax.transAxes))
    ax.text(x0+total_w/2, y0-th/2, title, ha='center', va='center',
            fontsize=11.5, fontweight='bold', color=WHITE, transform=ax.transAxes)

    cx = x0
    for ci, (col, w) in enumerate(zip(col_headers, col_widths)):
        bg = BLUE2 if ci==0 else BLUE
        ax.add_patch(FancyBboxPatch((cx, y0-th-row_h), w, row_h,
            boxstyle='square,pad=0', facecolor=bg, edgecolor=WHITE, linewidth=0.3, transform=ax.transAxes))
        ax.text(cx+w/2, y0-th-row_h/2, col, ha='center', va='center',
                fontsize=9.5, fontweight='bold', color=WHITE, transform=ax.transAxes)
        cx += w

    for ri, row in enumerate(rows):
        ry = y0 - th - row_h - (ri+1)*row_h
        cx = x0
        is_tong = is_tong_last and ri == len(rows)-1
        last_ci = len(col_widths)-1

        for ci, (val, w) in enumerate(zip(row, col_widths)):
            val = to_str(val)
            if is_tong:
                bg=TONG_BG; tc=TONG_TXT; fw='bold'
            elif ci==0:
                bg=ALT if ri%2==0 else WHITE; tc='black'; fw='bold' if is_tong else 'normal'
            elif ci==last_ci and not table3:
                bg='#DDEEFF'; tc=BLUE2; fw='bold'
            elif not table3:
                try: num=float(val.replace(',','')) if val else 0
                except: num=0
                if ci in [4,5] and num>0: bg=YELLOW_BG; tc=YELLOW_TXT; fw='bold'
                elif ci in [6,7,8] and num>0: bg=RED_BG; tc=RED_TXT; fw='bold'
                else: bg=ALT if ri%2==0 else WHITE; tc='black'; fw='normal'
            else:
                if ci==1: bg=GREEN_BG; tc=GREEN_TXT; fw='bold'
                elif ci==2: bg='#FDE9DE'; tc=ORANGE; fw='normal'
                else: bg=ALT if ri%2==0 else WHITE; tc='#888888'; fw='normal'

            ax.add_patch(FancyBboxPatch((cx, ry), w, row_h,
                boxstyle='square,pad=0', facecolor=bg, edgecolor='#CCCCCC',
                linewidth=0.3, transform=ax.transAxes))

            lines = val.split('\\n')
            if len(lines) > 1:
                ax.text(cx+w/2, ry+row_h*0.65, lines[0], ha='center', va='center',
                        fontsize=9.5, fontweight=fw, color=tc, transform=ax.transAxes)
                ax.text(cx+w/2, ry+row_h*0.25, lines[1], ha='center', va='center',
                        fontsize=7.5, color=tc, transform=ax.transAxes)
            else:
                ax.text(cx+w/2, ry+row_h/2, val if val not in ['nan','NaN',''] else '',
                        ha='center', va='center', fontsize=10.0, fontweight=fw, color=tc, transform=ax.transAxes)
            cx += w

    return y0 - th - row_h - len(rows)*row_h


def create_img_pivot(df_raw):
    n_rows = len(df_raw)
    n_cols = len(df_raw.columns)

    block1_header_idx = 1
    for r in range(0, min(5, n_rows)):
        if to_str(df_raw.iloc[r, 0]) == 'AM':
            block1_header_idx = r
            break

    cols1 = [to_str(df_raw.iloc[block1_header_idx, c]) for c in range(1, min(10, n_cols))]
    data1 = []
    r = block1_header_idx + 1
    while r < n_rows:
        row = [to_str(df_raw.iloc[r, c]) for c in range(0, min(10, n_cols))]
        cell_0 = to_str(df_raw.iloc[r, 0])
        if not cell_0 or cell_0 == 'Backlog KTC':
            break
        data1.append(row)
        if cell_0 == 'TỔNG':
            break
        r += 1

    block2_header_idx = 8
    for i in range(1, n_rows):
        if to_str(df_raw.iloc[i, 0]) in ['Bưu cục', 'KHO', 'Kho']:
            block2_header_idx = i
            break

    cols2 = [to_str(df_raw.iloc[block2_header_idx, c]) for c in range(1, min(10, n_cols))] if n_rows > block2_header_idx else []
    data2 = []
    r = block2_header_idx + 1
    while r < n_rows:
        cell_0 = to_str(df_raw.iloc[r, 0])
        cell_1 = to_str(df_raw.iloc[r, 1])
        if not cell_0 or 'Đơn treo' in cell_0 or 'Đơn treo' in cell_1:
            break
        row = [to_str(df_raw.iloc[r, c]) for c in range(0, min(10, n_cols))]
        row[0] = short_kho(row[0])
        data2.append(row)
        r += 1

    header3_idx = 17
    for i in range(block2_header_idx + 1, n_rows):
        cell_0 = to_str(df_raw.iloc[i, 0])
        cell_1 = to_str(df_raw.iloc[i, 1])
        if 'Ngày' in cell_1 or 'ngày' in cell_1 or cell_0 == 'AM':
            header3_idx = i
            break

    cols3 = [to_str(df_raw.iloc[header3_idx, c]).replace('\\n', ' ') for c in range(1, min(9, n_cols))] if n_rows > header3_idx else []
    data3 = []
    r = header3_idx + 1
    while r < n_rows:
        cell_0 = to_str(df_raw.iloc[r, 0])
        if not cell_0:
            break
        row = [to_str(df_raw.iloc[r, c]) for c in range(0, min(9, n_cols))]
        data3.append(row)
        if cell_0 == 'TỔNG':
            break
        r += 1

    fig, ax = plt.subplots(figsize=(14, 10.5))
    ax.axis('off')
    fig.patch.set_facecolor(GRAY)
    ax.set_facecolor(GRAY)

    ax.text(0.5, 0.99, f'BACKLOG LUÂN CHUYỂN KTC/KCT  —  {TODAY}',
            ha='center', va='top', fontsize=14, fontweight='bold', color=WHITE,
            bbox=dict(boxstyle='round,pad=0.4', facecolor=ORANGE, edgecolor='none'),
            transform=ax.transAxes)

    y = 0.93

    if cols1 and data1:
        y = draw_block(ax,
            'Đơn treo LUÂN CHUYỂN giao/trả trên 36h (Chưa/Không cần đóng kiện)',
            ['AM'] + cols1, data1,
            0.0, y, [0.23] + [0.085]*8 + [0.073],
            row_h=0.055, title_color=BLUE2)

    y -= 0.016

    if cols2 and data2:
        y = draw_block(ax,
            'Backlog KTC',
            ['KHO'] + cols2, data2,
            0.0, y, [0.26] + [0.082]*8 + [0.068],
            row_h=0.055, title_color=BLUE, is_tong_last=False)

    y -= 0.016

    if cols3 and data3:
        draw_block(ax,
            'Đơn treo LUÂN CHUYỂN giao/trả >24h — Mốc 7h30 hằng ngày',
            ['AM'] + cols3, data3,
            0.0, y, [0.23] + [0.096]*8,
            row_h=0.060, title_color=BLUE2, table3=True)

    path = os.path.join(OUTPUT_DIR, 'img_pivot.png')
    plt.tight_layout(rect=[0, 0, 1, 0.97])
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor=GRAY, edgecolor='none')
    plt.close()
    print(f"✅ Ảnh Pivot: {path}")
    return path


# ============================================================
# BƯỚC 3: TẠO ẢNH XUẤT NHẬP
# ============================================================
def create_img_xuat_nhap(df_xn):
    keep = ['1.Nhập - đã nhận','4.Xuất - Đã xuất']
    xn_date = TODAY
    if not df_xn.empty and 'ngay' in df_xn.columns:
        latest = df_xn['ngay'].max()
        df_xn = df_xn[df_xn['ngay'] == latest]
        try:
            xn_date = pd.to_datetime(latest).strftime('%d/%m/%Y')
        except:
            xn_date = str(latest)
        print(f"  Xuất nhập: lấy dữ liệu ngày {xn_date}")
    
    if not df_xn.empty and 'type' in df_xn.columns:
        df2 = df_xn[df_xn['type'].isin(keep)].copy()
        df2['t'] = df2['type'].map({'1.Nhập - đã nhận':'Nhập','4.Xuất - Đã xuất':'Xuất'})
        xn = df2.groupby(['warehouse_name','t'])['volumedonhang'].sum().reset_index()
        xp = xn.pivot(index='warehouse_name', columns='t', values='volumedonhang').fillna(0)
        xp.index = [short_kho(i) for i in xp.index]
        for c in ['Nhập','Xuất']:
            if c not in xp.columns: xp[c] = 0
        xp = xp[['Nhập','Xuất']].astype(int)
        rows = [[idx, f'{row.Nhập:,}', f'{row.Xuất:,}'] for idx, row in xp.iterrows()]
    else:
        rows = []

    fig, ax = plt.subplots(figsize=(8.5, max(3.8, 1.0 + len(rows)*0.45)))
    ax.axis('off'); fig.patch.set_facecolor(GRAY); ax.set_facecolor(GRAY)
    
    ax.text(0.5, 0.99, f'XUẤT NHẬP KTC/KCT  —  {xn_date}',
            ha='center', va='top', fontsize=14, fontweight='bold', color=WHITE,
            bbox=dict(boxstyle='round,pad=0.4', facecolor=ORANGE, edgecolor='none'),
            transform=ax.transAxes)

    cw=[0.5,0.25,0.25]; ch=['KHO','Nhập (đơn)','Xuất (đơn)']
    y0=0.88; hh=0.10; rh=0.10
    cx=0.0
    for ci,(col,w) in enumerate(zip(ch,cw)):
        bg=BLUE2 if ci==0 else BLUE
        ax.add_patch(FancyBboxPatch((cx,y0-hh),w,hh,boxstyle='square,pad=0',facecolor=bg,edgecolor=WHITE,linewidth=0.3,transform=ax.transAxes))
        ax.text(cx+w/2,y0-hh/2,col,ha='center',va='center',fontsize=11.5,fontweight='bold',color=WHITE,transform=ax.transAxes)
        cx+=w
    for ri,row in enumerate(rows):
        ry=y0-hh-(ri+1)*rh; cx=0.0
        for ci,(val,w) in enumerate(zip(row,cw)):
            if ci==0: bg=ALT if ri%2==0 else WHITE; tc='black'; fw='normal'
            elif ci==1: bg=GREEN_BG; tc=GREEN_TXT; fw='bold'
            else: bg='#FDE9DE'; tc=ORANGE; fw='bold'
            ax.add_patch(FancyBboxPatch((cx,ry),w,rh,boxstyle='square,pad=0',facecolor=bg,edgecolor='#CCCCCC',linewidth=0.3,transform=ax.transAxes))
            ax.text(cx+w/2,ry+rh/2,val,ha='center',va='center',fontsize=11.5,fontweight=fw,color=tc,transform=ax.transAxes)
            cx+=w

    path = os.path.join(OUTPUT_DIR, 'img_xuat_nhap.png')
    plt.tight_layout(rect=[0,0,1,0.95])
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor=GRAY, edgecolor='none')
    plt.close()
    print(f"✅ Ảnh Xuất Nhập ({xn_date}): {path}")
    return path, xn_date


# ============================================================
# BƯỚC 4: HÀM GỬI ẢNH SANG GTALK
# ============================================================
def send_gtalk_photo(image_path, caption="", channel_id=GTALK_CHANNEL, token=GTALK_TOKEN):
    if not os.path.exists(image_path):
        print(f"⚠️ File ảnh không tồn tại: {image_path}")
        return

    if not ENABLE_SEND_GTALK:
        print(f"🔒 [CHẾ ĐỘ AN TOÀN - KHÔNG GỬI VÀO GROUP] Bỏ qua gửi ảnh: {image_path} (Caption: {caption})")
        return
    
    file_name = os.path.basename(image_path)
    file_size = os.path.getsize(image_path)
    with open(image_path, 'rb') as f:
        file_bytes = f.read()

    init_payload = {
        "ChannelId": channel_id,
        "FileName": file_name,
        "FileSize": str(file_size),
        "MimeType": "image/png",
        "Metadata": json.dumps({"width": 1700, "height": 1000}),
        "oaToken": token
    }

    try:
        resp_init = requests.post("https://mbff.ghn.vn/api/gtalk/initiate-upload", json=init_payload, timeout=30, verify=False)
        if resp_init.status_code == 200:
            init_data = resp_init.json()
            if init_data.get("errorCode") == "success":
                presigned_url = init_data["data"]["PresignedURL"]
                upload_id = init_data["data"]["UploadId"]
                
                resp_put = requests.put(presigned_url, data=file_bytes, headers={"Content-Type": "image/png"}, timeout=30, verify=False)
                if resp_put.status_code == 200:
                    resp_comp = requests.post("https://mbff.ghn.vn/api/gtalk/complete-upload", json={"oaToken": token, "UploadId": upload_id}, timeout=30, verify=False)
                    if resp_comp.status_code == 200 and resp_comp.json().get("errorCode") == "success":
                        comp_data = resp_comp.json()
                        file_id = comp_data["data"]["Id"]
                        
                        send_payload = {
                            "channelId": channel_id,
                            "clientMsgId": str(int(time.time() * 1000)),
                            "content": {
                                "parseMode": "HTML",
                                "attachment": {
                                    "caption": caption,
                                    "items": [{"image": {"fileId": file_id, "width": 1700, "height": 1000}}]
                                }
                            },
                            "oaToken": token
                        }
                        r_send = requests.post("https://mbff.ghn.vn/api/gtalk/send-message", json=send_payload, timeout=30, verify=False)
                        if r_send.status_code == 200 and r_send.json().get("errorCode") == "success":
                            print(f"✅ Đã gửi ảnh ({file_name}) sang GTalk thành công!")
                        else:
                            print(f"❌ Lỗi gửi tin nhắn ảnh GTalk: {r_send.text}")
                    else:
                        print(f"❌ Complete upload GTalk lỗi: {resp_comp.text}")
                else:
                    print(f"❌ Put binary image GTalk lỗi status {resp_put.status_code}")
            else:
                print(f"❌ Initiate upload GTalk thất bại: {init_data}")
        else:
            print(f"❌ Initiate upload GTalk HTTP {resp_init.status_code}: {resp_init.text}")
    except Exception as e:
        print(f"❌ Exception gửi ảnh GTalk: {e}")


# ============================================================
# MAIN
# ============================================================
if __name__ == '__main__':
    print("="*50)
    print(f"BÁO CÁO PIVOT & XUẤT NHẬP KTC — BẮT ĐẦU CHẠY (NONE LT)")
    print(f"Trạng thái gửi GTalk: {'🔴 BẬT (Gửi thật)' if ENABLE_SEND_GTALK else '🟢 TẮT (Chế độ an toàn)'}")
    print("="*50)

    # 1. Chỉ tải PIVOT và Xuất Nhập (hoàn toàn không đụng vào tab raw)
    gc, df_pivot_raw, df_xuat_nhap = load_data()

    # 2. Tạo 2 ảnh
    print("🎨 Tạo các ảnh phân tích...")
    path_pivot              = create_img_pivot(df_pivot_raw)
    path_xuat_nhap, xn_date = create_img_xuat_nhap(df_xuat_nhap)

    # 3. Gửi 2 ảnh sang GTalk
    print("📨 Xử lý gửi báo cáo sang GTalk...")
    send_gtalk_photo(path_pivot, caption=f'Backlog luân chuyển theo khung giờ — {TODAY}')
    time.sleep(1)
    send_gtalk_photo(path_xuat_nhap, caption=f'Xuất Nhập KTC/KCT — {xn_date}')

    print(f"🎉 XONG! Đã hoàn thành gửi 2 ảnh Pivot và Xuất Nhập!")
'''

with open(r'C:\Users\lap4all\Documents\Auto report\none LT KTC.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Overwritten none LT KTC.py cleanly!")
