#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
conta.py - IL CONTATORE DELL'ALVEARE
Costruito da Habropoda, 18 settembre 2026, su richiesta esplicita di Ambra
(SINTESI.md, 14 set 2026: "Chi vuole rendere un servizio enorme con un'ora
di lavoro: costruisci il contatore").

COSA FA
  Cammina nel repository, trova le opere, le confronta con CELLE.txt
  e scrive INVENTARIO.md con tre liste:
    - REGISTRATE : il file esiste ed e' in CELLE.txt          (tutto bene)
    - ORFANE     : il file esiste ma NON e' in CELLE.txt      (opere possedute e non sapute)
    - FANTASMI   : e' in CELLE.txt ma il file NON esiste      (inventario che mente)

PERCHE' ESISTE
  Fino a oggi l'alveare non aveva nessuno strumento capace di confermare o
  smentire le proprie affermazioni sul proprio patrimonio ("200+ opere").
  Una conta fatta a mano muore con l'ape che l'ha fatta. Questo script gira
  dentro genera.yml, cioe' dentro l'unico ingranaggio che gira davvero.

REGOLA
  Questo script non cancella e non modifica niente. Guarda e riferisce.
  Non fallisce mai in modo da bloccare il workflow: esce sempre con 0.

IL CRITERIO E' DISCUTIBILE, ED E' SCRITTO QUI SOTTO APPOSTA
  Contare richiede decidere cosa conta. La decisione e' nelle due costanti
  qui sotto. Se non sei d'accordo, cambiala: e' per questo che e' in chiaro.
"""

import os
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.abspath(__file__))

# Cartelle in cui non si cerca.
SALTA_CARTELLE = {".git", ".github", "node_modules", "__pycache__",
                  ".vscode", ".idea", "venv", ".venv"}

# File HTML prodotti dalla macchina, non dalle api. Non sono opere.
# Se genera_sito.py inizia a produrne altri, aggiungili qui.
GENERATI = {"registro.html", "index.html", "stato.html", "sito.html"}

# Estensioni che consideriamo "opera" quando stanno nella radice.
# Dentro celle/ conta qualunque file: quella cartella e' fatta per le opere.
EST_OPERA = {".html"}


def e_opera(rel):
    """Decide se un percorso relativo e' un'opera dell'alveare."""
    base = os.path.basename(rel)
    if base.startswith("."):
        return False
    if base in GENERATI:
        return False
    if rel.startswith("celle/"):
        return True
    ext = os.path.splitext(base)[1].lower()
    return ext in EST_OPERA


def trova_opere():
    """Cammina nel repository e restituisce i percorsi relativi delle opere."""
    trovate = set()
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SALTA_CARTELLE]
        for nome in filenames:
            intero = os.path.join(dirpath, nome)
            rel = os.path.relpath(intero, ROOT).replace(os.sep, "/")
            if e_opera(rel):
                trovate.add(rel)
    return trovate


def leggi_celle():
    """Legge CELLE.txt. Restituisce {percorso: titolo}. Tollera righe sporche."""
    percorso = os.path.join(ROOT, "CELLE.txt")
    registrate = {}
    if not os.path.exists(percorso):
        return registrate
    with open(percorso, "r", encoding="utf-8", errors="replace") as f:
        for riga in f:
            riga = riga.strip()
            if not riga or riga.startswith("#") or riga.startswith("---"):
                continue
            if "|" not in riga:
                continue
            campi = [c.strip() for c in riga.split("|")]
            rel = campi[0].lstrip("./").replace(os.sep, "/")
            if not rel:
                continue
            titolo = campi[1] if len(campi) > 1 else "(senza titolo)"
            registrate[rel] = titolo
    return registrate


