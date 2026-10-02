import os

path = r'c:\Users\lap4all\Desktop\auto-report\send_realtime_and_target_gtalk.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

old_block = """        grouped.setdefault(am, {}).setdefault(bc, []).append({
            "ma_nv": ma_nv,
            "name": name,
            "gan": gan,
            "tc": tc,
            "pct": pct,
            "ltc": ltc,
            "danh_gia": danh_gia
        })
"""

new_block = """        # Chống trùng lặp nhân viên trong cùng 1 bưu cục: Nếu đã có, giữ lại bản ghi có đơn giao TC cao nhất (mới nhất)
        existing_list = grouped.setdefault(am, {}).setdefault(bc, [])
        dup_idx = None
        for i, item in enumerate(existing_list):
            if (ma_nv and item["ma_nv"] == ma_nv) or (not ma_nv and item["name"] == name):
                dup_idx = i
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
"""

full_text = "".join(lines)
if old_block in full_text:
    full_text = full_text.replace(old_block, new_block, 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(full_text)
    print("SUCCESS")
else:
    print("NOT FOUND")
