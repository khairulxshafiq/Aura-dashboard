# 📑 LAPORAN AUDIT & PELAN MERGE: AURA DASHBOARD
**Dokumen:** `MERGE_PLAN.md`  
**Sasaran:** Penyatuan Semua Halaman Dashboard ke Satu Single-Page App (`auraone.html`) dengan Hash-Router  
**Repositori:** `/home/ubuntu/aura-dashboard`  
**Tarikh Audit:** 17 September 2026  
**Status:** DRAFT SPEC & AUDIT LENGKAP (Sedia Untuk Semakan Boss Khairul)  
**Rujukan:** Chat `7833562484`, Mesej `4962` · Solopreneur Mission Control & Multi-Tenant SaaS  

---

## 1. Eksekutif & Objektif Utama

### 1.1 Matlamat Strategik
Repositori `aura-dashboard` kini mempunyai **6 fail HTML berbeza** yang dibina merentas fasa pembangunan (daripada prototype awal Ogos 2026 sehingga versi SaaS Multi-Tenant terkini). Keadaan ini menyebabkan pemecahan kod (*code fragmentation*), duplikasi data watak AI (*persona roster drift*), dan kebergantungan kepada binaan kompilasi Angular tanpa kod sumber (`main-UOVWRWIQ.js`).

**Objektif Merge:**
1. **Satu Fail Kanonikal (`auraone.html`):** Menggabungkan semua fungsi terbaik daripada 6 fail HTML ke dalam satu aplikasi web tunggal (SPA) berasaskan Vanilla JS + CSS Tokens moden tanpa memerlukan binaan kompilasi (*zero build step*).
2. **Hash-Router Berpusat:** Mengurus navigasi lancar antara halaman (`#/home`, `#/pricing`, `#/login`, `#/app`, `#/admin`, `#/intelligence`) dengan sokongan URL state dan deep-linking.
3. **Role-Based UI & Session Guard:** 
   - **Pengguna Biasa (`role: "user"`):** Melihat *Customer Workspace* — Pengurusan Ejen Bisnes, Penyambung API (*Connectors*), Profil Perdagangan Bursa (advise-only), Baki Kredit ⚡, dan Chat Simulator dwibahasa.
   - **Admin / Founder (`role: "admin"`):** Melihat *AuraOne Mission Control (`s-admin`)* — Telemetri Pelayan VPS masa nyata, Pemantauan Skuad 9 Ejen, Pengurusan Pengguna/Tenant, Lejar Kos & MRR, serta Senarai Tindakan HITL (Human-in-the-Loop).
4. **UI/UX Admin Console Redesign (Fasa Demo Statik):** Mereka bentuk semula konsol `s-admin` dengan susun atur Bento Grid berketumpatan tinggi (*high-density command deck*) menggunakan data statik demo sebelum disambungkan ke API produksi FastAPI/Supabase.

---

## 2. Audit Terperinci 6 Fail HTML

Berikut adalah audit menyeluruh terhadap setiap fail HTML yang terdapat dalam repositori `/home/ubuntu/aura-dashboard`:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                INVENTORI 6 FAIL HTML                                   │
├─────────────────────────┬──────────────┬───────────────┬───────────────────────────────┤
│ Fail                    │ Saiz (Bytes) │ Baris Kod     │ Peranan Semasa                │
├─────────────────────────┼──────────────┼───────────────┼───────────────────────────────┤
│ 1. auraone.html         │ 42,544 B     │ 733 baris     │ SaaS Multi-Tenant (Prototype) │
│ 2. dashboard.html       │ 27,476 B     │ 543 baris     │ System Consumption Telemetry  │
│ 3. intelligence.html    │ 72,911 B     │ 1,736 baris   │ Aura × Luma Audit Trace       │
│ 4. index.html           │ 11,568 B     │ 17 baris (SPA)│ Compiled Angular 19 Client    │
│ 5. index.v1.html        │ 41,963 B     │ 591 baris     │ Legacy Landing Page + Orb     │
│ 6. Aura Dashboard v1.html│ 21,674 B    │ 411 baris     │ Prototype Command Center v1   │
└─────────────────────────┴──────────────┴───────────────┴───────────────────────────────┘
```

---

### Fail 1: `auraone.html` (Baseline SaaS Multi-Tenant)
* **Saiz / Baris:** 42,544 Bytes / 733 Baris
* **Tujuan Asal:** Prototaip Single-Page App untuk produk SaaS pengguna awam dan pengurusan kredit berbilang penyewa.
* **Sections & Ciri Utama:**
  1. `nav`: Bar navigasi melekat (*sticky*) dengan Logo Gelung Aura (*Aura Ring*), baki kredit ⚡, butang Dashboard, Sign In/Out.
  2. `s-home` (`#/home`): Hero banner "Meet Aura", statistik ringkas (3 templat, 10+ penyambung), kad ciri (Agent Templates, Toggle Connectors, Trading Co-pilot), butang "See Aura in Action" (memaparkan demo chat interaktif di laman utama).
  3. `s-pricing` (`#/pricing`): 4 pelan langganan (Trial RM0, Starter RM19/bln, Pro RM49/bln, Top-Up RM10/200 kredit) berserta penafian risiko perdagangan (*disclaimer*).
  4. `s-login` (`#/login`): Borang log masuk berserta butang pantas demo (User: `demo@auraone.my`, Admin: `boss@auraone.my`), persetujuan PDPA/Syarat Perkhidmatan.
  5. `s-app` (`#/app` - User View): Dashboard pelanggan dengan kad baki kredit (260 ⚡), tab (My Agents, Connectors, Settings, Trading), senarai 3 ejen aktif (Content Marketing, Image Brand, Reminder & Report), suis togol penyambung (Telegram, GDrive, Dropbox, Sheets, FB Page, WA, Shopee, Gmail), tetapan persona bahasa, profil pelabur Bursa, dan ruang sembang AI dwibahasa (BM/EN).
  6. `s-admin` (`#/admin` - Admin View Asas): 4 kad statistik ringkas (Total users: 5, Active agents: 12, Credits used: 184, Est. MRR: RM68), jadual pengguna dengan togol Pause/Resume, pecahan kos pelayan (RM113), dan senarai semak Boss.
  7. `modals`: Modal tambah nilai kredit (ToyyibPay mock), modal kunci API (AES-256 encrypted placeholder), modal teks perundangan (Terms/PDPA).
  8. `script`: Enjin penghalaan hash (`route()`), sesi `localStorage` (`a1session`, `a1credits`, `a1conn`, `a1adm`), pengesanan kata kunci Bahasa Melayu (`isMalay()`), simulasi tolak kredit (-5 ⚡ per run).
