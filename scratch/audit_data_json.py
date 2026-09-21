import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print("ALL TOP LEVEL KEYS IN DATA.JSON:")
print(list(d.keys()))

def inspect_section(name, key):
    print(f"\n=================== {name} ({key}) ===================")
    if key not in d:
        print("KEY NOT FOUND")
        return
    val = d[key]
    if isinstance(val, dict):
        for subk in val.keys():
            subval = val[subk]
            if isinstance(subval, list):
                print(f"  Subkey: {subk} (len {len(subval)})")
                if len(subval) > 0 and isinstance(subval[0], dict):
                    # print first 2
                    print(f"    Sample: {subval[:2]}")
            else:
                print(f"  Subkey: {subk} -> {str(subval)[:80]}")

inspect_section("VOLUME", "volume")
inspect_section("GTC TONG", "gtc_tong")
inspect_section("GTC CA 1", "gtc_ca1_tts")
inspect_section("GAN", "gan")
inspect_section("ODR", "odr")
inspect_section("LTC", "ltc")
inspect_section("OPR", "opr_tts")
inspect_section("ROT LC", "rot_lc")
