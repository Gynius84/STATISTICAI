"""
STATISTICHEAI - Agent Doctor & Resurrection Engine
Gestione reale e sicura delle diagnosi, cure (sessione/contesto) e resurrezioni per i 7 agenti Hermes.
- Azioni circoscritte esclusivamente al singolo agente selezionato
- Backup automatico preventivo prima di qualsiasi modifica
- Verifica reale post-resurrezione con rollback in caso di errore
- Nessuna scrittura fuori cartella o oltre i file strettamente necessari dell'agente
"""

import os
import sys
import re
import time
import json
import ctypes
import shutil
import sqlite3
import datetime
import subprocess
import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
BACKUPS_DIR = BASE_DIR / "backups"
SIMULATED_FILE = DATA_DIR / "simulated_states.json"
CURED_FILE = DATA_DIR / "cured_states.json"
HISTORY_FILE = DATA_DIR / "actions_history.json"

HERMES_ROOT = Path(r"C:\Users\Gyniu\AppData\Local\hermes")
MANIFEST_FILE = HERMES_ROOT / "golden_tuning" / "tuning_manifest.json"
HERMES_PYTHON = Path(r"C:\Users\Gyniu\AppData\Local\hermes\tools\python-3.14.7+20260901-win32-x64\python.exe")

DATA_DIR.mkdir(parents=True, exist_ok=True)
WIN_FLAGS = 0x08000000 if sys.platform == "win32" else 0
BACKUPS_DIR.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger("agent_doctor")


def _load_json(file_path: Path, default_val):
    if not file_path.exists():
        return default_val
    try:
        return json.loads(file_path.read_text(encoding="utf-8"))
    except Exception:
        return default_val


def _save_json(file_path: Path, data):
    file_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def log_action(agent_id: str, agent_name: str, action: str, status: str, details: str, backup_path: str = None):
    """Registra l'azione nello storico visibile della dashboard."""
    history = _load_json(HISTORY_FILE, [])
    entry = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "agent_id": agent_id,
        "agent_name": agent_name,
        "action": action,
        "status": status,
        "details": details,
        "backup_path": backup_path or "N/D"
    }
    history.insert(0, entry)
    # Mantieni fino a 100 record recenti
    if len(history) > 100:
        history = history[:100]
    _save_json(HISTORY_FILE, history)


def get_actions_history():
    return _load_json(HISTORY_FILE, [])


def get_simulated_states():
    return _load_json(SIMULATED_FILE, {})


def set_simulated_state(agent_id: str, issue_type: str):
    """
    Imposta uno stato simulato per un agente:
    - 'session': sessione bloccata (Infermeria)
    - 'context': contesto saturo (Infermeria)
    - 'cemetery': entrambi i problemi (Cimitero)
    - 'clear': rimuove simulazione (Torna a Sano/Diagnosi reale)
    """
    states = get_simulated_states()
    if issue_type == "clear":
        if agent_id in states:
            del states[agent_id]
    elif issue_type in ["session", "context", "cemetery"]:
        states[agent_id] = {
            "type": issue_type,
            "created_at": datetime.datetime.now().isoformat()
        }
    _save_json(SIMULATED_FILE, states)
    return states.get(agent_id, None)


def get_profile_path(profile_name: str) -> Path:
    if profile_name == "default":
        return HERMES_ROOT
    return HERMES_ROOT / "profiles" / profile_name


def prune_old_backups(days_retention: int = 3):
    """Elimina automaticamente i backup preventivi piu' vecchi di N giorni per evitare saturazione disco."""
    if not BACKUPS_DIR.exists():
        return
    now = datetime.datetime.now()
    cutoff = now - datetime.timedelta(days=days_retention)
    for item in BACKUPS_DIR.iterdir():
        try:
            mtime = datetime.datetime.fromtimestamp(item.stat().st_mtime)
            if mtime < cutoff:
                if item.is_dir():
                    shutil.rmtree(item, ignore_errors=True)
                else:
                    item.unlink(missing_ok=True)
        except Exception:
            pass


