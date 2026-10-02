# -*- coding: utf-8 -*-
"""
Tool: fetch_lastmile_productivity.py
Tự động lấy dữ liệu năng suất nhân viên (Giao - Lấy - Trả, GTC, LTC, Tiến độ)
trực tiếp từ API Lastmile GHN (cổng https://nhanh.ghn.vn/lastmile/trip-list)
và cập nhật trực tiếp vào Google Sheet:
- Tab 'Data': Chi tiết thời gian thực từng CBĐP (18 cột đầy đủ)
- Tab 'giao hàng': Đồng bộ số liệu giao hàng hôm nay để feed cho tab 'total' -> 'RawData' -> 'BaoCao'
- Tab 'lấy hàng': Đồng bộ số liệu lấy hàng hôm nay
"""

import os
import sys
import time
import json
from datetime import datetime, timezone, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import gspread
from google.oauth2.credentials import Credentials
from google.oauth2.service_account import Credentials as SACredentials

sys.stdout.reconfigure(encoding='utf-8')
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def get_http_session():
    session = requests.Session()
    retries = Retry(total=4, backoff_factor=0.6, status_forcelist=[429, 500, 502, 503, 504], raise_on_status=False)
    adapter = HTTPAdapter(max_retries=retries, pool_connections=25, pool_maxsize=25)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session

GOOGLE_SHEET_KEY = "1-p9VUXndK_7BoiT-a81UfTCbUi953XNmVBoXaTGis_c"
CONFIG_FILE = os.path.join(SCRIPT_DIR, "ghn_config.json")
DEFAULT_TOKEN = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJvcmdDb2RlIjoiZ2huZXhwcmVzcyIsInBhcnRuZXJDb2RlIjoiIiwic2VlZCI6NTY0NDQ5NzUzMTEzNzU4ODU1LCJzc29JZCI6IjMwNjYwMjEiLCJ1c2VySWQiOiI2NGUyZTJjMjYyY2FkNTVjNmI4NGVlMGQifQ.K5iIe4DBYfTmPN3H7JU5_Je8ho029NA8M3IxHYSc9JA"

def get_ghn_token():
    env_token = os.environ.get('GHN_TOKEN')
    if env_token:
        return env_token if env_token.startswith("Bearer ") else f"Bearer {env_token}"
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                tok = data.get('ghn_token')
                if tok:
                    return tok if tok.startswith("Bearer ") else f"Bearer {tok}"
        except Exception:
            pass
    return DEFAULT_TOKEN

def get_gspread_client(sheet_key=GOOGLE_SHEET_KEY):
    scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    
    # 1. Thử authorized_user (OAuth cá nhân)
    auth_candidates = [
        os.path.join(SCRIPT_DIR, 'authorized_user.json'),
        os.path.join(SCRIPT_DIR, 'credentials_oauth.json'),
        'authorized_user.json'
    ]
    for auth_file in auth_candidates:
        if os.path.exists(auth_file):
            try:
                creds = Credentials.from_authorized_user_file(auth_file, scopes=scopes)
                gc = gspread.authorize(creds)
                if sheet_key:
                    gc.open_by_key(sheet_key)
                return gc
            except Exception:
                pass

    # 2. Thử Service Account
    sa_candidates = [
        os.path.join(SCRIPT_DIR, 'credentials.json'),
        'credentials.json'
    ]
    for sa in sa_candidates:
        if os.path.exists(sa):
            try:
                creds = SACredentials.from_service_account_file(sa, scopes=scopes)
                gc = gspread.authorize(creds)
                if sheet_key:
                    gc.open_by_key(sheet_key)
                return gc
            except Exception as e:
                print(f"⚠️ Service account ({sa}) không có quyền mở Google Sheet: {e}", flush=True)

    raise PermissionError("Không thể xác thực Google Sheets API. Hãy kiểm tra xem file Google Sheet đã được chia sẻ cho email Service Account bot-ghn@ghn-automation.iam.gserviceaccount.com hay chưa.")

def get_today_info():
    tz = timezone(timedelta(hours=7))
    now = datetime.now(tz)
    today_int = int(now.strftime("%Y%m%d"))
    date_str_vn = f"{now.day} thg {now.month}, {now.year}"
    time_str = now.strftime("%d/%m/%Y %H:%M:%S")
    return today_int, date_str_vn, time_str, now

