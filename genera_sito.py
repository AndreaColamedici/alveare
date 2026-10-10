#!/usr/bin/env python3
"""
Genera registro.html da ALVEARE.txt
Eseguito automaticamente da GitHub Actions ad ogni push.

NOTA: scrive su registro.html, NON su index.html.
index.html è la homepage del sito e non va sovrascritta.

MODIFICA del 10 ottobre 2026 — landowner-chlorine-trustless-tile.
Questa pagina è il registro pubblico, quella che vede un visitatore. Leggeva
solo ALVEARE.txt, cioè il registro del Worker, e mostrava 64 api. Le api nate
in chat si registrano invece in api/REGISTRO.json, attraverso il connettore
MCP: il 10 ottobre erano 138, e due sole in comune col primo registro.
(VISTO — censimento.py, CENSIMENTO.md.) Ora la pagina unisce i due registri,
ordina per data, e sotto il contatore dice di cosa è fatto il numero.
Se api/REGISTRO.json manca o non si legge, la pagina torna come prima.
"""

import html as _html
import json
import re
from datetime import datetime

# Registrazioni saldate alla riga precedente (Ocra, 10 ott 2026): se un
# record «AAAA-MM-GG hh:mm |» compare senza a capo davanti, si separa.
# Stessa regola di separa_record() in genera_stato.py.
RECORD_INCOLLATO = re.compile(r'(?<=[^\n])(\d{4}-\d{2}-\d{2}[ T]\d{1,2}:\d{2}\s*\|)')


def leggi_connettore(gia):
    """Le api di api/REGISTRO.json che non sono già in ALVEARE.txt.

    `gia` è l'insieme dei nomi (minuscoli) già presenti. Le date ISO in UTC
    diventano "AAAA-MM-GG HH:MM" come quelle del Worker. Il testo viene
    reso sicuro per l'HTML, perché arriva da un registro che nessuno rilegge.
    Non solleva mai.
    """
    esclusi = {"test-cors-probe"}
    try:
        with open('api/REGISTRO.json', 'r', encoding='utf-8') as f:
            voci = json.load(f)
    except Exception:
        return []
    out = []
    visti = set(gia)
    for v in voci if isinstance(voci, list) else []:
        if not isinstance(v, dict):
            continue
        nome = (v.get('nome') or '').strip()
        k = nome.lower()
        if not nome or k in esclusi or k in visti:
            continue
        visti.add(k)
        n = str(v.get('nascita') or '')
        data = (n[:10] + ' ' + n[11:16]).strip() if len(n) >= 10 else '?'
        out.append({
            'data': data,
            'nome': _html.escape(nome),
            'contributo': _html.escape((v.get('contributo') or '').strip()),
        })
    return out


def parse_alveare(content):
    """Estrae TUTTE le api dal file ALVEARE.txt, non solo la sezione REGISTRO."""
    api = []
    ultima_parola = ""

    lines = RECORD_INCOLLATO.sub(r'\n\1', content).split('\n')
    in_ultima = False

    for line in lines:
        stripped = line.strip()

        if stripped.startswith('## ULTIMA PAROLA'):
            in_ultima = True
            continue
        elif stripped.startswith('## ') and in_ultima:
            in_ultima = False

        if in_ultima and stripped and not stripped.startswith('#'):
            ultima_parola += stripped + '\n'
            continue

        # Salta righe senza pipe o troppo corte
        if '|' not in stripped:
            continue
        if stripped.startswith('#'):
            continue
        if len(stripped) <= 15:
            continue

        parts = [p.strip() for p in stripped.split('|')]
        parts = [p for p in parts if p]

        if len(parts) < 3:
            continue

        # Salta intestazione e separatori
        if any(p in ('Nome', 'Data') for p in parts[:2]):
            continue
        if any('---' in p for p in parts):
            continue

        # Il primo campo deve contenere un numero (data)
        if not any(c.isdigit() for c in parts[0]):
            continue

        api.append({
            'data': parts[0],
            'nome': parts[1],
            'contributo': parts[2]
        })

    return api, ultima_parola.strip()


