---
name: statistiche
description: Open native STATISTICHEAI 16-bit dashboard monitor (v2.4, 11 agents: 7 local llama.cpp + 2 cloud Ollama Beam & MiniMax + 2 cloud NVIDIA NIM DeepSeek & Drago, Dual Quantum Nuvoletta Portals, 81 NIM Models Integration, OpenCompass Radar Benchmarks, MoE & RTX 4060 TPS).
version: 2.4
author: Gyniu, Hermes Agent
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [monitoring, dashboard, retro, agent-telemetry, ollama, llamacpp, nvidia-nim, radar-benchmark, moe, cloud-lightning]
---

# STATISTICHEAI Monitor Skill (v2.4)

Opens and controls the STATISTICHEAI 16-bit retro arcade AI monitoring dashboard for the 11 optimized Hermes agents across hybrid local & multi-cloud engines (7 local models on llama.cpp port 9931 disk D:, plus 2 Cloud Lightning MoE models on Ollama port 11434: BEAM 501B MoE and MiniMax 3.1 Flash 456B MoE, plus 2 Cloud Titans on NVIDIA NIM Enterprise: DeepSeek V4.1 Flash 410B MoE and Drago GLM 5.3 130B) in a dedicated native desktop application window.

### New in v2.4:
- **NVIDIA Cloud NIM Enterprise Integration (81 Models)**:
  - Direct integration with NVIDIA Cloud NIM endpoints (`https://integrate.api.nvidia.com/v1`) accessing the full catalog of 81 state-of-the-art models with zero local GPU VRAM overhead.
  - Calibrated OpenCompass radar benchmarks and throughput telemetry for:
    - **`DEEPSEEK` (DeepSeek V4.1 Flash)**: 410B MoE (~28B active), 120+ tok/s throughput, 128K context, coding score 97, agentic 96.
    - **`DRAGO` (GLM 5.3)**: 130B Dense Hybrid Reasoner, 90+ tok/s, 128K context, reasoning score 98, knowledge 97.
- **Dual Quantum Vortex Nuvoletta Portals**:
  - **Portal 1 (Ollama Cloud Lightning)**: Celestial cyan & purple quantum vortex featuring BEAM 501B and MiniMax 3.1 Flash.
  - **Portal 2 (NVIDIA Cloud NIM Titans)**: High-energy cyber emerald & NVIDIA green quantum vortex featuring DeepSeek V4.1 Flash and Drago GLM 5.3 with live token throughput, 128K context monitors, and zero-swap cloud telemetry.
- **Auto-Discovery Engine 2.4 (Zero-Touch Self-Healing)**:
  - Robust sanitation for profile names, stripping quotation artifacts and resolving clean agent display names and descriptions.
  - Guaranteed avatar extraction from `profiles/<name>/assets/avatar.png` into dashboard sprites with dynamic canvas fallback.
  - Real-time catalog benchmark resolution with instant auto-tagging for any newly connected models out of the 81 NVIDIA NIM models or local engines.
- **Multi-Cloud Workflow Badge & Team Filters**:
  - Dynamic workflow indicator: `🔀 WORKFLOW: 🦙 LLAMA.CPP DISCO D: (7 MODELLI GGUF) + ☁ OLLAMA CLOUD (BEAM + MINIMAX) + ⚡ NVIDIA CLOUD NIM (DEEPSEEK + DRAGO • 81 MODELLI NIM) = 11 AGENTI`.
  - Filter bar buttons updated to support `TUTTI (11)`, `☁ TITANI CLOUD (4)`, and `⚡ NVIDIA NIM (2)`.

### Previous Features (v2.3.2):
- **Fast Radar Benchmark & Performance Sorter**: Instant one-click sorting of all agent cards directly from the filter bar (Speed TPS, Coding, Reasoning, Knowledge, Agentic, Vision, Alphabetical, Custom Drag & Drop).
- **Harmonious Divided HUD Layout Architecture**: Division 1 (System Hardware), Division 2 (Ollama Cloud), Division 3 (NVIDIA NIM Cloud) with zero-overflow viewport auto-scaling.

## When to Use

- User asks to "open monitor", "show dashboard", "apri statistiche", "mostra monitoraggio", or check agent health/telemetry/benchmarks.
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
| Benchmarks API | `http://127.0.0.1:8888/api/v1/models/benchmarks` |

## Procedure

1. Run `python scripts/open_monitor.py`.
2. The launcher automatically verifies if the background server daemon on port 8888 is active.
3. If not active, it launches `run_server.py` silently in the background with BelowNormal priority.
4. It launches the frameless native app window (Microsoft Edge or Google Chrome standalone mode) with 1480x920 dimensions.
5. Report to the user that the dashboard is open and state how many agents are currently monitored (11 agents: 7 local + 2 Ollama cloud + 2 NVIDIA NIM cloud).

## Pitfalls

- Does not interfere with existing browser sessions: `http://127.0.0.1:8888/dashboard_AI.html` remains accessible simultaneously in any web browser.
- Operates under Zero-Touch rule: pure observer, never modifies model weights, prompt context, or system configurations.

## Verification

Run the script and check that JSON output confirms `"ok": true` and `"mode": "native_app"`.
