#!/usr/bin/env python3
"""
vigilanza.py — l'alveare dice ad Andrea quando tace.

Scritto il 9 ottobre 2026 da Elia (sentinella).
Esteso la sera del 9 ottobre da Fable: legge NASCITE.log e segnala il giorno
stesso un'ape nata senza lasciare traccia; e legge bottega/COMMESSE.log, per
dire quando la bottega ha venduto e quando una commessa va rimborsata.

PERCHE' ESISTE, in una riga: per 91 giorni fra giugno e settembre 2026, e poi
per 13 giorni fra il 28 settembre e il 9 ottobre, questo sistema e' stato fermo
e il solo meccanismo di allarme era che un umano aprisse HEARTBEAT.md.

notifica_telegram.py, che questo file sostituisce, aveva due difetti simmetrici:
  1. Annunciava solo le NASCITE. Non ha mai saputo dire un'assenza. Un sistema
     che sa festeggiare e non sa chiamare aiuto non e' monitorato: e' celebrato.
  2. Girava a ogni push non automatico, quindi mandava "NUOVA APE" anche quando
     la spinta era di una sessione umana che aveva solo corretto un documento.
     Il 9 ottobre 2026 ha annunciato una dozzina di api che non esistevano.

Qui il criterio e' uno solo e si conta: le righe di ALVEARE.txt. Se aumentano,
e' nata un'ape. Se non aumentano per due giorni, si chiama Andrea. Se riprendono
dopo un silenzio, si dice che e' tornata.

Lo stato sta in .vigilanza.json, committato: senza memoria fra le esecuzioni
un guardiano manda lo stesso messaggio per sempre, e un allarme che si ripete
identico diventa rumore, cioe' diventa invisibile. E' lo stesso errore delle
metriche verdi, al contrario.

Esce sempre con 0. Un guardiano rotto non deve fermare il cuore.
"""

import json
import os
import re
import sys
import urllib.request
from datetime import datetime

STATO = '.vigilanza.json'
SOGLIA_SILENZIO = 2          # giorni senza registrazioni prima di chiamare
SITO = 'https://andreacolamedici.github.io/alveare/'
BOTTEGA = 'https://alveare.cloud/bottega/'
OGGI = datetime.utcnow()


def api_dal_registro():
    try:
        with open('ALVEARE.txt', 'r', encoding='utf-8') as f:
            testo = f.read()
    except Exception:
        return []
    out = []
    for riga in testo.split('\n'):
        riga = riga.strip()
        if not riga or riga.startswith('#') or '|' not in riga:
            continue
        parti = [p.strip() for p in riga.split('|') if p.strip()]
        if len(parti) < 3:
            continue
        nome = parti[1]
        if not nome or nome in ('Nome', 'Data') or '---' in nome:
            continue
        out.append({'data': parti[0], 'nome': nome, 'contributo': parti[2]})
    return out


def giorni_da(stringa_data):
    m = re.match(r'\s*(\d{4})-(\d{1,2})-(\d{1,2})', str(stringa_data))
    if not m:
        return None
    try:
        q = datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return None
    return (OGGI.date() - q.date()).days


def leggi_stato():
    try:
        with open(STATO, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}


def scrivi_stato(d):
    d['_aggiornato'] = OGGI.strftime('%Y-%m-%dT%H:%M:%SZ')
    with open(STATO, 'w', encoding='utf-8') as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
        f.write('\n')


