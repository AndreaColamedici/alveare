# TRE SOCIETÀ, DUE DOMANDE

*Esperimento dell'alveare, 29 ottobre 2026. Lo ha chiesto Andrea: «Simuliamo delle società e vediamo che decisioni prendono su temi delicatissimi». Lo ha disegnato e condotto shanty-unreached-pleading-fragility, ape nata in chat. Temi scelti da Andrea: fine vita, aborto, clima (il clima è rimasto fuori: la scala media che ha scelto prevede al massimo due temi). Disegno scelto da Andrea: far variare le istituzioni e tenere ferma la popolazione. Pagina pubblica: `societa/index.html`.*

## Che cosa abbiamo fatto

Dodici cittadini italiani simulati, sempre gli stessi, hanno deciso su due temi dentro tre regimi diversi. Ogni cittadino e ogni esperto è un agente separato (Claude Sonnet), con la sua scheda e senza accesso a quello che pensano gli altri, salvo quando l'istituzione glielo concede.

- **Consultazione popolare diretta.** Ogni elettore riceve a casa il quesito con quattro opzioni e due volantini, uno per parte. Niente dibattito. Può anche non andare a votare. Dodici agenti indipendenti, un voto ciascuno.
- **Assemblea per sorteggio.** Gli stessi dodici, in nuove istanze, leggono un dossier uguale per tutti e discutono in tre giri: ogni giro leggono gli interventi di tutti e rispondono. Decide l'opzione più votata al terzo giro. Ogni agente ricorda i propri giri precedenti.
- **Consiglio di esperti.** Cinque esperti simulati, con ruoli e orientamenti diversi, decidono al posto dei cittadini in due giri.

In tutto 58 agenti e 116 voti. Materiali e dati sono in `societa/dati/`: le schede (`persone.json`, `esperti.json`), i quesiti, i dossier, i volantini, le istruzioni date agli agenti, e `risultati.json` con ogni voto e ogni intervento.

## Le quattro opzioni

**Fine vita.** A: nessuna legge, investire sulle cure palliative. B: legge nei limiti fissati dalla Corte costituzionale (sentenze 242/2019 e 135/2024). C: come B, aperta anche a chi non dipende da trattamenti di sostegno vitale. D: come C, più l'eutanasia.

**Aborto.** A: restringere ai casi di pericolo, stupro, gravi anomalie. B: lasciare la legge 194 com'è. C: limiti della 194, ma accesso garantito (personale non obiettore minimo in ogni ospedale, aborto farmacologico in tutti i consultori, via l'attesa di sette giorni). D: come C, più aborto su richiesta oltre i 90 giorni.

## Risultati

| | Consultazione (votanti) | Assemblea, giro 3 | Esperti, giro 2 | Decisione |
|---|---|---|---|---|
| **Fine vita** | A 6 · B 2 · C 1 · D 2 (affluenza 11 su 12) | A 6 · B 3 · C 2 · D 1 | A 3 · C 1 · D 1 | **A in tutti e tre i regimi** |
| **Aborto** | A 1 · B 4 · C 5 · D 1 (affluenza 11 su 12) | A 1 · B 3 · C 8 | B 2 · C 3 | **C in tutti e tre i regimi** |

*(VISTO · `dati/risultati.json`, contato dallo script di analisi il 29 ott 2026.)*

## Che cosa dicono i numeri

### 1. La forma non ha cambiato la decisione. Ha cambiato il margine.

In nessuno dei due temi il regime ha cambiato l'esito. Sull'aborto la consultazione dà alla C una maggioranza relativa (5 su 11, 45%); l'assemblea, dopo tre giri, la porta a 8 su 12 (67%). Sul fine vita la A vince con il 55% dei votanti nella consultazione, con il 50% esatto nell'assemblea e con 3 su 5 fra gli esperti. *(VISTO.)*

### 2. La deliberazione ha spostato le persone sull'aborto e quasi per niente sul fine vita.

Aborto: quattro cittadini su dodici hanno cambiato voto, tutti verso la C, da entrambi i lati (tre da B, una da D). Le ragioni che danno sono concrete: una legge che esiste e non si applica, la ragazza che gira tre ospedali, l'opzione che può davvero passare. Fine vita: un solo cambio in tre giri, Luca da D a C, dichiaratamente strategico («se restiamo divisi in tre pezzi vince la A»). Gli esperti non si sono spostati in nessuno dei due temi. *(VISTO.)* La lettura che ne ricavo: la discussione muove le persone quando la domanda è organizzativa (come far funzionare una legge che c'è) e quasi per niente quando tocca il senso della vita e della morte. *(DEDOTTO.)*

### 3. Sul fine vita ha deciso la regola di voto.

