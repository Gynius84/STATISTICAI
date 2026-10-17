---
name: statistiche
description: Open native STATISTICHEAI 16-bit dashboard monitor.
version: 2.0.0
author: Gyniu, Hermes Agent
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [monitoring, dashboard, retro, agent-telemetry, ollama]
---

# STATISTICHEAI Monitor Skill

Opens and controls the STATISTICHEAI 16-bit retro arcade AI monitoring dashboard for Hermes agents and Ollama (local + cloud models) in a dedicated native desktop application window.

## When to Use

- User asks to "open monitor", "show dashboard", "apri statistiche", "mostra monitoraggio", or check agent health/telemetry.
- Triggered by slash command `/statistiche` or `/monitor`.
- User wants to view real-time VRAM, tokens, session memory, or agent status without leaving Hermes.

## How to Run

Execute the launcher script through Python:

```bash
python scripts/open_monitor.py
```

Or invoke via command shortcut:
```bash
statistiche
```

## Quick Reference

| Action | Command |
|---|---|
| Open Native App | `python scripts/open_monitor.py` |
| Fast CLI | `statistiche` |
| Direct URL | `http://127.0.0.1:8888/dashboard_AI.html` |
| Health Check | `http://127.0.0.1:8888/health` |

## Procedure

1. Run `python scripts/open_monitor.py`.
2. The launcher automatically verifies if the background server daemon on port 8888 is active.
3. If not active, it launches `run_server.py` silently in the background with BelowNormal priority.
4. It launches the frameless native app window (Microsoft Edge or Google Chrome standalone mode) with 1480x920 dimensions.
5. Report to the user that the dashboard is open and state how many agents are currently monitored.

## Pitfalls

- Does not interfere with existing browser sessions: `http://127.0.0.1:8888/dashboard_AI.html` remains accessible simultaneously in any web browser.
- Operates under Zero-Touch rule: pure observer, never modifies model weights, prompt context, or system configurations.

## Verification

Run the script and check that JSON output confirms `"ok": true` and `"mode": "native_app"`.
