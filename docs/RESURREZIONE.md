# SPECIFICHE E PROTOCOLLO DI RESURREZIONE (LIVELLI L1 - L4)

> **STATO ATTUALE**: SERVER IN MODALITÀ PROTETTA (`actions_enabled: false` in `config.json`).
> Badge interfaccia: **"SOLA LETTURA"**. Nessuna operazione di scrittura viene eseguita automaticamente né senza esplicita abilitazione e token CSRF.

---

## 1. Principi di Sicurezza (Regola Zero)
1. **Configurazione Intatta**: Nessun flag di configurazione, parametro del modello, provider o soglia viene mai alterato.
2. **Nessun Ricarico Autonomo**: Lo scarico da Ollama (L4) passa `keep_alive: 0` senza opzioni aggiuntive. Il caricamento successivo è delegato unicamente a Hermes al momento del prossimo prompt.
3. **Controllo di Concorrenza**: Rifiuto categorico dell'azione se l'agente target è correntemente in turno o in esecuzione attiva.
4. **Export Obbligatorio Preventivo**: Nessuna sessione viene compressa o rimossa senza backup preliminare in `data\archive\<agente>\<timestamp>\`.

---

## 2. Dettaglio dei Livelli di Resurrezione

### Livello 1 (L1) — Compressione Sessione Attiva
- **Meccanismo**: Invio comando di compressione della cronologia attiva (equivalente a `/compress` in sessione Hermes).
- **Azione Eseguita**: Riduce il volume dei token archiviando la cronologia dettagliata in una memoria sintetica compatta.
- **Risultato Atteso**: La percentuale di contesto usato passa tipicamente dall'85-95% a meno del 25-30%, ripristinando l'agente allo stato "In forma".

### Livello 2 (L2) — Nuova Sessione con Staffetta (Handoff)
- **Meccanismo**:
  1. Export completo in formato JSONL della sessione attiva in `data\archive\<agente>\<data-ora>\session_dump.jsonl`.
  2. Generazione sintesi di passaggio: stato attuale, decisioni prese, file toccati, prossimi task.
  3. Creazione nuova sessione titolata con injection del riassunto di staffetta.
- **Risultato Atteso**: Azzeramento contesto della nuova sessione con piena continuità operativa del task.

### Livello 3 (L3) — Pulizia Sessioni Concluse (Prune Safe)
- **Meccanismo**:
  1. Individuazione delle sole sessioni concluse (stato `ended_at IS NOT NULL` e non archiviate).
  2. Export di sicurezza in `data\archive\<agente>\<data-ora>\concluded_sessions.jsonl`.
  3. Pulizia selettiva tramite `hermes -p <profile> sessions prune --older-than 1d`.
- **Risultato Atteso**: Recupero spazio su disco in `state.db` senza intaccare sessioni in corso o recenti.

### Livello 4 (L4) — Scarico Modello da VRAM (Ollama Eviction)
- **Meccanismo**:
  - Chiamata HTTP `POST http://127.0.0.1:11434/api/generate` con payload:
    ```json
    {
      "model": "<nome_modello>",
      "keep_alive": 0
    }
    ```
- **Condizioni di Sicurezza**:
  - Verifica preliminare se altri agenti condividono il modello (es. `hermes3:64k` condiviso tra `QUALITY CHEKER` e `Growth Hacker`). Se l'altro agente è in turno attivo, l'operazione viene bloccata con avviso.
- **Risultato Atteso**: VRAM liberata istantaneamente (da 4-6 GB a 0 GB occupati dal modello).

---

## 3. Matrice di Dry-Run e Comandi Simulati

| Livello | Agente Esempio | Modello | Comando Dry-Run Pianificato | Verifica Post-Azione |
|---|---|---|---|---|
| **L1** | `PROGRAMMATORE` | `qwen2.5-coder:64k` | `DRY_RUN: /compress su sessione attiva gynbot2` | Contesto sceso sotto soglia 75% |
| **L2** | `CEH` | `whiterabbit:16k` | `DRY_RUN: export jsonl + new session staffetta hacker` | Nuova sessione creata con handoff |
| **L3** | `GynBot1` | `qwen3.5:64k` | `DRY_RUN: backup + prune concluse (> 24h) default` | Numero sessioni diminuito |
| **L4** | `mark2` | `llama3.1:64k` | `DRY_RUN: POST /api/generate {model: "llama3.1:64k", keep_alive: 0}` | Modello assente in `ollama ps` |
