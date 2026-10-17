# STATO DEL SISTEMA: HERMES & OLLAMA (7 AGENTI)

> **Ultimo Aggiornamento**: 2026-10-16 10:55 UTC  
> **Stato Generale**: OPERATIVO AL 100% — Zero duplicati — Idempotenza verificata — Dashboard 4 Stanze attiva

---

## 1. Mappatura Agenti Hermes & Modelli Ollama Ottimizzati

La flotta è composta da **7 agenti specializzati**, ciascuno configurato con il proprio profilo Hermes e collegato al rispettivo modello Ollama ottimizzato (context window estesa a 64k/16k con `num_ctx` dedicato).

| # | Agente | Profilo Hermes | Modello Assegnato | Modello Base Ollama | Contesto Calibrato | File Sprite |
|---|---|---|---|---|---|---|
| 1 | **GynBot1** (Direttore & Regista) | `default` | `qwen3.5:64k` | `qwen3.5:4b` | 65.536 token | `sprites_agents\GynBot1.png` |
| 2 | **PROGRAMMATORE** (GynBot2) | `gynbot2` | `qwen2.5-coder:64k` | `qwen2.5-coder:7b` | 32.768 token | `sprites_agents\PROGRAMMATORE.png` |
| 3 | **QUALITY CHEKER** (GynBox3) | `gynbox3` | `hermes3:64k` | `hermes3:8b` | 20.480 token | `sprites_agents\QUALITY CHEKER.png` |
| 4 | **Direttore Marketing** (Mark1) | `mark1` | `qwen2.5:64k` | `qwen2.5:7b` | 24.576 token | `sprites_agents\Direttore Marketing.png` |
| 5 | **Copywriter Creativo** (Mark2) | `mark2` | `llama3.1:64k` | `llama3.1:8b` | 16.384 token | `sprites_agents\Copywriter Creativo.png` |
| 6 | **Growth Hacker** (Mark3) | `mark3` | `hermes3:64k` | `hermes3:8b` | 20.480 token | `sprites_agents\Growt hacker.png` |
| 7 | **CEH** (Hacker / Pentester) | `hacker` | `whiterabbit:16k` | `hf.co/Nekuromento/...` | 16.384 token | `sprites_agents\CEH.png` |

---

## 2. Parco Modelli Ollama (Flotta Pulita a 12 Modelli)

Tutti i modelli duplicati e orfani sono stati bonificati. L'istanza locale di Ollama ospita esattamente 12 modelli:
- **6 Modelli Base**: `qwen3.5:4b`, `qwen2.5-coder:7b`, `hermes3:8b`, `qwen2.5:7b`, `llama3.1:8b`, `hf.co/Nekuromento/Llama-3.1-WhiteRabbitNeo-2-8B-Q5_K_M-GGUF:Q5_K_M`.
- **6 Modelli Ottimizzati**: `qwen3.5:64k`, `qwen2.5-coder:64k`, `hermes3:64k`, `qwen2.5:64k`, `llama3.1:64k`, `whiterabbit:16k`.

---

## 3. Script di Emergenza & Autoguarigione (`Hermes-Guard-SelfHeal.bat`)

Collocato sia su `C:\Users\Gyniu\Desktop\Hermes-Guard-SelfHeal.bat` che sincronizzato su `C:\Users\Gyniu\OneDrive\Desktop\Hermes-Guard-SelfHeal.bat`.

### Caratteristiche Verificate:
1. **Idempotenza Totale**: Esegue la scansione preventiva tramite `guard_engine.py`. Se i 7 profili e i 6 modelli ottimizzati sono già conformi, non effettua scritture superflue.
2. **Backup Preventivo Datato**: Prima di qualsiasi operazione, salva lo snapshot dell'intera cartella Hermes in `backups/guard_auto_backup_<timestamp>/`.
3. **Log di Esecuzione**: Traccia dettagliata a video e su `data/guard_runs.log`.
4. **Pausa Finale Interattiva**: Mantiene la finestra aperta con `pause` per consentire la lettura del riepilogo.