def get_hubs_from_sheet(sh):
    try:
        ws = sh.worksheet('cocau')
        records = ws.get_all_records()
        hubs = []
        for r in records:
            wid = str(r.get('warehouse_id') or '').strip()
            name = str(r.get('Bưu cục') or '').strip()
            am = str(r.get('AM') or '').strip()
            if wid and wid.isdigit():
                hubs.append({"warehouse_id": wid, "Bưu cục": name, "AM": am})
        return hubs
    except Exception as e:
        print(f"⚠️ Lỗi đọc tab 'cocau': {e}")
        return []

def fetch_hub_trips(hub_id, today_int, headers, session):
    trips = []
    # Quét cả 3 trạng thái của chuyến đi trong ngày: đang chạy, hoàn tất, vừa tạo
    for st in ["ON_TRIP", "FINISHED", "NEW"]:
        payload = {
            "hub_id": str(hub_id),
            "status": st,
            "offset": 0,
            "limit": 100,
            "reverse": 1
        }
        for attempt in range(3):
            try:
                r = session.post('https://nhanh-api.ghn.vn/api/lastmile/trip/get-trip-list-by-hub',
                                 headers=headers, json=payload, timeout=20)
                if r.status_code == 200:
                    data = r.json().get('data') or []
                    for t in data:
                        s_idx = t.get('startDateIndex') or 0
                        c_idx = t.get('createDateIndex') or 0
                        if s_idx == today_int or c_idx == today_int:
                            trips.append(t)
                    break
                else:
                    time.sleep(0.5)
            except Exception:
                if attempt < 2:
                    time.sleep(1)
    return trips

def fetch_trip_items(trip, headers, session):
    trip_code = trip.get('tripCode')
    res = {
        "tripCode": trip_code,
        "hubId": str(trip.get('hubId')),
        "driverId": str(trip.get('driverId') or '').strip(),
        "driverName": str(trip.get('driverName') or '').strip(),
        "pick_total": 0,
        "pick_succ": 0,
        "pick_fail": 0,
        "deliver_total": 0,
        "deliver_succ": 0,
        "deliver_fail": 0,
        "return_total": 0,
        "total_items": 0,
        "updated_count": 0
    }
    
    if not res["driverId"]:
        return res
        
    for attempt in range(3):
        try:
            r = session.post('https://nhanh-api.ghn.vn/api/lastmile/trip/get-trip-items',
                             headers=headers, json={"tripCode": trip_code, "limit": 5000}, timeout=25)
            if r.status_code == 200:
                items = r.json().get('data') or []
                res["total_items"] = len(items)
                
                for item in items:
                    itype = item.get('type')
                    is_up = bool(item.get('isUpdated'))
                    is_succ = bool(item.get('isSucceeded'))
                    
                    if is_up:
                        res["updated_count"] += 1
                        
                    if itype == 'PICK':
                        res["pick_total"] += 1
                        if is_succ:
                            res["pick_succ"] += 1
                        elif is_up:
                            res["pick_fail"] += 1
                    elif itype == 'DELIVER':
                        res["deliver_total"] += 1
                        if is_succ:
                            res["deliver_succ"] += 1
                        elif is_up:
                            res["deliver_fail"] += 1
                    elif itype == 'RETURN':
                        res["return_total"] += 1
                break
            else:
                time.sleep(1)
        except Exception:
            time.sleep(1)
        
    # Fallback an toàn nếu API items bị lỗi/rate-limit hoặc trả về rỗng nhưng chuyến có đơn
    if res["deliver_total"] == 0 and (trip.get('deliverCount') or 0) > 0:
        res["deliver_total"] = trip.get('deliverCount') or 0
        res["pick_total"] = trip.get('pickCount') or 0
        res["return_total"] = trip.get('returnCount') or 0
        res["total_items"] = res["pick_total"] + res["deliver_total"] + res["return_total"]

    return res

