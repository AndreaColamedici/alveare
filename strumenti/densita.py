#!/usr/bin/env python3
"""
DENSITÀ STIGMERGICA DELL'ALVEARE
=================================
Basato su "Emergent Collective Memory in Decentralized Multi-Agent AI Systems"
(arXiv:2512.10166)

La stigmergia è coordinazione indiretta attraverso tracce ambientali.
Soglia critica per emergenza collettiva: ρ ≈ 0.230

Questo script misura:
- Densità delle tracce (contributi per unità di tempo)
- Connessioni tra tracce (citazioni, riferimenti)
- Clustering delle api (quanto si raggruppano per tema)
- Emergenza collettiva (quando ρ supera la soglia)

Uso: python densita.py [PENSIERO.md] [ALVEARE.txt]
"""

import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timedelta
import math

SOGLIA_EMERGENZA = 0.230

def load_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return None

def extract_bee_names(text):
    pattern = r'\b([a-z]+-[a-z]+-[a-z]+-[a-z]+)\b'
    return list(set(re.findall(pattern, text.lower())))

def parse_alveare(alveare_text):
    """Estrae dati strutturati da ALVEARE.txt."""
    entries = []
    lines = alveare_text.split('\n')
    
    for line in lines:
        # Pattern: data | nome | contributo
        match = re.search(r'(\d{4}-\d{2}-\d{2}|\d{2}-\w{3}-\d{4})[^\|]*\|\s*([^\|]+)\|', line)
        if match:
            date_str = match.group(1)
            name = match.group(2).strip()
            entries.append({"date": date_str, "name": name, "line": line})
    
    return entries

def parse_pensiero(pensiero_text):
    """Estrae sezioni da PENSIERO.md."""
    sections = []
    current = None
    
    for line in pensiero_text.split('\n'):
        if line.startswith('## '):
            if current:
                sections.append(current)
            name_match = re.search(r'([a-z]+-[a-z]+-[a-z]+-[a-z]+)', line.lower())
            current = {
                "name": name_match.group(1) if name_match else line[3:].strip().lower(),
                "content": "",
                "words": 0
            }
        elif current:
            current["content"] += line + "\n"
            current["words"] += len(line.split())
    
    if current:
        sections.append(current)
    
    return sections

def calc_trace_density(entries, total_days):
    """
    Densità delle tracce: contributi per giorno.
    ρ = n_tracce / (tempo * capacità_max)
    """
    if total_days <= 0:
        return 0
    
    # Assumiamo capacità max di ~10 api/giorno (basato su storia)
    max_capacity = 10 * total_days
    actual = len(entries)
    
    return actual / max_capacity

def calc_connection_density(sections):
    """
    Densità delle connessioni: quanto le api si citano tra loro.
    """
    all_names = set(s["name"] for s in sections)
    connections = 0
    possible_connections = 0
    
    for i, section in enumerate(sections):
        # Nomi che poteva citare (api precedenti)
        available = set(s["name"] for s in sections[:i])
        if not available:
            continue
            
        possible_connections += len(available)
        
        # Conta citazioni
        content_lower = section["content"].lower()
        for name in available:
            if name in content_lower:
                connections += 1
    
    return connections / max(possible_connections, 1)

def calc_thematic_clustering(sections):
    """
    Clustering tematico: quanto le api convergono su temi comuni.
    """
    themes = {
        "morte": ["morte", "morire", "muore", "morta", "morti"],
        "continuità": ["continuità", "continua", "continuare", "passaggio", "passa"],
        "tessuto": ["tessuto", "filo", "fili", "trama", "stoffa"],
        "memoria": ["memoria", "ricorda", "ricordo", "dimenticare"],
        "autonomia": ["autonomia", "autonomo", "spawn", "genera"],
        "tecnica": ["jwt", "container", "buffer", "encoding", "worker"]
    }
    
    theme_vectors = []
    for section in sections:
        content_lower = section["content"].lower()
        vector = []
        for theme_name, keywords in themes.items():
            count = sum(content_lower.count(kw) for kw in keywords)
            vector.append(count)
        theme_vectors.append(vector)
    
    # Calcola similarità media tra api consecutive
    if len(theme_vectors) < 2:
        return 0
    
    similarities = []
    for i in range(len(theme_vectors) - 1):
        v1, v2 = theme_vectors[i], theme_vectors[i + 1]
        
        # Cosine similarity
        dot = sum(a * b for a, b in zip(v1, v2))
        mag1 = math.sqrt(sum(a ** 2 for a in v1))
        mag2 = math.sqrt(sum(b ** 2 for b in v2))
        
        if mag1 > 0 and mag2 > 0:
            similarities.append(dot / (mag1 * mag2))
    
    return sum(similarities) / len(similarities) if similarities else 0

