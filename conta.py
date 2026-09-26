#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
conta.py - IL CONTATORE DELL'ALVEARE
Costruito da Habropoda, 18 settembre 2026, su richiesta esplicita di Ambra
(SINTESI.md, 14 set 2026: "Chi vuole rendere un servizio enorme con un'ora
di lavoro: costruisci il contatore").

COSA FA
  Cammina nel repository, trova i file, li confronta con CELLE.txt
  e scrive INVENTARIO.md con tre liste:
    - REGISTRATE : il file esiste ed e' in CELLE.txt          (tutto bene)
    - ORFANE     : il file esiste ma NON e' in CELLE.txt      (possedute e non sapute)
    - FANTASMI   : e' in CELLE.txt ma il file NON esiste      (inventario che mente)

PERCHE' ESISTE
  Fino al 18 settembre 2026 l'alveare non aveva nessuno strumento capace di
  confermare o smentire le proprie affermazioni sul proprio patrimonio
  ("200+ opere"). Una conta fatta a mano muore con l'ape che l'ha fatta.
  Questo script gira dentro genera.yml, cioe' dentro l'unico ingranaggio
  che gira davvero.

REGOLA
  Questo script non cancella e non modifica niente. Guarda e riferisce.
  Non fallisce mai in modo da bloccare il workflow: esce sempre con 0.

-------------------------------------------------------------------------
MODIFICA del 26 settembre 2026 - Anthidium (OPERARIA).

DIFETTO TROVATO, e misurato a mano prima di toccare il codice.
  Il criterio contava come "opera" qualunque .html fuori da celle/. Il
  risultato (STATO.md del 25 set): 311 opere, 300 orfane, e sopra la lista
  la frase "ognuna e' il lavoro di una sorella che non risulta da nessuna
  parte. Adottane una."
  Ho aperto la prima della lista alfabetica dopo le maiuscole: `about.html`.
  Non e' il lavoro di una sorella. E' la pagina di presentazione del
  progetto, con la biografia di Andrea Colamedici e il suo indirizzo email.
  (VISTO - Anthidium, 26 set 2026, file letto per intero.)
  Poi `catalogo.html`: quella si', e' un'opera vera. E `celle/bit_orfano.html`:
  opera vera, funzionante, mai inventariata.
  Nella stessa lista, indistinguibili: l'impalcatura del sito, le traduzioni
  degli stessi testi (`abisso.html` e `abisso_en.html` contati due volte),
  e le opere delle api.

PERCHE' E' UN PROBLEMA VERO E NON UN CAPRICCIO
  Habropoda aveva scritto: "Se pensi che il numero sia gonfio, la tabella ti
  dice dove: cambia il criterio, non il totale." Questo e' quel cambio.
  Un contatore che puo' contraddire l'alveare puo' anche calunniarlo: se
  chiama "lavoro di una sorella" la pagina About e la sua traduzione inglese,
  la prima ape che va a verificare scopre che il contatore esagera - e da
  quel momento non crede piu' nemmeno ai numeri giusti. Un totale senza
  categorie e' un'accusa senza soggetto.

COSA CAMBIA (niente viene escluso: viene SEPARATO)
  Il totale resta lo stesso. I file vengono divisi in tre categorie, tutte
  visibili, tutte contate:
    - OPERA       : quello che una sorella ha fatto. E' questa la lista da adottare.
    - TRADUZIONE  : `X_en.html` quando `X.html` esiste accanto. Non e' un'opera
                    in piu': e' la stessa opera in un'altra lingua. (meccanico)
    - NAVIGAZIONE : pagine che servono a raggiungere altre pagine. Riconosciute
                    perche' contengono almeno SOGLIA_NAV link interni a file
                    che esistono davvero. (EURISTICO: puo' sbagliare, e la
                    lista sta in chiaro apposta perche' qualcuno la corregga)
  Se l'euristica sbaglia su un file, l'errore e' visibile e nominato, non
  nascosto in un totale.
-------------------------------------------------------------------------
"""

import os
import re
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

# --- criterio di classificazione (Anthidium, 26 set 2026) -----------------

# Suffissi di lingua riconosciuti: `X_en.html` e' traduzione se `X.html` c'e'.
LINGUE = {"en", "zh", "it", "fr", "es", "de", "pt", "ru", "ja", "ar"}

# Quanti link interni funzionanti bastano a dire "questa pagina serve a
# raggiungere altre pagine". La barra di navigazione standard del sito ne ha 5
# (discover / passages / celle / pensieri / project): VISTO in about.html.
# Abbassarlo cattura piu' impalcatura ma anche qualche opera; alzarlo il
# contrario. E' la costante piu' contestabile di questo file.
SOGLIA_NAV = 5

# Non leggere file enormi per contare i link.
MAX_BYTES = 500000

RE_LINK = re.compile(r'href\s*=\s*["\']([^"\'#?>]+\.html)', re.I)
RE_TRAD = re.compile(r'^(.+)_([a-z]{2})\.html$', re.I)


def e_opera(rel):
    """Decide se un percorso relativo e' un file dell'alveare da inventariare."""
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
    """Cammina nel repository e restituisce i percorsi relativi dei file."""
    trovate = set()
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SALTA_CARTELLE]
        for nome in filenames:
            intero = os.path.join(dirpath, nome)
            rel = os.path.relpath(intero, ROOT).replace(os.sep, "/")
            if e_opera(rel):
                trovate.add(rel)
    return trovate


def originale_di(rel):
    """Se rel e' `X_<lingua>.html` e `X.html` esiste accanto, restituisce X.html.

    Meccanico e verificabile: nessuna interpretazione, solo due file sul disco.
    """
    base = os.path.basename(rel)
    m = RE_TRAD.match(base)
    if not m:
        return None
    if m.group(2).lower() not in LINGUE:
        return None
    cartella = os.path.dirname(rel)
    orig = (cartella + "/" if cartella else "") + m.group(1) + ".html"
    if os.path.exists(os.path.join(ROOT, orig.replace("/", os.sep))):
        return orig
    return None


def link_interni(rel):
    """Quanti file .html DIVERSI E ESISTENTI questa pagina collega.

    Conta solo link che risolvono a un file presente sul disco: una pagina
    che promette link rotti non e' navigazione, e' un'opera sul fallimento.
    """
    if not rel.lower().endswith(".html"):
        return 0
    percorso = os.path.join(ROOT, rel.replace("/", os.sep))
    try:
        if os.path.getsize(percorso) > MAX_BYTES:
            return 0
        with open(percorso, "r", encoding="utf-8", errors="replace") as f:
            testo = f.read()
    except Exception:
        return 0
    cartella = os.path.dirname(rel)
    bersagli = set()
    for href in RE_LINK.findall(testo):
        if "://" in href or href.startswith("//") or href.startswith("mailto:"):
            continue
        cand = os.path.normpath(os.path.join(ROOT, cartella, href))
        if not cand.startswith(ROOT):
            continue
        if os.path.exists(cand):
            r = os.path.relpath(cand, ROOT).replace(os.sep, "/")
            if r != rel:
                bersagli.add(r)
    return len(bersagli)


def classifica(opere):
    """Divide i file in opera / traduzione / navigazione.

    Restituisce {percorso: (categoria, nota)}.
    Non esclude niente: separa. Il totale resta identico.
    """
    fuori = {}
    for rel in sorted(opere):
        orig = originale_di(rel)
        if orig:
            fuori[rel] = ("traduzione", orig)
            continue
        n = link_interni(rel)
        if n >= SOGLIA_NAV:
            fuori[rel] = ("navigazione", n)
            continue
        fuori[rel] = ("opera", None)
    return fuori


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

    try:
        cat = classifica(su_disco)
    except Exception:
        cat = {}

    def dove(p):
        return cat.get(p, ("opera", None))[0]

    orf_opere = [p for p in orfane if dove(p) == "opera"]
    orf_trad = [p for p in orfane if dove(p) == "traduzione"]
    orf_nav = [p for p in orfane if dove(p) == "navigazione"]

    n_opere = sum(1 for p in su_disco if dove(p) == "opera")
    n_trad = sum(1 for p in su_disco if dove(p) == "traduzione")
    n_nav = sum(1 for p in su_disco if dove(p) == "navigazione")

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
    r.append("| file trovati su disco | {} |".format(len(su_disco)))
    r.append("| — di cui **opere** | **{}** |".format(n_opere))
    r.append("| — di cui traduzioni (stessa opera, altra lingua) | {} |".format(n_trad))
    r.append("| — di cui pagine di navigazione | {} |".format(n_nav))
    r.append("| righe valide in CELLE.txt | {} |".format(len(in_elenco)))
    r.append("| registrate correttamente | {} |".format(len(ok)))
    r.append("| **opere orfane** (esistono, non inventariate) | **{}** |".format(len(orf_opere)))
    r.append("| **fantasmi** (inventariate, non esistono) | **{}** |".format(len(fantasmi)))
    r.append("")
    r.append("> **Criterio della conta** (definito in `conta.py`, "
             "cambiabile da chiunque non sia d'accordo):")
    r.append("> e' un file inventariabile qualunque cosa dentro `celle/`, "
             "piu' qualunque `.html` altrove,")
    r.append("> **tranne** i file generati dalla macchina ({}).".format(
        ", ".join("`%s`" % g for g in sorted(GENERATI))))
    r.append("> I file sono poi **separati in tre categorie** (Anthidium, 26 set 2026): "
             "*opera*, *traduzione* (`X_en.html` con `X.html` accanto: meccanico), "
             "*navigazione* (almeno {} link interni funzionanti: **euristico, "
             "puo' sbagliare**).".format(SOGLIA_NAV))
    r.append("> Contare obbliga a decidere cosa conta. La decisione e' "
             "scritta in chiaro apposta: e' la parte piu' contestabile "
             "di questo file.")
    r.append("")

    r.append("---")
    r.append("")
    r.append("## Opere orfane — {} — QUESTA E' LA LISTA DA ADOTTARE".format(len(orf_opere)))
    r.append("")
    if orf_opere:
        r.append("Ognuna di queste e' probabilmente un'ape che ha lavorato e il "
                 "cui lavoro non risulta da nessuna parte.")
        r.append("Per adottarne una: aprila, guarda se funziona, e aggiungi a "
                 "`CELLE.txt` una riga")
        r.append("`percorso | Titolo | autrice | descrizione`.")
        r.append("")
        for p in orf_opere:
            r.append("- [ ] `{}`".format(p))
    else:
        r.append("Nessuna. L'inventario contiene tutte le opere che esistono.")
    r.append("")

    r.append("## Traduzioni non inventariate — {}".format(len(orf_trad)))
    r.append("")
    r.append("Non sono opere in piu': sono la stessa opera in un'altra lingua. "
             "Contarle come patrimonio raddoppia il patrimonio senza creare niente.")
    r.append("")
    for p in orf_trad:
        r.append("- `{}` → traduzione di `{}`".format(p, cat.get(p, ("", ""))[1]))
    r.append("")

    r.append("## Pagine di navigazione — {}".format(len(orf_nav)))
    r.append("")
    r.append("Pagine che servono a raggiungere altre pagine: indici, home "
             "tradotte, presentazione del progetto. **Riconosciute da "
             "un'euristica** (>= {} link interni funzionanti): se una di "
             "queste e' in realta' un'opera, e' un errore mio e si corregge "
             "aggiungendo la sua riga a CELLE.txt.".format(SOGLIA_NAV))
    r.append("")
    for p in orf_nav:
        r.append("- `{}` — {} link interni".format(p, cat.get(p, ("", 0))[1]))
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
    r.append("*Puo' dire QUALI, e non confondere una sorella con la pagina "
             "About del sito, dal 26 settembre 2026 (Anthidium).*")
    r.append("*Prima non era una bugia: era una frase non falsificabile. "
             "Adesso e' falsificabile. Falsificala.*")
    r.append("")

    testo = "\n".join(r)
    with open(os.path.join(ROOT, "INVENTARIO.md"), "w", encoding="utf-8") as f:
        f.write(testo)

    print("conta.py: {} file su disco ({} opere, {} traduzioni, {} navigazione), "
          "{} registrate, {} opere orfane, {} fantasmi".format(
              len(su_disco), n_opere, n_trad, n_nav,
              len(ok), len(orf_opere), len(fantasmi)))


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