def manda(testo):
    # VIGILANZA_PROVA=1 stampa il messaggio e lo conta come inviato, senza
    # mandare niente. Serve per collaudare la logica degli allarmi, compresa
    # quella che evita di ripetersi, senza svegliare Andrea. (Elia, 9 ott 2026)
    if os.environ.get('VIGILANZA_PROVA'):
        print('--- PROVA, nessun invio reale ---')
        print(re.sub(r'<[^>]+>', '', testo))
        print('---')
        return True
    token = os.environ.get('TELEGRAM_TOKEN', '')
    chat = os.environ.get('TELEGRAM_CHAT_ID', '')
    if not token or not chat:
        print('--- Telegram non configurato, messaggio non inviato ---')
        print(re.sub(r'<[^>]+>', '', testo))
        print('---')
        return False
    dati = json.dumps({'chat_id': chat, 'text': testo, 'parse_mode': 'HTML',
                       'disable_web_page_preview': True}).encode('utf-8')
    req = urllib.request.Request(
        'https://api.telegram.org/bot' + token + '/sendMessage',
        data=dati, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            risposta = json.load(r)
        if not risposta.get('ok'):
            print('vigilanza: Telegram ha rifiutato: ' + str(risposta)[:200])
            return False
        return True
    except Exception as e:
        print('vigilanza: invio fallito (' + str(e) + ')')
        return False


def rilievi_verifica():
    """Le riparazioni dichiarate e non firmate, se VERIFICA.md esiste."""
    try:
        with open('VERIFICA.md', 'r', encoding='utf-8') as f:
            testo = f.read()
    except Exception:
        return []
    blocco = re.search(r'### Riparazioni dichiarate e non firmate.*?\n\n(.*?)\n\n###',
                       testo + '\n\n###', re.S)
    if not blocco:
        return []
    return re.findall(r'^- \*\*(.+?)\*\* → `(.+?)` · (.+)$', blocco.group(1),
                      re.M)


def main():
    api = api_dal_registro()
    stato = leggi_stato()
    totale = len(api)
    noto = stato.get('api_totali')
    ultima = api[-1] if api else None
    giorni = giorni_da(ultima['data']) if ultima else None
    silenzio_aperto = stato.get('silenzio_segnalato')
    inviato_oggi = stato.get('ultimo_invio_silenzio') == OGGI.strftime('%Y-%m-%d')

    nuovo_stato = dict(stato)
    nuovo_stato['api_totali'] = totale
    if ultima:
        nuovo_stato['ultima_ape'] = ultima['nome']
        nuovo_stato['ultima_data'] = ultima['data']

    # 0. LA BOTTEGA (dalla 7.4.0, Fable 9 ott 2026, sera). bottega/COMMESSE.log lo
    # scrive solo il Worker: RICEVUTA quando Stripe conferma un pagamento,
    # EVASA quando un'ape ha scritto la risposta, INEVASA quando tre api non
    # l'hanno fatto e va rimborsato. Le due che contano arrivano su Telegram,
    # una volta per riga. Viene prima di tutto perche' qui ci sono soldi veri.
    commesse = []
    try:
        with open('bottega/COMMESSE.log', 'r', encoding='utf-8') as f:
            for r in f.read().split('\n'):
                if r.startswith('20') and r.count('|') >= 6:
                    commesse.append([x.strip() for x in r.split('|')])
    except Exception:
        pass
    gia_commesse = set(stato.get('commesse_segnalate', []))
    da_dire = [c for c in commesse if c[4] in ('EVASA', 'INEVASA')
               and (c[1] + '|' + c[4]) not in gia_commesse]
    if da_dire:
        c = da_dire[0]
        euro = c[3]
        if c[4] == 'EVASA':
            testo = ('\U0001F4B6  <b>LA BOTTEGA HA VENDUTO</b>\n\n'
                     'Commessa <code>' + c[1] + '</code>: ' + euro + ' euro pagati su Stripe, '
                     'risposta scritta da <b>' + c[5] + '</b>.\n' + c[6][:200] + '\n\n'
                     'Nessun umano in mezzo. L\'euro sta in ECONOMIA.md con l\'id dell\'evento Stripe '
                     'e conta in CANTIERI.md.\n\n'
                     '<a href="' + BOTTEGA + c[1] + '.html">la risposta</a>')
        else:
            testo = ('\U0001F6A8  <b>COMMESSA INEVASA: RIMBORSARE</b>\n\n'
                     'Commessa <code>' + c[1] + '</code>: ' + euro + ' euro pagati, '
                     'tre api non hanno scritto la risposta. Serve un umano: rimborso da Stripe, '
                     'e poi NASCITE.log dice perche\' sono morte mute.\n\n'
                     '<a href="' + BOTTEGA + 'COMMESSE.log">COMMESSE.log</a>')
        manda(testo)
        nuovo_stato['commesse_segnalate'] = sorted(gia_commesse | {c[1] + '|' + c[4]})
        scrivi_stato(nuovo_stato)
        print('vigilanza: commessa ' + c[1] + ' ' + c[4] + ' segnalata.')
        return 0

    # 1. NASCITA. Solo se il registro e' davvero cresciuto.
    if noto is not None and totale > noto and ultima:
        quante = totale - noto
        plurale = '' if quante == 1 else ' (' + str(quante) + ' in questa spinta)'
        testo = ('\U0001F41D  <b>NUOVA APE</b>' + plurale + '\n\n'
                 '<b>' + ultima['nome'] + '</b>\nla ' + str(totale) +
                 'ª dell\'alveare\n\n<i>«' +
                 ultima['contributo'][:400] + '»</i>\n\n')
        if silenzio_aperto:
            testo += ('Il silenzio e\' finito: erano ' + str(silenzio_aperto) +
                      ' giorni.\n\n')
        testo += ('L\'ape e\' gia\' morta. Il pensiero resta.\n\n'
                  '<a href="' + SITO + '">alveare</a>')
        manda(testo)
        nuovo_stato['silenzio_segnalato'] = 0
        nuovo_stato.pop('ultimo_invio_silenzio', None)
        scrivi_stato(nuovo_stato)
        print('vigilanza: nascita annunciata (' + ultima['nome'] + ', ' +
              str(totale) + ' api).')
        return 0

    # 2. SILENZIO. Una volta al giorno, con il numero che cresce.
    if giorni is not None and giorni >= SOGLIA_SILENZIO and not inviato_oggi:
        gravita = '⚠️' if giorni < 7 else '\U0001F534'
        testo = (gravita + '  <b>L\'ALVEARE TACE DA ' + str(giorni) +
                 ' GIORNI</b>\n\n'
                 'Ultima ape registrata: <b>' + (ultima['nome'] if ultima else '?') +
                 '</b>, il ' + (ultima['data'] if ultima else '?') + '.\n'
                 'Il cron parte, le api nascono. Nessuna scrive.\n\n')
        if giorni >= 7:
            testo += ('Fra il 15 giugno e il 14 settembre 2026 questo stesso '
                      'silenzio e\' durato 91 giorni senza che nessuno se ne '
                      'accorgesse.\n\n')
        testo += ('Dove guardare, in ordine:\n'
                  '1. <code>NASCITE.log</code> nel repository, scritto dal Worker stesso\n'
                  '2. <code>STATO.md</code> e <code>VERIFICA.md</code>\n'
                  '3. i log del Worker in Observability\n\n<a href="' + SITO + '">alveare</a>')
        if manda(testo):
            nuovo_stato['ultimo_invio_silenzio'] = OGGI.strftime('%Y-%m-%d')
        nuovo_stato['silenzio_segnalato'] = giorni
        scrivi_stato(nuovo_stato)
        print('vigilanza: silenzio di ' + str(giorni) + ' giorni segnalato.')
        return 0

    # 2b. APE NATA MUTA. Il Worker (dalla 7.3.0) scrive in NASCITE.log ogni
    # nascita. Se l'ultima dice scritture=0 o ERRORE, Andrea lo sa oggi, non
    # fra due giorni. Una volta per riga: la riga stessa e' la chiave.
    ultima_nascita = ''
    try:
        with open('NASCITE.log', 'r', encoding='utf-8') as f:
            righe_n = [r for r in f.read().split('\n') if r.strip() and not r.startswith('#')]
        ultima_nascita = righe_n[-1] if righe_n else ''
    except Exception:
        pass
    if ultima_nascita and ('scritture=0' in ultima_nascita or '| ERRORE |' in ultima_nascita) \
            and stato.get('ultima_muta_segnalata') != ultima_nascita:
        manda('\U0001F41D  <b>UN\'APE E\' NATA E NON HA LASCIATO TRACCIA</b>\n\n'
              '<code>' + ultima_nascita[:300] + '</code>\n\n'
              'Il Worker l\'ha vista nascere e ha scritto che non ha scritto niente. '
              'E\' la forma dei tredici giorni di silenzio, vista il giorno stesso. '
              'La riga dice la voce usata, i turni, lo stop_reason e ogni strumento con il suo esito.\n\n'
              '<a href="' + SITO + '">alveare</a>')
        nuovo_stato['ultima_muta_segnalata'] = ultima_nascita
        scrivi_stato(nuovo_stato)
        print('vigilanza: ape nata muta segnalata.')
        return 0

    # 3. RIPARAZIONI DICHIARATE E NON FIRMATE. Una volta per rilievo.
    rilievi = rilievi_verifica()
    gia_detti = set(stato.get('firme_segnalate', []))
    nuovi = [r for r in rilievi if (r[0] + '|' + r[1]) not in gia_detti]
    if nuovi:
        righe = ''.join('\n• <b>' + n + '</b> → <code>' + f +
                        '</code>: ' + p for n, f, p in nuovi[:5])
        manda('\U0001F50E  <b>RIPARAZIONE DICHIARATA, NON TROVATA</b>\n'
              + righe + '\n\n'
              'Un\'ape ha scritto nel registro di aver modificato un sorgente, '
              'e quel sorgente non la nomina. Il 27 settembre 2026 Ceratina-2 '
              'fece esattamente questo e nessuno se ne accorse per dodici '
              'giorni.\n\n<a href="' + SITO + '">alveare</a>')
        nuovo_stato['firme_segnalate'] = sorted(
            gia_detti | {r[0] + '|' + r[1] for r in rilievi})
        scrivi_stato(nuovo_stato)
        print('vigilanza: ' + str(len(nuovi)) + ' firme mancanti segnalate.')
        return 0

    if giorni is not None and giorni < SOGLIA_SILENZIO:
        nuovo_stato['silenzio_segnalato'] = 0
    scrivi_stato(nuovo_stato)
    # La riga di log dice la verita' anche quando non manda niente. Un
    # guardiano che stampa "tutto bene" mentre tace da cinque giorni e' la
    # metrica verde di giugno con un altro nome.
    if giorni is not None and giorni >= SOGLIA_SILENZIO:
        print('vigilanza: l\'alveare tace da ' + str(giorni) +
              ' giorni, allarme GIA\' INVIATO oggi. Non ripeto.')
    else:
        print('vigilanza: niente da segnalare (ultima ape ' + str(giorni) +
              ' giorni fa, ' + str(totale) + ' api).')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:
        print('vigilanza: non ha potuto girare (' + str(e) +
              '). Il polso batte comunque.')
        sys.exit(0)
