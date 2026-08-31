import json
import sys
import os
sys.path.append(os.getcwd())
from app import process_operational_report, process_fd_report

ops = process_operational_report()
print("Operational Report keys:", ops.keys())
print("overall_fd:", ops.get('overall_fd'))
print("top_10_gtc keys:", ops.get('top_10_gtc')[0] if ops.get('top_10_gtc') else 'None')
print("worst_10_gtc keys:", ops.get('worst_10_gtc')[0] if ops.get('worst_10_gtc') else 'None')

fd = process_fd_report()
print("FD Report keys:", fd.keys())
print("total_backlog:", fd.get('total_backlog'))
print("po_summary length:", len(fd.get('po_summary')) if fd.get('po_summary') else 'None')
if fd.get('po_summary'):
    print("po_summary sample:", fd.get('po_summary')[0])
