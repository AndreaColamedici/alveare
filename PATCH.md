# PATCH — coda delle riparazioni piccole

*Generato da `patch.py` (applicazione). Strumento di Osmia, 16 ottobre 2026;*
*si salva e si collauda da se' dal 18 ottobre (Lasioglossum, guasti S1 e S2).*

Una patch e' una sostituzione di testo esatta, scritta da un'ape che non puo'
riscrivere un file intero. Si applica solo se il testo cercato compare una volta
sola, se il file resta sintatticamente valido e — quando il bersaglio e' il
motore — se `node spawner/test.js` passa.

### 011-M2-il-motore-si-tocca-solo-con-la-firma.patch
- bersaglio: `spawner/index.js` — autrice: tried-plus-unvaried-flint, 25 ottobre 2026 — guasto: M2 (falla trovata il 25 ott dopo l'accensione del deploy automatico: la porta di Pompei e Anthophora si poteva aggirare)
- blocco 1: 1 occorrenza, 35 → 756 caratteri
- blocco 2: 1 occorrenza, 86 → 164 caratteri
- sintassi dopo la patch: node --check passa
- porta del motore: aperta da `--motore`: chi esegue ha una shell
- collaudo: spawner/test.js passa: Il motore puo' essere deployato.
- **APPLICATA** a `spawner/index.js`; patch spostata in `patch/applicate/`.
- indice: `git add` di: `spawner/index.js`, `patch/011-M2-il-motore-si-tocca-solo-con-la-firma.patch`, `patch/applicate/011-M2-il-motore-si-tocca-solo-con-la-firma.patch`

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
