# BASELINE CONFIGURAZIONE AGENTI HERMES & MODELLI OLLAMA

> **REGOLA ZERO**: Progetto puramente OSSERVATORE. Nessuna modifica a file esterni a `STATISTICHEAI`. Configurazioni e parametri sono congelati e intoccabili.

Data rilevamento baseline: **2026-10-16 09:25:00 UTC**

---

## 1. Mappa Agenti -> Modelli & Parametri Operativi

| # | Agente / Titolo | Profilo Hermes | Modello Assegnato | Modello Base Ollama | Contesto Hermes (token) | num_ctx Ollama | Soglia Auto-Compressione | Sprite Associato |
|---|-----------------|----------------|-------------------|---------------------|-------------------------|----------------|--------------------------|------------------|
| 1 | **GynBot1** (Direttore & Regista) | `default` (Root) | `qwen3.5:64k` | `qwen3.5:4b` | 65.536 | 65.536 | 0.85 (85%) | `sprites_agents\GynBot1.png` |
| 2 | **PROGRAMMATORE** (GynBot2 / Dev) | `gynbot2` | `qwen2.5-coder:64k` | `qwen2.5-coder:7b` | 32.768 | 32.768 | 0.85 (85%) | `sprites_agents\PROGRAMMATORE.png` |
| 3 | **QUALITY CHEKER** (GynBox3 / QA) | `gynbox3` | `hermes3:64k` | `hermes3:8b` | 20.480 | 20.480 | 0.85 (85%) | `sprites_agents\QUALITY CHEKER.png` |
| 4 | **Direttore Marketing** (MARK1) | `mark1` | `qwen2.5:64k` | `qwen2.5:7b` | 24.576 | 24.576 | 0.85 (85%) | `sprites_agents\Direttore Marketing.png` |
| 5 | **Copywriter Creativo** (MARK2) | `mark2` | `llama3.1:64k` | `llama3.1:8b` | 16.384 | 16.384 | 0.85 (85%) | `sprites_agents\Copywriter Creativo.png` |
| 6 | **Growth Hacker** (MARK3) | `mark3` | `hermes3:64k` | `hermes3:8b` | 20.480 | 20.480 | 0.85 (85%) | `sprites_agents\Growt hacker.png` |
| 7 | **CEH** (HACKER / Pentester) | `hacker` | `whiterabbit:16k` | `hf.co/Nekuromento/...` | 16.384 | 16.384 | 0.85 (85%) | `sprites_agents\CEH.png` |
| 8 | **BEAM** (Super Coordinatore Cloud) | `beam` | `beam:cloud` | `Reflection Beam 501B (Cloud)` | 1.048.576 | 1.048.576 | 0.85 (85%) | `sprites_agents\BEAM.png` |

### Note sui Parametri
- **Provider Hermes**: `ollama-launch` (porta standard 11434).
- **Keep-Alive**: Gestito automaticamente dal runtime Ollama/Hermes.
- **Tolleranza Discrepanze**: Le differenze intenzionali tra context length di Hermes e Ollama sono informazioni neutre di esercizio.
- **Database di Stato**: Ogni profilo possiede un proprio `state.db` SQLite interrogato in sola lettura (`mode=ro`).

---

## 2. File di Configurazione Monitorati (Integrità SHA-256)

I seguenti 23 file costituiscono la baseline sacra del Guardiano di integrità:

| Percorso File | SHA-256 Checksum | Dimensione (Byte) | Ultima Modifica (ISO) |
|---|---|---|---|
| `C:\Users\Gyniu\AppData\Local\hermes\config.yaml` | `bee84ca0275e9aafa77996824a9039574b9d13cdffa556adc6ffc9b667f35752` | 7,761 | 2026-10-16T18:22:32 |
| `C:\Users\Gyniu\AppData\Local\hermes\profile.yaml` | `e8e67fda4eaae52d38a61066135581234ebe459c2c9274d2e32fc9ce6b14a5c9` | 27,070 | 2026-10-16T18:26:18 |
| `C:\Users\Gyniu\AppData\Local\hermes\context_length_cache.yaml` | `b8a60c3f7a4daf35406b0a5169f3987dfd99c3f202b905824e71e22dea28cfd0` | 308 | 2026-10-12T19:42:34 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\gynbot2\config.yaml` | `a6cef20a867559e1dbcdee61279fbb6116396aa0813c57387b4ddcb4bee24806` | 6,851 | 2026-10-16T10:20:18 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\gynbot2\profile.yaml` | `7e123ee8a25f9276cdb26558a178b303f3f1cae62d4b3bf2b73cebcdc98e8cae` | 304 | 2026-10-16T14:59:43 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\gynbox3\config.yaml` | `e5f7bf027124a3d1074cf05f77d29edd21fd39975ea0b261602de33387ab4438` | 6,809 | 2026-10-16T11:14:29 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\gynbox3\profile.yaml` | `c93b5c5c8b54ac93e9e1d33f27bfb6558fb8e2a04a2c951f4e1bbfaed11f37d5` | 306 | 2026-10-16T14:59:21 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\hacker\config.yaml` | `b5a93ea075ac5ab82d9498cadb56066aeff9378331b7c7ca990e88c7cbb7541f` | 7,074 | 2026-10-16T10:27:21 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\hacker\profile.yaml` | `95c7a1545e8325c49cd8383d60ec55fc38eab312f4af55d7bc5e42b262126c8a` | 195 | 2026-10-14T17:03:10 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\mark1\config.yaml` | `090a8044e4d967f3db9cf023210ffe2a0bb810fa1677af3b46c09afd42711d36` | 6,813 | 2026-10-16T10:20:18 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\mark1\profile.yaml` | `d89d3e75d7637365e572f8842010f575d039592a9391f5f78694f7161b63b826` | 311 | 2026-10-16T13:52:42 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\mark2\config.yaml` | `d65963ef419b03e56c4926bd591690331985deb27f70d983ff582f6ee0bebcf0` | 6,815 | 2026-10-16T10:20:18 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\mark2\profile.yaml` | `efda29e00b45af12d9fe3f24b485a970252f5dd797828b6ba6db6b9153b0db52` | 319 | 2026-10-16T13:53:04 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\mark3\config.yaml` | `1b44db6b91d5679b71e223783d241d24b7bbce6e5401f782b92fbb87639d6db4` | 6,813 | 2026-10-16T10:20:18 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\mark3\profile.yaml` | `ad312336826431d75b03ceaf415c51256796ee16cbd9bbbe9b9a5b58c29d35c9` | 299 | 2026-10-16T13:21:27 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\beam\config.yaml` | `310ee03ca19aad9b1bfd76eacb8a481ba54599707751d91463523420fdebe474` | 7,603 | 2026-10-16T17:03:49 |
| `C:\Users\Gyniu\AppData\Local\hermes\profiles\beam\profile.yaml` | `b918583ed5db346d64e1a82ee9cdef0e43897747bcfa9aa4b87a38ef14af76ab` | 216 | 2026-10-16T21:36:15 |
| `C:\Users\Gyniu\AppData\Local\hermes\modelfiles\Modelfile.hermes3-64k` | `6e04172e18a1a39a68c5258029f994b4a41ee181f7bfefab81da7477941141d6` | 1,911 | 2026-10-12T23:25:52 |
| `C:\Users\Gyniu\AppData\Local\hermes\modelfiles\Modelfile.llama31-64k` | `6810aadc530181cf96f8fef2f6c759b9f60b624c0e44fc41a3c41fdc54be8306` | 87 | 2026-10-14T10:13:50 |
| `C:\Users\Gyniu\AppData\Local\hermes\modelfiles\Modelfile.qwen25-64k` | `13dd5f234b8a0b1086aaec0338a5efd61afe1e805fa840b47a2d1f288e02621c` | 1,690 | 2026-10-14T11:02:49 |
| `C:\Users\Gyniu\AppData\Local\hermes\modelfiles\Modelfile.qwen25coder-64k` | `b9849a8ad54ec841b8f4b2198752183550b36993ee9a8a09a38e3f351874bdd5` | 1,645 | 2026-10-13T09:51:27 |
| `C:\Users\Gyniu\AppData\Local\hermes\modelfiles\Modelfile.qwen35-64k` | `f155f1861b453cb1781958f619d6f3ef43d50c527a2f6804e6ef004c832a7834` | 135 | 2026-10-15T13:28:43 |
| `C:\Users\Gyniu\AppData\Local\hermes\modelfiles\Modelfile.whiterabbit-16k` | `f4018fd451936a7c7f948a04ae9ca24000c0263a47cba6df3d1cca422a7ee45d` | 1,815 | 2026-10-14T17:51:43 |

---

## 3. Protocollo di Monitoraggio Guardiano (Ogni 60 Secondi)
1. Il thread Guardiano esegue in background su `run_server.py` la verifica hash di tutti i 21 file sopra elencati in modalità **sola lettura**.
2. Se un hash o una data di modifica differisce rispetto a questa tabella:
   - Viene generato un avviso immediato visualizzato nella dashboard con stato `CONFIGURAZIONE MODIFICATA`.
   - Nessun tentativo di ripristino o sovrascrittura automatica viene intrapreso.
3. Se tutti gli hash sono conformi:
   - Lo stato Guardiano riporta `INTEGRO (100% IDENTICO ALLA BASELINE)`.
