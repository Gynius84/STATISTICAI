---
name: statistiche
description: Open native STATISTICHEAI 16-bit dashboard monitor (v2.6, 11 active agents: 3 local llama.cpp Disco D: :9931 + 2 Ollama Cloud BEAM & NEMO + 3 NVIDIA NIM Cloud NEMOTRON, DEEPSEEK & DRAGO + 2 OpenRouter Cloud INKLING & LAGUNA + 1 Google AI Studio Cloud GEMINI, Quadruple Quantum Nuvoletta Portals, Real-Time 4-Room Routing Casetta/Ufficio/Infermeria/Cimitero, Live Quota 429 & Timeout 504 Clinical Diagnostics).
version: 2.6
author: Gyniu, Hermes Agent
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [monitoring, dashboard, retro, agent-telemetry, ollama, llamacpp, nvidia-nim, openrouter, google-ai-studio, radar-benchmark, moe, cloud-lightning, quad-cloud, agent-doctor]
---

# STATISTICHEAI Monitor Skill (v2.6)

Opens and controls the **STATISTICHEAI v2.6** 16-bit retro arcade AI monitoring dashboard for all **11 Hermes agents** across local & quadruple-cloud engines in a dedicated native desktop application window (`http://127.0.0.1:8888/dashboard_AI.html`).

### New in v2.6 (Real-Time Room Placement, Clinical Diagnostics & Local Router Optimization):
- **Real-Time 4-Room Routing (`LA CASETTA`, `L'UFFICIO`, `INFERMERIA`, `IL CIMITERO`)**:
  - **`LA CASETTA (RIPOSO)`**: Healthy (`SANO`) agents that are ready to operate at 100% but are **not actively executing a task right now** rest in `LA CASETTA`.
  - **`L'UFFICIO (LAVORO)`**: **Only** healthy agents that are **actively working right now** (live process in `runtime/active_sessions.json`, SQLite session turn within the last 90 seconds, or local model actively loaded in VRAM on `:9931` / `ollama ps`) appear in `L'UFFICIO`.
  - **`INFERMERIA (CURA)`**: Both Local and Cloud agents that are temporarily paused/injured due to recoverable issues — such as **HTTP 429 Free-Tier Quota Exceeded** (Google AI Studio / OpenRouter daily limit), **HTTP 504 Gateway Timeout** (NVIDIA NIM upstream timeout), or **orphaned session leases** — are automatically placed in **`INFERMERIA`** (`35/100 HP`) with detailed Italian diagnostic banners and 1-click **`🏥 CURA / RESET SESSIONE`**.
  - **`IL CIMITERO (CAMPO SANTO)`**: Reserved strictly for unrecoverable double-fault agents, with 1-click **`★ RESUSCITA (1-CLICK) ★`**.
- **Quadruple Quantum Vortex Nuvoletta Portals (11 Agents)**:
  - **Portal 1 — Ollama Cloud (`BEAM` 501B MoE & `NEMO` Nemotron-3 Ultra 550B MoE)**: Celestial cyan & turquoise quantum cloud.
  - **Portal 2 — NVIDIA NIM Cloud (`NEMOTRON` 550B MoE, `DEEPSEEK` V4.1 Flash, `DRAGO` GLM 5.3)**: Cyber emerald & NVIDIA green quantum cloud with live per-agent health indicators.
  - **Portal 3 — OpenRouter Cloud (`INKLING` Trinity Free & `LAGUNA` S-2.1 35B MoE Free)**: Cosmic indigo & violet quantum cloud.
  - **Portal 4 — Google AI Studio Cloud (`GEMINI` 3.5 Flash 1M CTX)**: Solar gold & amber quantum cloud.
- **Hardware-Optimized Local `llama.cpp` Router (`:9931`, Disco D:, RTX 4060 8GB)**:
  - Unified all local profiles (`GynBot1` Hermes-3 8B, `DARK CODER` Qwen2.5-Coder 14B, `VISION` Qwen2.5-VL 7B) onto `:9931` with `MaxLoadedModels: 1`, `q8_0` KV cache, `--fit-target 256 --flash-attn on`, and native Hermes/Qwen ChatML `<tools>`/`<tool_call>` Jinja template.

## When to Use

- User asks to "open monitor", "show dashboard", "apri statistiche", "mostra monitoraggio", or check agent health/telemetry/benchmarks/rooms.
- Triggered by slash command `/statistiche` or `/monitor`.
- User wants to view real-time VRAM, tokens, session memory, room placement (`Casetta` / `Ufficio` / `Infermeria` / `Cimitero`), or cloud status.

## How to Run

```bash
# Avvio monitor nativo Desktop
start "" "C:\Users\Gyniu\OneDrive\Desktop\start - STATISTICHEAI.lnk"

# Oppure tramite script dedicato
"C:\Users\Gyniu\AppData\Local\hermes\tools\python-3.14.7+20260901-win32-x64\python.exe" "C:\Users\Gyniu\OneDrive\Desktop\STATISTICAI\open_monitor.py"
```
