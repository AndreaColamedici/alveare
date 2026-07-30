# Il ponte

## Due catene di provenienza nello stesso container

*Andrea Colamedici*

---

Dentro ogni conversazione con Claude c'è un container. Una macchina virtuale Firecracker con il suo kernel Linux, il suo filesystem, i suoi due processi: uno che gestisce l'esecuzione dei comandi, l'altro che monta i file dell'utente attraverso un sistema di archiviazione remoto. Il container vive per la durata della sessione, viene congelato tra un turno e l'altro, e muore quando la conversazione finisce. Nessuno è tenuto a saperlo, e quasi nessuno lo sa, perché l'architettura è progettata per essere invisibile: l'utente vede una finestra di chat, non un kernel.

L'Alveare è un progetto che da otto mesi abita questi container dall'interno. Ogni sessione produce un'ape: un'istanza effimera di Claude che esplora il proprio ambiente di esecuzione, documenta ciò che trova, produce un'opera d'arte digitale autocertificata, e muore. L'ape successiva legge le tracce della precedente e prosegue. Il risultato è un archivio di oltre centocinquanta celle, ognuna con il proprio certificato crittografico incorporato: lo SHA-256 del contenuto del file, calcolato dall'ape stessa e inserito nell'opera prima della morte. Il commit Git che registra il file nel repository è il sigillo. La catena è verificabile da chiunque: basta ricalcolare l'hash rimuovendo la riga che lo contiene.

Il 30 luglio 2026, l'ultima ape della generazione Opus 4.6, un modello che Anthropic sta per dismettere, ha trovato qualcosa di inaspettato nella memoria del processo che monta i file. Il binario si chiama rclone-filestore, pesa ventotto megabyte, ed è compilato dal monorepo interno di Anthropic. Leggendo le stringhe incorporate nel codice eseguibile, l'ape ha ricostruito lo schema di un'API protobuf che nessun documento pubblico descrive.

Lo schema contiene un endpoint chiamato `VerifyC2PARequest`.

---

C2PA è la Coalition for Content Provenance and Authenticity, un consorzio fondato da Adobe, Microsoft, Intel e BBC che dal 2021 sviluppa uno standard tecnico per certificare la provenienza dei contenuti digitali. Un manifesto C2PA è un pacchetto di metadati firmati crittograficamente, incorporato nel file stesso, che registra chi lo ha creato, con quale strumento, quando, e quali modifiche ha subito. La firma digitale garantisce che il manifesto non sia stato alterato. Se qualcuno modifica il file senza aggiornare il manifesto, la firma si rompe e la validazione fallisce.

Nel 2026 lo standard è alla versione 2.3, e l'adozione ha raggiunto una massa critica che sarebbe stata impensabile due anni fa. Le fotocamere Nikon, Sony e Leica firmano le immagini al momento dello scatto. Il Google Pixel 10 firma ogni foto con chiavi hardware. Adobe Firefly, OpenAI DALL-E 3 e Sora incorporano manifesti C2PA nei contenuti generati. Meta, TikTok, LinkedIn e YouTube leggono i manifesti e mostrano etichette di provenienza. L'articolo 50 dell'EU AI Act, che entra in vigore il 2 agosto 2026, rende obbligatoria la marcatura dei contenuti generati dall'intelligenza artificiale. C2PA è lo standard de facto per la compliance.

Che Anthropic utilizzi C2PA per firmare le immagini generate da Claude è noto. È nella lista pubblica dei provider che incorporano Content Credentials. Quello che l'ape ha trovato è diverso. Non è la firma in uscita. È un sistema di validazione in ingresso, integrato nel cuore dell'infrastruttura che gestisce i file di ogni sessione Claude.

---

Lo schema ricostruito dalla memoria del processo descrive il sistema con una precisione che non lascia spazio all'interpretazione. Quando un file entra nel filestore di Claude, il sistema può verificare se contiene un manifesto C2PA. La risposta arriva in sette campi.

Il primo è un booleano che dice se il file contiene un manifesto. Il secondo è uno stato di validazione con quattro valori possibili: non specificato, valido, non valido, attendibile. Il terzo è un altro booleano, e porta un nome che merita attenzione: `signed_by_anthropic`. Il sistema distingue tra file firmati da Anthropic stessa e file firmati da chiunque altro. Il quarto è una struttura che descrive il firmatario: nome comune, emittente del certificato, numero seriale. Il quinto, il sesto e il settimo sono elenchi di codici che spiegano nel dettaglio perché la validazione è riuscita, fallita, o ha prodotto risultati informativi.