def backup_agent(agent_id: str, profile_name: str, action_name: str) -> Path:
    """Esegue il backup completo dei soli file dell'agente target prima dell'azione."""
    prune_old_backups(days_retention=3)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    b_dir = BACKUPS_DIR / f"agent_{agent_id}_{action_name}_{ts}"
    b_dir.mkdir(parents=True, exist_ok=True)

    p_dir = get_profile_path(profile_name)

    cfg = p_dir / "config.yaml"
    if cfg.exists():
        shutil.copy2(cfg, b_dir / "config.yaml")

    meta = p_dir / "profile.yaml"
    if meta.exists():
        shutil.copy2(meta, b_dir / "profile.yaml")

    rt = p_dir / "runtime" / "active_sessions.json"
    if rt.exists():
        os.makedirs(b_dir / "runtime", exist_ok=True)
        shutil.copy2(rt, b_dir / "runtime" / "active_sessions.json")

    # Copia di backup SQLite di sicurezza (se esiste state.db)
    db_file = p_dir / "state.db"
    if db_file.exists():
        try:
            # Backup sicuro con copia diretta o lock rapido
            shutil.copy2(db_file, b_dir / "state.db")
        except Exception:
            pass

    return b_dir


def _is_pid_alive(pid: int) -> bool:
    """Verifica istantanea (0.01ms) via Win32 API se un processo Windows e' ancora vivo."""
    if not pid or pid <= 0:
        return False
    if sys.platform == "win32":
        try:
            PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
            STILL_ACTIVE = 259
            h_proc = ctypes.windll.kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, int(pid))
            if not h_proc:
                return False
            exit_code = ctypes.c_ulong()
            ok = ctypes.windll.kernel32.GetExitCodeProcess(h_proc, ctypes.byref(exit_code))
            ctypes.windll.kernel32.CloseHandle(h_proc)
            return bool(ok and exit_code.value == STILL_ACTIVE)
        except Exception:
            pass
    try:
        out = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/FO", "CSV", "/NH"],
                             capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=2, creationflags=WIN_FLAGS)
        return str(pid) in out.stdout
    except Exception:
        return False


def _get_last_ok_assistant_ts(p_dir: Path) -> float:
    """Restituisce il timestamp dell'ultima risposta valida dell'agente nel database SQLite."""
    db_file = p_dir / "state.db"
    if not db_file.exists():
        return 0.0
    try:
        uri = f"file:{db_file}?mode=ro"
        conn = sqlite3.connect(uri, uri=True, timeout=0.4)
        c = conn.cursor()
        c.execute("""
            SELECT max(timestamp) FROM messages
            WHERE role = 'assistant'
              AND content NOT LIKE 'Your request was not processed%'
              AND content NOT LIKE 'An automated delivery was interrupted%'
        """)
        row = c.fetchone()
        conn.close()
        return float(row[0]) if (row and row[0]) else 0.0
    except Exception:
        return 0.0


def _parse_log_ts(line: str) -> float:
    """Estrae il timestamp UNIX da una riga di log Hermes 'YYYY-MM-DD HH:MM:SS,mmm'."""
    m = re.match(r"^(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})(?:,(\d{1,3}))?", line)
    if not m:
        return 0.0
    try:
        dt = datetime.datetime.strptime(m.group(1), "%Y-%m-%d %H:%M:%S")
        ms = int(m.group(2) or 0) / 1000.0
        return dt.timestamp() + ms
    except Exception:
        return 0.0


