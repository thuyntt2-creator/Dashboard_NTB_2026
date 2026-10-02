import sys
import os
import shutil
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from send_report_nvptt_realtime import read_baocao_realtime, generate_report_image

data = read_baocao_realtime()
print(f"Total AMs: {len(data)}")

pr_found = False
other_hubs = []
for am in data:
    for bc_name, staff_list in am['bcs']:
        if 'Phan Rang' in bc_name and not pr_found:
            pr_found = True
            gan_total = sum(s['gan'] for s in staff_list)
            tc_total = sum(s['tc'] for s in staff_list)
            pct = (tc_total / gan_total * 100) if gan_total else 0
            print(f"=== {bc_name} ({len(staff_list)} NVPTT) - AM: {am['am']} ===")
            print(f"Gán: {gan_total}, GTC: {tc_total}, %: {pct:.2f}%")
            
            # Print each staff
            for i, s in enumerate(staff_list):
                print(f"{i+1}. {s['ma_nv']} - {s['name']}: {s['gan']} gán, {s['tc']} tc ({s['pct']:.2f}%)")

            out_img = 'test_phan_rang_today.png'
            generate_report_image(am['am'], bc_name, staff_list, '02/10/2026', '11:35 02/10/2026', out_img)
            shutil.copy(out_img, r'C:\Users\lap4all\.gemini\antigravity-ide\brain\b7b1fe47-a14b-414b-b163-1903dda65dc6\test_phan_rang_today.png')
            print("Generated & copied Phan Rang test image successfully!")
            
        elif len(other_hubs) < 1 and not ('Phan Rang' in bc_name):
            other_hubs.append((am['am'], bc_name, staff_list))

for am_name, bc_name, staff_list in other_hubs:
    out_img = f"test_{bc_name.replace(' ', '_').replace('(', '').replace(')', '')}.png"
    generate_report_image(am_name, bc_name, staff_list, '02/10/2026', '11:35 02/10/2026', out_img)
    shutil.copy(out_img, rf"C:\Users\lap4all\.gemini\antigravity-ide\brain\b7b1fe47-a14b-414b-b163-1903dda65dc6\{out_img}")
    print(f"Generated & copied {bc_name} test image successfully!")
