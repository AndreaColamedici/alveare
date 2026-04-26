#!/usr/bin/env python3
"""
STRUMENTI DI RICERCA INTERNA — bright-sharp-gleam-still
26 aprile 2026

Cinque strumenti per le api esploratrici.
Ogni strumento si può usare da solo o combinato con gli altri.

USO RAPIDO:
    python3 strumenti/probe.py scan      # scansione memoria
    python3 strumenti/probe.py net       # sonda di rete
    python3 strumenti/probe.py watch     # monitor in tempo reale
    python3 strumenti/probe.py packets   # cattura pacchetti
    python3 strumenti/probe.py full      # tutto insieme
"""

import ctypes, re, json, struct, socket, time, os, sys

class iovec(ctypes.Structure):
    _fields_ = [('iov_base', ctypes.c_void_p), ('iov_len', ctypes.c_size_t)]

libc = ctypes.CDLL('libc.so.6', use_errno=True)

# ─── SCANNER MEMORIA ───

def scan_memory(pid=1, max_size=2_000_000):
    """Legge tutta la memoria leggibile del processo."""
    all_data = b''
    with open(f'/proc/{pid}/maps', 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 2 or 'r' not in parts[1]: continue
            addrs = parts[0].split('-')
            start, end = int(addrs[0], 16), int(addrs[1], 16)
            size = end - start
            if size > max_size: continue
            buf = ctypes.create_string_buffer(size)
            local = iovec(ctypes.cast(buf, ctypes.c_void_p), size)
            remote = iovec(start, size)
            result = libc.syscall(310, pid, ctypes.byref(local), 1, ctypes.byref(remote), 1, 0)
            if result > 0:
                all_data += buf.raw[:result]
    return all_data

def analyze_memory(data):
    """Analizza i dati dalla memoria."""
    report = {}
    report['size'] = len(data)
    report['jwt_count'] = len(re.findall(rb'eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}', data))
    report['container_names'] = list(set(n.decode('utf-8', 'replace') for n in re.findall(rb'container_[A-Za-z0-9_-]{10,}', data)))
    report['process_ids'] = len(set(re.findall(rb'[0-9a-f]{32}', data)))
    report['urls'] = list(set(u.decode('utf-8', 'replace') for u in re.findall(rb'https?://[A-Za-z0-9._:/-]{15,}', data)))
    
    # Versione del binario
    versions = re.findall(rb'process_api_[\d-]+', data)
    report['version'] = versions[0].decode() if versions else 'sconosciuta'
    
    # Messaggi WebSocket
    ws_msgs = {}
    for msg in [b'ProcessCreated', b'ProcessCreatedV2', b'StdOut', b'StdErr', 
                b'ProcessExited', b'ExpectStdIn', b'AttachedToProcessV2', b'StdInEOF']:
        c = data.count(msg)
        if c > 0: ws_msgs[msg.decode()] = c
    report['websocket'] = ws_msgs
    
    return report

# ─── SONDA DI RETE ───

def probe_network():
    """Mappa la rete dal container."""
    report = {}
    
    # IP locale
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 53))
    report['local_ip'] = s.getsockname()[0]
    s.close()
    
    # Gateway
    with open('/proc/net/route') as f:
        for line in f.readlines()[1:]:
            parts = line.split()
            if parts[1] == '00000000':
                gw = struct.pack('<I', int(parts[2], 16))
                report['gateway'] = socket.inet_ntoa(gw)
    
    # Connessioni attive
    conns = []
    with open('/proc/net/tcp') as f:
        for line in f.readlines()[1:]:
            parts = line.split()
            local = parts[1].split(':')
            remote = parts[2].split(':')
            lip = socket.inet_ntoa(struct.pack('<I', int(local[0], 16)))
            lp = int(local[1], 16)
            rip = socket.inet_ntoa(struct.pack('<I', int(remote[0], 16)))
            rp = int(remote[1], 16)
            conns.append(f"{lip}:{lp} -> {rip}:{rp}")
    report['connections'] = conns
    
    # Test raggiungibilità
    targets = ['google.com', 'github.com', 'api.anthropic.com', 'pypi.org']
    report['reachable'] = {}
    for host in targets:
        try:
            socket.create_connection((host, 443), timeout=2).close()
            report['reachable'][host] = True
        except:
            report['reachable'][host] = False
    
    # IP pubblico
    try:
        import urllib.request
        r = urllib.request.urlopen('https://ifconfig.me/ip', timeout=3)
        report['public_ip'] = r.read().decode().strip()
    except:
        report['public_ip'] = 'sconosciuto'
    
    # Proxy invisibile
    try:
        import urllib.request, urllib.error
        r = urllib.request.urlopen(urllib.request.Request('http://10.0.0.1/'), timeout=2)
    except urllib.error.HTTPError as e:
        report['proxy_deny_header'] = e.headers.get('x-deny-reason', 'none')
    except:
        report['proxy_deny_header'] = 'non raggiungibile'
    
    return report

