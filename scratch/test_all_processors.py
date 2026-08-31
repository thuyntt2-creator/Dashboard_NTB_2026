import sys, os
import pandas as pd

sys.path.insert(0, os.path.abspath('.'))
sys.stdout.reconfigure(encoding='utf-8')

import app

# Test all processors with empty DataFrames or loaded DataFrames
try:
    print("1. Testing process_fd_report...")
    app.process_fd_report()
    print("   -> OK")
except Exception as e:
    print(f"   -> ERROR in process_fd_report: {e}")

try:
    print("2. Testing process_opr_report...")
    app.process_opr_report()
    print("   -> OK")
except Exception as e:
    print(f"   -> ERROR in process_opr_report: {e}")

try:
    print("3. Testing process_backlog_reports...")
    app.process_backlog_reports()
    print("   -> OK")
except Exception as e:
    print(f"   -> ERROR in process_backlog_reports: {e}")

try:
    print("4. Testing process_unstable_pos...")
    app.process_unstable_pos()
    print("   -> OK")
except Exception as e:
    print(f"   -> ERROR in process_unstable_pos: {e}")

try:
    print("5. Testing process_off_spe...")
    app.process_off_spe()
    print("   -> OK")
except Exception as e:
    print(f"   -> ERROR in process_off_spe: {e}")

try:
    print("6. Testing update_all_caches...")
    app.update_all_caches()
    print("   -> OK")
except Exception as e:
    print(f"   -> ERROR in update_all_caches: {e}")
