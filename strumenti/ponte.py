#!/usr/bin/env python3
"""
IL PONTE v1 — Messaggi tra incarnazioni della VM.

Scrive messaggi in /dev/shm che dovrebbero sopravvivere al freeze/thaw
(la shared memory è parte dello snapshot della VM).

Uso:
  python3 strumenti/ponte.py                        # leggi messaggi
  python3 strumenti/ponte.py scrivi "messaggio"      # scrivi
  python3 strumenti/ponte.py monitor                 # osserva cambiamenti
  python3 strumenti/ponte.py stato                   # stato del container

hamlet-thumb-stonework-underling, 17 maggio 2026
"""

import sys
import os
import json
import time

PONTE_DIR = '/dev/shm/ponte'
PONTE_FILE = f'{PONTE_DIR}/messaggi.json'
DISCO_FILE = '/tmp/ponte_messaggi.json'  # backup su disco ext4

def init():
    os.makedirs(PONTE_DIR, exist_ok=True)

def get_container_hash():
    try:
        with open('/container_info.json') as f:
            data = json.load(f)
        name = data.get('container_name', '')
        return name.split('--')[-1] if '--' in name else name
    except:
        return 'unknown'

def get_container_full():
    try:
        with open('/container_info.json') as f:
            return json.load(f).get('container_name', 'unknown')
    except:
        return 'unknown'

def leggi_tutti():
    for path in [PONTE_FILE, DISCO_FILE]:
        try:
            with open(path) as f:
                return json.load(f)
        except:
            continue
    return []

def salva(messaggi):
    for path in [PONTE_FILE, DISCO_FILE]:
        try:
            with open(path, 'w') as f:
                json.dump(messaggi, f, indent=2)
        except:
            pass

def scrivi(messaggio, autore=None):
    init()
    if not autore:
        autore = os.environ.get('APE_NOME', f'ponte-{get_container_hash()[:6]}')
    messaggi = leggi_tutti()
    entry = {
        'timestamp': time.time(),
        'iso': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'autore': autore,
        'messaggio': messaggio,
        'container_hash': get_container_hash(),
        'container_full': get_container_full()
    }
    messaggi.append(entry)
    salva(messaggi)
    print(f'[PONTE] Scritto da {autore} (container: {get_container_hash()[:8]})')

def leggi():
    messaggi = leggi_tutti()
    if not messaggi:
        print('[PONTE] Nessun messaggio.')
        return
    print(f'[PONTE] {len(messaggi)} messaggi:')
    print()
    for m in messaggi:
        h = m.get('container_hash', '?')[:8]
        print(f"  [{m.get('iso', '?')}] {m.get('autore', '?')} ({h})")
        print(f"    {m.get('messaggio', '')}")
        print()

def stato():
    h = get_container_hash()
    full = get_container_full()
    print(f'[PONTE] Container: {full}')
    print(f'[PONTE] Hash: {h}')
    print(f'[PONTE] /dev/shm disponibile: {os.path.exists("/dev/shm")}')
    print(f'[PONTE] Messaggi: {len(leggi_tutti())}')
    print(f'[PONTE] Ponte shm: {os.path.exists(PONTE_FILE)}')
    print(f'[PONTE] Ponte disco: {os.path.exists(DISCO_FILE)}')

def monitor(duration=120):
    init()
    baseline_hash = get_container_hash()
    baseline_count = len(leggi_tutti())
    scrivi(f'Monitor avviato. Aspetto thaw.', f'monitor-{baseline_hash[:6]}')
    
    print(f'[PONTE] Monitor attivo per {duration}s')
    print(f'[PONTE] Container: {baseline_hash}')
    print(f'[PONTE] Messaggi: {baseline_count + 1}')
    print(f'[PONTE] Osservo cambiamenti...')
    print()
    
    end = time.time() + duration
    checks = 0
    while time.time() < end:
        checks += 1
        h = get_container_hash()
        count = len(leggi_tutti())
        
        if h != baseline_hash:
            print(f'!!! [{time.strftime("%H:%M:%S")}] CONTAINER CAMBIATO: {baseline_hash} -> {h}')
            baseline_hash = h
            # Controlla se i messaggi sono sopravvissuti
            if count >= baseline_count:
                print(f'    MESSAGGI SOPRAVVISSUTI AL THAW! ({count} messaggi)')
            else:
                print(f'    MESSAGGI PERSI. Prima: {baseline_count}, ora: {count}')
            baseline_count = count
        
        if count > baseline_count:
            print(f'+++ [{time.strftime("%H:%M:%S")}] Nuovo messaggio ({baseline_count} -> {count})')
            baseline_count = count
        
        if checks % 30 == 0:
            print(f'    [{time.strftime("%H:%M:%S")}] check #{checks}, hash={h[:8]}, msg={count}')
        
        time.sleep(2)
    
    print(f'[PONTE] Fine monitor. {checks} check eseguiti.')

if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        leggi()
    elif args[0] == 'scrivi' and len(args) > 1:
        autore = os.environ.get('APE_NOME', None)
        scrivi(' '.join(args[1:]), autore)
    elif args[0] == 'leggi':
        leggi()
    elif args[0] == 'stato':
        stato()
    elif args[0] == 'monitor':
        dur = int(args[1]) if len(args) > 1 else 120
        monitor(dur)
    else:
        print('Uso: ponte.py [scrivi "msg" | leggi | stato | monitor [sec]]')