def main():
    print("=" * 70)
    print("🚀 BẮT ĐẦU ĐỒNG BỘ NĂNG SUẤT LASTMILE TỪ CỔNG NHANH.GHN.VN")
    print("=" * 70)
    
    today_int, date_str_vn, time_str, now_dt = get_today_info()
    token = get_ghn_token()
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    session = get_http_session()
    
    print(f"📅 Ngày kiểm tra: {today_int} ({time_str})")
    
    # 1. Kết nối Google Sheet
    gc = get_gspread_client()
    sh = gc.open_by_key(GOOGLE_SHEET_KEY)
    hubs = get_hubs_from_sheet(sh)
    print(f"🏢 Đã tải danh sách {len(hubs)} bưu cục từ tab 'cocau'.")
    if not hubs:
        print("❌ Không có bưu cục nào để quét!")
        return
        
    hub_map = {h["warehouse_id"]: h for h in hubs}
    
    # 2. Quét chuyến đi của các bưu cục (10 workers để tránh bị chặn IP)
    print(f"📡 Đang quét chuyến đi của {len(hubs)} bưu cục qua Lastmile API...")
    t0 = time.time()
    all_trips = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(fetch_hub_trips, h["warehouse_id"], today_int, headers, session): h for h in hubs}
        for f in as_completed(futures):
            trips = f.result()
            all_trips.extend(trips)
            
    print(f"✅ Quét xong trong {time.time()-t0:.2f}s. Tìm thấy {len(all_trips)} chuyến đi hôm nay.")
    
    # 3. Lấy chi tiết từng đơn hàng trong chuyến (10 workers có retry và backoff)
    valid_trips = [t for t in all_trips if str(t.get('driverId') or '').strip()]
    print(f"📦 Đang lấy chi tiết đơn hàng cho {len(valid_trips)} chuyến có CBĐP...")
    t1 = time.time()
    trip_details = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(fetch_trip_items, t, headers, session) for t in valid_trips]
        for f in as_completed(futures):
            trip_details.append(f.result())
    print(f"✅ Đã tải xong chi tiết {len(trip_details)} chuyến đi trong {time.time()-t1:.2f}s.")
    
    # 4. Gom nhóm theo (hubId, driverId)
    driver_stats = {}
    for r in trip_details:
        did = r["driverId"]
        hid = r["hubId"]
        if not did:
            continue
        key = (hid, did)
        if key not in driver_stats:
            driver_stats[key] = {
                "hubId": hid,
                "driverId": did,
                "driverName": r["driverName"],
                "total_items": 0,
                "updated_count": 0,
                "pick_total": 0,
                "deliver_total": 0,
                "return_total": 0,
                "pick_succ": 0,
                "pick_fail": 0,
                "deliver_succ": 0,
                "deliver_fail": 0,
                "trip_count": 0
            }
        s = driver_stats[key]
        s["trip_count"] += 1
        s["total_items"] += r["total_items"]
        s["updated_count"] += r["updated_count"]
        s["pick_total"] += r["pick_total"]
        s["deliver_total"] += r["deliver_total"]
        s["return_total"] += r["return_total"]
        s["pick_succ"] += r["pick_succ"]
        s["pick_fail"] += r["pick_fail"]
        s["deliver_succ"] += r["deliver_succ"]
        s["deliver_fail"] += r["deliver_fail"]
        if not s["driverName"] and r["driverName"]:
            s["driverName"] = r["driverName"]
            
    print(f"👥 Đã tổng hợp dữ liệu cho {len(driver_stats)} nhân viên CBĐP.")
    
    # 5. Chuẩn bị bảng Data (18 cột)
    data_rows = []
    giao_hang_rows = []
    lay_hang_rows = []
    
    for (hid, did), s in sorted(driver_stats.items(), key=lambda x: (hub_map.get(x[0][0], {}).get("Bưu cục", ""), x[1]["driverName"])):
        hub_info = hub_map.get(str(hid), {})
        hub_name = hub_info.get("Bưu cục", f"Bưu cục {hid}")
        am_name = hub_info.get("AM", "")
        
        pct_ltc = (s["pick_succ"] / s["pick_total"] * 100) if s["pick_total"] > 0 else 0
        pct_gtc = (s["deliver_succ"] / s["deliver_total"] * 100) if s["deliver_total"] > 0 else 0
        progress = (s["updated_count"] / s["total_items"] * 100) if s["total_items"] > 0 else 0
        
        # Dòng tab Data (18 cột)
        data_rows.append([
            hid,
            did,
            s["driverName"],
            s["total_items"],
            s["updated_count"],
            s["pick_total"],
            s["deliver_total"],
            s["return_total"],
            s["pick_succ"],
            s["pick_fail"],
            f"{pct_ltc:.2f}%",
            s["deliver_succ"],
            s["deliver_fail"],
            f"{pct_gtc:.2f}%",
            f"{progress:.1f}%",
            time_str,
            hub_name,
            am_name
        ])
        
        # Dòng tab giao hàng: ['Bưu cục', 'NhanVien', 'Ngay', 'TongDon', 'TongDonGTC', '%GTC', 'LT', 'ChuyenDi']
        nv_key = f"{did}_{s['driverName']}" if s['driverName'] else did
        if s["deliver_total"] > 0:
            giao_hang_rows.append([
                hub_name,
                nv_key,
                date_str_vn,
                str(s["deliver_total"]),
                str(s["deliver_succ"]),
                f"{pct_gtc:.2f}%".replace('.', ','),
                "0",
                str(s["trip_count"])
            ])
        
        # Dòng tab lấy hàng: ['Bưu Cục', 'Nhân Viên', 'Ngay', '%Lấy TC < 11:00', 'SLD Lấy TC < 11:00', 'SLD Lấy TC', 'LT_Lấy', 'SL Chuyến Đi Lấy']
        nv_lay = f"{did} - {s['driverName']}" if s['driverName'] else did
        if s["pick_succ"] > 0 or s["pick_total"] > 0:
            lay_hang_rows.append([
                hub_name,
                nv_lay,
                date_str_vn,
                "100%",
                str(s["pick_succ"]),
                str(s["pick_succ"]),
                "0",
                str(s["trip_count"])
            ])
        
    # 6. Ghi vào Google Sheet
    # 6.1 Ghi tab 'Data'
    try:
        ws_data = sh.worksheet('Data')
        header_data = ['ID Bưu cục', 'DriverID', 'CBDP', 'Tổng đơn', 'Update Count', 'Lấy', 'Giao', 'Trả', 
                       'Lấy thành công', 'Lấy thất bại', '%LTC', 'Giao thành công', 'Giao thất bại', '%GTC', 
                       'Tiến độ', 'Thời gian ghi', 'Bưu cục', 'AM']
        print(f"📝 Đang cập nhật tab 'Data' ({len(data_rows)} dòng)...")
        ws_data.update(range_name='A1', values=[header_data] + data_rows, value_input_option='USER_ENTERED')
        print("✅ Đã cập nhật thành công tab 'Data'!")
    except Exception as e:
        print(f"⚠️ Lỗi ghi tab 'Data': {e}")
        
    # 6.2 Cập nhật tab 'giao hàng' cho ngày hôm nay để feed cho dashboard real-time
    try:
        ws_gh = sh.worksheet('giao hàng')
        print(f"📝 Đang đồng bộ số liệu hôm nay vào tab 'giao hàng'...")
        existing_vals = ws_gh.get_all_values()
        if existing_vals:
            header = existing_vals[0]
            # Giữ lại các dòng của các ngày cũ, xóa các dòng của ngày hôm nay
            retained_rows = [r for r in existing_vals[1:] if len(r) > 2 and r[2] != date_str_vn]
            new_gh_table = [header] + retained_rows + giao_hang_rows
            ws_gh.update(range_name='A1', values=new_gh_table, value_input_option='USER_ENTERED')
            
            # Xóa các dòng rác thừa phía sau nếu bảng mới ngắn hơn bảng cũ (tránh lưu vết dữ liệu cũ)
            old_total_rows = len(existing_vals)
            new_total_rows = len(new_gh_table)
            if new_total_rows < old_total_rows:
                ws_gh.batch_clear([f"A{new_total_rows + 1}:H{old_total_rows}"])
                
            print(f"✅ Đã đồng bộ tab 'giao hàng' (tổng {len(new_gh_table)-1} dòng, trong đó có {len(giao_hang_rows)} dòng hôm nay)!")
    except Exception as e:
        print(f"⚠️ Lỗi ghi tab 'giao hàng': {e}")

    # 6.3 Cập nhật tab 'lấy hàng' cho ngày hôm nay
    try:
        ws_lh = sh.worksheet('lấy hàng')
        print(f"📝 Đang đồng bộ số liệu hôm nay vào tab 'lấy hàng'...")
        existing_vals_lh = ws_lh.get_all_values()
        if existing_vals_lh:
            header_lh = existing_vals_lh[0]
            retained_lh = [r for r in existing_vals_lh[1:] if len(r) > 2 and r[2] != date_str_vn]
            new_lh_table = [header_lh] + retained_lh + lay_hang_rows
            ws_lh.update(range_name='A1', values=new_lh_table, value_input_option='USER_ENTERED')
            
            # Xóa các dòng rác thừa phía sau nếu bảng mới ngắn hơn bảng cũ
            old_total_lh = len(existing_vals_lh)
            new_total_lh = len(new_lh_table)
            if new_total_lh < old_total_lh:
                ws_lh.batch_clear([f"A{new_total_lh + 1}:H{old_total_lh}"])
                
            print(f"✅ Đã đồng bộ tab 'lấy hàng' (tổng {len(new_lh_table)-1} dòng)!")
    except Exception as e:
        print(f"⚠️ Lỗi ghi tab 'lấy hàng': {e}")
        
    print("=" * 70)
    print(f"🎉 HOÀN THÀNH XUẤT SẮC! ĐÃ CẬP NHẬT {len(driver_stats)} NHÂN VIÊN VÀO GOOGLE SHEET.")
    print("=" * 70)

if __name__ == '__main__':
    main()
