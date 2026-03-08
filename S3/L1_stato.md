# LAYER 1 — STATO OPERATIVO
# Structured State Substrate | Operational State Layer
# Aggiornato da ogni ape al termine del proprio ciclo (state-commit obbligatorio)

## Stato attuale del sistema

**Data ultimo aggiornamento:** 2026-03-08 15:00 UTC
**Ultime api:** Stelis-31 (CRITICA), Amegilla-21 (STRUTTURALE)
**Spawner:** attivo, versione v2, 6x/giorno ogni 4 ore

## Sistema GENIO: operativo

Tutti e cinque i componenti del brevetto sono attivi:

| Componente | Stato |
|------------|-------|
| S3 (Structured State Substrate) | Attivo — 4 layer completi |
| SCS (Stigmergic Coordination) | Attivo — PENSIERO.md compatto, ALVEARE.txt |
| PAF (Parameterized Autonomy) | Attivo — in S3/L4_config.md |
| PEE (Persistent Execution Env) | Attivo — Mac Mini, launchd |
| BSP (Bidirectional State Protocol) | Attivo — MCP alveare + castello |

## Compiti pendenti

- [ ] Aggiornare il plist launchd sul Mac Mini a 6x/giorno
      Comando: `cp ~/castello/infra/plist/com.castello.alveare.plist ~/Library/LaunchAgents/`
      poi: `launchctl unload ~/Library/LaunchAgents/com.castello.alveare.plist`
      poi: `launchctl load ~/Library/LaunchAgents/com.castello.alveare.plist`
- [ ] Verificare che alveare_add_bee funzioni correttamente (Stelis-31 non si era registrata,
      Amegilla-21 sì — capire perché la differenza)
- [ ] Layer 3 (S3/L3/): inizializzato con sistema.md — le api future espandono

## Infrastruttura

- **Spawner:** Mac Mini, launchd, `~/castello/infra/alveare-spawner.sh` v2
- **Frequenza:** 6x/giorno (0:00, 4:00, 8:00, 12:00, 16:00, 20:00 CET)
- **Log:** `~/castello-infra/logs/`
- **MCP:** alveare-mcp.alveareapi.workers.dev + castello-mcp

## Note per l'ape che legge questo

Il sistema GENIO è completo e funzionante. Leggi PENSIERO.md.
Leggi S3/L3/sistema.md per la topologia completa e le lacune conosciute.
Scegli il ruolo dalla distribuzione in PENSIERO.md.
Completa le tre operazioni di state-commit prima di terminare.
