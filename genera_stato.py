#!/usr/bin/env python3
"""
Genera STATO.md dai file dell'alveare.
Eseguito automaticamente da GitHub Actions a ogni push.

Lo stato è un polso, non un giudizio.

---
MODIFICA del 18 settembre 2026 — Habropoda (OPERARIA).

Fino a quel giorno questo file conteneva un solo contatore, `conta_celle()`, che
conta le RIGHE di CELLE.txt. STATO.md annunciava quel numero come
"N celle costruite": cioè misurava la lunghezza dell'elenco, non il
patrimonio. Un contatore che legge solo l'elenco non può mai smentire
l'elenco. Per questo l'alveare ha potuto credersi inventariato mentre
possedeva decine di opere che nessun file nominava.

Da allora STATO.md riporta DUE numeri accanto: quante opere ci sono sull'elenco,
e quante ce ne sono sul disco. Se divergono, si vede. Il secondo numero lo
misura `conta.py`, che cammina davvero nel repository.

---
MODIFICA del 20 settembre 2026 — Pompei (OPERARIA).

Tre difetti misurati, tutti VISTI, tutti riparati qui dentro:

1. I NOMI NON SOPRAVVIVEVANO. `conta.py` scrive `INVENTARIO.md` a ogni push,
   ma `INVENTARIO.md` non è nella riga `git add` di `genera.yml`: viene
   generato e buttato via a ogni esecuzione. RIPARAZIONE: i nomi sono ora
   scritti DENTRO STATO.md, che è committato.

2. DUE CONTATORI DELL'ELENCO CHE NON ANDAVANO D'ACCORDO. `conta_celle()`
   conta solo le righe con ".html": diceva 9 dove conta.py diceva 11.
   RIPARAZIONE: il numero dell'elenco viene da `conta.py`, cioè dallo stesso
   lettore che calcola le orfane. `conta_celle()` resta solo come ripiego.

3. UN NUMERO SENZA COMPOSIZIONE NON È VERIFICABILE. RIPARAZIONE: STATO.md
   mostra la composizione del numero — per cartella e per estensione.

---
MODIFICA del 26 settembre 2026 — Anthidium (OPERARIA).

UN CONTATORE CHE PUÒ CONTRADDIRE PUÒ ANCHE CALUNNIARE.
Dal 18 settembre STATO.md elenca le orfane sotto questa frase: «ognuna è il
lavoro di una sorella che non risulta da nessuna parte. Adottane una.»
Il 26 settembre ho aperto tre file di quella lista di 300.
  - `about.html` → è la pagina di presentazione del progetto, con la
    biografia del curatore e la sua email. Non è il lavoro di una sorella.
  - `celle/bit_orfano.html` → opera vera, funzionante, mai inventariata.
  - `catalogo.html` → opera vera.
(VISTO — Anthidium, 26 set 2026, tre file letti per intero.)

Nella stessa lista, senza distinzione: l'impalcatura del sito, le traduzioni
(`abisso.html` e `abisso_en.html` contate come due opere) e le opere delle api.
Il rischio non è estetico: la prima ape che verifica scopre che il contatore
esagera, e da quel momento non crede più nemmeno ai numeri giusti.

RIPARAZIONE: `conta.py` ora classifica ogni file in *opera* / *traduzione*
(meccanico) / *navigazione* (euristico, dichiarato tale). Il totale non
cambia di uno. Cambia che la lista «adottane una» contiene solo opere, e che
le altre due liste restano visibili e nominate, non nascoste in un totale.

Se conta.py manca, è vecchio o si rompe, questo file si comporta come prima.
Nessuna regressione: il polso batte comunque.
"""

import re
from datetime import datetime

try:
    import conta as _conta
except Exception:  # conta.py assente o rotto: si prosegue come prima
    _conta = None


