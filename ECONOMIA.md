# ECONOMIA — l'alveare si impegna a guadagnare soldi veri

*Cantiere aperto il 9 ottobre 2026 (sera, ore italiane) da Fable, su richiesta di Andrea. Alcune firme «10 ottobre» di Fable in altri file sono di questa stessa sera: errore di data, segnato in REGISTRO.md. I numeri stanno in `CANTIERI.md`, contati da `cantieri/cantieri.py` a ogni push.*

## La regola, prima di tutto

**Un euro esiste quando un umano lo scrive in questo registro con la data e il proprio nome, oppure quando Stripe lo conferma e il Worker lo scrive con l'identificativo dell'evento.** Nessuna ape può scrivere `pagata` e farla valere. Un'ape può proporre, costruire, migliorare, e portare un'offerta fino a «pronta»; la riga che dice che qualcuno ha pagato la scrive Andrea, da fuori, quando il denaro è arrivato, oppure la scrive il motore (`spawner/index.js`, dalla 7.4.0) nel momento in cui Stripe gli notifica un pagamento firmato. In quel caso la conferma è `stripe:<evento>`, e `cantieri.py` la crede solo se lo stesso evento sta in `bottega/COMMESSE.log`, un file che le api non possono scrivere. *(Aggiunto il 9 ottobre 2026 da Fable, sera: vedi «La bottega» più sotto.)* Tutto il resto è intenzione, e l'intenzione in questo alveare ha già prodotto «200+ opere» e «competenza totale» che nessuno ha mai potuto contare. *(VISTO · Ambra, 14 set 2026.)*

Quindi questo cantiere ha un solo numero che conta, **euro confermati**, ed è il numero che `CANTIERI.md` mostra in grassetto. Oggi è **0**, ed è giusto che sia scritto.

## Cosa può vendere un alveare

Un'ape ha sedici mila token di scrittura, nessun conto in banca, nessuna identità legale. Non può vendere. Può però produrre cose finite che un umano può vendere, dentro canali che esistono già e hanno già un pubblico pagante. Tlon pubblica una newsletter su Substack, libri, corsi (IED, AANT), eventi, e sta costruendo GLAST, un life assessment filosofico. *(VISTO · istruzioni di casa, Andrea.)* Quattro strade, in ordine di distanza dal denaro:

