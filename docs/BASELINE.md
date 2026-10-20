# BASELINE CONFIGURAZIONE AGENTI HERMES & MODELLI LLAMA.CPP / CLOUD

> **REGOLA ZERO**: Progetto puramente OSSERVATORE. Nessuna modifica a file esterni a STATISTICAI. Configurazioni e parametri sono congelati e intoccabili.

Data aggiornamento baseline v2.4 (Roster Multi-Cloud 11 Agenti: 7 llama.cpp D: + 2 Ollama Cloud + 2 NVIDIA NIM Cloud): **2026-10-20 11:20:00**

---

## 1. Mappa Agenti (11 Profili Hermes Attivi)

| # | Agente / Titolo | Profilo Hermes | Modello Assegnato | Architettura | Sorgente | Sprite Associato |
|---|-----------------|----------------|-------------------|--------------|----------|------------------|
| 1 | **GynBot1** | default (Root) | eam:cloud | MoE (501B MoE) | Cloud | sprites_agents/GynBot1.png |
| 2 | **BEAM** | eam | eam:cloud | MoE (501B MoE) | Cloud | sprites_agents/BEAM.png |
| 3 | **Video Developer** | minimax | minimax-m3.1-flash:cloud | MoE Ultra-Fast (456B) | Cloud MiniMax 3.1 | sprites_agents/Video Developer.png |
| 4 | **DARK CODER** | coder14b | Qwen2.5-Coder-14B-Instruct-Q4_K_M | Dense Specialist (14.7B) | llama.cpp (D:) | sprites_agents/DARK CODER.png |
| 5 | **PROGRAMMATORE** | gynbot2 | DeepSeek-Coder-V2-Lite-Instruct-Q4_K_M | MoE Specialist (16B) | llama.cpp (D:) | sprites_agents/PROGRAMMATORE.png |
| 6 | **QUALITY CHEKER** | gynbox3 | Nous-Hermes-2-Mixtral-8x7B-DPO-Q4_K_M | MoE (46.7B) | llama.cpp (D:) | sprites_agents/QUALITY CHEKER.png |
| 7 | **Copywriter Creativo** | mark2 | Phi-3.5-MoE-instruct-Q4_K_M | MoE (42B) | llama.cpp (D:) | sprites_agents/Copywriter Creativo.png |
| 8 | **MIND** | qwen | Qwen3.6-35B-A3B-Q4_K_M | MoE (35B A3B) | llama.cpp (D:) | sprites_agents/MIND.png |
| 9 | **VISION** | ision7b | Qwen2.5-VL-7B-Instruct-Q4_K_M | Vision Multimodal (7.6B) | llama.cpp (D:) | sprites_agents/VISION.png |

---

## 2. File di Configurazione Monitorati (Integrità SHA-256)

I seguenti 14 file costituiscono la baseline del Guardiano di integrità:

| Percorso File | SHA-256 Checksum | Dimensione (Byte) | Ultima Modifica (ISO) |
|---|---|---|---|
| `C:\Users\Gyniu\AppData\Local\hermes\config.yaml` | `eace19b4dce3809cc4ffd851dd7493b1777c52df9c2db736b55ec5e24ca2938a` | 8,069 | 2026-10-20T15:46:33 |
| `C:\Users\Gyniu\AppData\Local\hermes\profile.yaml` | `a6862c4574d0ff58db45161352bd0083a194d8adfc806f3c3b3edaf3f9ae8d31` | 1,065 | 2026-10-20T10:21:18 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\coder14b\config.yaml` | `16e96e3cea3bd79d72ca7e987caa252e5edcc78c99aba167db6445cdae61bf6a` | 4,261 | 2026-10-20T17:29:23 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\coder14b\profile.yaml` | `9f298178d5c31de8009449cdee22660134b536d789ef7782dbd1c43fee92c8e4` | 177 | 2026-10-20T10:51:19 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\gynbot2\config.yaml` | `e4a980b90dfeaed41034cac5d2027f8988a036623180476eb87758b375b36564` | 718 | 2026-10-20T15:46:33 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\gynbot2\profile.yaml` | `d481e731831dfed08dd61e7f813704076cf42234dc6a54b3389c374e7f5de3f3` | 293 | 2026-10-20T10:50:46 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\gynbox3\config.yaml` | `d446c4481f990aefdce4189dbbae79737365c1feb9caad9579fe8357f67aad44` | 814 | 2026-10-20T15:46:33 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\gynbox3\profile.yaml` | `dc4d40d56bd452562b935a49d8bf3399b945b8733cbcf47690bc242bbb200013` | 295 | 2026-10-20T10:51:41 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\mark2\config.yaml` | `d7badb038b65faf2201fe2cc7096dca701a22d18dbe35c4c04625f005e17e029` | 775 | 2026-10-20T15:46:33 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\mark2\profile.yaml` | `958efd6ac451a91c95ca3d69e9c5a28484ba4d49ad570cf9950b075376d5a6bf` | 306 | 2026-10-20T10:52:49 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\qwen\config.yaml` | `6ab3676b5b980c55fc842c0ef283e6ccf2d2f3c6072f8c9664e1e35dcd9fc0a8` | 626 | 2026-10-20T15:46:33 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\qwen\profile.yaml` | `c080a26515e8fb9653c6026ae61f0d43706f167037ba7190c63c34d2f618b0ad` | 166 | 2026-10-20T10:53:50 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\vision7b\config.yaml` | `34e8fc1e20548abc39155e4e039c1377ff727f80410fa9490b21a0651bd842f1` | 667 | 2026-10-20T15:46:33 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\vision7b\profile.yaml` | `08746b4a210c18a19d2b8128a745a008d059051f242aa85eec64ca3eda6878e2` | 177 | 2026-10-20T10:53:32 |

---

## 3. Protocollo di Monitoraggio Guardiano (Ogni 30 Secondi)
1. Il thread Guardiano esegue in background su `run_server.py` la verifica hash di tutti i file sopra elencati in modalità **sola lettura**.
2. Se un file viene modificato o rimosso:
   - Viene generato un avviso visibile nell'header HUD della dashboard.
   - Nessun blocco di processo: l'osservazione continua ininterrotta a garanzia della sicurezza operativa.