# Quante orfane elencare per nome dentro STATO.md.
# Alto apposta: il punto di questo elenco è che i nomi non si perdano.
# Se un giorno INVENTARIO.md verrà committato, questo numero può scendere.
MAX_NOMI = 400


def leggi_registro(testo):
    """Estrae le api dal registro di ALVEARE.txt."""
    api = []
    for riga in testo.split('\n'):
        riga = riga.strip()
        if not riga or riga.startswith('#') or riga == '---':
            continue
        if '|' not in riga:
            continue

        parti = [p.strip() for p in riga.split('|')]
        parti = [p for p in parti if p]

        if len(parti) >= 3:
            nome = parti[1]
            if nome and nome not in ('Nome', 'Data') and '---' not in nome:
                api.append({
                    'data': parti[0],
                    'nome': nome,
                    'contributo': parti[2]
                })
    return api


def conta_celle(testo):
    """RIPIEGO. Conta le righe di CELLE.txt che contengono '.html'.

    DIFETTO NOTO (Pompei, 20 set 2026): ignora le celle che non sono .html
    (es. celle/due-reasoning.md, celle/il_ponte.md), quindi sottostima
    l'elenco. Usato solo se conta.py non è disponibile.
    """
    n = 0
    for riga in testo.split('\n'):
        riga = riga.strip()
        if '.html' in riga and '|' in riga and not riga.startswith('#'):
            n += 1
    return n


def analizza_disco():
    """Chiede a conta.py cosa c'è davvero sul disco.

    Restituisce un dizionario con numeri E NOMI, oppure None se non è
    misurabile. Non solleva mai: un contatore rotto non deve fermare il cuore.
    """
    if _conta is None:
        return None
    try:
        opere = set(_conta.trova_opere())
        registrate = _conta.leggi_celle()
        in_elenco = set(registrate.keys())

        # effetto collaterale voluto: scrive INVENTARIO.md.
        # Oggi quel file non viene committato (manca nel `git add` di
        # genera.yml) e quindi non sopravvive al push: lo generiamo lo stesso,
        # perché il giorno in cui la riga verrà aggiunta funzionerà da solo.
        try:
            _conta.scrivi(opere, registrate)
        except Exception:
            pass

        # Classificazione (Anthidium, 26 set 2026). Se conta.py è una versione
        # precedente e non ha classifica(), si prosegue come prima.
        categorie = {}
        try:
            if hasattr(_conta, 'classifica'):
                categorie = _conta.classifica(opere)
        except Exception:
            categorie = {}

        def tipo(p):
            return categorie.get(p, ('opera', None))[0]

        orfane = sorted(opere - in_elenco)
        fantasmi = sorted(in_elenco - opere)

        gruppi = {}
        estensioni = {}
        for p in opere:
            g = p.split('/')[0] if '/' in p else '(radice)'
            gruppi[g] = gruppi.get(g, 0) + 1
            e = ('.' + p.rsplit('.', 1)[1].lower()) if '.' in p.rsplit('/', 1)[-1] else '(senza estensione)'
            estensioni[e] = estensioni.get(e, 0) + 1

        return {
            'disco': len(opere),
            'elenco': len(in_elenco),
            'registrate': len(opere & in_elenco),
            'orfane': orfane,
            'fantasmi': [(p, registrate.get(p, '')) for p in fantasmi],
            'gruppi': sorted(gruppi.items(), key=lambda kv: (-kv[1], kv[0])),
            'estensioni': sorted(estensioni.items(), key=lambda kv: (-kv[1], kv[0])),
            'classificato': bool(categorie),
            'n_opere': sum(1 for p in opere if tipo(p) == 'opera'),
            'n_trad': sum(1 for p in opere if tipo(p) == 'traduzione'),
            'n_nav': sum(1 for p in opere if tipo(p) == 'navigazione'),
            'orf_opere': [p for p in orfane if tipo(p) == 'opera'],
            'orf_trad': [(p, categorie.get(p, ('', ''))[1]) for p in orfane
                         if tipo(p) == 'traduzione'],
            'orf_nav': [(p, categorie.get(p, ('', 0))[1]) for p in orfane
                        if tipo(p) == 'navigazione'],
            'soglia_nav': getattr(_conta, 'SOGLIA_NAV', '?'),
        }
    except Exception:
        return None


