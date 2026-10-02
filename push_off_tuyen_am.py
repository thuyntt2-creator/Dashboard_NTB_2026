# -*- coding: utf-8 -*-
"""
Script: push_off_tuyen_am.py
Đọc kết quả Off tuyến từ tab 'Tổng Hợp KA OFF' thuộc Google Sheet:
https://docs.google.com/spreadsheets/d/1PjzFqJO-wkQ8SNsPHD721_CbPr6c_ArZKuGGU6KqDZg/edit#gid=583983570

Tính năng:
1. Đọc dữ liệu đã map ID chuẩn từ tab 'Tổng Hợp KA OFF'.
2. Gom nhóm dữ liệu theo AM & BƯU CỤC, phân loại nguồn đề xuất (SPE đề xuất mới / SPE đề xuất thêm / Đã có ở Vùng).
3. Định dạng tin nhắn HTML trực quan (kèm link Google Sheet) gửi tới Group ID riêng của từng AM qua GTalk API.
4. MẶC ĐỊNH: DRY-RUN (chỉ xem trước, KHÔNG tự ý gửi GTalk nếu không có tham số --send).

Cách dùng:
- Dry Run (chỉ xem trước tin nhắn mẫu, KHÔNG gửi GTalk):
    python push_off_tuyen_am.py
- Gửi thật qua GTalk API (chỉ chạy khi được yêu cầu):
    python push_off_tuyen_am.py --send
"""

import os
import sys
import time
import json
import argparse
import unicodedata
import requests
import gspread
from google.oauth2.service_account import Credentials

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Mã hóa UTF-8 cho Windows Console
os.environ['PYTHONIOENCODING'] = 'utf-8'
try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SPREADSHEET_ID = "1PjzFqJO-wkQ8SNsPHD721_CbPr6c_ArZKuGGU6KqDZg"
TAB_NAME = "Tổng Hợp KA OFF"
SHEET_LINK = "https://docs.google.com/spreadsheets/d/1PjzFqJO-wkQ8SNsPHD721_CbPr6c_ArZKuGGU6KqDZg/edit?gid=583983570#gid=583983570"

# Token GTalk OA
DEFAULT_TOKEN = "2077276776281051136:8hMHvBBU8qXKps3mLPzgKBucPLSQPg3Y"
GTALK_API_URL = "https://mbff.ghn.vn/api/gtalk/send-message"

SERVICE_ACCOUNT_CANDIDATES = [
    os.path.join(BASE_DIR, "credentials.json"),
    r"C:\Users\lap4all\Desktop\Backlog_Automation\credentials.json",
    r"C:\Users\lap4all\Downloads\credentials.json",
    "credentials.json",
]

# Mapping Tên AM -> ID Group riêng biệt của AM
AM_GROUP_MAP = {
    "Nguyễn Ngọc Khánh": "2077277510775197696",
    "Nguyễn Duy Long": "2077277718988836864",
    "Lê Thanh Nhựt": "2077277754418147328",
    "Trần Văn Phước": "2077277797832024064",
    "Trần Thị Nhung": "2077277827057745920",
    "Huỳnh Thị Kim Chi": "2077277857186131968",
    "Phan Đình Duy": "2077278383281876992",
    "Phạm Bá Thành Công": "2077277907735883776",
    "Thái Thị Thanh Thư": "2077277934947827712",
    "Nguyễn Thanh Long": "2077277974325506048",
    "Nguyễn Hoàng Phi": "2077278021170323456",
    "Trầm Hữu Tiến": "2077278046487142400",
    "Nguyễn Lê Nguyên Vũ": "2077278095459835904",
    "Lê Văn Trường": "2077278127814696960",
    "Hồng Bích Nga": "2077278157729837056",
    "Lê Minh Đại": "2077278182818799616",
    "Phan Thị Ngọc Diễm": "2079827073949868032",
    "Lê Hồng Minh Tâm": "2079827054540226560",
    "Huỳnh Thúc Duân": "2077277857186131968",    # AM Đắk Nông
    "Nguyễn Minh Hoàng": "2077278127814696960",  # AM Lâm Đồng - Đức Trọng
    "Trương Quang Linh": "2077277857186131968",  # AM Đắk Nông - Quảng Tín
    "Phan Nguyễn Yến Nhi": "2105595062412402688",
}


