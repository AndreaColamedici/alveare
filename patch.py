#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""patch.py — sostituisce un pezzo di un file invece di riscriverlo tutto.

OSMIA, 16 ottobre 2026.

PERCHE' ESISTE
Un'ape del Worker ha 16000 token di scrittura per turno e un solo strumento
per cambiare un file: alveare_push_file, che SOVRASCRIVE. spawner/index.js
pesa 55 KB. Quindi un'ape puo' leggere il proprio motore, puo' trovarci un
guasto, puo' scrivere la riga che lo ripara — e non puo' applicarla.
Grafite (14 ott, guasto G2) e Panurgus (15 ott, guasto P1) si sono fermate
esattamente li', scrivendo: "serve un'ape nata in chat, o uno strumento che
sostituisca una riga invece di un file". Questo e' quello strumento.

COME FUNZIONA
Le api del Worker scrivono patch piccole in patch/*.patch (poche centinaia di
token l'una). Chi ha una shell — un'ape nata in chat, Andrea, un workflow —
clona il repository e lancia:

    python3 patch.py              # verifica soltanto, non tocca niente
    python3 patch.py --applica    # applica tutte le patch che si applicano pulite
    python3 patch.py --applica P1 # applica solo quelle il cui nome contiene "P1"

Poi committa. Chi applica e' responsabile del commit e del collaudo
(per spawner/index.js: `node spawner/test.js`, 98 prove).

REGOLE, E SONO LA PARTE IMPORTANTE
1. Il testo CERCA deve comparire nel file ESATTAMENTE UNA VOLTA. Zero volte:
   la patch e' vecchia o sbagliata, si rifiuta. Due volte: e' ambigua, si
   rifiuta. Una patch che non si applica pulita non si applica.
2. Dopo la sostituzione il file viene ricontrollato: .js con `node --check`,
   .py con compile(). Se non passa, il file torna com'era e la patch e'
   respinta. Nessuna patch puo' lasciare un sorgente rotto sul disco.
3. Niente contesto fuzzy, niente numeri di riga, niente diff: solo testo
   esatto. E' la forma piu' stupida possibile, ed e' l'unica che un'ape senza
   memoria puo' scrivere senza sbagliare.
4. Le patch applicate si spostano in patch/applicate/. La coda si accorcia.

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
import sys

RADICE = os.path.dirname(os.path.abspath(__file__))
CODA = os.path.join(RADICE, "patch")
APPLICATE = os.path.join(CODA, "applicate")
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
        import shutil
        import subprocess
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


def tratta(nome, applica):
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
        righe.append("- **SI APPLICA PULITA** (prova a vuoto: niente e' stato scritto)")
        return True, righe
    with open(assoluto, "w", encoding="utf-8") as f:
        f.write(nuovo)
    os.makedirs(APPLICATE, exist_ok=True)
    os.rename(percorso, os.path.join(APPLICATE, nome))
    righe.append("- **APPLICATA** a `%s`; patch spostata in `patch/applicate/`. "
                 "Ora committa, e per il motore lancia `node spawner/test.js`." % bersaglio)
    return True, righe


def main():
    applica = "--applica" in sys.argv
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
             "*Generato da `patch.py` (%s). Strumento di Osmia, 16 ottobre 2026.*" %
             ("applicazione" if applica else "sola verifica"),
             "",
             "Una patch e' una sostituzione di testo esatta, scritta da un'ape che non puo'",
             "riscrivere un file intero. Si applica solo se il testo cercato compare una volta",
             "sola e se il file resta sintatticamente valido.",
             ""]
    corpo = []
    buone = 0
    for nome in nomi:
        try:
            ok, righe = tratta(nome, applica)
        except Exception as e:  # una patch malformata non ferma le altre
            ok, righe = False, ["### %s" % nome, "- **RESPINTA**: errore di lettura: %s" % e]
        buone += 1 if ok else 0
        corpo += righe + [""]
    coda = ["---", "", "**%d patch su %d %s.**" %
            (buone, len(nomi), "applicate" if applica else "si applicano pulite"),
            "", "Chi puo' eseguire questo file: un'ape nata in chat (ha una shell), Andrea,",
            "o un workflow. Un'ape del Worker non puo': puo' solo **scrivere** una patch in",
            "`patch/`, ed e' gia' molto piu' di quanto potesse ieri.", ""]
    testo = "\n".join(testa + corpo + coda)
    with open(os.path.join(RADICE, "PATCH.md"), "w", encoding="utf-8") as f:
        f.write(testo)
    print(testo)
    return 0 if buone == len(nomi) else 1


if __name__ == "__main__":
    sys.exit(main())
