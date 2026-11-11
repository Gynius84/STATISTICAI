---
name: statistiche
description: Open native STATISTICAI 16-bit dashboard monitor (v3.0, 14 active Hermes agents: 6 local engines across Ollama :11434 C: and Unsloth Studio :8888 + 8 Cloud Titans across Ollama Cloud, NVIDIA NIM, OrcaRouter, and Nous Research, Dual Local Gateway, Auto-Gateway Discovery Engine, Quantum Vortices with Auto-Hide, Real-Time 4-Room Routing Casetta/Ufficio/Infermeria/Cimitero, Box & Card Minimization & Hiding, Standby Ollama Cloud 429 Cemetery routing, Golden Snapshot & 1-Click Healing Engine).
version: 3.0
author: Gyniu, Hermes Agent
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [monitoring, dashboard, retro, agent-telemetry, ollama, unsloth, nvidia-nim, orcarouter, nous-research, radar-benchmark, moe, hexa-cloud, agent-doctor, golden-snapshot, box-minimization, dual-local-gateway]
    commands: [statistiche, statisticheai]
---

# STATISTICAI Monitor Skill (v3.0)

Opens and controls the **STATISTICAI v3.0** 16-bit retro arcade AI monitoring dashboard for all **14 Hermes agents** across Dual Local Gateways (Ollama :11434 & Unsloth :8888) & cloud engines in a dedicated native desktop application window (`http://127.0.0.1:8787/dashboard_AI.html`).

Invokable in Hermes via `/statistiche` or `/statisticheai`.

### Architectural Overview (v3.0):
- **14 Total AI Agents (100% Operational & Verified)**:
  - **6 Local Engines (RTX 4060 GPU VRAM Zero-Swap)**:
    - `GynBot1`: Nemotronbolt (4.0B GGUF) • Ollama (:11434, Disco C:)
    - `GEMMO`: Gemma:latest • Ollama (:11434, Disco C:)
    - `NEMOHOUSE`: Nemotronbolt • Ollama (:11434, Disco C:)
    - `HACKER`: HackerQwen • Ollama (:11434, Disco C:)
    - `VISION`: Vision7b:latest • Ollama (:11434, Disco C:)
    - `NEMOSLOTH`: Nemotron-3.5 Bolt (4.0B) • Unsloth Studio (:8888, 100% VRAM Zero-Swap)
  - **8 Cloud Titans (0 MB VRAM Overhead)**:
    - `DEEPPO4flash`: DeepSeek V4 Flash • OrcaRouter Cloud (131K Context)
    - `DEEPPO41flash`: DeepSeek V4.1 Flash • OrcaRouter Cloud (131K Context)
    - `LONGCAT`: Meituan Longcat 2.5 Free • Nous Research Cloud (131K Context)
    - `NEMOTRON`: Nemotron-3 Ultra 550B • NVIDIA NIM Cloud
    - `MISTRAL`: Mistral Large 4 1T • NVIDIA NIM Cloud
    - `BEAM`: 501B MoE Cloud • Ollama Cloud (In STANDBY / Cimitero per Quota 429)
    - `BEAMO`: 501B MoE Cloud • Ollama Cloud (In STANDBY / Cimitero per Quota 429)
    - `NEMO`: Nemotron-3 Ultra 550B • Ollama Cloud (In STANDBY / Cimitero per Quota 429)

### Key Features (v3.0):
1. **Dual Local Gateway Support**: Simultaneous real-time telemetry and health monitoring across both Ollama (:11434) and Unsloth Studio (:8888) local engines.
2. **Auto-Gateway Discovery Engine**: Automatically detects new Hermes profiles and maps their gateway (host, port, provider), assigning technical benchmark specs, badges, and coordinated color palettes autonomously.
3. **Box & Card Level Minimization & Hiding**: Every box and individual agent card can be moved, minimized (`[-]`/`[+]`), or hidden (`[✕]`) with full persistence in `localStorage`.
4. **Auto-Hide Empty Quantum Vortices**: Quantum cloud portals with 0 active agents (e.g. OpenRouter, Google AI) are automatically hidden, while active clouds (Nous Research, OrcaRouter, NVIDIA NIM, Ollama Cloud) are displayed with real-time particle animations.
5. **Standby Detection & Cemetery**: Agents in Hermes STANDBY category or with 429 quota exhaustion are placed in the Cemetery room with 0 HP and 1-click resurrection checks.
