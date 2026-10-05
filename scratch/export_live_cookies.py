import os
import sys
import json
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

PROFILE_DIR = r"C:\Users\lap4all\Documents\Auto report\playwright_profile"
OUTPUT_FILE = r"C:\Users\lap4all\Documents\Auto report\cookies_ghn.json"
DASHBOARD_URL = "https://baocao.ghn.vn/dashboards/63bd175cd4435a369fade8f5"

def export():
    print(f"Launching persistent context with profile: {PROFILE_DIR}...")
    with sync_playwright() as p:
        try:
            context = p.chromium.launch_persistent_context(
                user_data_dir=PROFILE_DIR,
                channel="msedge",
                headless=True,
                args=["--disable-blink-features=AutomationControlled"]
            )
        except Exception as e:
            print(f"Error launching msedge: {e}, trying chromium default...")
            context = p.chromium.launch_persistent_context(
                user_data_dir=PROFILE_DIR,
                headless=True,
                args=["--disable-blink-features=AutomationControlled"]
            )
        
        page = context.new_page()
        print(f"Navigating to {DASHBOARD_URL}...")
        try:
            page.goto(DASHBOARD_URL, timeout=30000, wait_until="domcontentloaded")
            page.wait_for_timeout(5000)
            print("Current page URL:", page.url)
            print("Current page title:", page.title())
        except Exception as e:
            print("Navigation error:", e)

        storage = context.storage_state()
        cookie_count = len(storage.get("cookies", []))
        print(f"Total cookies found: {cookie_count}")
        
        # Save to OUTPUT_FILE
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(storage, f, ensure_ascii=False, indent=2)
        print(f"Saved cookies to {OUTPUT_FILE}")
        
        # Also save a copy locally in scratch
        scratch_copy = os.path.join(os.path.dirname(__file__), "cookies_ghn.json")
        with open(scratch_copy, "w", encoding="utf-8") as f:
            json.dump(storage, f, ensure_ascii=False, indent=2)
        print(f"Saved copy to {scratch_copy}")

        context.close()

if __name__ == "__main__":
    export()
