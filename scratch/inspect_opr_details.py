import json, sys
sys.stdout.reconfigure(encoding='utf-8')

d = json.load(open('data.json', encoding='utf-8'))
opr = d.get('opr_tts', {})
ams = opr.get('am', [])
tinhs = opr.get('tinh', [])

print(f"=== OPR TIKTOK SHOP - 5 TỈNH ===")
tot_vol_day = sum(t.get('vol_day', 0) for t in tinhs)
tot_vol_night = sum(t.get('vol_night', 0) for t in tinhs)
tot_vol = sum(t.get('vol_total', 0) for t in tinhs)

# Weighted rates
sum_pass_day_w37 = sum(t.get('vol_day', 0) * t.get('w37_day', 0) for t in tinhs)
sum_pass_night_w37 = sum(t.get('vol_night', 0) * t.get('w37_night', 0) for t in tinhs)
sum_pass_tot_w37 = sum(t.get('vol_total', 0) * t.get('w37_total', 0) for t in tinhs)

sum_pass_day_w35 = sum(t.get('vol_day', 0) * t.get('w35_day', 0) for t in tinhs)
sum_pass_night_w35 = sum(t.get('vol_night', 0) * t.get('w35_night', 0) for t in tinhs)
sum_pass_tot_w35 = sum(t.get('vol_total', 0) * t.get('w35_total', 0) for t in tinhs)

rate_day_w37 = sum_pass_day_w37 / tot_vol_day if tot_vol_day else 0
rate_night_w37 = sum_pass_night_w37 / tot_vol_night if tot_vol_night else 0
rate_tot_w37 = sum_pass_tot_w37 / tot_vol if tot_vol else 0

rate_tot_w35 = sum_pass_tot_w35 / tot_vol if tot_vol else 0
diff_tot = rate_tot_w37 - rate_tot_w35

print(f"Toàn vùng: Tổng {tot_vol:,} đơn (Ngày: {tot_vol_day:,}, Đêm: {tot_vol_night:,})")
print(f"Tỷ lệ Toàn Vùng W37: Tổng={rate_tot_w37*100:.2f}% (WoW: {diff_tot*100:+.2f}%), Ca Ngày={rate_day_w37*100:.2f}%, Ca Đêm={rate_night_w37*100:.2f}%")

print("\n--- Chi tiết 5 Tỉnh ---")
for t in sorted(tinhs, key=lambda x: x.get('w37_total', 0), reverse=True):
    print(f"{t['tinh']}: Tổng={t.get('w37_total',0)*100:.2f}% (WoW: {t.get('diff_total',0)*100:+.2f}%), Ca Ngày={t.get('w37_day',0)*100:.2f}%, Ca Đêm={t.get('w37_night',0)*100:.2f}%, Vol={t.get('vol_total')}")

print(f"\n=== Chi tiết {len(ams)} AM (Sorted by W37 Total desc) ===")
for a in sorted(ams, key=lambda x: x.get('w37_total', 0), reverse=True):
    print(f"{a['am']} ({a.get('tinh')}): Tổng={a.get('w37_total',0)*100:.1f}% (WoW: {a.get('diff_total',0)*100:+.1f}%), Ca Ngày={a.get('w37_day',0)*100:.1f}%, Ca Đêm={a.get('w37_night',0)*100:.1f}%, Vol={a.get('vol_total')}")
