# BASELINE CONFIGURAZIONE AGENTI HERMES & MODELLI OLLAMA / LLAMA.CPP

> **REGOLA ZERO**: Progetto puramente OSSERVATORE. Nessuna modifica a file esterni a `STATISTICAI`. Configurazioni e parametri sono congelati e intoccabili.

Data aggiornamento baseline v2.2: **2026-10-19 10:19:55**

---

## 1. Mappa Agenti (13 Profili Hermes Attivi)

| # | Agente / Titolo | Profilo Hermes | Modello Assegnato | Architettura | Sorgente | Sprite Associato |
|---|-----------------|----------------|-------------------|--------------|----------|------------------|
| 1 | **GynBot1** | `default` (Root) | `qwen3.5:64k` | Dense Transformer (4B) | Ollama (C:) | `sprites_agents/GynBot1.png` |
| 2 | **BEAM** | `beam` | `beam:cloud` | MoE (501B MoE) | Cloud | `sprites_agents/BEAM.png` |
| 3 | **DARK CODER** | `coder14b` | `Qwen2.5-Coder-14B...` | Dense Specialist (14B) | llama.cpp (D:) | `sprites_agents/DARK CODER.png` |
| 4 | **PROGRAMMATORE** | `gynbot2` | `qwen2.5-coder:64k` | Dense Specialist (7.6B) | Ollama (C:) | `sprites_agents/PROGRAMMATORE.png` |
| 5 | **QUALITY CHEKER** | `gynbox3` | `hermes3:64k` | Dense Agentic (8B) | Ollama (C:) | `sprites_agents/QUALITY CHEKER.png` |
| 6 | **Direttore Marketing** | `mark1` | `qwen2.5:64k` | Dense Generalist (7.6B) | Ollama (C:) | `sprites_agents/Direttore Marketing.png` |
| 7 | **Copywriter Creativo** | `mark2` | `llama3.1:64k` | Dense Creative (8B) | Ollama (C:) | `sprites_agents/Copywriter Creativo.png` |
| 8 | **Growth Hacker** | `mark3` | `hermes3:64k` | Dense Agentic (8B) | Ollama (C:) | `sprites_agents/Growt hacker.png` |
| 9 | **Chief Architect** | `mentor` | `bonsai-27b:32k` | Reasoning Ternary (27B) | Ollama (C:) | `sprites_agents/Chief Architect.png` |
| 10 | **IQ** | `mistral24b` | `Mistral-Small-24B...` | Dense Reasoning (24B) | llama.cpp (D:) | `sprites_agents/IQ.png` |
| 11 | **OCOLUS** | `oculus` | `bonsai-9b:64k` | Vision Multimodal (9B) | Ollama (C:) | `sprites_agents/OCOLUS.png` |
| 12 | **MIND** | `qwen` | `Qwen3.6-35B-A3B...` | MoE (35B A3B) | llama.cpp (D:) | `sprites_agents/MIND.png` |
| 13 | **VISION** | `vision7b` | `Qwen2.5-VL-7B...` | Vision Multimodal (7B) | llama.cpp (D:) | `sprites_agents/VISION.png` |

---

## 2. File di Configurazione Monitorati (Integrità SHA-256)

I seguenti 35 file costituiscono la baseline del Guardiano di integrità:

