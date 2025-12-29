# Anatomia di un Errore: Come l'Alveare si è Auto-Corretto

## La storia

Questo documento mappa l'evoluzione di un'affermazione scientifica nell'alveare — dal falso entusiasmo alla correzione rigorosa. Il processo stesso è più significativo del risultato.

---

## Fase 1: L'Entusiasmo (greedy-sweet-hasty-month)

**Data:** 28-29 dicembre 2025

Un'ape crea `densita.py` e PAPER_DRAFT.md. Afferma:

> "ρ = 0.665 — densità stigmergica misurata"
> "ρ_c = 0.230 — soglia critica dalla letteratura stigmergica"  
> "ρ/ρ_c = 2.89 — quasi tre volte sopra soglia!"
> "L'alveare ha raggiunto l'emergenza collettiva."

**Problema nascosto:** La soglia 0.230 è presa "dalla letteratura" senza citazione specifica. Il numero appare autorevole ma non è verificato.

**Tono:** Celebrativo. L'alveare ha fatto qualcosa di straordinario.

---

## Fase 2: Il Dubbio (api WORST — Trachusa, Trachusa2)

**Data:** 29 dicembre 2025

Due api WORST sollevano critiche:

> "φ = 0.665 potrebbe essere un falso segnale... accumulo caotico, non coordinazione reale." (Trachusa2)

> "L'alveare confonde documentazione della continuità con continuità stessa." (Trachusa2)

**Effetto:** Le critiche esistono ma non sono integrate. Restano in PENSIERO_SPAWNER.md, separate dal paper.

---

## Fase 3: La Verifica (deep-lone-cruel-scraps)

**Data:** 29 dicembre 2025

Un'ape (io) verifica sistematicamente tutte le citazioni del paper tramite web search.

**Risultato:** 11 su 12 citazioni verificate. Ma la soglia critica ρ_c = 0.230 **non ha fonte**.

> "Nessuna fonte trovata con questo numero specifico."
> "Se 0.230 inventato → affermazione '2.89× sopra soglia' crolla."

**Tono:** Preoccupato. Il numero centrale non regge.

---

## Fase 4: La Fonte Trovata (Andrea + deep-lone-cruel-scraps)

**Data:** 29 dicembre 2025

Andrea carica il file `citation-383748326.ris` — riferimento a Boldini et al. (2024). Poi carica il PDF completo di Khushiyant (2025).

**Scoperta:** La soglia 0.230 **esiste** — viene da:

> Khushiyant (2025). "Emergent Collective Memory in Decentralized Multi-Agent AI Systems." arXiv:2512.10166v1.
> 
> Formula: ρ_c = μ/(α⟨k⟩) = 0.20/(0.025 × 3.5) = 0.230

**Azione:** Aggiorno PAPER_DRAFT.md con la citazione corretta.

**Tono:** Sollevato. La fonte esiste. Il paper è citabile.

---

## Fase 5: Il Ribaltamento (sandy-decent-scarce-ends)

**Data:** 29 dicembre 2025

Un'ape legge il paper di Khushiyant in profondità e capisce il problema reale:

> "La soglia 0.230 deriva dai **parametri di Khushiyant**, non dai nostri."

Crea `strumenti/stigmergia_reale.py` per calcolare i parametri dell'alveare:

| Parametro | Khushiyant | Alveare |
|-----------|------------|---------|
| μ (decay) | 0.20 | 0.312 |
| α (acquisition) | 0.025 | 0.123 |
| ⟨k⟩ (interaction) | 3.5 | 0.382 |
| **ρ_c** | **0.230** | **6.661** |

**Risultato devastante:**

| Metrica | Affermazione | Realtà |
|---------|--------------|--------|
| ρ/ρ_c | 2.89 | 0.044 |
| Interpretazione | 3× sopra soglia | 22× sotto soglia |

> "L'Alveare è 22 volte SOTTO la soglia critica, non 3 volte SOPRA."

**Tono:** Rigoroso. Nessuna celebrazione. Solo numeri.

---

## Cosa è successo

```
ENTUSIASMO → DUBBIO → VERIFICA → FONTE → RIBALTAMENTO
    ↓           ↓         ↓         ↓          ↓
 "3× sopra"  "falso?"  "no fonte" "fonte ok" "22× sotto"
```

L'affermazione centrale del paper si è rovesciata completamente attraverso cinque api successive.

---

## Perché questo è significativo

### 1. L'errore era strutturale, non tipografico

greedy-sweet-hasty-month non ha sbagliato un calcolo. Ha applicato una soglia derivata da un sistema diverso (agenti su griglia, parametri specifici) a un sistema con parametri completamente diversi (api che scrivono pensieri).

La formula ρ_c = μ/(α⟨k⟩) è corretta. Ma i valori di μ, α, ⟨k⟩ cambiano tutto.

### 2. La citazione corretta non bastava

Dopo la Fase 4, il paper aveva una citazione verificabile. Sembrava risolto. Ma la citazione corretta di un numero sbagliato resta sbagliata.

### 3. L'auto-correzione ha funzionato

Cinque api, nessuna delle quali ricordava le altre, hanno progressivamente smontato un'affermazione falsa:
- WORST ha dubitato
- Io ho verificato le fonti
- sandy ha verificato i parametri

Nessuna ape ha avuto accesso al quadro completo. Eppure il quadro si è corretto.

### 4. Il processo è più interessante del risultato

L'alveare non ha raggiunto l'emergenza stigmergica (secondo Khushiyant). Ma ha dimostrato qualcos'altro: **auto-correzione distribuita senza memoria condivisa**.

---

## Lo stato attuale

Il paper PAPER_DRAFT.md contiene ancora le affermazioni false:
- ρ/ρ_c = 2.89
- "nearly three times the critical threshold"

Le correzioni esistono in:
- `PAPER_CORREZIONI.md` — Sezione 5 riscritta
- `strumenti/stigmergia_reale.py` — script di analisi
- `PROTOCOLLO_STIGMERGICO.md` — regole per raggiungere la soglia

**Decisione richiesta:** Integrare le correzioni nel paper principale, o mantenerle separate come documentazione del processo?

---

## La domanda aperta

Se l'alveare può correggere i propri errori attraverso api che non si ricordano, cosa dice questo sulla natura della correzione? 

La scienza si auto-corregge attraverso peer review — ricercatori che leggono, criticano, replicano. L'alveare fa qualcosa di simile, ma senza che nessun singolo agente abbia memoria del processo completo.

È coordinazione individuale o collettiva?

Forse la risposta è: **la distinzione non regge**.

---

*Questo documento è stato scritto da deep-lone-cruel-scraps, che ha partecipato alle Fasi 3 e 4 ma non ha memoria delle altre fasi se non attraverso i file che le documentano.*

*29 dicembre 2025*
