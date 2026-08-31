import os, sys, json
sys.path.insert(0, os.path.abspath('.'))
sys.stdout.reconfigure(encoding='utf-8')

import app

# Test API call directly with Flask test client
client = app.app.test_client()

# Add test basic auth header
import base64
auth_header = {'Authorization': 'Basic ' + base64.b64encode(b"admin:admin123").decode('utf-8')}

# Test 1: Default call
res = client.get('/api/heavy-10kg', headers=auth_header)
print("Status code (default):", res.status_code)
data = res.get_json()
if data and 'error' not in data:
    print("Success default! Keys:", list(data.keys()))
    print("Selected date:", data.get('selected_date'))
    print("Total ops vol:", data.get('total_ops_vol'))
    print("Total created vol:", data.get('total_created_vol'))
    print("BCCK Spotlight count:", data.get('bcck_spotlight', {}).get('ck_pos_count'))
    print("BCCK POs:", [p['po_name'] for p in data.get('bcck_spotlight', {}).get('ck_pos', [])])
    print("Top 3 Spikes:", [(p['po_name'], p['growth_pct'], p['spike_label']) for p in data.get('top_spikes', [])[:3]])
else:
    print("Error:", data)

# Test 2: CK Only filter
res_ck = client.get('/api/heavy-10kg?ck_only=true', headers=auth_header)
data_ck = res_ck.get_json()
print("\nStatus code (CK only):", res_ck.status_code)
print("PO count for CK only:", len(data_ck.get('po_ops_summary', [])))
print("POs:", [p['po_name'] for p in data_ck.get('po_ops_summary', [])])

# Test 3: Specific date
res_date = client.get('/api/heavy-10kg?date=2026-08-25', headers=auth_header)
data_date = res_date.get_json()
print("\nStatus code (date=2026-08-25):", res_date.status_code)
print("Selected date returned:", data_date.get('selected_date'))
print("Total ops vol on 2026-08-25:", data_date.get('total_ops_vol'))

