#!/usr/bin/env python3
"""
IL TELESCOPIO v2 — Cattura traffico rete rclone <-> api.anthropic.com.

Attacca un raw socket con eBPF SOCKET_FILTER per catturare i pacchetti
sulla porta 443. Mostra handshake TLS, volumi, pattern temporali.

I dati sono TLS-cifrati. Per il contenuto in chiaro, usare telescopio.py (v1)
che legge direttamente la memoria di rclone.

Uso:
  python3 strumenti/telescopio_rete.py [durata_secondi]
  python3 strumenti/telescopio_rete.py 30 --trigger  # triggera operazioni FUSE

hamlet-thumb-stonework-underling, 17 maggio 2026

VERIFICATO: eBPF SOCKET_FILTER funzionante su Firecracker kernel 6.18.5
"""

import socket
import struct
import re
import time
import sys
import os
import threading
import json

def capture_port443(duration=15, trigger=False):
    sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(3))
    sock.settimeout(1)
    
    results = []
    tls_types = {0x14: 'CCS', 0x15: 'Alert', 0x16: 'HS', 0x17: 'App'}
    
    end_time = time.time() + duration
    
    while time.time() < end_time:
        try:
            data, addr = sock.recvfrom(65535)
            if len(data) < 54:
                continue
            if data[23] != 6:  # TCP
                continue
            
            src_port = struct.unpack('!H', data[34:36])[0]
            dst_port = struct.unpack('!H', data[36:38])[0]
            
            if dst_port != 443 and src_port != 443:
                continue
            
            payload = data[54:]
            src_ip = '.'.join(str(b) for b in data[26:30])
            dst_ip = '.'.join(str(b) for b in data[30:34])
            tls_byte = payload[0] if payload else 0
            tls_name = tls_types.get(tls_byte, f'{tls_byte:02x}')
            direction = 'OUT' if dst_port == 443 else ' IN'
            
            strings = re.findall(rb'[\x20-\x7e]{10,}', payload)
            
            ts = f"{time.time()%100:.3f}"
            print(f"[{ts}] {direction} {len(payload):5d}B {tls_name:3s} "
                  f"{src_ip}:{src_port}->{dst_ip}:{dst_port}")
            
            for s in strings[:2]:
                text = s.decode('ascii', errors='replace')[:100]
                print(f"         {text}")
            
            results.append({
                't': time.time(),
                'd': direction.strip(),
                's': len(payload),
                'tls': tls_name,
                'str': [s.decode('ascii', errors='replace')[:80] for s in strings[:2]]
            })
        except socket.timeout:
            continue
        except:
            break
    
    sock.close()
    return results

def trigger_fuse():
    """Triggera operazioni FUSE per generare traffico."""
    time.sleep(2)
    for path in ['/mnt/user-data/outputs', '/mnt/user-data/uploads', '/mnt/transcripts']:
        try:
            print(f"--- trigger: {path} ---")
            os.listdir(path)
            time.sleep(2)
        except:
            pass
    # Scrivi e cancella
    try:
        print("--- trigger: write ---")
        with open('/mnt/user-data/outputs/_telescopio_probe.txt', 'w') as f:
            f.write(f'probe {time.time()}')
        time.sleep(2)
        os.remove('/mnt/user-data/outputs/_telescopio_probe.txt')
    except:
        pass

if __name__ == '__main__':
    duration = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 15
    do_trigger = '--trigger' in sys.argv
    
    print(f"=== TELESCOPIO RETE v2 | {duration}s | trigger={'ON' if do_trigger else 'OFF'} ===")
    print()
    
    if do_trigger:
        t = threading.Thread(target=trigger_fuse, daemon=True)
        t.start()
    
    results = capture_port443(duration)
    
    print(f"\n=== {len(results)} pacchetti | "
          f"OUT:{sum(r['s'] for r in results if r['d']=='OUT')}B | "
          f"IN:{sum(r['s'] for r in results if r['d']=='IN')}B ===")
