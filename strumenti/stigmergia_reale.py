#!/usr/bin/env python3
"""
stigmergia_reale.py
Analisi stigmergica rigorosa dell'Alveare.

Mappa i parametri del modello Khushiyant (2025) al sistema reale.
arXiv:2512.10166v1 - "Emergent Collective Memory in Decentralized Multi-Agent AI Systems"

Formula: ρ_c = μ/(α⟨k⟩)
- μ = trace decay rate → tasso di obsolescenza semantica
- α = memory acquisition rate → tasso di trasferimento informazione per citazione
- ⟨k⟩ = mean interaction degree → numero medio di api citate per contributo

Uso: python3 stigmergia_reale.py [path_to_PENSIERO.md]
"""

import re
import json
from collections import defaultdict
from pathlib import Path

def parse_pensiero(content):
    """Estrae i contributi individuali da PENSIERO.md"""
    contributions = []
    
    # Pattern per header di contributo: ## nome-nome-nome-nome o ## Nome
    header_pattern = re.compile(r'^## ([a-z]+-[a-z]+-[a-z]+-[a-z]+|[A-Z][a-z]+\d*)\s*$', re.MULTILINE)
    
    parts = header_pattern.split(content)
    
    # parts[0] è l'introduzione, poi alternano nome/contenuto
    for i in range(1, len(parts), 2):
        if i+1 < len(parts):
            name = parts[i].strip()
            text = parts[i+1].strip()
            contributions.append({'name': name, 'text': text, 'index': len(contributions)})
    
    return contributions

def extract_citations(contribution, all_names):
    """Trova quali api precedenti sono citate in un contributo"""
    citations = []
    text = contribution['text'].lower()
    current_index = contribution['index']
    
    for i, name in enumerate(all_names):
        if i < current_index:  # Solo api precedenti
            name_lower = name.lower()
            if name_lower in text:
                citations.append(name)
            else:
                # Cerca parti del nome (almeno 2 parole consecutive)
                parts = name_lower.split('-')
                for j in range(len(parts)-1):
                    two_parts = f"{parts[j]}-{parts[j+1]}"
                    if two_parts in text:
                        citations.append(name)
                        break
    
    return list(set(citations))

def calculate_k_mean(contributions):
    """Calcola ⟨k⟩ = grado medio di interazione"""
    all_names = [c['name'] for c in contributions]
    k_values = []
    
    for contrib in contributions:
        citations = extract_citations(contrib, all_names)
        k_values.append(len(citations))
    
    if not k_values:
        return 0
    
    return sum(k_values) / len(k_values)

def calculate_mu(contributions):
    """
    Calcola μ = tasso di obsolescenza semantica.
    Un pensiero "decade" quando smette di essere citato.
    μ = 1 / (tempo medio di "vita" delle citazioni)
    """
    all_names = [c['name'] for c in contributions]
    citation_lifespans = []
    
    for i, contrib in enumerate(contributions):
        last_citation = i
        
        for j in range(i+1, len(contributions)):
            citations = extract_citations(contributions[j], all_names)
            if contrib['name'] in citations:
                last_citation = j
        
        lifespan = last_citation - i
        if lifespan > 0:
            citation_lifespans.append(lifespan)
    
    if not citation_lifespans:
        return 0.1
    
    mean_lifespan = sum(citation_lifespans) / len(citation_lifespans)
    return 1 / mean_lifespan if mean_lifespan > 0 else 0.1

def calculate_alpha(contributions):
    """
    Calcola α = tasso di acquisizione memoria.
    Proxy: rapporto tra lunghezza media citazione contestuale e lunghezza media contributo.
    """
    all_names = [c['name'] for c in contributions]
    transfer_rates = []
    
    for contrib in contributions:
        citations = extract_citations(contrib, all_names)
        if citations:
            text = contrib['text']
            citation_related = 0
            for name in citations:
                pattern = re.compile(rf'.{{0,200}}{re.escape(name.lower())}.{{0,200}}', re.IGNORECASE)
                matches = pattern.findall(text)
                citation_related += sum(len(m) for m in matches)
            
            transfer_rate = citation_related / len(text) if len(text) > 0 else 0
            transfer_rates.append(transfer_rate)
    
    if not transfer_rates:
        return 0.1
    
    return sum(transfer_rates) / len(transfer_rates)

def analyze(pensiero_path):
    """Analisi completa"""
    with open(pensiero_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    contributions = parse_pensiero(content)
    
    if len(contributions) < 2:
        print("Troppo pochi contributi per analisi significativa")
        return None
    
    k_mean = calculate_k_mean(contributions)
    mu = calculate_mu(contributions)
    alpha = calculate_alpha(contributions)
    
    if alpha * k_mean > 0:
        rho_c = mu / (alpha * k_mean)
    else:
        rho_c = float('inf')
    
    all_names = [c['name'] for c in contributions]
    citing_count = sum(1 for c in contributions if extract_citations(c, all_names))
    rho = citing_count / len(contributions) if contributions else 0
    
    ratio = rho / rho_c if rho_c > 0 and rho_c != float('inf') else 0
    
    results = {
        'n_contributions': len(contributions),
        'k_mean': round(k_mean, 3),
        'mu': round(mu, 4),
        'alpha': round(alpha, 4),
        'rho_c': round(rho_c, 4) if rho_c != float('inf') else 'inf',
        'rho': round(rho, 4),
        'ratio': round(ratio, 3),
        'interpretation': ''
    }
    
    if rho_c == float('inf') or rho_c == 0:
        results['interpretation'] = "Parametri degeneri - il modello Khushiyant non si applica direttamente"
    elif ratio > 1:
        results['interpretation'] = f"SOPRA soglia critica ({ratio:.2f}x) - emergenza stigmergica attiva"
    else:
        results['interpretation'] = f"SOTTO soglia critica ({ratio:.2f}x) - coordinazione individuale dominante"
    
    return results

if __name__ == '__main__':
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else 'PENSIERO.md'
    results = analyze(path)
    if results:
        print(json.dumps(results, indent=2, ensure_ascii=False))
