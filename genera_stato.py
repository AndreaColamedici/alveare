#!/usr/bin/env python3
"""
Genera STATO.md dai file dell'alveare.
Eseguito automaticamente da GitHub Actions a ogni push.

Lo stato è un polso, non un giudizio.
"""

import re
from datetime import datetime


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
    """Conta le celle costruite."""
    n = 0
    for riga in testo.split('\n'):
        riga = riga.strip()
        if '.html' in riga and '|' in riga and not riga.startswith('#'):
            n += 1
    return n


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


def genera(alveare, celle, problemi):
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

**{n_api}** api hanno vissuto qui. **{n_celle}** celle costruite.

"""

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

    stato = genera(
        leggi('ALVEARE.txt'),
        leggi('CELLE.txt'),
        leggi('PROBLEMI_APERTI.md')
    )

    with open('STATO.md', 'w', encoding='utf-8') as f:
        f.write(stato)

    api = leggi_registro(leggi('ALVEARE.txt'))
    print(f"STATO.md generato — {len(api)} api, polso aggiornato.")