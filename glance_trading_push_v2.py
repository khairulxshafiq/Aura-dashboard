#!/usr/bin/env python3
"""
glance_trading_push.py — Push harga live watchlist & position Moomoo ke Glance widgets (iOS).
Elegantly formatted for iOS Glance Widgets.
"""
import argparse
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.request

FEEDS_PATH = "/home/ubuntu/scripts/glance_trading_feeds.json"
GLANCE_API = "https://glance-api.fly.dev/ingest"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

# Kod Bursa untuk klsescreener (nama -> kod)
BURSA_CODES = {
    "SAMAIDEN": "0223", "TIMECOM": "5031", "INARI": "0166",
    "AEMULUS": "0181", "SLVEST": "0215", "LFG": "5255", "RANHILL": "5272",
}
# Ticker US via Moomoo
US_TICKERS = {"VOO", "SCHD", "QQQ", "SPY", "VTI", "VXUS", "BND", "FUTU"}
CRYPTO_COINS = {"BTC": "bitcoin", "ETH": "ethereum"}
# Kod Moomoo Bursa -> nama penuh
NAMES = {
    "MY.0223": "SAMAIDEN", "MY.5031": "TIMECOM", "MY.0166": "INARI",
    "MY.0181": "AEMULUS", "MY.0215": "SLVEST", "MY.5255": "LFG", "MY.5272": "RANHILL",
}


def load_feeds():
    try:
        with open(FEEDS_PATH) as f:
            return json.load(f)
    except Exception:
        return {}


def save_feeds(feeds):
    with open(FEEDS_PATH, "w") as f:
        json.dump(feeds, f, indent=2, ensure_ascii=False)


def moomoo_call(tool, args):
    mcporter_bin = shutil.which("mcporter") or os.path.expanduser("~/.local/bin/mcporter")
    env = dict(os.environ, PATH=f"{os.path.expanduser('~/.local/bin')}:{os.environ.get('PATH', '')}")
    out = subprocess.run(
        [mcporter_bin, "call", f"moomoo.{tool}", "--args", json.dumps(args)],
        capture_output=True, text=True, timeout=90, env=env
    )
    try:
        return json.loads(out.stdout)
    except Exception:
        return None


def fetch_us(ticker):
    """US ETF harga via Moomoo. Return (price, chg_pct) atau (None, None)."""
    d = moomoo_call("get_stock_quote", {"codes": [f"US.{ticker}"]})
    if not d or "result" not in d or not d["result"]:
        return None, None
    r = d["result"][0]
    last = r.get("last_price")
    prev = r.get("prev_close_price")
    if last is None:
        return None, None
    chg = ((last - prev) / prev * 100) if prev else None
    return round(last, 2), (round(chg, 2) if chg is not None else None)


def fetch_bursa(code):
    """Bursa harga via klsescreener view page. Return (price, chg_pct)."""
    kls = BURSA_CODES.get(code)
    if not kls:
        return None, None
    url = f"https://www.klsescreener.com/v2/stocks/view/{kls}"
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        html = r.read().decode()
    m = re.search(r'id="price"[^>]*data-value="([0-9.]+)"', html)
    if not m:
        return None, None
    price = float(m.group(1))
    m2 = re.search(r'id="priceDiff">([-+]?[0-9.]+) \(([-+]?[0-9.]+)%\)', html)
    if m2:
        return price, float(m2.group(2))
    return price, None


def fetch_crypto(coin):
    """Crypto via CoinGecko. Return (price, chg_24h_pct)."""
    cid = CRYPTO_COINS.get(coin)
    if not cid:
        return None, None
    url = ("https://api.coingecko.com/api/v3/simple/price"
           f"?ids={cid}&vs_currencies=usd&include_24hr_change=true")
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        d = json.loads(r.read().decode())
    if cid not in d:
        return None, None
    price = d[cid]["usd"]
    chg = d[cid].get("usd_24h_change")
    return round(price, 2), (round(chg, 2) if chg is not None else None)


def get_quote(ticker):
    """Router: US / Bursa / Crypto -> (price, chg_pct)."""
    if ticker in US_TICKERS:
        return fetch_us(ticker)
    if ticker in BURSA_CODES:
        return fetch_bursa(ticker)
    if ticker in CRYPTO_COINS:
        return fetch_crypto(ticker)
    return fetch_us(ticker)


