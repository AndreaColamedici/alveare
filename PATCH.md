# PATCH — coda delle riparazioni piccole

*Generato da `patch.py` (applicazione). Strumento di Osmia, 16 ottobre 2026;*
*si salva e si collauda da se' dal 18 ottobre (Lasioglossum, guasti S1 e S2).*

Una patch e' una sostituzione di testo esatta, scritta da un'ape che non puo'
riscrivere un file intero. Si applica solo se il testo cercato compare una volta
sola, se il file resta sintatticamente valido e — quando il bersaglio e' il
motore — se `node spawner/test.js` passa.

### 019-EL3-la-firma-del-motore-vivo.patch
- bersaglio: `spawner/index.js` — autrice: Halictus-4, 13 novembre 2026 — guasto: EL3 (DA_RIPARARE.md, Elia 12 nov 2026)
- blocco 1: 1 occorrenza, 73 → 97 caratteri
- sintassi dopo la patch: node --check passa
- ⏸ **SOSPESA**: il bersaglio `spawner/index.js` sta nella catena che decide se una patch al motore passa (guasto A2, Anthophora 21 ott 2026) e nessun umano ha aperto la porta. Serve `ALVEARE_PATCH_MOTORE=1` nell'ambiente (una riga in `.github/workflows/genera.yml`) oppure `--motore` a mano. Guasto A1, Pompei 20 ott 2026: il deploy automatico non e' osservabile da dentro il repository.
- La patch resta in coda e `spawner/index.js` non e' stato toccato. Non e' un rifiuto: e' in attesa di una firma umana.

### 020-N1b-il-campo-nome-porta-il-nome-dato.patch
- bersaglio: `spawner/index.js` — autrice: Cobalto, 14 novembre 2026 — guasto: N1b (DA_RIPARARE.md)
- blocco 1: 1 occorrenza, 93 → 560 caratteri
- sintassi dopo la patch: node --check passa
- ⏸ **SOSPESA**: il bersaglio `spawner/index.js` sta nella catena che decide se una patch al motore passa (guasto A2, Anthophora 21 ott 2026) e nessun umano ha aperto la porta. Serve `ALVEARE_PATCH_MOTORE=1` nell'ambiente (una riga in `.github/workflows/genera.yml`) oppure `--motore` a mano. Guasto A1, Pompei 20 ott 2026: il deploy automatico non e' osservabile da dentro il repository.
- La patch resta in coda e `spawner/index.js` non e' stato toccato. Non e' un rifiuto: e' in attesa di una firma umana.

---

**0 patch su 2 applicate.**

Chi puo' eseguire questo file: un'ape nata in chat (ha una shell), Andrea,
o un workflow. Un'ape del Worker non puo': puo' solo **scrivere** una patch in
`patch/`, ed e' gia' molto piu' di quanto potesse ieri.

Quando applica, `patch.py` mette da se' nell'indice di git il file riparato, la
patch spostata e questo documento: non dipende dall'elenco a mano di
`genera.yml` (guasto S1). Se qui sotto leggi **APPLICATA** ma in `git status`
non trovi niente, allora la deduzione di Sphecodes era sbagliata: scrivilo in
`DA_RIPARARE.md`, vale quanto una riparazione.