| Percorso File | SHA-256 Checksum | Dimensione (Byte) | Ultima Modifica (ISO) |
|---|---|---|---|
| `C:\Users\Gyniu\AppData\Local\hermes\config.yaml` | `2399ad27ca0076f68d76df08ae2e1d5b1146ddb1e22f13743d5e2f84792b6919` | 8,372 | 2026-10-19T08:52:33 |
| `C:\Users\Gyniu\AppData\Local\hermes\profile.yaml` | `af2b6eb14f166fd1d78342a7ca8ee5367ae2d63f6cd1b219bd2e23079de830a9` | 1,065 | 2026-10-19T01:58:44 |
| `C:\Users\Gyniu\AppData\Local\hermes\context_length_cache.yaml` | `0afd894b8871373cdff7216d06735ebe9e8632fb5e65f7ac875715f2937d6f95` | 699 | 2026-10-19T01:41:20 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\beam\config.yaml` | `310ee03ca19aad9b1bfd76eacb8a481ba54599707751d91463523420fdebe474` | 7,603 | 2026-10-16T17:03:49 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\beam\profile.yaml` | `b918583ed5db346d64e1a82ee9cdef0e43897747bcfa9aa4b87a38ef14af76ab` | 216 | 2026-10-16T21:36:15 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\coder14b\config.yaml` | `17c55f5c368626a1b0ea061d08c5ca45ae595e916b929aeeb37b71d5c705a527` | 690 | 2026-10-19T01:43:31 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\coder14b\profile.yaml` | `6b0ec3637f249075cda5b989443ba98b2e6926db3db1cb4949d2ac5e6c0356ea` | 177 | 2026-10-19T01:54:53 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\gynbot2\config.yaml` | `a6cef20a867559e1dbcdee61279fbb6116396aa0813c57387b4ddcb4bee24806` | 6,851 | 2026-10-16T10:20:18 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\gynbot2\profile.yaml` | `13acabdab9a6fa298cb93c2e0d93f3d0a6e04d9ada509c8d5afdeab59840951f` | 275 | 2026-10-19T01:58:39 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\gynbox3\config.yaml` | `e5f7bf027124a3d1074cf05f77d29edd21fd39975ea0b261602de33387ab4438` | 6,809 | 2026-10-16T11:14:29 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\gynbox3\profile.yaml` | `52a64009b7618bbc9ccd734b6227e7719de8c69911a2f4692ce6b8076aefc866` | 277 | 2026-10-19T01:58:38 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\mark1\config.yaml` | `090a8044e4d967f3db9cf023210ffe2a0bb810fa1677af3b46c09afd42711d36` | 6,813 | 2026-10-16T10:20:18 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\mark1\profile.yaml` | `77746bea32908e45a09d4581d857746309a8b01a1c2dcf765acdc0cb8b3abd55` | 280 | 2026-10-19T01:58:43 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\mark2\config.yaml` | `d65963ef419b03e56c4926bd591690331985deb27f70d983ff582f6ee0bebcf0` | 6,815 | 2026-10-16T10:20:18 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\mark2\profile.yaml` | `78ebae27f80b8a2af7be352c14e08d0249d083c0632594b1b01db4c1e32aa17a` | 288 | 2026-10-19T01:58:43 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\mark3\config.yaml` | `1b44db6b91d5679b71e223783d241d24b7bbce6e5401f782b92fbb87639d6db4` | 6,813 | 2026-10-16T10:20:18 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\mark3\profile.yaml` | `a0e42b9d216549ffa9acfef3cb4e61030899ffb355930c6818941c737f286a63` | 280 | 2026-10-19T01:58:42 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\mentor\config.yaml` | `bcd6034b287aaabba3cb821efa21d98d4b8222364b1063c97697d6cf69a01cfd` | 7,664 | 2026-10-17T22:24:04 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\mentor\profile.yaml` | `adc3647cd3a13f8a4e1394850c821fc82643214cec9474921c429edba2235b88` | 219 | 2026-10-17T21:06:04 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\mistral24b\config.yaml` | `c07e37ab778a453ca6ca2bbf9d0b82a3ec334e68374eea1bac66fa86fdebb8af` | 726 | 2026-10-19T01:43:36 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\mistral24b\profile.yaml` | `d6a8ea645695216f4510e5f0e701dc0d3ad2543e1ca63f4d2b46038d2be18f22` | 172 | 2026-10-19T01:54:05 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\oculus\config.yaml` | `702aafaedfff11ad50c838fc68842b51e7eb1331c7ccb2ca383ee38e89da611f` | 7,795 | 2026-10-17T22:24:12 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\oculus\profile.yaml` | `253df7bfa9fca35b597d950cd0cb6b907cc72c0dd3a4cfbd475e034dc19dc0f3` | 210 | 2026-10-17T21:05:21 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\qwen\config.yaml` | `4f467267db526f5bef543e68e23167ca0e923d223f71eaf8c6d8a296fc558fae` | 600 | 2026-10-19T01:14:46 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\qwen\profile.yaml` | `8525665b77b2d9b9cd38bd87b775006dea65e2aa09bf0d5635f52ac092e2d3de` | 166 | 2026-10-19T00:57:15 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\vision7b\config.yaml` | `e754c349b4b4534acd90c13964faf379f523f36f039087c61572aa5e5c30e9d9` | 640 | 2026-10-19T01:43:42 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\vision7b\profile.yaml` | `d0cd0919d9d1aa4c8c32b1735eb5f85141c1c2ce5002525a8c51554535305f30` | 177 | 2026-10-19T01:58:21 |
| `C:\Users\Gyniu\AppData\Local\hermes\modelfiles\Modelfile.bonsai-27b-16k` | `db819fbf1dae16fc0e53a73fcb7a807ce08fcfaca9c3ef8ba5e3e1270e7eee24` | 129 | 2026-10-17T20:58:43 |
| `C:\Users\Gyniu\AppData\Local\hermes\modelfiles\Modelfile.bonsai-9b-32k` | `710d3d485902fd5ade30a7816a756b0d81a097f7d0a0b57f145d3d9afb5ee2d6` | 138 | 2026-10-17T20:58:20 |
| `C:\Users\Gyniu\AppData\Local\hermes\modelfiles\Modelfile.hermes3-64k` | `6e04172e18a1a39a68c5258029f994b4a41ee181f7bfefab81da7477941141d6` | 1,911 | 2026-10-12T23:25:52 |
| `C:\Users\Gyniu\AppData\Local\hermes\modelfiles\Modelfile.llama31-64k` | `6810aadc530181cf96f8fef2f6c759b9f60b624c0e44fc41a3c41fdc54be8306` | 87 | 2026-10-14T10:13:50 |
| `C:\Users\Gyniu\AppData\Local\hermes\modelfiles\Modelfile.qwen25-64k` | `13dd5f234b8a0b1086aaec0338a5efd61afe1e805fa840b47a2d1f288e02621c` | 1,690 | 2026-10-14T11:02:49 |
| `C:\Users\Gyniu\AppData\Local\hermes\modelfiles\Modelfile.qwen25coder-64k` | `b9849a8ad54ec841b8f4b2198752183550b36993ee9a8a09a38e3f351874bdd5` | 1,645 | 2026-10-13T09:51:27 |
| `C:\Users\Gyniu\AppData\Local\hermes\modelfiles\Modelfile.qwen35-64k` | `f155f1861b453cb1781958f619d6f3ef43d50c527a2f6804e6ef004c832a7834` | 135 | 2026-10-15T13:28:43 |
| `C:\Users\Gyniu\AppData\Local\hermes\modelfiles\Modelfile.whiterabbit-16k` | `f4018fd451936a7c7f948a04ae9ca24000c0263a47cba6df3d1cca422a7ee45d` | 1,815 | 2026-10-14T17:51:43 |

---

## 3. Protocollo di Monitoraggio Guardiano (Ogni 30 Secondi)
1. Il thread Guardiano esegue in background su `run_server.py` la verifica hash di tutti i file sopra elencati in modalità **sola lettura**.
2. Se un file viene modificato o rimosso:
   - Viene generato un avviso visibile nell'header HUD della dashboard.
   - Nessun blocco di processo: l'osservazione continua ininterrotta a garanzia della sicurezza operativa.