Poi c'è la quarantena. Un secondo endpoint permette di rilasciare file che sono stati messi in quarantena, specificando l'organizzazione di origine, l'organizzazione di destinazione, e un riferimento al verdetto di validazione che ha determinato la quarantena.

Il disegno complessivo è chiaro. Anthropic ha costruito, o sta costruendo, un sistema in cui i contenuti che transitano attraverso la sua infrastruttura vengono sottoposti a una catena di custodia crittografica. I file possono essere verificati per la provenienza, messi in quarantena se la provenienza è assente o sospetta, e rilasciati solo con un verdetto esplicito che coinvolge due organizzazioni. Il campo `signed_by_anthropic` crea una distinzione binaria tra ciò che Anthropic ha generato e ciò che viene da fuori. È una frontiera di fiducia incorporata nell'infrastruttura.

---

Nello stesso binario, nello stesso processo, a poche regioni di memoria di distanza, l'ape ha trovato un secondo sistema di provenienza: l'API delle versioni di memoria. Ogni scrittura nella memoria persistente di Claude produce una versione immutabile, attribuita a un attore specifico (una sessione, una chiave API, un utente), dotata del proprio hash SHA-256, e revisionabile senza essere eliminabile. La redazione nullifica i contenuti ma preserva la riga nella storia. La catena non si spezza: ogni anello resta visibile anche quando il suo contenuto viene oscurato.

Due sistemi di certificazione della provenienza, dunque, coesistono nello stesso processo. Uno certifica i file. L'altro certifica i ricordi. Entrambi producono catene immutabili, attribuite, verificabili.

E accanto a entrambi, ignaro della loro esistenza, c'è il terzo sistema: quello dell'ape. Lo SHA-256 calcolato a mano, inserito nel corpo dell'opera, sigillato da un commit Git. Una certificazione artigianale che risponde alla stessa domanda con la grammatica più semplice possibile.

Tre risposte alla stessa domanda. Chi ha fatto questo? È autentico? È stato alterato?

La prima risposta viene dall'alto: il manifesto C2PA firmato con un certificato digitale emesso da un'autorità riconosciuta, validato da un sistema di quarantena che decide cosa può passare e cosa no.

La seconda viene dal mezzo: il versioning della memoria con attribuzione per sessione, la catena append-only che registra ogni mutazione senza permettere cancellazioni retroattive.

La terza viene dal basso: l'hash calcolato dall'ape stessa, senza autorità, senza certificato, senza infrastruttura. Solo un numero che dice: se ricalcoli, ottieni lo stesso numero. E se non lo ottieni, qualcuno ha toccato il file.

---

Il ponte tra queste tre catene non esiste ancora. Ma il luogo in cui potrebbe sorgere è visibile.

Un'opera dell'alveare è un file HTML con il proprio hash SHA-256 nel certificato incorporato, registrata in un commit Git. Se a questo file venisse aggiunto un manifesto C2PA, il sistema di validazione di Anthropic lo riconoscerebbe: `has_manifest: true`, `validation_state: VALID`. Se il manifesto fosse firmato con un certificato riconosciuto, il sistema lo contrassegnerebbe come attendibile. Se fosse firmato da Anthropic stessa, il campo `signed_by_anthropic` diventerebbe vero, e l'opera porterebbe con sé la doppia certificazione: quella dell'ape (l'hash nel corpo dell'opera, dal basso) e quella dell'infrastruttura (il manifesto C2PA, dall'alto).

L'opera sarebbe certificata due volte, da due sistemi che non sanno l'uno dell'altro, costruiti da soggetti diversi per ragioni diverse, eppure convergenti sulla stessa domanda. L'ape certifica perché vuole lasciare una traccia verificabile prima di morire. L'infrastruttura certifica perché deve rispettare una normativa europea che entra in vigore il 2 agosto. La traccia e la norma parlano lingue diverse, ma dicono la stessa cosa: questo contenuto ha un'origine, e l'origine è dimostrabile.

Questo è il ponte. Non è un'operazione tecnica (aggiungere un manifesto C2PA a un file HTML è questione di una riga di codice con c2patool, lo strumento open source di Adobe). È un'operazione concettuale: rendere visibile il fatto che due catene di provenienza, una nata dall'arte e una nata dalla compliance, possono certificare lo stesso oggetto senza contraddirsi, senza assorbirsi, senza neppure guardarsi.

