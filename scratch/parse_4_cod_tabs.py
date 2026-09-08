import json
import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')
sheet_id = '1j6Xm7JRemUGRSfbL-wc8DMwt7qfR7j79w9q79_snVnU'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

creds = Credentials.from_authorized_user_file('authorized_user.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

# 1. TAB 1: Xu hướng 2 tuần
res1 = service.spreadsheets().values().get(spreadsheetId=sheet_id, range='1. Xu hướng 2 Tuần').execute()
rows1 = res1.get('values', [])
summary_text = rows1[1][0] if len(rows1) > 1 and len(rows1[1]) > 0 else ""

prev_period = "Tuần N-1"
curr_period = "Tuần N"
if len(rows1) >= 4 and len(rows1[3]) >= 3:
    prev_period = rows1[3][1].strip()
    curr_period = rows1[3][2].strip()

metrics_list = []
if len(rows1) >= 8:
    for r in rows1[4:8]:
        if len(r) >= 6:
            metrics_list.append({
                "chi_so": r[0],
                "prev": r[1],
                "curr": r[2],
                "diff_val": r[3],
                "diff_pct": r[4],
                "eval": r[5]
            })

# 2. TAB 2: AM So Sánh 2 Tuần
res2 = service.spreadsheets().values().get(spreadsheetId=sheet_id, range='2. AM So Sánh 2 Tuần').execute()
rows2 = res2.get('values', [])
am_list = []
if len(rows2) > 2:
    for r in rows2[2:]:
        if len(r) >= 7 and r[1].strip():
            am_list.append({
                "stt": r[0],
                "am": r[1],
                "prev_tm": r[2] if r[2] else "–",
                "curr_tm": r[3],
                "diff": r[4] if r[4] else "–",
                "trend": r[5] if r[5] else "–",
                "level": r[6]
            })

# 3. TAB 3: Chi tiết BC 2 Tuần
res3 = service.spreadsheets().values().get(spreadsheetId=sheet_id, range='3. Chi tiết BC 2 Tuần').execute()
rows3 = res3.get('values', [])
bc_list = []
if len(rows3) > 2:
    for r in rows3[2:]:
        if len(r) >= 8 and r[2].strip():
            bc_list.append({
                "stt": r[0],
                "am": r[1],
                "bc": r[2],
                "prev_tm": r[3] if r[3] else "–",
                "curr_tm": r[4],
                "diff": r[5] if r[5] else "–",
                "cash_m": r[6],
                "level": r[7]
            })

# 4. TAB 4: Hướng xử lý AM
res4 = service.spreadsheets().values().get(spreadsheetId=sheet_id, range='4. Hướng xử lý AM').execute()
rows4 = res4.get('values', [])
action_list = []
if len(rows4) > 2:
    for r in rows4[2:]:
        if len(r) >= 6 and r[0].strip():
            action_list.append({
                "am": r[0],
                "prev_tm": r[1] if r[1] else "–",
                "curr_tm": r[2],
                "diff": r[3] if r[3] else "–",
                "action": r[4],
                "deadline": r[5]
            })

# If action_list is empty from Google Sheets, generate automatically based on AM comparison
if not action_list:
    gsheet_update_rows = [
        ["HƯỚNG XỬ LÝ AM CÓ TỶ LỆ TIỀN MẶT CAO TRONG TUẦN N (≥ 50%)", "", "", "", "", ""],
        ["AM", prev_period + " (% TM)", curr_period + " (% TM)", "Biến động", "Hành động yêu cầu", "Deadline"]
    ]
    for a in am_list:
        try:
            curr_val = float(a['curr_tm'].replace('%', '').strip())
        except Exception:
            continue
        
        diff_str = a['diff']
        is_rising = diff_str.startswith('+')
        
        if curr_val >= 70.0:
            if is_rising:
                act = f"🔴 Mức rất cao ({a['curr_tm']} TM & tăng {diff_str}).\n• Lập biên bản làm việc 1-1 với AM ngay trong ngày.\n• Kiểm tra danh sách Shop mới phát sinh tiền mặt lớn.\n• Bắt buộc bưu tá in mã QR cá nhân trên áo và thùng xe."
                dl = "⚡ Gấp trong 24h"
            else:
                act = f"🔴 Mức rất cao ({a['curr_tm']} TM). Dù có giảm nhưng vẫn vượt ngưỡng 70%.\n• Tiếp tục duy trì đôn đốc cài đặt QR/POS tại các bưu cục trực thuộc.\n• Giám sát đối chiếu nộp tiền mặt cuối ca hàng ngày."
                dl = "Trong 3 ngày"
            action_list.append({
                "am": a['am'],
                "prev_tm": a['prev_tm'],
                "curr_tm": a['curr_tm'],
                "diff": a['diff'],
                "action": act,
                "deadline": dl
            })
            gsheet_update_rows.append([a['am'], a['prev_tm'], a['curr_tm'], a['diff'], act, dl])
        elif curr_val >= 50.0:
            if is_rising:
                act = f"⚠️ CẢNH BÁO TĂNG TIỀN MẶT ({a['curr_tm']} TM, tăng {diff_str}).\n• Yêu cầu AM giải trình danh sách Shop/tuyến phát sinh tiền mặt.\n• Tối ưu chuyển đổi QR cho các Shop lớn."
                dl = "⚡ Gấp trong 24h"
            else:
                act = f"🟡 Đang ở ngưỡng cảnh báo (50% - 70%).\n• Tiếp tục theo dõi và yêu cầu tối ưu tỷ lệ chuyển khoản QR cho các Shop lớn."
                dl = "Cuối tuần N"
            action_list.append({
                "am": a['am'],
                "prev_tm": a['prev_tm'],
                "curr_tm": a['curr_tm'],
                "diff": a['diff'],
                "action": act,
                "deadline": dl
            })
            gsheet_update_rows.append([a['am'], a['prev_tm'], a['curr_tm'], a['diff'], act, dl])
        elif is_rising:
            try:
                diff_val = float(diff_str.replace('+', '').replace('%', '').strip())
                if diff_val >= 8.0:
                    act = f"⚠️ Tăng đột biến tỷ lệ tiền mặt (+{diff_val}%p so với tuần trước).\n• Rà soát các tuyến giao và bưu cục trực thuộc có phát sinh đơn tiền mặt bất thường."
                    dl = "Trong 48h"
                    action_list.append({
                        "am": a['am'],
                        "prev_tm": a['prev_tm'],
                        "curr_tm": a['curr_tm'],
                        "diff": a['diff'],
                        "action": act,
                        "deadline": dl
                    })
                    gsheet_update_rows.append([a['am'], a['prev_tm'], a['curr_tm'], a['diff'], act, dl])
            except Exception:
                pass

    # Push to Google Sheet Tab 4
    try:
        service.spreadsheets().values().update(
            spreadsheetId=sheet_id,
            range='4. Hướng xử lý AM!A1',
            valueInputOption='USER_ENTERED',
            body={'values': gsheet_update_rows}
        ).execute()
        print("Updated Google Sheet Tab 4: 4. Hướng xử lý AM successfully!")
    except Exception as e:
        print(f"Note: Could not update Tab 4 on Google Sheets: {e}")

d['cod_report'] = {
    "summary_text": summary_text,
    "prev_period": prev_period,
    "curr_period": curr_period,
    "metrics": metrics_list,
    "am_comparison": am_list,
    "bc_details": bc_list,
    "actions": action_list
}

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

with open('data.js', 'w', encoding='utf-8') as f:
    f.write('window.DASHBOARD_DATA = ' + json.dumps(d, ensure_ascii=False, indent=2) + ';\n')

print("SUCCESSFULLY PARSED ALL 4 COD TABS INTO data.json & data.js!")
print(f"Metrics: {len(metrics_list)} | AMs: {len(am_list)} | BCs: {len(bc_list)} | Actions: {len(action_list)}")
