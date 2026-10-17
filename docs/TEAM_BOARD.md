---
title: TEAM_BOARD — STATISTICHEAI SPRINT 0-4
status: 🚀 SP RINT 1 IN PROGRESS
last_updated: 2026-10-15_12:00:00
owner: @gynbot1 (Coordinator)
---

## 👥 TEAM ASSIGNMENTS (Oct 15, 2026)

| Agent   | Role                  | Sprint(s)         | Current Task                                    | Blocker?  | Locked Files      |
|---------|-----------------------|-------------------|-------------------------------------------------|-----------|-------------------|
| @gynbot1 | Coordinator/Lead      | S0-S4+            | **S1:** Fix `run_server.py` bugs, start server testing   | No        | None              |
| @programmatore | Backend Executor  | S1                | Implement `/resurrect/<agent_id>` API + logging          | No        | —                 |
| @quality-cheker | QA/Tester        | S1-S4+            | Test endpoints, verify pixel art canvas rendering         | No        | —                 |

## 📦 ACTIVE TASKS & FILES

### 🔄 Currently In-Progress
| File                     | Sprint | Owner          | Current Fix Needed                           | Blocker? Date       |
|--------------------------|--------|----------------|---------------------------------------------|---------------------|
| `run_server.py`          | S1     | @gynbot1       | Path fixes, imports, indentation, stats API  | Yes (buggy code)   |
| `dashboard_clean.html`   | S2     | @programmatore | CSS vars, closed HTML tags, overlay activation   | No                 |
| `dashboard.html`         | S3     | @quality-cheker | Real polling JS, canvas avatar rendering          | No                 |

### 🆕 To Create/Update (Sprint 1 → 2+)
- ✅ `TEAM_BOARD.md` (now created)
- ⏳ `docs/INVENTARIO.md` — Update with fresh sprint 1 status (already exists)
- ⏳ `backups/readme.md` — Manual backup instructions
- ⏳ `test_resurrection.html` — Unit test UI endpoint

---

## 🧪 SP RINT 0 COMPLETE ✅

**Done:** Backup created, bug list documented.  
**Next:** @gynbot1 will fix `run_server.py` in-place, then start server & test endpoints.

### 🔧 Bug Fixes Checklist (`run_server.py`)
- [ ] Replace static Bash paths with `BASE_DIR = os.path.dirname(os.path.abspath(__file__))`
- [ ] Add `import random` at top
- [ ] Fix `if context_capacity <= 0` → `if capacity <= 0` in `get_context_fill_percent()`
- [ ] Fix regex line 221: extra closing paren in `calculate_token_usage_per_agent`
- [ ] Fix `/api/ps` → read `model.get('size_vram', 0)` (correct Ollama key)
- [ ] Insert `def do_PUT(self):` **INSIDE** `HStatServer` class (not indented too deep)
- [ ] Fix `do_GET` for `/`: serve `dashboard_clean.html` with `Content-Type: text/html; charset=utf-8`
- [ ] Fix Windows CPU/RAM props: use `FreePhysicalMemory` (KB), not `AvailableMemory`
- [ ] Remove `collect_real_ollama_stats(1)` call (wrong arg count)

### ✅ QA Endpoints (After S1 Fixes)
```bash
curl http://127.0.0.1:8081/
# → <html>...</html> dashboard_clean.html
curl http://127.0.0.1:8081/health
# → {"status": "healthy"}
curl http://127.0.0.1:8081/api/v1/stats/agents 
# → [] (empty array, to be populated)
curl http://127.0.0.1:8081/api/v1/ollama/stats
# → {"models": [{"name":"gryffindor-llam", "size_vram": 4...}}
curl http://127.0.0.1:8081/api/v1/system/resources
# → {"cpu": 25, "mem": 3000}
```

---

## 🗓️ SPRINT TIMELINE (Current Focus: Sprint 0 → 1)

| Sprint | Milestone                              | Deadline      | Blocker?    | Notes                      |
|--------|----------------------------------------|---------------|-------------|----------------------------|
| **S0** | Document + backup `run_server.py`      | ✅ Done       | No          | Inventory created          |
| **S1** | Fix backend: paths, imports, indentation | Oct 17?       | Yes         | Server won't start without fixes |
| **S2** | Fix CSS/HTML `dashboard_clean.html`    | Oct 18?       | No          | Pixel art overlay missing  |
| **S3** | Add real polling + canvas avatar JS     | Oct 19?       | No          | Mock fetch → live API      |
| **S4+**| Align with `FASE2_BRIEF.md` (UI polish) | Ongoing       | None        | Animations, metrics log   |

---

## 🚨 CRITICAL REMINDERS (From FASE2_BRIEF)

1.  **Cartella Isolata:** Tutti i file → SOLAMENTE in `STATISTICHEAI`. Fuori = sola lettura.
2.  **Resuscita:** L'azione passa dall'interfaccia ufficiale di Hermes. Non mai forzati a mano.
3.  **Dati Reali Solo:** Mai inventare numeri. N/D o "stima" con fonte.
4.  **127.0.0.1 ONLY:** Server locale, nessun internet runtime, CDN offline.
5.  **Nessuna Resurrezione Auto:** I pulsanti si testano su agente di prova (`gynbot1`).
6.  **Backup PRIMA:** `backups/` prima ogni modifica!

---

## 🎯 COORDINATOR NOTE (@gynbot1)

**Sprint 0 Complete.** Ready to execute bug fixes in `run_server.py`:
- All paths dynamic via `os.path.abspath(__file__)`
- Import random added
- Regex, stats API keys (size_vram), indentation (`do_PUT`) fixed
- Serve `/` with HTML file (proper headers)
- Windows resource props correct (FreePhysicalMemory in KB)
- No arg passed to `collect_real_ollama_stats()`

**Sprint 1 Goal:** Server starts clean, endpoints return real data.  
**Awaiting @programmatore feedback on backend API impl.**

---

*Generated by SPRINT 0 COMPLETE | Owner: @gynbot1 | Last Updated: 2026-10-15_12:00:00*
