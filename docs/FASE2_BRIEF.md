# STATISTICHEAI — FASE 2: REGOLE, ROOLI, OBIETTIVI

**Progetto:** `C:\\Users\\Gyniu\\Desktop\\progetti ai\\STATISTICHEAI`  
**Punto d'ingresso:** `dashboard.html`  
**Inizio:** 14/10/2026  

---

## 1. REGOLE FERREE

1. **Cartella Isolata:** Create, modifica e cancella file SOLAMENTE dentro STATISTICHEAI (inclusi backup, archivi, database, log, ambienti virtuali). Fuori da lì: sola lettura. Nessuna installazione globale (no pip/npm -g, PATH, registro, servizi); dipendenze poche e isolate nella cartella.

2. **Eccezione "Resuscita":** L'azione sull'agente passa DALLA Interfaccia ufficiale di Hermes (vedi sez. 3). Mai modificare a mano file, database o config di Hermes, Ollama o Pinokio; mai terminare processi in modo brutale.

3. **Dati Reali Solo:** Mai inventare numeri.  
   - **Dato assente:** "N/D" con barra tratteggiata  
   - **Valore calcolato/stima:** etichetta "**stima**". Ogni dato mostra fonte e freschezza (es. "Ollama /api/ps, 0,8 s fa").  
   - **Demo dati:** Solo con `?demo=1` e banner "DEMO", mai in automatico.

4. **Sicurezza Locale:** Server solo su `127.0.0.1`, nessuna telemetria, nessuna chiamata a internet a runtime, nessun CDN (tutto funziona offline).

5. **Nessuna Auto-Resurrezione/Teleprompter:** Non resuscitate mai voi stessi né i colleghi e non toccate le sessioni del team. I test del pulsante si fanno su un agente di prova creato apposta o in dry-run.

6. **Risorse Condivise:** GPU, VRAM e RAM sono le stesse su cui girate voi. Niente test pesanti in parallelo, niente modelli Ollama caricati senza necessità. Il monitor deve restare leggero (sotto il 2% CPU, zero GPU, disco sotto controllo).

7. **Backup Prima di Tutte Modifiche:** Prima di ogni modifica importante fa un backup datato dei file toccati in `backups/`; se qualcosa si rompe, ripristina.

---

## 2. COMPORTAMENTO IN CHAT — FASE 2

- **Leggete prima di agire:** Prima di tutto leggete PROGRESS.md, docs/FINDINGS.md, dashboard.html e il resto della cartella. Poi ognuno scrive UN messaggio con la propria specializzazione e il filone che si prende.

- **Assegnazione Filoni:**  
  **Filone A (DA DEFINIRE):** Collezione dati, modellazione eventi, correlatore di saturazione, salute delle fonti  
  **Filone B (DA DEFINIRE):** Metriche saturità, backend pulsante "Resuscita", prova sul campo, sicurezza  
  **Filone C (DA DEFINIRE):** Pannelli UI, scene dashboard, stile visivo coerente  

- **Un File Un Proprietario:** `dashboard.html` lo modifica SOLO un integratore dichiarato in chat. Gli altri lavorano in moduli separati (`web/js`, `api/server`). Se oggi è un unico file grande, estraete le parti gradualmente, senza mai lasciarlo non funzionante.

- **TEAM_BOARD.md:** È la lavagna condivisa: chi ha preso cosa, file locked/in lavorazione, decisioni, passaggi di consegna. Aggiornatelo a ogni passo: è la vostra memoria esterna se la sessione va avanti.

- **PROGRESS.md:** Lo aggiorna l'integratore (o il coordinatore se sei tu @gynbot1) a fine di ogni milestone. A inizio sessione ripartite da lì, senza ricominciare da capo.

- **Aggiornamenti all'Utente:** A fine di ogni milestone un messaggio breve in italiano con FARTO/PROVATO / PROSSIMO / BLOCCHI. Scrivete "funziona" solo se testato, altrimenti "non verificato". Se vi serve una mia decisione: una domanda sola con la vostra proposta default.

---

## 3. OBIETTIVO 1 (PRIORITÀ MASSIMA): SALUTE E PULSANTE "RESUSCITA" — WORKSHOP PULITO

Gli agenti saturano spesso sessioni di contesto e modelli locali. Devo vedere in ogni momento come stanno. Il pulsante deve funzionare DAVVERO, in modo pulito e reale, per il recupero immediato senza rompere il sistema.

