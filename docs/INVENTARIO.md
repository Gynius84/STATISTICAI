# INVENTARIO FILE STATISTICHEAI

> Rilevamento automatico stato archivio al 2026-10-16.

## File Principali nella Root (`STATISTICHEAI\`)

| Nome File | Descrizione / Ruolo | Dimensione | Ultima Modifica |
|---|---|---|---|
| `dashboard_AI.html` | Entrypoint principale della dashboard web retrogame pixel art | 14.4 KB | 2026-10-14 23:55 |
| `run_server.py` | Backend HTTP server per telemetria reale, Guardiano e API | 27.8 KB | 2026-10-15 09:58 |
| `api_server.py` | Server API secondario legacy | 4.3 KB | 2026-10-14 19:08 |
| `backup_run.py` | Script utility per backup dello stato | 3.3 KB | 2026-10-15 09:51 |
| `PROGRESS.md` | Registro di avanzamento sprint e note operative | 4.1 KB | 2026-10-15 08:49 |
| `TEAM_BOARD.md` | Lavagna di coordinamento team | 4.1 KB | 2026-10-14 20:31 |
| `test_server.py` | Test unitari server backend | 2.0 KB | 2026-10-15 09:43 |
| `simple_test.html` | Pagina test minima per verifica API | 680 B | 2026-10-15 09:38 |
| `server.log` / `server.txt` | File di log locali del server | 236 B | 2026-10-15 10:19 |

## Documentazione (`docs\`)

| Nome File | Descrizione | Dimensione |
|---|---|---|
| `docs\BRIEF.md` | Specifiche integrali del committente e vincoli di progetto | 17.0 KB |
| `docs\BASELINE.md` | Baseline di riferimento, hash SHA-256 e parametri non segreti | 7.0 KB |
| `docs\INVENTARIO.md` | Inventario completo e dettagliato file e percorsi | Questo file |
| `docs\FINDINGS.md` | Mappatura agenti, profili, modelli, database SQLite e log | In creazione |
| `docs\STYLE.md` | Guida visuale retrogame pixel-art, canvas e animazioni | In creazione |
| `docs\RESURREZIONE.md` | Specifiche e procedure di dry-run livelli L1-L4 | In creazione |
| `docs\FASE2_BRIEF.md` | Brief storico Fase 2 | 11.5 KB |
| `docs\SPRINT0_FIX_SUMMARY.md` | Riepilogo bug fix Sprint 0 | 3.4 KB |
| `docs\TEAM_BOARD.md` | Copia documentale board | 5.3 KB |

## Sprite e Asset Pixel Art (`sprites_agents\`)

| Nome File | Agente Associato | Risoluzione | Formato |
|---|---|---|---|
| `GynBot1.png` | GynBot1 (Leadership / Regista) | 96x104 | PNG RGBA |
| `PROGRAMMATORE.png` | PROGRAMMATORE (GynBot2 / Dev) | 96x104 | PNG RGBA |
| `QUALITY CHEKER.png` | QUALITY CHEKER (GynBox3 / QA) | 96x104 | PNG RGBA |
| `Direttore Marketing.png` | Direttore Marketing (MARK1) | 96x104 | PNG RGBA |
| `Copywriter Creativo.png` | Copywriter Creativo (MARK2) | 96x104 | PNG RGBA |
| `Growt hacker.png` | Growth Hacker (MARK3) | 96x104 | PNG RGBA |
| `CEH.png` | CEH (HACKER / Pentester) | 96x104 | PNG RGBA |
| `retrogame_engine.html` | Prototipo motore canvas retro | 5.7 KB | HTML |
| `retrogame_sprites.html` | Prototipo visualizzatore sprite | 6.8 KB | HTML |

## Dati e Backup (`data\`, `backups\`)

| Cartella | Contenuto |
|---|---|
| `data\agent_stats.json` | Snapshot persistente stato agenti |
| `backups\` | Copie di sicurezza storiche (`backup_20261015_085021.json`, `run_server.py.bak20261015`, ecc.) |