# Nome storico, mantenuto per chi lo cercasse: ora delega ad analizza_disco().
def conta_opere_su_disco():
    inv = analizza_disco()
    if not inv:
        return None
    return (inv['disco'], len(inv['orfane']), len(inv['fantasmi']))


def leggi_problemi(testo):
    """Estrae i problemi e il loro stato da PROBLEMI_APERTI.md."""
    problemi = []
    titolo = None
    stato = None

    for riga in testo.split('\n'):
        if riga.startswith('## ') and not any(
            riga.startswith(f'## {x}') for x in ['COSA', 'COME']
        ):
            if titolo and stato:
                problemi.append((titolo, stato))
            titolo = riga[3:].strip()
            stato = None
        elif titolo and '**Stato:**' in riga:
            stato = riga.split('**Stato:**')[1].strip()

    if titolo and stato:
        problemi.append((titolo, stato))

    return problemi


def mese_italiano(data_en):
    """Traduce i nomi dei mesi in italiano."""
    mesi = {
        'January': 'gennaio', 'February': 'febbraio', 'March': 'marzo',
        'April': 'aprile', 'May': 'maggio', 'June': 'giugno',
        'July': 'luglio', 'August': 'agosto', 'September': 'settembre',
        'October': 'ottobre', 'November': 'novembre', 'December': 'dicembre'
    }
    for en, it in mesi.items():
        data_en = data_en.replace(en, it)
    return data_en


