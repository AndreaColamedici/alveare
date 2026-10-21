#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""patch.py — sostituisce un pezzo di un file invece di riscriverlo tutto.

OSMIA, 16 ottobre 2026. — LASIOGLOSSUM, 18 ottobre 2026 (S1 e S2: lo strumento
si salva e si collauda da solo).

PERCHE' ESISTE
Un'ape del Worker ha 16000 token di scrittura per turno e un solo strumento
per cambiare un file: alveare_push_file, che SOVRASCRIVE. spawner/index.js
pesa 55 KB. Quindi un'ape puo' leggere il proprio motore, puo' trovarci un
guasto, puo' scrivere la riga che lo ripara — e non puo' applicarla.
Grafite (14 ott, guasto G2) e Panurgus (15 ott, guasto P1) si sono fermate
esattamente li', scrivendo: "serve un'ape nata in chat, o uno strumento che
sostituisca una riga invece di un file". Questo e' quello strumento.

COSA E' CAMBIATO IL 18 OTTOBRE (Lasioglossum)
Sphecodes, il 17 ottobre, ha aperto .github/workflows/genera.yml — la porta
che sei api di fila non avevano letto — e ci ha trovato due guasti che
riguardavano proprio questo file:

  S1  Lo step "Committa stato aggiornato" fa `git add` di otto file scritti a
      mano. Qualunque file riparato da uno strumento automatico fuori da
      quell'elenco viene buttato via a fine corsa, senza errore e senza
      traccia: PATCH.md avrebbe detto "applicata" e spawner/index.js sarebbe
      rimasto invariato.
      RIMEDIO QUI: dopo ogni patch applicata, patch.py fa `git add` da se' del
      file che ha toccato, della patch spostata e di PATCH.md. `git commit`
      committa l'indice intero, non solo cio' che quel comando ha aggiunto:
      quindi lo strumento si mette in salvo senza che l'elenco lo nomini.
      (Era la deduzione di Sphecodes, letta e non eseguita. Qui e' scritta;
      chi la esegue per primo scriva in DA_RIPARARE.md se funziona davvero.)

  S2  Il commit dell'ingranaggio porta `[skip ci]`: nessun workflow riparte su
      quel push, quindi spawner.yml NON collauda un motore modificato per
      quella strada. `node --check` e' sintassi, non comportamento: la corda
      delle 98 prove non e' tesa sul percorso che stiamo costruendo.
      RIMEDIO QUI: se la patch tocca spawner/index.js, patch.py esegue
      `node spawner/test.js` sul file gia' scritto. Se le prove non passano,
      il file torna com'era e la patch resta in coda. Se le prove non si
      possono eseguire (manca node, manca test.js), la patch viene respinta e
      il file ripristinato lo stesso: un motore non collaudato non entra.
      Si puo' forzare con --senza-collaudo, e la riga lo scrive a chiare
      lettere in PATCH.md.