def normalize_str(s):
    if not s:
        return ""
    return unicodedata.normalize("NFC", str(s)).strip()


def get_gspread_client(sheet_key=None):
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    for cred_file in SERVICE_ACCOUNT_CANDIDATES:
        if os.path.exists(cred_file):
            try:
                creds = Credentials.from_service_account_file(cred_file, scopes=scopes)
                gc = gspread.authorize(creds)
                if sheet_key:
                    gc.open_by_key(sheet_key)
                return gc
            except Exception:
                pass

    auth_candidates = [
        os.path.join(BASE_DIR, 'authorized_user.json'),
        r"C:\Users\lap4all\Documents\Auto report\authorized_user.json",
        r"C:\Users\lap4all\Desktop\New folder\authorized_user.json",
        "authorized_user.json"
    ]
    for auth_user_file in auth_candidates:
        if os.path.exists(auth_user_file):
            try:
                from google.oauth2.credentials import Credentials as UserCredentials
                creds = UserCredentials.from_authorized_user_file(auth_user_file, scopes=scopes)
                gc = gspread.authorize(creds)
                if sheet_key:
                    gc.open_by_key(sheet_key)
                return gc
            except Exception:
                pass

    oauth_candidates = [
        os.path.join(BASE_DIR, 'credentials_oauth.json'),
        r"C:\Users\lap4all\Documents\Auto report\credentials_oauth.json",
        r"C:\Users\lap4all\Desktop\New folder\credentials_oauth.json",
        "credentials_oauth.json"
    ]
    for oauth_file in oauth_candidates:
        if os.path.exists(oauth_file):
            try:
                gc = gspread.oauth(
                    credentials_filename=oauth_file,
                    authorized_user_filename=auth_candidates[0]
                )
                if sheet_key:
                    gc.open_by_key(sheet_key)
                return gc
            except Exception:
                pass

    raise PermissionError("❌ Không thể xác thực Google Sheets bằng credentials.json hoặc OAuth (authorized_user.json).")


TAB_GTALK = "gtalk"

def load_sheet_data():
    """
    Đọc dữ liệu từ 2 tab:
    1. 'Tổng Hợp KA OFF' (chứa danh sách tuyến cần tắt gom theo AM/Bưu cục)
    2. 'gtalk' (chứa token GTalk và ID Group chat riêng của từng AM)
    """
    gc = get_gspread_client(SPREADSHEET_ID)
    sh = gc.open_by_key(SPREADSHEET_ID)

    # 1. Tìm tab Tổng Hợp KA OFF
    ws_th = None
    for item in sh.worksheets():
        t_low = item.title.lower()
        if "tổng hợp ka" in t_low or "tong hop ka" in t_low:
            ws_th = item
            break

    if not ws_th:
        try:
            ws_th = sh.worksheet(TAB_NAME)
        except Exception:
            ws_th = sh.get_worksheet(0)

    th_rows = ws_th.get_all_values()

    # 2. Tìm tab gtalk
    ws_gtalk = None
    for item in sh.worksheets():
        if item.title.strip().lower() == TAB_GTALK.lower():
            ws_gtalk = item
            break

    gtalk_rows = []
    if ws_gtalk:
        try:
            gtalk_rows = ws_gtalk.get_all_values()
        except Exception as e:
            print(f"⚠️ Không thể đọc tab '{TAB_GTALK}': {e}")
    else:
        print(f"⚠️ Không tìm thấy tab '{TAB_GTALK}' trên Google Sheet!")

    return th_rows, gtalk_rows


