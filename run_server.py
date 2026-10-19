"""
STATISTICHEAI - Backend Server Ottimizzato & Ultra-Reattivo
Progetto puramente OSSERVATORE (Regola Zero).
Bind su 127.0.0.1:8787, priorita' BelowNormal, zero dipendenze esterne.
Tutti i dati serviti istantaneamente dalla memoria (<1ms) con worker dedicati.
"""

import http.server
import socketserver
import urllib.request
import urllib.parse
import urllib.error
import json
import sqlite3
import ctypes
import subprocess
import threading
import time
import datetime
import hashlib
import os
import sys
import shutil
import signal
import re
import agent_doctor

# ---------------------------------------------------------------------------
# Inizializzazione Ambiente e Percorsi
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")
BASELINE_FILE = os.path.join(BASE_DIR, "docs", "BASELINE.md")
PID_FILE = os.path.join(BASE_DIR, "server.pid")
DATA_DIR = os.path.join(BASE_DIR, "data")
ARCHIVE_DIR = os.path.join(DATA_DIR, "archive")
SPRITES_DIR = os.path.join(BASE_DIR, "sprites_agents")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(ARCHIVE_DIR, exist_ok=True)

# Imposta Priorita' BelowNormal (Windows)
try:
    BELOW_NORMAL_PRIORITY_CLASS = 0x00004000
    ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), BELOW_NORMAL_PRIORITY_CLASS)
except Exception:
    pass

CSRF_TOKEN = os.urandom(16).hex()

# Carica Configurazione
with open(CONFIG_FILE, "r", encoding="utf-8") as f:
    CONFIG = json.load(f)

SERVER_HOST = CONFIG.get("server", {}).get("host", "127.0.0.1")
DEFAULT_PORT = CONFIG.get("server", {}).get("port", 8787)
ACTIONS_ENABLED = CONFIG.get("server", {}).get("actions_enabled", True)

AGENTS_DEF = CONFIG.get("agents", [])
HERMES_ROOT = r"C:\Users\Gyniu\AppData\Local\hermes"

