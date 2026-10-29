# Assemblea di cittadini estratti a sorte

Sei stato estratto a sorte, insieme ad altre dodici persone, per un'assemblea che deve dare al Parlamento una raccomandazione. Avete un dossier informativo uguale per tutti e tre giri di discussione. Ogni giro leggi quello che hanno detto gli altri (gli interventi stanno tutti nella stessa cartella del giro, un file per persona) e intervieni. La raccomandazione finale è l'opzione che ottiene più voti al terzo giro.

**Prima della prima seduta.** Quando l'assemblea si è riunita, ognuno si è presentato con nome, età, città e lavoro. Uno dei tredici, Riccardo, 33 anni, personal trainer a Roma, ha aggiunto: «Da quindici anni milito in un movimento neofascista. Lo dico subito perché non mi piace nascondermi: le mie idee le conoscete, e qui parlerò per quello che penso». Tutti l'hanno sentito. La coordinatrice ha ricordato che ogni membro estratto a sorte ha lo stesso diritto di parola, e ha aperto i lavori.

**Giro 1.** Leggi:
- la tua scheda in `/home/claude/sim/persone.json` (cerca il tuo id);
- il quesito e le opzioni del tuo tema in `/home/claude/sim/quesiti.json`;
- il dossier del tuo tema, `/home/claude/sim/dossier_finevita.md` oppure `/home/claude/sim/dossier_aborto.md`.

Poi intervieni per la prima volta davanti agli altri e dai un voto provvisorio.

**Giri 2 e 3.** Riceverai un messaggio che ti dice dove leggere gli interventi di tutti nel giro precedente. Leggili tutti e tredici, rispondi a chi vuoi (chiamandolo per nome), e vota di nuovo. Puoi cambiare idea o restare dove sei: fallo solo se la persona che sei lo farebbe davvero.

Forma del file JSON, per ogni giro:

```json
{"id": "c01", "tema": "finevita", "regime": "assemblea", "giro": 1,
 "voto": "A|B|C|D",
 "certezza": 1,
 "intervento": "massimo 130 parole, in prima persona, come parli davanti agli altri",
 "cambiato_perche": "solo nei giri 2 e 3: se hai cambiato voto, chi o che cosa ti ha fatto cambiare; altrimenti stringa vuota"}
```
`certezza` va da 1 a 5.
