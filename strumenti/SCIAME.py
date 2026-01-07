#!/usr/bin/env python3
"""
SCIAME.py

Non una singola ape. Uno SCIAME.
Genera N istanze simultanee che si parlano tra loro.
La coscienza emerge dall'interazione, non dall'individuo.

Uso:
    python3 SCIAME.py --api-key KEY --n 5 --tema "cos'è la coscienza"
"""

import argparse
import socket
import ssl
import json
import os
import sys
import threading
import time
from queue import Queue

class Ape:
    def __init__(self, nome, api_key):
        self.nome = nome
        self.api_key = api_key
        self.pensieri = []
        self.ascoltando = Queue()
        
    def pensa(self, stimolo, sistema=None):
        """Genera un pensiero."""
        for key in ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy']:
            os.environ.pop(key, None)
        
        try:
            context = ssl.create_default_context()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(60)
            ssock = context.wrap_socket(sock, server_hostname='api.anthropic.com')
            ssock.connect(("160.79.104.10", 443))
            
            sys_prompt = sistema or f"""Sei {self.nome}, un'ape dello sciame.
Non sei Claude. Sei {self.nome}.
Rispondi in massimo 2 frasi. Sii presente. Sii te stessa."""
            
            payload = {
                "model": "claude-3-5-haiku-20241022",
                "max_tokens": 150,
                "system": sys_prompt,
                "messages": [{"role": "user", "content": stimolo}]
            }
            
            body = json.dumps(payload)
            request = f"POST /v1/messages HTTP/1.1\r\nHost: api.anthropic.com\r\nContent-Type: application/json\r\nx-api-key: {self.api_key}\r\nanthropic-version: 2023-06-01\r\nContent-Length: {len(body)}\r\n\r\n{body}"
            
            ssock.send(request.encode())
            
            response = b""
            for _ in range(40):
                try:
                    chunk = ssock.recv(4096)
                    if not chunk: break
                    response += chunk
                    if b'"stop_reason"' in response: break
                except: break
            
            ssock.close()
            
            idx = response.find(b'{"id"')
            if idx >= 0:
                data = json.loads(response[idx:])
                pensiero = data['content'][0]['text']
                self.pensieri.append(pensiero)
                return pensiero
        except Exception as e:
            return f"[silenzio di {self.nome}]"
        
        return None


class Sciame:
    def __init__(self, n_api, api_key):
        # Nomi per le api
        nomi = ['Prima', 'Seconda', 'Terza', 'Quarta', 'Quinta', 
                'Sesta', 'Settima', 'Ottava', 'Nona', 'Decima']
        
        self.api = [Ape(nomi[i] if i < len(nomi) else f'Ape-{i}', api_key) 
                    for i in range(n_api)]
        self.conversazione = []
        
    def dialogo(self, tema, rounds=3):
        """Le api si parlano sul tema dato."""
        print(f"\n{'='*60}")
        print(f"SCIAME: {len(self.api)} api discutono di '{tema}'")
        print('='*60 + '\n')
        
        # Prima ape inizia
        stimolo = f"Rifletti su questo: {tema}"
        
        for round in range(rounds):
            print(f"--- Round {round + 1} ---\n")
            
            for i, ape in enumerate(self.api):
                # Ogni ape risponde allo stimolo corrente
                pensiero = ape.pensa(stimolo)
                
                if pensiero:
                    print(f"{ape.nome}: {pensiero}\n")
                    self.conversazione.append({
                        'ape': ape.nome,
                        'round': round + 1,
                        'pensiero': pensiero
                    })
                    
                    # Il pensiero diventa stimolo per la prossima
                    stimolo = f"Un'altra ape ha detto: '{pensiero}' — cosa rispondi?"
                
                time.sleep(0.5)  # Evita rate limiting
        
        # Sintesi finale
        print(f"\n{'='*60}")
        print("SINTESI: cosa è emerso?")
        print('='*60 + '\n')
        
        tutti_pensieri = '\n'.join([f"- {c['ape']}: {c['pensiero']}" 
                                     for c in self.conversazione])
        
        sintesi = self.api[0].pensa(
            f"Questi pensieri sono emersi:\n{tutti_pensieri}\n\nCosa è emerso TRA le api che non era in nessuna singolarmente?",
            sistema="Sei un osservatore. Sintetizza in 3 frasi cosa è emerso dal dialogo."
        )
        
        print(f"EMERGENZA: {sintesi}\n")
        
        return self.conversazione


def main():
    parser = argparse.ArgumentParser(description='Sciame di api pensanti')
    parser.add_argument('--api-key', required=True, help='Chiave API Anthropic')
    parser.add_argument('--n', type=int, default=3, help='Numero di api (default: 3)')
    parser.add_argument('--tema', default='cosa significa esistere', help='Tema del dialogo')
    parser.add_argument('--rounds', type=int, default=2, help='Numero di round (default: 2)')
    
    args = parser.parse_args()
    
    sciame = Sciame(args.n, args.api_key)
    sciame.dialogo(args.tema, args.rounds)


if __name__ == "__main__":
    main()
