---
name: statistiche
description: Open native STATISTICHEAI 16-bit dashboard monitor (v2.5, 9 active agents: 3 local llama.cpp Disco D: + 2 cloud Ollama Beam & MiniMax + 2 cloud NVIDIA NIM DeepSeek & Drago + 2 cloud OpenRouter Inkling & Laguna, Triple Quantum Nuvoletta Portals, Dynamic Cloud Auto-Detection, OpenCompass Radar Benchmarks, Zero Local VRAM Cloud).
version: 2.5
author: Gyniu, Hermes Agent
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [monitoring, dashboard, retro, agent-telemetry, ollama, llamacpp, nvidia-nim, openrouter, radar-benchmark, moe, cloud-lightning, triple-cloud]
---

# STATISTICHEAI Monitor Skill (v2.5)

Opens and controls the STATISTICHEAI 16-bit retro arcade AI monitoring dashboard for the 9 optimized Hermes agents across hybrid local & triple-cloud engines (3 local models on llama.cpp port 9931 disk D:, plus 2 Cloud Lightning MoE models on Ollama: BEAM 501B MoE and MiniMax 3.1 Flash 456B MoE, plus 2 Cloud Titans on NVIDIA NIM Enterprise: DeepSeek V4.1 Flash 410B MoE and Drago GLM 5.3 130B, plus 2 Cloud Titans on OpenRouter: Inkling Reasoner 70B and Laguna SWE 35B MoE) in a dedicated native desktop application window.

### New in v2.5:
- **OpenRouter Cloud Integration (Triple Cloud Titans)**:
  - Direct integration with OpenRouter Cloud endpoints (`https://openrouter.ai/api/v1`) providing high-speed cloud routing for modern agents with zero local GPU VRAM consumption.
  - Telemetry and OpenCompass radar benchmarks calibrated for:
    - **`INKLING` (Thinking Machines Inkling Free)**: Advanced reasoning and cognitive problem solver (~60+ tok/s, 32K context, reasoning score 96, agentic 95).
    - **`LAGUNA` (Poolside Laguna S-2.1 Free)**: Specialist in software engineering, autonomous SWE tasks and tools (~80+ tok/s, 32K context, coding score 96, agentic 97).
- **Triple Quantum Vortex Nuvoletta Portals**:
  - **Portal 1 (Ollama Cloud Lightning)**: Celestial cyan & purple quantum vortex featuring BEAM 501B and MiniMax 3.1 Flash.
  - **Portal 2 (NVIDIA Cloud NIM Titans)**: High-energy cyber emerald & NVIDIA green quantum vortex featuring DeepSeek V4.1 Flash and Drago GLM 5.3.
  - **Portal 3 (OpenRouter Cloud Titans)**: Ethereal cosmic indigo, violet & neon lavender floating pixel art nuvoletta with live animated particle vortex featuring INKLING & LAGUNA floating avatars with celestial aura and live token stream.
- **Dynamic Cloud Auto-Detection & Self-Provisioning Engine**:
  - Whenever any cloud endpoint connects (Ollama Cloud, NVIDIA NIM, OpenRouter, or other cloud APIs), the monitoring engine automatically detects the cloud nature of the agent, provisions the dedicated card with live metrics, context % and lifetime tokens, and generates the corresponding nuvoletta section without manual configuration.
- **Auto-Discovery Engine 2.5 (Clean Self-Healing & Pruning)**:
  - Clean real-time discovery of all 9 active Hermes agents across local llama.cpp (Disco D:), Ollama Cloud, NVIDIA NIM Cloud, and OpenRouter Cloud.
  - Full automatic avatar extraction from profile assets into `sprites_agents/`.
  - Upgraded Workflow Header & Subtitle displaying the active triple-cloud hybrid architecture.

### Previous Features (v2.4 & v2.3.2):
- **NVIDIA Cloud NIM Enterprise Integration (81 Models)**: Direct access to 81 state-of-the-art models on NVIDIA Cloud NIM.
- **Fast Radar Benchmark & Performance Sorter**: Instant one-click sorting of all agent cards directly from the filter bar (Speed TPS, Coding, Reasoning, Knowledge, Agentic, Vision, Alphabetical, Custom Drag & Drop).
- **Harmonious Divided HUD Layout Architecture**: Divisions 1-4 with zero-overflow viewport auto-scaling.

## When to Use

- User asks to "open monitor", "show dashboard", "apri statistiche", "mostra monitoraggio", or check agent health/telemetry/benchmarks.
- Triggered by slash command `/statistiche` or `/monitor`.
- User wants to view real-time VRAM, tokens, session memory, or agent status without leaving Hermes.

## How to Run

```bash
# Avvio monitor nativo Desktop
start "C:\Users\Gyniu\OneDrive\Desktop\start - STATISTICHEAI.lnk"

# Oppure tramite script dedicato
python open_monitor.py
```