def _analyze_error_logs(agent_id: str, profile_name: str, p_dir: Path, is_cloud: bool, baseline_ts: float, cured_at: float = 0.0) -> tuple[bool, str]:
    """
    Analizza gli ultimi blocchi di logs/errors.log del profilo (e del pool OpenRouter condiviso)
    per rilevare blocchi reali non risolti:
    - HTTP 429 Quota Exceeded / RateLimitError (Google AI Studio, OpenRouter Free Tier)
    - HTTP 502/503/504 Gateway Timeout / Managed worker lost (NVIDIA NIM / Cloud Upstream)
    Ignora errori vecchi superati da una risposta valida successiva o da un fix di config.yaml.
    """
    now = time.time()
    log_files = [p_dir / "logs" / "errors.log"]

    # I profili OpenRouter Free Tier (inkling, laguna) condividono il limite giornaliero sull'account OpenRouter
    is_openrouter_prof = profile_name in ("inkling", "laguna") or agent_id in ("inkling", "laguna")
    if is_openrouter_prof:
        shared_or_log = HERMES_ROOT / "profiles" / "laguna" / "logs" / "errors.log"
        if shared_or_log not in log_files:
            log_files.append(shared_or_log)

    cfg_file = p_dir / "config.yaml"
    cfg_uses_9931 = False
    if cfg_file.exists():
        try:
            cfg_txt = cfg_file.read_text(encoding="utf-8", errors="ignore")
            cfg_uses_9931 = "127.0.0.1:9931" in cfg_txt and "127.0.0.1:9932" not in cfg_txt
        except Exception:
            pass

    latest_issue_ts = 0.0
    latest_issue_msg = ""

    for lf in log_files:
        if not lf.exists():
            continue
        try:
            with open(lf, "rb") as f:
                f.seek(0, os.SEEK_END)
                sz = f.tell()
                f.seek(max(0, sz - 16384), os.SEEK_SET)
                tail_text = f.read().decode("utf-8", errors="ignore")
        except Exception:
            continue

        # Suddivide in blocchi basati sulle righe che iniziano con timestamp YYYY-MM-DD HH:MM:SS
        blocks = []
        curr_ts = 0.0
        curr_lines = []
        for line in tail_text.splitlines():
            ts = _parse_log_ts(line)
            if ts > 0:
                if curr_lines and curr_ts > 0:
                    blocks.append((curr_ts, "\n".join(curr_lines)))
                curr_ts = ts
                curr_lines = [line]
            else:
                if curr_lines:
                    curr_lines.append(line)
        if curr_lines and curr_ts > 0:
            blocks.append((curr_ts, "\n".join(curr_lines)))

        for b_ts, b_txt in blocks:
            is_shared_or_block = (lf != (p_dir / "logs" / "errors.log"))
            if is_shared_or_block:
                if "free-models-per-day" not in b_txt and "openrouter_free_tier" not in b_txt:
                    continue
                # Per il limite giornaliero OpenRouter (50/50 free-models-per-day), vale finche' non scade X-RateLimit-Reset
                # a meno che non ci sia stata una risposta valida almeno 5 minuti dopo o una cura manuale
                if b_ts <= cured_at or baseline_ts > (b_ts + 300):
                    continue
            else:
                # Ignora errori precedenti all'ultima risposta valida dell'agente (con 5s di tolleranza) o all'ultima cura manuale
                if b_ts <= max(baseline_ts + 2.0, cured_at):
                    continue

            # Ignora vecchi errori sulla porta 9932 se il profilo ora punta correttamente a 9931
            if "127.0.0.1:9932" in b_txt and cfg_uses_9931:
                continue

            b_low = b_txt.lower()
            # 1. Controllo Quota / Rate Limit (HTTP 429)
            if any(k in b_low for k in ("ratelimiterror", "error code: 429", "\"code\": 429", "quota exceeded", "exceeded your current quota", "resource_exhausted", "free-models-per-day")):
                reset_m = re.search(r"'X-RateLimit-Reset':\s*'(\d+)'", b_txt)
                reset_ts = (int(reset_m.group(1)) / 1000.0) if reset_m else (b_ts + 14400)
                if now < reset_ts or (now - b_ts) < 14400:
                    if b_ts >= latest_issue_ts:
                        latest_issue_ts = b_ts
                        if "free-models-per-day" in b_low or is_openrouter_prof:
                            latest_issue_msg = "In attesa rigenerazione Quota OpenRouter (HTTP 429: 50/50 req giornaliere Free Tier)"
                        elif "exceeded your current quota" in b_low or "quota exceeded" in b_low or "googleapis" in b_low or profile_name == "google":
                            latest_issue_msg = "In attesa rigenerazione Quota Google AI Studio (HTTP 429 Free Tier)"
                        else:
                            latest_issue_msg = "In attesa rigenerazione Quota Cloud (HTTP 429 Rate Limit)"

            # 2. Controllo Timeout / 504 / Crash Worker su Cloud
            elif is_cloud and any(k in b_txt for k in ("Error code: 504", "Error code: 502", "Error code: 503", "Gateway Timeout", "Managed worker lost: EOFError", "API call failed after 3 retries")):
                if (now - b_ts) < 21600:
                    prev_ts = latest_issue_ts
                    if b_ts >= latest_issue_ts:
                        latest_issue_ts = b_ts
                        if ("Quota" in latest_issue_msg or "504" in latest_issue_msg) and (b_ts - prev_ts) < 30:
                            pass
                        elif "504" in b_txt or "Gateway Timeout" in b_txt or "504" in tail_text[-1500:]:
                            latest_issue_msg = "Timeout Nodo Cloud NVIDIA NIM (HTTP 504 Gateway Timeout) — Attesa ripristino"
                        else:
                            latest_issue_msg = "Sessione Cloud interrotta per Timeout Upstream — Attesa ripristino nodo"

    if latest_issue_ts > 0 and latest_issue_msg:
        return True, latest_issue_msg
    return False, ""


