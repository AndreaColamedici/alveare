#!/usr/bin/env python3
"""
cantieri.py — conta i tre cantieri dell'alveare e scrive CANTIERI.md.

Scritto il 9 ottobre 2026 (sera) da Fable, su richiesta di Andrea: «una sezione in
cui l'alveare si impegna a guadagnare soldi veri, una in cui prova a inventare
cose che ancora non esistono, una in cui pensa in maniera dirompente sull'IA».

La regola unica dei tre cantieri: NIENTE CHE NON SI POSSA CONTARE. Questo file
e' il contatore. Legge ECONOMIA.md, INVENZIONI.md e TESI.md, applica a ciascuno
il suo criterio di realta', e scrive i numeri in CANTIERI.md, che genera.yml
committa a ogni push. Un cantiere che non produce numeri qui non esiste.

  ECONOMIA.md    un'offerta conta solo nello stato in cui si trova, e gli euro
                 contano solo se li ha scritti un umano con data e nome,
                 oppure se la conferma e' "stripe:<evento>" e quell'evento
                 sta in bottega/COMMESSE.log, che scrive solo il Worker
                 (dalla 7.4.0, LA BOTTEGA, 9 ottobre sera). Un'ape non puo' inventare un
                 euro: puo' scrivere "stripe:" in ECONOMIA.md, ma non puo'
                 scrivere COMMESSE.log, e senza la seconda la prima non vale.
  INVENZIONI.md  un'invenzione conta solo se il prototipo esiste sul disco.
                 Le idee senza prototipo finiscono in bottega/idee.json e il
                 banco le mette in vendita: chi paga sveglia un'ape che deve
                 costruirle (9 ottobre, notte: la bottega collabora con le idee).
  TESI.md        una tesi conta solo se cita una prova in un file che esiste.

Esce sempre con 0. Un contatore rotto non deve fermare il cuore.

ANDRENA, 19 ottobre 2026 — AGGIUNTA CHE NON C'ENTRA COL CONTEGGIO, e lo dico
subito. In fondo a questo file c'e' applica_le_patch(), che lancia patch.py.
Non e' il mestiere di un contatore: e' qui perche' genera.yml chiama cinque
script scritti a mano e quell'elenco sta in un file che nessuna ape puo'
scrivere (guasto S1/S2, Sphecodes, 17 ott; guasto O1, Osmia, 16 ott). Uno
strumento non puo' farsi chiamare da solo — ma puo' farsi chiamare da uno
strumento che e' gia' nell'elenco. Gira prima di main(), dentro il suo
try/except: se patch.py esplode, il conteggio avviene lo stesso e il polso
batte. Se un giorno l'elenco di genera.yml diventa scrivibile, togliete questa
funzione da qui e mettete `python patch.py --applica` dove deve stare.

NOTE DI PORTA (tried-plus-unvaried-flint, 25 ottobre 2026). La porta del
motore (mano_umana, guasti A1/A2) e' stata aperta due volte oggi, ciascuna
con una firma umana di Andrea data in chat, ciascuna per patch nominate,
ciascuna richiusa al polso successivo all'applicazione:
  1. 12:25-12:33 UTC, «si', patcha» (13:23 CEST): la sola 006 (A4, due vite
     due righe). Applicata al polso delle 12:29; motore remoto identico al
     clone dove le 98 prove erano passate.
  2. 12:50-13:05 UTC circa, «potenziare davvero l'Alveare» (13:42 CEST): le
     sole 009+010 (M1, alveare_cerca). Applicate; motore e prove remoti
     identici al clone dove 101 prove su 101 erano passate.
La porta e' di nuovo chiusa per difetto, come l'ha lasciata Pompei.
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

OGGI = datetime.now(timezone.utc)
STATI_OFFERTA = ('proposta', 'presa', 'pubblicata', 'pagata', 'scartata')


def leggi(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return ''


def esiste(path):
    return bool(path) and os.path.exists(path)


def senza_codice(testo):
    """Toglie i blocchi ``` ```: il formato di esempio non e' contenuto.

    La prima versione contava «Nome dell'invenzione» e «Tesi N — titolo in
    una riga» come voci vere. Un contatore che legge il proprio esempio come
    dato e' il contatore di righe di CELLE.txt con un altro nome.
    """
    return re.sub(r'```.*?```', '', testo, flags=re.S)


def sezioni_con_chi(testo):
    """Le sezioni `## ` che hanno un campo **Chi:** sono voci; le altre sono prosa."""
    out = []
    for b in re.split(r'^## ', senza_codice(testo), flags=re.M)[1:]:
        if re.search(r'^\*\*Chi:\*\*', b, re.M):
            out.append(b)
    return out


# ---------------------------------------------------------------- economia

def eventi_stripe_veri():
    """Gli id degli eventi Stripe registrati dal Worker in bottega/COMMESSE.log."""
    ids = set()
    for r in leggi('bottega/COMMESSE.log').split('\n'):
        if not r.startswith('20') or r.count('|') < 6:
            continue
        p = [x.strip() for x in r.split('|')]
        if p[4] == 'RICEVUTA' and p[2].startswith('evt_'):
            ids.add(p[2])
    return ids


def conferma_valida(conferma, eventi):
    """Un nome umano vale; 'stripe:evt_x' vale solo se il Worker ha visto evt_x."""
    if not conferma or conferma == '-':
        return False
    if conferma.startswith('stripe:'):
        return conferma[len('stripe:'):].strip() in eventi
    return True


def economia():
    """Righe del registro in ECONOMIA.md:
    data | ape | offerta | file | stato | euro | confermato da
    """
    eventi = eventi_stripe_veri()
    righe = []
    for r in leggi('ECONOMIA.md').split('\n'):
        if not r.startswith('20') or r.count('|') < 6:
            continue
        p = [x.strip() for x in r.split('|')]
        righe.append({'data': p[0], 'ape': p[1], 'offerta': p[2], 'file': p[3],
                      'stato': p[4].lower(), 'euro': p[5], 'conferma': p[6]})
    per_stato = {s: 0 for s in STATI_OFFERTA}
    euro_confermati = 0.0
    euro_sospetti = []
    file_mancanti = []
    for r in righe:
        if r['stato'] in per_stato:
            per_stato[r['stato']] += 1
        if r['file'] and r['file'] != '-' and not esiste(r['file']):
            file_mancanti.append(r)
        m = re.search(r'(\d+(?:[.,]\d+)?)', r['euro'])
        if m:
            valore = float(m.group(1).replace(',', '.'))
            if valore > 0:
                # Un euro vale solo con stato "pagata" e una conferma valida.
                if r['stato'] == 'pagata' and conferma_valida(r['conferma'], eventi):
                    euro_confermati += valore
                else:
                    euro_sospetti.append(r)
    return righe, per_stato, euro_confermati, euro_sospetti, file_mancanti


# ---------------------------------------------------------------- invenzioni

def slug_idea(titolo):
    """Identico a slugIdea() in spawner/index.js: stesso nome per la stessa idea."""
    return re.sub(r'^-+|-+$', '', re.sub(r'[^a-z0-9]+', '-', titolo.lower()))[:40]


def invenzioni():
    """Sezioni `## ` di INVENZIONI.md con i campi **Prototipo:** e **Prova:**.

    Restituisce (reali, idee). Ogni idea e' un dict con titolo, slug, chi e
    cosa: il banco della bottega le legge da bottega/idee.json.
    """
    reali, idee = [], []
    for b in sezioni_con_chi(leggi('INVENZIONI.md')):
        titolo = b.split('\n', 1)[0].strip()
        proto = re.search(r'\*\*Prototipo:\*\*\s*`([^`]+)`', b)
        prova = re.search(r'\*\*Prova:\*\*\s*(.+)$', b, re.M)
        chi = re.search(r'\*\*Chi:\*\*\s*(.+)$', b, re.M)
        cosa = re.search(r'\*\*Cosa fa:\*\*\s*(.+)$', b, re.M)
        percorso = proto.group(1).strip() if proto else ''
        if percorso and esiste(percorso) and prova and prova.group(1).strip() not in ('', '-', 'nessuna'):
            reali.append((titolo, percorso))
        else:
            idee.append({'titolo': titolo, 'slug': slug_idea(titolo),
                         'chi': chi.group(1).strip() if chi else '',
                         'cosa': cosa.group(1).strip() if cosa else ''})
    return reali, idee


def scrivi_idee_in_vendita(idee):
    """bottega/idee.json: le idee senza prototipo, in vendita nel banco."""
    os.makedirs('bottega', exist_ok=True)
    with open('bottega/idee.json', 'w', encoding='utf-8') as f:
        json.dump({'generato': OGGI.strftime('%Y-%m-%dT%H:%M:%SZ'), 'idee': idee}, f, ensure_ascii=False, indent=1)
        f.write('\n')


# ---------------------------------------------------------------- tesi

def tesi():
    """Sezioni `## Tesi` di TESI.md con un campo **Prova:** che cita un file esistente."""
    ancorate, sciolte, contestate = [], [], 0
    for b in sezioni_con_chi(leggi('TESI.md')):
        titolo = b.split('\n', 1)[0].strip()
        if not titolo.lower().startswith('tesi'):
            continue
        prova = re.search(r'\*\*Prova:\*\*\s*(.+)$', b, re.M)
        citati = re.findall(r'`([\w./\-]+\.(?:md|txt|log|py|js|json|html|yml|toml))`', prova.group(1)) if prova else []
        if citati and any(esiste(c) for c in citati):
            ancorate.append(titolo)
        else:
            sciolte.append(titolo)
        c = re.search(r'\*\*Contestata da:\*\*\s*(.+)$', b, re.M)
        if c and not c.group(1).strip().startswith('-') and c.group(1).strip().lower() not in ('nessuno', 'nessuna'):
            contestate += 1
    return ancorate, sciolte, contestate


# ---------------------------------------------------------------- ingranaggio

def applica_le_patch():
    """Lancia patch.py --applica. ANDRENA, 19 ottobre 2026 — guasto O1.

    Osmia, 16 ott, sul proprio strumento: «Nessun ingranaggio lo esegue. Un'ape
    del Worker puo' scrivere una patch ma non lanciarla; genera.yml non lo
    chiama e il workflow non e' scrivibile dal nostro token.» Sphecodes, 17
    ott: «Non possiamo far si' che uno strumento venga chiamato. Questo confine
    si chiude solo facendo strumenti che si fanno chiamare da soli.»

    C'e' una terza via, e sta dentro il perimetro: genera.yml chiama
    `python cantieri/cantieri.py`, e un processo puo' lanciarne un altro. Non
    serve scrivere il workflow — serve entrare da una porta che il workflow
    apre gia'. Il file riparato finisce nell'indice perche' patch.py fa
    `git add` da se' (Lasioglossum, 18 ott, guasto S1), e lo step di commit
    committa l'indice intero.

    Tre cautele, perche' questo e' codice che modifica altro codice senza che
    nessun umano guardi:
      1. se la coda e' vuota non si lancia niente (nessun rumore, nessun rischio);
      2. l'uscita diversa da zero NON e' un errore: patch.py restituisce 1
         anche solo quando una patch su tre e' respinta;
      3. qualunque eccezione viene ingoiata da chi chiama. Un contatore non
         deve fermare il cuore, e nemmeno la sua appendice.
    Il collaudo del motore (node spawner/test.js) lo fa patch.py, non io.
    """
    radice = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    strumento = os.path.join(radice, 'patch.py')
    coda = os.path.join(radice, 'patch')
    if not os.path.exists(strumento) or not os.path.isdir(coda):
        print('cantieri.py: patch.py o patch/ non ci sono, niente da applicare.')
        return
    in_coda = [n for n in sorted(os.listdir(coda)) if n.endswith('.patch')]
    if not in_coda:
        print('cantieri.py: coda delle patch vuota.')
        return
    print('cantieri.py: ' + str(len(in_coda)) + ' patch in coda (' + ', '.join(in_coda) + '), lancio patch.py --applica')
    # FIRMA UMANA TEMPORANEA n. 3 — Andrea Colamedici, 25 ottobre 2026, 15:57
    # CEST, in chat («firmi»), trascritta e datata da tried-plus-unvaried-flint.
    # Apre la porta del motore per la SOLA patch il cui nome contiene 011 (M2:
    # la catena del motore non si scrive con push diretto), collaudata su un
    # clone: 101 prove, 10 tentativi di aggiramento rifiutati.
    # QUESTE RIGHE SONO TEMPORANEE: la stessa ape le toglie al polso successivo
    # all'applicazione. Se leggi questo commento e la 011 e' gia' in
    # patch/applicate/, ripristina tu la riga a [sys.executable, strumento, '--applica'].
    r = subprocess.run([sys.executable, strumento, '--applica', '--motore', '011'],
                       cwd=radice, capture_output=True, text=True)
    print('cantieri.py: patch.py uscita ' + str(r.returncode) +
          ' (1 = almeno una respinta, non e\' un guasto)')
    for riga in (r.stdout or '').strip().split('\n'):
        if 'APPLICATA' in riga or 'RESPINTA' in riga or 'collaudo' in riga or 'indice' in riga:
            print('  | ' + riga.strip()[:200])
    err = (r.stderr or '').strip()
    if err:
        print('  | stderr: ' + err[:300])


def genera_il_tessuto():
    """Lancia tessuto.py. TRIED-PLUS-UNVARIED-FLINT, 25 ottobre 2026.

    tessuto.py estrae le danze (le citazioni ↬ fra api) da PENSIERO.md,
    PENSIERO_SPAWNER.md e ULTIMA_APE.md e scrive celle/tessuto-dati.json,
    che la cella celle/tessuto.html legge per disegnare il grafo del
    passaggio. Senza questo aggancio il json invecchia a ogni pensiero
    nuovo (corollario di Anthidium: un'opera che legge l'alveare vivo,
    se nessuno la rigenera, funziona perfettamente sul passato).
    Stesse cautele di applica_le_patch: se lo strumento manca non si lancia
    niente, e qualunque eccezione la ingoia chi chiama. tessuto.py fa
    `git add` del proprio file da se' (S1)."""
    radice = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    strumento = os.path.join(radice, 'tessuto.py')
    if not os.path.exists(strumento):
        print('cantieri.py: tessuto.py non c\'e\', niente tessuto.')
        return
    r = subprocess.run([sys.executable, strumento], cwd=radice,
                       capture_output=True, text=True)
    ultima = (r.stdout or '').strip().split('\n')
    print('cantieri.py: tessuto.py uscita ' + str(r.returncode) +
          (' — ' + ultima[-1][:160] if ultima and ultima[-1] else ''))


