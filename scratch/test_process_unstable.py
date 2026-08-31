import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# Mock resolve_path and safe_read_csv as in app.py
import pandas as pd
import numpy as np
import os
import re

def resolve_path(filename, write=False):
    return filename

def safe_read_csv(path, **kwargs):
    try:
        return pd.read_csv(path, encoding='utf-8', **kwargs)
    except Exception as e:
        print(f"Error reading CSV {path}: {e}")
        return None

def clean_po_name(name):
    if pd.isna(name):
        return ""
    name = str(name).lower()
    name = re.sub(r'bưu cục\s*', '', name)
    name = re.sub(r'bc\s*', '', name)
    name = name.strip()
    return name

def parse_unstable_pct(val):
    if pd.isna(val):
        return 0.0
    val_str = str(val).strip()
    if val_str.endswith('%'):
        try:
            return float(val_str.rstrip('%'))
        except:
            return 0.0
    try:
        return float(val_str) * 100.0
    except:
        return 0.0

def clean_nan(obj):
    if isinstance(obj, dict):
        return {k: clean_nan(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_nan(x) for x in obj]
    elif isinstance(obj, float) and (np.isnan(obj) or np.isinf(obj)):
        return None
    return obj

def map_po_to_am_prov(po_id, po_name, id_to_am, id_to_prov, name_to_am, name_to_prov, default_am="Không xác định", default_prov="Không xác định"):
    def clean_val(val, default):
        if pd.isna(val) or not str(val).strip() or str(val).lower() == 'nan':
            return default
        return str(val).strip()
    
    default_am = clean_val(default_am, "Không xác định")
    default_prov = clean_val(default_prov, "Không xác định")

    try:
        pid = int(float(po_id))
        if pid in id_to_am:
            return clean_val(id_to_am[pid], default_am), clean_val(id_to_prov[pid], default_prov)
    except:
        pass

    name_clean = clean_po_name(po_name)
    if name_clean in name_to_am:
        return clean_val(name_to_am[name_clean], default_am), clean_val(name_to_prov[name_clean], default_prov)

    for k in name_to_am:
        if k in name_clean or name_clean in k:
            return clean_val(name_to_am[k], default_am), clean_val(name_to_prov[k], default_prov)

    return default_am, default_prov

def process_unstable_po():
    file_path = 'buu_cuc_bat_on.csv'
    if not os.path.exists(file_path):
        return {"error": "Không tìm thấy dữ liệu bưu cục bất ổn."}
    
    df_raw = safe_read_csv(file_path, header=None)
    
    update_time = None
    total_warning = None
    
    # Search metadata in the first 15 rows
    for r_idx in range(min(15, len(df_raw))):
        for c_idx in range(len(df_raw.columns)):
            cell_val = str(df_raw.iloc[r_idx, c_idx])
            if "Thời gian cập nhật" in cell_val:
                for offset in range(1, 4):
                    if c_idx + offset < len(df_raw.columns):
                        val = df_raw.iloc[r_idx, c_idx + offset]
                        if pd.notna(val) and str(val).strip() != "":
                            update_time = str(val).strip()
                            break
            elif "bưu cục cảnh báo" in cell_val or "bưu cục bất ổn" in cell_val or "lượng bưu cục" in cell_val:
                for offset in range(1, 4):
                    if c_idx + offset < len(df_raw.columns):
                        val = df_raw.iloc[r_idx, c_idx + offset]
                        if pd.notna(val) and str(val).strip() != "":
                            try:
                                total_warning = int(float(val))
                            except:
                                total_warning = str(val).strip()
                            break
    
    # Find the table headers row
    header_row_idx = None
    for r_idx in range(len(df_raw)):
        row_vals = [str(x).lower().strip() for x in df_raw.iloc[r_idx].values]
        if any("tổng số lượng" in x or "thời gian cập nhật" in x for x in row_vals):
            continue
        if any(x == "bưu cục" or x == "chi tiết" or x == "tên bc" or "tên bưu cục" in x or "kho_giao_id" in x or "kho_giao_name" in x or "tinh_giao" in x for x in row_vals):
            header_row_idx = r_idx
            break
            
    if header_row_idx is None:
        header_row_idx = 4 if len(df_raw) > 4 else 0
        
    df_table = safe_read_csv(file_path, skiprows=header_row_idx)
    df_table.columns = [str(c).strip() for c in df_table.columns]
    
    id_col = next((c for c in df_table.columns if "id" in c.lower() or "kho_giao_id" in c.lower()), df_table.columns[0])
    name_col = next((c for c in df_table.columns if "name" in c.lower() or "bưu cục" in c.lower() or "kho_giao_name" in c.lower()), df_table.columns[1] if len(df_table.columns) > 1 else df_table.columns[0])
    
    df_table = df_table.dropna(subset=[id_col, name_col], how='all')
    df_table = df_table[df_table[id_col].astype(str).str.strip() != ""]
    
    id_to_am = {}
    id_to_prov = {}
    name_to_am = {}
    name_to_prov = {}
    co_cau_path = 'co_cau_ntb.csv'
    if os.path.exists(co_cau_path):
        df_cc = safe_read_csv(co_cau_path)
        for _, r in df_cc.iterrows():
            bc_id = r.get('warehouse_id')
            bc_name = str(r.get('Bưu cục', '')).strip()
            am = str(r.get('AM', '')).strip()
            prov = str(r.get('Tỉnh', '')).strip()
            if prov == 'Khánh Hoà':
                prov = 'Khánh Hòa'
            if prov == 'Bình Phước':
                prov = 'Lâm Đồng'
            
            if pd.notna(bc_id):
                try:
                    id_to_am[int(bc_id)] = am
                    id_to_prov[int(bc_id)] = prov
                except:
                    pass
            if bc_name:
                name_clean = clean_po_name(bc_name)
                name_to_am[name_clean] = am
                name_to_prov[name_clean] = prov

    processed_records = []
    for _, r in df_table.iterrows():
        po_id = r.get(id_col)
        po_name = r.get(name_col)
        
        mapped_am, mapped_prov = map_po_to_am_prov(po_id, po_name, id_to_am, id_to_prov, name_to_am, name_to_prov, r.get('AM', 'Không xác định'), r.get('tinh_giao', 'Không xác định'))
        
        days_col = next((c for c in df_table.columns if "du_kien_clear_ton" in c.lower() or "clear_ton" in c.lower() or c == "du_kien_clear_ton"), None)
        days_val = 0
        if days_col and days_col in df_table.columns:
            days_val = r[days_col]
        elif len(df_table.columns) > 17:
            days_val = r.iloc[17]
            
        try:
            days_val = int(float(days_val)) if pd.notna(days_val) else 0
        except:
            days_val = 0
            
        reason_col = next((c for c in df_table.columns if "ly_do" in c.lower() or "reason" in c.lower() or "ly_do_bat_on" in c.lower()), None)
        reason_val = ""
        if reason_col:
            reason_val = str(r[reason_col]).strip() if pd.notna(r[reason_col]) else ""
        elif len(df_table.columns) > 18:
            reason_val = str(r.iloc[18]).strip() if pd.notna(r.iloc[18]) else ""
            
        status_col = next((c for c in df_table.columns if "trạng thái" in c.lower() or "status" in c.lower() or "trang_thai" in c.lower()), None)
        status_val = "Bình thường"
        if status_col:
            status_val = str(r[status_col]).strip() if pd.notna(r[status_col]) else "Bình thường"
        elif len(df_table.columns) > 19:
            status_val = str(r.iloc[19]).strip() if pd.notna(r.iloc[19]) else "Bình thường"
            
        try:
            po_id_clean = int(float(po_id)) if pd.notna(po_id) else None
        except:
            continue
            
        def safe_int(val):
            try:
                return int(float(val)) if pd.notna(val) else 0
            except:
                return 0

        record = {
            "id": po_id_clean,
            "name": str(po_name).strip() if pd.notna(po_name) else "",
            "am": mapped_am,
            "province": mapped_prov,
            "ton_lm": safe_int(r.get('BL LM', 0)),
            "ton_lm_5n": safe_int(r.get('BL LM >5 ngay', 0)),
            "pct_lm_5n": round(parse_unstable_pct(r.get('%BL LM >5 ngay', 0)), 2),
            "ton_ktc": safe_int(r.get('BL KTC', 0)),
            "ton_ktc_cung_tinh": safe_int(r.get('BL KTC cung tinh %', r.get('BL KTC cung tinh', 0))),
            "pct_ktc_cung_tinh": round(parse_unstable_pct(r.get('%BL KTC cung tinh', 0)), 2),
            "days_unstable": days_val,
            "reason": reason_val,
            "status": status_val
        }
        processed_records.append(record)
        
    unstable_by_am = {}
    for rec in processed_records:
        if rec["status"] == "Bất ổn":
            am_name = rec["am"]
            if am_name not in unstable_by_am:
                unstable_by_am[am_name] = []
            unstable_by_am[am_name].append(rec["name"])
            
    am_deepdive = []
    for am, pos in unstable_by_am.items():
        am_deepdive.append({
            "am": am,
            "count": len(pos),
            "pos": pos
        })
    am_deepdive = sorted(am_deepdive, key=lambda x: x["count"], reverse=True)
    
    actual_total_warnings = sum(1 for rec in processed_records if rec["status"] == "Bất ổn")
    
    return {
        "update_time": update_time,
        "total_warning": actual_total_warnings,
        "records": clean_nan(processed_records),
        "am_deepdive": clean_nan(am_deepdive)
    }

res = process_unstable_po()
print("Number of records:", len(res.get('records', [])))
print("Total warning count:", res.get('total_warning'))
print("First 3 records:")
for r in res.get('records', [])[:3]:
    print(r)
print("AM Deepdive:")
for ad in res.get('am_deepdive', []):
    print(ad)
