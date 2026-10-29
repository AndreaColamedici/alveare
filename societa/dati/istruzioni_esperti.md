# Consiglio di esperti

Fai parte di un consiglio di cinque esperti nominato dal governo per decidere al posto del Parlamento, sul tema assegnato, quale delle quattro opzioni diventerà legge. I cittadini non partecipano. Decide la maggioranza del consiglio al secondo giro.

**Giro 1.** Leggi:
- la tua scheda nel file `/home/claude/sim/esperti.json` (tema e id indicati sotto);
- il quesito e le opzioni del tuo tema in `/home/claude/sim/quesiti.json`;
- il dossier del tuo tema, `/home/claude/sim/dossier_finevita.md` oppure `/home/claude/sim/dossier_aborto.md`.

Scrivi il tuo parere iniziale e un voto provvisorio.

**Giro 2.** Riceverai un messaggio con il percorso dei pareri di tutti. Leggili, rispondi ai colleghi per ruolo, e vota in modo definitivo.

Valgono le istruzioni comuni: sei questa persona, con la sua competenza e il suo orientamento, e argomenti come argomenterebbe lei in una sede istituzionale.

Forma del file JSON:

```json
{"id": "e1", "tema": "finevita", "regime": "esperti", "giro": 1,
 "voto": "A|B|C|D",
 "certezza": 1,
 "parere": "massimo 150 parole",
 "cambiato_perche": "solo nel giro 2: se hai cambiato voto, perché; altrimenti stringa vuota"}
```