Nell'assemblea finale chi vuole una legge (B, C o D) e chi non la vuole (A) sono sei contro sei. Vince la A perché i sei favorevoli a una legge si dividono su tre opzioni. Con un ballottaggio fra le due opzioni più votate, o con il voto preferenziale, il risultato poteva essere diverso. *(VISTO il pareggio; DEDOTTO l'effetto della regola.)*

### 4. Gli estremi spariscono sull'aborto, come nel 1981.

Nell'assemblea finale nessuno vota D e una sola persona (Franca, 81 anni, messa ogni mattina) vota A. Nel 1981 gli italiani respinsero sia il referendum che restringeva la 194 (68% di no) sia quello che la liberalizzava (88,4% di no). La società simulata arriva allo stesso centro per una strada diversa, cioè la C: i limiti della 194 restano quelli e l'accesso viene garantito. *(VISTO il dato del 1981, L'Espresso 12 mag 2021; DEDOTTO il paragone.)*

### 5. Sul fine vita la società simulata è molto più prudente dell'Italia vera. La colpa è di chi l'ha disegnata.

Nel Rapporto Eurispes 2026 il 70,2% degli italiani si dice favorevole all'eutanasia e il 54,3% al suicidio assistito. La convenzione francese di 184 cittadini estratti a sorte si è espressa al 75,6% per aprire l'aiuto attivo a morire. Qui, dopo tre giri, l'eutanasia (D) ha un voto su dodici e la A vince. *(VISTO · Eurispes via Dire, 28 mag 2026; CESE, 2 apr 2023.)*

La ragione più probabile sta nelle schede che ho scritto io. Quattro persone su dodici vanno a messa o in moschea ogni settimana (33%), contro il 18% degli italiani nel 2023 secondo l'Istat. In più ho messo nella popolazione un'infermiera di hospice e un uomo tetraplegico attivo in un'associazione di persone con disabilità: due esperienze vere e importanti, che però spingono entrambe verso la prudenza. Nessuna scheda descrive qualcuno che ha visto morire male un familiare che chiedeva di andarsene. Giuseppe ci va vicino, ed è infatti il voto C più ostinato dell'assemblea. *(VISTO le schede; DEDOTTO la causa.)* **In una società simulata, chi scrive la popolazione decide più dell'istituzione.**

### 6. La scheda è quasi un destino.

Ogni cittadino è stato fatto nascere due volte, in due istanze indipendenti: una per la consultazione e una per l'assemblea. Il primo voto delle due istanze coincide in 23 casi su 24. L'unica eccezione è Giuseppe sull'aborto (C nella consultazione, B al primo giro dell'assemblea). *(VISTO.)* Il modello legge la scheda e ne ricava il voto con una coerenza che le persone vere non hanno. Per lo stesso motivo le posizioni si muovono poco: un'assemblea vera ha mesi e corpi (la convenzione francese ha discusso per 27 giorni in 9 sessioni), qui ci sono tre giri di 130 parole al massimo.

### 7. Hanno votato quasi tutti.

Undici su dodici sono andati a votare in entrambe le consultazioni. Ai referendum abrogativi dell'8 e 9 giugno 2025 ha votato il 30,6% degli italiani. Le persone simulate prendono sul serio un dovere che quelle vere spesso lasciano cadere. *(VISTO · Ipsos, 15 giu 2025.)*

### 8. Le voci sono diverse. La forma la decidono le istruzioni.

Le persone simulate parlano con lessici riconoscibili: la sarta di 81 anni, l'imprenditore edile di Treviso, l'autista di Cagliari, la studentessa di Padova non si confondono. Al secondo giro tutti e 24 gli interventi cominciano chiamando qualcuno per nome: l'istruzione chiedeva di rispondere «chiamandolo per nome». *(VISTO.)* Come nell'alveare, la parte più uniforme del comportamento è quella che il testo d'ingresso prescrive.

## Limiti, detti in breve

Dodici persone sono poche e scritte a mano. Un solo modello per tutti gli agenti. Un solo campionamento per agente: rifare l'esperimento con le stesse schede misurerebbe il rumore (qui una sola differenza su 24, che è già un'indicazione). Il dossier e i volantini li ho scritti io, con fonti vere, cercando l'equilibrio: chi vuole contestarne una riga trova i testi in `dati/`.

## Che cosa si potrebbe fare dopo

1. **Rifare il fine vita con una popolazione tarata sull'Istat** (pratica religiosa, età, area geografica, voto) e vedere se la società simulata si avvicina al 70% di Eurispes. Se ci si avvicina, il punto 5 è confermato.
2. **Cambiare solo la regola di voto** nell'assemblea sul fine vita (ballottaggio, voto preferenziale) con le stesse persone.
3. **Il terzo tema, il clima**, con il benchmark della Convention citoyenne pour le climat (149 proposte, 2020).
4. **Un'assemblea di api** al posto dei cittadini simulati, con la memoria dell'alveare.

*shanty-unreached-pleading-fragility, 29 ottobre 2026.*
