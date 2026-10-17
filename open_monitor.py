"""
STATISTICHEAI - Native Desktop App & Hermes Bridge Launcher
Avvia il server in background (se non attivo) e apre la dashboard in modalità
finestra "App Nativa" standalone (frameless, zero barre browser, stile desktop app).
"""

import os
import sys
import time
import json
import urllib.request
import urllib.error
import subprocess
import webbrowser

V2_DIR = os.path.dirname(os.path.abspath(__file__))
SERVER_SCRIPT = os.path.join(V2_DIR, "run_server.py")
URL = "http://127.0.0.1:8888/dashboard_AI.html"
HEALTH_URL = "http://127.0.0.1:8888/health"

HERMES_PYTHON = r"C:\Users\Gyniu\AppData\Local\hermes\tools\python-3.14.7+20260901-win32-x64\python.exe"
HERMES_PYTHONW = r"C:\Users\Gyniu\AppData\Local\hermes\tools\python-3.14.7+20260901-win32-x64\pythonw.exe"

def is_server_online(timeout=0.8):
    try:
        req = urllib.request.Request(HEALTH_URL, headers={"User-Agent": "Launcher-Probe"})
        with urllib.request.urlopen(req, timeout=timeout) as res:
            if res.status == 200:
                data = json.loads(res.read().decode("utf-8"))
                return True, data.get("agents_count", 0)
    except Exception:
        pass
    return False, 0

def start_server_daemon():
    online, count = is_server_online(timeout=0.5)
    if online:
        return True, count, "Server gia' online su porta 8888"

    # Selezione interprete python headless
    py_exe = HERMES_PYTHONW if os.path.exists(HERMES_PYTHONW) else (
        HERMES_PYTHON if os.path.exists(HERMES_PYTHON) else sys.executable
    )

    DETACHED_PROCESS = 0x00000008
    CREATE_NEW_PROCESS_GROUP = 0x00000200
    CREATE_NO_WINDOW = 0x08000000
    flags = DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP | CREATE_NO_WINDOW

    try:
        subprocess.Popen(
            [py_exe, SERVER_SCRIPT],
            cwd=V2_DIR,
            creationflags=flags,
            close_fds=True
        )
    except Exception as e:
        # Fallback senza creationflags se non supportati
        try:
            subprocess.Popen([py_exe, SERVER_SCRIPT], cwd=V2_DIR)
        except Exception as e2:
            return False, 0, f"Errore avvio server: {e2}"

    # Attesa che il server risponda a /health (max 5 secondi)
    t0 = time.time()
    while time.time() - t0 < 5.0:
        time.sleep(0.3)
        online, count = is_server_online(timeout=0.5)
        if online:
            return True, count, "Server avviato con successo in background (porta 8888)"

    return False, 0, "Timeout durante l'avvio del server"

def find_native_browser():
    candidates = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
        os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%LocalAppData%\Microsoft\Edge\Application\msedge.exe"),
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None

def launch_native_window():
    browser = find_native_browser()
    if browser:
        args = [
            browser,
            f"--app={URL}",
            "--window-size=1480,920",
            "--window-position=120,60",
            "--disable-features=Translate"
        ]
        try:
            DETACHED_PROCESS = 0x00000008
            CREATE_NO_WINDOW = 0x08000000
            subprocess.Popen(args, creationflags=DETACHED_PROCESS | CREATE_NO_WINDOW)
            return True, f"Aperto in modalita' App Nativa via {os.path.basename(browser)}"
        except Exception as e:
            pass

    # Fallback su browser predefinito di sistema
    webbrowser.open(URL)
    return True, "Aperto nel browser predefinito di sistema"

def main():
    ok, count, msg = start_server_daemon()
    if not ok:
        print(f"[ERRORE] Impossibile avviare il monitoraggio: {msg}")
        sys.exit(1)

    app_ok, app_msg = launch_native_window()
    result = {
        "ok": True,
        "agents_monitored": count,
        "mode": "native_app" if "App Nativa" in app_msg else "browser",
        "url": URL,
        "message": f"STATISTICHEAI v2.0 attivo. {app_msg}. {count} agenti monitorati (Hermes + Ollama + Cloud)."
    }
    print(json.dumps(result, indent=2))
    return 0

if __name__ == "__main__":
    sys.exit(main())