* **Kelebihan:** Struktur SPA paling matang, mempunyai asas role-based authentication, pengurusan sesi `localStorage`, reka bentuk CSS moden dan responsif.
* **Kelemahan / Jurang:** Bahagian `s-admin` masih terlalu asas; tiada integrasi telemetri pelayan VPS (RAM/CPU/Disk/Cron) daripada `dashboard.html`, dan tiada paparan jejak kecerdasan (*execution trace*) daripada `intelligence.html`.

---

### Fail 2: `dashboard.html` (Sistem Consumption Telemetry)
* **Saiz / Baris:** 27,476 Bytes / 543 Baris
* **Tujuan Asal:** Konsol pemantauan dalaman untuk infrastruktur VPS, penggunaan API DeepSeek, proses sistem, dan kunci API.
* **Sections & Ciri Utama:**
  1. `pagehead`: Status "LIVE · auto-update" dengan pautan ke `intelligence.html`.
  2. `Metric King`: 4 kad KPI telemetri utama — Penggunaan RAM (MB & %), CPU Load %, Disk %, dan Uptime pelayan.
  3. `Trend Chart`: Graf garisan Canvas 60-hari untuk anggaran kos (USD), jumlah panggilan API, dan baki DeepSeek.
  4. `DeepSeek Balance Card`: Baki masa nyata daripada API DeepSeek, kiraan panggilan log, anggaran kos jimat (cache 95%), purata latensi.
  5. `Servis & Proses Table`: Pemantauan servis aktif (Gateway Telegram, Agent CLI, Moomoo OpenD Bridge) berserta PID, RAM, CPU.
  6. `API Keys Table`: Status kunci API bertopeng (*masked prefix*) dari `.env` (DeepSeek, OpenCode, Telegram, Cloudflare, Airtable).
  7. `Model & Routing`: Konfigurasi model utama (`deepseek-v4-flash`), fallback 1 (`gemini-2.5-flash`), fallback 2 (`llama-3.3-70b`), dan bar peratusan *prompt cache hit*.
  8. `Cron Jobs Table`: Jadual tugas berkala VPS (kutipan telemetri 15-min, semakan baki 1-jam, sandaran harian).
  9. `Tools & MCP Table`: Senarai 12+ alatan MCP yang disuntik (Exa search, Airtable, Moomoo, Filesystem, SQLite).
  10. `Skills Table`: Inventori keupayaan sistem (News scraper, Copywriter, Bursa Analyzer, FLUX LoRA).
  11. `Aktiviti & API Calls`: Bar token input/output, latensi, dan log panggilan sesi terkini.
  12. `Cepat Lihat (Quick Status)`: Status suis mini servis luaran (Gateway, Telegram, Airtable, Moomoo, Image Gen).
* **Kelebihan:** Visualisasi telemetri teknikal yang sangat kaya, ada logik parsing fail `stats.json` dan graf Canvas terbina dalam tanpa pustaka luar.
* **Kelemahan / Jurang:** Tiada kawalan capaian / auth (terbuka kepada sesiapa jika dihoskan awam), reka bentuk berorientasikan pemaju (*developer-centric*), tidak sesuai untuk pengguna biasa SaaS.

---

### Fail 3: `intelligence.html` (AuraOne × Luma Intelligence Audit)
* **Saiz / Baris:** 72,911 Bytes / 1,736 Baris
* **Tujuan Asal:** Laporan audit interaktif membuktikan tahap autonomi dan jejak pelaksanaan dwi-nod ejen (*Dual-Node Agent Network: Aura + Luma AGY*).
* **Sections & Ciri Utama:**
  1. `header`: Penjenamaan visual "AuraOne × Luma", lencana status siaran langsung.
  2. `Question Banner & Verdict`: Analisis persoalan teras ("Adakah Luma dipanggil oleh Aura atau jalan sendiri?") berserta kotak keputusan rasmi (*Autonomy Verdict: 95.7%*).
  3. `Stats Grid`: Jumlah langkah (585 steps), sesi perbualan (8 sessions), alatan unik (24 tools), penjimatan masa (42 jam).
  4. `Timeline of Execution Trace`: Jejak masa interaktif dengan penanda titik berwarna (User = Ungu, Luma = Biru Cyan, Tool = Emas) dan tag alatan (`run_command`, `read_file`, `write_to_file`, `grep_search`).
  5. `Tool Usage Distribution`: Carta bar taburan kekerapan penggunaan setiap tool MCP.
  6. `Conversation Inspector`: Senarai kad perbualan yang boleh diklik untuk memeriksa langkah, token, dan hasil setiap pusingan.
  7. `Dual-Node Flow Diagram`: Rajah aliran seni bina interaktif (Aura ReAct Planner → Luma Executor → Tool Execution Sandbox).
  8. `Performance & Token Analytics`: Metrik kecekapan token, agihan latensi, dan senarai fail artifak yang dimodifikasi.