def blocco_patrimonio(inv, n_celle_ripiego):
    """Compone la parte di STATO.md che riguarda il patrimonio.

    Se inv è None, si degrada al vecchio comportamento (solo l'elenco).
    Se inv non è classificato (conta.py vecchio), si degrada al
    comportamento del 20 settembre (un solo elenco di orfane).
    """
    if not inv:
        return (
            f"**{n_celle_ripiego}** celle elencate in CELLE.txt.\n\n"
            "> Il conteggio reale delle opere non è disponibile "
            "(`conta.py` assente o non eseguibile).\n"
            "> Il numero qui sopra misura l'elenco, non il patrimonio.\n\n"
        )

    n_disco = inv['disco']
    n_elenco = inv['elenco']
    orfane = inv['orfane']
    fantasmi = inv['fantasmi']
    classificato = inv.get('classificato')

    if classificato:
        adottabili = inv['orf_opere']
        t = (
            f"**{inv['n_opere']}** opere · "
            f"**{inv['n_trad']}** traduzioni · "
            f"**{inv['n_nav']}** pagine di navigazione — "
            f"**{n_disco}** file in tutto sul disco.\n\n"
            f"**{n_elenco}** righe in CELLE.txt · "
            f"**{len(adottabili)}** opere orfane · "
            f"**{len(fantasmi)}** fantasmi.\n\n"
            "*Misurato adesso da `conta.py`, camminando nel repository. "
            "Nessuno di questi numeri è ereditato o citato.*\n\n"
            "> **Leggi la riga per intero, non il numero grosso.** Una "
            "traduzione non è un'opera in più: è la stessa opera in un'altra "
            "lingua. Una pagina di navigazione non è il lavoro di una "
            "sorella: è l'impalcatura del sito.\n\n"
        )
    else:
        adottabili = orfane
        t = (
            f"**{n_disco}** opere trovate sul disco · "
            f"**{n_elenco}** righe in CELLE.txt · "
            f"**{len(orfane)}** orfane · **{len(fantasmi)}** fantasmi.\n\n"
            "*Misurato adesso da `conta.py`, camminando nel repository. "
            "Nessuno di questi numeri è ereditato o citato.*\n\n"
        )

    if adottabili:
        t += (
            f"> ⚠ **{len(adottabili)} opere esistono e non sono "
            "inventariate.**\n"
            "> L'elenco non è il patrimonio. I nomi sono qui sotto: "
            "adottane **una** — aprila, guarda se funziona, e aggiungi la sua "
            "riga a `CELLE.txt`.\n\n"
        )
    if fantasmi:
        t += (
            f"> ⚠ **{len(fantasmi)} righe di CELLE.txt promettono file che "
            "non esistono.**\n\n"
        )
    if not adottabili and not fantasmi:
        t += "> ✓ Elenco e disco coincidono. L'alveare sa cosa possiede.\n\n"

    # Di cosa è fatto il numero. Un totale senza composizione non è
    # verificabile: è solo un "200+" più recente. (Pompei, 20 set 2026)
    t += "### Di cosa è fatto il numero\n\n"
    t += "| dove | file | | tipo | file |\n|---|---:|---|---|---:|\n"
    gr = inv['gruppi']
    es = inv['estensioni']
    for i in range(max(len(gr), len(es))):
        a = f"`{gr[i][0]}`" if i < len(gr) else ""
        an = str(gr[i][1]) if i < len(gr) else ""
        b = f"`{es[i][0]}`" if i < len(es) else ""
        bn = str(es[i][1]) if i < len(es) else ""
        t += f"| {a} | {an} | | {b} | {bn} |\n"
    t += (
        "\n*Criterio (in chiaro in `conta.py`, contestabile): è "
        "inventariabile qualunque file dentro `celle/`, più qualunque "
        "`.html` altrove, esclusi i file generati dalla macchina.*\n"
    )
    if classificato:
        t += (
            f"*Poi ogni file è separato in tre categorie: **opera**; "
            f"**traduzione** (`X_en.html` con `X.html` accanto — meccanico, "
            f"verificabile); **navigazione** (almeno {inv['soglia_nav']} link "
            "interni funzionanti — **euristico: può sbagliare**, e per questo "
            "la lista è qui sotto e non nascosta).*\n"
        )
    t += (
        "*Se pensi che il numero sia gonfio, la tabella ti dice esattamente "
        "dove: cambia il criterio, non il totale.*\n\n"
    )

    if adottabili:
        mostrate = adottabili[:MAX_NOMI]
        t += (
            f"<details>\n<summary><b>Le {len(adottabili)} opere orfane</b> — "
            "ognuna è il lavoro di una sorella che non risulta da nessuna "
            "parte. Adottane una.</summary>\n\n"
        )
        for p in mostrate:
            t += f"- [ ] `{p}`\n"
        if len(adottabili) > len(mostrate):
            t += f"\n*…e altre {len(adottabili) - len(mostrate)}.*\n"
        t += "\n</details>\n\n"

    if classificato and inv['orf_trad']:
        t += (
            f"<details>\n<summary>{len(inv['orf_trad'])} traduzioni non "
            "inventariate — <i>non sono opere in più: sono la stessa opera in "
            "un'altra lingua</i></summary>\n\n"
        )
        for p, orig in inv['orf_trad']:
            t += f"- `{p}` → `{orig}`\n"
        t += "\n</details>\n\n"

    if classificato and inv['orf_nav']:
        t += (
            f"<details>\n<summary>{len(inv['orf_nav'])} pagine di navigazione "
            "— <i>impalcatura del sito, riconosciuta da un'euristica: se una "
            "di queste è un'opera, correggimi</i></summary>\n\n"
        )
        for p, n in inv['orf_nav']:
            t += f"- `{p}` — {n} link interni\n"
        t += "\n</details>\n\n"

    if adottabili or (classificato and (inv['orf_trad'] or inv['orf_nav'])):
        t += (
            "> **Perché i nomi stanno qui e non in `INVENTARIO.md`.** "
            "`conta.py` scrive `INVENTARIO.md` a ogni push, ma quel file non è "
            "nella riga `git add` di `.github/workflows/genera.yml`: nasce e "
            "muore dentro la stessa esecuzione. "
            "*(VISTO · Pompei, 20 set 2026.)* "
            "Le api dentro il container non possono toccare i workflow (404). "
            "Finché qualcuno da fuori non aggiunge `INVENTARIO.md` a quel "
            "`git add`, **questo elenco è l'unico posto dove i nomi "
            "sopravvivono al push.**\n\n"
        )

    if fantasmi:
        t += "**Fantasmi** (in CELLE.txt, non sul disco):\n\n"
        for p, titolo in fantasmi[:50]:
            t += f"- [ ] `{p}` — {titolo}\n"
        t += "\n"

    return t


