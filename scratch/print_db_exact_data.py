import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', encoding='utf-8') as f:
    d = json.load(f)

def print_section(title, data):
    print(f"\n==================== {title} ====================")
    if isinstance(data, dict):
        for k, v in data.items():
            if isinstance(v, list):
                print(f"{k}: list of {len(v)} items")
                for item in v[:5]:
                    print("  ", item)
            else:
                print(f"{k}: {v}")
    elif isinstance(data, list):
        print(f"List of {len(data)} items:")
        for item in data[:6]:
            print("  ", item)

print_section("GAN OVERVIEW", d.get('gan_overview'))
print_section("GAN AM", d.get('gan_am'))
print_section("ODR OVERVIEW", d.get('odr_overview'))
print_section("ODR AM", d.get('odr_am'))
print_section("ODR PROVINCE", d.get('odr_province'))
print_section("OPR TTS AM", d.get('opr_tts_am'))
print_section("ROT LC AM", d.get('rot_lc_am'))
print_section("ROT LC PROVINCE", d.get('rot_lc_province'))
print_section("ROT LC BC", d.get('rot_lc_bc'))
print_section("FD OVERVIEW", d.get('fd_overview'))
print_section("FD AM", d.get('fd_am'))
print_section("FD BC", d.get('fd_bc'))
print_section("COD REPORT", d.get('cod_report'))
print_section("TRUY THU REPORT", d.get('truy_thu_report'))
