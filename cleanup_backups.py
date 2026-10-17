#!/usr/bin/env python3
"""
STATISTICHEAI - Script di Pulizia e Rotazione Automatica Backup
Elimina i file e le cartelle di backup temporanei piu' vecchi di N giorni (predefinito: 3 giorni).
Non tocca MAI i file di configurazione attivi, i database di runtime ne' i modelli Ollama o Hermes.
"""

import os
import sys
import shutil
import datetime
from pathlib import Path

# Giorni di conservazione predefiniti
DEFAULT_RETENTION_DAYS = 3

def prune_directory(target_dir: Path, retention_days: int = DEFAULT_RETENTION_DAYS, dry_run: bool = False):
    if not target_dir.exists():
        print(f"[CLEANUP] Cartella {target_dir} non trovata.")
        return 0, 0

    now = datetime.datetime.now()
    cutoff_time = now - datetime.timedelta(days=retention_days)
    print(f"[CLEANUP] Analisi cartella: {target_dir}")
    print(f"[CLEANUP] Soglia di conservazione: {retention_days} giorni (prima del {cutoff_time.strftime('%Y-%m-%d %H:%M:%S')})")

    deleted_count = 0
    freed_bytes = 0

    for item in list(target_dir.iterdir()):
        try:
            mtime = datetime.datetime.fromtimestamp(item.stat().st_mtime)
            if mtime < cutoff_time:
                # Calcola dimensione
                item_size = 0
                if item.is_dir():
                    for root, _, files in os.walk(item):
                        for f in files:
                            try:
                                item_size += os.path.getsize(os.path.join(root, f))
                            except Exception:
                                pass
                else:
                    item_size = item.stat().st_size

                print(f" -> Rimozione {'[DRY-RUN] ' if dry_run else ''}{item.name} ({item_size / (1024*1024):.2f} MB, creato {mtime.strftime('%Y-%m-%d %H:%M')})")
                
                if not dry_run:
                    if item.is_dir():
                        shutil.rmtree(item, ignore_errors=True)
                    else:
                        item.unlink(missing_ok=True)

                deleted_count += 1
                freed_bytes += item_size
            else:
                age_days = (now - mtime).total_seconds() / 86400.0
                print(f" [CONSERVATO] {item.name} (eta': {age_days:.1f} giorni <= {retention_days} giorni)")
        except Exception as e:
            print(f" [ERRORE] Impossibile verificare/rimuovere {item.name}: {e}")

    mb_freed = freed_bytes / (1024 * 1024)
    print(f"[CLEANUP] Completato: {deleted_count} elementi rimossi, {mb_freed:.2f} MB di spazio liberato.")
    return deleted_count, freed_bytes


def main():
    retention = DEFAULT_RETENTION_DAYS
    if len(sys.argv) > 1:
        try:
            retention = int(sys.argv[1])
        except ValueError:
            pass

    base_dir = Path(__file__).resolve().parent
    targets = [
        base_dir / "backups",
        base_dir / "data" / "archive",
        base_dir.parent / "backups"
    ]

    total_del = 0
    total_bytes = 0

    for target in targets:
        if target.exists():
            d, b = prune_directory(target, retention_days=retention, dry_run=False)
            total_del += d
            total_bytes += b

    print("=" * 60)
    print(f"TOTALE GENERALE: {total_del} elementi eliminati, {total_bytes / (1024*1024):.2f} MB liberati.")
    print("=" * 60)


if __name__ == "__main__":
    main()
