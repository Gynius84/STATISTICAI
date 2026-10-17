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

```bash
python scripts/open_monitor.py
```
