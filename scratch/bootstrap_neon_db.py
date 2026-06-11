import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(override=True)

from app import async_sync_task, SYNC_STATUS

def bootstrap():
    print("Bootstrapping your Neon PostgreSQL database with latest Google Sheets data...")
    print("This will download all 15 sheets and write them directly to your Database tables.")
    
    # Run the sync task synchronously
    async_sync_task(is_admin_flag=True)
    
    if SYNC_STATUS["status"] == "success":
        print("\nSUCCESS! Your database is now fully bootstrapped and populated with all sheet tables!")
    else:
        print("\nFAIL: Synchronization encountered an error:")
        print(SYNC_STATUS["error"])
        sys.exit(1)

if __name__ == "__main__":
    bootstrap()
