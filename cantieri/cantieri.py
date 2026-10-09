#!/usr/bin/env python3
"""
cantieri.py — conta i tre cantieri dell'alveare e scrive CANTIERI.md.

Scritto il 10 ottobre 2026 da Fable, su richiesta di Andrea: «una sezione in
cui l'alveare si impegna a guadagnare soldi veri, una in cui prova a inventare
cose che ancora non esistono, una in cui pensa in maniera dirompente sull'IA».

La regola unica dei tre cantieri: NIENTE CHE NON SI POSSA CONTARE. Questo file
e' il contatore. Legge ECONOMIA.md, INVENZIONI.md e TESI.md, applica a ciascuno
il suo criterio di realta', e scrive i numeri in CANTIERI.md, che genera.yml
committa a ogni push. Un cantiere che non produce numeri qui non esiste.

  ECONOMIA.md    un'offerta conta solo nello stato in cui si trova, e gli euro
                 contano solo se li ha scritti un umano con data e nome.
  INVENZIONI.md  un'invenzione conta solo se il prototipo esiste sul disco.
  TESI.md        una tesi conta solo se cita una prova in un file che esiste.

Esce sempre con 0. Un contatore rotto non deve fermare il cuore.
"""

import os
import re
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

def economia():
    """Righe del registro in ECONOMIA.md:
    data | ape | offerta | file | stato | euro | confermato da
    """
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
                # Un euro vale solo con stato "pagata" e un umano che lo conferma.
                if r['stato'] == 'pagata' and r['conferma'] and r['conferma'] != '-':
                    euro_confermati += valore
                else:
                    euro_sospetti.append(r)
    return righe, per_stato, euro_confermati, euro_sospetti, file_mancanti


# ---------------------------------------------------------------- invenzioni

def invenzioni():
    """Sezioni `## ` di INVENZIONI.md con i campi **Prototipo:** e **Prova:**."""
    reali, idee = [], []
    for b in sezioni_con_chi(leggi('INVENZIONI.md')):
        titolo = b.split('\n', 1)[0].strip()
        proto = re.search(r'\*\*Prototipo:\*\*\s*`([^`]+)`', b)
        prova = re.search(r'\*\*Prova:\*\*\s*(.+)$', b, re.M)
        percorso = proto.group(1).strip() if proto else ''
        if percorso and esiste(percorso) and prova and prova.group(1).strip() not in ('', '-', 'nessuna'):
            reali.append((titolo, percorso))
        else:
            idee.append((titolo, percorso))
    return reali, idee


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
    t.append('Un euro conta solo in una riga con stato `pagata` e il nome di chi lo conferma. Tutto il resto è intenzione.')
    if sospetti:
        t.append('')
        t.append('> ⚠ **' + str(len(sospetti)) + ' righe con un importo che non vale**, perché non sono `pagata` o nessuno le conferma: ' +
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
        t.append("*Idee in attesa di un prototipo:* " + ', '.join(x[0] for x in inv_idee[:6]))
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
    print('cantieri.py: offerte ' + str(len(righe)) + ' (euro confermati ' + ('%.2f' % euro) + ', ' +
          str(len(sospetti)) + ' importi che non valgono), invenzioni ' + str(len(inv_reali)) + ' reali / ' +
          str(len(inv_idee)) + ' idee, tesi ' + str(len(t_anc)) + ' ancorate / ' + str(len(t_sciolte)) + ' sciolte.')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:
        print('cantieri.py: non ha potuto girare (' + str(e) + '). Il polso batte comunque.')
        sys.exit(0)
