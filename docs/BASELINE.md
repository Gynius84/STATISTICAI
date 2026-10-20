# BASELINE CONFIGURAZIONE AGENTI HERMES & MODELLI LLAMA.CPP / CLOUD

> **REGOLA ZERO**: Progetto puramente OSSERVATORE. Nessuna modifica a file esterni a STATISTICAI. Configurazioni e parametri sono congelati e intoccabili.

Data aggiornamento baseline v2.3.1 (Roster Ibrido 9 Agenti: 7 llama.cpp D: + 2 Ollama Cloud): **2026-10-20 11:20:00**

---

## 1. Mappa Agenti (9 Profili Hermes Attivi)

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
| `C:\Users\Gyniu\AppData\Local\hermes\config.yaml` | `472cb03ccc54030d43f654582c1644ae78b36c0e72d1f19c5366278face1cb4b` | 8,067 | 2026-10-20T11:21:40 |
| `C:\Users\Gyniu\AppData\Local\hermes\profile.yaml` | `a6862c4574d0ff58db45161352bd0083a194d8adfc806f3c3b3edaf3f9ae8d31` | 1,065 | 2026-10-20T10:21:18 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\coder14b\config.yaml` | `17c55f5c368626a1b0ea061d08c5ca45ae595e916b929aeeb37b71d5c705a527` | 690 | 2026-10-19T01:43:31 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\coder14b\profile.yaml` | `9f298178d5c31de8009449cdee22660134b536d789ef7782dbd1c43fee92c8e4` | 177 | 2026-10-20T10:51:19 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\gynbot2\config.yaml` | `e14ff7c2d67c31e88ff7af1a640e06a876b19c36e24b10a847ca61af19ce55f2` | 688 | 2026-10-19T13:14:20 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\gynbot2\profile.yaml` | `d481e731831dfed08dd61e7f813704076cf42234dc6a54b3389c374e7f5de3f3` | 293 | 2026-10-20T10:50:46 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\gynbox3\config.yaml` | `60b7e285b2df079bd7ceaed0da6dfcaf9b29f229798b62cddec11b3b8846d3a1` | 814 | 2026-10-19T18:43:50 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\gynbox3\profile.yaml` | `dc4d40d56bd452562b935a49d8bf3399b945b8733cbcf47690bc242bbb200013` | 295 | 2026-10-20T10:51:41 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\mark2\config.yaml` | `842b1c78557c89a9512c99d2da1857bc4b1cb538a4e9482da942b4f45e223c03` | 775 | 2026-10-19T18:53:18 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\mark2\profile.yaml` | `958efd6ac451a91c95ca3d69e9c5a28484ba4d49ad570cf9950b075376d5a6bf` | 306 | 2026-10-20T10:52:49 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\qwen\config.yaml` | `4f467267db526f5bef543e68e23167ca0e923d223f71eaf8c6d8a296fc558fae` | 600 | 2026-10-19T01:14:46 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\qwen\profile.yaml` | `c080a26515e8fb9653c6026ae61f0d43706f167037ba7190c63c34d2f618b0ad` | 166 | 2026-10-20T10:53:50 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\vision7b\config.yaml` | `e754c349b4b4534acd90c13964faf379f523f36f039087c61572aa5e5c30e9d9` | 640 | 2026-10-19T01:43:42 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\vision7b\profile.yaml` | `08746b4a210c18a19d2b8128a745a008d059051f242aa85eec64ca3eda6878e2` | 177 | 2026-10-20T10:53:32 |

---

## 3. Protocollo di Monitoraggio Guardiano (Ogni 30 Secondi)
1. Il thread Guardiano esegue in background su `run_server.py` la verifica hash di tutti i file sopra elencati in modalità **sola lettura**.
2. Se un file viene modificato o rimosso:
   - Viene generato un avviso visibile nell'header HUD della dashboard.
   - Nessun blocco di processo: l'osservazione continua ininterrotta a garanzia della sicurezza operativa.
