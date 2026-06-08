import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app

print("Testing app cache loading...")
app.update_all_caches()

if app.DF_TAO_DON_CACHE is None:
    print("Error: DF_TAO_DON_CACHE is None!")
    sys.exit(1)
else:
    print(f"Success: Loaded DF_TAO_DON_CACHE with {len(app.DF_TAO_DON_CACHE)} rows.")

print("Testing Flask test client...")
with app.app.test_client() as client:
    # Set authorization header since requires_auth is active
    import base64
    auth_header = {
        'Authorization': 'Basic ' + base64.b64encode(b"admin:admin123").decode('utf-8')
    }
    
    print("Fetching /api/volume-creation without parameters...")
    res = client.get('/api/volume-creation', headers=auth_header)
    print(f"Status Code: {res.status_code}")
    if res.status_code != 200:
        print(f"Error output: {res.data.decode('utf-8')}")
        sys.exit(1)
        
    data = res.get_json()
    print("Keys in response:", list(data.keys()))
    
    expected_keys = ["kpi", "table", "total", "filters", "matrix", "charts"]
    for k in expected_keys:
        if k in data:
            print(f"  Key '{k}': Present")
        else:
            print(f"  Error: Key '{k}' is missing!")
            sys.exit(1)
            
    print("Sample filters:", data["filters"].keys())
    print("Sample KPI card data:", data["kpi"])
    print("Matrix rows count:", len(data["matrix"]["rows"]))
    print("Treemap items count:", len(data["charts"]["treemap"]))
    print("Line chart series count:", len(data["charts"]["line"]["series"]))
    print("Grouped bar chart series count:", len(data["charts"]["bar"]["series"]))

print("All API tests passed successfully!")
