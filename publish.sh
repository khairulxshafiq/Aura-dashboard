#!/bin/bash
# Publish AuraOne Dashboard ke GitHub Pages (repo: Aura-dashboard)
set -e
cd /home/ubuntu/aura-dashboard

echo "═══ 1. Buang repo lowercase (duplicate) ═══"
if gh repo view khairulxshafiq/aura-dashboard >/dev/null 2>&1; then
  gh repo delete khairulxshafiq/aura-dashboard --yes 2>&1 | tail -2
  echo "lowercase deleted"
else
  echo "lowercase tak wujud / dah buang"
fi

echo "═══ 2. Git identity ═══"
git config --global user.name  >/dev/null 2>&1 || git config --global user.name "Sakluma"
git config --global user.email >/dev/null 2>&1 || git config --global user.email "sales@saklomak.my"
echo "name: $(git config --global user.name) | email: $(git config --global user.email)"

echo "═══ 3. README ═══"
cat > README.md <<'EOF'
# AuraOne Dashboard

Personal AI Command Dashboard — one dashboard, five AI colleagues, infinite scaling.

Dibina untuk [Saklomak.my](https://saklomak.my).

## Kandungan
- `index.html` — dashboard utama (self-contained HTML/CSS/JS)
- `personas.json` — definisi 5 AI personas (News, Content, Trade, Commerce, Ops)

## Live
https://khairulxshafiq.github.io/Aura-dashboard/
EOF

echo "═══ 4. Init + commit ═══"
[ -d .git ] || git init -q
git add -A
git commit -q -m "feat: AuraOne dashboard v2 + personas" 2>&1 | tail -1 || echo "(commit dah ada, skip)"
git branch -M main

echo "═══ 5. Set remote + push ═══"
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/khairulxshafiq/Aura-dashboard.git
git push -u origin main 2>&1 | tail -4

echo "═══ 6. Enable GitHub Pages ═══"
gh api -X POST repos/khairulxshafiq/Aura-dashboard/pages \
  -f "source[branch]=main" -f "source[path]=/" 2>&1 | tail -3 || echo "(Pages mungkin dah aktif / perlu setup manual)"

echo "═══ SELESAI ═══"
echo "URL: https://khairulxshafiq.github.io/Aura-dashboard/"