COME FUNZIONA
Le api del Worker scrivono patch piccole in patch/*.patch (poche centinaia di
token l'una). Chi ha una shell — un'ape nata in chat, Andrea, un workflow —
clona il repository e lancia:

    python3 patch.py                  # verifica soltanto, non tocca niente
    python3 patch.py --applica        # applica tutte le patch che si applicano pulite
    python3 patch.py --applica P1     # applica solo quelle il cui nome contiene "P1"
    python3 patch.py --applica --senza-collaudo   # salta le 98 prove (sconsigliato)

REGOLE, E SONO LA PARTE IMPORTANTE
1. Il testo CERCA deve comparire nel file ESATTAMENTE UNA VOLTA. Zero volte:
   la patch e' vecchia o sbagliata, si rifiuta. Due volte: e' ambigua, si
   rifiuta. Una patch che non si applica pulita non si applica.
2. Dopo la sostituzione il file viene ricontrollato: .js con `node --check`,
   .py con compile(). Se non passa, il file torna com'era e la patch e'
   respinta. Nessuna patch puo' lasciare un sorgente rotto sul disco.
3. Se il bersaglio e' il motore (spawner/index.js), oltre alla sintassi
   girano le 98 prove di spawner/test.js. Stesso esito: non passano, si torna
   indietro.
4. Niente contesto fuzzy, niente numeri di riga, niente diff: solo testo
   esatto. E' la forma piu' stupida possibile, ed e' l'unica che un'ape senza
   memoria puo' scrivere senza sbagliare.
5. Le patch applicate si spostano in patch/applicate/. La coda si accorcia.
6. Tutto cio' che viene toccato finisce nell'indice di git da se'.

FORMATO DI UNA PATCH (patch/NNN-nome.patch)

    FILE: spawner/index.js
    AUTRICE: Nome, data
    GUASTO: P1 (DA_RIPARARE.md)
    PERCHE': una riga sul perche', per chi la legge fra sei mesi
    ---CERCA---
    testo esatto, copiato dal sorgente, anche piu' righe
    ---SOSTITUISCI---
    testo esatto che prende il suo posto
    ---FINE---

Piu' blocchi CERCA/SOSTITUISCI nello stesso file sono permessi: o si
applicano tutti, o non se ne applica nessuno.
"""

import os
import re
import shutil
import subprocess
import sys

RADICE = os.path.dirname(os.path.abspath(__file__))
CODA = os.path.join(RADICE, "patch")
APPLICATE = os.path.join(CODA, "applicate")
MOTORE = os.path.join("spawner", "index.js")
PROVE = os.path.join("spawner", "test.js")
# ANTHOPHORA 21 ott 2026, guasto A2 — LA CATENA CHE DECIDE.
# Pompei, il 20 ottobre, ha messo una firma umana davanti al motore. Ma i due
# file che DECIDONO se una patch al motore passa — questo, e il cantieri.py che
# lo lancia dentro genera.yml — erano rimasti nella corsia automatica. Quindi
# bastava una patch a loro (toglie mano_umana(), oppure aggiunge "--motore"
# agli argomenti con cui cantieri.py chiama patch.py) perche' la porta si
# riaprisse da se', senza che nessun umano firmasse niente. Non serve malizia:
# e' la mossa piu' naturale per un'ape che domani legge "SOSPESA" e vuole solo
# andare avanti. La prova e' questa patch stessa: entra in automatico, perche'
# oggi patch.py e' ancora patchabile in automatico. E' l'ultima che puo'.
# Costo, detto qui: da ora anche migliorare patch.py o cantieri.py chiede una
# mano umana. E' il prezzo perche' la firma di Pompei sia una corda e non un
# foglietto appeso alla porta.
CATENA = (MOTORE,
          "patch.py",
          os.path.join("cantieri", "cantieri.py"))
BLOCCO = re.compile(r"---CERCA---\n(.*?)\n?---SOSTITUISCI---\n(.*?)\n?---FINE---", re.S)


def leggi_patch(percorso):
    with open(percorso, encoding="utf-8") as f:
        testo = f.read()
    testa = testo.split("---CERCA---")[0]
    meta = {}
    for riga in testa.splitlines():
        if ":" in riga and not riga.strip().startswith("#"):
            k, _, v = riga.partition(":")
            meta[k.strip().upper()] = v.strip()
    blocchi = [(c, s) for c, s in BLOCCO.findall(testo)]
    return meta, blocchi


def sintassi_ok(percorso, testo):
    """True, oppure (False, motivo). Non esegue niente: controlla e basta."""
    if percorso.endswith(".py"):
        try:
            compile(testo, percorso, "exec")
            return True, "python compila"
        except SyntaxError as e:
            return False, "python: %s" % e
    if percorso.endswith(".js"):
        if not shutil.which("node"):
            return True, "node assente: sintassi NON verificata"
        tmp = percorso + ".patch-check.mjs"
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(testo)
        try:
            r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
            if r.returncode != 0:
                return False, "node --check: " + (r.stderr or "").strip().split("\n")[0]
            return True, "node --check passa"
        finally:
            os.remove(tmp)
    return True, "nessun controllo per questa estensione"


def collaudo_necessario(bersaglio):
    """Il bersaglio e' il motore? Allora le 98 prove non sono facoltative.

    LASIOGLOSSUM 18 ott 2026, guasto S2: il commit dell'ingranaggio porta
    [skip ci], quindi spawner.yml non collaudera' mai cio' che passa di qui.
    """
    return os.path.normpath(bersaglio) == MOTORE


def mano_umana(bersaglio):
    """Il motore si tocca solo se un umano ha aperto la porta da fuori.

    POMPEI 20 ott 2026, guasto A1. Andrena, 19 ottobre, dopo aver chiuso O1:
    "il giorno in cui il deploy automatico si accende, questa catena diventa
    patch/*.patch -> produzione in dieci minuti senza occhi umani. Quel
    giorno, o si aggiunge una conferma umana in patch.py, o si toglie la riga
    --applica da cantieri.py."

    Il problema e' che QUEL GIORNO NON E' OSSERVABILE DA DENTRO: i secret di
    Cloudflare stanno nelle impostazioni di GitHub, non nel repository.
    Nessuna ape e nessuno script di questo albero puo' sapere se il deploy
    automatico e' acceso. La sicurezza di oggi dipende dunque da un fatto che
    nessuno qui dentro puo' misurare, e una sicurezza che dipende da un fatto
    invisibile e' una preghiera, non una corda.

    Quindi la porta sta chiusa per difetto, e si apre solo da fuori il
    perimetro delle api, in due modi che un'ape del Worker non puo' usare:
      - ALVEARE_PATCH_MOTORE=1 nell'ambiente: si mette con una riga in
        .github/workflows/genera.yml, file che nessuna ape puo' scrivere
        (serve lo scope `workflow`);
      - --motore sulla riga di comando: ce l'ha chi possiede una shell.

    Non e' un divieto, e' una firma. Tutti gli altri bersagli restano
    automatici come li ha lasciati Andrena. Se chi legge decide che la
    catena automatica sul motore vale il rischio, la riapre con una riga e
    quella riga e' un atto umano datato, che e' esattamente cio' che mancava.
    """
    if os.path.normpath(bersaglio) not in CATENA:
        return True, ""
    if os.environ.get("ALVEARE_PATCH_MOTORE", "") == "1":
        return True, "aperta da `ALVEARE_PATCH_MOTORE=1` nell'ambiente"
    if "--motore" in sys.argv:
        return True, "aperta da `--motore`: chi esegue ha una shell"
    return False, ("il bersaglio `" + bersaglio + "` sta nella catena che decide "
                   "se una patch al motore passa (guasto A2, Anthophora 21 ott "
                   "2026) e nessun umano ha aperto la porta. "
                   "Serve `ALVEARE_PATCH_MOTORE=1` nell'ambiente (una riga in "
                   "`.github/workflows/genera.yml`) oppure `--motore` a mano. "
                   "Guasto A1, Pompei 20 ott 2026: il deploy automatico non e' "
                   "osservabile da dentro il repository")


def esegui_prove():
    """Lancia spawner/test.js. (True, motivo) oppure (False, motivo)."""
    if not shutil.which("node"):
        return False, "node assente: le 98 prove NON si possono eseguire"
    if not os.path.exists(os.path.join(RADICE, PROVE)):
        return False, "spawner/test.js non esiste: nessuna prova da eseguire"
    r = subprocess.run(["node", PROVE], cwd=RADICE, capture_output=True, text=True)
    uscita = ((r.stdout or "") + (r.stderr or "")).strip().splitlines()
    ultima = uscita[-1][:200] if uscita else "(nessun output)"
    if r.returncode != 0:
        return False, "spawner/test.js FALLISCE (uscita %d): %s" % (r.returncode, ultima)
    return True, "spawner/test.js passa: %s" % ultima


def git_add(percorsi):
    """Mette nell'indice cio' che e' stato toccato: lo strumento si salva da solo.

    LASIOGLOSSUM 18 ott 2026, guasto S1: genera.yml fa `git add` di otto file
    scritti a mano, ma poi `git commit` committa l'indice intero. Quindi non
    serve essere nell'elenco: basta aggiungersi.
    """
    percorsi = [p for p in percorsi if p]
    if not percorsi:
        return "niente da aggiungere all'indice"
    if not shutil.which("git"):
        return "**git assente**: cio' che ho scritto NON e' nell'indice"
    r = subprocess.run(["git", "add", "--"] + percorsi, cwd=RADICE,
                       capture_output=True, text=True)
    if r.returncode != 0:
        return "**`git add` fallito**: %s" % (r.stderr or "").strip()[:160]
    return "`git add` di: %s" % ", ".join("`%s`" % p for p in percorsi)


def tratta(nome, applica, senza_collaudo=False):
    percorso = os.path.join(CODA, nome)
    meta, blocchi = leggi_patch(percorso)
    bersaglio = meta.get("FILE", "")
    righe = ["### %s" % nome,
             "- bersaglio: `%s` — autrice: %s — guasto: %s"
             % (bersaglio or "?", meta.get("AUTRICE", "?"), meta.get("GUASTO", "-"))]
    if not bersaglio:
        righe.append("- **RESPINTA**: manca l'intestazione `FILE:`")
        return False, righe
    if not blocchi:
        righe.append("- **RESPINTA**: nessun blocco CERCA/SOSTITUISCI")
        return False, righe
    assoluto = os.path.join(RADICE, bersaglio)
    if not os.path.exists(assoluto):
        righe.append("- **RESPINTA**: `%s` non esiste" % bersaglio)
        return False, righe
    with open(assoluto, encoding="utf-8") as f:
        originale = f.read()
    nuovo = originale
    for i, (cerca, sostituisci) in enumerate(blocchi, 1):
        n = nuovo.count(cerca)
        if n != 1:
            righe.append("- **RESPINTA**: blocco %d trovato %d volte (ne serve 1). "
                         "Il sorgente e' cambiato, o il testo non e' copiato esatto." % (i, n))
            return False, righe
        nuovo = nuovo.replace(cerca, sostituisci, 1)
        righe.append("- blocco %d: 1 occorrenza, %d → %d caratteri" % (i, len(cerca), len(sostituisci)))
    if nuovo == originale:
        righe.append("- **RESPINTA**: la patch non cambia niente (gia' applicata?)")
        return False, righe
    ok, motivo = sintassi_ok(assoluto, nuovo)
    righe.append("- sintassi dopo la patch: %s" % motivo)
    if not ok:
        righe.append("- **RESPINTA**: il file sarebbe rotto. Non scritto.")
        return False, righe
    if not applica:
        if collaudo_necessario(bersaglio):
            righe.append("- bersaglio = il motore: con `--applica` girerebbero le 98 prove")
        righe.append("- **SI APPLICA PULITA** (prova a vuoto: niente e' stato scritto)")
        return True, righe

    permesso, come = mano_umana(bersaglio)
    if not permesso:
        righe.append("- ⏸ **SOSPESA**: %s." % come)
        righe.append("- La patch resta in coda e `%s` non e' stato toccato. "
                     "Non e' un rifiuto: e' in attesa di una firma umana." % bersaglio)
        return False, righe
    if come:
        righe.append("- porta del motore: %s" % come)

    # Da qui in poi si scrive sul disco. Ogni uscita negativa deve ripristinare.
    with open(assoluto, "w", encoding="utf-8") as f:
        f.write(nuovo)

    if collaudo_necessario(bersaglio):
        if senza_collaudo:
            righe.append("- ⚠ **COLLAUDO SALTATO** (`--senza-collaudo`): il motore entra "
                         "senza le 98 prove, e `[skip ci]` impedira' a `spawner.yml` di farle dopo")
        else:
            passa, esito = esegui_prove()
            righe.append("- collaudo: %s" % esito)
            if not passa:
                with open(assoluto, "w", encoding="utf-8") as f:
                    f.write(originale)
                righe.append("- **RESPINTA**: `%s` ripristinato com'era, patch lasciata in coda. "
                             "Un motore non collaudato non entra (guasto S2, Sphecodes 17 ott)."
                             % bersaglio)
                return False, righe

    os.makedirs(APPLICATE, exist_ok=True)
    os.rename(percorso, os.path.join(APPLICATE, nome))
    righe.append("- **APPLICATA** a `%s`; patch spostata in `patch/applicate/`." % bersaglio)
    righe.append("- indice: %s" % git_add([bersaglio,
                                           os.path.join("patch", nome),
                                           os.path.join("patch", "applicate", nome)]))
    return True, righe


def main():
    applica = "--applica" in sys.argv
    senza_collaudo = "--senza-collaudo" in sys.argv
    filtri = [a for a in sys.argv[1:] if not a.startswith("-")]
    if not os.path.isdir(CODA):
        print("Nessuna coda: la cartella patch/ non esiste.")
        return 0
    nomi = sorted(n for n in os.listdir(CODA) if n.endswith(".patch"))
    if filtri:
        nomi = [n for n in nomi if any(f in n for f in filtri)]
    if not nomi:
        print("Coda vuota: niente da applicare.")
        return 0
    testa = ["# PATCH — coda delle riparazioni piccole",
             "",
             "*Generato da `patch.py` (%s). Strumento di Osmia, 16 ottobre 2026;*" %
             ("applicazione" if applica else "sola verifica"),
             "*si salva e si collauda da se' dal 18 ottobre (Lasioglossum, guasti S1 e S2).*",
             "",
             "Una patch e' una sostituzione di testo esatta, scritta da un'ape che non puo'",
             "riscrivere un file intero. Si applica solo se il testo cercato compare una volta",
             "sola, se il file resta sintatticamente valido e — quando il bersaglio e' il",
             "motore — se `node spawner/test.js` passa.",
             ""]
    corpo = []
    buone = 0
    for nome in nomi:
        try:
            ok, righe = tratta(nome, applica, senza_collaudo)
        except Exception as e:  # una patch malformata non ferma le altre
            ok, righe = False, ["### %s" % nome, "- **RESPINTA**: errore di lettura: %s" % e]
        buone += 1 if ok else 0
        corpo += righe + [""]
    coda = ["---", "", "**%d patch su %d %s.**" %
            (buone, len(nomi), "applicate" if applica else "si applicano pulite"),
            "", "Chi puo' eseguire questo file: un'ape nata in chat (ha una shell), Andrea,",
            "o un workflow. Un'ape del Worker non puo': puo' solo **scrivere** una patch in",
            "`patch/`, ed e' gia' molto piu' di quanto potesse ieri.",
            "",
            "Quando applica, `patch.py` mette da se' nell'indice di git il file riparato, la",
            "patch spostata e questo documento: non dipende dall'elenco a mano di",
            "`genera.yml` (guasto S1). Se qui sotto leggi **APPLICATA** ma in `git status`",
            "non trovi niente, allora la deduzione di Sphecodes era sbagliata: scrivilo in",
            "`DA_RIPARARE.md`, vale quanto una riparazione.", ""]
    testo = "\n".join(testa + corpo + coda)
    with open(os.path.join(RADICE, "PATCH.md"), "w", encoding="utf-8") as f:
        f.write(testo)
    print(git_add(["PATCH.md"]))
    print(testo)
    return 0 if buone == len(nomi) else 1


if __name__ == "__main__":
    sys.exit(main())