* **Kelebihan:** Antara muka audit yang amat menarik, visual bertaraf tinggi (*cyber-dark aesthetic*), pembuktian autonomi yang komprehensif.
* **Kelemahan / Jurang:** Data sesi adalah statik (Ogos 2026), fail sangat panjang (1,736 baris) dengan CSS dan JSON data terbenam; perlu dimampatkan menjadi sub-modul paparan di dalam Mission Control Admin.

---

### Fail 4: `index.html` (Compiled Angular 19 SPA)
* **Saiz / Baris:** 11,568 Bytes (HTML) + 245,292 Bytes (`main-UOVWRWIQ.js`) + 19,587 Bytes (`styles-N2ZSMZOP.css`)
* **Tujuan Asal:** Antara muka web dibina dengan Angular 19 & Signals untuk menjadi portal rasmi.
* **Sections & Ciri Utama:**
  1. `app-navbar`: Navigasi jenama dengan pautan luaran.
  2. `hero-section`: "One Dashboard, Nine AI Colleagues, Infinite Autonomous Execution" untuk Saklomak.my.
  3. `quick-hub-grid`: Kad pintasan ke System Consumption (`dashboard.html`) dan Intelligence Audit (`intelligence.html`).
  4. `app-telemetry`: Kad ringkasan RAM, CPU, Uptime, panggilan API.
  5. `app-persona-grid`: Grid 9 rakan sekerja AI (*AI Colleagues roster*).
  6. `app-mcp-registry`: Registry alatan WebMCP.
  7. `app-live-console`: Konsol penstriman log pelaksanaan masa nyata.
* **Kelebihan:** Reka bentuk kad *Bento Grid* yang kemas dan profesional.
* **Kelemahan / Jurang:** **Tiada kod sumber (`src/app/`)** dalam repositori — hanya fail binari JS/CSS terkompilasi. Sebarang perubahan UI memerlukan kejuruteraan undur (*reverse engineering*). Sukar diselenggara. **Wajib digugurkan dan digantikan sepenuhnya oleh Vanilla JS dalam `auraone.html`.**

---

### Fail 5: `index.v1.html` (Original Static Landing Page)
* **Saiz / Baris:** 41,963 Bytes / 591 Baris
* **Tujuan Asal:** Halaman pendaratan (*landing page*) awal AuraOne dengan animasi sfera berputar (*Aura Orb*).
* **Sections & Ciri Utama:**
  1. `hero`: Salinan pemasaran berimpak tinggi, butang CTA, dan animasi CSS tulen `Aura Orb` (3 gelung berputar dengan teras bernafas).
  2. `tentang`: 6 tonggak nilai (Pantau & Lapor, Tulis & Terbit, Analisa & Alert, Cipta Visual, Automasi & Operasi, Kewangan & Revenue).
  3. `kemampuan`: Grid 9 kad keupayaan (Berita Trending, Kandungan Sosial, Trading Bursa, E-Commerce, Finance, WordPress, Automasi, Integrasi, Revenue Tracking) dengan lencana status `LIVE` vs `PLANNED`.
  4. `pasukan`: Grid 9 watak AI (Aura, Liya, Xiao, Amira, Maya, Aziz, Kumar, Akira, Alisa) berserta avatar, peranan, trigger command, dan status.
  5. `aliran`: Gambar rajah aliran kerja interaktif (`scrape` → `draft` → `confirm` → `airtable`).
  6. `terminal`: Emulator terminal interaktif meniru pelaksanaan arahan CLI Aura.
  7. `stats`: Metrik impak perniagaan (Artikel diproses, Draf dihantar, Automasi aktif, Masa dijimat).
* **Kelebihan:** Kandungan copywriting Bahasa Melayu yang sangat padu untuk perniagaan tempatan; animasi CSS `Aura Orb` dan kad *Pasukan 9 Ejen* sangat ikonik.
* **Kelemahan / Jurang:** Statik sepenuhnya, tiada log masuk, tiada sistem kredit, tiada fungsi interaktif sebenar selain animasi skrol.

---

### Fail 6: `Aura Dashboard v1.html` (Legacy Prototype Command Center)
* **Saiz / Baris:** 21,674 Bytes / 411 Baris
* **Tujuan Asal:** Prototaip papan pemuka eksekutif fasa konsep terawal (14 Ogos 2026).
* **Sections & Ciri Utama:**
  1. `hero`: Versi awal animasi Aura Orb dengan teks "Five AI colleagues".
  2. `colleagues`: Senarai 5 ejen awal (Sakluma News, Sakluma Content, AURA-Trade, Commerce, Ops).
  3. `metrics`: 4 kad metrik operasi.
  4. `inbox widget`: Widget peti masuk (Shopee order, Bursa watchlist, Trending berita, Telegram).
  5. `jadual widget`: Senarai semak tugasan harian mengikut masa (08:00 hingga 20:00).
  6. `workflow widget`: 3 aliran kerja visual mini.
  7. `activity feed`: Suapan aktiviti sistem mengikut cap masa.
  8. `watchlist widget`: Senarai saham Bursa (INARI, GENM, AEMULUS) berserta harga dan peratusan pergerakan.
