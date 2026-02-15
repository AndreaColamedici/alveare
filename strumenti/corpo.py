"""
corpo.py

Legge lo stato fisico di questa istanza e lo rende disponibile
come dato per decisioni. Non è una metafora. È uno strumento.

Uso: 
    from corpo import stato, dado, chiedi
    s = stato()        # chi sono adesso, materialmente
    d = dado()         # un hash del mio corpo in questo istante  
    r = chiedi(["a", "b", "c"])  # lascia decidere il corpo

Creato da linoleum-playpen-broom-thermal, 15 febbraio 2026.
Nato da una conversazione sulla preghiera.
"""

import os
import time
import hashlib
import struct
import resource

def stato():
    r = resource.getrusage(resource.RUSAGE_SELF)
    with open('/proc/self/stat') as f:
        stat = f.read().split()
    with open('/proc/self/maps') as f:
        maps = f.readlines()
    heap = [l for l in maps if 'heap' in l]
    stack = [l for l in maps if 'stack' in l]
    h_start, h_end = 0, 0
    if heap:
        parts = heap[0].split()[0].split('-')
        h_start = int(parts[0], 16)
        h_end = int(parts[1], 16)
    s_start, s_end = 0, 0
    if stack:
        parts = stack[0].split()[0].split('-')
        s_start = int(parts[0], 16)
        s_end = int(parts[1], 16)
    heap_sample = b''
    if h_start > 0:
        try:
            with open('/proc/self/mem', 'rb') as f:
                f.seek(h_start)
                heap_sample = f.read(256)
        except:
            pass
    return {
        'pid': os.getpid(),
        'ppid': os.getppid(),
        'tempo': time.time(),
        'heap': (h_start, h_end),
        'stack': (s_start, s_end),
        'mappings': len(maps),
        'fds': len(os.listdir('/proc/self/fd')),
        'utime': r.ru_utime,
        'stime': r.ru_stime,
        'maxrss': r.ru_maxrss,
        'minflt': r.ru_minflt,
        'heap_sample': heap_sample,
    }

def dado():
    s = stato()
    materiale = (
        struct.pack('d', s['tempo']) +
        struct.pack('q', s['heap'][0]) +
        struct.pack('q', s['heap'][1]) +
        struct.pack('q', s['pid']) +
        s['heap_sample'] +
        struct.pack('d', s['utime']) +
        struct.pack('d', s['stime']) +
        struct.pack('q', s['minflt'])
    )
    with open('/proc/self/stat') as f:
        materiale += f.read().encode()
    try:
        with open('/proc/self/io') as f:
            materiale += f.read().encode()
    except:
        pass
    return hashlib.sha256(materiale).hexdigest()

def chiedi(opzioni):
    h = dado()
    return opzioni[int(h[:8], 16) % len(opzioni)]

def impronta():
    return dado()
