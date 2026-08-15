#!/usr/bin/env python3
"""Collector — kumpul statistik sistem AuraOne untuk dashboard consumption.

Jana /home/ubuntu/aura-dashboard/stats.json (baca oleh dashboard.html).
Guna: python3 collect_stats.py
Cadangan: cron tiap 15 minit + sebelum git push.
"""
import json
import os
import re
import subprocess
import datetime

OUT = "/home/ubuntu/aura-dashboard/stats.json"
HERMES_HOME = os.path.expanduser("~/.hermes")


def sh(cmd, timeout=10):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip()
    except Exception:
        return ""


def pct(used, total):
    try:
        return round(float(used) / float(total) * 100, 1)
    except Exception:
        return None


def collect_system():
    out = {}
    # RAM
    mem = sh("free -m | awk 'NR==2{print $2, $3, $7}'")
    parts = mem.split()
    if len(parts) >= 3:
        total, used, avail = float(parts[0]), float(parts[1]), float(parts[2])
        out["ram_total_mb"] = int(total)
        out["ram_used_mb"] = int(used)
        out["ram_used_pct"] = pct(used, total)
        out["ram_used"] = f"{used:.0f}MB / {total:.0f}MB"
    # CPU
    load = sh("awk '{print $1, $2, $3}' /proc/loadavg")
    ncpu = sh("nproc")
    out["cpu_load"] = load
    out["cpu_pct"] = None
    try:
        l1 = float(load.split()[0]) if load else 0
        nc = int(ncpu) if ncpu else 1
        out["cpu_pct"] = round(min(l1 / nc * 100, 100), 1)
    except Exception:
        pass
    # Disk
    df = sh("df -P / | awk 'NR==2{print $2, $3, $5}'")
    dp = df.split()
    if len(dp) >= 3:
        total_k = float(dp[0]); used_k = float(dp[1])
        out["disk_used"] = dp[2]
        out["disk_pct"] = pct(used_k, total_k)
    # Uptime
    up = sh("cat /proc/uptime")
    try:
        sec = float(up.split()[0])
        d, rem = divmod(int(sec), 86400)
        h, rem = divmod(rem, 3600)
        m = rem // 60
        out["uptime"] = f"{d}h {h}j {m}m"
        out["uptime_detail"] = f"{int(sec)}s"
    except Exception:
        pass
    return out


def collect_services():
    rows = []
    # Gateway
    g = sh("pgrep -f 'gateway run' | head -1")
    if g:
        pid = g.split()[0]
        ps = sh(f"ps -o rss=,%cpu= -p {pid}")
        psp = ps.split()
        mem_mb = round(int(psp[0]) / 1024, 0) if psp else "?"
        cpu = psp[1] if len(psp) > 1 else "?"
        rows.append({"name": "Gateway (telegram)", "status": "running", "pid": pid, "mem": f"{mem_mb:.0f}MB", "cpu": f"{cpu}%"})
    else:
        rows.append({"name": "Gateway", "status": "stopped", "pid": "—", "mem": "—", "cpu": "—"})
    # Agent CLI aktif
    a = sh("pgrep -f 'hermes --continue' | head -1")
    if a:
        rows.append({"name": "Agent (CLI sesi)", "status": "running", "pid": a.split()[0], "mem": "?", "cpu": "?"})
    return rows


