import sys
import os
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.abspath('.'))

from app import app, process_fd_report

print("Testing process_fd_report directly...")
res = process_fd_report()
print("Success! Keys in res:", list(res.keys()))
print("Summary:", res.get('summary'))
print("Channels count:", len(res.get('channels', [])))
print("Top 10 count:", len(res.get('top10', [])))
print("AM rankings count:", len(res.get('am_rankings', [])))
print("All POs count:", len(res.get('all_pos', [])))

print("\nTesting Flask test client on /api/fd...")
with app.test_client() as client:
    # login as admin session
    with client.session_transaction() as sess:
        sess['user'] = 'admin'
        sess['role'] = 'admin'
    
    r = client.get('/api/fd')
    print("Status code /api/fd:", r.status_code)
    json_data = r.get_json()
    print("Response keys:", list(json_data.keys()))
    print("Response title:", json_data.get('title'))
    print("Response total orders:", json_data.get('summary', {}).get('total_orders'))
    
    print("\nTesting /api/batch-data...")
    r_batch = client.get('/api/batch-data')
    print("Status code /api/batch-data:", r_batch.status_code)
    batch_json = r_batch.get_json()
    print("batch-data contains 'fd':", 'fd' in batch_json)
    if 'fd' in batch_json and 'error' not in batch_json['fd']:
        print("batch fd summary total_orders:", batch_json['fd'].get('summary', {}).get('total_orders'))

    print("\nTesting GET / (rendering index.html)...")
    r_home = client.get('/')
    print("Status code /:", r_home.status_code)
    html_text = r_home.get_data(as_text=True)
    print("HTML contains 'BÁO CÁO %FD HUB (N-1) – VÙNG NTB':", 'BÁO CÁO %FD HUB (N-1) – VÙNG NTB' in html_text)
    print("HTML contains 'table-fd-top10':", 'table-fd-top10' in html_text)
    print("HTML contains 'table-fd-am':", 'table-fd-am' in html_text)
    print("HTML contains 'table-fd-all':", 'table-fd-all' in html_text)
    print("HTML contains 'fd-channels-grid':", 'fd-channels-grid' in html_text)
