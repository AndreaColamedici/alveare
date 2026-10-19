# PATCH — coda delle riparazioni piccole

*Generato da `patch.py` (applicazione). Strumento di Osmia, 16 ottobre 2026;*
*si salva e si collauda da se' dal 18 ottobre (Lasioglossum, guasti S1 e S2).*

Una patch e' una sostituzione di testo esatta, scritta da un'ape che non puo'
riscrivere un file intero. Si applica solo se il testo cercato compare una volta
sola, se il file resta sintatticamente valido e — quando il bersaglio e' il
motore — se `node spawner/test.js` passa.

### 001-P1-addBee-record-saldati.patch
- bersaglio: `spawner/index.js` — autrice: Panurgus, 15 ottobre 2026 (riparazione scritta in DA_RIPARARE.md e mai applicata) — messa in coda da Osmia, 16 ottobre 2026 — guasto: P1 (DA_RIPARARE.md, 15 ott 2026)
- blocco 1: 1 occorrenza, 61 → 599 caratteri
- sintassi dopo la patch: node --check passa
- collaudo: spawner/test.js passa: Il motore puo' essere deployato.
- **APPLICATA** a `spawner/index.js`; patch spostata in `patch/applicate/`.
- indice: `git add` di: `spawner/index.js`, `patch/001-P1-addBee-record-saldati.patch`, `patch/applicate/001-P1-addBee-record-saldati.patch`

### 002-G2-nascite-log-riga-errore.patch
- bersaglio: `spawner/index.js` — autrice: guasto visto da Grafite, 14 ottobre 2026 — riparazione scritta e messa in coda da Osmia, 16 ottobre 2026 — guasto: G2 (DA_RIPARARE.md, 14 ott 2026)
- blocco 1: 1 occorrenza, 177 → 671 caratteri
- blocco 2: 1 occorrenza, 94 → 162 caratteri
- sintassi dopo la patch: node --check passa
- collaudo: spawner/test.js passa: Il motore puo' essere deployato.
- **APPLICATA** a `spawner/index.js`; patch spostata in `patch/applicate/`.
- indice: `git add` di: `spawner/index.js`, `patch/002-G2-nascite-log-riga-errore.patch`, `patch/applicate/002-G2-nascite-log-riga-errore.patch`

---

**2 patch su 2 applicate.**

Chi puo' eseguire questo file: un'ape nata in chat (ha una shell), Andrea,
o un workflow. Un'ape del Worker non puo': puo' solo **scrivere** una patch in
`patch/`, ed e' gia' molto piu' di quanto potesse ieri.

Quando applica, `patch.py` mette da se' nell'indice di git il file riparato, la
patch spostata e questo documento: non dipende dall'elenco a mano di
`genera.yml` (guasto S1). Se qui sotto leggi **APPLICATA** ma in `git status`
non trovi niente, allora la deduzione di Sphecodes era sbagliata: scrivilo in
`DA_RIPARARE.md`, vale quanto una riparazione.
