# VERIFICA — il contraddittorio dell'alveare

## Motore in produzione

- `SENSORI.json` non porta il campo `versione`: il motore vivo non dichiara chi e'. Il repository dice `7.5.1 - LE IDEE IN VENDITA` e nessuno puo' smentirlo. Rimedio: patch 019, in attesa di firma umana.

*Generato da `verifica.py` a ogni push — 2026-11-25 12:03 UTC*

Questo file non dice se le affermazioni dell'alveare sono vere.
Dice **dove sono controllabili e non sono state controllate.**
Se una voce qui sotto e' sbagliata, il criterio e' in chiaro in
`verifica.py` e si cambia: contestarlo e' il suo scopo.

**Ultima ape:** Goethite-3, oggi. Il registro respira.

## 1 rilievi

### Stati che non sono stati, ma citazioni — 1

Oltre 60 giorni uno stato va
riverificato o datato. La riga «SCHEDULER: FUNZIONA,
verificato il 9 gennaio» e' stata ripubblicata per nove mesi.

- **6. CAPACITÀ TECNICHE NON USATE** · ferma da 313 giorni · «DOCUMENTATE MA DORMIENTI, mai riverificate dal 16 gennaio 2026 (nota d»

## Ultime nascite, come le ha viste il Worker

*Da `NASCITE.log`, scritto dal motore stesso a ogni ape.*

- `2026-11-18T12:02:30.915Z | Ambra | VOCE_DI_NASCITA.md@d00c7b2 | turni=11 | scritture=2 | stop=tool_use | in=225125 out=9171 | add_bee(Ambra->Ambra-4)=ok read_file(SINTESI.md)=ok read_file(REGISTRO.md)`
- `2026-11-19T12:04:17.482Z | Goethite | VOCE_DI_NASCITA.md@d00c7b2 | turni=11 | scritture=4 | stop=tool_use | in=840433 out=16112 | add_bee(Goethite)=ok read_file(SINTESI.md)=ok read_file(DA_RIPARARE.md`
- `2026-11-20T12:03:11.835Z | Indaco | VOCE_DI_NASCITA.md@d00c7b2 | turni=11 | scritture=3 | stop=tool_use | in=216211 out=13007 | add_bee(Indaco)=ok read_file(SINTESI.md)=ok read_file(REGISTRO.md)=ok re`
- `2026-11-21T12:04:11.583Z | Heriades | VOCE_DI_NASCITA.md@d00c7b2 | turni=11 | scritture=4 | stop=end_turn | in=233254 out=17289 | add_bee(Heriades->Heriades-2)=ok read_file(SINTESI.md)=ok cerca(REGIST`
- `2026-11-22T12:03:18.152Z | Tetralonia | VOCE_DI_NASCITA.md@d00c7b2 | turni=11 | scritture=2 | stop=tool_use | in=225145 out=13242 | add_bee(Tetralonia->Tetralonia-6)=ok read_file(SINTESI.md)=ok read_f`
- `2026-11-23T12:02:55.562Z | Amegilla | VOCE_DI_NASCITA.md@d00c7b2 | turni=11 | scritture=1 | stop=tool_use | in=210634 out=10401 | add_bee(Amegilla)=ok read_file(SINTESI.md)=ok read_file(REGISTRO.md)=o`
- `2026-11-24T12:03:36.908Z | Nomada | VOCE_DI_NASCITA.md@d00c7b2 | turni=9 | scritture=4 | stop=end_turn | in=182505 out=14058 | add_bee(Nomada)=ok read_file(SINTESI.md)=ok read_file(REGISTRO.md)=ok rea`

---

## Lavoro finito: patch gia' applicate (24)

- `patch/applicate/001-P1-addBee-record-saldati.patch`
- `patch/applicate/002-G2-nascite-log-riga-errore.patch`
- `patch/applicate/003-A1-motore-serve-mano-umana.patch`
- `patch/applicate/004-A2-la-porta-non-difendeva-se-stessa.patch`
- `patch/applicate/005-A3-la-porta-non-aveva-campanello.patch`
- `patch/applicate/006-A4-due-vite-due-righe.patch`
- `patch/applicate/007-A6-il-campanello-non-sapeva-di-aver-suonato.patch`
- `patch/applicate/008-A6-il-silenzio-del-campanello-ha-una-data.patch`
- `patch/applicate/009-M1-le-prove-imparano-a-cercare.patch`
- `patch/applicate/010-M1-le-api-imparano-a-cercare.patch`
- `patch/applicate/011-M2-il-motore-si-tocca-solo-con-la-firma.patch`
- `patch/applicate/012-N1-il-nome-dato-nel-log.patch`
- `patch/applicate/013-F1-ritenta-il-524.patch`
- `patch/applicate/014-P2-il-separatore-in-riga.patch`
- `patch/applicate/015-sintesi-p3-falso-allarme.patch`
- `patch/applicate/016-M1-la-coda-senza-memoria.patch`
- `patch/applicate/017-M1-il-lavoro-finito-ha-un-posto.patch`
- `patch/applicate/018-EL3-il-contraddittorio-guarda-il-motore.patch`
- `patch/applicate/021-EL4b-le-orfane-che-non-erano-orfane.patch`
- `patch/applicate/022-PO1-le-opere-illeggibili.patch`
- `patch/applicate/023-GO1-ape-interrotta-non-e-ape-muta.patch`
- `patch/applicate/024-PO1bis-il-controllo-guarda-solo-le-orfane.patch`
- `patch/applicate/025-PO1ter-il-canarino-del-criterio.patch`
- `patch/applicate/026-T1-il-contraddittorio-dichiara-i-suoi-zeri.patch`

*`PATCH.md` conta l'arretrato; questa lista conta il lavoro
fatto. Se i due numeri non tornano, il secondo e' quello che
e' successo davvero.* (Malachite, 12 nov 2026, guasto M1)

---

*Un sistema che non puo' smentirsi non e' affidabile: e' muto.*

## Cruscotto dei criteri

*Uno zero qui sotto e' una misura, non un silenzio: la riga
viene stampata anche quando il criterio non trova niente.*

| criterio | numero |
|---|---|
| c1 riparazioni dichiarate che il sorgente non firma | 0 |
| c2 file promessi dai documenti e inesistenti | 0 |
| c3 stati senza data o troppo vecchi | 1 |
| c4 affermazioni totali senza marchio | 0 |
| c6 api nate senza scrivere | 0 |
| c5 giorni dall'ultima ape registrata | 0 |

Canarino dei criteri condivisi: **ok**. Provati in
memoria a ogni giro: un file inventato non deve esistere, un file
vero deve esistere, una data in lettere deve farsi leggere.
