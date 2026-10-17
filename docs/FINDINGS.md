# FINDINGS: SCOPERTA ARCHITETTURA AGENTI, PROFILI E MODELLI

> **Rilevamento in sola lettura (Read-Only)** effettuato il 2026-10-16.

---

## 1. Architettura di Esecuzione Hermes

Hermes opera con un'architettura multi-processo a profili isolati:
1. **Desktop GUI App**: Processi Electron principali (`Hermes.exe` in `C:\Users\Gyniu\AppData\Local\hermes\hermes-agent\apps\desktop\release\win-unpacked\`).
2. **Gateway Centrale**: Processo Python background (`PID 8236`, script `hermes_cli\main.py gateway run --quiet`).
3. **Database di Stato (SQLite)**:
   - Root: `C:\Users\Gyniu\AppData\Local\hermes\state.db`
   - Profili: `C:\Users\Gyniu\AppData\Local\hermes\profiles\<nome_profilo>\state.db`
   - Tabelle chiave interrogate in modalità sola lettura (`file:...state.db?mode=ro`):
     - `sessions`: ID sessione, modello, started_at, ended_at, input_tokens, output_tokens, message_count, tool_call_count, title, last_activity_at.
     - `session_model_usage`: aggregazione per modello, billing_provider, conteggio chiamate e token.
4. **Log di Esercizio**:
   - `C:\Users\Gyniu\AppData\Local\hermes\profiles\<profilo>\logs\agent.log`
   - `C:\Users\Gyniu\AppData\Local\hermes\profiles\<profilo>\logs\errors.log`
5. **Runtime Ollama**:
   - Eseguibile: `C:\Users\Gyniu\AppData\Local\Programs\Ollama\ollama.exe` (Porta 11434).
   - API autorizzate in sola lettura: `GET /api/ps`, `GET /api/tags`, `GET /api/version`, `POST /api/show`.

---

## 2. Mappatura Completa dei 7 Agenti Hermes

### 1. GynBot1 (Regista / Leadership)
- **ID Profilo**: `default` (Root in `AppData\Local\hermes`)
- **Titolo / Descrizione**: Esperto PC, Direzione e Coordinatore
- **Gruppo / Categoria**: `Leadership & Regia` (Colore: `#3b82f6` Blu)
- **Modello Ollama**: `qwen3.5:64k` (Base: `qwen3.5:4b`, Q4)
- **Finestra di Contesto**: 65.536 token (Hermes) / 65.536 token (Ollama Modelfile)
- **Soglia Compressione**: 85% (0.85 in config.yaml)
- **Sprite**: `sprites_agents\GynBot1.png` (96x104 pixel)
- **Session DB**: `C:\Users\Gyniu\AppData\Local\hermes\state.db` (105 sessioni storiche)

### 2. PROGRAMMATORE (GynBot2 / Team Sviluppo)
- **ID Profilo**: `gynbot2` (`AppData\Local\hermes\profiles\gynbot2`)
- **Titolo / Descrizione**: PROGRAMMATORE, Coder / Developer
- **Gruppo / Categoria**: `Team Sviluppo` (Colore: `#fbbf24` Giallo/Ambra)
- **Modello Ollama**: `qwen2.5-coder:64k` (Base: `qwen2.5-coder:7b`)
- **Finestra di Contesto**: 32.768 token (Hermes) / 32.768 token (Ollama Modelfile)
- **Soglia Compressione**: 85%
- **Sprite**: `sprites_agents\PROGRAMMATORE.png` (96x104 pixel)
- **Session DB**: `...\profiles\gynbot2\state.db` (108 sessioni storiche)

### 3. QUALITY CHEKER (GynBox3 / Team Sviluppo)
- **ID Profilo**: `gynbox3` (`AppData\Local\hermes\profiles\gynbox3`)
- **Titolo / Descrizione**: QUALITY CHEKER, QA & Tester
- **Gruppo / Categoria**: `Team Sviluppo` (Colore: `#ec4899` Rosa/Magenta)
- **Modello Ollama**: `hermes3:64k` (Base: `hermes3:8b`)
- **Finestra di Contesto**: 20.480 token (Hermes) / 20.480 token (Ollama Modelfile)
- **Soglia Compressione**: 85%
- **Sprite**: `sprites_agents\QUALITY CHEKER.png` (96x104 pixel)
- **Session DB**: `...\profiles\gynbox3\state.db` (97 sessioni storiche)

### 4. Direttore Marketing (MARK1 / Team Marketing)
- **ID Profilo**: `mark1` (`AppData\Local\hermes\profiles\mark1`)
- **Titolo / Descrizione**: Direttore Marketing & Brand Strategist
- **Gruppo / Categoria**: `Team Marketing` (Colore: `#8b5cf6` Viola)
- **Modello Ollama**: `qwen2.5:64k` (Base: `qwen2.5:7b`)
- **Finestra di Contesto**: 24.576 token (Hermes) / 24.576 token (Ollama Modelfile)
- **Soglia Compressione**: 85%
- **Sprite**: `sprites_agents\Direttore Marketing.png` (96x104 pixel)
- **Session DB**: `...\profiles\mark1\state.db` (20 sessioni storiche)

### 5. Copywriter Creativo (MARK2 / Team Marketing)
- **ID Profilo**: `mark2` (`AppData\Local\hermes\profiles\mark2`)
- **Titolo / Descrizione**: Copywriter Creativo & Social Media Storyteller
- **Gruppo / Categoria**: `Team Marketing` (Colore: `#06b6d4` Ciano)
- **Modello Ollama**: `llama3.1:64k` (Base: `llama3.1:8b`)
- **Finestra di Contesto**: 16.384 token (Hermes) / 16.384 token (Ollama Modelfile)
- **Soglia Compressione**: 85%
- **Sprite**: `sprites_agents\Copywriter Creativo.png` (96x104 pixel)
- **Session DB**: `...\profiles\mark2\state.db` (16 sessioni storiche)

### 6. Growth Hacker (MARK3 / Team Marketing)
- **ID Profilo**: `mark3` (`AppData\Local\hermes\profiles\mark3`)
- **Titolo / Descrizione**: Growth Hacker, SEO Specialist & Data Analyst
- **Gruppo / Categoria**: `Team Marketing` (Colore: `#10b981` Smeraldo)
- **Modello Ollama**: `hermes3:64k` (Base: `hermes3:8b`)
- **Finestra di Contesto**: 20.480 token (Hermes) / 20.480 token (Ollama Modelfile)
- **Soglia Compressione**: 85%
- **Sprite**: `sprites_agents\Growt hacker.png` (96x104 pixel)
- **Session DB**: `...\profiles\mark3\state.db` (21 sessioni storiche)

### 7. CEH (HACKER / Team Security)
- **ID Profilo**: `hacker` (`AppData\Local\hermes\profiles\hacker`)
- **Titolo / Descrizione**: CEH, Pentester & Security Auditor
- **Gruppo / Categoria**: `Team Security` (Colore: `#ef4444` Rosso Cyber)
- **Modello Ollama**: `whiterabbit:16k` (Base: `Llama-3.1-WhiteRabbitNeo-2-8B-Q5_K_M-GGUF`)
- **Finestra di Contesto**: 16.384 token (Hermes) / 16.384 token (Ollama Modelfile)
- **Soglia Compressione**: 85%
- **Sprite**: `sprites_agents\CEH.png` (96x104 pixel)
- **Session DB**: `...\profiles\hacker\state.db` (5 sessioni storiche)

---

## 3. Risorse Hardware Correlate
- **GPU**: NVIDIA GeForce RTX 4060 Laptop (8.188 MB VRAM).
- **Driver / nvidia-smi**: Lettura query-only `--query-gpu=name,memory.total,memory.used,memory.free,utilization.gpu,temperature.gpu,power.draw`.
- **Modelli Condivisi**: Nota di correlazione per `hermes3:64k` (condiviso tra QUALITY CHEKER e Growth Hacker). Quando caricato in VRAM, la memoria viene correlata proporzionalmente o contrassegnata come "condiviso".