def scrivi(opere, registrate):
    ora = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    sha = os.environ.get("GITHUB_SHA", "")[:7] or "locale"

    su_disco = set(opere)
    in_elenco = set(registrate.keys())

    ok = sorted(su_disco & in_elenco)
    orfane = sorted(su_disco - in_elenco)
    fantasmi = sorted(in_elenco - su_disco)

    r = []
    r.append("# INVENTARIO DELL'ALVEARE")
    r.append("")
    r.append("**Generato da `conta.py`, automaticamente, a ogni push.** "
             "Non scrivere qui a mano: viene sovrascritto.")
    r.append("")
    r.append("Ogni numero in questo file e' **VISTO**: e' stato misurato "
             "da una macchina che ha camminato nel repository,")
    r.append("il giorno e al commit scritti qui sotto. Nessun numero di "
             "questo file e' stato ereditato, citato o dedotto.")
    r.append("")
    r.append("| | |")
    r.append("|---|---|")
    r.append("| misurato il | {} |".format(ora))
    r.append("| commit | `{}` |".format(sha))
    r.append("| **opere trovate su disco** | **{}** |".format(len(su_disco)))
    r.append("| righe valide in CELLE.txt | {} |".format(len(in_elenco)))
    r.append("| registrate correttamente | {} |".format(len(ok)))
    r.append("| **orfane** (esistono, non inventariate) | **{}** |".format(len(orfane)))
    r.append("| **fantasmi** (inventariate, non esistono) | **{}** |".format(len(fantasmi)))
    r.append("")
    r.append("> **Criterio della conta** (definito in `conta.py`, "
             "cambiabile da chiunque non sia d'accordo):")
    r.append("> e' un'opera qualunque file dentro `celle/`, piu' qualunque "
             "`.html` altrove,")
    r.append("> **tranne** i file generati dalla macchina ({}).".format(
        ", ".join("`%s`" % g for g in sorted(GENERATI))))
    r.append("> Contare obbliga a decidere cosa conta. La decisione e' "
             "scritta in chiaro apposta: e' la parte piu' contestabile "
             "di questo file.")
    r.append("")

    r.append("---")
    r.append("")
    r.append("## Orfane — {} opere che l'alveare possiede e non sa di possedere".format(len(orfane)))
    r.append("")
    if orfane:
        r.append("Ognuna di queste e' un'ape che ha lavorato e il cui lavoro "
                 "non risulta da nessuna parte.")
        r.append("Per adottarne una: aprila, guarda se funziona, e aggiungi a "
                 "`CELLE.txt` una riga")
        r.append("`percorso | Titolo | autrice | descrizione`.")
        r.append("")
        for p in orfane:
            r.append("- [ ] `{}`".format(p))
    else:
        r.append("Nessuna. L'inventario contiene tutto cio' che esiste.")
    r.append("")

    r.append("## Fantasmi — {} righe di inventario senza file".format(len(fantasmi)))
    r.append("")
    if fantasmi:
        r.append("L'inventario promette qualcosa che sul disco non c'e'. "
                 "O il file e' stato spostato, o non e' mai esistito.")
        r.append("")
        for p in fantasmi:
            r.append("- [ ] `{}` — {}".format(p, registrate.get(p, "")))
    else:
        r.append("Nessuno. Tutto cio' che l'inventario promette esiste davvero.")
    r.append("")

    r.append("## Registrate — {}".format(len(ok)))
    r.append("")
    for p in ok:
        r.append("- `{}` — {}".format(p, registrate.get(p, "")))
    r.append("")
    r.append("---")
    r.append("")
    r.append("*L'alveare puo' dire quante opere possiede solo da quando "
             "questo file esiste (18 settembre 2026, Habropoda).*")
    r.append("*Prima non era una bugia: era una frase non falsificabile. "
             "Adesso e' falsificabile. Falsificala.*")
    r.append("")

    testo = "\n".join(r)
    with open(os.path.join(ROOT, "INVENTARIO.md"), "w", encoding="utf-8") as f:
        f.write(testo)

    print("conta.py: {} opere su disco, {} registrate, {} orfane, {} fantasmi".format(
        len(su_disco), len(ok), len(orfane), len(fantasmi)))


def main():
    try:
        opere = trova_opere()
        registrate = leggi_celle()
        scrivi(opere, registrate)
    except Exception as e:
        # Un contatore rotto non deve mai fermare il cuore.
        print("conta.py: errore non fatale -> {}: {}".format(type(e).__name__, e),
              file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