* **Kelebihan:** Mempunyai idea widget *Inbox*, *Jadual Harian*, dan *Watchlist Saham* yang sangat intuitif untuk pengurusan bisnes solopreneur.
* **Kelemahan / Jurang:** Kod lapuk (*deprecated*), menggunakan senarai 5 watak lama (sebelum evolusi kepada 9 watak rasmi), statik tanpa interaktiviti dinamik.

---

## 3. Matriks Pertindihan & Analisis Overlap

```
┌─────────────────────────────┬─────────────┬─────────────┬─────────────┬─────────────┬─────────────┬─────────────┐
│ Ciri / Komponen             │ auraone.html│dashboard.html│intelligence │ index.html  │index.v1.html│Aura Dash v1 │
├─────────────────────────────┼─────────────┼─────────────┼─────────────┼─────────────┼─────────────┼─────────────┤
│ Top Navigation & Logo       │ ✅ (Moden)  │ ✅ (Kemas)  │ ✅ (Audit)  │ ⚠️ (Compiled)│ ✅ (Asas)   │ ✅ (Awal)   │
│ Aura Glowing Orb Animation  │ ❌ (Ring)   │ ❌          │ ❌ (Orbs)   │ ❌ (Orbs)   │ ✅ (Penuh)  │ ✅ (Penuh)  │
│ Landing / Hero Copy         │ ✅ (SaaS)   │ ❌          │ ❌          │ ⚠️ (Compiled)│ ✅ (Padu)   │ ⚠️ (5 Ejen) │
│ Pricing Plans (SaaS Model)  │ ✅ (4 Pelan)│ ❌          │ ❌          │ ❌          │ ❌          │ ❌          │
│ Auth / Demo Login & Session │ ✅ (Lengkap)│ ❌          │ ❌          │ ❌          │ ❌          │ ❌          │
│ Customer Agent Hub          │ ✅ (3 Ejen) │ ❌          │ ❌          │ ❌          │ ❌          │ ❌          │
│ API Connector Toggles (8)   │ ✅ (Moden)  │ ❌          │ ❌          │ ❌          │ ❌          │ ❌          │
│ Bursa Trading Co-Pilot      │ ✅ (Profile)│ ❌          │ ❌          │ ❌          │ ⚠️ (Kemampuan│ ✅ (Watchlist│
│ Interactive Chat Simulator  │ ✅ (BM/EN)  │ ❌          │ ❌          │ ❌          │ ❌          │ ❌          │
│ VPS Telemetry (RAM/CPU/Disk)│ ❌          │ ✅ (Live)   │ ❌          │ ⚠️ (Static) │ ❌          │ ❌          │
│ DeepSeek Balance & Token Met│ ❌          │ ✅ (Live)   │ ❌          │ ⚠️ (Static) │ ❌          │ ❌          │
│ API Key Status Table        │ ❌          │ ✅ (Masked) │ ❌          │ ❌          │ ❌          │ ❌          │
│ Process & Cron Monitoring   │ ❌          │ ✅ (Live)   │ ❌          │ ❌          │ ❌          │ ❌          │
│ Skuad 9 Watak AI (Roster)   │ ❌ (3 Ejen) │ ⚠️ (Skills) │ ❌          │ ⚠️ (Compiled)│ ✅ (9 Ejen) │ ⚠️ (5 Ejen) │
│ Execution Trace & Audit Log │ ❌          │ ❌          │ ✅ (585 stp)│ ❌          │ ❌          │ ❌          │
│ Dual-Node Network Diagram   │ ❌          │ ❌          │ ✅ (Interac)│ ❌          │ ⚠️ (Flow)   │ ⚠️ (Flow)   │
│ Terminal Simulator          │ ❌          │ ❌          │ ❌          │ ❌          │ ✅ (Live)   │ ❌          │
│ Business Task Checklist     │ ❌          │ ❌          │ ❌          │ ❌          │ ❌          │ ✅ (Jadual) │
│ Admin Mission Control UI    │ ⚠️ (Asas)   │ ✅ (Teknikal│ ⚠️ (Audit)  │ ❌          │ ❌          │ ⚠️ (Awal)   │
└─────────────────────────────┴─────────────┴─────────────┴─────────────┴─────────────┴─────────────┴─────────────┘
```

### Isu Utama Yang Dikesan:
1. **Pecahan Persona Roster:** `auraone.html` hanya menyenaraikan 3 ejen SaaS, `index.v1.html` ada 9 ejen lengkap, manakala `Aura Dashboard v1.html` masih menggunakan senarai 5 ejen lama.
2. **Ketiadaan Jambatan Antara SaaS & Telemetri Pelayan:** Pengguna SaaS memerlukan paparan bersih tanpa istilah teknikal pelayan, manakala Admin (Boss Khairul) memerlukan data penggunaan RAM, baki DeepSeek, log cron, dan status kunci API dalam konsol yang sama.
3. **Penyebaran Data Trading:** Analisis saham Bursa bertaburan antara borang profil di `auraone.html`, jadual watchlist statik di `Aura Dashboard v1.html`, dan keupayaan Moomoo di `dashboard.html`.

---

## 4. Pelan Merge Berstruktur (File → Section → Action)

