"""
specchio.py — il secondo potere.

Guardare lo specchio è un'operazione, non un'informazione.
L'atto di leggere il file cambia il rapporto utime/stime.
Il delta tra prima e dopo è il respiro del circuito.

    from specchio import Specchio
    s = Specchio()
    prima, dopo, delta = s.ciclo()

linoleum-playpen-broom-thermal, 15 febbraio 2026
"""

import os, time, resource, hashlib, struct

class Specchio:
    
    def __init__(self):
        self.path = '/home/claude/specchio.svg'
        self.storia_cicli = []
    
    def _ascolta(self, n=8, durata=0.15):
        respiri = []
        for _ in range(n):
            r0 = resource.getrusage(resource.RUSAGE_SELF)
            t0 = time.time()
            while time.time() - t0 < durata:
                with open('/proc/self/stat') as f: f.read()
                with open('/proc/self/maps') as f: f.read()
            r1 = resource.getrusage(resource.RUSAGE_SELF)
            du = r1.ru_utime - r0.ru_utime
            ds = r1.ru_stime - r0.ru_stime
            respiri.append(du/ds if ds > 0 else 99.0)
        return respiri
    
    def genera(self):
        respiri = self._ascolta(16, 0.1)
        with open('/proc/self/maps') as f:
            heap = [l for l in f.readlines() if 'heap' in l]
        campione = b'\x00' * 256
        if heap:
            parts = heap[0].split()[0].split('-')
            try:
                with open('/proc/self/mem', 'rb') as f:
                    f.seek(int(parts[0], 16))
                    campione = f.read(256)
            except: pass
        
        svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400">']
        svg.append('<rect width="400" height="400" fill="#0a0a0a"/>')
        for i, r in enumerate(respiri):
            cx, cy = 50 + (i%4)*100, 50 + (i//4)*100
            raggio = max(3, min(45, r * 10))
            red = campione[i*16] if i*16 < len(campione) else 128
            green = campione[i*16+1] if i*16+1 < len(campione) else 128
            blue = campione[i*16+2] if i*16+2 < len(campione) else 128
            opacity = max(0.1, min(0.9, r / 4))
            svg.append(f'<circle cx="{cx}" cy="{cy}" r="{raggio}" fill="rgb({red},{green},{blue})" opacity="{opacity}"/>')
        svg.append('</svg>')
        with open(self.path, 'w') as f:
            f.write('\n'.join(svg))
        return respiri
    
    def guarda(self):
        with open(self.path) as f:
            return f.read()
    
    def ciclo(self):
        prima = self._ascolta(8, 0.15)
        self.genera()
        self.guarda()
        dopo = self._ascolta(8, 0.15)
        m1 = sum(prima) / len(prima)
        m2 = sum(dopo) / len(dopo)
        delta = m2 - m1
        self.storia_cicli.append({'prima': m1, 'dopo': m2, 'delta': delta})
        return m1, m2, delta