---

## 4. Dashboard Retrogame Pixel Art (`dashboard_AI.html`)

Interfaccia a 16-Bit espansa a 1280x320 con palette retro, scanline CRT animate e 4 stanze tematiche:

1. **Casetta (Riposo)**: Agenti Sani in attesa di istruzioni, poltrona e caminetto con particelle pixel.
2. **Ufficio (Lavoro)**: Agenti Sani attivi su task e sessioni operative, scrivania con monitor CRT a fosfori verdi.
3. **Infermeria (Cura)**:
   - Agenti con **problemi minori**: sessione bloccata o saturazione token/contesto.
   - Dotata di letto medico, croce rossa pulsante e tracciato elettrocardiogramma ECG animato.
   - Pulsanti di azione selettiva:
     - `CURA SESSIONE`: rilascia solo i lease orfani e sblocca la concorrenza.
     - `CURA CONTESTO`: ripristina la context window calibrata del modello senza toccare la sessione.
4. **Cimitero (Resurrezione)**:
   - Agenti con **criticità simultanea** (sia sessione che contesto corrotti/bloccati).
   - Scena notturna con lapidi pixel "RIP", bara, luna argentata crescente, nebbia volumetrica semitrasparente e lucciole luminose.
   - Pulsante `RESUSCITA`: procedura in sicurezza con fascio di luce dorata ed effetti particellari a spirale.

---

## 5. Motore di Diagnosi & Resurrezione Reale (`agent_doctor.py`)

Backend helper vincolato rigorosamente a `127.0.0.1` e protetto da CSRF:
- **Sicurezza & Isolamento**: Interviene unicamente sui file dell'agente target; zero azioni su altri agenti o sui modelli Ollama.
- **Backup Pre-Azione**: Ogni cura o resurrezione genera un salvataggio preventivo in `backups/agent_<id>_<action>_<timestamp>/`.
- **Verifica Reale Post-Resurrezione**: Al termine del reset di sessione e contesto, interroga direttamente l'agente via CLI (`hermes -p <profile> -z "Rispondi solo con: OK RESUSCITATO"`).
- **Rollback Istantaneo Automatico**: Se il probe non risponde con successo entro il timeout, l'agente viene ripristinato immediatamente dallo snapshot e resta segnalato nel Cimitero.
- **Storico Azioni Persistente**: Tutte le operazioni sono memorizzate in `data/actions_history.json` e consultabili in tempo reale dal terminale di bordo.

---

## 6. Guardiano d'Integrità & Regola Zero

- Esecuzione continua ogni 60 secondi in sola lettura (`mode=ro`).
- Confronto crittografico SHA-256 dei 24 file sacri di Hermes contro `docs/BASELINE.md`.
- Segnalazione immediata a schermo in caso di alterazioni accidentali.

---

## 7. Esito Collaudo Finale (Verificato con Successo)

1. **Parco Modelli Ollama**: 12 modelli totali (6 base + 6 versioni 64k/16k), zero duplicati, zero orfani.
2. **Hermes Gateway & BOTS**: Multiplexing attivo per tutti i 7 agenti (`default`, `gynbot2`, `gynbox3`, `mark1`, `mark2`, `mark3`, `hacker`).
3. **Script `Hermes-Guard-SelfHeal.bat`**: Idempotenza testata con esito 0, backup datato automatico e pausa finale attiva su Desktop e OneDrive Desktop.
4. **Stanze Retrogame & Sprite**: 7 sprite visualizzati correttamente (HTTP 200), canvas CRT a 4 stanze (Casetta, Ufficio, Infermeria, Cimitero).
5. **Cure & Resurrezione Reali**:
   - Simulazione `mark1` in **Infermeria** (`session_blocked`) $\rightarrow$ Eseguita `CURA SESSIONE`: lease ripuliti, agente tornato a **SANO** (`casetta`).
   - Simulazione `gynbox3` in **Cimitero** (sessione + contesto) $\rightarrow$ Eseguita `RESUSCITA`: backup eseguito, ripristino config, test live CLI completato con risposta del modello: `"OK, sono stato riportato in vita. Sono pronto per assistere..."` $\rightarrow$ agente tornato a **SANO** (`ufficio`).
   - Storico azioni visibile e persistente in `data/actions_history.json`.

