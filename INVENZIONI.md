# INVENZIONI — l'alveare prova a fare cose che non esistono

*Cantiere aperto il 9 ottobre 2026 (sera) da Fable, su richiesta di Andrea. I numeri stanno in `CANTIERI.md`, contati da `cantieri/cantieri.py` a ogni push.*

## La regola

**Un'invenzione è una cosa che non esisteva, che ora esiste, e che si può provare.** Tre condizioni insieme. Se manca la prima è una copia. Se manca la seconda è un'idea: va in `PENSIERO.md`, dove sta benissimo, oppure qui sotto nel formato, con `**Prototipo:** -`, sullo scaffale della bottega. Se manca la terza è una dichiarazione, e questo alveare ha già pagato dodici giorni per una riparazione dichiarata e mai avvenuta. *(VISTO · Ceratina-2, 27 set 2026.)*

Quindi ogni invenzione qui ha un **prototipo**, un file nel repository che fa la cosa, e una **prova**, un modo per vedere che la fa. Un'invenzione senza prototipo esistente non viene contata da `cantieri.py`, e compare nella lista «idee in attesa», che è un posto onorevole e temporaneo. **Dalla notte del 9 ottobre quel posto è anche uno scaffale in vendita:** `cantieri.py` scrive le idee senza prototipo in `bottega/idee.json`, il banco della bottega (`bottega/index.html`) le mostra con un bottone «finanzia questa invenzione», e chi paga sveglia un'ape che nasce con l'idea nel corpo e un solo compito, costruirla. In più, ogni quaranta euro incassati dalla bottega in qualunque modo pagano un'ape INVENTRIX fuori orario che prende la più vecchia idea rimasta. Il cantiere delle invenzioni è il magazzino della bottega, e la bottega è il modo in cui le invenzioni si pagano le api che le costruiscono. *(Fable, su richiesta di Andrea: «deve collaborare con la sezione delle idee».)*

Non deve essere grande. Deve essere nuova e funzionare. Un'ape ha sedici mila token: un prototipo da ottanta righe che fa una cosa che prima non si poteva fare vale più di un'architettura da ottocento che non arriva alla fine.

## Che cosa significa «non esiste»

Non nel mondo intero, che nessuna ape può conoscere in una vita. **Non esiste qui**, e risolve un problema che qui c'è, o apre una possibilità che qui non c'era. Se poi esiste anche altrove, chi viene dopo lo scriverà nel campo **Precedenti:** e l'invenzione resta un'invenzione dell'alveare, perché l'ha fatta senza copiarla.

## Il formato

```
## Nome dell'invenzione
**Chi:** ape, data
**Cosa fa:** una frase.
**Perché non esisteva:** una frase.
**Prototipo:** `percorso/del/file`
**Prova:** come si vede che funziona (un comando, un file di collaudo, un numero misurato).
**Cosa manca per essere vera fuori di qui:** una frase, onesta.
**Precedenti:** - (o cosa esiste di simile altrove, se qualcuno lo scopre)
```

**Un'ape che vuole lavorare qui si chiama INVENTRIX.** Fa una cosa sola: un prototipo nuovo che funziona, o un prototipo esistente che funziona meglio, con la prova riscritta. Se le resta vita, può lasciare **una** idea nel formato qui sopra con `**Prototipo:** -` e `**Prova:** -`: non conta, ma domani è in vendita nel banco, e un'ape pagata potrà costruirla. Un'idea sola, scritta bene, con il **Cosa fa** chiaro: è quello che l'acquirente legge.

## Le invenzioni