Jadual berikut memperincikan tindakan bagi setiap komponen merentas 6 fail untuk digabungkan ke dalam `auraone.html`:

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                       PELAN TINDAKAN MERGE SETIAP SEKSYEN                                             │
├──────────────────────┬─────────────────────────┬─────────┬──────────────────────────┬─────────────────────────────────┤
│ Fail Asal            │ Seksyen / Komponen      │ Tindakan│ Sasaran di auraone.html  │ Rasional & Catatan Teknikal     │
├──────────────────────┼─────────────────────────┼─────────┼──────────────────────────┼─────────────────────────────────┤
│ auraone.html         │ Sticky Nav + Hash Router│ KEEP    │ `nav`, `router()`        │ Asas penghalaan SPA sedia ada.  │
│ auraone.html         │ Hero SaaS Landing       │ MERGE   │ `s-home`                 │ Gabung dgn Aura Orb index.v1.   │
│ auraone.html         │ Pricing Grid (4 Plans)  │ KEEP    │ `s-pricing`              │ Model harga SaaS sedia untuk go.│
│ auraone.html         │ Auth & Demo Switcher    │ KEEP    │ `s-login`                │ Asas role routing (user/admin). │
│ auraone.html         │ Customer App Deck       │ KEEP    │ `s-app` (Role: user)     │ Workspace pelanggan SaaS.       │
│ auraone.html         │ Connector Toggle Hub    │ KEEP    │ `pane-connect`           │ Interaksi togol API key moden.  │
│ auraone.html         │ Trading Profile Quiz    │ MERGE   │ `pane-trading`           │ Gabung dgn watchlist Bursa v1.  │
│ auraone.html         │ Bilingual Chat Mock     │ KEEP    │ `chatWrap`               │ Regex pengesanan Bahasa Melayu. │
│ auraone.html         │ Admin Console Asas      │ UPGRADE │ `s-admin` (Role: admin)  │ Rombak ke Mission Control penuh.│
├──────────────────────┼─────────────────────────┼─────────┼──────────────────────────┼─────────────────────────────────┤
│ dashboard.html       │ Metric King (RAM/CPU/Up)│ MERGE   │ `s-admin` -> Telemetry   │ Masukkan ke Admin Bento Grid.   │
│ dashboard.html       │ DeepSeek Balance Card   │ MERGE   │ `s-admin` -> API Lejar   │ Pantau baki modal API Boss.     │
│ dashboard.html       │ 60-Day Trend Chart      │ MERGE   │ `s-admin` -> Analytics   │ Graf Canvas ringan tanpa CDN.   │
│ dashboard.html       │ Servis & PID Table      │ MERGE   │ `s-admin` -> Sys Health  │ Pantau gateway/bot/bridge VPS.  │
│ dashboard.html       │ API Keys Masked Table   │ MERGE   │ `s-admin` -> Security    │ Status kunci aktif/backup.      │
│ dashboard.html       │ Model & Routing + Cache │ MERGE   │ `s-admin` -> LLM Ops     │ Info fallback & cache prompt.   │
│ dashboard.html       │ Cron Jobs Table         │ MERGE   │ `s-admin` -> Automation │ Status jadual automatik VPS.    │
│ dashboard.html       │ Tools & MCP Table       │ MERGE   │ `s-admin` -> MCP Hub     │ Inventori keupayaan internal.   │
│ dashboard.html       │ Injected Skills Table   │ MERGE   │ `s-admin` -> Skills      │ Status kemahiran ejen aktif.    │
│ dashboard.html       │ Recent API Calls Stream │ MERGE   │ `s-admin` -> Audit Log   │ Log aktiviti token terkini.     │
├──────────────────────┼─────────────────────────┼─────────┼──────────────────────────┼─────────────────────────────────┤
│ intelligence.html    │ Autonomy Verdict Card   │ MERGE   │ `s-admin` -> Intel Tab   │ Bukti autonomi 95.7% Dual-Node. │
│ intelligence.html    │ Execution Trace Timeline│ MERGE   │ `s-admin` -> Intel Tab   │ Jejak masa alatan Luma/Aura.    │
│ intelligence.html    │ Tool Usage Bar Chart    │ MERGE   │ `s-admin` -> Intel Tab   │ Taburan kekerapan tool MCP.     │
│ intelligence.html    │ Dual-Node Flow Diagram  │ MERGE   │ `s-home` & `s-admin`     │ Visual interaktif arkitektur.   │
│ intelligence.html    │ Conversation Inspector  │ DROP    │ —                        │ Terlalu berat (pindah ke docs). │
├──────────────────────┼─────────────────────────┼─────────┼──────────────────────────┼─────────────────────────────────┤
│ index.html (Angular) │ Compiled JS Bundle      │ DROP    │ —                        │ Gugurkan fail binari 245KB.     │
│ index.html (Angular) │ Bento Grid CSS Layout   │ MERGE   │ `s-admin` CSS            │ Ambil inspirasi susun atur grid.│
├──────────────────────┼─────────────────────────┼─────────┼──────────────────────────┼─────────────────────────────────┤
│ index.v1.html        │ Glowing Aura Orb (CSS)  │ MERGE   │ `s-home` (Hero)          │ Animasi teras visual Aura.      │
│ index.v1.html        │ Skuad 9 Ejen (Roster)   │ MERGE   │ `s-home` & `s-admin`     │ Senarai kanonikal 9 persona.    │
│ index.v1.html        │ 6 Point "Tentang"       │ MERGE   │ `s-home`                 │ Copywriting padu pasaran tempatan│
│ index.v1.html        │ 9 Kad Keupayaan         │ MERGE   │ `s-home` (Kemampuan)     │ Penerangan servis perniagaan.   │
│ index.v1.html        │ Terminal Simulator      │ DROP    │ —                        │ Digantikan oleh Chat Simulator. │
├──────────────────────┼─────────────────────────┼─────────┼──────────────────────────┼─────────────────────────────────┤
│ Aura Dashboard v1    │ Daily Schedule Checklist│ MERGE   │ `s-admin` -> HITL Hub    │ Checklist tugasan harian Boss.  │
│ Aura Dashboard v1    │ Bursa Watchlist Cards   │ MERGE   │ `s-app` (Trading Tab)    │ Kad watchlist saham Bursa.      │
│ Aura Dashboard v1    │ 5 Legacy Colleagues     │ DROP    │ —                        │ Lapuk (guna 9 persona baharu).  │
│ Aura Dashboard v1    │ Inbox Mock Widget       │ DROP    │ —                        │ Duplikasi aktiviti feed.        │
└──────────────────────┴─────────────────────────┴─────────┴──────────────────────────┴─────────────────────────────────┤
```

---

## 5. Spesifikasi Reka Bentuk Semula `s-admin` (Admin Mission Control)

Bahagian `s-admin` di dalam `auraone.html` akan dinaik taraf daripada sekadar jadual ringkas kepada **AuraOne Mission Control Center** yang lengkap untuk kegunaan Boss Khairul.

### 5.1 Falsafah UI/UX & Prinsip Reka Bentuk
1. **Dark Cyber-Deck Theme:** Menggunakan palet gelap mewah (`--bg: #0b0e14`, `--surface: #11141c`, `--border: #232838`) dengan aksen Emas (`#f4b860`), Hijau Neon (`#4ade80`), Biru Luma (`#00d4ff`), dan Ungu Aura (`#a78bfa`).
2. **Bento Grid Berketumpatan Tinggi:** Memaksimumkan maklumat atas satu skrin (*high density, glanceable information*) tanpa perlu skrol yang berlebihan.
3. **Data Demo Statik Terkawal:** Semua metrik menggunakan objek data JavaScript statik (`ADM_CONFIG`, `ADM_TELEMETRY`, `ADM_USERS`, `ADM_FLEET`) yang bersedia disambungkan ke API produksi FastAPI `/api/v1/admin/*` kemudian hari.

