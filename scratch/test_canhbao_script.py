import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import report_BC_canh_bao_gtalk as rpt

items, update_time, n1_compare = rpt.load_data()
print('=== KẾT QUẢ TỪ REPORT_BC_CANH_BAO_GTALK.PY ===')
print('Cập nhật lúc:', update_time)
print('Số lượng bưu cục cảnh báo:', len(items))
for it in items:
    print(f"{it['bc_name']:<28} | 7d: {it['gtc_7d']:<6} | Vol Nay: {it['vol_today']:<5} | Target: {it['req_gtc']:<5} | Achievable: {it['is_achievable']}")
