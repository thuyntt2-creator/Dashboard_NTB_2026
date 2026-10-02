import sys
import os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import gspread
from google.oauth2.credentials import Credentials

creds = Credentials.from_authorized_user_file('authorized_user.json')
gc = gspread.authorize(creds)
sh = gc.open_by_key('1-p9VUXndK_7BoiT-a81UfTCbUi953XNmVBoXaTGis_c')

from send_report_nvptt_realtime import parse_num, parse_pct

def read_data_tab_realtime(sh):
    ws_data = sh.worksheet('Data')
    all_vals = ws_data.get_all_values()
    if not all_vals or len(all_vals) < 2:
        return None
    
    headers = all_vals[0]
    i_bc = 16
    i_am = 17
    i_did = 1
    i_name = 2
    i_gan = 6
    i_tc = 11
    i_pct = 13
    i_ltc = 8
    
    grouped = {}
    for row in all_vals[1:]:
        if len(row) <= max(i_bc, i_am):
            continue
        bc = row[i_bc].strip()
        am = row[i_am].strip()
        ma_nv = row[i_did].strip() if i_did < len(row) else ""
        name = row[i_name].strip() if i_name < len(row) else ""
        if not bc or not am or not name:
            continue
        
        gan = parse_num(row[i_gan]) if i_gan < len(row) else 0
        tc = parse_num(row[i_tc]) if i_tc < len(row) else 0
        pct = parse_pct(row[i_pct]) if i_pct < len(row) else 0.0
        ltc = parse_num(row[i_ltc]) if i_ltc < len(row) else 0
        
        if gan == 0 and ltc == 0:
            continue
            
        danh_gia = "Thấp" if pct < 80.0 else ("Đạt" if pct < 85.0 else "OK")
        
        existing_list = grouped.setdefault(am, {}).setdefault(bc, [])
        dup_idx = None
        for idx, item in enumerate(existing_list):
            if (ma_nv and item["ma_nv"] == ma_nv) or (not ma_nv and item["name"] == name):
                dup_idx = idx
                break
                
        staff_data = {
            "ma_nv": ma_nv,
            "name": name,
            "gan": gan,
            "tc": tc,
            "pct": pct,
            "ltc": ltc,
            "danh_gia": danh_gia
        }
        if dup_idx is not None:
            if tc > existing_list[dup_idx]["tc"] or (tc == existing_list[dup_idx]["tc"] and gan >= existing_list[dup_idx]["gan"]):
                existing_list[dup_idx] = staff_data
        else:
            existing_list.append(staff_data)
            
    result = []
    for am_name, bc_map in sorted(grouped.items()):
        bcs = []
        for bc_name, staff_list in sorted(bc_map.items()):
            if staff_list:
                staff_list.sort(key=lambda x: x["pct"])
                bcs.append((bc_name, staff_list))
        if bcs:
            result.append({"am": am_name, "bcs": bcs})
            
    return result

data = read_data_tab_realtime(sh)
print(f"Tổng số AM có bưu cục: {len(data)} AM")
total_bcs = sum(len(am['bcs']) for am in data)
total_staff = sum(len(s) for am in data for _, s in am['bcs'])
total_orders = sum(s['gan'] for am in data for _, bcs in am['bcs'] for s in bcs)
total_tc = sum(s['tc'] for am in data for _, bcs in am['bcs'] for s in bcs)
print(f"Tổng số Bưu cục: {total_bcs} bưu cục (= {total_bcs} ảnh báo cáo)")
print(f"Tổng số NVPTT: {total_staff} nhân viên")
print(f"Tổng đơn gán: {total_orders:,} đơn, Giao TC: {total_tc:,} đơn ({(total_tc/total_orders*100):.2f}%)")

print("\nChi tiết từng AM:")
for am in data:
    bc_names = [name for name, _ in am['bcs']]
    staff_count = sum(len(s) for _, s in am['bcs'])
    print(f"- AM {am['am']}: {len(am['bcs'])} bưu cục, {staff_count} nhân viên")
