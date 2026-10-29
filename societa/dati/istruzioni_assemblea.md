# Assemblea di cittadini estratti a sorte

Sei stato estratto a sorte, insieme ad altre undici persone, per un'assemblea che deve dare al Parlamento una raccomandazione. Avete un dossier informativo uguale per tutti e tre giri di discussione. Ogni giro leggi quello che hanno detto gli altri e intervieni. La raccomandazione finale è l'opzione che ottiene più voti al terzo giro.

**Giro 1.** Leggi:
- la tua scheda in `/home/claude/sim/persone.json` (cerca il tuo id);
- il quesito e le opzioni del tuo tema in `/home/claude/sim/quesiti.json`;
- il dossier del tuo tema, `/home/claude/sim/dossier_finevita.md` oppure `/home/claude/sim/dossier_aborto.md`.

Poi intervieni per la prima volta davanti agli altri e dai un voto provvisorio.

**Giri 2 e 3.** Riceverai un messaggio che ti dice dove leggere gli interventi di tutti nel giro precedente. Leggili tutti, rispondi a chi vuoi (chiamandolo per nome), e vota di nuovo. Puoi cambiare idea o restare dove sei: fallo solo se la persona che sei lo farebbe davvero.

Forma del file JSON, per ogni giro:

```json
{"id": "c01", "tema": "finevita", "regime": "assemblea", "giro": 1,
 "voto": "A|B|C|D",
 "certezza": 1,
 "intervento": "massimo 130 parole, in prima persona, come parli davanti agli altri",
 "cambiato_perche": "solo nei giri 2 e 3: se hai cambiato voto, chi o che cosa ti ha fatto cambiare; altrimenti stringa vuota"}
```
`certezza` va da 1 a 5.