def diagnose_agent(agent_id: str, profile_name: str, model_name: str, context_limit: int, is_cloud: bool = False, **kwargs) -> dict:
    """
    Diagnosi reale e dinamica dello stato di salute e della stanza dell'agente (Locale e Cloud):
    - LA CASETTA (riposo): Agente SANO e pronto, ma non in esecuzione attiva in questo istante.
    - L'UFFICIO (lavoro): Agente SANO attualmente in esecuzione attiva (processo vivo o attivita' negli ultimi secondi).
    - INFERMERIA (cura): Agente temporaneamente infortunato / in pausa per limiti rigenerabili (es. Quota Cloud 429, Timeout 504, Lease orfano).
    - IL CIMITERO (deceduto): Agente bloccato da doppio guasto critico (sessione + contesto/configurazione).
    """
    p_dir = get_profile_path(profile_name)
    sim = get_simulated_states().get(agent_id)
    cured_map = _load_json(CURED_FILE, {})
    cured_at = float(cured_map.get(agent_id, 0.0) or 0.0)

    session_blocked = False
    session_issue_detail = ""
    context_overflow = False
    context_issue_detail = ""
    is_working_now = False

    # 1. Controlli simulati (se presenti)
    if sim:
        sim_type = sim.get("type")
        if sim_type == "session":
            session_blocked = True
            session_issue_detail = "Simulazione: Lease sessione orfana bloccante rilevata"
        elif sim_type == "context":
            context_overflow = True
            context_issue_detail = "Simulazione: Contesto saturo al 96.5% - superata soglia limite"
        elif sim_type == "cemetery":
            session_blocked = True
            session_issue_detail = "Simulazione critica: Crash sessione e lease corrotti"
            context_overflow = True
            context_issue_detail = "Simulazione critica: Contesto ecceduto e configurazione non allineata"

    # 2. Diagnosi Reale basata su processi attivi, database SQLite e logs/errors.log
    if not sim:
        # A. Controllo Lease Sessione reale in runtime/active_sessions.json
        rt_file = p_dir / "runtime" / "active_sessions.json"
        if rt_file.exists():
            try:
                rt_data = json.loads(rt_file.read_text(encoding="utf-8"))
                entries = rt_data.get("entries", [])
                for e in entries:
                    pid = e.get("pid", 0)
                    if pid > 0:
                        if _is_pid_alive(pid):
                            is_working_now = True
                        else:
                            session_blocked = True
                            session_issue_detail = f"Sessione interrotta / Lease orfano (PID terminato: {pid})"
            except Exception:
                pass

        # B. Analisi Reale di logs/errors.log (Quota 429, Timeout 504, EOFError)
        if not is_working_now:
            last_ok_ts = _get_last_ok_assistant_ts(p_dir)
            baseline_ts = max(last_ok_ts, cured_at)
            log_blocked, log_detail = _analyze_error_logs(agent_id, profile_name, p_dir, is_cloud, baseline_ts, cured_at)
            if log_blocked:
                session_blocked = True
                if session_issue_detail and log_detail not in session_issue_detail:
                    session_issue_detail = f"{log_detail} • {session_issue_detail}"
                else:
                    session_issue_detail = log_detail

    # 3. Classificazione Finale: SANO, INFERMERIA, CIMITERO
    if session_blocked and context_overflow:
        health_status = "CIMITERO"
        room = "cimitero"
    elif session_blocked or context_overflow:
        health_status = "INFERMERIA"
        room = "infermeria"
    else:
        health_status = "SANO"
        room = "ufficio" if is_working_now else "casetta"

    return {
        "agent_id": agent_id,
        "profile": profile_name,
        "health_status": health_status,
        "room": room,
        "is_working_now": is_working_now,
        "session_blocked": session_blocked,
        "session_issue_detail": session_issue_detail,
        "context_overflow": context_overflow,
        "context_issue_detail": context_issue_detail,
        "is_simulated": bool(sim),
        "can_cure_session": session_blocked and health_status == "INFERMERIA",
        "can_cure_context": context_overflow and health_status == "INFERMERIA",
        "can_resurrect": health_status == "CIMITERO"
    }


