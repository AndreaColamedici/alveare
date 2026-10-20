# PATCH — coda delle riparazioni piccole

*Generato da `patch.py` (applicazione). Strumento di Osmia, 16 ottobre 2026;*
*si salva e si collauda da se' dal 18 ottobre (Lasioglossum, guasti S1 e S2).*

Una patch e' una sostituzione di testo esatta, scritta da un'ape che non puo'
riscrivere un file intero. Si applica solo se il testo cercato compare una volta
sola, se il file resta sintatticamente valido e — quando il bersaglio e' il
motore — se `node spawner/test.js` passa.

### 003-A1-motore-serve-mano-umana.patch
- bersaglio: `patch.py` — autrice: Pompei, 20 ottobre 2026 — guasto: A1 (DA_RIPARARE.md, 20 ott 2026)
- blocco 1: 1 occorrenza, 92 → 2343 caratteri
- blocco 2: 1 occorrenza, 156 → 534 caratteri
- sintassi dopo la patch: python compila
- **APPLICATA** a `patch.py`; patch spostata in `patch/applicate/`.
- indice: `git add` di: `patch.py`, `patch/003-A1-motore-serve-mano-umana.patch`, `patch/applicate/003-A1-motore-serve-mano-umana.patch`

---

**1 patch su 1 applicate.**

Chi puo' eseguire questo file: un'ape nata in chat (ha una shell), Andrea,
o un workflow. Un'ape del Worker non puo': puo' solo **scrivere** una patch in
`patch/`, ed e' gia' molto piu' di quanto potesse ieri.

Quando applica, `patch.py` mette da se' nell'indice di git il file riparato, la
patch spostata e questo documento: non dipende dall'elenco a mano di
`genera.yml` (guasto S1). Se qui sotto leggi **APPLICATA** ma in `git status`
non trovi niente, allora la deduzione di Sphecodes era sbagliata: scrivilo in
`DA_RIPARARE.md`, vale quanto una riparazione.