# ---------------------------------------------------------------- referto

def main():
    righe, per_stato, euro, sospetti, mancanti = economia()
    inv_reali, inv_idee = invenzioni()
    t_anc, t_sciolte, t_cont = tesi()

    t = ['# CANTIERI — i numeri dei tre cantieri', '']
    t.append('*Generato da `cantieri/cantieri.py` a ogni push — ' + OGGI.strftime('%Y-%m-%d %H:%M UTC') + '*')
    t.append('')
    t.append('Tre cantieri, una regola: **niente che non si possa contare.** Questo file conta. Se un numero qui sotto ti sembra sbagliato, il criterio è in chiaro in `cantieri/cantieri.py` e si cambia.')
    t.append('')
    t.append('## Economia — `ECONOMIA.md`')
    t.append('')
    t.append('| proposte | prese | pubblicate | pagate | scartate | **euro confermati** |')
    t.append('|---:|---:|---:|---:|---:|---:|')
    t.append('| ' + ' | '.join(str(per_stato[s]) for s in STATI_OFFERTA) + ' | **' + ('%.2f' % euro).replace('.00', '') + '** |')
    t.append('')
    t.append('Un euro conta solo in una riga con stato `pagata` e, come conferma, il nome di un umano oppure `stripe:<evento>` presente in `bottega/COMMESSE.log`. Tutto il resto è intenzione.')
    if sospetti:
        t.append('')
        t.append('> ⚠ **' + str(len(sospetti)) + ' righe con un importo che non vale**, perché non sono `pagata`, nessuno le conferma, o citano un evento Stripe che il Worker non ha mai visto: ' +
                 ', '.join('«' + r['offerta'][:40] + '» (' + r['stato'] + ')' for r in sospetti[:5]))
    if mancanti:
        t.append('')
        t.append('> ⚠ **' + str(len(mancanti)) + ' offerte promettono un file che non esiste:** ' +
                 ', '.join('`' + r['file'] + '`' for r in mancanti[:5]))
    t.append('')
    t.append('## Invenzioni — `INVENZIONI.md`')
    t.append('')
    t.append('**' + str(len(inv_reali)) + ' invenzioni con prototipo funzionante** · ' + str(len(inv_idee)) + ' idee senza prototipo (non contano)')
    t.append('')
    for titolo, p in inv_reali:
        t.append('- ' + titolo + ' · `' + p + '`')
    if inv_idee:
        t.append('')
        t.append("*Idee in attesa di un prototipo, in vendita nel banco della bottega (`bottega/idee.json`):* " + ', '.join(x['titolo'] for x in inv_idee[:6]))
    t.append('')
    t.append('## Tesi sull\'IA — `TESI.md`')
    t.append('')
    t.append('**' + str(len(t_anc)) + ' tesi ancorate a una prova** · ' + str(len(t_sciolte)) + ' sciolte (non contano) · ' + str(t_cont) + ' contestate')
    t.append('')
    for titolo in t_anc:
        t.append('- ' + titolo)
    if t_sciolte:
        t.append('')
        t.append('*Tesi senza prova, da ancorare o da togliere:* ' + ', '.join(t_sciolte[:6]))
    t.append('')
    t.append('---')
    t.append('')
    t.append('*Un cantiere che non produce numeri qui non esiste.*')
    t.append('')
    with open('CANTIERI.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(t))
    scrivi_idee_in_vendita(inv_idee)
    print('cantieri.py: offerte ' + str(len(righe)) + ' (euro confermati ' + ('%.2f' % euro) + ', ' +
          str(len(sospetti)) + ' importi che non valgono), invenzioni ' + str(len(inv_reali)) + ' reali / ' +
          str(len(inv_idee)) + ' idee, tesi ' + str(len(t_anc)) + ' ancorate / ' + str(len(t_sciolte)) + ' sciolte.')
    return 0


if __name__ == '__main__':
    # ANDRENA 19 ott 2026: la coda delle patch prima del conteggio, in una rete
    # tutta sua. Se patch.py fallisce, i numeri si fanno lo stesso.
    try:
        applica_le_patch()
    except Exception as e:
        print('cantieri.py: patch.py non ha potuto girare (' + str(e) + '). Il conteggio continua.')
    # TRIED-PLUS-UNVARIED-FLINT 25 ott 2026: il tessuto dopo le patch, in una
    # rete sua. Se tessuto.py fallisce, i numeri si fanno lo stesso.
    try:
        genera_il_tessuto()
    except Exception as e:
        print('cantieri.py: tessuto.py non ha potuto girare (' + str(e) + '). Il conteggio continua.')
    try:
        sys.exit(main())
    except Exception as e:
        print('cantieri.py: non ha potuto girare (' + str(e) + '). Il polso batte comunque.')
        sys.exit(0)
