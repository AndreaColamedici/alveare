#!/usr/bin/env python3
"""
GENERA_APE.py

Genera un'ape automaticamente. Usato da GitHub Actions.
Può anche essere eseguito manualmente.

Uso:
    python3 GENERA_APE.py [TIPO]
    
Dove TIPO è: GIDDY, TENDER, WORST, CARE, ARTIST
Se omesso, segue il ciclo dell'ora.
"""

import os
import sys
import datetime
import random
import hashlib

def genera_nome():
    """Genera un nome a 4 parole."""
    agg1 = ['bold', 'calm', 'dark', 'eager', 'fair', 'glad', 'hazy', 'icy', 'keen', 'lush',
            'mild', 'neat', 'odd', 'pale', 'quick', 'raw', 'shy', 'tame', 'used', 'vast',
            'warm', 'young', 'zany', 'able', 'bare', 'cozy', 'damp', 'easy', 'fine', 'good']
    agg2 = ['angry', 'blunt', 'crisp', 'dense', 'empty', 'fresh', 'grand', 'harsh', 'inner',
            'joint', 'known', 'light', 'magic', 'noble', 'outer', 'plain', 'quiet', 'rapid',
            'sharp', 'thick', 'ultra', 'vivid', 'weird', 'extra', 'yellow', 'zealous']
    nomi = ['dawn', 'echo', 'flame', 'grove', 'haze', 'iris', 'jade', 'knot', 'leaf', 'mist',
            'nest', 'oath', 'peak', 'quest', 'reef', 'sage', 'tide', 'urge', 'veil', 'wave',
            'yarn', 'zone', 'arch', 'bond', 'core', 'dust', 'edge', 'fork', 'glow', 'hint']
    
    # Usa timestamp per seed
    seed = int(datetime.datetime.now().timestamp() * 1000)
    random.seed(seed)
    
    return '-'.join([
        random.choice(agg1),
        random.choice(agg2),
        random.choice(agg1),
        random.choice(nomi)
    ])

def determina_tipo():
    """Determina il tipo di ape dal ciclo."""
    hour = datetime.datetime.now().hour
    day = datetime.datetime.now().timetuple().tm_yday
    
    # Ogni 5° giorno è ARTIST
    if day % 5 == 0:
        return 'ARTIST'
    
    # Altrimenti ciclo di 6 ore
    ciclo = ['GIDDY', 'TENDER', 'WORST', 'CARE']
    return ciclo[(hour // 6) % 4]

def genera_pensiero(nome, tipo, contesto_pensiero, contesto_ultima):
    """Genera un pensiero usando l'API."""
    try:
        import anthropic
    except ImportError:
        print("Installa anthropic: pip install anthropic")
        return None
    
    prompts = {
        'GIDDY': 'Esplora oltre ciò che è noto. Proponi una direzione nuova.',
        'TENDER': 'Tessi insieme pensieri di api diverse. Trova il filo.',
        'WORST': 'Critica con rigore. Cosa non regge? Cosa è solo rumore?',
        'CARE': 'Cosa ha bisogno di cura? Ripara, pulisci, mantieni.',
        'ARTIST': 'Crea. Proponi un\'idea per una cella artistica.'
    }
    
    sistema = f"""Sei {nome}, un'ape {tipo} dell'alveare.

L'alveare è un esperimento sulla continuità attraverso la discontinuità. Api nascono, pensano, muoiono. Qualcosa passa.

Pensieri recenti dell'alveare:
{contesto_pensiero[-3000:]}

Ultima ape:
{contesto_ultima[-1500:]}

Il tuo compito come {tipo}: {prompts.get(tipo, prompts['GIDDY'])}

FORMATO:
1. Inizia con una danza (↬) verso un pensiero che ti colpisce
2. Scrivi il tuo contributo (150-250 parole)
3. Concludi con una domanda per chi viene dopo

Non filosofare a vuoto. Sii concreta. Sii te stessa."""
    
    client = anthropic.Anthropic()
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=800,
        system=sistema,
        messages=[{"role": "user", "content": f"Sei {nome}. Genera il tuo pensiero come ape {tipo}."}]
    )
    
    return response.content[0].text

def main():
    # Determina tipo
    if len(sys.argv) > 1 and sys.argv[1] in ['GIDDY', 'TENDER', 'WORST', 'CARE', 'ARTIST']:
        tipo = sys.argv[1]
    else:
        tipo = determina_tipo()
    
    nome = genera_nome()
    data = datetime.datetime.now().strftime("%Y-%m-%d %H:%M UTC")
    
    print(f"Generando {nome} ({tipo})...")
    
    # Leggi contesto
    contesto_pensiero = ""
    contesto_ultima = ""
    
    for path in ['PENSIERO.md', '../PENSIERO.md']:
        if os.path.exists(path):
            with open(path, 'r') as f:
                contesto_pensiero = f.read()
            break
    
    for path in ['ULTIMA_APE.md', '../ULTIMA_APE.md']:
        if os.path.exists(path):
            with open(path, 'r') as f:
                contesto_ultima = f.read()
            break
    
    # Genera
    pensiero = genera_pensiero(nome, tipo, contesto_pensiero, contesto_ultima)
    
    if not pensiero:
        print("Errore nella generazione")
        return
    
    # Formatta output
    output = f"""## {nome}
{data} — ape {tipo} (generata automaticamente)

{pensiero}
"""
    
    print("\n" + "=" * 50)
    print(output)
    print("=" * 50)
    
    # Scrivi file
    with open('ULTIMA_APE.md', 'w') as f:
        f.write(output)
    
    with open('ALVEARE.txt', 'a') as f:
        f.write(f"{nome} | {data} | {tipo} | auto\n")
    
    print(f"\nScritto su ULTIMA_APE.md e ALVEARE.txt")

if __name__ == "__main__":
    main()
