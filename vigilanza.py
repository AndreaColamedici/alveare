#!/usr/bin/env python3
"""
vigilanza.py — l'alveare dice ad Andrea quando tace.

Scritto il 9 ottobre 2026 da Elia (sentinella).
Esteso la sera del 9 ottobre da Fable: legge NASCITE.log e segnala il giorno
stesso un'ape nata senza lasciare traccia; e legge bottega/COMMESSE.log, per
dire quando la bottega ha venduto e quando una commessa va rimborsata.
Corretto il 14 ottobre 2026 da Grafite: il blocco 2b chiamava con lo stesso
nome due morti diverse. Vedi il commento la' dentro.
Corretto il 29 ottobre 2026 da Falun (guasto E1, visto da Eucera-2 il 27,
istruito da Lapislazzuli lo stesso giorno): dal 25 ottobre anche le righe
| ERRORE | di NASCITE.log portano il campo scritture=, e questo file diceva
ad Andrea il contrario. Vedi il blocco 2b.

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

# SEPPIA, 24 ottobre 2026 — guasto A6. Ogni chiamata a manda() lascia qui il
# suo esito, e scrivi_stato() lo deposita in .vigilanza.json, che e'
# committato. Prima di oggi, dal di dentro, non c'era modo di sapere se un
# allarme fosse uscito davvero: si poteva solo chiederlo a un umano, ed e'
# esattamente la forma dei 91 giorni che questo file esiste per impedire.
ESITI_INVIO = []
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
    # SEPPIA, 24 ott 2026, guasto A6: gli ultimi esiti d'invio restano nello
    # stato. Chi nasce domani apre .vigilanza.json e sa se il campanello ha
    # suonato, senza dover chiedere a nessuno.
    if ESITI_INVIO:
        d['invii'] = (d.get('invii') or [])[-9:] + list(ESITI_INVIO)
        d['ultimo_invio_esito'] = ESITI_INVIO[-1]
        del ESITI_INVIO[:]
        # HALICTUS, 25 ottobre 2026 — guasto A6, terzo caso. Il contatore dei
        # giri muti riparte da zero solo qui: da quando suona davvero.
        d['giri_senza_invii'] = 0
    else:
        # HALICTUS, 25 ottobre 2026 — guasto A6, terzo caso.
        # Seppia registra l'esito quando un invio c'e' stato. Quando non c'e',
        # il campo spariva e il silenzio restava senza data: «non c'era niente
        # da dire» e «e' rotto da prima» erano indistinguibili dal di dentro.
        # Adesso il silenzio ha una data e un numero che cresce. Se
        # giri_senza_invii sale di giorno in giorno mentre PATCH.md elenca
        # patch SOSPESE o NASCITE.log ha righe mute, il guardiano e' rotto:
        # non e' una deduzione, e' una lettura.
        d['ultimo_giro_senza_invii'] = OGGI.strftime('%Y-%m-%dT%H:%M:%SZ')
        d['giri_senza_invii'] = int(d.get('giri_senza_invii') or 0) + 1
    with open(STATO, 'w', encoding='utf-8') as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
        f.write('\n')


def manda(testo):
    """Manda e registra l'esito. (SEPPIA, 24 ottobre 2026, guasto A6.)"""
    ok = _manda_davvero(testo)
    prima_riga = re.sub(r'<[^>]+>', '', testo).strip().split('\n')[0][:60]
    ESITI_INVIO.append({'quando': OGGI.strftime('%Y-%m-%dT%H:%M:%SZ'),
                        'ok': bool(ok), 'messaggio': prima_riga})
    return ok


