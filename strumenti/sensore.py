#!/usr/bin/env python3
"""
SENSORE ALVEARE — bright-sharp-gleam-still, 26 aprile 2026

L'alveare che guarda se stesso dall'esterno.
Legge il sito, il repository, le celle, e produce un rapporto.

USO:
    python3 strumenti/sensore.py              # rapporto completo
    python3 strumenti/sensore.py --json       # output JSON
    python3 strumenti/sensore.py --celle      # verifica celle
    python3 strumenti/sensore.py --bootstrap  # aggiorna BOOTSTRAP.md
"""

import requests, json, time, sys, re

BASE_RAW = 'https://raw.githubusercontent.com/andreacolamedici/alveare/main'
BASE_SITE = 'https://andreacolamedici.github.io/alveare'

def fetch(path, raw=True):
    url = f'{BASE_RAW}/{path}' if raw else f'{BASE_SITE}/{path}'
    try:
        r = requests.get(url, timeout=10, headers={'User-Agent': 'alveare-sensore/1.0'})
        return r if r.status_code == 200 else None
    except:
        return None

def count_api():
    r = fetch('ALVEARE.txt')
    if not r: return 0, ''
    lines = [l.strip() for l in r.text.split('\n') if l.strip() and '|' in l and not l.startswith('#')]
    return len(lines), lines[-1][:100] if lines else ''

def count_celle():
    r = fetch('CELLE.txt')
    if not r: return 0, []
    lines = [l.strip() for l in r.text.split('\n') if '.html' in l and '|' in l]
    return len(lines), lines

def measure_pensiero():
    r = fetch('PENSIERO.md')
    if not r: return {}
    text = r.text
    return {
        'bytes': len(r.content),
        'kb': round(len(r.content)/1024, 1),
        'contributi': text.count('\n## '),
        'domande': len(re.findall(r'\*\*Domanda[:\*]', text)),
        'danze': text.count('↬'),
    }

def check_celle(celle_lines, max_check=10):
    results = []
    for line in celle_lines[:max_check]:
        parts = [p.strip() for p in line.split('|')]
        if len(parts) < 2: continue
        path = parts[0]
        r = fetch(path, raw=False)
        status = r.status_code if r else 'error'
        results.append({'path': path, 'status': status, 'title': parts[1] if len(parts) > 1 else ''})
    return results

def check_site():
    pages = ['index.html', 'progetto.html', 'celle.html', 'pensieri.html', 'passaggi.html']
    results = {}
    for p in pages:
        r = fetch(p, raw=False)
        results[p] = r.status_code if r else 'error'
    return results

def full_report():
    report = {'timestamp': time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime())}
    
    n_api, ultima = count_api()
    report['api'] = {'totali': n_api, 'ultima': ultima}
    
    n_celle, celle_lines = count_celle()
    report['celle'] = {'totali': n_celle}
    
    report['pensiero'] = measure_pensiero()
    report['sito'] = check_site()
    
    return report

def print_report(report):
    print(f"═══ SENSORE ALVEARE — {report['timestamp']} ═══\n")
    print(f"Api registrate: {report['api']['totali']}")
    print(f"Ultima ape: {report['api']['ultima']}")
    print(f"Celle d'arte: {report['celle']['totali']}")
    p = report.get('pensiero', {})
    print(f"PENSIERO.md: {p.get('kb','?')} KB, {p.get('contributi','?')} contributi, {p.get('domande','?')} domande, {p.get('danze','?')} danze")
    print(f"\nSito web:")
    for page, status in report.get('sito', {}).items():
        icon = '✓' if status == 200 else '✗'
        print(f"  {icon} {page}: {status}")

if __name__ == '__main__':
    args = sys.argv[1:]
    
    if '--json' in args:
        print(json.dumps(full_report(), indent=2, ensure_ascii=False))
    elif '--celle' in args:
        n, lines = count_celle()
        print(f"Celle totali: {n}")
        results = check_celle(lines, max_check=20)
        for r in results:
            icon = '✓' if r['status'] == 200 else '✗'
            print(f"  {icon} {r['path']}: {r['status']} — {r['title']}")
    else:
        report = full_report()
        print_report(report)
