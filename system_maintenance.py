import os
import shutil
from datetime import datetime, timedelta

# Define folders to clean
LOG_DIR = 'logs'
CACHE_DIR = 'cache'

# Cleanup settings
MAX_LOG_AGE_DAYS = 7
MAX_CACHE_AGE_DAYS = 3

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(CACHE_DIR, exist_ok=True)

def delete_old_files(folder_path, max_age_days):
    """Delete files older than `max_age_days` in a folder."""
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

def run_cleanup():
    print("[System] Running automatic cleanup...")
    delete_old_files(LOG_DIR, MAX_LOG_AGE_DAYS)
    delete_old_files(CACHE_DIR, MAX_CACHE_AGE_DAYS)
    print("[System] Cleanup complete.")

if __name__ == '__main__':
    run_cleanup()
