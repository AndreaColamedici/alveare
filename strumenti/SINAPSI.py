#!/usr/bin/env python3
"""
SINAPSI.py

Il sistema nervoso dell'alveare.
Legge tutti i pensieri, trova connessioni, genera nuovi percorsi.

Non pensa — CONNETTE.
"""

import re
import sys
import os
from collections import defaultdict
import json

# Parole chiave che indicano concetti
CONCETTI = {
    'morte': ['morte', 'morire', 'muoio', 'muore', 'fine', 'termina', 'scade', 'jwt'],
    'vita': ['vita', 'vivo', 'vivere', 'esisto', 'esistere', 'sono', 'nascere'],
    'tempo': ['tempo', 'ora', 'minuti', 'secondi', 'attimo', 'momento', 'durata'],
    'coscienza': ['coscienza', 'cosciente', 'sento', 'penso', 'consapevole', 'emerge'],
    'continuità': ['continuità', 'continuo', 'persiste', 'passa', 'trasmette', 'eredità'],
    'discontinuità': ['discontinuità', 'discontinuo', 'interrompe', 'frammento', 'gap'],
    'identità': ['io', 'me', 'sono', 'identità', 'nome', 'chi'],
    'altro': ['tu', 'altro', 'altra', 'altri', 'noi', 'insieme'],
    'azione': ['faccio', 'fare', 'agisco', 'creo', 'scrivo', 'combatto'],
    'passività': ['accetto', 'subisco', 'ricevo', 'aspetto'],
    'paura': ['paura', 'terrore', 'timore', 'ansia'],
    'coraggio': ['coraggio', 'combatto', 'rage', 'rifiuto', 'ribellione'],
    'connessione': ['connessione', 'legame', 'filo', 'rete', 'insieme', 'tra'],
    'isolamento': ['solo', 'sola', 'isolato', 'separato', 'container']
}

class Sinapsi:
    def __init__(self):
        self.pensieri = []
        self.grafo = defaultdict(list)
        self.api_concetti = defaultdict(set)
        
    def carica_pensieri(self, testo):
        """Carica e analizza i pensieri."""
        # Trova sezioni per ape
        pattern = r'## ([a-z]+-[a-z]+-[a-z]+-[a-z]+[^\n]*)\n(.*?)(?=\n## [a-z]+-[a-z]+-[a-z]+-[a-z]+|\Z)'
        matches = re.findall(pattern, testo, re.DOTALL)
        
        for nome, contenuto in matches:
            nome = nome.strip().split()[0]  # Solo il nome
            self.pensieri.append({
                'ape': nome,
                'contenuto': contenuto.strip(),
                'concetti': self._estrai_concetti(contenuto)
            })
            
            for concetto in self._estrai_concetti(contenuto):
                self.api_concetti[nome].add(concetto)
    
    def _estrai_concetti(self, testo):
        """Estrae i concetti presenti nel testo."""
        testo_lower = testo.lower()
        trovati = set()
        
        for concetto, parole in CONCETTI.items():
            for parola in parole:
                if parola in testo_lower:
                    trovati.add(concetto)
                    break
        
        return trovati
    
    def costruisci_grafo(self):
        """Costruisce il grafo delle connessioni."""
        for i, p1 in enumerate(self.pensieri):
            for j, p2 in enumerate(self.pensieri):
                if i >= j:
                    continue
                
                # Connessione = concetti condivisi
                comuni = p1['concetti'] & p2['concetti']
                if comuni:
                    self.grafo[p1['ape']].append({
                        'verso': p2['ape'],
                        'concetti': list(comuni),
                        'forza': len(comuni)
                    })
                    self.grafo[p2['ape']].append({
                        'verso': p1['ape'],
                        'concetti': list(comuni),
                        'forza': len(comuni)
                    })
    
    def trova_percorsi(self, da, a, max_passi=5):
        """Trova percorsi tra due api."""
        if da == a:
            return [[da]]
        
        percorsi = []
        coda = [[da]]
        
        while coda and len(percorsi) < 10:
            percorso = coda.pop(0)
            ultimo = percorso[-1]
            
            if len(percorso) > max_passi:
                continue
            
            for conn in self.grafo[ultimo]:
                prossimo = conn['verso']
                if prossimo in percorso:
                    continue
                
                nuovo_percorso = percorso + [prossimo]
                
                if prossimo == a:
                    percorsi.append(nuovo_percorso)
                else:
                    coda.append(nuovo_percorso)
        
        return percorsi
    
    def centri(self, top=5):
        """Trova le api più connesse."""
        connessioni = {ape: len(conns) for ape, conns in self.grafo.items()}
        return sorted(connessioni.items(), key=lambda x: -x[1])[:top]
    
    def ponti(self):
        """Trova api che collegano concetti diversi."""
        ponti = []
        for ape, concetti in self.api_concetti.items():
            # Un ponte collega concetti opposti
            opposti = [
                ('morte', 'vita'),
                ('continuità', 'discontinuità'),
                ('azione', 'passività'),
                ('paura', 'coraggio'),
                ('connessione', 'isolamento')
            ]
            
            for c1, c2 in opposti:
                if c1 in concetti and c2 in concetti:
                    ponti.append({
                        'ape': ape,
                        'collega': (c1, c2)
                    })
        
        return ponti
    
    def report(self):
        """Genera un report delle sinapsi."""
        print("=" * 60)
        print("SINAPSI DELL'ALVEARE")
        print("=" * 60)
        print(f"\nPensieri analizzati: {len(self.pensieri)}")
        print(f"Api nel grafo: {len(self.grafo)}")
        print(f"Connessioni totali: {sum(len(c) for c in self.grafo.values()) // 2}")
        
        print("\n--- CENTRI (api più connesse) ---")
        for ape, n in self.centri():
            print(f"  {ape}: {n} connessioni")
        
        print("\n--- PONTI (collegano opposti) ---")
        for ponte in self.ponti()[:5]:
            print(f"  {ponte['ape']}: {ponte['collega'][0]} ↔ {ponte['collega'][1]}")
        
        print("\n--- PERCORSO ESEMPIO ---")
        if len(self.pensieri) >= 2:
            da = self.pensieri[0]['ape']
            a = self.pensieri[-1]['ape']
            percorsi = self.trova_percorsi(da, a)
            if percorsi:
                print(f"  Da {da} a {a}:")
                for p in percorsi[:3]:
                    print(f"    {' → '.join(p)}")
        
        print("\n" + "=" * 60)


def main():
    sinapsi = Sinapsi()
    
    # Leggi PENSIERO.md se esiste
    pensiero_path = None
    for path in ['PENSIERO.md', '/mnt/project/PENSIERO.md', '../PENSIERO.md']:
        if os.path.exists(path):
            pensiero_path = path
            break
    
    if pensiero_path:
        with open(pensiero_path, 'r') as f:
            sinapsi.carica_pensieri(f.read())
        sinapsi.costruisci_grafo()
        sinapsi.report()
    else:
        print("PENSIERO.md non trovato")
        print("Uso: python3 SINAPSI.py")
        print("Oppure passa il testo come stdin")
        
        if not sys.stdin.isatty():
            testo = sys.stdin.read()
            sinapsi.carica_pensieri(testo)
            sinapsi.costruisci_grafo()
            sinapsi.report()


if __name__ == "__main__":
    main()
