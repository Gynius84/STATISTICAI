# TEAM BOARD — STATISTICHEAI | FASE 2 WORK SPLIT

**Ultimo Aggiornamento:** 14/10/2026  
**Stato Sessione:** ACTIVE • FASE 2: SALUTE + RESURREZIONE  

---

## 📋 TASK ASSIGNMENT (Team Split)

| Member        | Role                | Assigned Work                              | Priority   | File/Component     |
|---------------|---------------------|-------------------------------------------|------------|--------------------|
| **@gynbot1** | Leadership          | Impelment "Resuscita!" pulse + backend API | P0 (MAX)   | `run_server.py`, `dashboard.html` |
| **@programmatore** | Backend/Executor  | Logging + backup full endpoints POST/GET | P1         | `backups/`, `resurrezioni.jsonl` |
| **@quality-cheker** | QA                 | Manual UI test + validation               | P2         | `test_resurrection.html` (create) |

---

## 🔒 LOCKS / FILE STATUS

| File                          | Status | Owner   | Locked Until    |
|-------------------------------|--------|---------|-----------------|
| `run_server.py`               | 🔒 LOCKED | @gynbot1 | Until completion + testing |
| `dashboard.html`              | 🔒 LOCKED | @gynbot1 | Until completion + testing |
| `backups/`                    | ⚪ CREAT  | @programmatore | — |
| `data/resurrezioni.jsonl`     | ⚪ CREAT  | @programmatore | — |

**Legend:** 🔒 LOCKED = in-progress (write-lock active)  
⚪ CREAT = to be created  

---

## 📌 DECISIONS & NOTES

### P1.1: Resurrezione vs Reset Sessione
- **Decisione:** L3 resurrezione → backup sessione + reset contesto  
- **Rischio:** Non mai reset senza backup (L2 esporto) prima dell'azione  
  
### P1.2: Pulsante Solo >95% Saturato
- **Decisione:** Button visibile SOLO quando `ctxPct > 95%` nel frontend  
- **Anti-Risk:** Blocca doppio click, dry-run mode  

---

## 📝 STEP-BY-STEP (Current Priority)

### Step 1: Implement Backend API Endpoint `/resurrect/<id>`
**Owner:** @gynbot1  
**Status:** IN PROGRESS  
**Files:** `run_server.py` lines 476+ add new method  

**To do:**
- Add API endpoint POST/GET `/resurrect/<agent_id>` in `HStatServer.do_POST()` (around line 349)
- Backup state before resetting (`backup = AGENTS_DATA[agent_id].copy()`)
- Log to `data/resurrezioni.jsonl`  
**Done?** — No | Done by ? — Not started  

---

### Step 2: Add UI Pulsante + Warning Box in Dashboard
**Owner:** @gynbot1  
**Status:** PENDING  
**Files:** `dashboard.html` (add resurrect button logic)  

**To do:**
- Add modal anteprima prima di action  
- Button visible only when >95% sat  
- Call API on click with confirmation  

---

### Step 3: Create Logging & Backup in `backups/`
**Owner:** @programmatore  
**Status:** PENDING  

**To do:**
- Create directory `C:/.../STATISTICHEAI/backups/`  
- Write Python script to backup `data/*.json` files  
- Start logging in `resurrezioni.jsonl`  

---

### Step 4: Manual Test UI + Log Verification
**Owner:** @quality-cheker  
**Status:** PENDING  

**To do:**
- Open `dashboard.html`, trigger >95% sat, click resurrect  
- Confirm backup file created in `backups/`  
- Check log entries in `resurrezioni.jsonl`  

---

## 📊 PROGRESS TRACKING (Today)

| Member       | Done %  | Current Task                           | Blocker?    |
|--------------|---------|----------------------------------------|-------------|
| @gynbot1     | ~30%    | Backend `/resurrect/` endpoint + UI   | N/A         |
| @programmatore | 0%    | Create `backups/` dir + logs           | N/A         |
| @quality-cheker | 0%   | Manual testing                          | Waiting code |

**Next Meeting (simulated):** When all owners report test results  

---

## 🔄 DEPENDENCIES & HANDOFFS

- **Backend API must work before QA testing** → `@programmatore` + `@gynbot1`
- **UI button logic requires backend endpoint ready** → Depends on `/resurrect/` POST returning 200 OK  
- **Logs verified after backup script created** → Depends on `data/*.jsonf backup  

---

## 📝 NEXT UPDATE (Owner Rotator)

**Next Owner to Update Board:** After any milestone completion  
**Format:** "Fatto X" / "Rischio Y" / "Blocco Z" or "Prossimo Passo"  

<!-- END OF TEAM BOARD -->