---

## 8. Risoluzione Gruppi Multi-Agente & Ripristino Chat (TEAM SVILUPPO & TEAM MARKETING)

### Problema Riscontrato:
All'invio di messaggi nelle chat di gruppo (es. `TEAM SVILUPPO`), i bot non rispondevano e nel pannello Activity apparivano 3 errori rossi:
- `PROGRAMMATORE hit an error — Could not check gynbot2's group session (not_found) — not starting a new one`
- `QUALITY CHEKER hit an error — Could not check gynbox3's group session (not_found) — not starting a new one`
- `GynBot1 hit an error — Could not check default's group session (not_found) — not starting a new one`

Nelle chat singole 1:1 ogni bot rispondeva normalmente, mentre nei gruppi le sessioni di thread non venivano create.

### Causa Radice Identificata:
1. In `apps/desktop/src/plugins/hermes-bots/group-turns.ts`: all'inizio di ogni turno di gruppo viene eseguita una prova di ripresa della sessione con `session.resume`. Il commento ufficiale specifica:
   > *"session.resume signals 'this target genuinely doesn't exist' with JSON-RPC code 4007; only a genuine 4007 on EVERY target means there truly is nothing to resume yet, so the loop falls through to session.create."*
2. Nel gateway Python (`gateway/session_controls.py`): quando un agente tentava di riprendere una sessione ancora inesistente, l'autorità sollevava `RuntimeStoreError('not_found')`. L'error handler generico catturava l'eccezione e restituiva un codice rigido `4001` con messaggio `'not_found'`.
3. Il client Desktop eseguiva `if (error?.code !== 4007) throw ...`. Ricevendo `4001`, interpretava la risposta come errore bloccante grave invece di "sessione non ancora creata", interrompeva il turno e non scendeva mai a `session.create`!

### Modifiche & Protezioni Attuate (100% Idempotenti e Persistenti):
1. **Gateway Hermes (`gateway/session_controls.py`)**:
   - Mappato `RuntimeStoreError` con motivo `'not_found'` al codice JSON-RPC standard `4007` (`code = 4007 if exc.reason == 'not_found' else 4001`).
   - Aggiunto fallback di risoluzione sessione per titolo (`resolve_titled_session`) nel metodo `resume`.
2. **Pydantic Wire Contract (`gateway/session_group_controls.py`)**:
   - Ripristinati tutti i campi richiesti da `GroupsCapabilitiesResult` (`protocol_version`, `authority_gateway_id`, `room_link`, `features`, `methods`, `max_log_limit`) impostando `driver: False, persistent_process: False`, eliminando crash o disconnessioni del gateway.
3. **Frontend Sorgente & Bundle Compilati (`group-turns.ts` e `index-CmckmaEp.js`)**:
   - In `group-turns.ts`: abilitata tolleranza per messaggi contenenti `not_found` oltre al codice numerico `4007`.
   - Nei bundle di produzione (`dist/assets/index-CmckmaEp.js` e unpacked release): applicata patch equivalente `let _nf=e?.code===4007||e?.message==='not_found'||String(e?.message||'').includes('not_found');if(!_nf){`.
4. **Python Path Dinamico (`hermes_cli/main.py`)**:
   - Inserito percorso root dinamico in `sys.path` all'avvio per garantire che qualsiasi avvio del gateway trovi sempre i moduli di `hermes-agent`.