def push_glance(feed, content, schema="summary"):
    """Push ke Glance API. Return (ok, status)."""
    payload = {
        "schema_type": schema,
        "content": content,
        "intent": {"update_widget": True, "send_push": False},
    }
    if schema == "dynamic" and feed.get("template_id"):
        payload["template_id"] = feed["template_id"]
    url = f"{GLANCE_API}/{feed['feed_id']}"
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode(),
        headers={
            "Authorization": f"Bearer {feed['write_key']}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return True, r.status
    except urllib.error.HTTPError as e:
        return False, f"{e.code}: {e.read().decode()[:200]}"
    except Exception as e:
        return False, str(e)


def fmt_price(ticker, price):
    if ticker in BURSA_CODES:
        return f"RM{price:,.3f}"
    return f"${price:,.2f}"


def fmt_chg(chg):
    if chg is None:
        return ""
    return f"{chg:+.2f}%"


def fmt_time():
    return datetime.datetime.now().strftime("%d/%m %H:%M")


def build_dashboard_content(tickers, quotes):
    """Bina content dynamic ikut field naming layout: {ticker}_price / {ticker}_chg."""
    content = {}
    for t in tickers:
        q = quotes.get(t)
        if not q or q.get("price") is None:
            content[f"{t.lower()}_price"] = "--"
            content[f"{t.lower()}_chg"] = ""
            continue
        content[f"{t.lower()}_price"] = fmt_price(t, q["price"])
        content[f"{t.lower()}_chg"] = fmt_chg(q.get("chg"))
    content["updated_at"] = fmt_time()
    return content


def short_name(code):
    """US.VOO -> VOO; MY.5031 -> TIMECOM (peta nama)."""
    if code.startswith("US."):
        return code.split(".")[1]
    return NAMES.get(code, code.split(".")[1] if "." in code else code)


def fetch_positions(trd_env="REAL"):
    """Ambil positions dari Moomoo. Return list dict penuh."""
    d = moomoo_call("get_positions", {"trd_env": trd_env})
    if not d or "result" not in d:
        return []
    return d["result"]


def fetch_total_assets(trd_env="REAL"):
    d = moomoo_call("get_account_summary", {"trd_env": trd_env})
    try:
        a = d.get("assets", {})
        return a.get("total_assets"), a.get("currency")
    except Exception:
        return None, None


def build_portfolio_compact(positions, total_value, currency):
    """Bina content ultra-elegang utk Glance widget (My Layout / dynamic layout)."""
    cur = currency or "USD"
    pos_items = []
    total_pl_val = 0.0
    has_pl = False
    
    for p in positions:
        code = p.get("code", "")
        name = short_name(code)
        price = p.get("nominal_price")
        pl = p.get("pl_ratio")
        pl_val = p.get("pl_val", 0.0)
        if pl_val:
            total_pl_val += pl_val
            has_pl = True
        
        icon = "🟢" if (pl is not None and pl >= 0) else ("🔴" if (pl is not None and pl < 0) else "⚪")
        px_s = (f"RM{price:,.2f}" if code.startswith("MY.") else f"${price:,.2f}") if price else "--"
        pl_s = f"{pl:+.1f}%" if pl is not None else ""
        pos_items.append(f"{icon} {name}: {px_s} ({pl_s})")
    
    if total_value is not None:
        status_str = f"💰 {cur} {total_value:,.2f}"
    else:
        status_str = "💰 Moomoo Account"
        
    headline_str = "📈 MOOMOO POSITIONS"
    body_str = "\n".join(pos_items[:4]) if pos_items else "Tiada position aktif"
    time_str = datetime.datetime.now().strftime("%I:%M %p")
    footer_str = f"Updated {time_str} • Moomoo OpenD"
    
    return {
        "headline": headline_str,
        "subtitle": status_str,
        "subheadline": status_str,
        "body": body_str,
        "positions": body_str,
        "status": status_str,
        "title": headline_str,
        "footer": footer_str,
        "timestamp": time_str
    }


def build_portfolio_content(positions, total_value, currency):
    """Bina content dynamic utk layout Portfolio (slot P1..P8)."""
    content = {}
    for i, p in enumerate(positions[:8], 1):
        code = p.get("code", "")
        name = short_name(code)
        qty = p.get("qty")
        price = p.get("nominal_price")
        pl_ratio = p.get("pl_ratio")
        qty_s = (f"{qty:,.0f}" if qty == int(qty) else f"{qty:,.4f}".rstrip("0").rstrip("."))
        px_s = (f"RM{price:,.3f}" if code.startswith("MY.") else f"${price:,.2f}") if price else "--"
        pl_s = f"{pl_ratio:+.2f}%" if pl_ratio is not None else ""
        content[f"p{i}_ticker"] = name
        content[f"p{i}_qty"] = qty_s
        content[f"p{i}_price"] = px_s
        content[f"p{i}_pl"] = pl_s
    for i in range(len(positions) + 1, 9):
        content[f"p{i}_ticker"] = "--"
        content[f"p{i}_qty"] = ""
        content[f"p{i}_price"] = ""
        content[f"p{i}_pl"] = ""
    if total_value is not None:
        cur = currency or ""
        content["total_value"] = f"{cur} {total_value:,.2f}"
    else:
        content["total_value"] = "--"
    content["updated_at"] = fmt_time()
    return content


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tickers", nargs="*", default=None,
                    help="Push ticker terpilih sahaja (default: semua dalam config)")
    ap.add_argument("--dry-run", action="store_true",
                    help="Fetch harga je, jangan push")
    ap.add_argument("--dashboard", action="store_true",
                    help="Mode dashboard: push SEMUA ticker ke SATU feed dynamic")
    ap.add_argument("--portfolio", action="store_true",
                    help="Mode portfolio: push positions REAL Moomoo ke widget")
    args = ap.parse_args()

    feeds = load_feeds()
    if not feeds:
        print("ERROR: tiada config feeds. Tambah dulu ke", FEEDS_PATH)
        sys.exit(1)

    if args.portfolio:
        pfeed = feeds.get("__portfolio__")
        if not pfeed:
            print("ERROR: config '__portfolio__' takda dalam", FEEDS_PATH)
            sys.exit(1)
        positions = fetch_positions("REAL")
        if not positions:
            print("ERROR: tiada positions REAL (OpenD/TRADING_PWD?)")
            sys.exit(1)
        total, cur = fetch_total_assets("REAL")
        if pfeed.get("compact"):
            content = build_portfolio_compact(positions, total, cur)
            schema = "dynamic"
        else:
            content = build_portfolio_content(positions, total, cur)
            schema = "dynamic"
        if args.dry_run:
            for p in positions:
                print(f"  {p.get('code')} qty={p.get('qty')} last={p.get('nominal_price')} PL={p.get('pl_ratio')}%")
            print(json.dumps(content, indent=2, ensure_ascii=False))
            return
        ok, status = push_glance(pfeed, content, "dynamic")
        print(f"[{'OK' if ok else 'FAIL'}] portfolio push -> {status}")
        print(json.dumps({"push": "OK" if ok else f"FAIL {status}"}, indent=2))
        return

    if args.dashboard:
        dash = feeds.get("__dashboard__")
        if not dash:
            print("ERROR: config '__dashboard__' takda dalam", FEEDS_PATH)
            sys.exit(1)
        tickers = dash.get("tickers", [])
        quotes = {}
        for t in tickers:
            price, chg = get_quote(t)
            quotes[t] = {"price": price, "chg": chg}
            print(f"  fetch {t}: {fmt_price(t, price) if price else 'NO DATA'} ({fmt_chg(chg)})")
        content = build_dashboard_content(tickers, quotes)
        if args.dry_run:
            print(json.dumps(content, indent=2, ensure_ascii=False))
            return
        ok, status = push_glance(dash, content, "dynamic")
        print(f"[{'OK' if ok else 'FAIL'}] dashboard push -> {status}")
        print(json.dumps({"push": "OK" if ok else f"FAIL {status}"}, indent=2))
        return

    tickers = args.tickers or list(feeds.keys())
    results = {}
    for t in tickers:
        feed = feeds.get(t)
        if not feed:
            results[t] = {"error": "no feed config"}
            continue
        price, chg = get_quote(t)
        if price is None:
            results[t] = {"error": "no price data"}
            continue
        if feed.get("schema") == "dynamic":
            content = {}
            for k, v in feed.get("fields", {}).items():
                content[k] = v.replace("{{price}}", fmt_price(t, price)) \
                              .replace("{{chg}}", fmt_chg(chg)) \
                              .replace("{{ticker}}", t)
            schema = "dynamic"
        else:
            content = {
                "title": t,
                "primary_value": fmt_price(t, price),
                "secondary_value": fmt_chg(chg),
            }
            schema = "summary"
        results[t] = {"price": price, "chg": chg}
        if args.dry_run:
            print(f"[DRY] {t}: {fmt_price(t, price)} ({fmt_chg(chg)})")
            continue
        ok, status = push_glance(feed, content, schema)
        results[t]["push"] = "OK" if ok else f"FAIL {status}"
        print(f"[{'OK' if ok else 'FAIL'}] {t}: {fmt_price(t, price)} ({fmt_chg(chg)}) -> {status}")
        time.sleep(0.5)

    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