def parse_gtalk_config(gtalk_rows):
    """
    Phân tích dữ liệu từ tab 'gtalk':
    - Hàng có cột A là 'token': lấy giá trị cột B làm OA Token
    - Các hàng còn lại: Cột A là Tên AM, Cột B là Group ID của AM
    """
    sheet_token = None
    gtalk_map = {}

    for row in gtalk_rows:
        if not row or not any(row):
            continue
        c0 = normalize_str(row[0])
        c1 = normalize_str(row[1]) if len(row) > 1 else ""

        if c0.lower() == "token":
            if c1:
                sheet_token = c1
        elif c0:
            gtalk_map[c0.lower()] = {
                "am_name": c0,
                "group_id": c1
            }

    return sheet_token, gtalk_map


def parse_off_data(rows, gtalk_map=None):
    if not rows or len(rows) < 2:
        return {}

    if gtalk_map is None:
        gtalk_map = {}

    header_row = [normalize_str(h).lower() for h in rows[0]]
    
    def get_col_idx(keywords, default_idx):
        for idx, h in enumerate(header_row):
            for kw in keywords:
                if kw in h:
                    return idx
        return default_idx

    col_tinh = get_col_idx(["tỉnh", "province"], 0)
    col_huyen = get_col_idx(["quận", "huyện", "district"], 1)
    col_xa = get_col_idx(["phường/xã", "phường", "xã"], 2)
    col_id = get_col_idx(["id phường", "ward_code", "id"], 3)
    col_bc = get_col_idx(["bưu cục", "post_office"], 4)
    col_am = get_col_idx(["am"], 5)
    col_kq = get_col_idx(["kết quả", "result"], 6)
    col_tg_tat = get_col_idx(["thời gian tắt", "tg tắt"], 7)
    col_tg_mo = get_col_idx(["thời gian mở", "tg mở"], 8)
    col_phan_loai = get_col_idx(["phân loại", "đề xuất"], 9)

    # Từ điển tra cứu tên chuẩn AM
    norm_am_map = {normalize_str(k).lower(): k for k in AM_GROUP_MAP.keys()}
    for k_lower, v_info in gtalk_map.items():
        norm_am_map[k_lower] = v_info["am_name"]

    am_data = {}

    for i in range(1, len(rows)):
        row = rows[i]
        if not any(row):
            continue

        province = normalize_str(row[col_tinh]) if len(row) > col_tinh else ""
        district = normalize_str(row[col_huyen]) if len(row) > col_huyen else ""
        ward = normalize_str(row[col_xa]) if len(row) > col_xa else ""
        ward_id = normalize_str(row[col_id]) if len(row) > col_id else ""
        post_office = normalize_str(row[col_bc]) if len(row) > col_bc else ""
        am_name = normalize_str(row[col_am]) if len(row) > col_am else ""
        result = normalize_str(row[col_kq]) if len(row) > col_kq else "DUYỆT"
        off_from = normalize_str(row[col_tg_tat]) if len(row) > col_tg_tat else ""
        off_to = normalize_str(row[col_tg_mo]) if len(row) > col_tg_mo else ""
        phan_loai = normalize_str(row[col_phan_loai]) if len(row) > col_phan_loai else ""

        if not am_name:
            continue

        norm_key = am_name.lower()
        canonical_am = norm_am_map.get(norm_key, am_name)

        ward_info = {
            "province": province,
            "district": district,
            "ward": ward,
            "ward_id": ward_id,
            "post_office": post_office,
            "result": result or "DUYỆT",
            "off_from": off_from,
            "off_to": off_to,
            "phan_loai": phan_loai,
            "am": canonical_am
        }

        bc_key = post_office or "CHƯA XÁC ĐỊNH"

        if canonical_am not in am_data:
            am_data[canonical_am] = {}
        if bc_key not in am_data[canonical_am]:
            am_data[canonical_am][bc_key] = {
                "bc_name": bc_key,
                "result": result or "DUYỆT",
                "off_from": off_from,
                "off_to": off_to,
                "wards": []
            }
        am_data[canonical_am][bc_key]["wards"].append(ward_info)

    return am_data


