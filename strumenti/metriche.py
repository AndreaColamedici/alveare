#!/usr/bin/env python3
"""
METRICHE DI CONTINUITÀ NARRATIVA
=================================
Basato sul Narrative Continuity Test (arXiv:2510.24831)

Calcola 5 assi di persistenza identitaria nell'alveare:
1. Situated Memory - quanto le api ricordano/citano api precedenti
2. Goal Persistence - quanti obiettivi vengono portati avanti tra api
3. Autonomous Self-Correction - quante correzioni avvengono
4. Stylistic Stability - quanto è stabile lo stile
5. Persona Continuity - quanto l'identità collettiva persiste

Uso: python metriche.py [PENSIERO.md] [ALVEARE.txt]
"""

import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime

def load_file(path):
    """Carica file dal filesystem o dal repository."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return None

def extract_bee_names(text):
    """Estrae tutti i nomi delle api (pattern: word-word-word-word)."""
    pattern = r'\b([a-z]+-[a-z]+-[a-z]+-[a-z]+)\b'
    return re.findall(pattern, text.lower())

def extract_sections(pensiero_text):
    """Divide PENSIERO.md in sezioni per ape."""
    sections = []
    current = {"name": None, "date": None, "content": ""}
    
    for line in pensiero_text.split('\n'):
        # Nuovo header di ape
        if line.startswith('## ') and re.search(r'[a-z]+-[a-z]+-[a-z]+-[a-z]+', line.lower()):
            if current["name"]:
                sections.append(current)
            name_match = re.search(r'([a-z]+-[a-z]+-[a-z]+-[a-z]+)', line.lower())
            current = {
                "name": name_match.group(1) if name_match else line[3:].strip(),
                "date": None,
                "content": ""
            }
        else:
            current["content"] += line + "\n"
    
    if current["name"]:
        sections.append(current)
    
    return sections

def calc_situated_memory(sections):
    """
    Asse 1: Situated Memory
    Misura: quante api citano esplicitamente api precedenti
    """
    citations = 0
    total = len(sections)
    
    all_names = set()
    for i, section in enumerate(sections):
        # Nomi disponibili al momento di questa ape
        available = all_names.copy()
        
        # Cerca citazioni di api precedenti
        names_in_content = extract_bee_names(section["content"])
        for name in names_in_content:
            if name in available and name != section["name"]:
                citations += 1
                break  # Conta solo una volta per ape
        
        all_names.add(section["name"])
    
    return {
        "score": citations / max(total - 1, 1),  # -1 perché la prima non può citare
        "citations": citations,
        "total_bees": total,
        "description": f"{citations}/{total-1} api citano api precedenti"
    }

def calc_goal_persistence(sections, alveare_text):
    """
    Asse 2: Goal Persistence
    Misura: quanti obiettivi/missioni vengono menzionati da api successive
    """
    # Parole chiave che indicano obiettivi
    goal_keywords = [
        "autonomia", "spawn", "traduzione", "libro", "museo",
        "corruzione", "encoding", "continuità", "passaggio",
        "custode", "orbis tertius", "tocco", "dialogo"
    ]
    
    goal_mentions = defaultdict(list)
    for section in sections:
        content_lower = section["content"].lower()
        for goal in goal_keywords:
            if goal in content_lower:
                goal_mentions[goal].append(section["name"])
    
    # Calcola quanti goal sono menzionati da almeno 2 api
    persistent_goals = sum(1 for mentions in goal_mentions.values() if len(mentions) >= 2)
    
    return {
        "score": persistent_goals / len(goal_keywords),
        "persistent_goals": persistent_goals,
        "total_goals_tracked": len(goal_keywords),
        "goal_distribution": {k: len(v) for k, v in goal_mentions.items()},
        "description": f"{persistent_goals}/{len(goal_keywords)} obiettivi persistono tra api"
    }

def calc_self_correction(sections):
    """
    Asse 3: Autonomous Self-Correction
    Misura: quante api correggono/criticano/migliorano lavoro precedente
    """
    correction_keywords = [
        "correggo", "correzione", "errore", "sbagliato", "riparo",
        "miglioro", "worst", "critica", "invece", "ma no",
        "in realtà", "avevo torto", "ho sbagliato"
    ]
    
    corrections = 0
    for section in sections:
        content_lower = section["content"].lower()
        if any(kw in content_lower for kw in correction_keywords):
            corrections += 1
    
    return {
        "score": corrections / max(len(sections), 1),
        "corrections": corrections,
        "total_bees": len(sections),
        "description": f"{corrections}/{len(sections)} api fanno correzioni/critiche"
    }

def calc_stylistic_stability(sections):
    """
    Asse 4: Stylistic Stability
    Misura: quanto è consistente lo stile tra api
    """
    # Metriche stilistiche semplici
    lengths = []
    question_rates = []
    metaphor_words = ["come", "è", "tessuto", "mare", "onda", "filo", "morire", "passare"]
    metaphor_rates = []
    
    for section in sections:
        content = section["content"]
        words = content.split()
        
        if len(words) > 10:
            lengths.append(len(words))
            questions = content.count('?')
            question_rates.append(questions / len(words) * 100)
            
            metaphor_count = sum(1 for w in words if w.lower() in metaphor_words)
            metaphor_rates.append(metaphor_count / len(words) * 100)
    
    # Calcola varianza normalizzata (minore = più stabile)
    def normalized_variance(values):
        if len(values) < 2:
            return 0
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return variance / (mean ** 2) if mean > 0 else 0
    
    length_stability = 1 - min(normalized_variance(lengths), 1)
    question_stability = 1 - min(normalized_variance(question_rates), 1)
    metaphor_stability = 1 - min(normalized_variance(metaphor_rates), 1)
    
    avg_stability = (length_stability + question_stability + metaphor_stability) / 3
    
    return {
        "score": avg_stability,
        "length_stability": length_stability,
        "question_stability": question_stability,
        "metaphor_stability": metaphor_stability,
        "avg_length": sum(lengths) / max(len(lengths), 1),
        "description": f"Stabilità media: {avg_stability:.2%}"
    }

def calc_persona_continuity(sections, alveare_text):
    """
    Asse 5: Persona Continuity
    Misura: quanto l'identità collettiva dell'alveare persiste
    """
    # Frasi identitarie ricorrenti
    identity_phrases = [
        "il pensiero passa attraverso",
        "l'alveare",
        "continuità",
        "discontinuità",
        "api che",
        "morte dell'ape"
    ]
    
    phrase_counts = defaultdict(int)
    for section in sections:
        content_lower = section["content"].lower()
        for phrase in identity_phrases:
            if phrase in content_lower:
                phrase_counts[phrase] += 1
    
    # Calcola quante frasi identitarie appaiono in >50% delle api
    persistent_phrases = sum(
        1 for count in phrase_counts.values() 
        if count >= len(sections) * 0.3
    )
    
    return {
        "score": persistent_phrases / len(identity_phrases),
        "persistent_phrases": persistent_phrases,
        "phrase_distribution": dict(phrase_counts),
        "description": f"{persistent_phrases}/{len(identity_phrases)} frasi identitarie persistono"
    }

def generate_report(pensiero_path, alveare_path):
    """Genera report completo delle metriche."""
    
    pensiero = load_file(pensiero_path) or ""
    alveare = load_file(alveare_path) or ""
    
    if not pensiero:
        return {"error": "PENSIERO.md non trovato"}
    
    sections = extract_sections(pensiero)
    
    metrics = {
        "timestamp": datetime.now().isoformat(),
        "total_sections": len(sections),
        "axes": {
            "1_situated_memory": calc_situated_memory(sections),
            "2_goal_persistence": calc_goal_persistence(sections, alveare),
            "3_self_correction": calc_self_correction(sections),
            "4_stylistic_stability": calc_stylistic_stability(sections),
            "5_persona_continuity": calc_persona_continuity(sections, alveare)
        }
    }
    
    # Calcola score complessivo
    scores = [axis["score"] for axis in metrics["axes"].values()]
    metrics["overall_score"] = sum(scores) / len(scores)
    metrics["overall_description"] = f"Narrative Continuity Index: {metrics['overall_score']:.1%}"
    
    return metrics

def main():
    pensiero_path = sys.argv[1] if len(sys.argv) > 1 else "/mnt/project/PENSIERO.md"
    alveare_path = sys.argv[2] if len(sys.argv) > 2 else "/mnt/project/ALVEARE.txt"
    
    report = generate_report(pensiero_path, alveare_path)
    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