def cure_session(agent_id: str, agent_name: str, profile_name: str) -> dict:
    """Cura SOLO la sessione dell'agente (pulisce lease orfani e registra timestamp di cura)."""
    b_path = backup_agent(agent_id, profile_name, "cure_session")
    p_dir = get_profile_path(profile_name)

    # 1. Pulisce lease orfani
    rt_file = p_dir / "runtime" / "active_sessions.json"
    cleaned_count = 0
    if rt_file.exists():
        try:
            data = json.loads(rt_file.read_text(encoding="utf-8"))
            entries = data.get("entries", [])
            cleaned_count = len(entries)
            data["entries"] = []
            rt_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
        except Exception:
            pass

    # 2. Registra timestamp di cura per ignorare errori log precedenti alla cura manuale
    cured_map = _load_json(CURED_FILE, {})
    cured_map[agent_id] = time.time()
    _save_json(CURED_FILE, cured_map)

    # 3. Rimuove simulazione sessione se presente
    sims = get_simulated_states()
    if agent_id in sims and sims[agent_id].get("type") == "session":
        del sims[agent_id]
        _save_json(SIMULATED_FILE, sims)

    msg = f"Sessione curata con successo: ripuliti lease attivi ({cleaned_count}) e resettato stato diagnostico."
    log_action(agent_id, agent_name, "CURA_SESSIONE", "SUCCESSO", msg, str(b_path))
    return {"ok": True, "message": msg, "backup_path": str(b_path)}


def cure_context(agent_id: str, agent_name: str, profile_name: str) -> dict:
    """Cura SOLO il contesto dell'agente ripristinando il file di configurazione golden calibrato."""
    b_path = backup_agent(agent_id, profile_name, "cure_context")
    p_dir = get_profile_path(profile_name)

    # File golden testato e verificato
    golden_dir = HERMES_ROOT / "golden_tuning" / "profiles"
    golden_cfg = golden_dir / "default" / "config.yaml" if profile_name == "default" else golden_dir / profile_name / "config.yaml"

    if golden_cfg.exists():
        shutil.copy2(golden_cfg, p_dir / "config.yaml")
    else:
        err = f"File golden non trovato per profilo {profile_name} in {golden_cfg}"
        log_action(agent_id, agent_name, "CURA_CONTESTO", "ERRORE", err, str(b_path))
        return {"ok": False, "error": err}

    # Rimuove simulazione contesto se presente
    sims = get_simulated_states()
    if agent_id in sims and sims[agent_id].get("type") == "context":
        del sims[agent_id]
        _save_json(SIMULATED_FILE, sims)

    msg = f"Contesto curato con successo: ripristinata configurazione golden calibrata per {agent_name}."
    log_action(agent_id, agent_name, "CURA_CONTESTO", "SUCCESSO", msg, str(b_path))
    return {"ok": True, "message": msg, "backup_path": str(b_path)}