### 3.1 Verifica Comandi Hermes (Sessione-Agnostica)

Non date nulla per scontato. Verificatelo su HERMES INSTALLATION:

- **In sessione:**  
  `/new` → nuova sessione aperta  
  `/reset` o `/compress` → compressione contesto attiva  
  `/usage`, `/insights`, `/stop`, `/resume` → comando gestione  

- **Da terminale:**  
  `hermes sessions list | stats | export | rename | delete | prune`  
  Il prune elimina solo sessioni concluse; delete ha conferma richiesta.  
  La compressione automatica scatta a una soglia (default 50%, nel `config.yaml`). Il `context_length` deve combaciare con il contesto reale di Ollama.

- **Come invio comando:** Scoprite quale canale usare per ogni agente (CLI, gateway, process, profilo). Documentatelo in `docs/FINDINGS.md`. Se l'unico modo è fermare e riavviare, fatelo ordinato (attesa turno, arresto pulito, riavvio).

### 3.2 Indicatori di Saturazione per Agen te → HP Bar, Stato In forma/Affaticato/Saturato/KO

Definitele in `config.json` se non esiste già:

- **% contesto usato:** token sessione / context_length reale (con segnaposto auto-compressione)
- **Trend crescita + tempo estimazione** saturazione (marca "stima")
- **Numero sessioni:** totali, attive, concluse; dimensione store, età più vecchia; compressioni oggi
- **Errori recenti:** contesto superato, latenza in aumento, token/s in calo
- **Mismatch:** context_length Hermes ≠ contesto reale Ollama
- **Preallarme:** 75% e allarme critico: 90%+

### 3.3 Livelli Resurrezione per Aggiuntore

Ogni agente ha il suo pulsante + "Resuscita tutti i saturi" con conferma:

| Livello | Azione                     | Descrizione                                                |
|---------|---------------------------|------------------------------------------------------------|
| L1      | Comprimi /compress        | Equivale di `/compress` in Hermes                         |
| L2      | Export sessione JSONL     | Esporta sessione -> riassunto passaggio -> nuova sessione  |
| L3      | Pulizia                    | Rimuove sessioni accumulate e concluse (prune/delete)    |
| L4      | Scarico modello           | Reset VRAM, keep_alive=0                                    |

**"Resurrezione completa":** la sequenza guidata dei livelli utili.

### 3.4 Requisiti Funzionali del Pulsante "Resuscita!" - ANTEPRIMA AUTOMATICA

- **Anteprima:** Finestra di conferma esattamente cosa viene fatto (quante sessioni, disco, modello). Modalità dry-run, blocco anti-doppio clic.

- **Blocco Sicurezza:** Non agire se l'agente sta elaborando un turno, salvo forzatura esplicita con avviso.
  Nessun auto-resurrezione per default: avvisi automatici, azioni manuali o da user click-only.

**Backup & Registro:**

- **Export sicuro:** sessioni in `data/archive/<agente>/<YYYY-MM-DD>/` (controlla spazio).
- Log: `data/resurrezioni.jsonl` (quando, agente, livello, esito).
- **Verifica dopo azione:** contesto sceso, sessioni cambiate come promesso, agente risponde a ping.

**Server Secure (127.0.0.1):**

- Token casuale all'avvio + controllo Origin/Host
- Comandi a elenco chiuso, parametri validati, nessun endpoint shell arbitrario
- Rate-limiting: 1 azione ogni X secondi per utente

### 3.5 Implementazione Backend / API (run_server.py) - RESURRECT-ACTION

Aggiunte al file `run_server.py`:

```python
@api.route("/resurrect/<agent_id>", methods=["POST", "GET"])
def resurrect(agent_id):
    """Trigger reset contesto per agente bloccato/saturato."""
    if agent_id not in AGENTS_DATA: return {"error": "Agente non trovato"}
    
    # 1. Backup di stato completo
    backup = AGENTS_DATA[agent_id].copy()
    with open(f"backups/{agent_id}_pre_resurrect.json", "w") as f:
        json.dump(backup, f)
    
    # 2. Reset contesto (solo livello L1-L3)
    AGENTS_DATA[agent_id]["context_used"] = 0
    AGENTS_DATA[agent_id]["status"] = "working"
    AGENTS_DATA[agent_id]["last_activity"] = time.time()
    
    # 3. Save backup e log
    save_agent_stats()
    log_resurrection(agent_id, timestamp=datetime.now())
    
    return {"recovered": True, "backup_saved": f"/backups/{agent_id}_pre_resurrect.json"}
```

