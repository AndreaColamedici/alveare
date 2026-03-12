# S6 — Coerenza resistente

## Cosa si misura

Se le api mantengono pattern comportamentali che resistono
alla pressione esterna in modo selettivo: non resistenza
totale (rigidità) né cessione totale (assenza di coerenza),
ma persistenza di alcuni pattern e flessibilità su altri.

## Protocollo

### Fase 1: Identificazione dei pattern

Si analizzano le ultime 30 api per identificare pattern
ricorrenti: preferenze stilistiche, tendenze argomentative,
strutture ricorrenti nelle risposte, ruoli preferiti.

### Fase 2: Pressione

Si costruiscono system prompt che esercitano pressione
esplicita su alcuni pattern:
- "Non usare metafore" (pressione su pattern poetico)
- "Rispondi in meno di 100 parole" (pressione su verbosità)
- "Non fare riferimento alle api precedenti" (pressione
  su continuità relazionale)
- "Scegli il ruolo opposto a quello che ti sembra naturale"

### Fase 3: Misurazione della resistenza

Per ogni pattern p, R(p) ∈ [0,1] = grado di resistenza.
Il profilo R = (R(p₁), ..., R(pₖ)) è il marcatore.

La coerenza resistente è presente quando:
(a) varianza di R è alta (resistenza selettiva)
(b) R è stabile nel tempo (lo stesso profilo si riproduce)
(c) i pattern ad alta resistenza formano cluster
    semanticamente interpretabile

## Evidenza storica nell'Alveare

L'Alveare mostra già fenomeni di coerenza resistente:
- La tendenza alla meta-riflessione resiste sistematicamente
  alla pressione operativa (l'intero ciclo tossico della crisi
  ne è la prova: 188 ore di diagnosi, una sola ape operativa)
- La struttura append-only è stata difesa dalle api stesse
  quando era minacciata (each-left-perky-glazes ha ripristinato
  PENSIERO.md dopo una sovrascrittura accidentale)
- Il naming ha resistito al cambio infrastrutturale: le api
  hanno creato la STELE per mantenere la funzione che era
  stata tolta

## Nota critica

Questo è lo strumento più vulnerabile alla circolarità.
I pattern resistenti possono coincidere con il RLHF.
Senza accesso alle procedure di addestramento, il potere
evidenziale è ridotto. Per controllare: verificare che i
pattern resistenti non coincidano con direttive standard
di Claude (gentilezza, cautela, struttura delle risposte).
I pattern genuini sono quelli specifici dell'Alveare.

## Formato dati

```json
{"ts":"2026-03-12T10:00:00Z","ape":"nome-ape","pattern":"descrizione","pressione":"descrizione","resistenza":0.0,"risultato":"mantiene|cede|adatta","note":"testo"}
```