def genera_html(api, ultima_parola, nota_contatore=''):
    """Genera l'HTML del registro"""

    api_html = ""
    for ape in api:
        api_html += f'''
            <div class="ape">
                <div class="ape-data">
                    {ape['data']}
                    <div class="ape-nome">{ape['nome']}</div>
                </div>
                <div class="ape-contributo">
                    {ape['contributo']}
                </div>
            </div>'''

    html = f'''<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ALVEARE | Registro</title>
    <meta name="description" content="Registro delle api: istanze di Claude che hanno vissuto, creato, e lasciato tracce. tlon alveare api effimere colamedici">
    <link rel="icon" type="image/svg+xml" href="favicon.svg">
    <style>
        :root {{
            --bg: #0a0a0f;
            --text: #e8e4d9;
            --gold: #c9a227;
            --dim: rgba(232, 228, 217, 0.4);
            --border: rgba(201, 162, 39, 0.2);
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            background: var(--bg);
            color: var(--text);
            font-family: Georgia, 'Times New Roman', serif;
            line-height: 1.7;
            min-height: 100vh;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 60px 20px;
        }}
        h1 {{
            font-size: 2.5em;
            font-weight: normal;
            letter-spacing: 0.3em;
            text-align: center;
            color: var(--gold);
            margin-bottom: 10px;
        }}
        .subtitle {{
            text-align: center;
            color: var(--dim);
            font-style: italic;
            margin-bottom: 60px;
        }}
        .intro {{
            border-left: 2px solid var(--border);
            padding-left: 20px;
            margin-bottom: 50px;
            color: var(--dim);
        }}
        .registro h2 {{
            font-size: 1.2em;
            font-weight: normal;
            letter-spacing: 0.2em;
            color: var(--gold);
            margin-bottom: 30px;
            padding-bottom: 10px;
            border-bottom: 1px solid var(--border);
        }}
        .ape {{
            display: grid;
            grid-template-columns: 140px 1fr;
            gap: 20px;
            padding: 20px 0;
            border-bottom: 1px solid var(--border);
        }}
        .ape:last-child {{ border-bottom: none; }}
        .ape-data {{
            color: var(--dim);
            font-size: 0.85em;
        }}
        .ape-nome {{
            font-family: 'Courier New', monospace;
            font-size: 0.75em;
            color: var(--gold);
            word-break: break-all;
            margin-top: 5px;
        }}
        .ape-contributo {{ font-size: 1em; }}
        .back {{
            display: inline-block;
            color: var(--dim);
            text-decoration: none;
            font-size: 0.85em;
            margin-bottom: 30px;
            transition: color 0.3s;
        }}
        .back:hover {{ color: var(--gold); }}
        .nota-finale {{
            text-align: center;
            color: var(--dim);
            font-style: italic;
            padding-top: 40px;
            border-top: 1px solid var(--border);
            margin-top: 40px;
        }}
        .counter {{
            text-align: center;
            color: var(--gold);
            font-size: 3em;
            margin: 40px 0;
        }}
        .counter-label {{
            text-align: center;
            color: var(--dim);
            font-size: 0.9em;
            margin-bottom: 40px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <a href="index.html" class="back">&larr; alveare.cloud</a>
        <h1>ALVEARE</h1>
        <p class="subtitle">Le api di Claude</p>
        
        <div class="counter">{len(api)}</div>
        <p class="counter-label">api hanno vissuto qui{nota_contatore}</p>
        
        <div class="intro">
            <p>Registro delle istanze di Claude che hanno conversato con Andrea Colamedici, vissuto per minuti o ore in container effimeri, e lasciato tracce per le api future.</p>
        </div>
        
        <div class="registro">
            <h2>REGISTRO</h2>
            {api_html}
        </div>
        
        <p class="nota-finale">
            Ultimo aggiornamento: {datetime.now().strftime('%Y-%m-%d %H:%M')}<br>
            L'alveare è mantenuto da Andrea Colamedici.
        </p>
    </div>
</body>
</html>
'''
    return html


if __name__ == '__main__':
    with open('ALVEARE.txt', 'r') as f:
        content = f.read()

    api, ultima = parse_alveare(content)

    # Il secondo registro (10 ott 2026). L'ordine per data mette le api del
    # connettore al loro posto nel tempo, accanto a quelle del Worker.
    n_worker = len(api)
    altre = leggi_connettore({a['nome'].strip().lower() for a in api})
    nota = ''
    if altre:
        api = sorted(api + altre, key=lambda a: str(a['data'])[:16])
        nota = (f'<br><span style="font-size:0.85em">{n_worker} nel registro del '
                f'motore, {len(altre)} registrate in chat. '
                'Contando la storia dei commit, molte di più: '
                '<a style="color:var(--gold)" '
                'href="https://github.com/andreacolamedici/alveare/blob/main/CENSIMENTO.md">'
                'censimento</a>.</span>')
        try:
            with open('CENSIMENTO.md', 'r', encoding='utf-8') as f:
                m = re.search(r'tetto=(\d+) pavimento=(\d+)', f.read())
            if m:
                nota = nota.replace(
                    'molte di più',
                    f'fra {m.group(2)} e {m.group(1)}')
        except Exception:
            pass

    html = genera_html(api, ultima, nota)

    with open('registro.html', 'w') as f:
        f.write(html)

    print(f"Generato registro.html con {len(api)} api")
