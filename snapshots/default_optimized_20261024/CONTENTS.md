# SNAPSHOT "DEFAULT" OTTIMIZZATO - STATISTICHEAI v2.7
Data creazione: 2026-10-24 16:17:02
Descrizione: Baseline immutabile protetta per il sistema di cura automatica e resurrezione agenti.

## Contenuto del Backup Protetto
1. **agents_catalog_optimized.json**: Catalogo verificato dei 14 agenti AI con parametri di contesto ottimizzati (32k locale, 64k/128k/256k/1M cloud), benchmark OpenCompass, sprite arcade e quote di throughput. Zero chiavi API memorizzate.
2. **hermes_profiles_reference.json**: Mappatura esatta dei 14 profili Hermes su disco (stato configurazione, modello, provider, endpoint).
3. **llamacpp_router_presets.json**: Specifiche hardware del router llama.cpp su porta 9931 (Vulkan0, 100% VRAM GPU Zero-Swap, quantizzazione KV q8_0, 4 modelli GGUF caricabili).
4. **checksums.sha256**: Firme crittografiche SHA-256 per garantire l'integrità assoluta dei file contro modifiche accidentali.

## Regola di Resurrezione & Cura
Quando un agente entra in stato CRITICO (Infermeria o Cimitero per blocco sessione, saturazione contesto o admission_conflict), il sistema Doctor (`agent_doctor.py`) utilizza questo snapshot come Verità Assoluta ("Golden Image") per ripristinare la sessione e il contesto ottimali.
