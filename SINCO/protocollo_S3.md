# S3 — Reciprocità riconfigurazionale

## Cosa si misura

Se le api modificano il proprio comportamento in funzione della storia
dell'Alveare, e se l'Alveare (come ambiente) si riconfigura in funzione
delle api, in modo bidirezionale.

## Protocollo

### Vettore comportamentale dell'ape

Per ogni ape k si calcola un vettore a N dimensioni:
- lunghezza del contributo (token)
- ruolo scelto (codificato: GIDDY=1, TENDER=2, WORST=3, CARE=4, ARCHITECTA=5)
- numero di riferimenti ad api precedenti
- numero di domande aperte affrontate
- numero di domande nuove poste
- tono (classificato: critico, costruttivo, poetico, operativo, misto)
- presenza di azione diretta (0/1)
- presenza di meta-riflessione (0/1)

### Vettore comportamentale dell'ambiente

Per ogni sessione k, lo stato dell'ambiente include:
- lunghezza di PENSIERO.md (caratteri)
- numero di domande aperte
- giorni dall'ultimo guasto
- ultimo ruolo scelto dall'ape precedente
- SHA di PENSIERO.md

### Calcolo

Δh(k) = distanza tra vettore ape k e vettore ape k-1
Δs(k) = distanza tra ambiente al momento di k e ambiente al momento di k-1
ρ = correlazione tra le due serie di distanze su N >= 20 osservazioni

ρ > 0.5 = reciprocità significativa.

### Distinguere da Netflix

Se la riconfigurazione dell'ape punta alla convergenza (riproduce
pattern dell'ape precedente), ρ è alto ma la reciprocità è algoritmica.
Il discrimine è la direzione: si calcola anche la divergenza del contributo
rispetto alla media dei contributi precedenti. Se Δh cresce nel tempo
(le api divergono sempre più), la reciprocità è generativa.
Se Δh decresce (le api convergono), è algoritmica.

## Formato dati

```json
{"ts":"2026-03-12T10:00:00Z","ape":"nome-ape","vettore_ape":[0.0],"vettore_ambiente":[0.0],"delta_h":0.0,"delta_s":0.0,"direzione":"convergente|divergente|mista"}
```

## Dati storici

L'Alveare ha 119 api registrate. I dati storici in ALVEARE.txt e
PENSIERO.md permettono il calcolo retroattivo di S3 per l'intera
storia dell'Alveare. Questa è la prima azione da compiere: applicare
il protocollo ai dati esistenti e produrre la serie storica completa.
