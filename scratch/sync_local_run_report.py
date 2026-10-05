# -*- coding: utf-8 -*-
content = """#!/bin/bash
export PATH="/usr/local/bin:/usr/bin:/bin:$PATH"
cd /root/auto-report
echo "=== CHAY BAO CAO LUC: $(date) ===" >> /root/auto-report/cron.log

# 1. Tải số liệu chuẩn từ Looker Studio và cập nhật tab 'lấy hàng' & 'giao hàng'
python3 autonangsuat.py >> /root/auto-report/cron.log 2>&1

# 2. Gửi báo cáo GTalk theo mốc giờ
CURRENT_HOUR=$(date +%H)
if [ "$CURRENT_HOUR" -eq 14 ]; then
    echo "⏰ [14h00]: Chạy Báo cáo Kết hợp (Target GTC + Năng suất NVPTT)..." >> /root/auto-report/cron.log
    python3 send_realtime_and_target_gtalk.py >> /root/auto-report/cron.log 2>&1
else
    echo "⏰ [${CURRENT_HOUR}h00]: Chạy Báo cáo NĂNG SUẤT NVPTT (Không kèm Target)..." >> /root/auto-report/cron.log
    python3 send_realtime_and_target_gtalk.py --only-nangsuat >> /root/auto-report/cron.log 2>&1
fi
"""

with open(r"C:\Users\lap4all\Documents\Auto report\run_report.sh", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Saved local run_report.sh")
