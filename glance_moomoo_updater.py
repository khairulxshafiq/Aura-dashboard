#!/usr/bin/env python3
"""
Glance Widget Stock Position Updater for Moomoo / AuraOne.
Converts Moomoo stock portfolio positions into an elegant iOS Glance Widget payload.
"""

import json
import requests
import datetime

# Glance API Credentials (loaded from environment)
FEED_ID = os.getenv("GLANCE_FEED_ID", "")
WRITE_KEY = os.getenv("GLANCE_WRITE_KEY", "")
LAYOUT_ID = os.getenv("GLANCE_LAYOUT_ID", "a8284d6e-3ff9-4fb4-aa51-ad8f65d51071")
INGEST_URL = f"https://glance-api.fly.dev/ingest/{FEED_ID}" if FEED_ID else ""

def format_elegant_payload(portfolio_summary, positions):
    """
    Format portfolio and position data into an ultra-elegant, readable Glance widget text.
    """
    total_val = portfolio_summary.get("total_value", 0.0)
    unrealized_pnl = portfolio_summary.get("pnl", 0.0)
    unrealized_pnl_pct = portfolio_summary.get("pnl_pct", 0.0)
    
    # Status emoji & color badge indicator
    if unrealized_pnl > 0:
        pnl_badge = f"🟢 +${unrealized_pnl:,.2f} (+{unrealized_pnl_pct:.2f}%)"
        headline = f"📈 PORTFOLIO | +{unrealized_pnl_pct:.1f}%"
    elif unrealized_pnl < 0:
        pnl_badge = f"🔴 -${abs(unrealized_pnl):,.2f} ({unrealized_pnl_pct:.2f}%)"
        headline = f"📉 PORTFOLIO | {unrealized_pnl_pct:.1f}%"
    else:
        pnl_badge = f"⚪ ${unrealized_pnl:,.2f} (0.00%)"
        headline = "⚖️ PORTFOLIO | EVEN"

    # Build top positions text
    pos_lines = []
    for pos in positions[:3]:  # Top 3 positions for widget size constraint
        code = pos.get("code", "STK")
        last = pos.get("last_price", 0.0)
        pnl = pos.get("pnl", 0.0)
        pnl_pct = pos.get("pnl_pct", 0.0)
        icon = "🟢" if pnl >= 0 else "🔴"
        pos_lines.append(f"{icon} {code}: ${last:.2f} ({'+' if pnl>=0 else ''}{pnl_pct:.1f}%)")
    
    pos_summary = "\n".join(pos_lines) if pos_lines else "No active positions"
    
    time_str = datetime.datetime.now().strftime("%I:%M %p")
    
    # Combined elegant content layout
    payload = {
        "schema_type": "dynamic",
        "template_id": LAYOUT_ID,
        "content": {
            "headline": headline,
            "subheadline": pnl_badge,
            "body": pos_summary,
            "footer": f"Updated {time_str} • Moomoo OpenD",
            # Flexible key backups matching common Glance layout bindings
            "title": headline,
            "status": pnl_badge,
            "positions": pos_summary,
            "timestamp": time_str
        },
        "intent": {
            "update_widget": True
        }
    }
    return payload

def push_to_glance(payload, dry_run=False):
    """Push formatted payload to Glance Ingest API."""
    headers = {
        "Authorization": f"Bearer {WRITE_KEY}",
        "Content-Type": "application/json"
    }
    
    if dry_run:
        print("[DRY RUN] Payload to be sent:")
        print(json.dumps(payload, indent=2))
        return None

    response = requests.post(INGEST_URL, headers=headers, json=payload, timeout=10)
    return response.json()

if __name__ == "__main__":
    # Sample position data for testing
    sample_portfolio = {
        "total_value": 15420.50,
        "pnl": 680.20,
        "pnl_pct": 4.61
    }
    sample_positions = [
        {"code": "NVDA", "last_price": 128.50, "pnl": 450.00, "pnl_pct": 8.2},
        {"code": "TSLA", "last_price": 215.30, "pnl": 280.20, "pnl_pct": 5.4},
        {"code": "AAPL", "last_price": 224.10, "pnl": -50.00, "pnl_pct": -1.1}
    ]
    
    payload = format_elegant_payload(sample_portfolio, sample_positions)
    print("Generated Elegant Payload:")
    print(json.dumps(payload, indent=2))
