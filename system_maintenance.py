import os
import shutil
from datetime import datetime, timedelta

LOG_DIR = 'logs'
CACHE_DIR = 'cache'
LAST_CLEAN_FILE = '.last_cleanup'  # hidden file to store last cleanup time

MAX_LOG_AGE_DAYS = 7
MAX_CACHE_AGE_DAYS = 3
CLEANUP_INTERVAL_DAYS = 30  # perform full clean once every 30 days

def delete_old_files(folder_path, max_age_days):
    if not os.path.exists(folder_path):
        return

    now = datetime.now()
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            file_age = now - datetime.fromtimestamp(os.path.getmtime(file_path))
            if file_age > timedelta(days=max_age_days):
                try:
                    os.remove(file_path)
                    print(f"[Cleanup] Deleted: {file_path}")
                except Exception as e:
                    print(f"[Cleanup] Failed to delete {file_path}: {e}")

def should_run_cleanup():
    if not os.path.exists(LAST_CLEAN_FILE):
        return True
    with open(LAST_CLEAN_FILE, 'r') as f:
        last_clean = datetime.fromisoformat(f.read().strip())
    return datetime.now() - last_clean >= timedelta(days=CLEANUP_INTERVAL_DAYS)

def update_cleanup_time():
    with open(LAST_CLEAN_FILE, 'w') as f:
        f.write(datetime.now().isoformat())

def run_cleanup(force=False):
    if force or should_run_cleanup():
        print("[System] Running monthly cleanup...")
        os.makedirs(LOG_DIR, exist_ok=True)
        os.makedirs(CACHE_DIR, exist_ok=True)

        delete_old_files(LOG_DIR, MAX_LOG_AGE_DAYS)
        delete_old_files(CACHE_DIR, MAX_CACHE_AGE_DAYS)

        update_cleanup_time()
        print("[System] Cleanup complete.")
    else:
        print("[System] Cleanup not needed yet.")

if __name__ == '__main__':
    run_cleanup(force=True)
