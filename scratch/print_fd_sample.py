import sys
import os
sys.path.append(os.getcwd())
from app import process_fd_report

fd = process_fd_report()
print("FD Report root keys:", fd.keys())
if 'kpi' in fd:
    print("KPI details:", fd['kpi'])
if 'po' in fd and len(fd['po']) > 0:
    print("PO list length:", len(fd['po']))
    print("PO sample:", fd['po'][0])
if 'province' in fd and len(fd['province']) > 0:
    print("Province list length:", len(fd['province']))
    print("Province sample:", fd['province'][0])
