"""
Hermes Skill Bridge - STATISTICHEAI
Launcher dinamico cross-path per apertura dashboard in modalita' App Nativa.
"""
import sys
import os
import subprocess

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CANDIDATE_PATHS = [
    os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", "..", "open_monitor.py")),
    os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", "open_monitor.py")),
    r"C:\Users\Gyniu\Desktop\progetti ai\STATISTICHEAI\VERSIONE2.0\open_monitor.py",
]

def main():
    target = None
    for p in CANDIDATE_PATHS:
        if os.path.exists(p):
            target = p
            break

    if target:
        res = subprocess.run([sys.executable, target] + sys.argv[1:], capture_output=True, text=True)
        if res.stdout:
            print(res.stdout.strip())
        if res.stderr:
            print(res.stderr.strip(), file=sys.stderr)
        return res.returncode
    else:
        print("[ERRORE] File open_monitor.py master non trovato.", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