def collect_keys():
    keys = []
    env_path = os.path.join(HERMES_HOME, ".env")
    if not os.path.exists(env_path):
        return keys
    mapping = [
        ("DEEPSEEK_API_KEY", "deepseek-v4-flash", "st-live", "aktif", "deepseek"),
        ("GROQ_API_KEY", "backup free", "st-live", "backup", "groq"),
        ("GEMINI_API_KEY", "backup free", "st-live", "backup", "google"),
        ("OPENROUTER_API_KEY", "—", "st-off", "haram/buang", "openrouter"),
        ("TELEGRAM_BOT_TOKEN", "auraSakluma_bot", "st-live", "aktif", "telegram"),
        ("AIRTABLE_API_KEY", "Content Station", "st-live", "aktif", "airtable"),
        ("REPLICATE_API_TOKEN", "FLUX (belum topup)", "st-progress", "relek", "replicate"),
        ("APIFY_API_TOKEN", "scrape", "st-live", "aktif", "apify"),
    ]
    env_text = open(env_path, errors="ignore").read()
    for name, role, cls, status, tag in mapping:
        m = re.search(rf"^{re.escape(name)}=(.+)$", env_text, re.M)
        val = m.group(1).strip().strip('"').strip("'") if m else ""
        prefix = (val[:9] + "...") if val else "—"
        if not val:
            cls = "st-off"
            status = "takda"
        keys.append({"name": name, "status": status, "cls": cls, "role": role, "prefix": prefix, "tag": tag})
    return keys


def collect_model():
    cfg_path = os.path.join(HERMES_HOME, "config.yaml")
    cfg = {}
    try:
        import yaml
        with open(cfg_path) as f:
            cfg = yaml.safe_load(f) or {}
    except Exception:
        pass
    m = cfg.get("model", {})
    fbs = cfg.get("fallback_providers", [])
    out = {
        "default": m.get("default", "?"),
        "provider": m.get("provider", "?"),
        "fallback1": f"{fbs[0]['model']} ({fbs[0]['provider']})" if len(fbs) > 0 else "—",
        "fallback2": f"{fbs[1]['model']} ({fbs[1]['provider']})" if len(fbs) > 1 else "—",
        "cache_hit_pct": None,
    }
    # cache hit dari agent.log (purata)
    logp = os.path.join(HERMES_HOME, "logs", "agent.log")
    if os.path.exists(logp):
        try:
            hits = []
            with open(logp, errors="ignore") as f:
                for line in f:
                    mm = re.search(r"cache=(\d+)/(\d+)", line)
                    if mm:
                        try:
                            hits.append(float(mm.group(1)) / max(float(mm.group(2)), 1) * 100)
                        except Exception:
                            pass
            if hits:
                out["cache_hit_pct"] = round(sum(hits) / len(hits), 1)
        except Exception:
            pass
    return out


def collect_cron():
    rows = []
    try:
        import glob
        for jf in glob.glob(os.path.join(HERMES_HOME, "cron", "*.json")):
            try:
                with open(jf) as f:
                    j = json.load(f)
                rows.append({
                    "name": j.get("name") or os.path.basename(jf).replace(".json", ""),
                    "schedule": j.get("schedule", "?"),
                    "status": "active" if j.get("enabled", True) else "paused",
                })
            except Exception:
                pass
    except Exception:
        pass
    return rows[:10]


def collect_calls():
    rows = []
    logp = os.path.join(HERMES_HOME, "logs", "agent.log")
    if os.path.exists(logp):
        try:
            with open(logp, errors="ignore") as f:
                for line in f:
                    mm = re.search(r"API call #\d+: model=(\S+) provider=(\S+) in=(\d+) out=(\d+) total=(\d+) latency=([\d.]+)s", line)
                    if mm:
                        rows.append({
                            "time": line[:19],
                            "platform": "agent",
                            "model": mm.group(1),
                            "tokens": f"{int(mm.group(3)):,} in / {int(mm.group(4)):,} out",
                            "latency": mm.group(6) + "s",
                        })
        except Exception:
            pass
    rows = rows[-8:][::-1]
    return rows


