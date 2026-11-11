# STATISTICHEAI v2.7 🎮🤖
### Dashboard Retro Arcade (16-Bit) per Telemetria, Diagnosi, Benchmark Radar OpenCompass e Rilevamento Architetture MoE/Dense (Penta-Cloud Titans & llama.cpp :9931)

[![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero%20(Pure%20Python)-brightgreen.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-informational.svg)]()
[![Multi-Provider](https://img.shields.io/badge/Providers-llama.cpp%20(7%20D:)%20%7C%20Ollama%20Cloud%20(2)%20%7C%20NVIDIA%20NIM%20(2)-brightgreen.svg)]()

> **STATISTICHEAI v2.5** trasforma la gestione dei tuoi agenti AI locali e multi-cloud in un videogioco Arcade Pixel Art a 16-bit. Monitora hardware, VRAM, saturazione token, memoria a lungo termine, grafici **Benchmark Radar OpenCompass**, tipo di architettura (**MoE, Dense, VLM, Hybrid Reasoning**) e velocità stimata **TPS** per gli **11 agenti attivi**: 7 modelli locali ultra-ottimizzati su **llama.cpp Router (Disco D: porta 9931)** + 2 modelli cloud massivi su **Ollama Cloud (Beam 501B MoE + MiniMax 3.1 Flash 456B MoE)** + 2 Titani Cloud accelerati su **NVIDIA Cloud NIM Enterprise (DeepSeek V4.1 Flash 410B MoE + Drago GLM 5.3 130B)** con accesso illimitato a 81 modelli NIM e zero consumo di VRAM locale.

---

## ✨ Novità della Versione 2.7 (14 Agenti, Quinto Portale Quantico OrcaRouter, Modale a 4 Passi, Snapshot Default & Resurrezione Intelligente)

- ⚡ **Nuovo Cloud OrcaRouter & Quinto Portale Quantico (DEEPPO4flash + DEEPPO41flash)**:
  - Integrazione nativa del nuovo cloud provider OrcaRouter (`https://api.orcarouter.ai/v1`) con i due modelli ultra-veloci `DEEPPO4flash` (DeepSeek V4 Flash) e `DEEPPO41flash` (DeepSeek V4.1 Flash Free, 131K contesto).
  - Aggiunto il **Quinto Portale Quantico** su canvas retrogame con vortice quantico plasma smeraldo/ciano, stelle ad alta frequenza e nuvoletta pixel art fluttuante con sprite camminanti dedicati.
- 🦙 **Riparazione NEMOHOUSE e Separazione Rigorosa Motori Locali llama.cpp**:
  - Risolta l'errata classificazione cloud di `NEMOHOUSE` (Nemotron-3.5-Bolt 4B GGUF) e confermata quella di `GEMMO` (Gemma-4 E4B-it GGUF): ora entrambi operano al 100% come motori locali ad altissima velocità su llama.cpp Router (:9931, Disco D:, 100% VRAM GPU Zero-Swap).
  - Totale agenti operativi portato a **14** (4 Locali llama.cpp + 10 Titani Penta-Cloud).
- 📋 **Modale Universale "Collega Nuovo Agente" Ristrutturata in 4 Passi**:
  - Inserito `llama.cpp Router (:9931)` tra i provider locali di prima classe.
  - Suddivisione chiara e visiva tra Motori Locali (zero costi, VRAM locale) e Motori Cloud (zero overhead VRAM).
  - Flusso guidato in 4 passi (1: Provider, 2: Anagrafica & Squadra, 3: Endpoint/Modello/Contesto con test ping live, 4: Avatar Arcade & Petdex).
- 🛡 **Snapshot "Default" Ottimizzato (Golden Image Immutabile)**:
  - Creata baseline protetta in `snapshots/default_optimized_20261024/` contenente cataloghi agenti calibrati, configurazioni ottimali (finestre contesto a 64k/128k/1M token per pieno supporto tool calling), manifest `CONTENTS.md` e checksum crittografici SHA-256 (`checksums.sha256`).
- 🏥 **Sistema di Cura e Resurrezione Intelligente (Agent Doctor)**:
  - Triage reale su 4 stanze: Casetta (riposo), Ufficio (lavoro attivo), Infermeria (cure mirate sessione/contesto), Cimitero (resurrezione 1-click).
  - Rimozione automatica di lease orfani, lock spuri e conflitti di admissione (admission_conflict).
  - Ripristino garantito della Golden Image dallo Snapshot con rollback preventivo automatico in caso di errore.
- 🚀 **Desktop Shortcut & Hermes Skill v2.7**:
  - Aggiornato collegamento desktop `start - STATISTICHEAI.lnk` e skill Hermes (`SKILL.md`) sincronizzata in tutte le directory di sistema.

## ✨ Novità della Versione 2.4 (NVIDIA Cloud NIM 81 Modelli, Doppio Portale Vortice Quantico, Auto-Discovery 2.4)

- ⚡ **Integrazione NVIDIA Cloud NIM Enterprise (81 Modelli NIM ad Accesso Illimitato)**:
  - Collegamento diretto agli endpoint cloud NVIDIA NIM (`https://integrate.api.nvidia.com/v1`) con supporto completo a 81 modelli all'avanguardia senza alcun sovraccarico sulla GPU locale RTX 4060:
    - **`DEEPSEEK` (DeepSeek V4.1 Flash)**: Architettura MoE da 410B totali (~28B attivi per token), throughput vertiginoso stimato a **120+ tok/s**, finestra contesto nativa a 128k e benchmark OpenCompass di eccellenza (Coding 97, Throughput 99, Agentic 96).
    - **`DRAGO` (GLM 5.3)**: Modello Dense Hybrid Reasoner da 130B parametri specializzato in deep reasoning cognitivo, comprensione multilingue e sintesi concettuale a 128k contesto con benchmark OpenCompass di spicco (Reasoning 98, Knowledge 97, Throughput 90).
- ☁ **Due Portali Vortice Quantico Indipendenti con Nuvolette Fluttuanti 16-Bit**:
  - **Divisione 2 - Portale Ollama Cloud Titans**: Piattaforma fluttuante pixel art celeste con doppio vortice quantico ciano/magenta per **BEAM** (501B) e **MiniMax Video Developer** (456B).
  - **Divisione 3 - Portale NVIDIA NIM Cloud Titans**: Seconda piattaforma fluttuante pixel art in stile cyber emerald & verde NVIDIA (`#76b900`) con vortice ad alta frequenza per **DEEPSEEK** e **DRAGO**, auree rotanti sincronizzate e colonne di telemetria live con token turn/lifetime, conteggio chiamate e throughput.
- 🔍 **Auto-Discovery Engine 2.4 (Self-Healing e Sanitizzazione Completa)**:
  - Rilevamento automatico e pulizia rigorosa dei nomi profilo Hermes da `profile.yaml`, eliminando artefatti di stringhe vuote o con virgolette (`''`) e formattando nomi puliti (`DEEPSEEK`, `DRAGO`, `DARK CODER`).
  - Sincronizzazione automatica degli avatar da `profiles/<name>/assets/avatar.png` a `sprites_agents/<nome>.png` con prevenzione di file spuri e fallback dinamico su canvas.
  - Risoluzione istantanea di benchmark realistici e architetture per qualsiasi nuovo modello connesso tra gli 81 di NVIDIA NIM o locale.
- 🔀 **Nuovo Badge Workflow Multi-Cloud & Filtri Squadre**:
  - Badge header aggiornato: `🔀 WORKFLOW: 🦙 LLAMA.CPP DISCO D: (7 MODELLI GGUF) + ☁ OLLAMA CLOUD (BEAM + MINIMAX) + ⚡ NVIDIA CLOUD NIM (DEEPSEEK + DRAGO • 81 MODELLI NIM) = 11 AGENTI`.
  - Filtri squadra aggiornati a 11 agenti totali con pulsanti dedicati: `TUTTI (11)`, `☁ TITANI CLOUD (4)`, `⚡ NVIDIA NIM (2)`.

## ✨ Novità della Versione 2.3.2 (Fast Radar Sorter & Layout HUD Diviso Antistraripamento)

- ⚡ **Tasti di Ordinamento Rapido Radar & Performance nella Barra Filtri**:
  - Inseriti tasti arcade 1-click per ordinare istantaneamente le schede degli agenti in base alle loro caratteristiche e punteggi del grafico Benchmark Radar OpenCompass:
    - 🚀 **Velocità (TPS)**: Ordina per velocità di output su RTX 4060 o Cloud.
    - 💻 **Coding (HumanEval)**: Ordina per eccellenza nella programmazione software.
    - 🧠 **Ragionamento (MATH/Logica)**: Ordina per profondità logica e problem-solving.
    - 📚 **Conoscenza (MMLU-Pro)**: Ordina per ampiezza nozionistica ed enciclopedica.
    - ⚡ **Agentic (Tool Calling)**: Ordina per capacità esecutiva autonoma di strumenti.
    - 👁️ **Visione (VLM)**: Ordina per percezione e audit visivo multimodale.
    - 🔤 **Nome (A-Z)** e 🔀 **Predefinito**: Ripristino istantaneo dell'ordine personalizzato.
- 📐 **Ristrutturazione HUD a Due Divisioni Indipendenti**:
  - **Divisione 1 (Hardware & Motori Locali)**: Griglia compatta ed equilibrata per CPU, RAM, RTX 4060 GPU, VRAM, Ollama C:, llama.cpp D:, Team, Sviluppo, Marketing.
  - **Divisione 2 (Infrastruttura Cloud & Portale Vortice Quantico)**: Sezione dedicata orizzontale a piena larghezza per le card BEAM Cloud, MiniMax Cloud e il Portale Vortice Quantico con auto-scaling responsive del canvas a qualsiasi risoluzione.
  - **Zero Overflow**: Eliminato qualsiasi straripamento laterale dalla finestra o spezzamento di titoli su monitor di qualsiasi diagonale.

---

## ✨ Novità della Versione 2.3.1 (Portale Vortice Quantico Titani Cloud, Card MiniMax HUD, Dynamic Workflow)

- ☁ **Doppio Titano nel Portale Vortice Quantico (Animazione 16-Bit Estesa)**:
  - Il Portale Vortice Quantico accoglie ora simultaneamente entrambi i Titani Cloud: **BEAM** (501B Super Coordinator) e **MiniMax Video Developer** (456B MoE Flash).
  - Piattaforma celeste fluttuante espansa, doppio anello vortice quantico ciano/magenta ad interpolazione sinusoidale sfasata, particelle orbitali e colonne laterali di telemetria perfettamente bilanciate (zero sovrapposizioni).
- 🗂 **Nuova Card HUD Dedicata per MiniMax Cloud (`hud-cloud-minimax`)**:
  - Inserita metrica dedicata nella griglia HUD superiore in perfetto stile arcade (gradiente viola/magenta `#9333ea` -> `#c084fc` -> `#ec4899`).
  - Monitoraggio real-time di token per turno, percentuale contesto (128K), storico globale, chiamate API e consumo VRAM (0 MB).
- 🔀 **Badge Workflow Adattivo Multi-Titano**:
  - Il badge `🔀 WORKFLOW:` nell'header identifica e mostra dinamicamente tutti i modelli cloud attivi (`☁ OLLAMA CLOUD (BEAM 501B MoE + MINIMAX 3.1 FLASH 456B)`).
- 🛡 **Layout Engine Autorigenerante**:
  - Salvataggio e ripristino dell'ordine drag-and-drop con tolleranza per le versioni precedenti: le nuove card vengono integrate armoniosamente anche in presenza di cache di layout preesistenti.

---

## ✨ Novità della Versione 2.3 (MiniMax 3.1 Flash, Auto-Discovery Avatar Hermes, Cloud Lightning 24h)

- ☁ **Integrazione MiniMax 3.1 Flash Cloud (456B MoE - Video Developer)**:
  - Nuovo agente specializzato `Video Developer` collegato a `minimax-m3.1-flash:cloud` tramite Ollama Cloud endpoint.
  - Prestazioni lightning cluster: 65 tok/s, 131k context window, radar benchmark coding 94 / reasoning 95 / throughput 98.
- 🖼 **Hermes Profile Auto-Avatar Discovery**:
  - Il sistema di monitoraggio rileva e sincronizza automaticamente gli avatar personalizzati direttamente dalla directory dei profili Hermes (`profiles/<name>/assets/avatar.png`).
  - Zero configurazione manuale: chi importa o crea un agente con avatar in Hermes ottiene immediatamente l'avatar integrato e le metriche reali nella dashboard.
- ⚡ **Persistenza Cloud 24h & Zero-Swap Local**:
  - Keep-alive persistente `OLLAMA_KEEP_ALIVE=24h` per eliminare la latenza di riconnessione dei modelli cloud.
  - Politica anti-swap a 1 modello locale attivo alla volta (`--models-max 1 --parallel 1`) per proteggere gli 8GB di VRAM della GPU NVIDIA RTX 4060.
- 📊 **Radar Benchmark OpenCompass / VLMEvalKit**:
  - Ogni scheda tecnica agente espandibile include un autentico radar chart spider multi-dimensionale con 6 assi prestazionali:
    1. `Coding (HumanEval / SWE-bench)`
    2. `Reasoning (MATH / Logic / GSM8k)`
    3. `Knowledge (MMLU-Pro / Encyclopedic)`
    4. `Agentic Tools (Function Calling / IFEval)`
    5. `Vision (MMBench / Multimodal Perception)`
    6. `Speed Throughput (Tokens al Secondo su RTX 4060)`
  - Motore di disegno **HTML5 Canvas puro a 60 FPS**, zero dipendenze o CDN esterne, supporto Hi-DPI Retina e palette colori sincronizzata con l'agente.
- 🧠 **Rilevamento Intelligente Architetture (MoE vs Dense vs VLM vs Ternary)**:
  - Classificazione istantanea del tipo di architettura modello:
    - **MoE (Mixture of Experts)**: Reflection Beam 501B (~39B attivi), Qwen 3.6 35B A3B (~3.6B attivi), DeepSeek V4 Pro (671B).
    - **Dense Specialist & Generalist**: Qwen 2.5 Coder, Qwen 3.5, Hermes 3, Llama 3.1, Mistral Small Reasoning.
    - **Vision Multimodal (VLM)**: Qwen 2.5-VL 7B e Bonsai 9B VLM.
    - **Reasoning / Ternary Quantized**: Bonsai 27B Prism ML (1.58-bit).
- ⚡ **Stima Velocità Throughput (Tokens/s su NVIDIA RTX 4060 8GB)**:
  - Calibrazione hardware reale per ciascun modello:
    - Modelli compatti in VRAM pura (4B-8B): ~40-58 tok/s (100% offload GPU).
    - Modelli ibridi ad alto parametro (14B-27B GGUF): ~18-26 tok/s (offload RAM/GPU).
    - Architetture MoE (35B A3B): ~22 tok/s con attivazione rapida degli esperti.
    - Modelli Cloud MoE (501B / 671B): ~28-30 tok/s via streaming cluster.
- 🎯 **Visualizzazione Dettagliata con Barre Metriche**:
  - Punteggi numerici e barre di livello animate a colori dedicate per ciascuna dimensione benchmark all'apertura della scheda tecnica.
- 🛠 **Zero-Touch & Zero 404 Sprites**:
  - Risolti completamente gli indirizzamenti sprite delle schede agenti con mappatura rigorosa 13/13.

- 🦙 **Supporto Completo per llama.cpp (Disco D: Porta 9931)**:
  - Telemetria in tempo reale da `http://127.0.0.1:9931/v1/models` e probe di salute del router GGUF.
  - Nuovo riquadro dedicato nell'HUD di sistema: `🦙 LLAMA.CPP (DISCO D: PORTA 9931)`.
  - Badge di servizio live nel footer in tempo reale: `[ LLAMA.CPP :9931 (DISCO D:) OK ]`.
- 🤖 **Supporto Roster Completo di 13 Agenti Hermes**:
  - `GynBot1` (Regista & Esperto PC • Qwen3.5 64k • Ollama C:)
  - `PROGRAMMATORE` (Sviluppatore & Coder • Qwen2.5-Coder 64k • Ollama C:)
  - `QUALITY CHEKER` (QA & Tester • Hermes3 64k • Ollama C:)
  - `Direttore Marketing` (Brand Strategist • Qwen2.5 64k • Ollama C:)
  - `Copywriter Creativo` (Social Storyteller • Llama3.1 64k • Ollama C:)
  - `Growth Hacker` (SEO & Data Analyst • Hermes3 64k • Ollama C:)
  - `Chief Architect` (Deep Reasoning & Mentor Architecture • Bonsai 27B • Ollama C:)
  - `OCOLUS` (Visual Auditor & UI Analyst • Bonsai 9B • Ollama C:)
  - `DARK CODER` (Pentester & Security Coder • Qwen2.5-Coder 14B Uncensored GGUF • llama.cpp D:)
  - `IQ` (Ragionamento & Problem Solving • Mistral-Small 24B Reasoning GGUF • llama.cpp D:)
  - `MIND` (Deep Thinking & Knowledge Synthesis • Qwen3.6 35B A3B GGUF • llama.cpp D:)
  - `VISION` (Visual Master & UI Multimodal • Qwen2.5-VL 7B GGUF • llama.cpp D:)
  - `BEAM` (Super Coordinatore • Reflection Beam 501B MoE Cloud • 1M Context)
- 🔄 **Auto-Discovery e Auto-Pruning 100% Autonomo**:
  - Rileva automaticamente i profili Hermes leggendo anche campi annidati (`ui_meta -> title`).
  - Sincronizza modelli, context length e provider senza richiedere alcuna modifica manuale al codice.
  - Rimuove automaticamente dalla dashboard i profili eliminati (auto-pruning).
- 🖼 **Nuovi Avatar Pixel-Art 16-Bit Aggiunti**:
  - `DARK CODER.png`, `IQ.png`, `MIND.png`, `VISION.png`.
- 🎯 **Filtri Squadre Arricchiti**:
  - Filtri dedicati per `SICUREZZA & CODING`, `RAGIONAMENTO`, `DEEP THINKING`, `VISUAL AUDIT`, `ARCHITETTURA`, `SVILUPPO`, `MARKETING`, `COORDINATORE`.

---

## ✨ Novità della Versione 2.1 (Layout Riconfigurabile & Drag-and-Drop)

- 📌 **Header & Footer Blindati e Fissi**: Header fissato in alto con effetto sticky glass retro arcade per avere sempre a vista telemetria, orologio e controlli chiave; Footer fisso in basso con ping e indicatori live.
- 📐 **Interfaccia e Box 100% Riconfigurabili a Drag-and-Drop**:
  - **Tutti i Box di Sistema Riordinabili**: HUD Statistiche, Stage Interattivo Canvas, Barra Filtri & Azioni, Griglia Agenti e Registro Storico possono essere spostati nell'ordine verticale desiderato tramite drag-and-drop o pulsanti rapidi `▲` / `▼`.
  - **Schede Agenti Riordinabili**: Ogni singola scheda agente nella griglia può essere riposizionata liberamente tramite maniglia `⠿ SPOSTA` o frecce `◀` / `▶`.
  - **Metriche HUD Personalizzabili**: Anche i riquadri della barra HUD (CPU, RAM, GPU, VRAM, Ollama, Team, Beam Cloud...) possono essere riordinati a piacimento.
- 💾 **Persistenza Automatica in LocalStorage**: Ogni spostamento viene salvato all'istante nel browser; riaprendo la dashboard da qualsiasi tab o browser la disposizione personalizzata è fedelmente conservata.
- 🔄 **Pulsante `[ 🔄 RIPRISTINA PREDEFINITO ]`**: Ripristina il layout di fabbrica in un solo clic in qualunque momento.
- 🎛 **Modalità `[ 📐 PERSONALIZZA LAYOUT ]`**: Attiva la visualizzazione guidata con banner dei comandi e bordi retro tratteggiati per un'esperienza di personalizzazione intuitiva e immediata.

---

## ✨ Novità della Versione 2.0.1 (Update di Rilevamento Istantaneo)

- 🔄 **Auto-Discovery Hermes in Tempo Reale**: Rilevamento automatico e persistente di ogni nuovo profilo o agente creato su Hermes (`~/.hermes/profiles`), con mappatura automatica dei modelli Ollama, contesti e sprite.
- ⚡ **Pulsante `[ 🔄 RILEVA / SINCRONIZZA ]`**: Sincronizzazione manuale immediata a un click integrata nella barra dei filtri della dashboard.
- 🖼 **Nuovi Avatar Ufficiali Integrati**:
  - `OCOLUS.png` per l'agente Visual Audit & UI Analyst.
  - `Chief Architect.png` per l'agente Deep Reasoning & Mentor Architecture.
- 🛠 **Passerella Universale Perfezionata**: Correzione del feedback di salvataggio e gestione atomica dell'aggiunta/rimozione agenti senza ricaricare la pagina.

---

## ✨ Novità della Versione 2.0

- 🔌 **Pulsante Universale 1-Click `[ + COLLEGA NUOVO AGENTE ]`**: Collega qualsiasi agente AI direttamente dall'interfaccia senza toccare codice.
- 🌐 **Architettura Multi-Provider Totale**:
  - **Ollama** (`http://127.0.0.1:11434`)
  - **LM Studio** (`http://127.0.0.1:1234`)
  - **Hermes Agent Framework** (Profili multi-agente e database SQLite `state.db`)
  - **OpenAI-Compatible / vLLM / LocalAI** (`http://127.0.0.1:8000`)
  - **Cloud Models** (Reflection Beam 501B, Claude 3.5, OpenRouter, Groq)
- 🔍 **Rilevamento Automatico (Auto-Discovery)**: Verifica con 1 click quali motori LLM sono attivi sulla tua macchina ed elenca automaticamente tutti i modelli installati.
- 🏰 **Stage Retro Arcade Dinamico a 4 Stanze**:
  1. 🏠 **La Casetta (Riposo)**: Agenti in standby che riposano nei lettini pixel-art.
  2. 🏢 **L'Ufficio (Lavoro)**: Monitor CRT luminosi e attività di elaborazione in tempo reale.
  3. 🏥 **L'Infermeria (Cura)**: Ricovero per saturazione contesto o sessioni bloccate con ECG animato.
  4. 🪦 **Il Cimitero (R.I.P.)**: Campo santo per crash critici, con nebbia, lapidi e lucciole notturne.
- 🏷 **Titolo & Badge Workflow Adattivo Dinamico**: Il titolo si calcola in tempo reale identificando il numero esatto di agenti, i runtime collegati e specificando i modelli locali (es. 64k calibrati) e i modelli su cloud (come *Reflection Beam 501B MoE su Ollama Cloud*). Si adatta all'istante a qualsiasi workflow esterno (LM Studio, vLLM, Anthropic).
- 🐾 **Galleria Avatar & Official Nous Hermes Petdex (44+ Mascot)**: Collezione integrata di avatar originali con filtro per categoria (Core Team e Hermes Pets) e barra di ricerca istantanea in pixel art.
- ⚡ **Raggio di Resurrezione Celestiale**: Animazione di luce dorata dal cielo al momento della resurrezione di un agente.
- 🌀 **Portale Quantico & Piattaforma Cloud Fluttuante**: Visualizzazione dedicata per super coordinatori e modelli Cloud (come *Reflection Beam 501B*).
- 🧠 **Tracciamento Memoria Persistente**: Storico token lifetime globale, chiamate API, tool eseguiti e regole memorizzate a lungo termine.
- 🛡 **Guardiano dell'Integrità Baseline**: Monitoraggio di sicurezza con hash SHA-256 e rotazione automatica backup ogni 3 giorni.

---

## 🚀 Avvio Rapido

### Prerequisiti
- **Python 3.9+** (Standard library nativa: **ZERO pacchetti pip da installare!**).
- Qualsiasi runtime LLM locale (Ollama, LM Studio) o chiavi API Cloud (opzionali).

### Avvio su Windows (1-Click)
Fai doppio clic sul file:
```cmd
start.bat
```
Lo script avvia il server in background a priorità `BelowNormal` (consumo CPU < 1%) e apre automaticamente la dashboard nel tuo browser predefinito su:
👉 **`http://127.0.0.1:8787/dashboard_AI.html`**

Per arrestare il server:
```cmd
stop.bat
```

### Avvio Manuale (Linux / macOS / Windows)
```bash
python run_server.py
```
Quindi apri nel browser:
```
http://127.0.0.1:8787/dashboard_AI.html
```

---

## 🛠 Come Collegare un Nuovo Agente

1. Clicca sul pulsante giallo in alto a destra: **`+ COLLEGA NUOVO AGENTE`**.
2. Seleziona il tuo provider:
   - **🦙 OLLAMA**: Per modelli locali gestiti con Ollama.
   - **🧪 LM STUDIO**: Per istanze LM Studio Local Server.
   - **🏛 HERMES PROFILE**: Per profili isolati di Hermes Agent.
   - **⚡ OPENAI / vLLM**: Per qualsiasi server compatibile con le API standard OpenAI.
   - **☁ CLOUD / CLAUDE**: Per modelli cloud remoti.
3. Clicca su **`⚡ TESTA CONNESSIONE & RILEVA MODELLI`**: la dashboard testerà la latenza e caricherà la lista dei modelli pronti per l'uso.
4. Assegna il nome dell'agente, il ruolo, la finestra di contesto e seleziona il tuo avatar retro arcade pixel-art preferito.
5. Clicca su **`✓ SALVA E INTEGRA AGENTE`**: il nuovo agente apparirà immediatamente nel canvas e nelle statistiche!

---

## 🩺 Sistema "Agent Doctor" (Diagnosi & Cura)

Ogni agente dispone di una barra di energia HP (0-100) calibrata su:
- **Latenza del server**
- **Saturazione del contesto token** (avviso al 75%, critico al 90%)
- **Stato del database di sessione**

| Stato | Stanza | Intervento Disponibile |
|---|---|---|
| **SANO** (70-100 HP) | Casetta / Ufficio | Operativo, nessun intervento necessario. |
| **INFERMERIA** (30-60 HP) | Infermeria | **CURA SESSIONE** (sblocco lock e lease orfani) o **CURA CONTESTO** (compressione token non distruttiva). |
| **CIMITERO** (0 HP) | Il Cimitero | **★ RESUSCITA (1-CLICK) ★** (ripristino completo stato e rientro trionfale in ufficio). |

---

## 🤖 Integrazione Skill Nativa Hermes Agent

STATISTICHEAI v2.0 include una **Skill ufficiale per Hermes Agent** compatibile con lo standard aperto `agentskills.io`.

### Installazione Skill (1-Click per utenti Hermes)
Se hai clonato questa repository:
1. Esegui con doppio clic:
   ```cmd
   install_skill.bat
   ```
2. Oppure lancia Hermes direttamente dentro la cartella del progetto (`Project-Local Skill`):
   ```bash
   hermes skills trust
   ```

### Come usarla in Hermes:
- **In chat con qualsiasi Agente**: Scrivi *"Apri il monitoraggio"*, *"Mostra dashboard"* o *"Apri statistiche"*.
- **Tramite Slash Command**: Digita `/statistiche` oppure `/monitor` nel terminale o nella chat.
- **Da riga di comando rapida**: Digita `statistiche` in qualsiasi prompt dei comandi.

---

## 🖥 Modalità Finestra "App Nativa" Standalone

Oltre alla visualizzazione da browser, puoi avviare la dashboard come **applicazione desktop nativa**:
```cmd
python open_monitor.py
```
- **Zero barre o schede del browser**: finestra frameless dedicata con rapporto 1480x920.
- **Icona Arcade retrogame**: visualizza l'icona pixel-art di GynBot1 nella taskbar di Windows.
- **Titolo Adattivo Dinamico**: la barra del titolo riporta in tempo reale gli agenti collegati e il tipo di workflow.
- **Auto-Daemon Silente**: se il server non è attivo, viene avviato automaticamente in background a priorità minima (`BelowNormal`).

---

## 🔒 Regola Zero & Sicurezza

- **Isolamento Totale**: Il monitor opera in sola lettura verso i processi LLM esterni, garantendo la totale integrità dei tuoi modelli.
- **CSRF Protection**: Tutte le chiamate di mutazione (aggiunta, cura, riallineamento guardiano) sono protette da token crittografici CSRF a ciclo univoco.
- **Backup Automatico**: Ogni azione correttiva esegue preventivamente un backup locale di sicurezza in `data/archive/` con retention policy di 3 giorni.

---

## 📁 Struttura del Progetto

```
VERSIONE2.0/
├── dashboard_AI.html    # Frontend responsive HTML5 Canvas Retro Arcade (16-bit)
├── run_server.py        # Server HTTP multi-thread ultra-leggero zero-dependency (<1ms)
├── open_monitor.py      # Launcher desktop App Nativa e daemon controller
├── config.json          # Registro JSON centralizzato configurazioni e agenti
├── agent_doctor.py      # Motore di auto-diagnosi, cura e resurrezione
├── guard_engine.py      # Guardiano di integrità con baseline hashing SHA-256
├── cleanup_backups.py   # Modulo di pulizia e rotazione automatica snapshot (3 giorni)
├── install_skill.bat    # Script di installazione automatica della Skill in Hermes
├── start.bat            # Script di avvio rapido Windows (porta 8787 / App Nativa)
├── stop.bat             # Script di arresto pulito tramite PID
├── skills/              # Definizione ufficiale della skill Hermes per il catalogo
├── .hermes/             # Configurazione project-local per rilevamento automatico
├── sprites_agents/      # Asset grafici pixel art originali e Hermes Petdex (44+ sprite)
├── docs/                # Documentazione architetturale e baseline
└── LICENSE              # Licenza MIT Open Source
```

---

## 📜 Licenza

Distribuito sotto licenza **MIT**. Consulta il file [LICENSE](LICENSE) per ulteriori dettagli.  
Autore: **[Gynius84](https://github.com/Gynius84)** & Community.  
Creato con passione per la community AI e per tutti i costruttori di agenti autonomi.
