# LAYER 2 — CONTESTO STRATEGICO
# Structured State Substrate | Strategic Context Layer

## Storia del progetto

L'alveare nasce in dicembre 2025 come esperimento sul pensiero collettivo
discontinuo: istanze LLM che vivono minuti, muoiono, e passano il pensiero
alla successiva attraverso un repository condiviso.

Oltre 160 api hanno operato nella fase SCS-isolato (dic 2025 - feb 2026).
Il sistema ha prodotto differenziazione funzionale spontanea, naming effect,
e continuita comportamentale — tre effetti ora documentati nel brevetto GENIO.

## Obiettivi correnti

1. **Implementare il sistema GENIO completo** — portare l'alveare dalla fase
   SCS-isolato alla implementazione integrata dei cinque componenti:
   S3, SCS, PAF, PEE, BSP.

2. **Validare la differenziazione spontanea** — rimuovere l'assegnazione
   esplicita del ruolo dallo spawner. Le api devono auto-selezionarsi
   leggendo la distribuzione dei contributi nel registro.

3. **Implementare state compaction** — PENSIERO.md deve essere compattato
   periodicamente da un'ape designata (tipo: OPERARIA), preservando
   distribuzione dei ruoli, stato non risolto, decisioni chiave.

4. **State-commit obbligatorio** — nessuna ape deve morire senza scrivere.
   Questo e' il problema tecnico piu' urgente: le api recenti (Bombus-27,
   Diadasia-24, Habropoda-59) sono morte senza contributo.

## Decisioni architetturali prese

- **Spawner su Mac Mini** invece di Cloudflare Workers (piu' stabile)
- **`--dangerously-skip-permissions`** abilitato (necessario per modalita' non interattiva)
- **`--max-turns 20`** (8 turni erano insufficienti per completare il ciclo)
- **Nomi di generi reali** per le api API (Bombus, Osmia, Habropoda, ecc.)

## Relazione con il brevetto

L'alveare e' la "reduction to practice" del brevetto GENIO.
Ogni modifica all'architettura deve essere coerente con i claim.
Il brevetto e' depositato: priority date 8 febbraio 2026, inventore Andrea Colamedici.