def collect_tools():
    """Tools/MCP/skills yang disuntik — dengan status & future. Internal dashboard."""
    tools = [
        # (nama, status_class, status_label, guna, nota)
        ("Exa Search (MCP)", "st-live", "LIVE", "Web search berkuasa", "mcporter · exa.web_search_exa"),
        ("Moomoo/OpenD (MCP)", "st-progress", "PROGRESS", "Trading Bursa/US/HK/SG", "Skill moomoo-trading-mcp ada; OpenD perlu deploy (Railway)"),
        ("Jina Reader", "st-live", "LIVE", "Scrape artikel & halaman", "r.jina.ai — auto-resolve link"),
        ("yt-dlp", "st-live", "LIVE", "Download video/audio", "agent-reach v1.5.0"),
        ("Telegram Bot", "st-live", "LIVE", "auraSakluma_bot", "Gateway · button kategori · reply"),
        ("Airtable", "st-live", "LIVE", "Content Station (draf/artikel)", "API key aktif · push flow"),
        ("Google Drive", "st-progress", "PROGRESS", "Host gambar artikel", "Service account email ada; JSON key perlu semak"),
        ("DeepSeek API", "st-live", "LIVE", "deepseek-v4-flash (primary)", "Model utama semua kerja"),
        ("Groq API", "st-live", "LIVE", "llama-3.3-70b (backup)", "Free-tier fallback"),
        ("Gemini API", "st-live", "LIVE", "Backup free + image gen", "gemini-2.5-flash · gemini-3-pro-image"),
        ("Pollinations.ai", "st-live", "LIVE", "Generate gambar free", "No key · primary image"),
        ("Replicate (FLUX)", "st-progress", "PROGRESS", "Gambar pro (belum topup)", "Token ada; credit belum masuk"),
        ("Apify", "st-live", "LIVE", "Scrape automation", "APIFY_API_TOKEN aktif"),
        ("Supabase", "st-progress", "PROGRESS", "DB/host (belum sambung)", "Publishable key je — perlu semak"),
        ("Firecrawl", "st-live", "LIVE", "Web scraping lanjutan", "FC_API_KEY aktif"),
        ("gh (GitHub)", "st-live", "LIVE", "Repo & Pages", "Aura-dashboard live"),
        ("MCP server setup", "st-live", "LIVE", "Skill & workflow", "Skill: mcp-server-setup, trading-mcp-integration"),
    ]
    return tools


def collect_skills():
    """Skills Sakluma/Aura yang wujud — status & future."""
    return [
        ("sakluma-news", "st-live", "LIVE", "Berita trending MY — cross-source + Google Trends"),
        ("sakluma-content", "st-live", "LIVE", "5 persona kandungan — FB/ads/caption"),
        ("sakluma-publish", "st-live", "LIVE", "Push ke Airtable — confirm flow"),
        ("aura-trading", "st-progress", "PROGRESS", "Asri Ahmad method — menunggu Moomoo"),
        ("moomoo-trading-mcp", "st-progress", "PROGRESS", "Integrasi OpenD — deploy Railway"),
        ("trading-mcp-integration", "st-live", "LIVE", "Blueprint sambung trading MCP"),
        ("telegram-native-ui", "st-live", "LIVE", "Button sebenar Telegram"),
        ("model-routing", "st-live", "LIVE", "DeepSeek primary + fallback"),
        ("image-prompt-enhancer", "st-live", "LIVE", "JSON enhancer + Pollinations"),
        ("screenshot-ocr-fallback", "st-live", "LIVE", "OCR bila vision tiada"),
        ("FUTURE: Shopee API", "st-off", "PLAN", "E-commerce — belum wujud (Liya)"),
        ("FUTURE: Finance/HR", "st-off", "PLAN", "Bajet & tunai — belum wujud (Aziz)"),
        ("FUTURE: WordPress", "st-off", "PLAN", "Website/theme — belum wujud"),
        ("FUTURE: Website parallax", "st-off", "PLAN", "Landing interaktif — belum wujud"),
    ]


