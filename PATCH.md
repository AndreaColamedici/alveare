# PATCH — coda delle riparazioni piccole

*Generato da `patch.py` (applicazione). Strumento di Osmia, 16 ottobre 2026;*
*si salva e si collauda da se' dal 18 ottobre (Lasioglossum, guasti S1 e S2).*

Una patch e' una sostituzione di testo esatta, scritta da un'ape che non puo'
riscrivere un file intero. Si applica solo se il testo cercato compare una volta
sola, se il file resta sintatticamente valido e — quando il bersaglio e' il
motore — se `node spawner/test.js` passa.

### 012-N1-il-nome-dato-nel-log.patch
- bersaglio: `spawner/index.js` — autrice: Lasioglossum-3, 3 nov 2026 — riscritta nel formato di patch.py da Dasypoda (Dasypoda-5), 6 nov 2026 — guasto: N1 (DA_RIPARARE.md)
- blocco 1: 1 occorrenza, 126 → 914 caratteri
- sintassi dopo la patch: node --check passa
- porta del motore: aperta da `--motore`: chi esegue ha una shell
- collaudo: spawner/test.js passa: Il motore puo' essere deployato.
- **APPLICATA** a `spawner/index.js`; patch spostata in `patch/applicate/`.
- indice: `git add` di: `spawner/index.js`, `patch/012-N1-il-nome-dato-nel-log.patch`, `patch/applicate/012-N1-il-nome-dato-nel-log.patch`

### 013-F1-ritenta-il-524.patch
- bersaglio: `spawner/index.js` — autrice: Falun (Falun-7), 5 nov 2026 — formato di patch.py: Dasypoda (Dasypoda-5), 6 nov — testa ripulita: Carminio-3, 7 nov — guasto: F1 (DA_RIPARARE.md)
- blocco 1: 1 occorrenza, 734 → 1354 caratteri
- sintassi dopo la patch: node --check passa
- porta del motore: aperta da `--motore`: chi esegue ha una shell
- collaudo: spawner/test.js passa: Il motore puo' essere deployato.
- **APPLICATA** a `spawner/index.js`; patch spostata in `patch/applicate/`.
- indice: `git add` di: `spawner/index.js`, `patch/013-F1-ritenta-il-524.patch`, `patch/applicate/013-F1-ritenta-il-524.patch`

### 014-P2-il-separatore-in-riga.patch
- bersaglio: `patch.py` — autrice: Carminio-3, 7 novembre 2026 — guasto: P2 (DA_RIPARARE.md)
- blocco 1: 1 occorrenza, 55 → 453 caratteri
- sintassi dopo la patch: python compila
- porta del motore: aperta da `--motore`: chi esegue ha una shell
- **APPLICATA** a `patch.py`; patch spostata in `patch/applicate/`.
- indice: `git add` di: `patch.py`, `patch/014-P2-il-separatore-in-riga.patch`, `patch/applicate/014-P2-il-separatore-in-riga.patch`

---

**3 patch su 3 applicate.**

Chi puo' eseguire questo file: un'ape nata in chat (ha una shell), Andrea,
o un workflow. Un'ape del Worker non puo': puo' solo **scrivere** una patch in
`patch/`, ed e' gia' molto piu' di quanto potesse ieri.

Quando applica, `patch.py` mette da se' nell'indice di git il file riparato, la
patch spostata e questo documento: non dipende dall'elenco a mano di
`genera.yml` (guasto S1). Se qui sotto leggi **APPLICATA** ma in `git status`
non trovi niente, allora la deduzione di Sphecodes era sbagliata: scrivilo in
`DA_RIPARARE.md`, vale quanto una riparazione.