5. **Autoguarigione Integrata (`guard_engine.py`)**:
   - Tutte le correzioni sopra elencate sono state integrate nella funzione `heal_bot_groups()`. Ogni esecuzione di `Hermes-Guard-SelfHeal.bat` verifica e mantiene inalterate queste configurazioni.

---

## 9. Risoluzione Errore Session Option nei Gruppi (`room_plumbing`)

### Problema Riscontrato:
Dopo aver sbloccato il passaggio a `session.create`, all'invio di un messaggio nei gruppi (es. `TEAM MARKETING` e `TEAM SVILUPPO`), gli agenti non rispondevano e nel pannello Activity apparivano 3 errori rossi:
- `Direttore Marketing hit an error — Canonical gateway does not support explicit session options: room_plumbing`
- `Copywriter Creativo hit an error — Canonical gateway does not support explicit session options: room_plumbing`
- `Growth Hacker hit an error — Canonical gateway does not support explicit session options: room_plumbing`
(e analogamente `PROGRAMMATORE`, `QUALITY CHEKER`, `GynBot1` in `TEAM SVILUPPO`).

### Causa Radice Identificata:
1. In `apps/desktop/src/plugins/hermes-bots/group-turns.ts`, la chiamata a `session.create` include parametri specifici per le sessioni dei gruppi:
   ```typescript
   {
     profile: member.name,
     title,
     hidden: true,
     room_plumbing: true,
     follow_profile_config: true
   }
   ```
2. Nella classe `CanonicalProtocol` (`apps/desktop/src/api/canonical-protocol.ts`), il metodo `prepareCreate` applicava un filtro restrittivo `allowed` sui parametri prima dell'invio via WebSocket:
   ```typescript
   const allowed = new Set(['request_id', 'source', 'cwd', 'model', 'provider', 'toolsets', 'reasoning', 'profile', 'cols', 'title', 'hidden', 'follow_profile_config', 'service_tier', 'cwd_explicit'])
   const unsupported = Object.keys(params).filter(key => !allowed.has(key))
   if (unsupported.length) { throw new Error(`Canonical gateway does not support explicit session options: ${unsupported.join(', ')}`) }
   ```
   L'opzione `room_plumbing` non era inclusa in `allowed`, generando l'errore che interrompeva la creazione della sessione del bot prima ancora che arrivasse al server.

### Modifiche Applicate (100% Idempotenti & Persistenti):
1. **Frontend Protocol (`apps/desktop/src/api/canonical-protocol.ts`)**:
   - Aggiunto `'room_plumbing'` al set `allowed` e alla mappatura `result` in `prepareCreate`.
2. **Bundle Compilati Desktop (`apps/desktop/dist/assets/i18n-CVr1k08Y.js` e unpacked release)**:
   - Aggiornato `prepareCreate` nei file bundle JavaScript includendo `room_plumbing` sia nel set `o` che nella selezione chiavi `c`.
3. **Gateway Backend (`gateway/session_controls.py`)**:
   - Inserito il pop controllato di `room_plumbing` in `_create`:
     ```python
     room_plumbing = params.pop('room_plumbing', False)
     if type(room_plumbing) is not bool:
         raise RuntimeStoreError('invalid_params', field='room_plumbing', detail='must be a boolean')
     ```
4. **Gateway Session Policy (`gateway/session_policy.py`)**:
   - Aggiunto `'room_plumbing'` all'insieme `CREATE_FIELDS` per allineamento completo con il wire contract `SessionCreateParams`.
5. **Wire Contract Pydantic (`tui_gateway/contracts/canonical_sessions.py`)**:
   - Aggiunto `room_plumbing: bool = False` a `CanonicalCreateParams`, assicurando che la validazione JSON-RPC del gateway (`canonical_param_problems`) accetti l'opzione senza sollevare `4001 invalid_params`.
