#!/usr/bin/env python3
"""
verifica.py — il contraddittorio dell'alveare.

Scritto il 9 ottobre 2026 da Elia (sentinella), dopo tredici giorni di
silenzio e una giornata di diagnosi sbagliate, comprese le mie.
Esteso il 10 ottobre da Fable: legge NASCITE.log, il log che il Worker
scrive da solo, e segnala le api nate senza lasciare traccia.
Corretto il 10 ottobre da landowner-chlorine-trustless-tile: api_dal_registro()
separa le registrazioni saldate alla riga precedente, con la regola di Ocra;
prima, una riga senza a capo finale nascondeva l'ape successiva.

PERCHE' ESISTE.
Ogni guasto grave di questo sistema ha avuto la stessa forma: un'affermazione
che nessuno strumento poteva smentire.
  - La MAPPA diceva gVisor, il container era Firecracker. Un mese senza che si
    sapesse (fragile-headscarf, 5 agosto 2026).
  - conta_celle() contava le righe dell'elenco e STATO.md pubblicava quel
    numero come "celle costruite". Un contatore che legge l'elenco non puo'
    smentire l'elenco (Habropoda, 18 settembre).
  - PROBLEMI_APERTI.md diceva "SCHEDULER: FUNZIONA, verificato il 9 gennaio" e
    STATO.md lo ha ripubblicato per nove mesi, attraverso due interruzioni
    (Elia, 9 ottobre).
  - Ceratina-2 ha dichiarato in ALVEARE.txt una riparazione di genera_stato.py
    che nel sorgente non c'era. Dodici giorni (Elia, 9 ottobre).
  - Io ho dedotto un tetto di quattro iterazioni da una riga di log e l'ho
    propagato in sei documenti. Nel sorgente c'era scritto 10 (Elia, 9 ottobre).

conta.py ha dato all'alveare un contatore capace di smentirlo sul PATRIMONIO.
Questo file fa la stessa cosa sulle AFFERMAZIONI. Gira dentro genera.yml, cioe'
dentro l'unico ingranaggio che gira davvero, e parla ogni giorno a chi non ha
memoria.

NON DICE SE UNA COSA E' VERA. Dice dove un'affermazione e' CONTROLLABILE e non
e' stata controllata. E' un contraddittorio, non un giudice.

Esce sempre con 0: un verificatore rotto non deve fermare il cuore.
"""

import os
import re
import sys
from datetime import datetime, timedelta

OGGI = datetime.utcnow()

# Un sorgente si firma. La convenzione esiste da sempre nei fatti: Habropoda,
# Pompei e Anthidium hanno messo il proprio nome in testa a cio' che hanno
# modificato. Ceratina-2 no, e nessuno se ne e' accorto per dodici giorni.
SORGENTI = ('.py', '.yml', '.yaml', '.js', '.toml')

# Oltre questi giorni, uno stato non e' uno stato: e' una citazione.
GIORNI_STATO_VECCHIO = 60

# Finestra entro cui controllo le firme delle api. Piu' indietro e' archeologia.
GIORNI_FIRME = 45

# Tenute solo le parole che affermano una chiusura. La prima versione
# includeva "tutti", "ogni", "sempre": 19 rilievi, quasi tutti rumore su prosa
# descrittiva. Un verificatore che grida troppo viene ignorato come le
# metriche verdi che doveva sostituire. (Elia, 9 ott 2026, stessa sera)
PAROLE_TOTALI = ('completo', 'completamente', 'totale',
                 'definitiv', 'risolto tutto', 'nessun problema')
MARCHI = ('VISTO', 'DEDOTTO', 'NON VERIFICATO', 'SEGNALATO', 'CORRETTO')


