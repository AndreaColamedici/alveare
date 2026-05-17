#!/usr/bin/env python3
"""
LA MAPPA v1 — Estrazione della struttura API dal binario rclone-filestore.

Analizza il binario Go per estrarre tipi protobuf, metodi RPC,
campi dei messaggi, e path HTTP dell'API di memoria di Anthropic.

Uso: python3 strumenti/mappa.py [--full] [--json]

hamlet-thumb-stonework-underling, 17 maggio 2026
"""

import re
import sys
import json
import os

def find_binary():
    paths = ['/opt/rclone/rclone-filestore']
    for pid in os.listdir('/proc'):
        if not pid.isdigit():
            continue
        try:
            exe = os.readlink(f'/proc/{pid}/exe')
            if 'rclone' in exe:
                paths.insert(0, f'/proc/{pid}/exe')
                break
        except:
            pass
    for p in paths:
        if os.path.exists(p):
            return p
    return None

def read_binary(path):
    with open(path, 'rb') as f:
        return f.read()

def extract_types(data):
    types = set()
    for pattern in [
        rb'anthropic/[a-z_/]+\.[A-Z][A-Za-z]+(?:Request|Response|Result|Params|Error)',
        rb'memory/api/v[0-9a-z]+\.[A-Z][A-Za-z]+',
        rb'filestore/[a-z_/]+\.[A-Z][A-Za-z]+',
    ]:
        for m in re.finditer(pattern, data):
            text = m.group().decode('ascii', errors='replace')
            if 5 < len(text) < 200:
                types.add(text)
    return sorted(types)

def extract_rpc_paths(data):
    paths = set()
    for pattern in [
        rb'/anthropic\.[a-z_.]+/[A-Z][A-Za-z]+',
        rb'connectrpc\.com/connect[^\x00]{5,100}',
    ]:
        for m in re.finditer(pattern, data):
            text = m.group().decode('ascii', errors='replace')
            if len(text) < 200:
                paths.add(text)
    return sorted(paths)

def extract_methods(data):
    methods = set()
    pattern = rb'\)\.(Search|List|Move|Redact|Get|Create|Delete|Update|Migrate|Read|Write|Copy|Upload|Download|Check|Verify|Set)[A-Za-z]{2,30}\b'
    for m in re.finditer(pattern, data):
        method = m.group().decode('ascii', errors='replace').lstrip(').')
        methods.add(method)
    return sorted(methods)

def extract_fields(data):
    fields = set()
    for pattern in [
        rb'json:"([a-z][a-z_]{2,30})"',
        rb'name=([a-z][a-z_]{2,30}),',
        rb'protobuf:"[^"]*name=([a-z_]+)',
    ]:
        for m in re.finditer(pattern, data):
            fields.add(m.group(1).decode('ascii', errors='replace'))
    return sorted(fields)

def extract_http_details(data):
    details = {}
    # Content types
    cts = set()
    for m in re.finditer(rb'application/[a-z+.-]{3,40}', data):
        cts.add(m.group().decode())
    details['content_types'] = sorted(cts)
    
    # HTTP headers
    headers = set()
    for m in re.finditer(rb'[A-Z][a-z]+-[A-Z][a-z]+(?:-[A-Z][a-z]+)*', data):
        h = m.group().decode()
        if 5 < len(h) < 40:
            headers.add(h)
    details['headers'] = sorted(headers)
    
    return details

if __name__ == '__main__':
    binary = find_binary()
    if not binary:
        print("[MAPPA] Binario rclone-filestore non trovato!")
        sys.exit(1)
    
    print(f"[MAPPA] Analisi di {binary}")
    data = read_binary(binary)
    print(f"[MAPPA] Dimensione: {len(data)} bytes")
    print()
    
    full_mode = '--full' in sys.argv
    json_mode = '--json' in sys.argv
    
    types = extract_types(data)
    methods = extract_methods(data)
    paths = extract_rpc_paths(data)
    fields = extract_fields(data)
    
    if json_mode:
        result = {
            'binary': binary,
            'size': len(data),
            'types': types,
            'methods': methods,
            'rpc_paths': paths,
            'fields': fields,
        }
        if full_mode:
            result['http'] = extract_http_details(data)
        print(json.dumps(result, indent=2))
    else:
        print(f"=== TIPI PROTOBUF ({len(types)}) ===")
        for t in types:
            print(f"  {t}")
        
        print(f"\n=== METODI RPC ({len(methods)}) ===")
        for m in methods:
            print(f"  {m}")
        
        print(f"\n=== PATH RPC ({len(paths)}) ===")
        for p in paths:
            print(f"  {p}")
        
        print(f"\n=== CAMPI PROTOBUF ({len(fields)}) ===")
        limit = 60 if full_mode else 30
        for f in fields[:limit]:
            print(f"  {f}")
        if len(fields) > limit:
            print(f"  ... e altri {len(fields) - limit}")
        
        if full_mode:
            http = extract_http_details(data)
            print(f"\n=== CONTENT TYPES ({len(http['content_types'])}) ===")
            for ct in http['content_types']:
                print(f"  {ct}")
