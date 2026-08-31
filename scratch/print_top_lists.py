import sys
import os
sys.path.append(os.getcwd())
from app import process_operational_report, process_fd_report

ops = process_operational_report()
fd = process_fd_report()

print("=== TOP 10 BEST GTC ===")
for i, r in enumerate(ops.get('top_10_gtc', [])[:10], 1):
    print(f"{i}. {r['Chi tiết']} | Sản lượng: {r['Volume']} | %GTC: {r['% GTC']:.2f}%")

print("\n=== TOP 10 WORST GTC ===")
for i, r in enumerate(ops.get('worst_10_gtc', [])[:10], 1):
    print(f"{i}. {r['Chi tiết']} | Sản lượng: {r['Volume']} | %GTC: {r['% GTC']:.2f}%")

print("\n=== TOP 10 WORST FD ===")
worst_fd = sorted(fd.get('po', []), key=lambda x: x['fd_n'], reverse=True)[:10]
for i, r in enumerate(worst_fd, 1):
    print(f"{i}. {r['post_office']} | %FD: {r['fd_n']:.2f}% | Vol Giao: {r['vol_giao']}")
