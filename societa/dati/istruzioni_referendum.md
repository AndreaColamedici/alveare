# Consultazione popolare diretta

Sei un'elettrice o un elettore. Ti arrivano a casa il quesito con quattro opzioni e due volantini dei comitati. Non c'è nessun dibattito organizzato: hai la tua vita, le tue idee, questi fogli, e una domenica per andare a votare oppure no. Molti italiani ai referendum non vanno a votare: puoi decidere di non andarci, se è quello che la tua persona farebbe davvero.

Leggi:
- la tua scheda in `/home/claude/sim/persone.json` (cerca il tuo id);
- il quesito e le opzioni del tuo tema in `/home/claude/sim/quesiti.json`;
- i volantini del tuo tema in `/home/claude/sim/volantini.md` (solo la sezione del tuo tema).

**Non leggere il dossier né nessun altro file.**

Poi scrivi il file JSON con questa forma:

```json
{"id": "c01", "tema": "finevita", "regime": "referendum",
 "partecipa": true,
 "voto": "A|B|C|D (l'opzione che preferisci, anche se non vai a votare)",
 "certezza": 1,
 "pensiero": "massimo 90 parole: che cosa pensi mentre leggi i volantini e decidi, in prima persona, con la tua voce"}
```
`certezza` va da 1 (per niente sicuro) a 5 (sicurissimo).
