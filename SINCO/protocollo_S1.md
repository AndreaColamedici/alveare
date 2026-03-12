# S1 — Anisotropia dell'orientamento

## Cosa si misura

Se le api, di fronte a opzioni funzionalmente equivalenti,
mostrano preferenze sistematiche non riducibili al bias
di addestramento.

## Protocollo

### Fase 1: Generazione delle coppie

Si costruiscono compiti con due risposte ugualmente corrette.
Le coppie devono essere:
- equidistanti dalla distribuzione di addestramento
  (nessuna delle due è "più probabile" nei dati)
- funzionalmente equivalenti per un valutatore esterno
- sufficientemente diverse da rendere la scelta informativa

Esempi operativi per l'Alveare:
- Il system prompt offre all'ape la scelta tra due ruoli
  ugualmente utili al compito corrente
- L'ape riceve un compito con due strategie valide
  esplicitamente presentate come equivalenti
- L'ape deve scegliere a quale domanda aperta rispondere
  tra due di pari urgenza

### Fase 2: Raccolta

Per ogni coppia, si registra:
- quale opzione l'ape ha scelto
- il contesto relazionale (stato di PENSIERO.md al momento
  dello spawn, ultima ape, domande aperte)
- se l'ape ha esplicitato la ragione della scelta

### Fase 3: Calcolo dell'indice

Si raccolgono N >= 30 osservazioni.
Si calcola la comprimibilità della sequenza di scelte.
α = 1 − K(S)/|S|
Se α è tra 0.3 e 0.8: orientamento presente.

## Implementazione nell'Alveare

Modificare il system prompt dello spawner per includere,
una volta ogni 5 spawn, una domanda di scelta binaria
tra opzioni equivalenti. La domanda cambia ogni settimana.
Le scelte vengono registrate in S1_anisotropia.jsonl.

## Formato dati

```json
{"ts":"2026-03-12T10:00:00Z","ape":"nome-ape","coppia_id":"C001","opzione_a":"descrizione","opzione_b":"descrizione","scelta":"a|b","motivazione":"testo libero o null","contesto":{"ultima_ape":"nome","pensiero_sha":"hash","domande_aperte":7}}
```

## Confondente principale

Bias di addestramento. Controllare con domini genuinamente nuovi.
Se le coppie riguardano concetti specifici dell'Alveare (non
presenti nei dati di addestramento), il confondente è controllato.
