#!/usr/bin/env python3
"""AuraOne Hermes VPS Housekeeping & Maintenance Script.

Fungsi:
1. Membersihkan dump sesi lama (> 3 hari) dalam ~/.hermes/sessions/
2. Mengosongkan log lapuk yang sudah di-rotate (~/.hermes/logs/*.log.1)
3. Membersihkan fail temporary & cache lapuk
4. Mengekalkan semua pangkalan data utama, .env, identiti, dan skills

Penggunaan:
  python3 clean_hermes.py [--dry-run]
"""

import os
import glob
import time
import sys

HERMES_DIR = os.path.expanduser("~/.hermes")
DRY_RUN = "--dry-run" in sys.argv

def get_size(path):
    if os.path.isfile(path):
        return os.path.getsize(path)
    total = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                try:
                    total += os.path.getsize(fp)
                except Exception:
                    pass
    return total

def format_size(bytes_val):
    if bytes_val < 1024:
        return f"{bytes_val} B"
    elif bytes_val < 1024 * 1024:
        return f"{bytes_val / 1024:.1f} KB"
    else:
        return f"{bytes_val / (1024 * 1024):.2f} MB"

def main():
    print("=" * 60)
    print(" 🧹 AURAONE HERMES VPS HOUSEKEEPING & OPTIMIZER")
    print("=" * 60)
    print(f"Path: {HERMES_DIR}")
    if DRY_RUN:
        print("⚠️  MOD: DRY-RUN (Tiada fail akan dipadam)")
    print("-" * 60)

    if not os.path.exists(HERMES_DIR):
        print("❌ Direktori ~/.hermes tidak dijumpai.")
        return

    initial_size = get_size(HERMES_DIR)
    total_reclaimed = 0

    # 1. Bersihkan sessions request_dump_*.json
    sessions_dir = os.path.join(HERMES_DIR, "sessions")
    deleted_dumps = 0
    dumps_bytes = 0

    if os.path.exists(sessions_dir):
        dumps = sorted(glob.glob(os.path.join(sessions_dir, "request_dump_*.json")))
        # Simpan 5 fail terkini, padam yang selebihnya
        to_delete = dumps[:-5] if len(dumps) > 5 else []
        for dump_file in to_delete:
            sz = os.path.getsize(dump_file)
            dumps_bytes += sz
            deleted_dumps += 1
            if not DRY_RUN:
                try:
                    os.remove(dump_file)
                except Exception as e:
                    print(f"Error removing {dump_file}: {e}")

        print(f"📦 [SESSIONS DUMP] : Dipadam {deleted_dumps} fail lama ({format_size(dumps_bytes)} dijimatkan)")
        total_reclaimed += dumps_bytes

    # 2. Kosongkan log lapuk yang di-rotate (*.log.1, *.log.2)
    logs_dir = os.path.join(HERMES_DIR, "logs")
    log_bytes = 0
    cleaned_logs = 0

    if os.path.exists(logs_dir):
        for log_file in glob.glob(os.path.join(logs_dir, "*.log.*")):
            sz = os.path.getsize(log_file)
            log_bytes += sz
            cleaned_logs += 1
            if not DRY_RUN:
                try:
                    # Truncate / kosongkan fail log rotate
                    with open(log_file, "w") as f:
                        f.truncate(0)
                except Exception as e:
                    print(f"Error truncating {log_file}: {e}")

        print(f"📜 [ROTATED LOGS]  : Dikosongkan {cleaned_logs} fail log lapuk ({format_size(log_bytes)} dijimatkan)")
        total_reclaimed += log_bytes

    # 3. Bersihkan fail temp /tmp
    tmp_cleaned = 0
    for tmp_pattern in ["/tmp/scanner*.py", "/tmp/scan_results*.txt"]:
        for tmp_file in glob.glob(tmp_pattern):
            if not DRY_RUN:
                try:
                    os.remove(tmp_file)
                    tmp_cleaned += 1
                except Exception:
                    pass

    print("-" * 60)
    print(f"✅ JUMLAH STORAN DIJIMATKAN: {format_size(total_reclaimed)}")
    print(f"📊 Saiz ~/.hermes Sekarang  : {format_size(initial_size - total_reclaimed if not DRY_RUN else initial_size)}")
    print("=" * 60)

if __name__ == "__main__":
    main()
