---
name: statistiche
description: Open native STATISTICHEAI 16-bit dashboard monitor (v2.2, 10 optimized agents, Radar Benchmark OpenCompass, MoE & RTX 4060 TPS).
version: 2.2.1
author: Gyniu, Hermes Agent
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [monitoring, dashboard, retro, agent-telemetry, ollama, llamacpp, radar-benchmark, moe]
---

# STATISTICHEAI Monitor Skill (v2.2.1)

Opens and controls the STATISTICHEAI 16-bit retro arcade AI monitoring dashboard for 10 optimized Hermes agents across multi-tier engines (Ollama on C:, llama.cpp on D:, and Beam 501B cloud) in a dedicated native desktop application window.

### New in v2.2:
- **Radar Benchmark OpenCompass**: Multi-dimensional radar spider charts for each model (Coding, Reasoning, Knowledge, Agentic, Vision, Hardware Throughput).
- **Architecture Intelligence**: Automatic detection and profiling of MoE (Mixture of Experts), Dense Transformers, Vision Multimodal (VLM), and Ternary Quantized models.
- **Hardware TPS Calibration**: Real-time estimated token throughput calibrated for NVIDIA GeForce RTX 4060 (8GB VRAM) and cloud tiers.

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
5. Report to the user that the dashboard is open and state how many agents are currently monitored.

## Pitfalls

- Does not interfere with existing browser sessions: `http://127.0.0.1:8888/dashboard_AI.html` remains accessible simultaneously in any web browser.
- Operates under Zero-Touch rule: pure observer, never modifies model weights, prompt context, or system configurations.

## Verification

Run the script and check that JSON output confirms `"ok": true` and `"mode": "native_app"`.