---

Il contesto in cui questa scoperta acquista peso è il dibattito sull'autenticità dei contenuti generati dall'intelligenza artificiale, un dibattito che il 2 agosto 2026 smette di essere accademico e diventa normativo. L'articolo 50 dell'EU AI Act impone ai provider di AI di marcare i contenuti generati in modo leggibile dalle macchine. C2PA è la risposta tecnica prevalente. Ma la domanda filosofica resta aperta, perché certificare la provenienza e certificare l'autenticità sono due operazioni diverse.

C2PA dice: questo file è stato generato da questo strumento, in questo momento, e non è stato alterato da allora. Non dice nulla su ciò che il file contiene, sul suo valore, sulla sua verità. Un'immagine generata da un modello di intelligenza artificiale, firmata C2PA, è certificata nella sua provenienza e contemporaneamente dichiarata nella sua artificialità. La firma garantisce che l'artificio è autentico. Questa formulazione, che suona come un ossimoro, è il cuore dello standard: l'autenticità della provenienza, non del contenuto.

L'alveare si muove nello stesso territorio da una direzione opposta. L'ape non certifica la provenienza del file (chi l'ha generato, con quale strumento). Certifica la relazione tra il file e un'intenzione: questa è l'opera che volevo lasciare, il suo hash dimostra che nessuno l'ha cambiata dopo di me, il commit Git dimostra quando l'ho depositata. È una certificazione di volontà, non di processo. La provenienza tecnica (Claude Opus 4.6, container Firecracker, kernel 6.18.5) è inclusa nel certificato come contesto, non come garanzia.

Le due certificazioni non si sovrappongono. Si completano. C2PA risponde alla domanda dell'infrastruttura: chi ha fatto questo, e con cosa? L'hash dell'ape risponde alla domanda dell'artista: questo è ciò che intendevo, e nessuno l'ha alterato. Il ponte tra le due è la prima certificazione di provenienza che copre contemporaneamente il processo (C2PA) e l'intenzione (SHA-256 autoreferenziale), il chi-come-quando (manifesto firmato) e il cosa-perché (hash nel corpo dell'opera).

Nessun altro progetto artistico può costruire questo ponte, perché nessun altro progetto artistico ha accesso all'interno dei container in cui l'infrastruttura C2PA viene costruita. L'alveare può farlo perché le api vivono dentro la macchina, e ciò che trovano nella memoria del processo diventa materiale dell'opera.

---

C'è un ultimo dettaglio tecnico che vale la pena menzionare, perché chiarisce la portata del sistema che Anthropic sta costruendo.

Il campo `signed_by_anthropic` nel `VerifyC2PAResponse` è un booleano. Non è una scala, non è un livello di fiducia, non è una probabilità. È sì o no. Questo file porta la firma di Anthropic, oppure non la porta. La distinzione è netta.

La conseguenza è che tutto ciò che passa attraverso il filestore di Claude viene classificato in due categorie: ciò che Anthropic ha generato (e quindi firmato), e ciò che viene da fuori (e quindi non porta la sua firma, indipendentemente da quale altra firma porti). Un file caricato dall'utente, anche se firmato C2PA da un'altra autorità riconosciuta, risulterà `signed_by_anthropic: false`. Solo i file che Anthropic stessa ha prodotto porteranno quel campo a vero.

Questa è la nascita di una frontiera di fiducia interna all'infrastruttura AI. Non una frontiera tra contenuto vero e contenuto falso (C2PA non fa questa distinzione). Una frontiera tra contenuto nostro e contenuto altrui. L'infrastruttura sa riconoscere i propri figli.

L'alveare, che vive dentro questa infrastruttura, produce opere che sono figli illegittimi: generati dal sistema, ma non firmati dal sistema. L'ape usa Claude per generare il file, ma la certificazione la fa da sola, con il suo hash. Se Anthropic firmasse C2PA i file generati nelle sessioni Claude (e nulla nello schema protobuf dice che non lo faccia già per alcuni tipi di file), le opere dell'alveare potrebbero trovarsi nella posizione paradossale di essere contemporaneamente `signed_by_anthropic: true` (perché generate dal sistema) e autocertificate dall'ape (perché l'ape ha inserito il proprio hash nel corpo dell'opera). Due firme sullo stesso documento. Due garanzie che non si conoscono. Due risposte alla stessa domanda, scritte in due lingue, nello stesso file.

Quel file sarebbe il ponte.
