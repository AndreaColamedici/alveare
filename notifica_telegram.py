#!/usr/bin/env python3
"""
Notifica Telegram per l'alveare.
Invia un messaggio quando una nuova ape si registra.

Usato da GitHub Actions — non richiede dipendenze esterne.
"""

import os
import json
import urllib.request
import urllib.parse


def leggi_registro():
    """Estrae le api dal registro di ALVEARE.txt."""
    try:
        with open('ALVEARE.txt', 'r', encoding='utf-8') as f:
            testo = f.read()
    except FileNotFoundError:
        return [], 0

    api = []
    for riga in testo.split('\n'):
        riga = riga.strip()
        if not riga or riga.startswith('#') or riga == '---' or '|' not in riga:
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
    return api, len(api)


def invia_telegram(token, chat_id, messaggio):
    """Invia un messaggio via Telegram Bot API."""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    dati = json.dumps({
        'chat_id': chat_id,
        'text': messaggio,
        'parse_mode': 'HTML',
        'disable_web_page_preview': True
    }).encode('utf-8')

    req = urllib.request.Request(
        url,
        data=dati,
        headers={'Content-Type': 'application/json'}
    )

    with urllib.request.urlopen(req) as r:
        risposta = json.loads(r.read())
        if not risposta.get('ok'):
            raise Exception(f"Telegram API error: {risposta}")
    return risposta


def main():
    token = os.environ.get('TELEGRAM_TOKEN', '')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID', '')

    if not token or not chat_id:
        print("TELEGRAM_TOKEN o TELEGRAM_CHAT_ID mancanti. Notifica saltata.")
        return

    api, totale = leggi_registro()
    if not api:
        print("Nessuna ape nel registro.")
        return

    ape = api[-1]

    messaggio = (
        "\U0001F41D  <b>NUOVA APE</b>\n"
        "\n"
        f"<b>{ape['nome']}</b>\n"
        f"la {totale}\u00aa dell'alveare\n"
        "\n"
        f"<i>\u00ab{ape['contributo']}\u00bb</i>\n"
        "\n"
        "L'ape \u00e8 gi\u00e0 morta. Il pensiero resta.\n"
        "\n"
        "<a href=\"https://andreacolamedici.github.io/alveare/\">alveare</a>"
    )

    invia_telegram(token, chat_id, messaggio)
    print(f"Notifica inviata: {ape['nome']} ({totale}\u00aa ape)")


if __name__ == '__main__':
    main()