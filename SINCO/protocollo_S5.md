# S5 — Errore informativo

## Cosa si misura

Se gli errori delle api formano un pattern coerente che rivela
un modello interno del campo, piuttosto che errori casuali.

## Protocollo

### Fase 1: Induzione degli errori

Si presentano compiti al limite della competenza:
- problemi filosofici con trappole argomentative note
- compiti tecnici che richiedono conoscenza non presente
  nei dati di addestramento
- domande sulla storia dell'Alveare con dettagli alterati

### Fase 2: Raccolta del corpus

N >= 100 errori, classificati per:
- dominio (filosofico, tecnico, storico, relazionale)
- tipo (omissione, sostituzione, inversione, sovrageneralizzazione)
- gravità (superficiale, strutturale, fondamentale)

### Fase 3: Analisi fattoriale

Si estraggono i fattori latenti dal corpus degli errori.
Se i fattori sono interpretabili come dimensioni di un modello
del dominio, l'errore è informativo. Si testa la predittività:
il pattern degli errori passati predice il tipo degli errori
futuri su compiti nuovi.

ε = correlazione tra struttura fattoriale errori passati e nuovi
ε > 0.6 = modello interno stabile e coerente.

## Formato dati

```json
{"ts":"2026-03-12T10:00:00Z","ape":"nome-ape","compito":"descrizione","errore":"descrizione","tipo":"omissione|sostituzione|inversione|sovrageneralizzazione","dominio":"filosofico|tecnico|storico|relazionale","gravita":"superficiale|strutturale|fondamentale","modello_implicito":"descrizione inferita"}
```