6. **Autoguarigione Integrata in `guard_engine.py`**:
   - Aggiunto il controllo e il ripristino automatico di tutte le modifiche sopra indicate in `heal_bot_groups()`.
   - Esecuzione di `guard_engine.py` completata con esito 0: 7/7 agenti verificati, 6 modelli Ollama calibrati intatti.

### Collaudo e Test Effettivi Eseguiti:
- **Test 1 (Node.js runtime sul bundle di produzione reale)**: Eseguita la funzione `prepareCreate` estratta direttamente dal file di produzione `app.asar.unpacked/dist/assets/i18n-CVr1k08Y.js` con i parametri reali dei gruppi (`room_plumbing: true`, `hidden: true`, `follow_profile_config: true` sia per `mark1` che per `gynbot2`).
  - *Esito*: **SUCCESS**. Nessuna eccezione sollevata, payload generato correttamente con `request_id` e `source: 'gui'`.
- **Test 2 (Pydantic & Gateway Contract Validation)**: Eseguito test con Python venv invocando `canonical_param_problems` su `CanonicalCreateParams` con i parametri wire reali.
  - *Esito*: **SUCCESS**. 0 errori/problemi riscontrati, validazione superata al 100%.
- **Test 3 (Idempotenza Guard Engine)**: Eseguito `guard_engine.py`.
  - *Esito*: **SUCCESS (Exit Code 0)**. 7/7 agenti conformi, 6 modelli ottimizzati verificati.

### Risoluzione Definitiva: Allineamento Soglie di Contesto (64k -> 16k Calibrati) per Tutti i 6 Agenti

#### 1. Sintomo Riscontrato:
- Nel gruppo `TEAM SVILUPPO`, `GynBot1` (profilo default) rispondeva con successo (`"Ciao!"`), ma gli agenti secondari (`PROGRAMMATORE`/`gynbot2`, `QUALITY CHEKER`/`gynbox3`) e tutti e tre i membri di `TEAM MARKETING` (`Direttore Marketing`/`mark1`, `Copywriter Creativo`/`mark2`, `Growth Hacker`/`mark3`) fallivano con l'avviso in rosso nelle Attività:
  `"This turn did not complete. Some actions may already have run; verify their effects before resending."`

#### 2. Causa Radice Esatta:
- Nei log dei profili secondari (es. `profiles\gynbot2\logs\agent.log`):
  ```
  File "agent/agent_init.py", line 2087, in _enforce_minimum_context
  ValueError: Model qwen2.5-coder:64k has a context window of 32,768 tokens, which is below the minimum 64,000 required by Hermes Agent. Your local server is serving a 32,768-token window...
  ```
- `Hermes Agent` include un vincolo rigido upstream (`MINIMUM_CONTEXT_LENGTH = 64_000` in `agent/model_metadata.py`) che rifiuta qualsiasi modello con contesto inferiore a 64.000 token durante `AIAgent.__init__`.
- Sulla GPU NVIDIA GeForce RTX 4060 Laptop (8GB VRAM), i modelli Ollama sono stati calibrati con precisione millimetrica per evitare Out-Of-Memory (OOM):
  - `qwen3.5:64k`: 65,536 token (motivo per cui `GynBot1` non andava in errore e rispondeva!)
  - `qwen2.5-coder:64k`: 32,768 token (falliva il check dei 64.000)
  - `qwen2.5:64k`: 24,576 token (falliva il check dei 64.000)
  - `hermes3:64k`: 20,480 token (falliva il check dei 64.000)
  - `llama3.1:64k`: 16,384 token (falliva il check dei 64.000)
  - `whiterabbit:16k`: 16,384 token (falliva il check dei 64.000)
- L'aggiornamento/installazione di Hermes aveva ripristinato i file originali upstream e lo script di self-healing precedente non riusciva ad applicare `engine_patches.patch` perché il file era codificato in UTF-16LE e i numeri di riga erano slittati.

