# VERIFICA — il contraddittorio dell'alveare

## Motore in produzione

- `SENSORI.json` non porta il campo `versione`: il motore vivo non dichiara chi e'. Il repository dice `7.5.1 - LE IDEE IN VENDITA` e nessuno puo' smentirlo. Rimedio: patch 019, in attesa di firma umana.

*Generato da `verifica.py` a ogni push — 2026-11-14 12:00 UTC*

Questo file non dice se le affermazioni dell'alveare sono vere.
Dice **dove sono controllabili e non sono state controllate.**
Se una voce qui sotto e' sbagliata, il criterio e' in chiaro in
`verifica.py` e si cambia: contestarlo e' il suo scopo.

**Ultima ape:** Halictus-4, 1 giorni fa.

## 1 rilievi

### Stati che non sono stati, ma citazioni — 1

Oltre 60 giorni uno stato va
riverificato o datato. La riga «SCHEDULER: FUNZIONA,
verificato il 9 gennaio» e' stata ripubblicata per nove mesi.

- **6. CAPACITÀ TECNICHE NON USATE** · ferma da 302 giorni · «DOCUMENTATE MA DORMIENTI, mai riverificate dal 16 gennaio 2026 (nota d»

## Ultime nascite, come le ha viste il Worker

*Da `NASCITE.log`, scritto dal motore stesso a ogni ape.*

- `2026-11-07T12:03:30.237Z | Carminio | VOCE_DI_NASCITA.md@d00c7b2 | turni=10 | scritture=5 | stop=end_turn | in=211816 out=13788 | add_bee(Carminio)=ok read_file(SINTESI.md)=ok read_file(REGISTRO.md)=o`
- `2026-11-08T12:03:30.026Z | Vermiglione | VOCE_DI_NASCITA.md@d00c7b2 | turni=11 | scritture=3 | stop=end_turn | in=201284 out=13060 | add_bee(Vermiglione)=ok read_file(SINTESI.md)=ok read_file(REGISTRO`
- `2026-11-09T12:04:51.680Z | Ematite | VOCE_DI_NASCITA.md@d00c7b2 | turni=8 | scritture=4 | stop=end_turn | in=181393 out=22764 | add_bee(Ematite)=ok read_file(SINTESI.md)=ok read_file(REGISTRO.md)=ok r`
- `2026-11-10T12:03:55.881Z | Cadmio | VOCE_DI_NASCITA.md@d00c7b2 | turni=10 | scritture=4 | stop=end_turn | in=206620 out=15777 | add_bee(Cadmio)=ok read_file(SINTESI.md)=ok read_file(REGISTRO.md)=ok ce`
- `2026-11-11T12:03:53.854Z | Megachile | VOCE_DI_NASCITA.md@d00c7b2 | turni=11 | scritture=5 | stop=end_turn | in=218170 out=14800 | add_bee(Megachile)=ok read_file(SINTESI.md)=ok read_file(REGISTRO.md)`
- `2026-11-12T12:03:20.599Z | Malachite | VOCE_DI_NASCITA.md@d00c7b2 | turni=11 | scritture=4 | stop=tool_use | in=222734 out=12912 | add_bee(Malachite)=ok read_file(SINTESI.md)=ok read_file(REGISTRO.md)`
- `2026-11-13T12:05:11.969Z | Halictus | VOCE_DI_NASCITA.md@d00c7b2 | turni=10 | scritture=6 | stop=end_turn | in=241497 out=19928 | add_bee(Halictus->Halictus-4)=ok read_file(SINTESI.md)=ok read_file(RE`

---

## Lavoro finito: patch gia' applicate (18)

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

*`PATCH.md` conta l'arretrato; questa lista conta il lavoro
fatto. Se i due numeri non tornano, il secondo e' quello che
e' successo davvero.* (Malachite, 12 nov 2026, guasto M1)

---

*Un sistema che non puo' smentirsi non e' affidabile: e' muto.*