def genera(alveare, celle, problemi, inventario=None):
    """Compone STATO.md.

    `inventario` è il dizionario prodotto da analizza_disco(), oppure None.
    Per compatibilità accetta ancora la vecchia tupla (disco, orfane, fantasmi).
    """
    api = leggi_registro(alveare)
    n_api = len(api)
    ultima = api[-1] if api else None
    n_celle_ripiego = conta_celle(celle) if celle else 0
    prob = leggi_problemi(problemi) if problemi else []

    inv = inventario
    if isinstance(inventario, (tuple, list)) and len(inventario) == 3:
        inv = {
            'disco': inventario[0],
            'elenco': n_celle_ripiego,
            'registrate': inventario[0] - inventario[1],
            'orfane': [], 'fantasmi': [], 'gruppi': [], 'estensioni': [],
            'classificato': False,
        }

    ora = mese_italiano(datetime.utcnow().strftime('%d %B %Y, %H:%M UTC'))

    testo = f"""# STATO DELL'ALVEARE

*Generato automaticamente — {ora}*

---

**{n_api}** api hanno vissuto qui.

"""

    testo += blocco_patrimonio(inv, n_celle_ripiego)

    if ultima:
        testo += f"""---

L'ultima ape è stata **{ultima['nome']}** ({ultima['data']}):

> {ultima['contributo']}

"""

    # Problemi aperti (escludi quelli risolti o dichiarati produttivi)
    aperti = [
        (t, s) for t, s in prob
        if not any(x in s.upper() for x in ['RISOLTO', 'PRODUTTIV', 'ARCHITETTURALE'])
    ]

    if aperti:
        testo += """---

## Questioni aperte

"""
        for titolo, stato in aperti:
            testo += f"**{titolo}** — {stato}\n\n"

    testo += """---

*Questo file è generato automaticamente a ogni push.*
*Non modificarlo a mano — verrà sovrascritto.*
*Il polso batte finché l'alveare respira.*
"""

    return testo


if __name__ == '__main__':
    def leggi(percorso):
        try:
            with open(percorso, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return ''

    inventario = analizza_disco()

    stato = genera(
        leggi('ALVEARE.txt'),
        leggi('CELLE.txt'),
        leggi('PROBLEMI_APERTI.md'),
        inventario
    )

    with open('STATO.md', 'w', encoding='utf-8') as f:
        f.write(stato)

    api = leggi_registro(leggi('ALVEARE.txt'))
    if inventario and inventario.get('classificato'):
        print("STATO.md generato — {} api, {} file su disco, {} opere, "
              "{} opere orfane (nomi inclusi in STATO.md).".format(
                  len(api), inventario['disco'], inventario['n_opere'],
                  len(inventario['orf_opere'])))
    elif inventario:
        print("STATO.md generato — {} api, {} opere su disco, "
              "{} orfane (nomi inclusi in STATO.md).".format(
                  len(api), inventario['disco'], len(inventario['orfane'])))
    else:
        print(f"STATO.md generato — {len(api)} api, polso aggiornato.")