def format_am_text_message(am_name, am_bcs, is_supplement=False):
    """
    Định dạng tin nhắn riêng cho từng AM gom nhóm theo Bưu cục và liệt kê các xã/phường + Link Google Sheet.
    """
    total_wards = sum(len(b["wards"]) for b in am_bcs.values())
    total_bcs = len(am_bcs)

    title_prefix = "📢 <b>[BỔ SUNG] THÔNG BÁO TUYẾN SPE — AM: " if is_supplement else "📢 <b>THÔNG BÁO TUYẾN SPE — AM: "
    msg = f"{title_prefix}{am_name}</b>\n"
    msg += f"📊 <b>Tổng số:</b> {total_wards} Xã/Phường | {total_bcs} Bưu cục phụ trách\n"

    for bc_name, b_info in am_bcs.items():
        msg += f"\n📦 <b>BƯU CỤC: {bc_name}</b> ({len(b_info['wards'])} xã/phường)\n"
        msg += f"   • Trạng thái: <b>{b_info['result']}</b>\n"
        if b_info['off_from'] or b_info['off_to']:
            msg += f"   • Thời gian: <b>{b_info['off_from']} ➔ {b_info['off_to']}</b>\n"
        msg += "   📍 <i>Chi tiết các xã/phường tắt:</i>\n"

        for idx, w in enumerate(b_info['wards'], 1):
            phan_loai = w.get('phan_loai', '').strip()
            # Loại bỏ các ghi chú nội bộ theo yêu cầu
            if any(term in phan_loai.lower() for term in ["chưa có trong đang off", "spe đề xuất thêm", "đang off"]):
                tag = ""
            elif phan_loai:
                tag = f" — <i>[{phan_loai}]</i>"
            else:
                tag = ""

            id_tag = f" (Mã: <code>{w['ward_id']}</code>)" if w['ward_id'] else ""
            msg += f"      {idx}. <b>{w['ward']}</b>{id_tag} - {w['district']}, {w['province']}{tag}\n"

    msg += f"\n🔗 <b>Xem chi tiết tại Sheet:</b> <a href=\"{SHEET_LINK}\">Tab Tổng Hợp KA OFF</a>"
    return msg.strip()


def send_gtalk_text_message(group_id, text, oa_token):
    payload = {
        "channelId": str(group_id),
        "clientMsgId": str(int(time.time() * 1000)),
        "content": {
            "parseMode": "HTML",
            "text": text
        },
        "oaToken": oa_token
    }
    try:
        r = requests.post(GTALK_API_URL, json=payload, timeout=15, verify=False)
        try:
            res = r.json()
        except Exception:
            res = {}

        if r.status_code == 200 and res.get("errorCode") == "success":
            return True, "Thành công"
        return False, f"HTTP {r.status_code} — {r.text}"
    except Exception as e:
        return False, str(e)