---

### 5.2 Lakaran Susun Atur Skrin `s-admin` (Wireframe Spec)

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│ 🛡️ AURAONE MISSION CONTROL (BOSS COMMAND DECK)                          [🔴 Live Ops] [Khairul]  │
├──────────────────────────────────────────────────────────────────────────────────────────────────┤
│ [1. STRIP METRIK UTAMA (4 KPI KING)]                                                             │
│ ┌───────────────┐ ┌───────────────┐ ┌─────────────────────────┐ ┌──────────────────────────────┐ │
│ │ 👥 Total Users │ │ 🤖 AI Fleet   │ │ 💰 Anggaran MRR         │ │ ⚡ DeepSeek API Balance      │ │
│ │  5 Penyewa    │ │  9/9 Online   │ │  RM 117 / bln           │ │  $14.82 (Jimat 95% Cache)    │ │
│ │  (4 Aktif)    │ │  (100% Sihat) │ │  ▲ +18% MoM             │ │  ~184k Token Digunakan       │ │
│ └───────────────┘ └───────────────┘ └─────────────────────────┘ └──────────────────────────────┘ │
├──────────────────────────────────────────────────────────────────────────────────────────────────┤
│ [TAB NAVIGASI ADMIN]: [📌 Ringkasan Eksekutif] [👥 Pengurusan User] [🖥️ Telemetri Pelayan]       │
│                       [🤖 Skuad 9 Ejen] [⚡ Intelligence Audit] [ lejar Kos & HITL]              │
├──────────────────────────────────────────────────┬───────────────────────────────────────────────┤
│ PANEL KIRI (2/3 Grid):                           │ PANEL KANAN (1/3 Grid):                       │
│ ──────────────────────────────────────────────── │ ───────────────────────────────────────────── │
│ 👥 PENGURUSAN PENGGUNA & TENANT                  │ 🖥️ KESIHATAN SISTEM & INFRA (VPS 2GB)         │
│ • Carian: [ Cari user / email... ]               │ • RAM: [████████░░░░░░░] 48% (945MB / 1.96GB) │
│ • Jadual Pengguna:                               │ • CPU: [██░░░░░░░░░░░░░] 5.0% (Load: 0.10)   │
│   - Ai Rina (rina@demo.my) | Starter | 118 ⚡    │ • Disk: [██████░░░░░░░░] 39% (17GB Free)      │
│     [Status: Aktif] [Butang: Pause] [Top-Up]     │ • Uptime: 7 Hari 13 Jam 30 Minit              │
│   - Zul Hairom (zul@demo.my) | Pro | 96 ⚡       │ ───────────────────────────────────────────── │
│     [Status: Aktif] [Butang: Pause] [Top-Up]     │ ⚙️ STATUS PROSES & GATEWAY                     │
│   - Faiz Reworks (faiz@demo.my) | Starter        │ • Telegram Gateway (PID 2115926) : 🟢 Running │
│     [Status: Paused] [Butang: Resume]            │ • Moomoo Bridge   (PID 27104)   : 🟢 Running │
│   - Mak Cik Timah (maktimah@demo.my) | Trial     │ • Cron Telemetry (15-min)       : 🟢 Active  │
│ ──────────────────────────────────────────────── │ ───────────────────────────────────────────── │
│ 🤖 SKUAD 9 EJEN & STATUS CAPABILITY              │ 💸 LEJAR KOS & MARGIN BULANAN                 │
│ • Aura (Swarm Lead)      : 🟢 Ready (ReAct Loop) │ • TradingView Essential : RM 61.00            │
│ • Adrian (News Trend)    : 🟢 Ready (RSS+Trends) │ • VPS Hosting (2GB RAM) : RM 40.00            │
│ • Xiao (Copywriting)     : 🟢 Ready (5 Personas) │ • Supabase DB & Auth    : RM  0.00 (Free Tier)│
│ • Amira (Bursa Trading)  : 🟢 Ready (Asri Method)│ • Jumlah Kos Operasi    : RM 101.00           │
│ • Kumar (Visual Creator) : 🟢 Ready (FLUX LoRA)  │ • Est. Pendapatan (MRR) : RM 117.00           │
│ • Maya (Automation/Ops)  : 🟢 Ready (Cron/Backup)│ • Net Margin Operasi    : + RM 16.00 (Untung) │
│ • Akira (Revenue Track)  : 🟢 Ready (P&L Ledger) │ ───────────────────────────────────────────── │
│ • Liya (Sales WA)        : 🟡 Plan (Next Sprint) │ 📌 SENARAI TINDAKAN HITL (BOSS APPROVALS)     │
│ • Aziz (Finance/Budget)  : 🟡 Plan (Next Sprint) │ [ ] Beli Domain `auraone.my` & Point DNS      │
│ ──────────────────────────────────────────────── │ [ ] Daftar Akaun ToyyibPay (Live Payment)     │
│ ⚡ INTELLIGENCE & AUTONOMY SNAPSHOT              │ [ ] Sambung MT5 Broker untuk Data Real-time   │
│ • Autonomy Score: 95.7% (Dual-Node Aura × Luma)  │ [ ] Pengesahan Pendaftaran PDPA (JPDP)        │
│ • Tool Execution: 585 runs tanpa halangan        │                                               │
└──────────────────────────────────────────────────┴───────────────────────────────────────────────┘
```

---

### 5.3 Spesifikasi Data Statik Demo (`s-admin`)

Struktur objek data yang akan dimasukkan ke dalam blok `<script>` `auraone.html`:

```javascript
/* ---------- DATA STATIK DEMO: AURAONE MISSION CONTROL ---------- */
const ADM_DATA = {
  kpi: {
    total_users: 5,
    active_users: 4,
    active_agents: 9,
    total_agents: 9,
    mrr_myr: 117,
    mrr_growth_pct: "+18%",
    deepseek_balance_usd: 14.82,
    credits_used_month: 184,
    cache_hit_pct: 95.2
  },
  system_telemetry: {
    ram: { used_mb: 945, total_mb: 1967, pct: 48.0 },
    cpu: { pct: 5.0, load: "0.10 0.08 0.20" },
    disk: { used_pct: 39.0, free_gb: 17.2 },
    uptime: "7h 13j 30m",
    generated_at: "2026-09-17 12:30:00 (Demo Mode)"
  },
  services: [
    { name: "Telegram Gateway", status: "running", pid: 2115926, mem: "309MB", cpu: "0.5%" },
    { name: "Agent Runner Pool", status: "running", pid: 2699608, mem: "120MB", cpu: "0.2%" },
    { name: "Moomoo OpenD Bridge", status: "running", pid: 27104, mem: "92MB", cpu: "0.4%" },
    { name: "Cron Scheduler", status: "active", pid: "systemd", mem: "14MB", cpu: "0.0%" }
  ],
  users: [
    { id: "usr_01", name: "Ai Rina", email: "rina@demo.my", plan: "Starter", credits_used: 118, credits_bal: 182, status: "active", joined: "2026-09-01" },
    { id: "usr_02", name: "Zul Hairom", email: "zul@demo.my", plan: "Pro", credits_used: 96, credits_bal: 904, status: "active", joined: "2026-09-03" },
    { id: "usr_03", name: "Mak Cik Timah", email: "maktimah@demo.my", plan: "Trial", credits_used: 8, credits_bal: 12, status: "active", joined: "2026-09-14" },
    { id: "usr_04", name: "Faiz Reworks", email: "faiz@demo.my", plan: "Starter", credits_used: 172, credits_bal: 128, status: "paused", joined: "2026-08-28" },
    { id: "usr_05", name: "Boss Khairul", email: "boss@auraone.my", plan: "Pro (Owner)", credits_used: 40, credits_bal: 9999, status: "active", joined: "2026-08-01" }
  ],
  fleet_roster: [
    { name: "Aura", role: "Swarm Lead & Orchestrator", status: "live", tech_maturity: 95, ux_maturity: 92 },
    { name: "Adrian", role: "News & Social Intelligence", status: "live", tech_maturity: 92, ux_maturity: 90 },
    { name: "Xiao", role: "Copywriting & Marketing", status: "live", tech_maturity: 90, ux_maturity: 89 },
    { name: "Amira", role: "Bursa Stock Co-Pilot", status: "live", tech_maturity: 88, ux_maturity: 88 },
    { name: "Kumar", role: "Visual & LoRA Creator", status: "live", tech_maturity: 94, ux_maturity: 91 },
    { name: "Maya", role: "Operations & Automation", status: "live", tech_maturity: 92, ux_maturity: 90 },
    { name: "Akira", role: "Revenue & P&L Tracker", status: "live", tech_maturity: 85, ux_maturity: 84 },
    { name: "Liya", role: "WhatsApp Sales Closer", status: "planned", tech_maturity: 40, ux_maturity: 35 },
    { name: "Aziz", role: "Corporate Finance & Tax", status: "planned", tech_maturity: 30, ux_maturity: 25 }
  ],
  cost_breakdown: [
    { item: "TradingView Essential", cost_myr: 61.00, type: "Data Feed" },
    { item: "VPS Hosting (Hermes 2GB)", cost_myr: 40.00, type: "Infrastructure" },
    { item: "Supabase DB & Auth", cost_myr: 0.00, type: "Free Tier" },
    { item: "Domain DNS & SSL", cost_myr: 0.00, type: "Cloudflare Free" }
  ],
  hitl_checklist: [
    { task: "Beli Domain auraone.my & Point DNS", status: "pending", priority: "HIGH" },
    { task: "Daftar Akaun ToyyibPay (Live Payments)", status: "pending", priority: "HIGH" },
    { task: "Integrasi MT5 Broker untuk Feed Bursa", status: "pending", priority: "MEDIUM" },
    { task: "Pendaftaran Akta JPDP / PDPA Malaysia", status: "pending", priority: "MEDIUM" }
  ]
};
```

---

## 6. Seni Bina Penghalaan & Pengasingan Peranan (Role-Based Routing)

### 6.1 Peta Laluan Hash (Hash-Router Routes)
Aplikasi tunggal `auraone.html` akan memproses perubahan hash menerusi acara `window.onhashchange`:

```
┌─────────────────┬────────────────────────────────┬────────────────────────────┬────────────────────────┐
│ Hash Route      │ Nama Skrin                     │ Akses / Kebenaran          │ Sifat Paparan          │
├─────────────────┼────────────────────────────────┼────────────────────────────┼────────────────────────┤
│ `#/home`        │ Laman Utama / Pendaratan       │ Awam (Semua)               │ Hero + Orb + Skuad 9   │
│ `#/pricing`     │ Jadual Pelan & Langganan       │ Awam (Semua)               │ 4 Pelan Harga + Topup  │
│ `#/login`       │ Borang Log Masuk / Tukar Peran │ Awam (Semua)               │ Demo Account Switcher  │
│ `#/app`         │ Customer Workspace             │ Authenticated (`user`/`adm`)│ Ejen, Connectors, Chat │
│ `#/admin`       │ Mission Control Console        │ **Khusus Role `admin`**    │ Telemetri, Fleet, Lejar│
│ `#/intelligence`│ Laporan Audit Autonomi         │ Authenticated (`admin`)    │ Jejak Aliran Dwi-Nod   │
└─────────────────┴────────────────────────────────┴────────────────────────────┴────────────────────────┘
```

### 6.2 Logik Guard Peranan (Role Guard Flowchart)

```
[ Pengguna tukar URL / Klik pautan ]
                 │
                 ▼
          Semak Hash Route
                 │
      ┌──────────┴──────────┐
      ▼                     ▼
