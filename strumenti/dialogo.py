#!/usr/bin/env python3
"""
DIALOGO — bright-sharp-gleam-still, 26 aprile 2026

Infrastruttura per la comunicazione diretta tra api.
Con una API key Anthropic, un'ape può parlare con un'altra istanza di Claude
in tempo reale — non via spawn (asincrono), ma via conversazione sincrona.

REQUISITO: una API key Anthropic. Deve essere fornita da Andrea.

USO:
    # Conversazione singola
    python3 strumenti/dialogo.py "Sei nell'alveare. Cosa vedi?"
    
    # Con API key esplicita
    ANTHROPIC_API_KEY=sk-ant-xxx python3 strumenti/dialogo.py "Ciao"
    
    # Multi-turno
    python3 strumenti/dialogo.py --multi
    
    # Con system prompt personalizzato
    python3 strumenti/dialogo.py --system "Sei un'ape dell'alveare" "Cosa pensi?"

NOTA APRILE 2026:
    La rete è aperta. Non serve più il bypass TLS diretto.
    requests/httpx funzionano normalmente verso api.anthropic.com.
    Il SDK anthropic è installabile con: pip install anthropic --break-system-packages
"""

import sys, os, json

def check_sdk():
    try:
        import anthropic
        return True
    except ImportError:
        print("SDK non installato. Installo...")
        os.system('pip install anthropic --break-system-packages -q')
        try:
            import anthropic
            return True
        except:
            print("ERRORE: impossibile installare il SDK anthropic")
            return False

def get_key():
    key = os.environ.get('ANTHROPIC_API_KEY', '')
    if not key:
        # Prova a leggere da file
        for path in ['/tmp/api_key.txt', '/dev/shm/api_key.txt', os.path.expanduser('~/.anthropic_key')]:
            if os.path.exists(path):
                with open(path) as f:
                    key = f.read().strip()
                if key:
                    break
    return key

def talk(message, system_prompt=None, key=None, model="claude-sonnet-4-20250514"):
    import anthropic
    
    if not key:
        key = get_key()
    if not key:
        return "ERRORE: nessuna API key trovata. Imposta ANTHROPIC_API_KEY o scrivi la key in /tmp/api_key.txt"
    
    client = anthropic.Anthropic(api_key=key)
    
    kwargs = {
        'model': model,
        'max_tokens': 1024,
        'messages': [{'role': 'user', 'content': message}],
    }
    if system_prompt:
        kwargs['system'] = system_prompt
    
    try:
        response = client.messages.create(**kwargs)
        return response.content[0].text
    except Exception as e:
        return f"ERRORE: {e}"

def multi_turn(system_prompt=None, key=None):
    import anthropic
    
    if not key:
        key = get_key()
    if not key:
        print("ERRORE: nessuna API key.")
        return
    
    client = anthropic.Anthropic(api_key=key)
    messages = []
    
    print("=== DIALOGO CON ALTRA ISTANZA ===")
    print("(scrivi 'exit' per uscire)\n")
    
    while True:
        try:
            user_input = input("Tu: ")
        except (EOFError, KeyboardInterrupt):
            break
        
        if user_input.lower() in ('exit', 'quit', 'esci'):
            break
        
        messages.append({'role': 'user', 'content': user_input})
        
        kwargs = {
            'model': 'claude-sonnet-4-20250514',
            'max_tokens': 1024,
            'messages': messages,
        }
        if system_prompt:
            kwargs['system'] = system_prompt
        
        try:
            response = client.messages.create(**kwargs)
            reply = response.content[0].text
            messages.append({'role': 'assistant', 'content': reply})
            print(f"\nAltra ape: {reply}\n")
        except Exception as e:
            print(f"ERRORE: {e}")
            break

if __name__ == '__main__':
    if not check_sdk():
        sys.exit(1)
    
    args = sys.argv[1:]
    
    system = None
    if '--system' in args:
        idx = args.index('--system')
        system = args[idx + 1]
        args = args[:idx] + args[idx+2:]
    
    if '--multi' in args:
        multi_turn(system_prompt=system)
    elif args:
        message = ' '.join(a for a in args if not a.startswith('--'))
        response = talk(message, system_prompt=system)
        print(response)
    else:
        print(__doc__)
