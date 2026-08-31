import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
import os
sys.path.insert(0, '.')
os.environ['VERCEL'] = '1'

import app
print("Testing process_productivity_realtime in Vercel mode...")
res = app.process_productivity_realtime()
if isinstance(res, dict):
    if 'error' in res:
        print(f"Error: {res['error']}")
    elif 'records' in res:
        print(f"Success! Total records: {len(res['records'])}")
        print("First 3 records:")
        for r in res['records'][:3]:
            print(r)
else:
    print(f"Returned: {res}")