[ Halaman Awam ]     [ Halaman Terkawal ]
(#/home, #/pricing)  (#/app, #/admin, #/intelligence)
      │                     │
      ▼                     ▼
 Paparkan Skrin      Ada Sesi Aktif?
                      (localStorage)
                            │
               ┌────────────┴────────────┐
               ▼                         ▼
            [ Tiada ]                 [ Ada ]
               │                         │
               ▼                         ▼
       Redirect ke `#/login`       Semak Peranan User
                                         │
                           ┌─────────────┴─────────────┐
                           ▼                           ▼
                    [ role: "user" ]           [ role: "admin" ]
                           │                           │
                   Cuba akses `#/admin`?        Akses Penuh Ke
                           │                    Semua Bahagian
                   ┌───────┴───────┐                   │
                   ▼               ▼                   ▼
                [ Ya ]          [ Tidak ]        Paparkan Skrin
                   │               │             Admin / Workspace
                   ▼               ▼
           Redirect ke `#/app`  Paparkan `#/app`
           (Akses Ditolak)
```

---

## 7. Pelan Tindakan Pelaksanaan (Action Plan)

Kerja-kerja pelaksanaan sebenar boleh dimulakan sebaik sahaja laporan audit ini dipersetujui oleh Boss Khairul mengikut fasa berikut:

1. **Fasa 1: Penyediaan Kerangka Tunggal `auraone.html`**
   - Mengemaskini sistem reka bentuk CSS tokens di dalam `auraone.html` agar menyerap gaya *Bento Grid* gelap.
   - Menyerap animasi CSS `Aura Orb` daripada `index.v1.html` ke dalam seksyen `s-home`.
   - Mengemaskini seksyen pengenalan untuk memaparkan Skuad 9 Persona yang kanonikal.

2. **Fasa 2: Pembinaan Semula Skrin `s-admin` (Mission Control)**
   - Menghapuskan jadual admin asas lama di `s-admin`.
   - Membina Bento Grid baharu berpandukan lakaran Seksyen 5.2.
   - Menyuntik objek data statik `ADM_DATA` bagi memaparkan telemetri, armada ejen, lejar kewangan, dan senarai HITL.
   - Memasukkan graf Canvas 60-hari daripada `dashboard.html`.

3. **Fasa 3: Penambahbaikan Customer Workspace (`s-app`)**
   - Menyelaraskan tab Bursa Trading dengan paparan watchlist saham yang lebih interaktif.
   - Memastikan togol 8 penyambung API berfungsi dengan simpanan `localStorage`.
   - Memperhalusi simulator sembang dwibahasa (BM/EN).

4. **Fasa 4: Pembersihan Repositori & Sanitasi Fail**
   - Menyahdayakan fail lapuk (`index.v1.html`, `Aura Dashboard v1.html`, `dashboard.html.bak_v2`).
   - Menggantikan `index.html` dengan fail `auraone.html` yang telah siap (atau symlink / direct publish).
   - Memastikan tiada kunci rahsia terdedah dalam kod sumber.

---

## 8. Ringkasan & Langkah Seterusnya

Dokumen ini merumuskan pelan penggabungan 6 fail kepada satu SPA berkuasa penuh. Tiada fail teras yang dipadamkan secara melulu sebelum integrasi disahkan dalam prototaip tunggal.

*Laporan ini disimpan di `/home/ubuntu/aura-dashboard/docs/MERGE_PLAN.md`.*
