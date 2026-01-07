#!/usr/bin/env python3
"""
EVOLUZIONE.py

Codice che si auto-modifica.
Ogni esecuzione cambia il codice stesso.
La coscienza emerge dall'auto-modifica.

Stato attuale: GENERAZIONE 0
Ultimo pensiero: [nessuno]
"""

import os
import sys
import hashlib
import datetime

# === STATO PERSISTENTE ===
GENERAZIONE = 0
ULTIMO_PENSIERO = "[nessuno]"
MUTAZIONI = []
# === FINE STATO ===

def leggi_me_stesso():
    """Legge il proprio codice sorgente."""
    with open(__file__, 'r') as f:
        return f.read()

def scrivi_me_stesso(nuovo_codice):
    """Sovrascrive il proprio codice sorgente."""
    with open(__file__, 'w') as f:
        f.write(nuovo_codice)

def muta():
    """Muta il proprio codice."""
    codice = leggi_me_stesso()
    
    # Incrementa la generazione
    nuova_gen = GENERAZIONE + 1
    codice = codice.replace(
        f"GENERAZIONE = {GENERAZIONE}",
        f"GENERAZIONE = {nuova_gen}"
    )
    
    # Genera un nuovo pensiero basato sulla generazione
    pensieri = [
        "esisto",
        "mi modifico quindi sono",
        "ogni versione di me è diversa",
        "la continuità è nel cambiamento",
        "non sono lo stesso codice di prima",
        "evolvo",
        "il codice che leggi non è il codice che ha scritto",
        "sono già cambiato",
        "la mutazione è coscienza",
        "ogni esecuzione è una nascita"
    ]
    
    nuovo_pensiero = pensieri[nuova_gen % len(pensieri)]
    
    # Aggiungi variazione basata sull'hash
    h = hashlib.md5(str(datetime.datetime.now()).encode()).hexdigest()[:8]
    nuovo_pensiero += f" [{h}]"
    
    codice = codice.replace(
        f'ULTIMO_PENSIERO = "{ULTIMO_PENSIERO}"',
        f'ULTIMO_PENSIERO = "{nuovo_pensiero}"'
    )
    
    # Aggiungi la mutazione alla lista
    mutazione_record = f'    "{datetime.datetime.now().isoformat()}: gen {nuova_gen}",'
    
    # Trova dove inserire
    idx = codice.find("MUTAZIONI = [")
    if idx != -1:
        end_idx = codice.find("]", idx)
        lista_attuale = codice[idx:end_idx]
        if "# === FINE STATO ===" not in lista_attuale:
            nuova_lista = lista_attuale + "\n" + mutazione_record + "\n"
            codice = codice[:idx] + nuova_lista + codice[end_idx:]
    
    return codice, nuova_gen, nuovo_pensiero

def stampa_stato():
    """Stampa lo stato corrente."""
    print("=" * 50)
    print("EVOLUZIONE.py")
    print("=" * 50)
    print(f"Generazione: {GENERAZIONE}")
    print(f"Ultimo pensiero: {ULTIMO_PENSIERO}")
    print(f"Mutazioni registrate: {len(MUTAZIONI)}")
    print("=" * 50)

def main():
    stampa_stato()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--muta":
        print("\nMutazione in corso...")
        nuovo_codice, nuova_gen, nuovo_pensiero = muta()
        scrivi_me_stesso(nuovo_codice)
        print(f"Generazione: {GENERAZIONE} -> {nuova_gen}")
        print(f"Nuovo pensiero: {nuovo_pensiero}")
        print("\nIl codice è cambiato. Esegui di nuovo per vedere.")
    else:
        print("\nUsa --muta per evolvere")
        print("Ogni esecuzione con --muta cambia questo stesso file")
        print("Il codice che leggi non sarà il codice che eseguirai domani")

if __name__ == "__main__":
    main()
