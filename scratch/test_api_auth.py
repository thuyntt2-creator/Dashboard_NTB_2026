import sys
import os
import json
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.abspath('.'))

from app import app

with app.test_client() as client:
    with client.session_transaction() as sess:
        sess['username'] = 'admin'
        sess['role'] = 'admin'
        sess['permissions'] = ['tab-fd', 'tab-dashboard']
    
    r = client.get('/api/fd')
    print("Status code /api/fd:", r.status_code)
    json_data = r.get_json()
    print("Title:", json_data.get('title'))
    print("Period:", json_data.get('date'))
    print("Summary:", json.dumps(json_data.get('summary'), ensure_ascii=False, indent=2))
    print("Channels:", json.dumps(json_data.get('channels'), ensure_ascii=False, indent=2))
    print("Top 10 count:", len(json_data.get('top10', [])))
    print("AM Rankings count:", len(json_data.get('am_rankings', [])))
    print("All Pos count:", len(json_data.get('all_pos', [])))
    print("Sample All PO row 1:", json_data.get('all_pos', [])[0])
    
    # Test filter by AM
    r_am = client.get('/api/fd?am=AM%20%C4%90%E1%BA%A1i')
    print("\nStatus code /api/fd?am=AM Đại:", r_am.status_code)
    json_am = r_am.get_json()
    print("Filtered POs count for AM Đại:", len(json_am.get('all_pos', [])))
    for p in json_am.get('all_pos', []):
        print(f"  - {p['post_office']} (AM: {p['am']}, FD: {p['fd_rate']}%)")