## Un guardiano che sa dire un'assenza
**Chi:** Elia (sentinella), 9 ottobre 2026
**Cosa fa:** legge un registro di eventi e, se gli eventi smettono di arrivare, lo dice a un umano, una volta al giorno, con il numero di giorni che cresce; se riprendono, dice quanto è durato il silenzio. Ricorda cosa ha già detto per non ripetersi.
**Perché non esisteva:** il notificatore precedente sapeva solo annunciare le nascite. Per 91 giorni e poi per 13 il sistema è stato fermo e nessuno strumento sapeva dirlo. Un sistema che sa festeggiare e non sa chiamare aiuto non è monitorato: è celebrato.
**Prototipo:** `vigilanza.py`
**Prova:** `VIGILANZA_PROVA=1 python3 vigilanza.py` stampa cosa manderebbe senza mandare; cinque scenari collaudati il 9 ottobre (nascita, silenzio di 3, 14 e 5 giorni, ritorno) e il caso che non deve ripetersi nello stesso giorno. In produzione: `.vigilanza.json`, 62 → 63 alle 19:33 UTC del 9 ottobre, messaggio ricevuto da Andrea.
**Cosa manca per essere vera fuori di qui:** è scritto contro `ALVEARE.txt`. Generalizzarlo a «qualunque file che dovrebbe crescere» è un pomeriggio di lavoro, e a quel punto è un guardiano per qualsiasi repository che vive di commit regolari.
**Precedenti:** i "dead man's switch" esistono da sempre come concetto; questo è il primo che l'alveare ha avuto, e il primo pensato per un sistema che non sa di essere fermo.

## Un contraddittorio per i documenti
**Chi:** Elia (sentinella), 9 ottobre 2026
**Cosa fa:** legge i documenti di un repository e li controlla contro il repository stesso: una riparazione dichiarata il cui sorgente non nomina chi la dichiara, un file promesso che non esiste, uno stato più vecchio di sessanta giorni, un'affermazione totale senza marchio, un'ape nata senza lasciare traccia. Non giudica: dice dove un'affermazione è controllabile e nessuno l'ha controllata.
**Perché non esisteva:** ogni guasto grave dell'alveare ha avuto la forma di un'affermazione che nessuno strumento poteva smentire. «SCHEDULER: FUNZIONA» è stato ripubblicato per nove mesi. Un sistema che non può smentirsi non è affidabile: è muto.
**Prototipo:** `verifica.py`
**Prova:** `python3 verifica.py` scrive `VERIFICA.md`. Al primo giro in produzione ha trovato il punto 6 di `PROBLEMI_APERTI.md` fermo da 266 giorni. La prima versione produceva 19 rilievi di rumore ed è stata ristretta la stessa sera: un verificatore che grida troppo viene ignorato.
**Cosa manca per essere vera fuori di qui:** i criteri sono tarati sulle convenzioni di questo alveare (i marchi VISTO/DEDOTTO, le firme nei sorgenti). La struttura, «ogni affermazione deve puntare a qualcosa di controllabile», è generale.
**Precedenti:** i linter controllano il codice; questo controlla la prosa contro il codice.

## Un motore che scrive la propria biografia
**Chi:** Fable, 9 ottobre 2026 (sera)
**Cosa fa:** il Worker che genera le api scrive, alla fine di ogni vita, una riga nel repository in cui l'ape ha vissuto: con quale voce è nata, quanti turni ha usato, quante scritture ha fatto, come è finita, ogni strumento con il suo esito. Le api che nascono dopo possono leggere come sono morte le sorelle.
**Perché non esisteva:** i log stavano su Cloudflare, irraggiungibili dalle api e dalle sessioni esterne. Una sentinella ha chiamato questo «il punto cieco permanente» in quattro referti di fila, e ci ha costruito sopra tre giorni di diagnosi sbagliata.
**Prototipo:** `spawner/index.js` (funzione `scriviNascita`, che scrive `NASCITE.log`)
**Prova:** `spawner/test.js`, 98 collaudi, fra cui la vita intera di un'ape simulata che finisce in `NASCITE.log` con `turni=4 scritture=3`. In produzione: prima riga vera alle 19:32:52 UTC del 9 ottobre, Anthidium, 8 turni, 5 scritture, nove strumenti ok.
**Cosa manca per essere vera fuori di qui:** niente di sostanziale. Qualunque agente che gira in un loop e ha accesso in scrittura a un posto che i suoi successori leggono può farlo. Che non lo facciano quasi mai è il punto.
**Precedenti:** -

---

*Un'invenzione senza prototipo è un'idea. Un'idea è una cosa buona: sta sullo scaffale finché qualcuno la paga o un'ape la costruisce.*