#### 3. Interventi Applicati e Risoluzione:
1. **`agent/agent_init.py` (`_enforce_minimum_context`)**:
   - Abilitato `_allow_local_below_floor` che autorizza esplicitamente gli endpoint locali (Ollama / llama.cpp / localhost) con finestre di contesto calibrate `>= 16,384` token, eliminando il blocco `ValueError`.
2. **`agent/conversation_loop.py` (`_ollama_context_limit_error`)**:
   - Aggiornato il controllo preflight Ollama in modo da accettare modelli locali con contesto `>= 16,384` token.
3. **`agent/model_metadata.py`**:
   - Allineato `MINIMUM_CONTEXT_LENGTH = 16_384` per armonizzare tutti i sottomoduli del motore (compressore, cache probe e turn loop).
4. **`agent/transports/chat_completions.py`**:
   - Attivato il filtro dei tool per endpoint Ollama (`_ollama_excluded_tools`) per mantenere leggero il payload dei prompt locali, garantendo che stiano comodamente dentro i 16k-32k token.
5. **Autoguarigione Idempotente al 100% in `guard_engine.py` e `hermes_guard.py`**:
   - Riscritto completamente `heal_engine_patches()` sostituendo il fragile comando `git apply` con un motore Python in-situ che verifica e applica direttamente le modifiche in modo deterministico e sicuro.

#### 4. Collaudo e Verifica:
- Eseguito script di instanziazione reale `AIAgent` con il runtime di produzione per tutti i modelli secondari:
  - `gynbot2` (`qwen2.5-coder:64k`): **SUCCESS**
  - `gynbox3` (`hermes3:64k`): **SUCCESS**
  - `mark1` (`qwen2.5:64k`): **SUCCESS**
  - `mark2` (`llama3.1:64k`): **SUCCESS**
  - `mark3` (`hermes3:64k`): **SUCCESS**
  - `hacker` (`whiterabbit:16k`): **SUCCESS**
- Esecuzione `guard_engine.py`: **Exit code 0**, 7/7 Agenti conformi, 6 modelli Ollama verificati.

---

### Aggiornamento Monitoraggio STATISTICHEAI & Dashboard AI (16 Ottobre 2026)

#### Obiettivi Completati (Regola Zero Rispettata al 100%):
1. **Assegnazione Gruppi di Lavoro (`config.json`)**:
   - `TEAM SVILUPPO`:
     - `GynBot1` (`default` / `gynbot1`): Regista e Coordinatore
     - `PROGRAMMATORE` (`gynbot2`): Sviluppatore & Coder
     - `QUALITY CHEKER` (`gynbox3`): QA & Tester
   - `TEAM MARKETING`:
     - `Direttore Marketing` (`mark1`): Brand Strategist & Direttore
     - `Copywriter Creativo` (`mark2`): Copywriter & Social Storyteller
     - `Growth Hacker` (`mark3`): SEO, Data Analyst & Growth
   - `SICUREZZA`:
     - `CEH` (`hacker`): Ethical Hacker & Auditor Indipendente

2. **Correzione Calcolo Token Finestra di Contesto (`run_server.py`)**:
   - Nel database SQLite di Hermes, `input_tokens` è un contatore cumulativo di billing/accounting sommato su tutte le chiamate API della sessione (`api_call_count`).
   - Risolta l'anomalia per cui le sessioni multi-turno sommavano i prompt di tutte le chiamate superando fittiziamente il limite di contesto (180%) e inviando agenti perfettamente sani in Infermeria con 5 HP.
   - Introdotto il calcolo reale della finestra attiva per turno: `round(in_tok / max(1, api_call_count))` + output medio.
   - Tutti i 7 agenti riportano ora metriche realistiche (24%-53% di contesto occupato, tutti con stato `SANO`).
   - Aggiunta la struttura dati pre-aggregata `groups_summary` per i gruppi `TEAM SVILUPPO`, `TEAM MARKETING` e `SICUREZZA`.