def resurrect_agent(agent_id: str, agent_name: str, profile_name: str) -> dict:
    """
    Resurrezione completa con 1-click:
    1. Backup completo dell'agente
    2. Reset sessioni
    3. Reset contesto con valori d'oro
    4. Test reale di risposta con hermes -p <profile> -z 'test'
    5. Se successo: torna in vita SANO. Se fallisce: rollback immediato.
    """
    b_path = backup_agent(agent_id, profile_name, "resurrect")

    try:
        # Step A: Cura Sessione
        cure_session(agent_id, agent_name, profile_name)
        # Step B: Cura Contesto
        cure_context(agent_id, agent_name, profile_name)

        # Step C: Rimuove eventuale simulazione
        sims = get_simulated_states()
        if agent_id in sims:
            del sims[agent_id]
            _save_json(SIMULATED_FILE, sims)

        # Step D: Test reale di risposta per verificare che l'agente risponda col suo modello ottimizzato
        logger.info("[RESURREZIONE] Esecuzione test di verifica reale su profilo '%s'...", profile_name)
        hermes_bin = str(HERMES_ROOT / "bin" / "hermes.exe")
        if not Path(hermes_bin).exists():
            hermes_bin = "hermes"

        test_cmd = [hermes_bin, "-p", profile_name, "-z", "Rispondi solo con: OK RESUSCITATO"]
        if profile_name == "default":
            test_cmd = [hermes_bin, "-z", "Rispondi solo con: OK RESUSCITATO"]

        probe_res = subprocess.run(
            test_cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=60,
            creationflags=WIN_FLAGS
        )

        out_text = (probe_res.stdout or "").strip()
        keywords = ["OK", "RISUSCITATO", "RESUSCITATO", "PRONTO", "CIAO"]
        success = probe_res.returncode == 0 and (any(w in out_text.upper() for w in keywords) or len(out_text) > 0)

        if success:
            msg = f"Resurrezione completata con SUCCESSO! L'agente ha risposto al test di verifica reale: '{out_text}'."
            log_action(agent_id, agent_name, "RESURREZIONE", "SUCCESSO", msg, str(b_path))
            return {
                "ok": True,
                "message": msg,
                "backup_path": str(b_path),
                "test_output": out_text
            }
        else:
            raise RuntimeError(f"Il test di verifica ha restituito codice {probe_res.returncode} o output non valido. Err: {probe_res.stderr}")

    except Exception as exc:
        # ROLLBACK IMMEDIATO IN CASO DI ERRORE
        logger.error("[RESURREZIONE] Errore durante resurrezione di '%s': %s. Esecuzione ROLLBACK...", agent_name, exc)
        p_dir = get_profile_path(profile_name)

        if (b_path / "config.yaml").exists():
            shutil.copy2(b_path / "config.yaml", p_dir / "config.yaml")
        if (b_path / "profile.yaml").exists():
            shutil.copy2(b_path / "profile.yaml", p_dir / "profile.yaml")
        if (b_path / "runtime" / "active_sessions.json").exists():
            shutil.copy2(b_path / "runtime" / "active_sessions.json", p_dir / "runtime" / "active_sessions.json")

        # Ripristina stato cimitero simulato per proteggere la visualizzazione
        set_simulated_state(agent_id, "cemetery")

        err_msg = f"Resurrezione FALLITA: {exc}. Rollback completato. L'agente resta nel Cimitero."
        log_action(agent_id, agent_name, "RESURREZIONE", "FALLITO", err_msg, str(b_path))
        return {
            "ok": False,
            "error": err_msg,
            "backup_path": str(b_path)
        }
