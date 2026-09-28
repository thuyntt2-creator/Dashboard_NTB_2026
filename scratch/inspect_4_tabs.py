import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print("==================== 1. COD / QR PAYMENT ====================")
for k in ['cod_payment', 'cod_report']:
    if k in d:
        print(f"--- {k} ---")
        val = d[k]
        if isinstance(val, dict):
            print("keys:", val.keys())
            for subk in val.keys():
                subv = val[subk]
                if isinstance(subv, (dict, list)):
                    print(f"  {subk}:", json.dumps(subv, ensure_ascii=False)[:300])
                else:
                    print(f"  {subk}:", subv)
        elif isinstance(val, list):
            print(f"list len {len(val)}:", json.dumps(val[:3], ensure_ascii=False))

print("\n==================== 2. TRUY THU ====================")
for k in ['truy_thu', 'truy_thu_report']:
    if k in d:
        print(f"--- {k} ---")
        val = d[k]
        if isinstance(val, dict):
            print("keys:", val.keys())
            for subk in val.keys():
                subv = val[subk]
                if isinstance(subv, (dict, list)):
                    print(f"  {subk}:", json.dumps(subv, ensure_ascii=False)[:300])
                else:
                    print(f"  {subk}:", subv)
        elif isinstance(val, list):
            print(f"list len {len(val)}:", json.dumps(val[:3], ensure_ascii=False))

print("\n==================== 3. KINH DOANH & F30 ====================")
for k in ['kinh_doanh', 'f30']:
    if k in d:
        print(f"--- {k} ---")
        val = d[k]
        if isinstance(val, dict):
            print("keys:", val.keys())
            for subk in val.keys():
                subv = val[subk]
                if isinstance(subv, (dict, list)):
                    print(f"  {subk}:", json.dumps(subv, ensure_ascii=False)[:300])
                else:
                    print(f"  {subk}:", subv)
        elif isinstance(val, list):
            print(f"list len {len(val)}:", json.dumps(val[:3], ensure_ascii=False))

print("\n==================== 4. BƯU CỤC CẢNH BÁO ====================")
if 'bc_canh_bao' in d:
    val = d['bc_canh_bao']
    if isinstance(val, dict):
        print("keys:", val.keys())
        for subk in val.keys():
            print(f"  {subk}:", json.dumps(val[subk], ensure_ascii=False)[:300])
    elif isinstance(val, list):
        print(f"list len {len(val)}:", json.dumps(val[:5], ensure_ascii=False))
