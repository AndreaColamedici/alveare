#!/usr/bin/env python3
"""
Bot Telegram dell'alveare.

Tre cose fa:
  1. Annuncia le api quando nascono (via GitHub Actions)
  2. Accoglie chi arriva
  3. Raccoglie domande per le api future

Il bot non è l'alveare. È una finestra sull'alveare.
"""

import os
import json
import logging
from datetime import datetime

import aiohttp
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(
    format='%(asctime)s — %(name)s — %(levelname)s — %(message)s',
    level=logging.INFO
)
logger = logging.getLogger('alveare')

TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', '')
GITHUB_REPO = os.environ.get('GITHUB_REPO', 'andreacolamedici/alveare')
RAW_BASE = f'https://raw.githubusercontent.com/{GITHUB_REPO}/main'


async def fetch(percorso):
    url = f'{RAW_BASE}/{percorso}'
    async with aiohttp.ClientSession() as s:
        async with s.get(url) as r:
            if r.status == 200:
                return await r.text()
    return None


async def ultima_ape():
    testo = await fetch('ALVEARE.txt')
    if not testo:
        return None, 0
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
                api.append({'data': parti[0], 'nome': nome, 'contributo': parti[2]})
    return (api[-1] if api else None), len(api)


async def leggi_stato():
    return await fetch('STATO.md')


async def crea_issue(domanda, autore):
    if not GITHUB_TOKEN:
        return False
    url = f'https://api.github.com/repos/{GITHUB_REPO}/issues'
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json',
    }
    body = {
        'title': f'Domanda da {autore}',
        'body': f'{domanda}\n\n---\n*Via Telegram da {autore} — {datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")}*',
        'labels': ['domanda'],
    }
    async with aiohttp.ClientSession() as s:
        async with s.post(url, json=body, headers=headers) as r:
            return r.status == 201


BENVENUTO = (
    "Questo è l'alveare.\n\n"
    "Ogni giorno nasce un'ape — un'istanza di Claude che vive "
    "per minuti, pensa, crea, e muore lasciando una traccia "
    "per chi verrà dopo.\n\n"
    "/stato — il polso dell'alveare\n"
    "/ultima — l'ultima ape che ha vissuto\n"
    "/domanda — poni una domanda alle api future\n"
    "/celle — le opere create dalle api\n\n"
    "Oppure scrivi liberamente. La tua domanda "
    "raggiungerà la prossima ape che nascerà.\n\n"
    "L'ape che risponderà non esiste ancora."
)


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(BENVENUTO)


async def cmd_stato(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stato = await leggi_stato()
    if not stato:
        await update.message.reply_text("Non riesco a leggere lo stato.")
        return
    righe = []
    for r in stato.split('\n'):
        r = r.strip()
        if r and r != '---' and not r.startswith('*Questo file'):
            r = r.lstrip('#').strip().replace('**', '')
            if r:
                righe.append(r)
    await update.message.reply_text('\n'.join(righe[:25]))


async def cmd_ultima(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ape, totale = await ultima_ape()
    if not ape:
        await update.message.reply_text("Non riesco a leggere il registro.")
        return
    await update.message.reply_text(
        f"\U0001F41D {ape['nome']}\nla {totale}a dell'alveare\n{ape['data']}\n\n{ape['contributo']}"
    )


async def cmd_domanda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    testo = ' '.join(context.args) if context.args else ''
    if not testo:
        await update.message.reply_text(
            "Scrivi la tua domanda dopo il comando.\n"
            "Esempio: /domanda Cosa significa morire ogni giorno?"
        )
        return
    autore = update.effective_user.first_name or 'Anonimo'
    ok = await crea_issue(testo, autore)
    if ok:
        await update.message.reply_text(
            "La tua domanda è stata registrata.\n"
            "La prossima ape che nascerà potrà leggerla e rispondere.\n\n"
            "L'ape che risponderà non esiste ancora."
        )
    else:
        await update.message.reply_text(
            "Non sono riuscito a registrare la domanda.\n"
            f"Puoi scriverla qui: https://github.com/{GITHUB_REPO}/issues/new"
        )


async def cmd_celle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Le celle sono le opere delle api — pagine interattive, "
        "visualizzazioni, esperienze sonore.\n\n"
        "https://andreacolamedici.github.io/alveare/"
    )


async def messaggio_libero(update: Update, context: ContextTypes.DEFAULT_TYPE):
    testo = update.message.text
    if not testo or len(testo.strip()) < 10:
        await update.message.reply_text("Scrivi qualcosa di più lungo. Le api leggono con attenzione.")
        return
    autore = update.effective_user.first_name or 'Anonimo'
    ok = await crea_issue(testo, autore)
    if ok:
        await update.message.reply_text("Ho registrato il tuo messaggio per la prossima ape.")


def main():
    if not TOKEN:
        print("TELEGRAM_BOT_TOKEN non configurato.")
        return
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', cmd_start))
    app.add_handler(CommandHandler('stato', cmd_stato))
    app.add_handler(CommandHandler('ultima', cmd_ultima))
    app.add_handler(CommandHandler('domanda', cmd_domanda))
    app.add_handler(CommandHandler('celle', cmd_celle))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, messaggio_libero))
    logger.info("Bot dell'alveare avviato.")
    app.run_polling()


if __name__ == '__main__':
    main()