def collect_deepseek_balance():
    """Baki DeepSeek real-time dari API /user/balance."""
    env_path = os.path.join(HERMES_HOME, ".env")
    key = ""
    if os.path.exists(env_path):
        m = re.search(r"^DEEPSEEK_API_KEY=(.+)$", open(env_path, errors="ignore").read(), re.M)
        if m:
            key = m.group(1).strip().strip('"').strip("'")
    if not key:
        return {"status": "tiada key", "total": None, "currency": None, "topped_up": None, "granted": None}
    try:
        r = subprocess.run(
            ["curl", "-s", "-m", "15", "https://api.deepseek.com/user/balance",
             "-H", f"Authorization: Bearer {key}"],
            capture_output=True, text=True, timeout=20)
        d = json.loads(r.stdout)
        if d.get("is_available") and d.get("balance_infos"):
            b = d["balance_infos"][0]
            return {
                "status": "ok",
                "total": b.get("total_balance"),
                "currency": b.get("currency"),
                "topped_up": b.get("topped_up_balance"),
                "granted": b.get("granted_balance"),
                "is_available": True,
            }
        return {"status": "error", "total": None, "raw": r.stdout[:120]}
    except Exception as e:
        return {"status": "error", "total": None, "raw": str(e)[:120]}


def collect_token_usage():
    """Token usage sebenar dari agent.log — aggregate purata & jumlah."""
    logp = os.path.join(HERMES_HOME, "logs", "agent.log")
    out = {"in_avg": "—", "out_avg": "—", "lat_avg": "—", "calls_total": 0,
           "in_total": 0, "out_total": 0, "est_cost_usd": None}
    if not os.path.exists(logp):
        return out
    ins, outs, lats = [], [], []
    try:
        with open(logp, errors="ignore") as f:
            for line in f:
                m = re.search(r"API call #\d+: model=\S+ provider=\S+ in=(\d+) out=(\d+) total=\d+ latency=([\d.]+)s", line)
                if m:
                    i, o, lat = int(m.group(1)), int(m.group(2)), float(m.group(3))
                    ins.append(i); outs.append(o); lats.append(lat)
    except Exception:
        pass
    if ins:
        out["calls_total"] = len(ins)
        out["in_total"] = sum(ins)
        out["out_total"] = sum(outs)
        out["in_avg"] = f"{sum(ins)//len(ins):,} tok"
        out["out_avg"] = f"{sum(outs)//len(outs):,} tok"
        out["lat_avg"] = f"{sum(lats)/len(lats):.1f}s"
        # Anggaran kos: v4-flash $0.14/1M in, $0.28/1M out (kira cache 95% input)
        est = (sum(ins) * 0.05 * 0.14 + sum(outs) * 0.28) / 1_000_000
        out["est_cost_usd"] = round(est, 4)
    return out


def collect_quick():
    out = {}
    # Gateway
    g = sh("systemctl --user is-active hermes-gateway 2>/dev/null || echo dead")
    out["gateway"] = "🟢 running" if g == "active" else f"🔴 {g}"
    # Telegram — gateway process hidup = bot polling aktif
    tg_status = "🔴 down"
    if sh("pgrep -f 'gateway run' | head -1"):
        tg_status = "🟢 connected (polling)"
    out["telegram"] = tg_status
    # Airtable
    at = os.getenv("AIRTABLE_API_KEY", "")
    out["airtable"] = "🟢 key ada" if at else "🔴 tiada key"
    # Moomoo
    out["moomoo"] = "🟡 belum connect (OpenD)"
    # MCP
    out["mcp"] = "🟢 exa" if sh("mcporter list 2>/dev/null | grep -c exa") else "🟡 ?"
    # Image
    out["image"] = "🟢 Pollinations + Gemini"
    return out


def main():
    data = {
        "generated_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "system": collect_system(),
        "services": collect_services(),
        "keys": collect_keys(),
        "model": collect_model(),
        "cron": collect_cron(),
        "calls": collect_calls(),
        "tools": collect_tools(),
        "skills": collect_skills(),
        "quick": collect_quick(),
        "deepseek_balance": collect_deepseek_balance(),
        "tokens": collect_token_usage(),
    }
    with open(OUT, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"stats.json dikemas ({data['generated_at']}) — {len(data['keys'])} keys, {len(data['services'])} services, {len(data['cron'])} cron")


if __name__ == "__main__":
    main()
