import sys
import os
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

artifact_dir = r"C:\Users\lap4all\.gemini\antigravity-ide\brain\1048c0be-798c-47f0-9d90-dfb903985b99\.tempmediaStorage"
os.makedirs(artifact_dir, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1600, 'height': 1000})

    errors = []
    page.on("pageerror", lambda err: errors.append(f"PAGE ERROR: {err}"))
    page.on("console", lambda msg: errors.append(f"CONSOLE: {msg.text}") if msg.type == "error" else None)

    print("Navigating to http://127.0.0.1:3000/hop ...", flush=True)
    page.goto("http://127.0.0.1:3000/hop", wait_until="domcontentloaded")
    page.wait_for_timeout(1000)

    # 1. TAB 2: SẢN LƯỢNG (data-tab="tab-volume")
    print("\n--- TAB 2: SẢN LƯỢNG ---", flush=True)
    page.locator('[data-tab="tab-volume"]').click()
    page.wait_for_timeout(500)
    th_vol_full = page.locator('#table-vol-tinh-full thead tr th').all_inner_texts()
    th_vol_tts = page.locator('#table-vol-tinh-tts thead tr th').all_inner_texts()
    print("Table Vol Tinh Full Headers:", th_vol_full, flush=True)
    print("Table Vol Tinh TTS Headers:", th_vol_tts, flush=True)
    row_vol_full_1 = page.locator('#table-vol-tinh-full tbody tr').first.all_inner_texts()
    print("Table Vol Tinh Full Row 1:", row_vol_full_1, flush=True)
    page.locator('#tab-volume').screenshot(path=os.path.join(artifact_dir, "tab2_san_luong.png"))

    # 2. TAB 3: %GTC TỔNG (data-tab="tab-gtc-tong")
    print("\n--- TAB 3: %GTC TỔNG ---", flush=True)
    page.locator('[data-tab="tab-gtc-tong"]').click()
    page.wait_for_timeout(500)
    th_gtc_full = page.locator('#table-gtc-tinh-full thead tr th').all_inner_texts()
    th_gtc_tts = page.locator('#table-gtc-tinh-tts thead tr th').all_inner_texts()
    print("Table GTC Tinh Full Headers:", th_gtc_full, flush=True)
    print("Table GTC Tinh TTS Headers:", th_gtc_tts, flush=True)
    row_gtc_full_1 = page.locator('#table-gtc-tinh-full tbody tr').first.all_inner_texts()
    print("Table GTC Tinh Full Row 1:", row_gtc_full_1, flush=True)
    page.locator('#tab-gtc-tong').screenshot(path=os.path.join(artifact_dir, "tab3_gtc_tong.png"))

    # 3. TAB 4: %GTC CA 1 TTS (data-tab="tab-gtc-tts-ca1")
    print("\n--- TAB 4: %GTC CA 1 TTS ---", flush=True)
    page.locator('[data-tab="tab-gtc-tts-ca1"]').click()
    page.wait_for_timeout(500)
    th_ca1_tts = page.locator('#table-gtc-tts-ca1-detailed thead tr th').all_inner_texts()
    count_ca1_tts = page.locator('#table-gtc-tts-ca1-detailed tbody tr').count()
    print("Table GTC TTS Ca 1 Headers:", th_ca1_tts, flush=True)
    print("Table GTC TTS Ca 1 Rows count:", count_ca1_tts, flush=True)
    if count_ca1_tts > 0:
        print("Row 1:", page.locator('#table-gtc-tts-ca1-detailed tbody tr').first.all_inner_texts(), flush=True)
    page.locator('#tab-gtc-tts-ca1').screenshot(path=os.path.join(artifact_dir, "tab4_gtc_ca1_tts.png"))

    # 4. TAB 5: %GÁN (data-tab="tab-gan")
    print("\n--- TAB 5: %GÁN ---", flush=True)
    page.locator('[data-tab="tab-gan"]').click()
    page.wait_for_timeout(500)
    th_gan_ov = page.locator('#table-gan-overview-region thead tr th').all_inner_texts()
    count_gan_ov = page.locator('#table-gan-overview-region tbody tr').count()
    print("Table Gan Overview Headers:", th_gan_ov, flush=True)
    print("Table Gan Overview Rows count:", count_gan_ov, flush=True)
    if count_gan_ov > 0:
        print("Row 1:", page.locator('#table-gan-overview-region tbody tr').first.all_inner_texts(), flush=True)
    page.locator('#tab-gan').screenshot(path=os.path.join(artifact_dir, "tab5_gan.png"))

    # 5. TAB 6: %ODR (data-tab="tab-odr")
    print("\n--- TAB 6: %ODR ---", flush=True)
    page.locator('[data-tab="tab-odr"]').click()
    page.wait_for_timeout(500)
    th_odr_full = page.locator('#table-odr-tinh-full thead tr th').all_inner_texts()
    th_odr_tts = page.locator('#table-odr-tinh-tts thead tr th').all_inner_texts()
    print("Table ODR Tinh Full Headers:", th_odr_full, flush=True)
    print("Table ODR Tinh TTS Headers:", th_odr_tts, flush=True)
    row_odr_full_1 = page.locator('#table-odr-tinh-full tbody tr').first.all_inner_texts()
    print("Table ODR Tinh Full Row 1:", row_odr_full_1, flush=True)
    page.locator('#tab-odr').screenshot(path=os.path.join(artifact_dir, "tab6_odr.png"))

    # 6. TAB 9: RỚT LUÂN CHUYỂN (data-tab="tab-rot-lc")
    print("\n--- TAB 9: RỚT LUÂN CHUYỂN ---", flush=True)
    page.locator('[data-tab="tab-rot-lc"]').click()
    page.wait_for_timeout(500)
    th_rot_am = page.locator('#table-rot-am-detailed thead tr th').all_inner_texts()
    th_rot_tinh = page.locator('#table-rot-tinh-detailed thead tr th').all_inner_texts()
    th_rot_bc = page.locator('#table-rot-lc-top-bc thead tr th').all_inner_texts()
    count_rot_am = page.locator('#table-rot-am-detailed tbody tr').count()
    count_rot_tinh = page.locator('#table-rot-tinh-detailed tbody tr').count()
    count_rot_bc = page.locator('#table-rot-lc-top-bc tbody tr').count()
    print("Table Rot AM Headers:", th_rot_am, flush=True)
    print("Table Rot AM Rows count:", count_rot_am, flush=True)
    if count_rot_am > 0:
        print("Rot AM Row 1:", page.locator('#table-rot-am-detailed tbody tr').first.all_inner_texts(), flush=True)
    print("Table Rot Tinh Headers:", th_rot_tinh, flush=True)
    print("Table Rot Tinh Rows count:", count_rot_tinh, flush=True)
    if count_rot_tinh > 0:
        print("Rot Tinh Row 1:", page.locator('#table-rot-tinh-detailed tbody tr').first.all_inner_texts(), flush=True)
    print("Table Rot Top BC Headers:", th_rot_bc, flush=True)
    print("Table Rot Top BC Rows count:", count_rot_bc, flush=True)
    if count_rot_bc > 0:
        print("Rot Top BC Row 1:", page.locator('#table-rot-lc-top-bc tbody tr').first.all_inner_texts(), flush=True)
    page.locator('#tab-rot-lc').screenshot(path=os.path.join(artifact_dir, "tab9_rot_lc.png"))

    print("\n--- CONSOLE / PAGE ERRORS ---", flush=True)
    print(f"Total errors: {len(errors)}", flush=True)
    for err in errors:
        print(err, flush=True)

    browser.close()
    print("\nALL CHECKS COMPLETED SUCCESSFULLY!", flush=True)
