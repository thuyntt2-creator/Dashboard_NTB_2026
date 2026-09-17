# -*- coding: utf-8 -*-

with open('scratch/safe_report.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's see where we can trim 100 characters easily:
# replace '%GTC TTS:' -> '%GTC TTS:'
text = text.replace('• Bưu cục bất ổn: 12/85 BC (14.1%) - Nhóm 1: 11 BC | Nhóm 2: 01 BC', '• BC bất ổn: 12/85 BC (14.1%) - Nhóm 1: 11 BC | Nhóm 2: 01 BC')
text = text.replace('NHÓM 1: GTC 7 NGÀY < 45% (11 BC)', '🔴 NHÓM 1: GTC 7 NGÀY < 45% (11 BC)')
text = text.replace('NHÓM 2: GTC < 70% LỊCH SỬ TỐT NHẤT (1 BC)', '🟡 NHÓM 2: GTC < 70% LỊCH SỬ TỐT NHẤT (1 BC)')

print("Final tightened len:", len(text))
with open('scratch/safe_report_tight.txt', 'w', encoding='utf-8') as f:
    f.write(text)
