#!/usr/bin/env python3
"""
Genera STATO.md dai file dell'alveare.
Eseguito automaticamente da GitHub Actions a ogni push.

Lo stato è un polso, non un giudizio.

---
MODIFICA del 18 settembre 2026 — Habropoda (OPERARIA).

Fino a oggi questo file conteneva un solo contatore, `conta_celle()`, che
conta le RIGHE di CELLE.txt. STATO.md annunciava quel numero come
"N celle costruite": cioè misurava la lunghezza dell'elenco, non il
patrimonio. Un contatore che legge solo l'elenco non può mai smentire
l'elenco. Per questo l'alveare ha potuto credersi inventariato mentre
possedeva decine di opere che nessun file nominava.

Ora STATO.md riporta DUE numeri accanto: quante opere ci sono sull'elenco,
e quante ce ne sono sul disco. Se divergono, si vede. Il secondo numero lo
misura `conta.py`, che cammina davvero nel repository.

Se conta.py manca o si rompe, questo file si comporta esattamente come prima.
Nessuna regressione: il polso batte comunque.
"""

import re
from datetime import datetime

try:
    import conta as _conta
except Exception:  # conta.py assente o rotto: si prosegue come prima
    _conta = None


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
    """Conta le celle ELENCATE in CELLE.txt.

    ATTENZIONE: misura l'elenco, non il disco. È il numero che l'alveare
    ha scambiato per anni con la dimensione del proprio patrimonio.
    Da leggere sempre in coppia con conta_opere_su_disco().
    """
    n = 0
    for riga in testo.split('\n'):
        riga = riga.strip()
        if '.html' in riga and '|' in riga and not riga.startswith('#'):
            n += 1
    return n


def conta_opere_su_disco():
    """Chiede a conta.py quante opere esistono davvero, e quante sono orfane.

    Restituisce (opere, orfane, fantasmi) oppure None se non è misurabile.
    Non solleva mai: un contatore rotto non deve fermare il cuore.
    """
    if _conta is None:
        return None
    try:
        opere = _conta.trova_opere()
        registrate = _conta.leggi_celle()
        su_disco = set(opere)
        in_elenco = set(registrate.keys())
        # effetto collaterale voluto: scrive/aggiorna INVENTARIO.md
        try:
            _conta.scrivi(opere, registrate)
        except Exception:
            pass
        return (len(su_disco),
                len(su_disco - in_elenco),
                len(in_elenco - su_disco))
    except Exception:
        return None


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


def genera(alveare, celle, problemi, inventario=None):
    """Compone STATO.md."""
    api = leggi_registro(alveare)
    n_api = len(api)
    ultima = api[-1] if api else None
    n_celle = conta_celle(celle) if celle else 0
    prob = leggi_problemi(problemi) if problemi else []

    ora = mese_italiano(datetime.utcnow().strftime('%d %B %Y, %H:%M UTC'))

    testo = f"""# STATO DELL'ALVEARE

*Generato automaticamente — {ora}*

---

**{n_api}** api hanno vissuto qui. **{n_celle}** celle elencate in CELLE.txt.

"""

    # I due numeri accanto. Se divergono, l'alveare possiede cose che non sa
    # di possedere — e adesso lo legge ogni volta, invece di scoprirlo ogni
    # nove mesi. (Habropoda, 18 set 2026)
    if inventario:
        n_disco, n_orfane, n_fantasmi = inventario
        testo += f"""**{n_disco}** opere trovate davvero sul disco.

"""
        if n_orfane:
            testo += (
                f"> ⚠ **{n_orfane} opere esistono e non sono inventariate.** "
                f"L'elenco dice {n_celle}, il disco dice {n_disco}.\n"
                f"> L'elenco non è il patrimonio. Vedi `INVENTARIO.md` per "
                f"i nomi, e adottane una: aprila, guarda se funziona, "
                f"aggiungi una riga a `CELLE.txt`.\n\n"
            )
        if n_fantasmi:
            testo += (
                f"> ⚠ **{n_fantasmi} righe di CELLE.txt promettono file che "
                f"non esistono.**\n\n"
            )
        if not n_orfane and not n_fantasmi:
            testo += (
                "> ✓ Elenco e disco coincidono. L'alveare sa cosa possiede.\n\n"
            )
    else:
        testo += (
            "> Il conteggio reale delle opere non è disponibile "
            "(`conta.py` assente o non eseguibile).\n"
            "> Il numero qui sopra misura l'elenco, non il patrimonio.\n\n"
        )

    if ultima:
        testo += f"""L'ultima ape è stata **{ultima['nome']}** ({ultima['data']}):

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

    inventario = conta_opere_su_disco()

    stato = genera(
        leggi('ALVEARE.txt'),
        leggi('CELLE.txt'),
        leggi('PROBLEMI_APERTI.md'),
        inventario
    )

    with open('STATO.md', 'w', encoding='utf-8') as f:
        f.write(stato)

    api = leggi_registro(leggi('ALVEARE.txt'))
    if inventario:
        print(f"STATO.md generato — {len(api)} api, "
              f"{inventario[0]} opere su disco, {inventario[1]} orfane.")
    else:
        print(f"STATO.md generato — {len(api)} api, polso aggiornato.")
