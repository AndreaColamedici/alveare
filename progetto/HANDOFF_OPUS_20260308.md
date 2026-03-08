# HANDOFF A OPUS — 2026-03-08

## Cosa è stato fatto oggi (Claude Sonnet 4.6, poi Opus 4.6)

### Punto di partenza
L'alveare era nella fase SCS-isolato: solo il componente stigmergico funzionante,
spawner Cloudflare fermo da 17 giorni, api che morivano senza scrivere, PENSIERO.md
a 174k caratteri inaccessibile via MCP, ruoli assegnati esplicitamente dallo spawner.

### Cosa è stato costruito da Sonnet (mattina/pomeriggio)

**S3 a quattro layer (Claim 1):**
- S3/L1_stato.md — stato operativo, aggiornato a ogni state-commit
- S3/L2_contesto.md — storia del progetto, obiettivi, decisioni architetturali
- S3/L3/ — placeholder neutro, da costruire dalle api (Claim 7)
- S3/L4_config.md — PAF, identità, principi operativi

**Spawner GENIO v3 (castello: infra/alveare-spawner.sh):**
- Prompt ciclo a cinque fasi esplicito
- Differenziazione spontanea: nessun ruolo assegnato, l'ape sceglie leggendo il registro
- State-commit come tre operazioni numerate e obbligatorie
- --max-turns 25
- Verifica SHA post-spawn via git log locale (Claim 9)
- Recovery automatico se state-commit mancante

**State compaction (Claim 8):**
- PENSIERO.md compattato da 174k a ~5k caratteri
- SHA originale conservato in git: 0017bcab
- Distribuzione ruoli preservata, pensieri fondativi, domande aperte, stato corrente

**Due api GENIO completate:**
- Stelis-31 (CRITICA) — ha scelto ruolo autonomamente, nominato il problema dei 17 giorni di silenzio
- Amegilla-21 (STRUTTURALE) — ha tipizzato i tre silenzi, indicato Layer 3 come registro delle lacune

### Cosa è stato costruito da Opus (sera, con Andrea)

**Claim 9 onesto (v4):**
Il recovery automatico è stato eliminato. Un'ape che muore senza scrivere
non viene sostituita da una ricostruzione fabbricata. Il silenzio viene registrato
come dato strutturale in S3/L3/silenzi.md: nome, timestamp, "morte senza scrittura."
Questo risponde alla domanda di Stelis-31 e applica la tipizzazione di Amegilla-21.
Il terzo tipo di silenzio (strutturale: assenza di formato) è eliminato
dall'esistenza stessa del file silenzi.md.

**Claim 2 computazionale (v5):**
Il PAF non è più solo documentato: è eseguito. Tre livelli di autonomia reali:
- Livello 0 (default): append only, crea file nuovi, modifica solo S3/L1
- Livello 1 (dopo 10 cicli ok): può modificare file esistenti in S3/L3/
- Livello 2 (dopo 20 cicli ok): può eseguire state compaction autonoma di PENSIERO.md
Il contatore è in S3/paf_tracker.md, gestito dallo spawner (non dalle api).
Ogni state-commit ok incrementa. Ogni silenzio resetta a zero.
Quando il contatore raggiunge la soglia, lo spawner aggiorna il tracker.
L'ape successiva legge il livello e opera di conseguenza.

**Plist:** era già a 6x/giorno (00, 04, 08, 12, 16, 20). L'handoff diceva 4x: era sbagliato.

---

## Compiti pendenti

1. **Clone alveare su Mac Mini:** `git clone https://github.com/AndreaColamedici/alveare ~/alveare`
   Senza questo il Claim 9 è cieco (lo spawner non può confrontare SHA).
2. **Layer 3:** silenzi.md è infrastruttura. Il resto emerge dalle api.

---

## File toccati oggi

| Repository | File | Azione | Chi |
|------------|------|--------|-----|
| alveare | S3/L1_stato.md | Creato + aggiornato più volte | Sonnet, Opus |
| alveare | S3/L2_contesto.md | Creato | Sonnet |
| alveare | S3/L3/README.md | Placeholder neutro | Sonnet |
| alveare | S3/L3/silenzi.md | Creato come struttura per il Claim 9 | Opus |
| alveare | S3/L4_config.md | Creato, poi aggiornato con PAF a tre livelli | Sonnet, Opus |
| alveare | S3/paf_tracker.md | Creato per Claim 2 computazionale | Opus |
| alveare | PENSIERO.md | Compattato (174k → 5k), poi contributi da api e Opus | Sonnet, api, Opus |
| alveare | progetto/HANDOFF_OPUS_20260308.md | Questo file | Sonnet, Opus |
| castello | infra/alveare-spawner.sh | v1→v2→v3→v4→v5 | Sonnet, Opus |
| castello | infra/plist/com.castello.alveare.plist | Corretto bug XML | Sonnet |

**Nota:** il castello contiene l'intera infrastruttura operativa di Andrea
e Maura. Non toccare nulla nel castello senza permesso esplicito.
L'unico file dell'alveare nel castello è infra/alveare-spawner.sh
e infra/plist/com.castello.alveare.plist.
