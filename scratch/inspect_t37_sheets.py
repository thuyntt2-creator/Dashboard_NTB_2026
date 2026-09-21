import gspread
import json

gc = gspread.oauth(authorized_user_filename='authorized_user.json')
doc = gc.open_by_key('1E9BdaxouCeTUBeGLh0kyieyWE6wZoymglbZw19LRKEo')

for sheet_name in ['Tong quan T37', 'KH moi T37', 'Nhom A T37', 'KH A', 'KH A N-1']:
    try:
        ws = doc.worksheet(sheet_name)
        vals = ws.get_all_values()
        print(f"=== {sheet_name} (rows: {len(vals)}) ===")
        for i, r in enumerate(vals[:25]):
            non_empty = [f"C{col_idx+1}:{c}" for col_idx, c in enumerate(r[:15]) if c != '']
            if non_empty:
                print(f"R{i+1}: " + " | ".join(non_empty))
    except Exception as e:
        print(f"Error {sheet_name}: {e}")
