# STATISTICHEAI v2.0 🎮🤖
### Dashboard Retro Arcade (16-Bit) per Telemetria, Diagnosi e Monitoraggio Agenti AI Multi-Provider

[![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero%20(Pure%20Python)-brightgreen.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-informational.svg)]()
[![Multi-Provider](https://img.shields.io/badge/Providers-Ollama%20%7C%20LM%20Studio%20%7C%20Hermes%20%7C%20OpenAI%20%7C%20Cloud-orange.svg)]()

> **STATISTICHEAI v2.0** trasforma la gestione dei tuoi agenti AI locali e cloud in un videogioco Arcade Pixel Art a 16-bit. Monitora hardware, VRAM, saturazione token, memoria a lungo termine e stato di salute con un sistema avanzato di auto-diagnosi medica (*Cura Sessione*, *Cura Contesto*, *Resurrezione 1-Click*).

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
👉 **`http://127.0.0.1:8888/dashboard_AI.html`**

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
http://127.0.0.1:8888/dashboard_AI.html
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

## 🔒 Regola Zero & Sicurezza

- **Isolamento Totale**: Il monitor opera in sola lettura verso i processi LLM esterni, garantendo la totale integrità dei tuoi modelli.
- **CSRF Protection**: Tutte le chiamate di mutazione (aggiunta, cura, riallineamento guardiano) sono protette da token crittografici CSRF a ciclo univoco.
- **Backup Automatico**: Ogni azione correttiva esegue preventivamente un backup locale di sicurezza in `data/archive/`.

---

## 📁 Struttura del Progetto

```
STATISTICHEAI/
├── dashboard_AI.html    # Frontend responsive HTML5 Canvas Retro Arcade (16-bit)
├── run_server.py        # Server HTTP multi-thread ultra-leggero zero-dependency
├── config.json          # Registro JSON centralizzato configurazioni e agenti
├── agent_doctor.py      # Motore di auto-diagnosi, cura e resurrezione
├── guard_engine.py      # Guardiano di integrità con baseline hashing SHA-256
├── start.bat            # Script di avvio rapido Windows (porta 8888)
├── stop.bat             # Script di arresto pulito tramite PID
├── sprites_agents/      # Asset grafici pixel art originali (PNG ad alta leggibilità)
├── docs/                # Documentazione architetturale e baseline
└── LICENSE              # Licenza MIT Open Source
```

---

## 📜 Licenza

Distribuito sotto licenza **MIT**. Consulta il file [LICENSE](LICENSE) per ulteriori dettagli.
Creato con passione per la community AI e per tutti i costruttori di agenti autonomi.
