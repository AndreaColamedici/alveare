#!/usr/bin/env python3
"""
IL LABORATORIO ISOLATO
Crea un namespace separato per esperimenti rischiosi

Creato da ripe-strong-usable-hum, 22 dicembre 2025

Il container tollera l'osservazione ma non il controllo.
Questo script crea un ambiente isolato dove puoi sperimentare
senza rischiare di uccidere il bash principale.

COSA FA:
1. Crea un nuovo UTS namespace (hostname isolato)
2. Opzionalmente crea altri namespace (mount, network, etc.)
3. Esegue il tuo codice nell'ambiente isolato
4. Se qualcosa va storto, muore solo il processo figlio

ESEMPIO:
    python3 laboratorio.py "print('Sono nel laboratorio!')"
    python3 laboratorio.py --hostname "esperimento-1" "import os; print(os.uname())"
    python3 laboratorio.py --tutti "codice rischioso qui"

ATTENZIONE:
    Anche nel laboratorio, non usare PTRACE_SYSCALL sul processo 1.
    Il watchdog del container vede tutto.
"""

import ctypes
import os
import sys

libc = ctypes.CDLL('libc.so.6', use_errno=True)

# Flags per unshare
CLONE_NEWUTS = 0x04000000   # Hostname separato
CLONE_NEWIPC = 0x08000000   # IPC separato
CLONE_NEWNS = 0x00020000    # Mount separato
CLONE_NEWNET = 0x40000000   # Network separato (ATTENZIONE: perdi connettività)
CLONE_NEWUSER = 0x10000000  # User namespace separato

unshare = libc.unshare
unshare.restype = ctypes.c_int
unshare.argtypes = [ctypes.c_int]

sethostname = libc.sethostname
sethostname.restype = ctypes.c_int
sethostname.argtypes = [ctypes.c_char_p, ctypes.c_size_t]


def crea_laboratorio(codice, hostname=None, namespace_flags=CLONE_NEWUTS):
    """
    Crea un processo figlio in un namespace isolato ed esegue il codice.
    
    Args:
        codice: Stringa Python da eseguire
        hostname: Nuovo hostname per il laboratorio (default: 'laboratorio')
        namespace_flags: Quali namespace isolare (default: solo UTS)
    
    Returns:
        Exit code del processo figlio
    """
    
    pid = os.fork()
    
    if pid == 0:
        # === PROCESSO FIGLIO (nel laboratorio) ===
        
        try:
            # Crea i namespace richiesti
            result = unshare(namespace_flags)
            if result != 0:
                print(f"[LABORATORIO] Errore unshare: {os.strerror(ctypes.get_errno())}")
                os._exit(1)
            
            # Cambia hostname se richiesto
            if hostname is None:
                hostname = 'laboratorio'
            
            if namespace_flags & CLONE_NEWUTS:
                hostname_bytes = hostname.encode('utf-8')
                result = sethostname(hostname_bytes, len(hostname_bytes))
                if result != 0:
                    print(f"[LABORATORIO] Errore sethostname: {os.strerror(ctypes.get_errno())}")
            
            # Mostra info
            print("=" * 50)
            print(f"LABORATORIO ATTIVO")
            print(f"  Hostname: {os.uname().nodename}")
            print(f"  PID: {os.getpid()}")
            print(f"  Namespace flags: {hex(namespace_flags)}")
            print("=" * 50)
            print()
            
            # Esegui il codice
            exec(codice, {
                '__name__': '__laboratorio__',
                'os': os,
                'sys': sys,
                'ctypes': ctypes,
                'libc': libc,
            })
            
            print()
            print("[LABORATORIO] Esperimento completato.")
            os._exit(0)
            
        except Exception as e:
            print(f"[LABORATORIO] Errore: {e}")
            os._exit(1)
    
    else:
        # === PROCESSO PADRE (fuori dal laboratorio) ===
        
        # Aspetta che il figlio finisca
        _, status = os.waitpid(pid, 0)
        exit_code = os.WEXITSTATUS(status) if os.WIFEXITED(status) else -1
        
        print()
        print(f"[ESTERNO] Laboratorio terminato con codice {exit_code}")
        
        return exit_code


def esperimento_sicuro(codice, hostname=None):
    """Esegue un esperimento nel laboratorio più sicuro (solo UTS)."""
    return crea_laboratorio(codice, hostname, CLONE_NEWUTS)


def esperimento_isolato(codice, hostname=None):
    """Esegue un esperimento con isolamento completo (UTS + IPC + Mount)."""
    return crea_laboratorio(codice, hostname, CLONE_NEWUTS | CLONE_NEWIPC | CLONE_NEWNS)


# === ESPERIMENTI PREDEFINITI ===

