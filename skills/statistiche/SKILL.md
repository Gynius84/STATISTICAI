---
name: statistiche
description: Open native STATISTICHEAI 16-bit dashboard monitor (v2.7, 14 active agents: 4 local llama.cpp Disco D: :9931 + 10 Penta-Cloud Titans across Ollama Cloud, NVIDIA NIM, OpenRouter, Google AI Studio and OrcaRouter, 5 Quantum Nuvoletta Portals, Real-Time 4-Room Routing Casetta/Ufficio/Infermeria/Cimitero, Golden Snapshot Default & 1-Click Healing Engine).
version: 2.7
author: Gyniu, Hermes Agent
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [monitoring, dashboard, retro, agent-telemetry, ollama, llamacpp, nvidia-nim, openrouter, google-ai-studio, orcarouter, radar-benchmark, moe, penta-cloud, agent-doctor, golden-snapshot]
---

# STATISTICHEAI Monitor Skill (v2.7)

Opens and controls the **STATISTICHEAI v2.7** 16-bit retro arcade AI monitoring dashboard for all **14 Hermes agents** across local llama.cpp (:9931) & penta-cloud engines in a dedicated native desktop application window (`http://127.0.0.1:8888/dashboard_AI.html`).

### Architectural Overview (v2.7):
- **14 Total AI Agents (100% Operational & Verified)**:
  - **4 Local Engines (`llama.cpp` Router :9931, Disco D:, RTX 4060 GPU VRAM)**:
    - `GynBot1`: Hermes-3 Llama-3.1 8B (Q4_K_M) • Team Sviluppo
    - `VISION`: Qwen2.5-VL 7B Multimodal (Q4_K_M) • Team Visual Audit
    - `GEMMO`: Gemma-4 E4B-it (Q4_0, Draft-MTP) • Team Sviluppo
    - `NEMOHOUSE`: Nemotron-3.5-Bolt 4B (Q4_K_M) • Team Sviluppo
  - **10 Cloud Titans (0 MB VRAM Overhead)**:
    - `BEAM`: 501B MoE Cloud • 1M Context (1.048.576 tok) • Super Coordinatore (Ollama Cloud)
    - `NEMO`: Nemotron-3 Ultra 550B MoE • 256K Context • Team Ollama Cloud
    - `NEMOTRON`: Nemotron-3 Ultra 550B MoE • 128K Context • Team Cloud Titans (NVIDIA NIM)
    - `DEEPSEEK`: DeepSeek V4.1 Flash 410B MoE • 128K Context • Team Cloud Titans (NVIDIA NIM)
    - `DRAGO`: GLM 5.3 Hybrid Reasoner 130B Dense • 64K Context • Team Cloud Titans (NVIDIA NIM)
    - `INKLING`: Thinking Machines Inkling 70B • 128K Context • Team OpenRouter Cloud
    - `LAGUNA`: Poolside Laguna S-2.1 35B MoE • 128K Context • Team OpenRouter Cloud
    - `GEMINI`: Google Gemini 3.5 Flash Multimodal • 1M Context • Team Google AI Cloud
    - `DEEPPO4flash`: DeepSeek V4 Flash 410B MoE • 131K Context • Team Deep Thinking (OrcaRouter Cloud)
    - `DEEPPO41flash`: DeepSeek V4.1 Flash 410B MoE • 131K Context • Team Deep Thinking (OrcaRouter Cloud)
- **5 Quantum Nuvoletta Vortex Portals (Penta-Cloud Infrastructure)**:
  - **Portal 1 — Ollama Cloud**: Celestial cyan & turquoise plasma swirl (`BEAM` + `NEMO`).
  - **Portal 2 — NVIDIA NIM Cloud**: Cyber emerald & NVIDIA green plasma swirl (`NEMOTRON` + `DEEPSEEK` + `DRAGO`).
  - **Portal 3 — OpenRouter Cloud**: Cosmic indigo & violet plasma swirl (`INKLING` + `LAGUNA`).
  - **Portal 4 — Google AI Studio Cloud**: Solar gold & amber plasma swirl (`GEMINI` 3.5 Flash).
  - **Portal 5 — OrcaRouter Cloud**: Emerald mint & cyan plasma swirl (`DEEPPO4flash` + `DEEPPO41flash`).
- **Real-Time 4-Room Routing (`LA CASETTA`, `L'UFFICIO`, `INFERMERIA`, `IL CIMITERO`)**:
  - `LA CASETTA (RIPOSO)`: Healthy agents ready to operate, resting when not executing turns.
  - `L'UFFICIO (LAVORO)`: Only agents actively executing requests right now.
  - `INFERMERIA (CURA)`: Agents with minor recoverable issues (orphan leases, admission_conflict, context warning) with 1-click targeted cure.
  - `IL CIMITERO (CAMPO SANTO)`: Agents with double-faults, restored via 1-click `★ RESUSCITA ★`.
- **Golden Snapshot Default & Resurrection Engine**:
  - Immutable baseline snapshot in `snapshots/default_optimized_20261024/` with cryptographic SHA-256 checksums (`checksums.sha256`) and manifest.
  - Automatic backup before every cure/resurrection operation with zero data loss and automated rollback.

## When to Use

- User asks to "open monitor", "show dashboard", "apri statistiche", "mostra monitoraggio", or check agent health/telemetry/benchmarks/rooms.
- Triggered by slash command `/statistiche` or `/monitor`.
- User wants to view real-time VRAM, tokens, session memory, room placement (`Casetta` / `Ufficio` / `Infermeria` / `Cimitero`), or cloud status.

## How to Run

```bash
# Avvio monitor nativo Desktop
start "" "C:\Users\Gyniu\OneDrive\Desktop\start - STATISTICHEAI.lnk"

# Oppure tramite script dedicato
"C:\Users\Gyniu\AppData\Local\hermes\tools\python-3.14.7+20260901-win32-x64\python.exe" "C:\Users\Gyniu\Desktop\progetti ai\STATISTICAI\open_monitor.py"
```