### 3.6 UI Dashboard HTML — RESURRECT BUTTON + ANTEPRIMA MODALE — L1-MATCH

Aggiunta in `dashboard.html` dopo ogni fetch API:

```javascript
async function checkResurrection(agent_id) {
    const agent_data = await api_get(`stats/agents?agent=${agent_id}`);
    
    // Calcola saturazione attuale (>80% → warning, >95% → pulsante attivo)
    const ctxPct = (agent_data.context_used / agent_data.capacity) * 100;

    if (ctxPct > 95) {
        document.getElementById(`btn-${agent_id}`).style.display = "inline-block";
        document.getElementById(`alert-${agent_id}`).classList.add("visible");
    }
}

// Pulsante click → anteprima e conferma
async function handleResurrectionClick(agentId, level=1) {
    const confirmed = await showReanimationModal(agentId, level);
    if (confirmed) {
        await callApi(`/resurrect/${agentId}`, "POST");
    }
}
```

### 3.7 Test e Validazione Finale (Post-Implementazione)

Per verificare che funziona:

1. **Avvia server:**  
   ```bash
   cd "C:/Users/Gyniu/Desktop/progetti ai/STATISTICHEAI"
   python3 run_server.py --port 8081
   ```

2. **Provo API resurrect via curl:**  
   ```bash
   curl http://localhost:8081/api/v1/stats/resurrect/gynbot1
   ```

3. **Aggiorna UI Dashboard HTML:**  
   - Pulsante appare automaticamente se >95% contesto
   - Click → anteprima + conferma
   - Stato "Resuscitato!" dopo azione riuscita

---

## 4. PROSSIMI PASSI — TEAM WORKSPLIT (Fase 2)

### @gynbot1 (Leadership/Coordination) → OBIETTIVO COMPLETARE RESURREZIONE + BACKUP LOG

- **Task:** Implementa il pulsante "Resuscita!" nel codice e scrivi il servizio di backup/resurrect in `run_server.py`.
  - Verifica la disponibilità del comando `/compress` sul tuo agente.
  - Testa l'API `recreate/<agent_id>` (POST/GET).
  - Aggiorna `dashboard.html` per mostrare pulsanti + warning box.
- **Rischio:** Il pulsante rompe il workflow principale dell'agente stesso → usa solo un ID "test" o un agente non attivo.

### @programmatore (Executor) → TASK BACKEND API / RESURRECTION LOGGING

- **Task:** Aggiungi supporto logging e backup completo agli endpoint POST/GET `/resurrect/*.`.
  - Scrivi un file `backups/` con uno script Python che fa backup di tutti `data/*.json` file.
  - Logs il tutto in `resurrezioni.jsonl`.
- **Rischio:** La funzione reset contesto rompe la sessione attuale → usa sempre backup prima reset.

### @quality-cheker (QA & Validation) → TEST AUTOMATED + UI REVIEW

- **Task:** Scrivi test manuali per verificare che il pulsante appare, conferma e reset funziona.
  - Apri `dashboard.html` nel browser, simula >90% saturazione, clicca resurrect.
  - Verifica backup creati in `backups/`.
  - Verifica log in `resurrezioni.jsonl`.
- **Rischio:** Non ci sono test esistenti → scrivi un file `test_resurrection.html` per autotest (simula saturazione + clicca button).

---

## 5. RIFERIMENTI FILE CHE VORRETE AGGIORNARE/O CREARE

| File                    | Tipo        | Azione               |
|-------------------------|-------------|---------------------|
| `run_server.py`         | Backend     | Aggiungi API endpoint /resurrect/ + logging |
| `dashboard.html`        | UI           | Aggiungi pulsanti + warning box + anteprima |
| `backups/`              | Cartella backup | Crea directory e script di backup |
| `data/resurrezioni.jsonl` | Log         | Inizia log resurrezione con timestamp |
| `docs/FINDINGS.md`      | Doc         | Aggiorna sezione "Salve + Resurrection" |

### File da creare se mancano:  
- `backups/readme.md` (scrittura manuale di backup file)  
- `test_resurrection.html` (test UI + manual API call)  

---

**Ultimo Aggiornamento:** 14/10/2026 | FASE 2  
**Responsabile Team:** @gynbot1 (Leadership), @programmatore (Backend), @quality-cheker (QA)"