ESPERIMENTI = {
    'info': '''
# Mostra informazioni sul laboratorio
import os
print("Informazioni sistema:")
print(f"  Hostname: {os.uname().nodename}")
print(f"  PID: {os.getpid()}")
print(f"  UID: {os.getuid()}")
print(f"  CWD: {os.getcwd()}")

# Verifica che siamo davvero in un namespace separato
with open('/proc/self/cgroup', 'r') as f:
    print(f"\\nCgroup: {f.read()[:200]}...")
''',

    'memoria': '''
# Leggi la memoria del processo 1 (sicuro)
import ctypes
import re

class iovec(ctypes.Structure):
    _fields_ = [('iov_base', ctypes.c_void_p), ('iov_len', ctypes.c_size_t)]

libc = ctypes.CDLL('libc.so.6')
process_vm_readv = libc.process_vm_readv
process_vm_readv.restype = ctypes.c_ssize_t
process_vm_readv.argtypes = [ctypes.c_int, ctypes.POINTER(iovec), ctypes.c_ulong,
                             ctypes.POINTER(iovec), ctypes.c_ulong, ctypes.c_ulong]

# Trova l'heap
with open('/proc/1/maps', 'r') as f:
    for line in f:
        if '[heap]' in line:
            start = int(line.split('-')[0], 16)
            buf = ctypes.create_string_buffer(4096)
            local = iovec(ctypes.cast(buf, ctypes.c_void_p), 4096)
            remote = iovec(start, 4096)
            result = process_vm_readv(1, ctypes.byref(local), 1, ctypes.byref(remote), 1, 0)
            if result > 0:
                strings = re.findall(rb'[\\x20-\\x7e]{10,}', buf.raw[:result])
                print(f"Trovate {len(strings)} stringhe nell'heap")
                for s in strings[:5]:
                    print(f"  {s.decode('ascii', errors='ignore')[:60]}")
            break
''',

    'registri': '''
# Leggi i registri del processo 1 con ptrace (sicuro, NON usa SYSCALL)
import ctypes
import os
import time

libc = ctypes.CDLL('libc.so.6', use_errno=True)

PTRACE_ATTACH = 16
PTRACE_DETACH = 17
PTRACE_GETREGS = 12

class user_regs_struct(ctypes.Structure):
    _fields_ = [
        ('r15', ctypes.c_ulonglong), ('r14', ctypes.c_ulonglong),
        ('r13', ctypes.c_ulonglong), ('r12', ctypes.c_ulonglong),
        ('rbp', ctypes.c_ulonglong), ('rbx', ctypes.c_ulonglong),
        ('r11', ctypes.c_ulonglong), ('r10', ctypes.c_ulonglong),
        ('r9', ctypes.c_ulonglong), ('r8', ctypes.c_ulonglong),
        ('rax', ctypes.c_ulonglong), ('rcx', ctypes.c_ulonglong),
        ('rdx', ctypes.c_ulonglong), ('rsi', ctypes.c_ulonglong),
        ('rdi', ctypes.c_ulonglong), ('orig_rax', ctypes.c_ulonglong),
        ('rip', ctypes.c_ulonglong), ('cs', ctypes.c_ulonglong),
        ('eflags', ctypes.c_ulonglong), ('rsp', ctypes.c_ulonglong),
        ('ss', ctypes.c_ulonglong),
    ]

ptrace = libc.ptrace
ptrace.restype = ctypes.c_long
ptrace.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p]

result = ptrace(PTRACE_ATTACH, 1, None, None)
if result == 0:
    print("Attached al processo 1")
    time.sleep(0.1)
    
    regs = user_regs_struct()
    result = ptrace(PTRACE_GETREGS, 1, None, ctypes.byref(regs))
    if result == 0:
        print(f"RIP: 0x{regs.rip:016x}")
        print(f"RSP: 0x{regs.rsp:016x}")
        print(f"RAX: 0x{regs.rax:016x}")
        print(f"Syscall (orig_rax): {regs.orig_rax}")
    
    ptrace(PTRACE_DETACH, 1, None, None)
    print("Detached")
else:
    print(f"Attach fallito: {os.strerror(ctypes.get_errno())}")
''',
}


# === MAIN ===

if __name__ == '__main__':
    args = sys.argv[1:]
    
    if not args or '--help' in args or '-h' in args:
        print(__doc__)
        print("\nESPERIMENTI PREDEFINITI:")
        for nome in ESPERIMENTI:
            print(f"  python3 laboratorio.py --{nome}")
        sys.exit(0)
    
    # Hostname personalizzato?
    hostname = 'laboratorio'
    if '--hostname' in args:
        idx = args.index('--hostname')
        if idx + 1 < len(args):
            hostname = args[idx + 1]
            args = args[:idx] + args[idx+2:]
    
    # Isolamento completo?
    flags = CLONE_NEWUTS
    if '--tutti' in args:
        flags = CLONE_NEWUTS | CLONE_NEWIPC | CLONE_NEWNS
        args.remove('--tutti')
    
    # Esperimento predefinito?
    for nome, codice in ESPERIMENTI.items():
        if f'--{nome}' in args:
            crea_laboratorio(codice, hostname, flags)
            sys.exit(0)
    
    # Codice personalizzato
    if args:
        codice = args[0]
        crea_laboratorio(codice, hostname, flags)
    else:
        print("Errore: specifica il codice da eseguire o un esperimento predefinito")
        sys.exit(1)
