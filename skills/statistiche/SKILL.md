---
name: statistiche
description: Open native STATISTICHEAI 16-bit dashboard monitor (v2.3.2, 9 agents, 7 local llama.cpp + 2 cloud Ollama Beam & MiniMax, Dual Cloud Titans Quantum Portal, Radar Benchmark OpenCompass, MoE & RTX 4060 TPS).
version: 2.3.2
author: Gyniu, Hermes Agent
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [monitoring, dashboard, retro, agent-telemetry, ollama, llamacpp, radar-benchmark, moe, cloud-lightning]
---

# STATISTICHEAI Monitor Skill (v2.3.2)

Opens and controls the STATISTICHEAI 16-bit retro arcade AI monitoring dashboard for the 9 optimized Hermes agents across hybrid local & cloud engines (7 local models on llama.cpp port 9931 disk D:, plus 2 Cloud Lightning MoE models on Ollama port 11434: BEAM 501B MoE and MiniMax 3.1 Flash 456B MoE) in a dedicated native desktop application window.

### New in v2.3.2:
- **Fast Radar Benchmark & Performance Sorter**: Instant one-click sorting of all agent cards directly from the filter bar based on benchmark dimensions:
  - 🚀 **Speed / Throughput (TPS)**: Sort by real-time hardware inference tokens/sec on RTX 4060 or Cloud Lightning.
  - 💻 **Coding (HumanEval)**: Sort by programming benchmark precision.
  - 🧠 **Reasoning (MATH/Logic)**: Sort by analytical and mathematical benchmark depth.
  - 📚 **Knowledge (MMLU-Pro)**: Sort by comprehensive knowledge and encyclopedic accuracy.
  - ⚡ **Agentic (Tool Calling)**: Sort by tool execution and workflow autonomy.
  - 👁️ **Vision (VLM Perception)**: Sort by multimodal visual capabilities.
  - 🔤 **Alphabetical (A-Z)** and 🔀 **Custom Drag & Drop** restoration.
- **Harmonious Divided HUD Layout Architecture**: Completely eliminated grid overflow by dividing `#box-hud-metrics` into two distinct, dedicated architectural divisions:
  - **Division 1 (Hardware & Local Inference)**: 9 local system metrics (CPU, RAM, GPU, VRAM, Ollama C:, llama.cpp D:, Team, Sviluppo, Marketing) in an auto-fitting balanced grid.
  - **Division 2 (Cloud Titans & Portale Vortice Quantico)**: Dedicated flex tier accommodating BEAM (501B), MiniMax (456B), and an auto-responsive dynamic Portale Vortice Quantico with zero-overflow viewport scaling.

### New in v2.3.1:
- **Dual Cloud Titans in Portale Vortice Quantico**: Simultaneous cosmic rendering of both Cloud Titans (`BEAM:cloud` 501B MoE and `MiniMax 3.1 Flash:cloud` 456B MoE Video Developer) side-by-side on an expanded celestial floating platform, equipped with dual rotating quantum vortices, independent cyber-auras, and balanced real-time telemetry columns.
- **Dedicated MiniMax Cloud Top HUD Card (`hud-cloud-minimax`)**: High-visibility HUD metric card featuring live turn tokens, context percentage, historical tokens, API calls, and zero-VRAM cloud indicators with purple/magenta gradient visual styling.
- **Dynamic Multi-Titan Cloud Workflow Badge**: Header badge automatically adapts to identify and format multi-cloud agent clusters (`☁ OLLAMA CLOUD (BEAM 501B MoE + MINIMAX 3.1 FLASH 456B)`).
- **Self-Healing Adaptive Layout Engine**: Seamless automatic layout restoration and upgrade handling for persisted localStorage configurations.

### New in v2.3:
- **Cloud Lightning Integration**: Seamless telemetry and persistent 24h keep-alive for `BEAM:cloud` (501B Super Coordinator) and `MiniMax 3.1 Flash:cloud` (456B Video Developer).
- **Hermes Profile Auto-Avatar Discovery**: Automatic extraction and synchronization of agent avatars directly from Hermes profiles (`profiles/<name>/assets/avatar.png`) into dashboard sprites with real catalog benchmarks.
- **Radar Benchmark OpenCompass**: Multi-dimensional radar spider charts for each model (Coding, Reasoning, Knowledge, Agentic, Vision, Hardware Throughput).
- **Architecture Intelligence**: Automatic detection and profiling of MoE (Mixture of Experts), Dense Transformers, Vision Multimodal (VLM), and Flash Cloud models.
- **Hardware TPS Calibration**: Real-time estimated token throughput calibrated for NVIDIA GeForce RTX 4060 (8GB VRAM) and Cloud Lightning clusters.

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

## Procedure

1. Run `python scripts/open_monitor.py`.
2. The launcher automatically verifies if the background server daemon on port 8888 is active.
3. If not active, it launches `run_server.py` silently in the background with BelowNormal priority.
4. It launches the frameless native app window (Microsoft Edge or Google Chrome standalone mode) with 1480x920 dimensions.
5. Report to the user that the dashboard is open and state how many agents are currently monitored (9 agents: 7 local + 2 cloud).

## Pitfalls

- Does not interfere with existing browser sessions: `http://127.0.0.1:8888/dashboard_AI.html` remains accessible simultaneously in any web browser.
- Operates under Zero-Touch rule: pure observer, never modifies model weights, prompt context, or system configurations.

## Verification

Run the script and check that JSON output confirms `"ok": true` and `"mode": "native_app"`.