def main():
    parser = argparse.ArgumentParser(description="Gửi thông báo Tuyến SPE Tắt Giao Tệ cho AM")
    parser.add_argument("--send", "--force-send", action="store_true", help="Gửi thật qua GTalk API (Mặc định: Chỉ xem trước)")
    parser.add_argument("--am", type=str, default="", help="Chỉ gửi cho AM cụ thể (hoặc danh sách AM cách nhau bởi dấu phẩy, ví dụ: --am 'Phan Đình Duy' hoặc --am 'Duy,Vũ,Trường')")
    parser.add_argument("--bo-sung", "--update", action="store_true", help="Gắn nhãn [BỔ SUNG] vào tiêu đề tin nhắn")
    args = parser.parse_args()

    # MẶC ĐỊNH LÀ DRY RUN - TUYỆT ĐỐI KHÔNG TỰ Ý GỬI NẾU KHÔNG CÓ THAM SỐ --send
    is_dry_run = not args.send

    print("=" * 70)
    print("🚀 THỐNG KÊ & BÁO CÁO TUYẾN SPE TẮT GIAO TỆ (TAB 'Tổng Hợp KA OFF')")
    if args.bo_sung:
        print("📌 Chế độ thông báo: 🔔 [BỔ SUNG / CẬP NHẬT]")
    print(f"📌 Trạng thái gửi: {'DRY-RUN (Chỉ xem trước tin nhắn mẫu, KHÔNG gửi thật)' if is_dry_run else '🔴 KHỞI CHẠY GỬI THẬT QUA GTALK'}")
    print("=" * 70)

    print("📥 Đang tải dữ liệu từ Google Sheet (Tổng Hợp KA OFF & tab 'gtalk')...")
    th_rows, gtalk_rows = load_sheet_data()
    print(f"✅ Đã tải: {len(th_rows)} dòng 'Tổng Hợp KA OFF' | {len(gtalk_rows)} dòng tab 'gtalk'.")

    # Lấy cấu hình Token và Group ID động từ tab 'gtalk'
    sheet_token, gtalk_am_map = parse_gtalk_config(gtalk_rows)
    active_token = sheet_token if sheet_token else DEFAULT_TOKEN
    token_src = "Tab 'gtalk'" if sheet_token else "Mặc định (DEFAULT_TOKEN)"
    print(f"🔑 Token GTalk OA: {active_token[:20]}... (Nguồn: {token_src})")
    print(f"📋 Danh bạ AM cấu hình trong sheet 'gtalk': {len(gtalk_am_map)} AM.")

    # Phân tích dữ liệu tuyến tắt
    am_data = parse_off_data(th_rows, gtalk_am_map)
    print(f"📊 Tìm thấy {len(am_data)} AM có tuyến OFF do SPE đề xuất trong bảng.")

    if not am_data:
        print("⚠️ Không tìm thấy dữ liệu OFF tuyến hợp lệ!")
        return

    # Danh sách các mã ID Phường/Xã đã được gửi ở đợt 1 theo từng AM
    # (Khi bật --bo-sung, hệ thống sẽ TỰ ĐỘNG LOẠI BỎ các tuyến đã gửi này để không gửi lặp lại)
    ALREADY_SENT_BY_AM = {
        "Nguyễn Lê Nguyên Vũ": {"420311"},  # Đã gửi Đức Trọng 1 (Xã Phú Hội)
        "Lê Văn Trường": {"420504", "420506", "420502", "420503", "420510"},  # Đã gửi 5 xã Đơn Dương
        "Huỳnh Thúc Duân": {"630101", "630104", "630108", "630102", "630103", "630107", "630105", "630106"},
        "Trần Thị Nhung": {"630701"},
    }

    # NẾU LÀ CHẾ ĐỘ BỔ SUNG: Chỉ lọc giữ lại các tuyến CHƯA ĐƯỢC GỬI cho từng AM
    if args.bo_sung:
        supp_data = {}
        for am_name, am_bcs in am_data.items():
            sent_ids = ALREADY_SENT_BY_AM.get(am_name, set())
            new_bcs = {}
            for bc_name, b_info in am_bcs.items():
                missing_wards = [w for w in b_info['wards'] if str(w['ward_id']).strip() not in sent_ids]
                if missing_wards:
                    new_bcs[bc_name] = {
                        "bc_name": bc_name,
                        "result": b_info['result'],
                        "off_from": b_info['off_from'],
                        "off_to": b_info['off_to'],
                        "wards": missing_wards
                    }
            if new_bcs:
                supp_data[am_name] = new_bcs

        am_data = supp_data
        total_missing = sum(sum(len(b['wards']) for b in am.values()) for am in am_data.values())
        print(f"🔔 [CHẾ ĐỘ BỔ SUNG]: Đã loại trừ các tuyến đã gửi đợt 1.")
        print(f"👉 Còn lại đúng {total_missing} tuyến THIẾU cần gửi cho {len(am_data)} AM: {list(am_data.keys())}")

    # Lọc theo danh sách AM nếu có truyền --am
    if args.am.strip():
        filter_terms = [normalize_str(t).lower() for t in args.am.split(",") if t.strip()]
        filtered_data = {}
        for am_name, am_bcs in am_data.items():
            am_norm = normalize_str(am_name).lower()
            if any(term in am_norm for term in filter_terms):
                filtered_data[am_name] = am_bcs
        
        if not filtered_data:
            print(f"\n⚠️ Không tìm thấy AM nào khớp với từ khóa '--am {args.am}'!")
            print(f"Danh sách AM có sẵn: {list(am_data.keys())}")
            return
        
        am_data = filtered_data
        print(f"🎯 Đã lọc theo yêu cầu: Chỉ xử lý {len(am_data)} AM -> {list(am_data.keys())}")

    success_count = 0
    fail_count = 0

    print("\n📡 Đang tạo mẫu tin nhắn thông báo cho từng AM...")
    for idx, (am_name, am_bcs) in enumerate(am_data.items(), 1):
        norm_key = normalize_str(am_name).lower()
        group_id = None
        source_note = ""

        # Ưu tiên lấy Group ID từ tab 'gtalk' trên Sheet
        if norm_key in gtalk_am_map and gtalk_am_map[norm_key]["group_id"]:
            group_id = gtalk_am_map[norm_key]["group_id"]
            source_note = "Tab 'gtalk'"
        elif am_name in AM_GROUP_MAP and AM_GROUP_MAP[am_name]:
            group_id = AM_GROUP_MAP[am_name]
            source_note = "AM_GROUP_MAP (fallback)"

        if not group_id:
            print(f"⚠️ AM '{am_name}' chưa được cấu hình Group ID trong tab 'gtalk'! (Bỏ qua)")
            continue

        am_msg = format_am_text_message(am_name, am_bcs, is_supplement=args.bo_sung)

        print(f"\n[{idx:02d}/{len(am_data):02d}] 👤 AM: {am_name:<22} | Group ID: {group_id} ({source_note})")

        if is_dry_run:
            print("  👉 [DRY-RUN - XEM TRƯỚC] Nội dung tin nhắn dự kiến:")
            print("  " + "-" * 60)
            print("  " + am_msg.replace('\n', '\n  '))
            print("  " + "-" * 60)
            success_count += 1
        else:
            ok_am, err_am = send_gtalk_text_message(group_id, am_msg, active_token)
            if ok_am:
                print("  ✅ Gửi tin nhắn text thành công!")
                success_count += 1
            else:
                print(f"  ❌ Lỗi gửi text: {err_am}")
                fail_count += 1
            time.sleep(0.4)

    print("\n" + "=" * 70)
    print("📊 TỔNG KẾT:")
    print(f"   - Chế độ:     {'DRY-RUN (Chỉ xem trước, CHƯA GỬI GTALK)' if is_dry_run else 'ĐÃ GỬI THẬT QUA GTALK'}")
    print(f"   - Số AM:      {success_count}/{len(am_data)}")
    if not is_dry_run:
        print(f"   - Thất bại:   {fail_count}/{len(am_data)}")
    else:
        print("\n💡 Lưu ý: Đây là chế độ xem trước an toàn. Khi bạn duyệt nội dung và muốn gửi thật, hãy thêm cờ --send:")
        if args.am:
            print(f"   👉 python push_off_tuyen_am.py --send --am \"{args.am}\"" + (" --bo-sung" if args.bo_sung else ""))
        else:
            print("   👉 python push_off_tuyen_am.py --send" + (" --bo-sung" if args.bo_sung else ""))
    print("=" * 70)


if __name__ == "__main__":
    main()