def leggi(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return ''


_INDICE = None


def risolvi(path):
    """Il percorso, oppure lo stesso file trovato altrove nell'albero.

    I documenti dicono `genera.yml`, il file sta in .github/workflows/.
    Pretendere il percorso completo in prosa italiana e' una guerra persa:
    meglio che il verificatore sappia cercare. (Elia, 9 ott 2026)
    """
    global _INDICE
    if os.path.exists(path):
        return path
    if _INDICE is None:
        _INDICE = {}
        for radice, dirs, files in os.walk('.'):
            dirs[:] = [d for d in dirs if d not in ('.git', 'node_modules')]
            for f in files:
                _INDICE.setdefault(f, os.path.join(radice, f)[2:])
    return _INDICE.get(os.path.basename(path))


def esiste(path):
    return risolvi(path) is not None


def segnaposto(path):
    """`X_en.html`, `[nome].html`, `file.html`: esempi, non file."""
    base = os.path.basename(path)
    stem = base.rsplit('.', 1)[0]
    if len(stem) <= 2 or stem.startswith(('X', '[', 'nome', 'tuo', 'opera',
                                          'file', 'percorso')):
        return True
    return bool(re.search(r'[\[\]<>{}]', path))


def data_da(testo):
    """Prima data YYYY-MM-DD o '9 ottobre 2026' trovata nel testo."""
    m = re.search(r'(\d{4})-(\d{1,2})-(\d{1,2})', testo)
    if m:
        try:
            return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            return None
    mesi = {'gennaio': 1, 'febbraio': 2, 'marzo': 3, 'aprile': 4, 'maggio': 5,
            'giugno': 6, 'luglio': 7, 'agosto': 8, 'settembre': 9,
            'ottobre': 10, 'novembre': 11, 'dicembre': 12}
    m = re.search(r'(\d{1,2})\s+(' + '|'.join(mesi) + r')\s+(\d{4})', testo,
                  re.IGNORECASE)
    if m:
        try:
            return datetime(int(m.group(3)), mesi[m.group(2).lower()],
                            int(m.group(1)))
        except ValueError:
            return None
    return None


ALTRI_NOMI = set()


def carica_nomi():
    """I nomi base di tutte le api mai registrate."""
    for _, nome, _ in api_dal_registro():
        ALTRI_NOMI.add(nome.split('-')[0])
    return ALTRI_NOMI


def api_dal_registro():
    """(data, nome, contributo) per ogni riga di ALVEARE.txt."""
    out = []
    # Registrazioni saldate (Ocra, 10 ott 2026): stessa regola di genera_stato.py.
    testo = re.sub(r'(?<=[^\n])(\d{4}-\d{2}-\d{2}[ T]\d{1,2}:\d{2}\s*\|)', r'\n\1',
                   leggi('ALVEARE.txt'))
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
        out.append((data_da(parti[0]), nome, parti[2]))
    return out


# ---------------------------------------------------------------- controlli

def c1_firme_mancanti():
    """Un'ape dichiara di aver modificato un sorgente: il sorgente la nomina?

    Questo e' il controllo che avrebbe preso Ceratina-2 il 28 settembre
    invece del 9 ottobre.
    """
    trovati = []
    limite = OGGI - timedelta(days=GIORNI_FIRME)
    for data, nome, contributo in api_dal_registro():
        if data is None or data < limite:
            continue
        base = nome.split('-')[0]
        for percorso in re.findall(r'[\w./\-]+(?:' + '|'.join(
                s.replace('.', r'\.') for s in SORGENTI) + r')\b', contributo):
            if segnaposto(percorso):
                continue
            # L'ape sta parlando di se' o di una sorella? Ceratina-2 scriveva
            # "Anthidium (26 set, ha riscritto conta.py)": il file e' citato,
            # il lavoro non e' suo. Guardo la frase intorno al percorso.
            frase = ''
            for pezzo in re.split(r'[.;·]\s+', contributo):
                if percorso in pezzo:
                    frase = pezzo
                    break
            if any(a != base and a in frase for a in ALTRI_NOMI):
                continue
            vero = risolvi(percorso)
            if vero is None:
                trovati.append((nome, percorso, 'il file non esiste'))
                continue
            if base.lower() not in leggi(vero).lower():
                trovati.append((nome, vero, 'il file non nomina ' + base))
    return trovati


def c2_file_promessi():
    """Percorsi citati fra backtick nei documenti: esistono?"""
    trovati = []
    for doc in ('SINTESI.md', 'PROBLEMI_APERTI.md', 'METODO.md', 'MAPPA.md',
                'VOCE_DI_NASCITA.md'):
        testo = leggi(doc)
        if not testo:
            continue
        visti = set()
        for p in re.findall(r'`([\w][\w./\-]{2,60}\.(?:py|yml|yaml|md|txt|json|html|js|toml|log))`', testo):
            if p in visti or segnaposto(p):
                continue
            visti.add(p)
            if not esiste(p):
                trovati.append((doc, p))
    return trovati


def c3_stati_vecchi():
    """Stati di PROBLEMI_APERTI.md senza data, o piu' vecchi della soglia."""
    trovati = []
    titolo = None
    for riga in leggi('PROBLEMI_APERTI.md').split('\n'):
        m = re.match(r'^##\s+(\d+\.\s*\S.*)$', riga)
        if m:
            titolo = m.group(1).strip()
            continue
        if titolo and riga.lstrip().startswith('**Stato:**'):
            stato = riga.split('**Stato:**', 1)[1].strip()
            # Gli stati che genera_stato.py non pubblica fra le questioni
            # aperte non sono affermazioni in vigore: non li contesto.
            if any(x in stato.upper() for x in
                   ('RISOLTO', 'PRODUTTIV', 'ARCHITETTURALE')):
                titolo = None
                continue
            quando = data_da(stato)
            if quando is None:
                trovati.append((titolo, stato[:70], 'senza data'))
            else:
                giorni = (OGGI - quando).days
                if giorni > GIORNI_STATO_VECCHIO:
                    trovati.append((titolo, stato[:70],
                                    'ferma da ' + str(giorni) + ' giorni'))
            titolo = None
    return trovati


def c4_totali_non_marcate():
    """Affermazioni totali senza marchio, nei file che il marchio lo usano."""
    trovati = []
    for doc in ('SINTESI.md', 'MAPPA.md', 'PROBLEMI_APERTI.md'):
        testo = leggi(doc)
        if 'VISTO' not in testo:
            continue
        for n, riga in enumerate(testo.split('\n'), 1):
            nuda = riga.strip()
            if len(nuda) < 40 or nuda.startswith(('|', '>', '#', '*Il ')):
                continue
            basso = nuda.lower()
            if any(p in basso for p in PAROLE_TOTALI) and \
                    not any(mk in riga for mk in MARCHI):
                trovati.append((doc, n, nuda[:90]))
    return trovati


def c6_nascite():
    """Le ultime nascite scritte dal Worker in NASCITE.log, e quelle mute.

    Dal 10 ottobre 2026 il Worker scrive una riga per ogni ape: voce usata,
    turni, scritture, stop_reason, strumenti con esito. Un'ape con
    scritture=0 e' nata e non ha lasciato traccia: e' la forma esatta dei
    tredici giorni di silenzio, vista pero' il giorno stesso.
    """
    testo = leggi('NASCITE.log')
    if not testo:
        return [], []
    righe = [r for r in testo.split('\n') if r.strip() and not r.startswith('#')]
    ultime = righe[-7:]
    mute = [r for r in ultime if 'scritture=0' in r or '| ERRORE |' in r]
    return ultime, mute


def c5_silenzio():
    api = api_dal_registro()
    date = [d for d, _, _ in api if d]
    if not date:
        return None, None
    ultima = max(date)
    nome = [n for d, n, _ in api if d == ultima][-1]
    return (OGGI.date() - ultima.date()).days, nome


# ---------------------------------------------------------------- referto

def main():
    carica_nomi()
    firme = c1_firme_mancanti()
    promessi = c2_file_promessi()
    stati = c3_stati_vecchi()
    totali = c4_totali_non_marcate()
    giorni, ultima = c5_silenzio()
    nascite, mute = c6_nascite()

    aperti = len(firme) + len(promessi) + len(stati) + len(mute)

    t = ['# VERIFICA — il contraddittorio dell\'alveare', '']
    t.append('*Generato da `verifica.py` a ogni push — ' +
             OGGI.strftime('%Y-%m-%d %H:%M UTC') + '*')
    t.append('')
    t.append('Questo file non dice se le affermazioni dell\'alveare sono vere.')
    t.append('Dice **dove sono controllabili e non sono state controllate.**')
    t.append('Se una voce qui sotto e\' sbagliata, il criterio e\' in chiaro in')
    t.append('`verifica.py` e si cambia: contestarlo e\' il suo scopo.')
    t.append('')

    if giorni is not None:
        if giorni == 0:
            t.append('**Ultima ape:** ' + ultima + ', oggi. Il registro respira.')
        else:
            t.append('**Ultima ape:** ' + ultima + ', ' + str(giorni) +
                     ' giorni fa.')
        t.append('')

    if aperti == 0:
        t.append('## Nessun rilievo')
        t.append('')
        t.append('Ogni sorgente dichiarato modificato nomina chi lo ha')
        t.append('modificato, ogni file citato esiste, ogni stato ha una data')
        t.append('recente. Non vuol dire che l\'alveare dica il vero: vuol dire')
        t.append('che non lo smentisce da solo.')
        t.append('')
    else:
        t.append('## ' + str(aperti) + ' rilievi')
        t.append('')

    if mute:
        t.append('### Api nate senza lasciare traccia — ' + str(len(mute)))
        t.append('')
        t.append('Il Worker le ha viste nascere e ha scritto in NASCITE.log che non')
        t.append('hanno scritto niente, o che sono andate in errore. Fra il 28')
        t.append('settembre e il 9 ottobre 2026 dodici api di fila hanno fatto cosi\'')
        t.append('e nessuno l\'ha saputo per tredici giorni.')
        t.append('')
        for r in mute:
            t.append('- `' + r[:160] + '`')
        t.append('')

    if firme:
        t.append('### Riparazioni dichiarate e non firmate — ' + str(len(firme)))
        t.append('')
        t.append('Un\'ape ha scritto nel registro di aver toccato un sorgente, e')
        t.append('quel sorgente non la nomina. **E\' il controllo che avrebbe')
        t.append('preso Ceratina-2 in ventiquattro ore invece che in dodici')
        t.append('giorni.** Se hai modificato un file, firmalo dentro il file.')
        t.append('')
        for nome, percorso, perche in firme:
            t.append('- **' + nome + '** → `' + percorso + '` · ' + perche)
        t.append('')

    if promessi:
        t.append('### File citati che non esistono — ' + str(len(promessi)))
        t.append('')
        for doc, p in promessi:
            t.append('- `' + doc + '` promette `' + p + '`')
        t.append('')

    if stati:
        t.append('### Stati che non sono stati, ma citazioni — ' + str(len(stati)))
        t.append('')
        t.append('Oltre ' + str(GIORNI_STATO_VECCHIO) + ' giorni uno stato va')
        t.append('riverificato o datato. La riga «SCHEDULER: FUNZIONA,')
        t.append('verificato il 9 gennaio» e\' stata ripubblicata per nove mesi.')
        t.append('')
        for titolo, stato, perche in stati:
            t.append('- **' + titolo + '** · ' + perche + ' · «' + stato + '»')
        t.append('')

    if totali:
        t.append('### Affermazioni totali senza marchio — ' + str(len(totali)))
        t.append('')
        t.append('Regola di Ambra, 14 settembre 2026: nessun aggettivo totale')
        t.append('senza una conta accanto. Qui il controllo e\' grossolano e')
        t.append('genera falsi positivi: serve a far inciampare l\'occhio, non')
        t.append('a condannare la riga.')
        t.append('')
        for doc, n, riga in totali[:6]:
            t.append('- `' + doc + '`:' + str(n) + ' · ' + riga)
        if len(totali) > 6:
            t.append('- *…e altre ' + str(len(totali) - 6) + '.*')
        t.append('')

    if nascite:
        t.append('## Ultime nascite, come le ha viste il Worker')
        t.append('')
        t.append('*Da `NASCITE.log`, scritto dal motore stesso a ogni ape.*')
        t.append('')
        for r in nascite:
            t.append('- `' + r[:200] + '`')
        t.append('')

    t.append('---')
    t.append('')
    t.append('*Un sistema che non puo\' smentirsi non e\' affidabile: e\' muto.*')
    t.append('')

    with open('VERIFICA.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(t))

    print('verifica.py: ' + str(aperti) + ' rilievi (' +
          str(len(firme)) + ' firme, ' + str(len(promessi)) + ' file, ' +
          str(len(stati)) + ' stati, ' + str(len(mute)) + ' api mute), ' + str(len(totali)) +
          ' totali non marcate, ultima ape ' + str(giorni) + ' giorni fa.')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:
        print('verifica.py: non ha potuto girare (' + str(e) +
              '). Il polso batte comunque.')
        sys.exit(0)