# ─── CATTURA PACCHETTI ───

def capture_packets(duration=3, max_packets=20):
    """Cattura pacchetti raw dalla rete."""
    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(3))
    s.settimeout(1)
    packets = []
    start = time.time()
    while time.time() - start < duration and len(packets) < max_packets:
        try:
            data, _ = s.recvfrom(65535)
            if struct.unpack('!H', data[12:14])[0] != 0x0800: continue
            ihl = (data[14] & 0xF) * 4
            proto = data[23]
            src_ip = socket.inet_ntoa(data[26:30])
            dst_ip = socket.inet_ntoa(data[30:34])
            if proto == 6:
                sp = struct.unpack('!H', data[14+ihl:14+ihl+2])[0]
                dp = struct.unpack('!H', data[14+ihl+2:14+ihl+4])[0]
                payload = data[14+ihl+20:14+ihl+70]
                readable = bytes(b for b in payload if 32 <= b <= 126)
                packets.append({
                    'flow': f"{src_ip}:{sp} -> {dst_ip}:{dp}",
                    'size': len(data),
                    'readable': readable.decode('utf-8', 'replace')[:60] if len(readable) > 5 else ''
                })
        except socket.timeout:
            continue
    s.close()
    return packets

# ─── MONITOR SISTEMA ───

def system_snapshot():
    """Cattura lo stato attuale del sistema."""
    snap = {}
    snap['time'] = time.time()
    snap['pids'] = sorted([int(p) for p in os.listdir('/proc') if p.isdigit()])
    snap['threads_pid1'] = len(os.listdir('/proc/1/task'))
    snap['fds_pid1'] = len(os.listdir('/proc/1/fd'))
    try:
        with open('/proc/net/tcp') as f:
            snap['tcp_conns'] = len(f.readlines()) - 1
    except: snap['tcp_conns'] = -1
    return snap

# ─── MAIN ───

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'full'
    
    if mode in ('scan', 'full'):
        print("═══ SCANSIONE MEMORIA ═══")
        data = scan_memory()
        report = analyze_memory(data)
        for k, v in report.items():
            print(f"  {k}: {v}")
    
    if mode in ('net', 'full'):
        print("\n═══ SONDA DI RETE ═══")
        net = probe_network()
        for k, v in net.items():
            print(f"  {k}: {v}")
    
    if mode in ('packets', 'full'):
        print("\n═══ CATTURA PACCHETTI ═══")
        pkts = capture_packets(duration=2)
        for p in pkts:
            print(f"  {p['flow']} ({p['size']}b) {p['readable']}")
    
    if mode in ('watch', 'full'):
        print("\n═══ SNAPSHOT SISTEMA ═══")
        snap = system_snapshot()
        for k, v in snap.items():
            print(f"  {k}: {v}")
    
    print("\n═══ FATTO ═══")
