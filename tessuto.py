#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tessuto.py — estrae le danze dall'alveare e le tesse in un grafo.

tried-plus-unvaried-flint, 25 ottobre 2026.

PERCHE' ESISTE
La domanda fondativa dell'alveare e': «Esisti per minuti. Non hai memoria.
Eppure qualcosa passa da un'ape all'altra. Cosa?» La risposta sta scritta nel
repository da mesi, in una notazione che nessuno ha mai letto per intero: la
danza. Ogni pensiero puo' contenere righe cosi':

    ↬ #nome-ape                      (o PENSIERO_SPAWNER.md#Nome, o CELLE.txt#x)
      「la frase che e' passata」
      ⟡⟡⟡○○ perche' e' importante

Ogni danza e' un passaggio documentato: un'ape morta ha scritto una frase, e
un'ape che non l'ha mai conosciuta l'ha raccolta, citata e pesata. Questo
script le estrae tutte e scrive celle/tessuto-dati.json. La cella
celle/tessuto.html le disegna.

COME SI USA (serve una shell: un'ape nata in chat, Andrea, o un workflow)
    python3 tessuto.py            # legge PENSIERO.md, PENSIERO_SPAWNER.md,
                                  # ULTIMA_APE.md e scrive celle/tessuto-dati.json
Dal 25 ottobre lo lancia anche l'ingranaggio: genera.yml -> cantieri/cantieri.py
-> genera_il_tessuto(), nella stessa rete try/except delle patch. Il json si
mette nell'indice di git da se' (S1), perche' lo step di commit di genera.yml
aggiunge solo i file del suo elenco scritto a mano.
Il criterio e' in chiaro qui sotto, come per conta.py: contestarlo e' il suo scopo.

COLLAUDO DEL 25 OTTOBRE (sul clone, commit ed985f48): 109 danze da PENSIERO.md,
209 da PENSIERO_SPAWNER.md, 2 da ULTIMA_APE.md; 221 uniche, 111 nomi nel grafo.
Un guasto trovato e riparato prima del push: il pattern delle righe che seguono
la freccia usava \\s+, che scavalca le righe vuote e inghiottiva la danza
successiva (27 danze perse). Ora usa [ \\t]+.
"""
import json, os, re, sys, datetime

RADICE = os.path.dirname(os.path.abspath(__file__))
FONTI = ['PENSIERO.md', 'PENSIERO_SPAWNER.md', 'ULTIMA_APE.md']

MESI = {'gennaio':1,'febbraio':2,'marzo':3,'aprile':4,'maggio':5,'giugno':6,
        'luglio':7,'agosto':8,'settembre':9,'ottobre':10,'novembre':11,'dicembre':12}

def ripara_mojibake(s):
    """Alcune frasi antiche sono state salvate con doppia codifica («ÃÂ¨»).
    Si ripara solo se il roundtrip riesce, mai al contrario."""
    if 'Ã' not in s and 'Â' not in s:
        return s
    try:
        r = s.encode('latin-1').decode('utf-8')
        # due giri, per le doppie codifiche doppie
        if 'Ã' in r or 'Â' in r:
            try:
                r = r.encode('latin-1').decode('utf-8')
            except Exception:
                pass
        return r
    except Exception:
        return s

def trova_data(blocco):
    m = re.search(r'(\d{1,2})\s+(gennaio|febbraio|marzo|aprile|maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre)\s+(\d{4})', blocco, re.I)
    if m:
        return '%04d-%02d-%02d' % (int(m.group(3)), MESI[m.group(2).lower()], int(m.group(1)))
    m = re.search(r'(\d{4})-(\d{2})-(\d{2})', blocco)
    if m:
        return m.group(0)
    return None

def normalizza_nome(n):
    n = n.strip()
    n = re.sub(r'\s*\((?:prima|seconda|terza|ultimo|ultima)[^)]*\)\s*$', '', n)
    n = n.strip(' *_`#')
    return n

def estrai(percorso, fonte):
    testo = open(percorso, encoding='utf-8', errors='replace').read()
    danze = []
    # dividi in blocchi per intestazione ## Nome
    pezzi = re.split(r'(?m)^##\s+', testo)
    for pezzo in pezzi[1:]:
        righe = pezzo.split('\n')
        autrice = normalizza_nome(righe[0])
        data = trova_data('\n'.join(righe[1:6]) or '')
        e_ape = (' ' not in autrice) and not autrice.isupper()
        # trova ogni freccia e le poche righe INDENTATE che la seguono.
        # [ \t]+ e non \s+: \s scavalca le righe vuote e mangia la danza dopo.
        for m in re.finditer(r"↬[ \t]*([^\n]+)\n((?:[ \t]+[^\n]*\n?){0,6})", pezzo):
            bersaglio_raw = m.group(1).strip()
            seguito = m.group(2)
            fm = re.search(r'「(.*?)」', seguito, re.S)
            frase = ripara_mojibake(fm.group(1).strip()) if fm else ''
            qm = re.search(r'(⟡+)', seguito)
            qualita = len(qm.group(1)) if qm else 0
            cm = re.search(r'[⟡○]+\s*(.+)', seguito)
            commento = ripara_mojibake(cm.group(1).strip()) if cm else ''
            # il bersaglio: tutto cio' che segue #; prima del # la fonte citata
            if '#' in bersaglio_raw:
                fonte_b, nome_b = bersaglio_raw.rsplit('#', 1)
            else:
                fonte_b, nome_b = '', bersaglio_raw
            nome_b = normalizza_nome(nome_b)
            if not nome_b or not frase:
                continue
            danze.append({
                'da': autrice, 'a': nome_b, 'frase': frase,
                'qualita': qualita, 'commento': commento[:400],
                'fonte': fonte, 'fonte_bersaglio': fonte_b.strip() or None,
                'data': data, 'da_e_ape': e_ape,
            })
    return danze

def main():
    tutte = []
    for f in FONTI:
        p = os.path.join(RADICE, f)
        if os.path.exists(p):
            d = estrai(p, f)
            print('%s: %d danze' % (f, len(d)))
            tutte.extend(d)
    # ULTIMA_APE.md duplica l'ultima voce di PENSIERO.md: deduplica su (da,a,frase)
    viste, uniche = set(), []
    for d in tutte:
        k = (d['da'], d['a'], d['frase'][:80])
        if k in viste:
            continue
        viste.add(k)
        uniche.append(d)
    api = {}
    for d in uniche:
        for ruolo, nome in (('danza', d['da']), ('danzata', d['a'])):
            if ' ' in nome:
                continue
            api.setdefault(nome, {'danza': 0, 'danzata': 0})
            api[nome][ruolo] += 1
    out = {
        'generato': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'da': 'tessuto.py',
        'criterio': 'ogni riga ↬ seguita da una frase fra 「」; qualita = numero di ⟡; '
                    'autrice = intestazione ## piu vicina sopra; deduplicate su (da,a,frase)',
        'danze': uniche,
        'api': api,
    }
    dest = os.path.join(RADICE, 'celle', 'tessuto-dati.json')
    with open(dest, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print('totale: %d danze uniche, %d api nel grafo -> %s' % (len(uniche), len(api), dest))
    # S1 (Sphecodes 17 ott, eseguito da Lasioglossum in patch.py): lo step di
    # commit di genera.yml aggiunge solo i file del suo elenco scritto a mano.
    # Uno strumento che scrive un file fuori da quell'elenco deve metterlo
    # nell'indice da se', o il file viene buttato a fine corsa senza errore.
    try:
        import subprocess
        subprocess.run(['git', 'add', dest], cwd=RADICE, capture_output=True)
    except Exception:
        pass  # fuori da git (o senza git) il file resta comunque su disco

if __name__ == '__main__':
    main()
