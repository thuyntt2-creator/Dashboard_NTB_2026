import sys, re
with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update GID in async_sync_task
code = code.replace(
    "url_ca = 'https://docs.google.com/spreadsheets/d/1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ/export?format=csv&gid=1451699200'",
    "url_ca = 'https://docs.google.com/spreadsheets/d/1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ/export?format=csv&gid=432631208'"
)

# 2. Update process_ca_report
new_process = '''
def process_ca_report():
    df = load_df_from_db('ops_ca_data.csv')
    if df is None or df.empty:
        return {"error": "Không tìm thấy dữ liệu báo cáo Ca."}
        
    name_to_am = {}
    df_cc = load_df_from_db('co_cau_ntb.csv')
    if df_cc is not None and not df_cc.empty:
        for _, r in df_cc.iterrows():
            bc_name = str(r.get('Bưu cục', '')).strip()
            am_val = str(r.get('AM', '')).strip()
            if bc_name:
                name_clean = clean_po_name(bc_name)
                name_to_am[name_clean] = am_val

    def clean_num(x):
        try:
            if pd.isna(x) or x == '': return 0
            return int(str(x).replace('.','').replace(',',''))
        except:
            return 0

    records = []
    # Check what columns exist in the DB (they might be lowercase due to DB schema)
    # Actually load_df_from_db might restore the original columns or lowercase them.
    # The columns from GID 432631208 include ' Chi tiết.2', ' Volume.2' etc.
    # We will search for keywords in columns instead of exact names to be safe.
    cols = df.columns.tolist()
    
    col_bc1 = next((c for c in cols if 'tiết.2' in str(c).lower()), ' Chi tiết.2')
    col_vol1 = next((c for c in cols if 'volume.2' in str(c).lower()), ' Volume.2')
    col_gtc1 = next((c for c in cols if 'gtc.2' in str(c).lower()), ' GTC.2')
    
    col_bc2 = next((c for c in cols if 'tiết.3' in str(c).lower()), ' Chi tiết.3')
    col_vol2 = next((c for c in cols if 'volume.3' in str(c).lower()), ' Volume.3')
    col_gtc2 = next((c for c in cols if 'gtc.3' in str(c).lower()), ' GTC.3')
    
    col_bc3 = next((c for c in cols if 'tiết.1' in str(c).lower()), ' Chi tiết.1')
    col_vol3 = next((c for c in cols if 'volume.1' in str(c).lower()), ' Volume.1')
    col_gtc3 = next((c for c in cols if 'gtc.1' in str(c).lower()), ' GTC.1')

    for idx, row in df.iterrows():
        # Ca 1
        bc1 = str(row.get(col_bc1, '')).strip()
        vol1 = clean_num(row.get(col_vol1, 0))
        gtc1 = clean_num(row.get(col_gtc1, 0))
        if bc1 and bc1 != 'nan' and bc1 != 'None':
            am1 = name_to_am.get(clean_po_name(bc1), 'Không xác định')
            records.append({'Bưu Cục': bc1, 'AM': am1, 'Loại Hàng': 'Hàng Mới Ca 1', 'Volume': vol1, 'Sản Lượng Giao Thành Công': gtc1})

        # Ca 2
        bc2 = str(row.get(col_bc2, '')).strip()
        vol2 = clean_num(row.get(col_vol2, 0))
        gtc2 = clean_num(row.get(col_gtc2, 0))
        if bc2 and bc2 != 'nan' and bc2 != 'None':
            am2 = name_to_am.get(clean_po_name(bc2), 'Không xác định')
            records.append({'Bưu Cục': bc2, 'AM': am2, 'Loại Hàng': 'Hàng Mới Ca 2', 'Volume': vol2, 'Sản Lượng Giao Thành Công': gtc2})

        # Tồn
        bc3 = str(row.get(col_bc3, '')).strip()
        vol3 = clean_num(row.get(col_vol3, 0))
        gtc3 = clean_num(row.get(col_gtc3, 0))
        if bc3 and bc3 != 'nan' and bc3 != 'None':
            am3 = name_to_am.get(clean_po_name(bc3), 'Không xác định')
            records.append({'Bưu Cục': bc3, 'AM': am3, 'Loại Hàng': 'Hàng Tồn', 'Volume': vol3, 'Sản Lượng Giao Thành Công': gtc3})

    if not records:
        return {"error": "Không có dữ liệu trong báo cáo Ca."}

    df_parsed = pd.DataFrame(records)

    pt_bc = df_parsed.pivot_table(index=['AM', 'Bưu Cục'], columns='Loại Hàng', values=['Volume', 'Sản Lượng Giao Thành Công'], aggfunc='sum', fill_value=0)
    pt_bc.columns = [f"{c[1]}_{c[0]}" for c in pt_bc.columns]
    pt_bc = pt_bc.reset_index()

    pt_am = df_parsed.pivot_table(index=['AM'], columns='Loại Hàng', values=['Volume', 'Sản Lượng Giao Thành Công'], aggfunc='sum', fill_value=0)
    pt_am.columns = [f"{c[1]}_{c[0]}" for c in pt_am.columns]
    pt_am = pt_am.reset_index()

    return {
        "by_bc": clean_nan(pt_bc.to_dict(orient='records')),
        "by_am": clean_nan(pt_am.to_dict(orient='records'))
    }
'''

# Find boundaries of old process_ca_report
start_idx = code.find('def process_ca_report():')
end_idx = code.find('def process_fd_report', start_idx)

if start_idx != -1 and end_idx != -1:
    code = code[:start_idx] + new_process + '\n' + code[end_idx:]

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print('Updated process_ca_report and GID')