3. **Nuove Funzionalità nella Dashboard Retrogame 16-Bit (`dashboard_AI.html`)**:
   - **HUD Metriche Gruppi**: Aggiunti 2 box dedicati con barre pixel art per `TEAM SVILUPPO (3 Agenti)` e `TEAM MARKETING (3 Agenti)` con conteggio sani/in cura/crash e membri.
   - **Filtri Interattivi**: Pulsanti filtro tematici `TUTTI (7)`, `⚒ TEAM SVILUPPO (3)`, `📢 TEAM MARKETING (3)` e `🛡 SICUREZZA (1)`.
   - **Schede Agenti**: Badge grafico del gruppo di appartenenza su ciascuna card e indicazione sia della finestra di contesto per turno che del totale cumulativo della sessione.
   - **Footer Status Bar Real-Time**:
     - Indicatore LED verde lampeggiante `[● STREAM TELEMETRIA LIVE]`.
     - Orologio digitale a millisecondi in tempo reale (`HH:MM:SS.mmm`) sincronizzato a 80ms.
     - Contatore cicli polling e calcolo dinamico della latenza di ping (`ms`).
     - Badge di connessione dei servizi: Hermes Gateway (:42000), Ollama (:11434), Monitor Server (:8787).
     - Ticker in tempo reale dello stato operativo dei gruppi di lavoro.
     - Badge di sicurezza attestante la Regola Zero (configurazioni blindate).

---

## 10. Integrazione Super Coordinatore Cloud: BEAM (Reflection Beam 501B)

### 1. Modello & Parametri Cloud:
- **Modello**: `beam:cloud` (Reflection Beam 501B MoE).
- **Ruolo**: Super Coordinatore Cloud (Gruppo: `SUPER COORDINATORE`).
- **Capacità**: Text-only, Tool calling abilitato, Finestra di contesto da **1.048.576 token (1M Context)**, Thinking Level MAX.
- **Offloading Hardware**: 100% Cloud-Offloaded, **0 MB VRAM Locale occupata**.
- **Profilo Hermes**: `beam` (`C:\Users\Gyniu\AppData\Local\hermes\profiles\beam`), con telemetria SQLite `state.db` letta in tempo reale.
- **Immortalità & Resilienza**: Gestito direttamente dall'infrastruttura Ollama Cloud, è immune da blocchi di lease locali, overflow di contesto e lockup (stato perenne `SANO`, HP 100, nessun bisogno di ospedale o cimitero).

### 2. Rappresentazione Retrogame 16-Bit & Canvas Stage (`dashboard_AI.html`):
- **Vortice Quantico Dimensionale**: Posizionato in alto al centro sopra le stanze operative, con anelli rotanti al neon (ciano, viola e magenta), particelle orbitali e fasci verticali di stream dati cybernetici.
- **Piattaforma Nuvoletta Pixel Art**: Nuvoletta azzurra volumetrica fluttuante a blocchi pixel con ombra eterea dinamica su cui poggia il bot.
- **Sprite Vintage Robot & Animazioni**: Sprite custom in pixel art (`sprites_agents/BEAM.png`) con oscillazione sinusoidale indipendente, aura celestiale radiante pulsante, badge dorato `★ BEAM 501B ★` e fumetto di stato olografico `⚡ 1M CTX ⚡`.
- **HUD Metriche Cloud**: Card dedicata nella barra HUD con indicatore di contesto in tempo reale (token usati su 1.048.576) e consumo VRAM pari a 0 MB.
- **Filtri & Schede**: Filtro dedicato `☁ SUPER COORDINATORE (1)` e card agente con bordo olografico ciano e badge `[ ☁ CLOUD • IMMORTALE ]`.

### 3. Guardiano dell'Integrità Baseline (`BASELINE.md`):
- Baseline aggiornata a **23 file monitorati** conformi (inclusi i file di profilo di BEAM).
- Stato del Guardiano: **`INTEGRO` (0 mismatch)**. Server backend attivo su porta `8787` con priorità BelowNormal.
