#!/usr/bin/env python3
"""alert_balance.py — Alert Telegram bila baki DeepSeek bawah threshold.

Semak balance real-time dari api.deepseek.com. Kalau bawah THRESHOLD,
hantar mesej ke Telegram bot (auraSakluma_bot) — boss akan dapat notif.

Guna: python3 alert_balance.py [--threshold 1.0] [--dry-run]
Cadangan cron: tiap 30 minit (deliver tidak perlu — script hantar sendiri).
"""
import argparse
import json
import os
import re
import subprocess
import sys
import urllib.request

THRESHOLD = 1.0  # USD
HERMES_HOME = os.path.expanduser("~/.hermes")
CHAT_ID = "7833562484"  # Sakluma Original


def env_val(name):
    p = os.path.join(HERMES_HOME, ".env")
    if os.path.exists(p):
        m = re.search(rf"^{re.escape(name)}=(.+)$", open(p, errors="ignore").read(), re.M)
        if m:
            return m.group(1).strip().strip('"').strip("'")
    return ""


def get_balance():
    key = env_val("DEEPSEEK_API_KEY")
    if not key:
        return None, "tiada key"
    try:
        r = subprocess.run(
            ["curl", "-s", "-m", "15", "https://api.deepseek.com/user/balance",
             "-H", f"Authorization: Bearer {key}"],
            capture_output=True, text=True, timeout=20)
        d = json.loads(r.stdout)
        if d.get("is_available") and d.get("balance_infos"):
            b = d["balance_infos"][0]
            return float(b.get("total_balance", 0)), b.get("currency", "USD")
        return None, d.get("message", "error")
    except Exception as e:
        return None, str(e)[:80]


def send_telegram(text):
    token = env_val("TELEGRAM_BOT_TOKEN")
    if not token:
        return False, "tiada token"
    payload = json.dumps({"chat_id": CHAT_ID, "text": text}).encode("utf-8")
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            d = json.load(r)
            return d.get("ok", False), d.get("description", "?")
    except Exception as e:
        return False, str(e)[:80]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--threshold", type=float, default=THRESHOLD, help="Baki bawah berapa (USD)")
    ap.add_argument("--dry-run", action="store_true", help="Cetak sahaja, tak hantar")
    args = ap.parse_args()

    bal, cur = get_balance()
    if bal is None:
        print(f"⚠️ balance tak dapat: {cur}")
        sys.exit(1)

    msg = (f"🔴 *ALERT: Baki DeepSeek bawah $1!*\n"
           f"Baki semasa: *${bal:.2f} {cur}*\n"
           f"Kredit hampir habis — backup (Gemini/Groq) akan auto guna.\n"
           f"Tindakan: top-up kat https://platform.deepseek.com/usage")
    if bal < args.threshold:
        if args.dry_run:
            print("DRY-RUN — akan hantar:")
            print(msg)
            sys.exit(0)
        ok, desc = send_telegram(msg)
        if ok:
            print(f"✅ Alert dihantar — baki ${bal:.2f} {cur} (bawah ${args.threshold})")
        else:
            print(f"❌ Gagal hantar: {desc}")
            sys.exit(1)
    else:
        print(f"🟢 Baki ${bal:.2f} {cur} — melebihi ${args.threshold}, tiada alert")


if __name__ == "__main__":
    main()