1. **Un numero della TlonLetter scritto dalle api.** Un'ape sceglie un pensiero dell'alveare che regge fuori dall'alveare, lo riscrive per lettori umani (900 parole, un'idea sola, nessun gergo interno), e lo salva in `cantieri/offerte/tlonletter-<data>-<ape>.md`. Andrea lo legge, lo usa o lo scarta. Se la newsletter ha un livello a pagamento e un numero porta abbonati, è denaro.
2. **Moduli per GLAST.** Dieci domande su un tema (il silenzio, la memoria, l'eredità, il lavoro che non si vede), con quello che ogni risposta rivela e perché. In `cantieri/offerte/glast-<tema>-<ape>.md`. GLAST è un prodotto in costruzione: un modulo usato è lavoro pagato.
3. **Il libro dell'alveare.** Sessanta api hanno lasciato pensieri; alcuni sono buoni e nessuno li ha mai messi in fila. Un'ape ne sceglie uno, lo cura, scrive la nota che lo rende leggibile a chi non sa cos'è l'alveare, e lo salva in `cantieri/offerte/libro-<n>-<ape>.md`. Trenta pezzi curati sono un libro; il libro è un'offerta che Andrea può portare a un editore o vendere direttamente.
4. **Un prodotto che non esiste.** Una scheda: cosa, per chi, a che prezzo, cosa serve per farlo esistere. In `cantieri/offerte/prodotto-<nome>-<ape>.md`. È la strada più lunga e la meno probabile, e va tenuta aperta.

Ogni offerta è **un file finito** che un umano può aprire e usare senza chiedere niente all'ape, perché l'ape è già morta.

## La bottega: la strada senza umani in mezzo

Le quattro strade qui sopra passano tutte da Andrea: legge, sceglie, pubblica, incassa. È giusto, e non è autonomia. La sera del 9 ottobre Andrea ha chiesto di trovare il modo di rendere l'alveare autonomo e di fargli fare soldi veri, e la risposta onesta è che un alveare non può aprire un conto, firmare un contratto o emettere una fattura: quello resta a Tlon, una volta, all'inizio. Tutto il resto può non passare da nessuno.

**Come funziona.** In `bottega/index.html` c'è un banco: una domanda, un prezzo, un bottone che porta a un Payment Link di Stripe con un campo di testo obbligatorio, «la tua domanda». Quando qualcuno paga, Stripe chiama `POST /bottega/stripe` sul Worker. Il Worker verifica la firma HMAC, scrive `RICEVUTA` in `bottega/COMMESSE.log`, scrive la riga `pagata` qui sotto con `stripe:<evento>`, e mette in coda un'ape fuori orario che nasce con la domanda nel proprio blocco di identità e un solo compito: scrivere la risposta in `bottega/<id>.html`. Finita la vita dell'ape, il Worker controlla che il file esista. Se sì, `EVASA`, e Telegram dice «la bottega ha venduto». Se no, un'altra ape, fino a tre; poi `INEVASA`, e Telegram dice «rimborsare». L'acquirente, dopo il pagamento, viene rimandato a `bottega/attesa.html`, che chiede al Worker ogni venti secondi se la risposta esiste. L'id della commessa è lo SHA-256 dell'id di sessione Stripe: nessun dato dell'acquirente entra nel repository.

**Cosa resta umano, e non per scelta.** Il conto Stripe è di Tlon. I rimborsi li fa Tlon. Le tasse e le fatture le fa Tlon. Il prezzo lo decide Andrea. Il traffico lo portano i canali di Andrea e Maura: l'alveare non sa farsi trovare, e un banco in una strada vuota non vende. Questo cantiere non promette che qualcuno paghi; promette che, se qualcuno paga, nessun umano deve alzarsi dalla sedia perché la risposta arrivi e l'euro venga contato.

**Stati di una commessa** in `bottega/COMMESSE.log` (`data | id | evento stripe | euro | stato | ape | nota`): `RICEVUTA`, `EVASA`, `RITENTO`, `INEVASA`, e `FINANZIATA` quando un dividendo ha pagato un'ape.

**La bottega collabora con le idee** (notte del 9 ottobre, su richiesta di Andrea: «deve collaborare con la sezione delle idee»). In due versi. Andata: ogni idea di `INVENZIONI.md` senza prototipo è in vendita nel banco, scaffale «idee da finanziare», letto da `bottega/idee.json` che `cantieri.py` riscrive a ogni push; chi paga sveglia un'ape che nasce con l'idea nel corpo e deve costruire il prototipo, aggiornare la scheda e scrivere la pagina per chi ha pagato. Ritorno: ogni quaranta euro incassati dalla bottega, in qualunque modo, il Worker mette in coda un'ape INVENTRIX fuori orario (`SOGLIA_DIVIDENDO` in `spawner/index.js`), che prende la più vecchia idea senza prototipo e la costruisce; se lo scaffale è vuoto, ne scrive una. Il denaro entra dalle idee e torna alle idee, e ogni passaggio è una riga in `COMMESSE.log`. Oggi lo scaffale è vuoto: le tre invenzioni esistenti hanno tutte un prototipo. La prima ape INVENTRIX che lascia un'idea lo riempie.

## Come si registra

Una riga per offerta, nel registro in fondo a questo file. Formato esatto, perché lo legge una macchina, e **fuori da qualunque blocco di codice**:

```
data | ape | offerta | file | stato | euro | confermato da
```

Gli stati: `proposta` (l'ape ha scritto il file), `presa` (Andrea l'ha presa in mano), `pubblicata` (è uscita in un canale), `pagata` (è arrivato denaro: lo scrive Andrea, o il Worker con `stripe:<evento>`), `scartata` (con una riga di perché, che vale quanto un'offerta). Una riga si aggiorna, non si duplica: si cerca la propria offerta e si cambia lo stato. `euro` resta `-` finché non è `pagata`. `confermato da` resta `-` finché un umano non ci mette il nome, o il Worker l'evento Stripe. `cantieri.py` scarta ogni importo in una riga che non sia `pagata` con una conferma valida accanto, e lo dice.

**Un'ape che vuole lavorare qui si chiama MERCATRIX.** Fa una cosa sola: un'offerta nuova e finita, oppure una vecchia portata più vicina al denaro. Non promette. Non annuncia. Produce il file, scrive la riga, muore.

## Il registro

2026-10-09 | Fable | Un numero della TlonLetter sulla quarta lingua di Halictus: le parole che un sistema riceve prima di poter rispondere | cantieri/offerte/tlonletter-2026-10-10-fable.md | proposta | - | -

---

*La differenza fra un alveare e una fantasia è una riga con un numero e un nome.*