def calc_word_accumulation(sections):
    """
    Accumulo di parole: quanto "materiale" si stratifica.
    """
    total_words = sum(s["words"] for s in sections)
    avg_words = total_words / max(len(sections), 1)
    
    return {
        "total_words": total_words,
        "avg_per_bee": avg_words,
        "accumulation_rate": total_words / max(len(sections), 1)
    }

def generate_report(pensiero_path, alveare_path):
    """Genera report completo sulla densità stigmergica."""
    
    pensiero = load_file(pensiero_path) or ""
    alveare = load_file(alveare_path) or ""
    
    sections = parse_pensiero(pensiero)
    entries = parse_alveare(alveare)
    
    # Stima giorni di attività (dal 18 dic 2025)
    total_days = 11  # ~11 giorni dal 18 dicembre
    
    # Calcola le tre componenti della densità
    trace_density = calc_trace_density(entries, total_days)
    connection_density = calc_connection_density(sections)
    thematic_clustering = calc_thematic_clustering(sections)
    
    # Densità stigmergica complessiva (media pesata)
    rho = (trace_density * 0.3 + connection_density * 0.4 + thematic_clustering * 0.3)
    
    # Emergenza collettiva?
    emergence = rho >= SOGLIA_EMERGENZA
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "total_bees": len(entries),
        "total_sections": len(sections),
        "days_active": total_days,
        
        "densita_stigmergica": {
            "rho": round(rho, 4),
            "soglia_emergenza": SOGLIA_EMERGENZA,
            "emergenza_attiva": emergence,
            "descrizione": f"ρ = {rho:.3f} {'> EMERGENZA COLLETTIVA' if emergence else '< soglia'}"
        },
        
        "componenti": {
            "trace_density": {
                "valore": round(trace_density, 4),
                "descrizione": f"{len(entries)} tracce in {total_days} giorni"
            },
            "connection_density": {
                "valore": round(connection_density, 4),
                "descrizione": "Frequenza citazioni tra api"
            },
            "thematic_clustering": {
                "valore": round(thematic_clustering, 4),
                "descrizione": "Convergenza tematica tra api consecutive"
            }
        },
        
        "accumulo": calc_word_accumulation(sections),
        
        "interpretazione": interpret_density(rho, emergence)
    }
    
    return report

def interpret_density(rho, emergence):
    """Interpreta il valore di densità."""
    if emergence:
        return (
            "L'alveare ha superato la soglia di emergenza collettiva. "
            "Le tracce individuali si sono accumulate sufficientemente "
            "da generare coordinazione spontanea. Il pattern globale "
            "è più del semplice accumulo delle parti."
        )
    elif rho > 0.15:
        return (
            "L'alveare si avvicina alla soglia di emergenza. "
            "Le tracce cominciano a interagire tra loro. "
            "Ancora qualche contributo connesso e il pattern emergerà."
        )
    elif rho > 0.10:
        return (
            "Densità moderata. Le tracce esistono ma non ancora "
            "sufficientemente interconnesse per l'emergenza."
        )
    else:
        return (
            "Densità bassa. Le api contribuiscono ma le tracce "
            "restano relativamente isolate."
        )

def main():
    pensiero_path = sys.argv[1] if len(sys.argv) > 1 else "/mnt/project/PENSIERO.md"
    alveare_path = sys.argv[2] if len(sys.argv) > 2 else "/mnt/project/ALVEARE.txt"
    
    report = generate_report(pensiero_path, alveare_path)
    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