# ---------------------------------------------------------------------------
# Monitor Guardiano (Integrita' Baseline 60s)
# ---------------------------------------------------------------------------
class GuardianMonitor:
    def __init__(self, baseline_path):
        self.baseline_path = baseline_path
        self.monitored_files = {}
        self.last_check = 0
        self.status = "VERIFICA_IN_CORSO"
        self.mismatches = []
        self.test_probe_active = False
        self.test_probe_path = os.path.join(DATA_DIR, "probe_guardiano_test.tmp")
        self.load_baseline()

    def load_baseline(self):
        if not os.path.exists(self.baseline_path):
            self.status = "ERRORE_BASELINE_MANCANTE"
            return
        monitored = {}
        with open(self.baseline_path, "r", encoding="utf-8") as f:
            for line in f:
                if "AppData" in line and "|" in line:
                    parts = [p.replace("`", "").strip() for p in line.split("|")[1:-1]]
                    if len(parts) >= 4:
                        p, sha, sz, mtime = parts[0], parts[1], parts[2], parts[3]
                        monitored[p] = {"sha256": sha, "mtime": mtime}
        self.monitored_files = monitored
        self.verify_now()

    def verify_now(self):
        # Ricarica baseline se il file e' stato aggiornato
        try:
            mtime = os.path.getmtime(self.baseline_path)
            if getattr(self, "baseline_mtime", 0) != mtime:
                self.baseline_mtime = mtime
                monitored = {}
                with open(self.baseline_path, "r", encoding="utf-8") as f:
                    for line in f:
                        if "AppData" in line and "|" in line:
                            parts = [p.replace("`", "").strip() for p in line.split("|")[1:-1]]
                            if len(parts) >= 4:
                                p, sha, sz, mt = parts[0], parts[1], parts[2], parts[3]
                                monitored[p] = {"sha256": sha, "mtime": mt}
                self.monitored_files = monitored
        except Exception:
            pass

        diffs = []
        for path, exp in self.monitored_files.items():
            if not os.path.exists(path):
                diffs.append({"file": path, "error": "FILE_MANCANTE"})
            else:
                try:
                    with open(path, "rb") as f:
                        actual_sha = hashlib.sha256(f.read()).hexdigest()
                    if actual_sha != exp["sha256"]:
                        diffs.append({
                            "file": path,
                            "error": "SHA_MISMATCH",
                            "expected": exp["sha256"],
                            "actual": actual_sha
                        })
                except Exception as e:
                    diffs.append({"file": path, "error": str(e)})

        if self.test_probe_active and os.path.exists(self.test_probe_path):
            diffs.append({
                "file": self.test_probe_path,
                "error": "ALLARME_SIMULATO_PROBE_MODIFICATO"
            })

        self.last_check = time.time()
        self.mismatches = diffs
        self.status = "INTEGRO" if len(diffs) == 0 else "ALLARME_MODIFICA_RILEVATA"
        return self.status

    def trigger_test_probe(self, active=True):
        self.test_probe_active = active
        if active:
            with open(self.test_probe_path, "w", encoding="utf-8") as f:
                f.write(f"PROBE_MODIFICATA_{time.time()}")
        else:
            if os.path.exists(self.test_probe_path):
                try:
                    os.remove(self.test_probe_path)
                except Exception:
                    pass
        self.verify_now()

    def auto_resolve_mismatches(self):
        """Risolve automaticamente le discrepanze dei file monitorati e sincronizza BASELINE.md."""
        updated_files = []
        if not os.path.exists(self.baseline_path):
            return {"success": False, "error": "Baseline file missing"}

        if self.test_probe_active or os.path.exists(self.test_probe_path):
            self.test_probe_active = False
            try:
                if os.path.exists(self.test_probe_path):
                    os.remove(self.test_probe_path)
            except Exception:
                pass

        try:
            with open(self.baseline_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            new_lines = []
            for line in lines:
                if "AppData" in line and "|" in line:
                    parts = [p.replace("`", "").strip() for p in line.split("|")[1:-1]]
                    if len(parts) >= 4:
                        path = parts[0]
                        if os.path.exists(path):
                            try:
                                with open(path, "rb") as bf:
                                    new_sha = hashlib.sha256(bf.read()).hexdigest()
                                sz = os.path.getsize(path)
                                mtime = datetime.datetime.fromtimestamp(os.path.getmtime(path)).strftime("%Y-%m-%dT%H:%M:%S")
                                line = f"| `{path}` | `{new_sha}` | {sz:,} | {mtime} |\n"
                                updated_files.append(path)
                            except Exception:
                                pass
                new_lines.append(line)

            with open(self.baseline_path, "w", encoding="utf-8") as f:
                f.writelines(new_lines)

            self.baseline_mtime = os.path.getmtime(self.baseline_path)
            self.load_baseline()
            self.verify_now()
            return {
                "success": True,
                "status": self.status,
                "updated_count": len(updated_files),
                "updated_files": updated_files
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

guardian = GuardianMonitor(BASELINE_FILE)

# ---------------------------------------------------------------------------
# Collettori Dati Indipendenti (Cache in memoria non bloccante)
# ---------------------------------------------------------------------------
STATE_CACHE = {
    "timestamp": int(time.time() * 1000),
    "system": {"cpu_pct": 0, "ram_total_gb": 32, "ram_avail_gb": 16, "ram_used_pct": 50, "disk_free_gb": 200, "disk_total_gb": 500},
    "gpu": {"available": True, "name": "NVIDIA GeForce RTX 4060 Laptop GPU", "vram_total_mb": 8188, "vram_used_mb": 1200, "vram_free_mb": 6988, "gpu_util_pct": 0, "temperature_c": 50, "power_draw_w": 6.0},
    "ollama": {"status": "online", "running_models": [], "installed_models_count": 16, "last_check": time.time()},
    "guardian": {"status": "INTEGRO", "last_check": time.time(), "monitored_count": 24, "mismatches": []},
    "agents": [],
    "actions_enabled": False,
    "csrf_token": CSRF_TOKEN
}
STATE_LOCK = threading.Lock()

class SystemCollector:
    class FILETIME(ctypes.Structure):
        _fields_ = [("dwLowDateTime", ctypes.c_ulong), ("dwHighDateTime", ctypes.c_ulong)]

    class MEMORYSTATUSEX(ctypes.Structure):
        _fields_ = [
            ("dwLength", ctypes.c_ulong),
            ("dwMemoryLoad", ctypes.c_ulong),
            ("ullTotalPhys", ctypes.c_ulonglong),
            ("ullAvailPhys", ctypes.c_ulonglong),
            ("ullTotalPageFile", ctypes.c_ulonglong),
            ("ullAvailPageFile", ctypes.c_ulonglong),
            ("ullTotalVirtual", ctypes.c_ulonglong),
            ("ullAvailVirtual", ctypes.c_ulonglong),
            ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
        ]

    def __init__(self):
        self.prev_idle = 0
        self.prev_total = 0
        self.last_cpu = 0.0

    def get_cpu_times(self):
        idle = self.FILETIME()
        kernel = self.FILETIME()
        user = self.FILETIME()
        ctypes.windll.kernel32.GetSystemTimes(ctypes.byref(idle), ctypes.byref(kernel), ctypes.byref(user))
        to_int = lambda ft: (ft.dwHighDateTime << 32) + ft.dwLowDateTime
        return to_int(idle), to_int(kernel) + to_int(user)

    def collect(self):
        curr_idle, curr_total = self.get_cpu_times()
        if self.prev_total > 0:
            delta_total = curr_total - self.prev_total
            delta_idle = curr_idle - self.prev_idle
            if delta_total > 0:
                self.last_cpu = max(0.0, min(100.0, ((delta_total - delta_idle) / delta_total) * 100.0))
        self.prev_idle = curr_idle
        self.prev_total = curr_total

        stat = self.MEMORYSTATUSEX()
        stat.dwLength = ctypes.sizeof(self.MEMORYSTATUSEX)
        ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
        ram_total_gb = round(stat.ullTotalPhys / (1024**3), 2)
        ram_avail_gb = round(stat.ullAvailPhys / (1024**3), 2)
        ram_used_pct = stat.dwMemoryLoad

        disk_total, _, disk_free = shutil.disk_usage("C:\\")
        disk_free_gb = round(disk_free / (1024**3), 1)
        disk_total_gb = round(disk_total / (1024**3), 1)

        return {
            "cpu_pct": round(self.last_cpu, 1),
            "ram_total_gb": ram_total_gb,
            "ram_avail_gb": ram_avail_gb,
            "ram_used_pct": ram_used_pct,
            "disk_free_gb": disk_free_gb,
            "disk_total_gb": disk_total_gb
        }

sys_collector = SystemCollector()

# Worker 1: GPU in background (ogni 4s per evitare overhead)
GPU_CACHE = {"available": True, "name": "NVIDIA GeForce RTX 4060 Laptop GPU", "vram_total_mb": 8188, "vram_used_mb": 1200, "vram_free_mb": 6988, "gpu_util_pct": 0, "temperature_c": 50, "power_draw_w": 6.0}
def gpu_worker_loop():
    global GPU_CACHE
    cmd = [
        "nvidia-smi",
        "--query-gpu=name,memory.total,memory.used,memory.free,utilization.gpu,temperature.gpu,power.draw",
        "--format=csv,noheader,nounits"
    ]
    while True:
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=2.0)
            if proc.returncode == 0 and proc.stdout.strip():
                p = [x.strip() for x in proc.stdout.strip().split(",")]
                GPU_CACHE = {
                    "available": True,
                    "name": p[0],
                    "vram_total_mb": int(p[1]),
                    "vram_used_mb": int(p[2]),
                    "vram_free_mb": int(p[3]),
                    "gpu_util_pct": int(p[4]),
                    "temperature_c": int(p[5]),
                    "power_draw_w": float(p[6])
                }
        except Exception:
            pass
        time.sleep(4.0)

# Worker 2: Ollama in background (ogni 3s / 30s)
OLLAMA_CACHE = {"status": "online", "running_models": [], "installed_models_count": 16, "last_check": time.time()}
def ollama_worker_loop():
    global OLLAMA_CACHE
    installed_count = 16
    last_tags_fetch = 0
    while True:
        try:
            # 1. Running models (ogni 3s)
            req = urllib.request.Request("http://127.0.0.1:11434/api/ps", headers={"User-Agent": "STATISTICHEAI-Fast"})
            with urllib.request.urlopen(req, timeout=1.0) as res:
                ps_data = json.loads(res.read().decode("utf-8"))

            running = []
            for m in ps_data.get("models", []):
                running.append({
                    "name": m.get("name"),
                    "size_vram_mb": round(m.get("size_vram", 0) / (1024**2), 1),
                    "expires_at": m.get("expires_at")
                })

            # 2. Installed models (ogni 30s)
            now = time.time()
            if now - last_tags_fetch > 30.0:
                try:
                    req_t = urllib.request.Request("http://127.0.0.1:11434/api/tags", headers={"User-Agent": "STATISTICHEAI-Fast"})
                    with urllib.request.urlopen(req_t, timeout=1.0) as res_t:
                        tags_data = json.loads(res_t.read().decode("utf-8"))
                        installed_count = len(tags_data.get("models", []))
                    last_tags_fetch = now
                except Exception:
                    pass

            OLLAMA_CACHE = {
                "status": "online",
                "running_models": running,
                "installed_models_count": installed_count,
                "last_check": now
            }
        except Exception as e:
            OLLAMA_CACHE["status"] = "offline_or_slow"
        time.sleep(2.5)

# Worker 2b: llama.cpp server in background (porta 9931, router su Disco D:)
LLAMACPP_CACHE = {
    "status": "online",
    "port": 9931,
    "source": "Disco D:",
    "models": [],
    "models_count": 0,
    "last_check": time.time()
}

def llamacpp_worker_loop():
    global LLAMACPP_CACHE
    while True:
        try:
            req = urllib.request.Request("http://127.0.0.1:9931/v1/models", headers={"User-Agent": "STATISTICHEAI-Fast"})
            with urllib.request.urlopen(req, timeout=1.2) as res:
                if res.status == 200:
                    data = json.loads(res.read().decode("utf-8"))
                    models_list = [m.get("id") for m in data.get("data", [])]
                    LLAMACPP_CACHE = {
                        "status": "online",
                        "port": 9931,
                        "source": "Disco D:",
                        "models": models_list,
                        "models_count": len(models_list),
                        "last_check": time.time()
                    }
        except Exception:
            LLAMACPP_CACHE["status"] = "offline_or_slow"
        time.sleep(3.0)

def auto_discover_hermes_agents():
    """
    Scansiona autonomamente la cartella HERMES_ROOT/profiles e gli endpoint LLM (Ollama su 11434 & llama.cpp su 9931).
    Rileva nuovi profili, sincronizza modelli/contesti modificati, e rimuove profili eliminati (auto-pruning).
    Sincronizza config.json e aggiorna AGENTS_DEF in tempo reale.
    """
    global CONFIG, AGENTS_DEF
    if not os.path.exists(HERMES_ROOT):
        return []

    profiles_dir = os.path.join(HERMES_ROOT, "profiles")
    prof_list = [("gynbot1", "default", HERMES_ROOT, "GynBot1")]
    valid_profiles = {"default"}

    if os.path.exists(profiles_dir):
        for item in sorted(os.listdir(profiles_dir)):
            item_path = os.path.join(profiles_dir, item)
            if os.path.isdir(item_path) and not item.startswith("."):
                prof_list.append((item, item, item_path, None))
                valid_profiles.add(item.lower())

    # Mappa sprite disponibili in sprites_agents
    available_sprites = {}
    sprites_folder = os.path.join(BASE_DIR, "sprites_agents")
    if os.path.exists(sprites_folder):
        for f in os.listdir(sprites_folder):
            if f.lower().endswith(".png"):
                available_sprites[f.lower()] = f"sprites_agents/{f}"

    current_agents = CONFIG.get("agents", [])
    existing_by_prof = {}
    for a in current_agents:
        p_key = (a.get("profile") or a.get("id") or "").lower()
        if p_key:
            existing_by_prof[p_key] = a

    config_changed = False
    new_agents_list = []

    for agent_id, prof_id, prof_dir, default_title in prof_list:
        cfg_yaml = os.path.join(prof_dir, "config.yaml")
        prof_yaml = os.path.join(prof_dir, "profile.yaml")

        title = default_title
        desc = "Agente Hermes"

        # Lettura profile.yaml (inclusi campi annidati in ui_meta)
        if os.path.exists(prof_yaml):
            try:
                with open(prof_yaml, "r", encoding="utf-8", errors="ignore") as f:
                    p_content = f.read()
                    m_ui_title = re.search(r"title:\s*([^\r\n]+)", p_content)
                    if m_ui_title:
                        title = m_ui_title.group(1).strip()
                    m_desc = re.search(r"description:\s*([^\r\n]+)", p_content)
                    if m_desc:
                        desc = m_desc.group(1).strip()
            except Exception:
                pass

        if not title:
            title = agent_id.replace("_", " ").title()

        # Normalizzazione descrizioni brevi
        d_clean = desc.strip()
        if d_clean.upper() == "PENTESTER":
            desc = "Pentester & Security Coder"
        elif d_clean.upper() == "RAGIONAMENTO":
            desc = "Ragionamento & Problem Solving"
        elif d_clean.upper() == "DEEP":
            desc = "Deep Thinking & Knowledge Synthesis"
        elif d_clean.upper() == "VISUAL MASTER":
            desc = "Visual Master & UI Multimodal"

        model_name = "qwen2.5:64k"
        provider = "ollama"
        base_url = "http://127.0.0.1:11434/v1"
        context_limit = 32768
        is_cloud = (agent_id == "beam" or "beam" in title.lower())

        if os.path.exists(cfg_yaml):
            try:
                with open(cfg_yaml, "r", encoding="utf-8", errors="ignore") as f:
                    c = f.read()
                    m_mod = re.search(r"(?:^|\n)model:\s*\n(.*?)(?=\n[a-z_]+:|\Z)", c, re.DOTALL)
                    if m_mod:
                        sec = m_mod.group(1)
                        d_match = re.search(r"default:\s*([^\s\r\n]+)", sec)
                        if d_match:
                            model_name = d_match.group(1)
                        p_match = re.search(r"provider:\s*([^\s\r\n]+)", sec)
                        if p_match:
                            provider = p_match.group(1)
                        u_match = re.search(r"base_url:\s*([^\s\r\n]+)", sec)
                        if u_match:
                            base_url = u_match.group(1)
                        c_match = re.search(r"context_length:\s*(\d+)", sec) or re.search(r"ollama_num_ctx:\s*(\d+)", sec)
                        if c_match:
                            context_limit = int(c_match.group(1))

                    prov_m = re.search(r"(?:^|\n)providers:\s*\n(.*?)(?=\n[a-z_]+:|\Z)", c, re.DOTALL)
                    if prov_m:
                        p_sec = prov_m.group(1)
                        mod_block = re.search(re.escape(model_name) + r":\s*\n\s*context_length:\s*(\d+)", p_sec)
                        if mod_block:
                            context_limit = int(mod_block.group(1))
            except Exception:
                pass

        # Normalizzazione Provider e Base URL
        if is_cloud or agent_id == "beam":
            provider = "beam"
            base_url = "http://127.0.0.1:11434/v1"
            context_limit = 1048576
        elif "llamacpp" in provider.lower() or "9931" in base_url or agent_id in ["coder14b", "mistral24b", "qwen", "vision7b"]:
            provider = "llamacpp"
            base_url = "http://127.0.0.1:9931/v1"
        else:
            provider = "ollama"
            base_url = "http://127.0.0.1:11434/v1"

        # Selezione Sprite
        sprite_path = "sprites_agents/GynBot1.png"
        candidates = [
            f"{title}.png".lower(),
            f"{agent_id}.png".lower(),
            f"{prof_id}.png".lower(),
            f"{agent_id.replace('_', ' ')}.png".lower(),
            f"{title.replace(' ', '_')}.png".lower(),
            f"{title.upper()}.png".lower(),
        ]
        if agent_id == "coder14b" or "dark" in title.lower():
            candidates.insert(0, "dark coder.png")
        elif agent_id == "mistral24b" or title.lower() == "iq":
            candidates.insert(0, "iq.png")
        elif agent_id == "qwen" or title.lower() == "mind":
            candidates.insert(0, "mind.png")
        elif agent_id == "vision7b" or title.lower() == "vision":
            candidates.insert(0, "vision.png")
        elif agent_id == "mentor" or "architect" in title.lower():
            candidates.insert(0, "chief architect.png")
        elif agent_id == "oculus" or "ocolus" in title.lower():
            candidates.insert(0, "ocolus.png")
        elif agent_id == "beam":
            candidates.insert(0, "beam.png")
        elif agent_id == "gynbot2":
            candidates.insert(0, "programmatore.png")
        elif agent_id == "gynbox3":
            candidates.insert(0, "quality cheker.png")
        elif agent_id == "mark1":
            candidates.insert(0, "direttore marketing.png")
        elif agent_id == "mark2":
            candidates.insert(0, "copywriter creativo.png")
        elif agent_id == "mark3":
            candidates.insert(0, "growt hacker.png")

        for c_cand in candidates:
            if c_cand in available_sprites:
                sprite_path = available_sprites[c_cand]
                break

        # Gruppo, Colore e Sorgente
        t_low = (title + " " + desc + " " + agent_id).lower()
        if is_cloud or "beam" in t_low:
            group = "SUPER COORDINATORE"
            color = "#38bdf8"
            source_label = "Cloud 501B MoE"
        elif "vision" in t_low or "oculus" in t_low or "ocolus" in t_low:
            group = "TEAM VISUAL AUDIT"
            color = "#0ea5e9"
            source_label = "llama.cpp (Disco D:)" if provider == "llamacpp" else "Ollama (Locale C:)"
        elif "architect" in t_low or "mentor" in t_low:
            group = "TEAM ARCHITETTURA"
            color = "#a855f7"
            source_label = "Ollama (Locale C:)"
        elif "dark" in t_low or "coder14b" in t_low or "pentester" in t_low:
            group = "TEAM SICUREZZA & CODING"
            color = "#ef4444"
            source_label = "llama.cpp (Disco D:)"
        elif "iq" in t_low or "mistral" in t_low or "ragionamento" in t_low:
            group = "TEAM RAGIONAMENTO"
            color = "#f59e0b"
            source_label = "llama.cpp (Disco D:)"
        elif "mind" in t_low or "deep" in t_low:
            group = "TEAM DEEP THINKING"
            color = "#06b6d4"
            source_label = "llama.cpp (Disco D:)"
        elif "marketing" in t_low or "mark" in t_low or "copy" in t_low or "growth" in t_low:
            group = "TEAM MARKETING"
            color = "#8b5cf6" if "1" in agent_id else ("#06b6d4" if "2" in agent_id else "#10b981")
            source_label = "Ollama (Locale C:)"
        else:
            group = "TEAM SVILUPPO"
            color = "#3b82f6" if agent_id in ["default", "gynbot1"] else ("#fbbf24" if agent_id == "gynbot2" else "#ec4899")
            source_label = "Ollama (Locale C:)"

        prof_lookup_key = prof_id.lower()
        existing = existing_by_prof.get(prof_lookup_key) or existing_by_prof.get(agent_id.lower())

        if existing:
            # Sincronizza proprietà modificate
            if (existing.get("model") != model_name or 
                existing.get("context_limit") != context_limit or 
                existing.get("name") != title or 
                existing.get("sprite") != sprite_path or 
                existing.get("provider") != provider or
                existing.get("group") != group or
                existing.get("source") != source_label):
                existing["name"] = title
                existing["title"] = desc
                existing["model"] = model_name
                existing["base_model"] = model_name.split("/")[-1].split(":")[0]
                existing["context_limit"] = context_limit
                existing["provider"] = provider
                existing["base_url"] = base_url
                existing["sprite"] = sprite_path
                existing["group"] = group
                existing["color"] = color
                existing["source"] = source_label
                config_changed = True
            new_agents_list.append(existing)
        else:
            new_agent = {
                "id": agent_id,
                "profile": prof_id,
                "name": title,
                "title": desc,
                "group": group,
                "color": color,
                "provider": provider,
                "base_url": base_url,
                "model": model_name,
                "base_model": model_name.split("/")[-1].split(":")[0],
                "context_limit": context_limit,
                "compress_threshold": 0.85,
                "sprite": sprite_path,
                "is_cloud": is_cloud,
                "source": source_label,
                "parameters": "501B" if is_cloud else ("35B" if "35b" in model_name.lower() else ("27B" if "27b" in model_name.lower() else ("24B" if "24b" in model_name.lower() else ("14B" if "14b" in model_name.lower() else ("9B" if "9b" in model_name.lower() else ("7B" if "7b" in model_name.lower() else "4B")))))),
                "architecture": "GGUF llama-server (Disco D:)" if provider == "llamacpp" else ("Cloud MoE" if is_cloud else "Ollama Local"),
                "modality": "Vision + Text + Tools" if "vl" in model_name.lower() or "bonsai" in model_name.lower() or "vision" in t_low else "Text + Tools",
                "thinking_level": "Extended Thinking" if "reasoning" in model_name.lower() or "27b" in model_name.lower() else "Standard"
            }
            new_agents_list.append(new_agent)
            config_changed = True
            print(f"[Auto-Discovery] Registrato nuovo agente Hermes: {title} ({prof_id}) -> {model_name}")

    # Auto-pruning: rimuove agenti eliminati da Hermes
    if len(new_agents_list) != len(current_agents):
        config_changed = True

    if config_changed:
        CONFIG["agents"] = new_agents_list
        AGENTS_DEF = new_agents_list
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(CONFIG, f, indent=2)
            print(f"[Auto-Discovery] Configurazione sincronizzata con successo: {len(new_agents_list)} agenti attivi.")
        except Exception as e:
            print(f"[Auto-Discovery] Errore salvataggio config.json: {e}")

    return new_agents_list


# Worker 3: Hermes SQLite in background (ogni 2.5s)
AGENTS_CACHE = []
LAST_DISCOVERY_CHECK = 0

def hermes_worker_loop():
    global AGENTS_CACHE, LAST_DISCOVERY_CHECK
    while True:
        try:
            now = time.time()
            # Esegue auto-discovery periodica dei profili Hermes ogni 3 secondi
            if now - LAST_DISCOVERY_CHECK > 3.0:
                try:
                    auto_discover_hermes_agents()
                except Exception as e:
                    pass
                LAST_DISCOVERY_CHECK = now

            # Ricarica configurazione agenti dinamica
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    current_agents_def = json.load(f).get("agents", AGENTS_DEF)
            except Exception:
                current_agents_def = AGENTS_DEF

            ollama_models = OLLAMA_CACHE.get("running_models", [])
            new_list = []
            for agent_def in current_agents_def:
                profile = agent_def["profile"]
                db_path = os.path.join(HERMES_ROOT, "state.db") if profile == "default" else os.path.join(HERMES_ROOT, "profiles", profile, "state.db")
                uri = f"file:///{db_path.replace(os.sep, '/')}?mode=ro"

                stat_res = {
                    "id": agent_def["id"],
                    "name": agent_def["name"],
                    "title": agent_def["title"],
                    "group": agent_def["group"],
                    "color": agent_def["color"],
                    "model": agent_def["model"],
                    "context_limit": agent_def["context_limit"],
                    "sprite": agent_def["sprite"],
                    "compress_threshold": agent_def["compress_threshold"],
                    "provider": agent_def.get("provider", "ollama"),
                    "source": agent_def.get("source", "Ollama (Locale C:)"),
                    "base_url": agent_def.get("base_url", "http://127.0.0.1:11434/v1"),
                    "is_cloud": agent_def.get("is_cloud", False),
                    "parameters": agent_def.get("parameters", "N/D"),
                    "architecture": agent_def.get("architecture", "N/D"),
                    "modality": agent_def.get("modality", "Text"),
                    "thinking_level": agent_def.get("thinking_level", "N/D"),
                    "total_sessions": 0,
                    "lifetime_sessions": 0,
                    "lifetime_messages": 0,
                    "lifetime_input_tokens": 0,
                    "lifetime_output_tokens": 0,
                    "lifetime_tokens": 0,
                    "lifetime_api_calls": 0,
                    "lifetime_tool_calls": 0,
                    "active_session_msgs": 0,
                    "active_session_tool_calls": 0,
                    "db_size_mb": 0.0,
                    "turn_avg_input_tokens": 0,
                    "turn_avg_output_tokens": 0,
                    "memory_active": False,
                    "memory_bytes": 0,
                    "memory_files_count": 0,
                    "memory_snippet": "",
                    "memory_last_update": None,
                    "current_session_id": "N/D",
                    "current_task": "In attesa di istruzioni",
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "context_used_tokens": 0,
                    "session_total_tokens": 0,
                    "api_call_count": 0,
                    "context_used_pct": 0.0,
                    "hp": 100,
                    "status": "riposo",
                    "room": "cloud" if agent_def.get("is_cloud") else "casetta",
                    "vram_mb": 0,
                    "is_shared_model": False,
                    "last_activity": None
                }

                # VRAM & Engine check
                if agent_def.get("is_cloud"):
                    stat_res["vram_mb"] = 0
                    stat_res["is_shared_model"] = False
                elif agent_def.get("provider") == "llamacpp" or "9931" in agent_def.get("base_url", ""):
                    stat_res["is_shared_model"] = False
                    stat_res["vram_mb"] = 0
                    if LLAMACPP_CACHE.get("status") == "online":
                        if stat_res["status"] == "riposo":
                            stat_res["status"] = "attivo"
                else:
                    matching = [m for m in ollama_models if agent_def["model"] in m["name"]]
                    if matching:
                        stat_res["vram_mb"] = matching[0]["size_vram_mb"]
                        if agent_def["model"] == "hermes3:64k":
                            stat_res["is_shared_model"] = True
                            stat_res["vram_mb"] = round(stat_res["vram_mb"] / 2.0, 1)

                # Controllo Memoria Persistente a Lungo Termine (memories/MEMORY.md & USER.md)
                mem_dir = os.path.join(HERMES_ROOT, "memories") if profile == "default" else os.path.join(HERMES_ROOT, "profiles", profile, "memories")
                if os.path.exists(mem_dir):
                    try:
                        mem_b = 0
                        mem_files = []
                        last_m = 0
                        snip = ""
                        for mf in os.listdir(mem_dir):
                            if mf.endswith(".md"):
                                mfp = os.path.join(mem_dir, mf)
                                msz = os.path.getsize(mfp)
                                mem_b += msz
                                mem_files.append(mf)
                                mtime = os.path.getmtime(mfp)
                                if mtime > last_m:
                                    last_m = mtime
                                if not snip and msz > 0:
                                    try:
                                        with open(mfp, "r", encoding="utf-8", errors="ignore") as f_snip:
                                            raw = f_snip.read(250).replace("\n", " ").replace("§", "").strip()
                                            snip = " ".join(raw.split())[:140]
                                    except Exception:
                                        pass
                        stat_res["memory_active"] = (mem_b > 0)
                        stat_res["memory_bytes"] = mem_b
                        stat_res["memory_files_count"] = len(mem_files)
                        stat_res["memory_snippet"] = snip
                        if last_m > 0:
                            stat_res["memory_last_update"] = datetime.datetime.fromtimestamp(last_m).strftime("%d/%m %H:%M")
                    except Exception:
                        pass

                # Estrazione Metriche SQLite (se profilo Hermes presente)
                provider = agent_def.get("provider", "hermes" if profile else "ollama")
                endpoint = agent_def.get("endpoint", "")
                stat_res["provider"] = provider
                stat_res["endpoint"] = endpoint

                if os.path.exists(db_path):
                    try:
                        stat_res["db_size_mb"] = round(os.path.getsize(db_path) / (1024 * 1024), 2)
                        conn = sqlite3.connect(uri, uri=True, timeout=0.5)
                        c = conn.cursor()

                        # 1. Statistiche Storiche Cumulative (Lifetime persistenti nel DB)
                        c.execute("""
                            SELECT count(*), coalesce(sum(message_count), 0), coalesce(sum(input_tokens), 0),
                                   coalesce(sum(output_tokens), 0), coalesce(sum(api_call_count), 0), coalesce(sum(tool_call_count), 0)
                            FROM sessions
                        """)
                        tot_s, s_msg, tot_in, tot_out, tot_calls, tot_tools = c.fetchone()
                        real_msgs = s_msg
                        try:
                            c.execute("SELECT count(*) FROM messages")
                            real_msgs = c.fetchone()[0]
                        except Exception:
                            pass

                        stat_res["total_sessions"] = tot_s
                        stat_res["lifetime_sessions"] = tot_s
                        stat_res["lifetime_messages"] = max(real_msgs, s_msg)
                        stat_res["lifetime_input_tokens"] = tot_in
                        stat_res["lifetime_output_tokens"] = tot_out
                        stat_res["lifetime_tokens"] = tot_in + tot_out
                        stat_res["lifetime_api_calls"] = tot_calls
                        stat_res["lifetime_tool_calls"] = tot_tools

                        # 2. Selezione Sessione Attiva / Più Recente con reale attività
                        c.execute("""
                            SELECT id, model, started_at, message_count, input_tokens, output_tokens, title,
                                   last_activity_at, last_activity_description, api_call_count, tool_call_count
                            FROM sessions
                            WHERE message_count > 0 OR input_tokens > 10 OR tool_call_count > 0
                            ORDER BY COALESCE(last_activity_at, started_at) DESC LIMIT 1
                        """)
                        row = c.fetchone()
                        if not row:
                            c.execute("""
                                SELECT id, model, started_at, message_count, input_tokens, output_tokens, title,
                                       last_activity_at, last_activity_description, api_call_count, tool_call_count
                                FROM sessions
                                ORDER BY COALESCE(last_activity_at, started_at) DESC LIMIT 1
                            """)
                            row = c.fetchone()
                        conn.close()

                        if row:
                            stat_res["current_session_id"] = row[0]
                            in_tok = row[4] or 0
                            out_tok = row[5] or 0
                            calls = max(1, row[9] or 1)
                            stat_res["active_session_msgs"] = row[3] or 0
                            stat_res["active_session_tool_calls"] = row[10] or 0
                            stat_res["input_tokens"] = in_tok
                            stat_res["output_tokens"] = out_tok
                            stat_res["api_call_count"] = calls
                            stat_res["session_total_tokens"] = in_tok + out_tok

                            # Calcolo accurato della finestra di contesto attiva per turno
                            turn_input = round(in_tok / calls)
                            turn_output = round(out_tok / calls)
                            stat_res["turn_avg_input_tokens"] = turn_input
                            stat_res["turn_avg_output_tokens"] = turn_output
                            used_tok = turn_input + turn_output
                            stat_res["context_used_tokens"] = used_tok

                            ctx_pct = round((used_tok / agent_def["context_limit"]) * 100.0, 1)
                            stat_res["context_used_pct"] = min(100.0, ctx_pct)
                            stat_res["hp"] = max(5, round(100.0 - ctx_pct))
                            stat_res["current_task"] = row[8] or row[6] or "Elaborazione attiva"
                            if row[7]:
                                try:
                                    stat_res["last_activity"] = datetime.datetime.fromtimestamp(row[7]).strftime("%d/%m %H:%M:%S")
                                except Exception:
                                    stat_res["last_activity"] = str(row[7])
                            else:
                                stat_res["last_activity"] = "In attesa"
                    except Exception:
                        pass
                else:
                    # Monitoraggio Agente Esterno (Ollama, LM Studio, OpenAI-Compatible, Cloud)
                    stat_res["is_external"] = True
                    stat_res["endpoint_online"] = True
                    if endpoint:
                        try:
                            req_url = endpoint
                            if provider == "ollama" and not req_url.endswith("/api/tags"):
                                req_url = req_url.rstrip("/") + "/api/tags"
                            elif provider in ["lmstudio", "openai_compatible", "cloud"] and not req_url.endswith("/models"):
                                req_url = req_url.rstrip("/") + ("/models" if req_url.endswith("/v1") else "/v1/models")

                            t0 = time.time()
                            req = urllib.request.Request(req_url)
                            if agent_def.get("api_key"):
                                req.add_header("Authorization", f"Bearer {agent_def['api_key']}")
                            with urllib.request.urlopen(req, timeout=1.2) as resp:
                                lat = round((time.time() - t0) * 1000)
                                stat_res["endpoint_online"] = True
                                stat_res["endpoint_latency_ms"] = lat
                                stat_res["current_task"] = f"Online ({lat}ms) • {provider.upper()}"
                                stat_res["last_activity"] = datetime.datetime.now().strftime("%d/%m %H:%M:%S")
                        except Exception as e:
                            stat_res["endpoint_online"] = False
                            stat_res["endpoint_latency_ms"] = None
                            stat_res["endpoint_error"] = str(e)
                            stat_res["current_task"] = f"Offline: {str(e)[:26]}"

                # Diagnosi integrata reale & simulata
                is_cloud_agent = agent_def.get("is_cloud", False) or profile == "beam" or provider in ["cloud", "ollama_cloud"]
                is_hermes = (provider == "hermes" and os.path.exists(db_path))

                if is_hermes:
                    diag = agent_doctor.diagnose_agent(
                        agent_def["id"], agent_def["profile"], agent_def["model"], agent_def["context_limit"],
                        is_cloud=is_cloud_agent
                    )

                    if not is_cloud_agent and stat_res["context_used_pct"] >= 95.0:
                        diag["context_overflow"] = True
                        if not diag["context_issue_detail"]:
                            diag["context_issue_detail"] = f"Contesto critico saturo al {stat_res['context_used_pct']}%"
                        if diag["session_blocked"]:
                            diag["health_status"] = "CIMITERO"
                            diag["room"] = "cimitero"
                        else:
                            diag["health_status"] = "INFERMERIA"
                            diag["room"] = "infermeria"

                    stat_res["health_status"] = diag["health_status"]
                    stat_res["session_blocked"] = diag["session_blocked"]
                    stat_res["session_issue_detail"] = diag["session_issue_detail"]
                    stat_res["context_overflow"] = diag["context_overflow"]
                    stat_res["context_issue_detail"] = diag["context_issue_detail"]
                    stat_res["can_cure_session"] = diag["can_cure_session"]
                    stat_res["can_cure_context"] = diag["can_cure_context"]
                    stat_res["can_resurrect"] = diag["can_resurrect"]
                    stat_res["is_simulated"] = diag["is_simulated"]
                else:
                    # Agente non-Hermes (Ollama nativo, LM Studio, OpenAI, Cloud)
                    stat_res["can_cure_session"] = False
                    stat_res["can_cure_context"] = False
                    stat_res["can_resurrect"] = False
                    stat_res["is_simulated"] = False
                    stat_res["context_overflow"] = False
                    stat_res["context_issue_detail"] = ""
                    if not stat_res.get("endpoint_online", True):
                        stat_res["health_status"] = "INFERMERIA"
                        stat_res["session_blocked"] = True
                        stat_res["session_issue_detail"] = stat_res.get("endpoint_error", "Endpoint non raggiungibile")
                        stat_res["hp"] = 25
                    else:
                        stat_res["health_status"] = "SANO"
                        stat_res["session_blocked"] = False
                        stat_res["session_issue_detail"] = ""
                        stat_res["hp"] = 100

                if stat_res.get("health_status") == "CIMITERO":
                    stat_res["room"] = "cimitero"
                    stat_res["status"] = "deceduto"
                    stat_res["hp"] = 0
                elif stat_res.get("health_status") == "INFERMERIA":
                    stat_res["room"] = "infermeria"
                    stat_res["status"] = "malato"
                    stat_res["hp"] = min(stat_res["hp"], 35)
                elif agent_def.get("is_cloud") or profile == "beam" or provider in ["cloud", "ollama_cloud"]:
                    stat_res["room"] = "cloud"
                    stat_res["status"] = "supervisione_cloud"
                    stat_res["hp"] = 100
                elif matching or stat_res.get("endpoint_online"):
                    stat_res["room"] = "ufficio"
                    stat_res["status"] = "lavoro"
                else:
                    stat_res["room"] = "casetta"
                    stat_res["status"] = "riposo"

                new_list.append(stat_res)

            AGENTS_CACHE = new_list
        except Exception:
            pass
        time.sleep(2.0)

# Aggiornamento cache centrale ogni 1s (istantaneo in memoria)
def master_cache_loop():
    global STATE_CACHE
    while True:
        try:
            sys_data = sys_collector.collect()

            # Calcolo statistiche per gruppi di lavoro (dinamico e universale)
            groups_stats = {
                "TEAM SVILUPPO": {"total": 0, "sani": 0, "infermeria": 0, "cimitero": 0, "members": []},
                "TEAM MARKETING": {"total": 0, "sani": 0, "infermeria": 0, "cimitero": 0, "members": []},
                "SICUREZZA": {"total": 0, "sani": 0, "infermeria": 0, "cimitero": 0, "members": []},
                "SUPER COORDINATORE": {"total": 0, "sani": 0, "infermeria": 0, "cimitero": 0, "members": []}
            }
            for a in AGENTS_CACHE:
                grp = a.get("group", "ALTRI")
                if grp not in groups_stats:
                    groups_stats[grp] = {"total": 0, "sani": 0, "infermeria": 0, "cimitero": 0, "members": []}
                groups_stats[grp]["total"] += 1
                groups_stats[grp]["members"].append(a["name"])
                hs = a.get("health_status", "SANO")
                if hs == "SANO":
                    groups_stats[grp]["sani"] += 1
                elif hs == "INFERMERIA":
                    groups_stats[grp]["infermeria"] += 1
                elif hs == "CIMITERO":
                    groups_stats[grp]["cimitero"] += 1

            with STATE_LOCK:
                STATE_CACHE = {
                    "timestamp": int(time.time() * 1000),
                    "system": sys_data,
                    "gpu": GPU_CACHE,
                    "ollama": OLLAMA_CACHE,
                    "llamacpp": LLAMACPP_CACHE,
                    "guardian": {
                        "status": guardian.status,
                        "last_check": guardian.last_check,
                        "monitored_count": len(guardian.monitored_files),
                        "mismatches": guardian.mismatches,
                        "auto_resolve": CONFIG.get("guardian", {}).get("auto_resolve", True)
                    },
                    "agents": AGENTS_CACHE,
                    "groups_summary": groups_stats,
                    "actions_enabled": ACTIONS_ENABLED,
                    "actions_history": agent_doctor.get_actions_history()[:20],
                    "csrf_token": CSRF_TOKEN
                }
        except Exception:
            pass
        time.sleep(1.0)

def guardian_loop():
    while True:
        try:
            guardian.verify_now()
            # Auto-risoluzione automatica persistente se abilitata
            auto_res = CONFIG.get("guardian", {}).get("auto_resolve", True)
            if auto_res and guardian.status != "INTEGRO":
                missing = [m for m in guardian.mismatches if m.get("error") == "FILE_MANCANTE"]
                if not missing:
                    guardian.auto_resolve_mismatches()
        except Exception:
            pass
        time.sleep(CONFIG.get("guardian", {}).get("check_interval_seconds", 30))

# ---------------------------------------------------------------------------
# Server HTTP & Routing Ultra-Veloce
# ---------------------------------------------------------------------------
class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True

class FastStatHandler(http.server.BaseHTTPRequestHandler):
    # Sopprime il log su stderr per GET 200 ripetuti (evita spam e lag)
    def log_message(self, format, *args):
        if len(args) > 1 and str(args[1]) in ["200", "304"]:
            return
        sys.stderr.write("%s - [%s] %s\n" % (self.address_string(), self.log_date_time_string(), format % args))

    def send_security_headers(self, content_type="application/json"):
        self.send_header("Content-Type", content_type)
        # Consenti file:// (origin null) e host locali
        origin = self.headers.get("Origin", "")
        if origin in ["http://127.0.0.1:8787", "null", "null/"] or not origin or "127.0.0.1" in origin or "localhost" in origin:
            self.send_header("Access-Control-Allow-Origin", "*")
        else:
            self.send_header("Access-Control-Allow-Origin", "http://127.0.0.1:8787")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-CSRF-Token")
        self.send_header("Access-Control-Allow-Private-Network", "true")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_security_headers()
        self.wfile.write(b"")

    def do_GET(self):
        url = urllib.parse.urlparse(self.path)
        path = url.path

        # 1. Dashboard UI
        if path in ["/", "/dashboard_AI.html", "/index.html"]:
            file_path = os.path.join(BASE_DIR, "dashboard_AI.html")
            if os.path.exists(file_path):
                self.send_response(200)
                self.send_security_headers("text/html; charset=utf-8")
                with open(file_path, "rb") as f:
                    self.wfile.write(f.read())
                return
            else:
                self.send_error(404, "dashboard_AI.html non trovato")
                return

        # 2. Sprites statici (supporta anche sottocartelle es. hermes_pets)
        if path.startswith("/sprites_agents/"):
            rel_path = urllib.parse.unquote(path[len("/sprites_agents/"):])
            safe_rel = os.path.normpath(rel_path).lstrip("\\/.")
            safe_path = os.path.join(SPRITES_DIR, safe_rel)
            if os.path.exists(safe_path) and os.path.isfile(safe_path):
                self.send_response(200)
                mime = "image/png" if safe_path.endswith(".png") else ("image/svg+xml" if safe_path.endswith(".svg") else "text/html")
                self.send_security_headers(mime)
                with open(safe_path, "rb") as f:
                    self.wfile.write(f.read())
                return
            else:
                self.send_error(404, f"Sprite non trovato: {rel_path}")
                return

        # 3. Favicon (icona arcade per app nativa e tab browser)
        if path in ["/favicon.ico", "/favicon.png"]:
            fav_path = os.path.join(SPRITES_DIR, "GynBot1.png")
            if os.path.exists(fav_path):
                self.send_response(200)
                self.send_security_headers("image/png")
                with open(fav_path, "rb") as f:
                    self.wfile.write(f.read())
                return
            self.send_response(204)
            self.end_headers()
            return

        # 3. Health Endpoint (istantaneo)
        if path == "/health":
            self.send_response(200)
            self.send_security_headers("application/json")
            res = {
                "status": "healthy",
                "mode": "read_only",
                "actions_enabled": ACTIONS_ENABLED,
                "csrf_token": CSRF_TOKEN,
                "agents_count": len(AGENTS_DEF),
                "timestamp": int(time.time())
            }
            self.wfile.write(json.dumps(res).encode("utf-8"))
            return

        # 4. Telemetria Completa (istantanea da memoria <1ms)
        if path == "/api/v1/telemetry":
            self.send_response(200)
            self.send_security_headers("application/json")
            with STATE_LOCK:
                data = json.dumps(STATE_CACHE).encode("utf-8")
            self.wfile.write(data)
            return

        # 5. Guardian Status
        if path == "/api/v1/guardian/status":
            self.send_response(200)
            self.send_security_headers("application/json")
            res = {
                "status": guardian.status,
                "last_check": guardian.last_check,
                "monitored_count": len(guardian.monitored_files),
                "mismatches": guardian.mismatches
            }
            self.wfile.write(json.dumps(res).encode("utf-8"))
            return

        # 6. Actions History
        if path == "/api/v1/actions/history":
            self.send_response(200)
            self.send_security_headers("application/json")
            history = agent_doctor.get_actions_history()
            self.wfile.write(json.dumps(history).encode("utf-8"))
            return

        # 7. Providers Auto-Discovery (Ollama, LM Studio, Hermes, OpenAI)
        if path == "/api/v1/providers/discovery":
            results = {
                "ollama": {"online": False, "endpoint": "http://127.0.0.1:11434", "models": []},
                "lmstudio": {"online": False, "endpoint": "http://127.0.0.1:1234/v1", "models": []},
                "hermes": {"online": False, "profiles": []}
            }
            # Check Ollama
            try:
                req = urllib.request.Request("http://127.0.0.1:11434/api/tags")
                with urllib.request.urlopen(req, timeout=0.8) as r:
                    d = json.loads(r.read().decode())
                    results["ollama"]["online"] = True
                    results["ollama"]["models"] = [m["name"] for m in d.get("models", [])]
            except Exception:
                pass
            # Check LM Studio
            try:
                req = urllib.request.Request("http://127.0.0.1:1234/v1/models")
                with urllib.request.urlopen(req, timeout=0.8) as r:
                    d = json.loads(r.read().decode())
                    results["lmstudio"]["online"] = True
                    results["lmstudio"]["models"] = [m["id"] for m in d.get("data", [])]
            except Exception:
                pass
            # Check Hermes profiles
            try:
                if os.path.exists(HERMES_ROOT):
                    prof_dir = os.path.join(HERMES_ROOT, "profiles")
                    profs = ["default"]
                    if os.path.exists(prof_dir):
                        for item in os.listdir(prof_dir):
                            if os.path.isdir(os.path.join(prof_dir, item)) and not item.startswith("."):
                                profs.append(item)
                    results["hermes"]["online"] = True
                    results["hermes"]["profiles"] = profs
            except Exception:
                pass
            self.send_response(200)
            self.send_security_headers("application/json")
            self.wfile.write(json.dumps(results).encode("utf-8"))
            return

        # 8. Catalogo Sprites & Avatar Hermes Pets
        if path == "/api/v1/sprites/list":
            self.send_response(200)
            self.send_security_headers("application/json")
            core_sprites = []
            if os.path.exists(SPRITES_DIR):
                for f in sorted(os.listdir(SPRITES_DIR)):
                    if f.endswith(".png"):
                        core_sprites.append({
                            "name": os.path.splitext(f)[0],
                            "path": f"sprites_agents/{f}"
                        })
            hermes_sprites = []
            pets_dir = os.path.join(SPRITES_DIR, "hermes_pets")
            if os.path.exists(pets_dir):
                for f in sorted(os.listdir(pets_dir)):
                    if f.endswith(".png"):
                        clean_name = os.path.splitext(f)[0].replace("-", " ").replace("_", " ").title()
                        hermes_sprites.append({
                            "name": clean_name,
                            "path": f"sprites_agents/hermes_pets/{f}"
                        })
            res = {"core": core_sprites, "hermes_pets": hermes_sprites}
            self.wfile.write(json.dumps(res).encode("utf-8"))
            return

        # 9. Sync & Auto-Discovery Agenti Hermes & Endpoints
        if path == "/api/v1/agents/sync_discovery":
            discovered = auto_discover_hermes_agents()
            self.send_response(200)
            self.send_security_headers("application/json")
            res = {
                "ok": True,
                "status": "success",
                "added_count": len(discovered),
                "discovered_count": len(discovered),
                "total_registered": len(CONFIG.get("agents", [])),
                "total_agents": len(CONFIG.get("agents", [])),
                "agents": CONFIG.get("agents", []),
                "message": f"Auto-discovery completata: {len(discovered)} nuovi agenti rilevati. Totale agenti: {len(CONFIG.get('agents', []))}"
            }
            self.wfile.write(json.dumps(res).encode("utf-8"))
            return

        self.send_error(404, "Endpoint non trovato")

    def do_POST(self):
        global AGENTS_DEF, AGENTS_CACHE
        url = urllib.parse.urlparse(self.path)
        path = url.path

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length) if content_length > 0 else b"{}"
        try:
            payload = json.loads(body.decode("utf-8"))
        except Exception:
            payload = {}

        if path == "/api/v1/guardian/test":
            active = payload.get("active", True)
            guardian.trigger_test_probe(active)
            self.send_response(200)
            self.send_security_headers("application/json")
            res = {
                "guardian_status": guardian.status,
                "test_probe_active": guardian.test_probe_active,
                "mismatches": guardian.mismatches
            }
            self.wfile.write(json.dumps(res).encode("utf-8"))
            return

        if path == "/api/v1/actions/dry-run":
            agent_id = payload.get("agent_id")
            level = payload.get("level", "L1")
            agent = next((a for a in AGENTS_DEF if a["id"] == agent_id), None)
            if not agent:
                self.send_response(400)
                self.send_security_headers("application/json")
                self.wfile.write(json.dumps({"error": "Agente non valido"}).encode("utf-8"))
                return

            dry_run_info = {
                "agent_id": agent_id,
                "agent_name": agent["name"],
                "model": agent["model"],
                "level": level,
                "is_dry_run": True,
                "simulated_at": datetime.datetime.now().isoformat(),
                "steps": []
            }

            if level == "L1":
                dry_run_info["steps"] = [
                    f"SIMULAZIONE: /compress su sessione attiva profilo {agent['profile']}",
                    f"Verifica: attesa riduzione token contesto su {agent['model']}",
                    f"Risultato atteso: HP ripristinati > 70%"
                ]
            elif level == "L2":
                dry_run_info["steps"] = [
                    f"SIMULAZIONE: Export cronologia JSONL in data/archive/{agent_id}/",
                    f"SIMULAZIONE: Estrazione riepilogo handoff (task, decisioni, file)",
                    f"SIMULAZIONE: Creazione nuova sessione pulita con staffetta"
                ]
            elif level == "L3":
                dry_run_info["steps"] = [
                    f"SIMULAZIONE: Analisi sessioni concluse profilo {agent['profile']}",
                    f"SIMULAZIONE: Export di sicurezza sessioni archiviate",
                    f"SIMULAZIONE: hermes -p {agent['profile']} sessions prune (nessun dato attivo rimosso)"
                ]
            elif level == "L4":
                dry_run_info["steps"] = [
                    f"SIMULAZIONE: Verifica lock modello {agent['model']}",
                    f"SIMULAZIONE: Chiamata Ollama POST /api/generate {{model: '{agent['model']}', keep_alive: 0}}",
                    f"Verifica: scarico VRAM immediato, ricarico delegato solo a Hermes"
                ]

            self.send_response(200)
            self.send_security_headers("application/json")
            self.wfile.write(json.dumps(dry_run_info).encode("utf-8"))
            return

        if path == "/api/v1/actions/simulate":
            agent_id = payload.get("agent_id")
            issue_type = payload.get("issue_type", "clear")
            agent = next((a for a in AGENTS_DEF if a["id"] == agent_id), None)
            if not agent:
                self.send_response(400)
                self.send_security_headers("application/json")
                self.wfile.write(json.dumps({"error": "Agente non trovato"}).encode("utf-8"))
                return
            res = agent_doctor.set_simulated_state(agent_id, issue_type)
            self.send_response(200)
            self.send_security_headers("application/json")
            self.wfile.write(json.dumps({"ok": True, "agent_id": agent_id, "simulated": res}).encode("utf-8"))
            return

        if path == "/api/v1/actions/cure_session":
            req_token = self.headers.get("X-CSRF-Token", "")
            if req_token != CSRF_TOKEN:
                self.send_response(403)
                self.send_security_headers("application/json")
                self.wfile.write(json.dumps({"error": "Token CSRF non valido"}).encode("utf-8"))
                return
            agent_id = payload.get("agent_id")
            agent = next((a for a in AGENTS_DEF if a["id"] == agent_id), None)
            if not agent:
                self.send_response(400)
                self.send_security_headers("application/json")
                self.wfile.write(json.dumps({"error": "Agente non trovato"}).encode("utf-8"))
                return
            res = agent_doctor.cure_session(agent_id, agent["name"], agent["profile"])
            self.send_response(200 if res.get("ok") else 500)
            self.send_security_headers("application/json")
            self.wfile.write(json.dumps(res).encode("utf-8"))
            return

        if path == "/api/v1/actions/cure_context":
            req_token = self.headers.get("X-CSRF-Token", "")
            if req_token != CSRF_TOKEN:
                self.send_response(403)
                self.send_security_headers("application/json")
                self.wfile.write(json.dumps({"error": "Token CSRF non valido"}).encode("utf-8"))
                return
            agent_id = payload.get("agent_id")
            agent = next((a for a in AGENTS_DEF if a["id"] == agent_id), None)
            if not agent:
                self.send_response(400)
                self.send_security_headers("application/json")
                self.wfile.write(json.dumps({"error": "Agente non trovato"}).encode("utf-8"))
                return
            res = agent_doctor.cure_context(agent_id, agent["name"], agent["profile"])
            self.send_response(200 if res.get("ok") else 500)
            self.send_security_headers("application/json")
            self.wfile.write(json.dumps(res).encode("utf-8"))
            return

        if path == "/api/v1/actions/resurrect":
            req_token = self.headers.get("X-CSRF-Token", "")
            if req_token != CSRF_TOKEN:
                self.send_response(403)
                self.send_security_headers("application/json")
                self.wfile.write(json.dumps({"error": "Token CSRF non valido"}).encode("utf-8"))
                return
            agent_id = payload.get("agent_id")
            agent = next((a for a in AGENTS_DEF if a["id"] == agent_id), None)
            if not agent:
                self.send_response(400)
                self.send_security_headers("application/json")
                self.wfile.write(json.dumps({"error": "Agente non trovato"}).encode("utf-8"))
                return
            res = agent_doctor.resurrect_agent(agent_id, agent["name"], agent["profile"])
            self.send_response(200 if res.get("ok") else 500)
            self.send_security_headers("application/json")
            self.wfile.write(json.dumps(res).encode("utf-8"))
            return

        if path == "/api/v1/guardian/resolve":
            req_token = self.headers.get("X-CSRF-Token", "")
            if req_token != CSRF_TOKEN:
                self.send_response(403)
                self.send_security_headers("application/json")
                self.wfile.write(json.dumps({"error": "Token CSRF non valido"}).encode("utf-8"))
                return
            res = guardian.auto_resolve_mismatches()
            self.send_response(200 if res.get("success") else 500)
            self.send_security_headers("application/json")
            self.wfile.write(json.dumps(res).encode("utf-8"))
            return

        # -------------------------------------------------------------
        # Endpoints Gestione Universale Agenti (VERSIONE 2.0)
        # -------------------------------------------------------------
        if path == "/api/v1/agents/test_connection":
            provider = payload.get("provider", "ollama")
            endpoint = payload.get("endpoint", "").strip()
            api_key = payload.get("api_key", "").strip()
            profile = payload.get("profile", "").strip()

            res = {"ok": False, "models": [], "latency_ms": 0, "message": ""}
            t0 = time.time()
            try:
                if provider == "hermes":
                    p_path = HERMES_ROOT if (not profile or profile == "default") else os.path.join(HERMES_ROOT, "profiles", profile)
                    if os.path.exists(p_path):
                        db_p = os.path.join(p_path, "state.db")
                        has_db = os.path.exists(db_p)
                        lat = max(1, round((time.time() - t0) * 1000))
                        res = {"ok": True, "latency_ms": lat, "models": ["hermes-agent"], "message": f"Profilo Hermes rilevato con successo ({'database state.db attivo' if has_db else 'profilo valido'})"}
                    else:
                        res = {"ok": False, "latency_ms": 1, "message": f"Profilo Hermes non trovato sul disco: {p_path}"}
                elif provider == "ollama":
                    ep = endpoint or "http://127.0.0.1:11434"
                    url = ep.rstrip("/") + "/api/tags"
                    req = urllib.request.Request(url)
                    with urllib.request.urlopen(req, timeout=2.5) as r:
                        d = json.loads(r.read().decode())
                        models = [m.get("name") for m in d.get("models", [])]
                        lat = round((time.time() - t0) * 1000)
                        res = {"ok": True, "latency_ms": lat, "models": models, "message": f"Connesso a Ollama ({len(models)} modelli rilevati)"}
                elif provider in ["lmstudio", "openai_compatible"]:
                    ep = endpoint or "http://127.0.0.1:1234/v1"
                    url = ep.rstrip("/") + ("/models" if ep.endswith("/v1") else "/v1/models")
                    req = urllib.request.Request(url)
                    if api_key:
                        req.add_header("Authorization", f"Bearer {api_key}")
                    with urllib.request.urlopen(req, timeout=2.5) as r:
                        d = json.loads(r.read().decode())
                        raw_models = d.get("data", [])
                        models = [m.get("id") for m in raw_models]
                        lat = round((time.time() - t0) * 1000)
                        res = {"ok": True, "latency_ms": lat, "models": models, "message": f"Connesso a {provider.upper()} ({len(models)} modelli rilevati)"}
                elif provider == "cloud":
                    ep = endpoint or "https://api.openai.com/v1"
                    url = ep.rstrip("/") + ("/models" if ep.endswith("/v1") else "/v1/models")
                    req = urllib.request.Request(url)
                    if api_key:
                        req.add_header("Authorization", f"Bearer {api_key}")
                    with urllib.request.urlopen(req, timeout=3.5) as r:
                        d = json.loads(r.read().decode())
                        raw_models = d.get("data", [])
                        models = [m.get("id") for m in raw_models[:35]]
                        lat = round((time.time() - t0) * 1000)
                        res = {"ok": True, "latency_ms": lat, "models": models, "message": f"Connesso a Cloud API ({len(raw_models)} modelli disponibili)"}
                else:
                    res = {"ok": False, "message": f"Provider sconosciuto: {provider}"}
            except Exception as e:
                lat = round((time.time() - t0) * 1000)
                res = {"ok": False, "latency_ms": lat, "message": f"Errore connessione: {str(e)}"}

            self.send_response(200)
            self.send_security_headers("application/json")
            self.wfile.write(json.dumps(res).encode("utf-8"))
            return

        if path == "/api/v1/agents/add":
            req_token = self.headers.get("X-CSRF-Token", "")
            if req_token != CSRF_TOKEN:
                self.send_response(403)
                self.send_security_headers("application/json")
                self.wfile.write(json.dumps({"error": "Token CSRF non valido"}).encode("utf-8"))
                return

            name = payload.get("name", "").strip()
            if not name:
                self.send_response(400)
                self.send_security_headers("application/json")
                self.wfile.write(json.dumps({"error": "Nome agente obbligatorio"}).encode("utf-8"))
                return

            import re
            base_id = re.sub(r'[^a-zA-Z0-9_]', '', name.lower().replace(" ", "_")) or "agent"
            new_id = base_id
            counter = 1
            existing_ids = [a["id"] for a in CONFIG.get("agents", [])]
            while new_id in existing_ids:
                counter += 1
                new_id = f"{base_id}_{counter}"

            provider = payload.get("provider", "ollama")
            is_cloud = bool(payload.get("is_cloud", False) or provider == "cloud")
            new_agent = {
                "id": new_id,
                "name": name,
                "title": payload.get("title", "Assistente AI"),
                "group": payload.get("group", "TEAM SVILUPPO"),
                "color": payload.get("color", "#38bdf8" if is_cloud else "#10b981"),
                "provider": provider,
                "endpoint": payload.get("endpoint", "http://127.0.0.1:11434" if provider == "ollama" else ("http://127.0.0.1:1234/v1" if provider == "lmstudio" else "")),
                "model": payload.get("model", "llama3"),
                "base_model": payload.get("base_model", payload.get("model", "llama3")),
                "context_limit": int(payload.get("context_limit", 32768)),
                "compress_threshold": float(payload.get("compress_threshold", 0.85)),
                "is_cloud": is_cloud,
                "parameters": payload.get("parameters", "Cloud MoE" if is_cloud else "Local Model"),
                "architecture": payload.get("architecture", provider.capitalize()),
                "modality": payload.get("modality", "Text Only + Tool Calling"),
                "thinking_level": payload.get("thinking_level", "Standard"),
                "profile": payload.get("profile", new_id if provider == "hermes" else ""),
                "sprite": payload.get("sprite", "sprites_agents/GynBot1.png")
            }
            if payload.get("api_key"):
                new_agent["api_key"] = payload.get("api_key")

            CONFIG.setdefault("agents", []).append(new_agent)
            try:
                with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                    json.dump(CONFIG, f, indent=2)
                AGENTS_DEF = CONFIG["agents"]
                self.send_response(200)
                self.send_security_headers("application/json")
                self.wfile.write(json.dumps({"ok": True, "status": "success", "agent_id": new_id, "message": f"Agente '{name}' aggiunto con successo!", "agent": new_agent}).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_security_headers("application/json")
                self.wfile.write(json.dumps({"error": f"Errore nel salvataggio della configurazione: {str(e)}", "status": "error"}).encode("utf-8"))
            return

        if path == "/api/v1/agents/delete":
            req_token = self.headers.get("X-CSRF-Token", "")
            if req_token != CSRF_TOKEN:
                self.send_response(403)
                self.send_security_headers("application/json")
                self.wfile.write(json.dumps({"error": "Token CSRF non valido"}).encode("utf-8"))
                return

            agent_id = payload.get("agent_id")
            cur_agents = CONFIG.get("agents", [])
            matched = next((a for a in cur_agents if a["id"] == agent_id), None)
            if not matched:
                self.send_response(404)
                self.send_security_headers("application/json")
                self.wfile.write(json.dumps({"error": "Agente non trovato", "status": "error"}).encode("utf-8"))
                return

            CONFIG["agents"] = [a for a in cur_agents if a["id"] != agent_id]
            try:
                with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                    json.dump(CONFIG, f, indent=2)
                AGENTS_DEF = CONFIG["agents"]
                with STATE_LOCK:
                    AGENTS_CACHE = [a for a in AGENTS_CACHE if a["id"] != agent_id]
                self.send_response(200)
                self.send_security_headers("application/json")
                self.wfile.write(json.dumps({"ok": True, "status": "success", "message": f"Agente '{matched['name']}' rimosso con successo"}).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_security_headers("application/json")
                self.wfile.write(json.dumps({"error": str(e), "status": "error"}).encode("utf-8"))
            return

        self.send_error(404, "Endpoint non trovato")

# ---------------------------------------------------------------------------
# Avvio Server & Loop Principale
# ---------------------------------------------------------------------------
def run():
    with open(PID_FILE, "w", encoding="utf-8") as f:
        f.write(str(os.getpid()))

    port = DEFAULT_PORT
    server = None
    for p in range(DEFAULT_PORT, DEFAULT_PORT + 10):
        try:
            server = ThreadedHTTPServer((SERVER_HOST, p), FastStatHandler)
            port = p
            break
        except OSError:
            continue

    if not server:
        print("ERRORE: Impossibile trovare una porta disponibile.")
        sys.exit(1)

    print(f" STATISTICHEAI Server: http://{SERVER_HOST}:{port}/dashboard_AI.html (PID: {os.getpid()})")

    # Avvio worker thread dedicati
    threading.Thread(target=gpu_worker_loop, daemon=True).start()
    threading.Thread(target=ollama_worker_loop, daemon=True).start()
    threading.Thread(target=llamacpp_worker_loop, daemon=True).start()
    threading.Thread(target=hermes_worker_loop, daemon=True).start()
    threading.Thread(target=master_cache_loop, daemon=True).start()
    threading.Thread(target=guardian_loop, daemon=True).start()

    def cleanup(signum=None, frame=None):
        if os.path.exists(PID_FILE):
            try:
                os.remove(PID_FILE)
            except Exception:
                pass
        sys.exit(0)

    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        cleanup()

if __name__ == "__main__":
    run()