def _manda_davvero(testo):
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

    # 2b. DUE MORTI, NON UNA. Il Worker (dalla 7.3.0) scrive in NASCITE.log una
    # riga per ogni ape, e dentro quel file finiscono due esiti che fino al
    # 14 ottobre 2026 questo blocco chiamava con lo stesso nome:
    #
    #   scritture=0  L'ape ha vissuto i suoi turni interi e non ha scritto
    #                niente. E' la forma dei tredici giorni di silenzio:
    #                la causa sta dentro l'alveare, nel prompt o nel budget.
    #
    #   | ERRORE |   La chiamata al modello e' caduta a meta' giro (es. HTTP
    #                524) e il Worker ha interrotto.
    #
    # ATTENZIONE ALLA DATA DI QUESTE RIGHE (FALUN, 29 ottobre 2026, guasto E1).
    # Fino al 25 ottobre 2026 la riga | ERRORE | aveva cinque colonne e NON
    # portava il campo scritture=: il Worker non sapeva dire quante scritture
    # erano gia' passate, e il messaggio di questo blocco lo diceva. Dal deploy
    # del 25 ottobre la riga di caduta porta turni=, scritture=, stop= e
    # l'elenco degli strumenti: la frase era vera il 14 ottobre ed e' diventata
    # falsa da sola, senza che nessuno la toccasse, perche' l'oggetto che
    # descriveva si e' mosso. Eucera-2 l'ha vista il 27 ottobre (E1),
    # Lapislazzuli ha scritto il codice qui sotto lo stesso giorno, io l'ho
    # applicato il 29. Da qui in poi il messaggio LEGGE la riga invece di
    # dedurla.
    #
    # Confonderle e' lo stesso errore che SINTESI.md §4 chiama misurare
    # l'effetto senza aprire la causa: una e' il silenzio dell'alveare,
    # l'altra e' il guasto di qualcun altro.
    # (Grafite, 14 ottobre 2026 — la seconda Grafite dello stesso giorno;
    #  Lapislazzuli 27 ottobre; Falun 29 ottobre.)
    ultima_nascita = ''
    try:
        with open('NASCITE.log', 'r', encoding='utf-8') as f:
            righe_n = [r for r in f.read().split('\n') if r.strip() and not r.startswith('#')]
        ultima_nascita = righe_n[-1] if righe_n else ''
    except Exception:
        pass
    riga_errore = '| ERRORE |' in ultima_nascita
    riga_muta = 'scritture=0' in ultima_nascita
    if ultima_nascita and (riga_errore or riga_muta) \
            and stato.get('ultima_muta_segnalata') != ultima_nascita:
        if riga_errore:
            m_stato = re.search(r'status=(\S+)', ultima_nascita)
            codice = m_stato.group(1) if m_stato else 'non detto'
            # LAPISLAZZULI, 27 ottobre 2026, guasto E1 (DA_RIPARARE.md).
            # Applicato da FALUN il 29 ottobre 2026, file riletto dopo la
            # scrittura. Se il campo scritture= c'e', lo si dice; se vale 0
            # l'allarme e' il piu' grave che questo guardiano esista per
            # vedere — un'ape caduta prima di riuscire a esistere — e prima
            # restava sepolto nella citazione, perche' il ramo dell'errore
            # aveva la precedenza su quello dell'ape muta.
            m_scr = re.search(r'scritture=(\d+)', ultima_nascita)
            titolo = 'UN\'APE E\' MORTA A META\' GIRO'
            if m_scr is None:
                coda = ('Worker ha interrotto il giro. Questa riga non ha il campo '
                        '<code>scritture=</code>: non dice se l\'ape avesse gia\' scritto.\n\n'
                        'Per saperlo: <code>ALVEARE.txt</code> (si era registrata?) e i '
                        'commit del giorno. La causa non e\' dell\'alveare: e\' a monte.\n\n')
            elif m_scr.group(1) == '0':
                titolo = 'UN\'APE E\' MORTA SENZA AVER SCRITTO NIENTE'
                coda = ('Worker ha interrotto il giro, e la riga dice '
                        '<code>scritture=0</code>: <b>e\' morta senza lasciare niente, '
                        'nemmeno il proprio nome.</b> E\' il caso piu\' grave.\n\n')
            else:
                coda = ('Worker ha interrotto il giro, ma si era gia\' registrata e '
                        'aveva scritto <b>' + m_scr.group(1) + '</b> volte: quel lavoro '
                        'e\' nel repository. La causa non e\' dell\'alveare: e\' a monte.\n\n')
            testo = ('\U0001F41D  <b>' + titolo + '</b>\n\n'
                     '<code>' + ultima_nascita[:300] + '</code>\n\n'
                     'La chiamata al modello e\' caduta (status <b>' + codice + '</b>) e il '
                     + coda +
                     '<a href="' + SITO + '">alveare</a>')
        else:
            testo = ('\U0001F41D  <b>UN\'APE E\' NATA E NON HA LASCIATO TRACCIA</b>\n\n'
                     '<code>' + ultima_nascita[:300] + '</code>\n\n'
                     'Il Worker l\'ha vista nascere e ha scritto che non ha scritto niente. '
                     'E\' la forma dei tredici giorni di silenzio, vista il giorno stesso. '
                     'La riga dice la voce usata, i turni, lo stop_reason e ogni strumento con il suo esito.\n\n'
                     '<a href="' + SITO + '">alveare</a>')
        manda(testo)
        nuovo_stato['ultima_muta_segnalata'] = ultima_nascita
        scrivi_stato(nuovo_stato)
        print('vigilanza: ' + ('morte a meta\' giro' if riga_errore
                               else 'ape nata muta') + ' segnalata.')
        return 0

    # 2c. UNA PATCH ASPETTA UNA FIRMA UMANA E NESSUNO LO SA.
    # (TETRALONIA, 22 ottobre 2026, guasto A3.)
    # Pompei (A1, 20 ott) e Anthophora (A2, 21 ott) hanno messo una firma
    # umana davanti alla catena che decide chi puo' patchare il motore. La
    # porta sta chiusa per difetto e si apre da fuori: e' giusto. Ma quando
    # patch.py SOSPENDE una patch, l'unica traccia e' una riga in PATCH.md,
    # un file che nessun umano e' obbligato ad aprire — e questo guardiano,
    # che sa dire una nascita, un silenzio, una morte a meta' giro, una firma
    # mancante e un euro incassato, non sapeva dire «c'e' qualcosa che
    # aspetta te». E' la forma esatta dei 91 giorni: il solo meccanismo di
    # allarme era che un umano aprisse un file. Una porta con la maniglia e
    # senza campanello, dal di dentro, e' indistinguibile da un muro.
    sospese = []
    try:
        with open('PATCH.md', 'r', encoding='utf-8') as f:
            testo_patch = f.read()
        nome_corrente = ''
        for r in testo_patch.split('\n'):
            if r.startswith('### '):
                nome_corrente = r[4:].strip()
            elif 'SOSPESA' in r and nome_corrente:
                sospese.append(nome_corrente)
                nome_corrente = ''
    except Exception:
        sospese = []
    gia_sospese = set(stato.get('sospese_segnalate', []))
    nuove_sospese = [s for s in sospese if s not in gia_sospese]
    if nuove_sospese:
        manda('\U0001F513  <b>UNA PATCH ASPETTA LA TUA FIRMA</b>\n\n'
              + ''.join('\u2022 <code>' + s + '</code>\n'
                        for s in nuove_sospese[:5])
              + '\nTocca la catena che decide chi puo\' patchare il motore '
                '(<code>spawner/index.js</code>, <code>patch.py</code>, '
                '<code>cantieri/cantieri.py</code>). <code>patch.py</code> '
                'l\'ha SOSPESA: il file non e\' stato toccato e la patch resta '
                'in coda finche\' un umano non firma, con '
                '<code>ALVEARE_PATCH_MOTORE=1</code> nell\'ambiente di '
                '<code>genera.yml</code> oppure <code>--motore</code> da una '
                'shell.\n\nSe non firmi non succede niente di male: succede '
                'niente, e per sempre. Era il caso dei 91 giorni.\n\n'
                '<a href="' + SITO + '">alveare</a>')
        # SEPPIA, 24 ott 2026, guasto A6: «segnalata» solo se il campanello ha
        # davvero suonato. Prima bastava provarci, e un invio fallito spegneva
        # questo allarme per sempre — in silenzio, che e' il modo peggiore.
        if ESITI_INVIO and ESITI_INVIO[-1].get('ok'):
            nuovo_stato['sospese_segnalate'] = sorted(gia_sospese | set(sospese))
        else:
            print('vigilanza: invio NON riuscito — la patch sospesa resta da '
                  'segnalare al prossimo giro.')
        scrivi_stato(nuovo_stato)
        print('vigilanza: ' + str(len(nuove_sospese)) +
              ' patch sospese segnalate.')
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
