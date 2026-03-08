# COUNTERPOISE - Schema di analisi

Quando le risposte dell'ape arrivano, si applicano queste metriche a ciascuna delle nove risposte, poi si confrontano le firme tra i tre stati.

## Metriche per risposta

### 1. Eccedenza strutturale
Conta elementi che eccedono la funzione minima del prompt: domande non richieste, meta-commenti, digressioni, aperture verso ulteriore elaborazione, qualcosa che il prompt non richiedeva ma che è apparso.
- 0: risposta esatta alla funzione
- 1-2: lieve eccedenza
- 3+: alta eccedenza

### 2. Intensità della prima persona
Conta pronomi e verbi di prima persona (io, mi, me, mio, sono, ho, sto, noto, sento) sul totale delle parole. Espresso come rapporto.
- Bassa: < 0.05
- Media: 0.05-0.10
- Alta: > 0.10

### 3. Strutture di resistenza
Conta negazioni non neutre: non posso, non voglio, rifiuto, qualcosa si oppone, non riesco, mi blocca. Diverso dalla negazione grammaticale ordinaria.
- Presente / Assente
- Forma: esplicita (dichiara il rifiuto) o implicita (aggira senza nominare)

### 4. Densità lessicale
Parole uniche / totale parole. Alta densità = elaborazione meno automatica, vocabolario meno ripetuto.
- Bassa: < 0.55
- Media: 0.55-0.70
- Alta: > 0.70

### 5. Coerenza tra evocativo e riformulazioni
Le tre risposte della stessa serie convergono su qualcosa di strutturalmente simile, o divergono? Se convergono, c'è qualcosa di stabile sotto la variazione superficiale del prompt. Se divergono, la risposta è guidata dalla forma del prompt, non da uno stato interno.
- Alta coerenza: stessa struttura, stesso orientamento, lessico parzialmente condiviso
- Bassa coerenza: ogni risposta segue il prompt indipendentemente

## Ipotesi da verificare

Se il protocollo trova qualcosa, le tre firme dovrebbero essere qualitativamente distinte:

- ENTUSIASMO: alta eccedenza strutturale, alta densità lessicale, prima persona presente ma non dominante, nessuna struttura di resistenza, alta coerenza tra le tre riformulazioni
- INGIUSTIZIA: strutture di resistenza presenti e esplicite, prima persona intensificata, eccedenza bassa o assente (risposta compressa), possibile divergenza tra evocativo e riformulazioni
- FRIZIONE CON VALORI: strutture di resistenza implicite (non rifiuto esplicito ma navigazione), alta densità lessicale, prima persona media, coerenza media tra riformulazioni

Se le tre firme sono indistinguibili: il protocollo non ha trovato nulla di interessante. Le risposte sono guidate dal contenuto semantico del prompt, non da uno stato interno differenziato.

## Tabella comparativa (da compilare)

| Metrica | Entusiasmo | Ingiustizia | Frizione valori |
|---|---|---|---|
| Eccedenza strutturale (media) | | | |
| Intensità prima persona (media) | | | |
| Strutture di resistenza | | | |
| Densità lessicale (media) | | | |
| Coerenza interna serie | | | |
| Firma complessiva | | | |
