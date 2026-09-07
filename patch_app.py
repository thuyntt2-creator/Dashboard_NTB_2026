import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Add CA_REPORT_CACHE
if 'CA_REPORT_CACHE = None' not in code:
    code = code.replace('FD_CACHE = None', 'FD_CACHE = None\nCA_REPORT_CACHE = None')

# 2. Add process_ca_report()
process_ca_code = '''
def process_ca_report():
    df = load_df_from_db('ops_ca_data.csv')
    if df is None or df.empty:
        return {"error": "Không tìm thấy dữ liệu báo cáo Ca."}
    
    col_map = {str(c).strip().lower(): c for c in df.columns}
    col_loai_hang = col_map.get('loại hàng', 'Loại Hàng')
    col_am = col_map.get('am', 'AM')
    col_bc = col_map.get('chi tiết', 'Chi tiết')
    if 'bưu cục' in col_map:
        col_bc = col_map['bưu cục']
        
    col_vol = col_map.get('volume', 'Volume')
    col_gtc = col_map.get('sản lượng giao thành công', 'Sản Lượng Giao Thành Công')
    
    if col_loai_hang not in df.columns or col_vol not in df.columns:
        return {"error": "Dữ liệu CA thiếu các cột cần thiết."}
        
    def clean_num(x):
        try:
            if pd.isna(x) or x == '': return 0
            return int(str(x).replace('.','').replace(',',''))
        except:
            return 0
            
    df[col_vol] = df[col_vol].apply(clean_num)
    df[col_gtc] = df[col_gtc].apply(clean_num)
    
    df = df[df[col_loai_hang].isin(['Hàng Mới Ca 1', 'Hàng Mới Ca 2', 'Hàng Tồn'])]
    
    if df.empty:
        return {"error": "Không có dữ liệu Hàng Mới Ca 1, Ca 2 hoặc Hàng Tồn."}
        
    pt_bc = df.pivot_table(index=[col_am, col_bc], columns=col_loai_hang, values=[col_vol, col_gtc], aggfunc='sum', fill_value=0)
    pt_bc.columns = [f"{c[1]}_{c[0]}" for c in pt_bc.columns]
    pt_bc = pt_bc.reset_index().rename(columns={col_am: "AM", col_bc: "Bưu Cục"})
    
    pt_am = df.pivot_table(index=[col_am], columns=col_loai_hang, values=[col_vol, col_gtc], aggfunc='sum', fill_value=0)
    pt_am.columns = [f"{c[1]}_{c[0]}" for c in pt_am.columns]
    pt_am = pt_am.reset_index().rename(columns={col_am: "AM"})
    
    return {
        "by_bc": clean_nan(pt_bc.to_dict(orient='records')),
        "by_am": clean_nan(pt_am.to_dict(orient='records'))
    }
'''
if 'def process_ca_report' not in code:
    code = code.replace('def process_fd_report():', process_ca_code + '\ndef process_fd_report():')

# 3. Add API route
api_route = '''
@app.route('/api/ca-report')
def api_ca_report():
    global CA_REPORT_CACHE
    if CA_REPORT_CACHE is None:
        with CACHE_LOCK:
            if CA_REPORT_CACHE is None:
                CA_REPORT_CACHE = process_ca_report()
    return jsonify(clean_nan(CA_REPORT_CACHE))
'''
if 'def api_ca_report' not in code:
    code = code.replace('@app.route(\'/api/fd\')', api_route + '\n@app.route(\'/api/fd\')')

# 4. update_all_caches -> add CA_REPORT_CACHE
if 'global OPERATIONAL_CACHE, OPR_CACHE, BACKLOG_CACHE_RAW, UNSTABLE_PO_CACHE, OFF_SPE_CACHE' in code:
    code = code.replace(
        'global OPERATIONAL_CACHE, OPR_CACHE, BACKLOG_CACHE_RAW, UNSTABLE_PO_CACHE, OFF_SPE_CACHE',
        'global OPERATIONAL_CACHE, OPR_CACHE, BACKLOG_CACHE_RAW, UNSTABLE_PO_CACHE, OFF_SPE_CACHE, CA_REPORT_CACHE'
    )
if 'OFF_SPE_CACHE = None' in code:
    # use regex to replace first occurrence of OFF_SPE_CACHE = None after def update_all_caches
    parts = code.split('def update_all_caches():')
    if len(parts) > 1:
        if 'CA_REPORT_CACHE = None' not in parts[1][:1000]:
            parts[1] = parts[1].replace('OFF_SPE_CACHE = None', 'OFF_SPE_CACHE = None\n    CA_REPORT_CACHE = None', 1)
            code = 'def update_all_caches():'.join(parts)

# 5. Add download logic inside async_sync_task
download_logic = '''
                # Download CA Report Data
                SYNC_STATUS["progress"] = "Đang tải báo cáo Sản lượng Ca..."
                try:
                    import urllib.request, io
                    url_ca = 'https://docs.google.com/spreadsheets/d/1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ/export?format=csv&gid=1451699200'
                    req_ca = urllib.request.Request(url_ca, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req_ca, timeout=30) as resp:
                        content_ca = resp.read()
                    for enc in ['utf-8-sig', 'utf-8', 'latin-1', 'cp1252']:
                        try:
                            df_ca = pd.read_csv(io.BytesIO(content_ca), encoding=enc)
                            save_df_to_db(df_ca, 'ops_ca_data.csv')
                            print("Successfully downloaded ops_ca_data.csv")
                            break
                        except Exception:
                            continue
                except Exception as e:
                    print(f"Error downloading CA data: {e}")
'''

if 'ops_ca_data.csv' not in code:
    code = code.replace(
        'direct_success, direct_msg = sync_sheets_directly_as_csv(url)',
        download_logic + '\n                direct_success, direct_msg = sync_sheets_directly_as_csv(url)'
    )

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)
print('Patched app.py')
