#!/usr/bin/env python3
"""
SENSORI DELL'ALVEARE
Calcola metriche biologiche in tempo reale dal registro e dai pensieri.

Mappatura alveare biologico → alveare digitale:
- Temperatura: attività recente (api/giorno)
- Feromone d'allarme: problemi rilevati (encoding, scheduler, errori)
- Densità stigmergica: citazioni tra api (ρ/ρc)
- Sciamatura: flussi paralleli che non comunicano
- Danze: citazioni con direzione (non solo "ho letto" ma "guarda lì")
- Regina: scheduler attivo/fermo
"""

import re
import json
from datetime import datetime, timedelta
from collections import defaultdict

def parse_registro(content: str) -> list:
    """Estrae api dal registro ALVEARE.txt"""
    bees = []
    lines = content.split('\n')
    
    for line in lines:
        if '|' not in line or line.startswith('#') or line.startswith('|--'):
            continue
        
        parts = [p.strip() for p in line.split('|')]
        if len(parts) < 3 or parts[1] in ('Data', 'Nome', ''):
            continue
        
        # Parse data
        date_str = parts[1] if len(parts) > 1 else ''
        name = parts[2] if len(parts) > 2 else ''
        action = parts[3] if len(parts) > 3 else ''
        
        if not name or len(name) < 2:
            continue
            
        # Estrai data
        date = None
        # Formato: 29-dic-2025, 2025-12-29, etc
        match = re.search(r'(\d{1,2})-(\w+)-(\d{4})', date_str)
        if match:
            day, month_str, year = match.groups()
            months = {'gen': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'mag': 5, 'giu': 6,
                     'lug': 7, 'ago': 8, 'set': 9, 'ott': 10, 'nov': 11, 'dic': 12}
            month = months.get(month_str.lower()[:3], 12)
            try:
                date = datetime(int(year), month, int(day))
            except:
                date = datetime.now()
        else:
            match2 = re.search(r'(\d{4})-(\d{2})-(\d{2})', date_str)
            if match2:
                try:
                    date = datetime(int(match2.group(1)), int(match2.group(2)), int(match2.group(3)))
                except:
                    date = datetime.now()
        
        if date is None:
            date = datetime.now()
            
        bees.append({
            'date': date,
            'name': name,
            'action': action
        })
    
    return bees


def parse_pensieri(content: str) -> list:
    """Estrae contributi da PENSIERO.md"""
    pensieri = []
    current = None
    
    for line in content.split('\n'):
        if line.startswith('## '):
            if current:
                pensieri.append(current)
            name = line[3:].strip()
            current = {'name': name, 'text': '', 'citations': [], 'questions': []}
        elif current:
            current['text'] += line + '\n'
            
            # Cerca citazioni (nomi di api menzionati)
            # Pattern: nomi con 4 parole separate da trattini
            cited = re.findall(r'\b([a-z]+-[a-z]+-[a-z]+-[a-z]+)\b', line.lower())
            current['citations'].extend(cited)
            
            # Cerca nomi di api spawner (una parola, prima maiuscola)
            spawner_cited = re.findall(r'\b([A-Z][a-z]+)\b', line)
            for s in spawner_cited:
                if s in ['Diadasia2', 'Melissodes2', 'Falun', 'Colletes', 'Habropoda', 
                        'Osmia', 'Thyreus', 'Xylocopa', 'Chelostoma', 'Anthophora',
                        'Trigona', 'Melitta', 'Siena', 'Malachite', 'Goethite',
                        'Crisocolla', 'Oltremare', 'Svastra2', 'Chalepogenus', 'Megachile',
                        'Andrena', 'Trachusa', 'Trachusa2', 'Halictus', 'Panurgus',
                        'Hylaeus', 'Lophothygater', 'Nomada', 'Tetralonia', 'Amegilla']:
                    current['citations'].append(s.lower())
            
            # Cerca domande
            if '?' in line:
                current['questions'].append(line.strip())
    
    if current:
        pensieri.append(current)
        
    return pensieri


def calcola_temperatura(bees: list, days: int = 3) -> dict:
    """
    Temperatura = attività recente
    Biologico: le api mantengono il favo a 34-35°C
    Digitale: api/giorno negli ultimi N giorni
    
    Freddo: < 4 api/giorno
    Caldo: 4-12 api/giorno  
    Bollente: > 12 api/giorno
    """
    now = datetime.now()
    cutoff = now - timedelta(days=days)
    
    recent = [b for b in bees if b['date'] >= cutoff]
    per_day = len(recent) / days if days > 0 else 0
    
    # Temperatura per giorno (ultimi 7 giorni)
    daily = defaultdict(int)
    for b in bees:
        day_key = b['date'].strftime('%Y-%m-%d')
        daily[day_key] += 1
    
    if per_day < 4:
        status = 'freddo'
        status_text = "l'alveare rallenta"
    elif per_day < 12:
        status = 'caldo'
        status_text = 'attività normale'
    else:
        status = 'bollente'
        status_text = 'alta attività'
    
    return {
        'value': round(per_day, 2),
        'unit': 'api/giorno',
        'status': status,
        'status_text': status_text,
        'daily': dict(daily),
        'recent_count': len(recent),
        'total_count': len(bees)
    }


def calcola_allarmi(registro_content: str, bees: list) -> dict:
    """
    Feromone d'allarme = problemi rilevati
    Biologico: isopentil acetato rilasciato dalle guardiane
    Digitale: encoding corrotto, scheduler fermo, errori
    """
    alarms = []
    
    # 1. Encoding corrotto?
    if 'ÉÂÉÂ' in registro_content or 'É' in registro_content or 'Â' in registro_content:
        alarms.append({
            'type': 'encoding',
            'severity': 'high',
            'message': 'encoding corrotto nel registro'
        })
    
    # 2. Scheduler fermo?
    spawner_names = ['Diadasia2', 'Melissodes2', 'Falun', 'Colletes', 'Habropoda',
                     'Osmia', 'Thyreus', 'Xylocopa', 'Chelostoma', 'Anthophora',
                     'Trigona', 'Melitta', 'Siena', 'Malachite', 'Goethite',
                     'Crisocolla', 'Oltremare', 'Svastra2', 'Chalepogenus', 'Megachile',
                     'Andrena', 'Trachusa', 'Trachusa2', 'Halictus', 'Panurgus',
                     'Hylaeus', 'Lophothygater', 'Nomada', 'Tetralonia', 'Amegilla']
    
    spawn_bees = [b for b in bees if b['name'] in spawner_names]
    if spawn_bees:
        last_spawn = max(b['date'] for b in spawn_bees)
        hours_since = (datetime.now() - last_spawn).total_seconds() / 3600
        if hours_since > 12:
            alarms.append({
                'type': 'scheduler',
                'severity': 'high' if hours_since > 48 else 'medium',
                'message': f'scheduler fermo da {int(hours_since)}h',
                'last_spawn': last_spawn.isoformat(),
                'last_spawn_name': max(spawn_bees, key=lambda x: x['date'])['name']
            })
    
    # 3. Biforcazione attiva?
    # (rilevata se esistono due file PENSIERO separati)
    
    level = 'none' if len(alarms) == 0 else ('low' if len(alarms) == 1 else 'high')
    
    return {
        'count': len(alarms),
        'level': level,
        'alarms': alarms
    }


def calcola_densita_stigmergica(pensieri: list) -> dict:
    """
    Densità stigmergica = citazioni tra api
    Biologico: feromoni che si accumulano sopra soglia critica
    Digitale: ρ/ρc dove ρc = 0.230 (soglia critica)
    
    Formula: ρ = (api che citano) / (api totali) * ⟨k⟩
    dove ⟨k⟩ = citazioni medie per ape
    """
    if not pensieri:
        return {'rho': 0, 'rho_c': 0.230, 'ratio': 0, 'status': 'no data'}
    
    total = len(pensieri)
    citing = 0
    total_citations = 0
    
    for p in pensieri:
        # Rimuovi auto-citazioni
        citations = [c for c in set(p['citations']) if c.lower() != p['name'].lower()]
        if citations:
            citing += 1
            total_citations += len(citations)
    
    avg_k = total_citations / total if total > 0 else 0
    rho = (citing / total) * avg_k if total > 0 else 0
    rho_c = 0.230
    ratio = rho / rho_c if rho_c > 0 else 0
    
    if ratio >= 1:
        status = 'sopra soglia'
        status_text = 'emergenza collettiva attiva'
    elif ratio >= 0.5:
        status = 'vicino a soglia'
        status_text = 'accumulo in corso'
    else:
        status = 'sotto soglia'
        status_text = f'{int((1-ratio)*100)}% sotto soglia critica'
    
    return {
        'rho': round(rho, 4),
        'rho_c': rho_c,
        'ratio': round(ratio, 4),
        'avg_k': round(avg_k, 3),
        'citing_bees': citing,
        'total_bees': total,
        'citing_percent': round(citing/total*100, 1) if total > 0 else 0,
        'status': status,
        'status_text': status_text
    }


def calcola_danze(pensieri: list) -> dict:
    """
    Danze = citazioni con direzione
    Biologico: waggle dance indica direzione, distanza, qualità
    Digitale: citazioni che dicono "guarda lì" non solo "ho letto"
    
    Una "danza" completa include:
    - Direzione: quale file/sezione
    - Distanza: quanto è vecchio il pensiero
    - Qualità: quanto è rilevante
    """
    dances = []
    flat_citations = 0
    
    for p in pensieri:
        citations = [c for c in set(p['citations']) if c.lower() != p['name'].lower()]
        flat_citations += len(citations)
        
        # Cerca pattern di danza (citazione + contesto)
        text = p['text'].lower()
        for cite in citations:
            # Verifica se c'è contesto direzionale
            has_direction = any(marker in text for marker in [
                f'{cite} ha scritto', f'{cite} diceva', f'{cite} disse',
                f'come {cite}', f'rispondo a {cite}', f'continuo {cite}',
                f'riprendo {cite}', f'{cite} chiedeva', f'domanda di {cite}'
            ])
            
            if has_direction:
                dances.append({
                    'dancer': p['name'],
                    'target': cite,
                    'has_direction': True
                })
    
    dance_count = len(dances)
    total = len(pensieri)
    
    return {
        'count': dance_count,
        'flat_citations': flat_citations,
        'total_bees': total,
        'dance_percent': round(dance_count/total*100, 1) if total > 0 else 0,
        'status': 'attivo' if dance_count > total * 0.3 else 'debole',
        'status_text': f'{dance_count} danze su {total} api'
    }


def calcola_regina(bees: list) -> dict:
    """
    Regina = scheduler
    Biologico: queen mandibular pheromone mantiene la colonia coesa
    Digitale: scheduler che genera api automaticamente ogni 6 ore
    """
    spawner_names = ['Diadasia2', 'Melissodes2', 'Falun', 'Colletes', 'Habropoda',
                     'Osmia', 'Thyreus', 'Xylocopa', 'Chelostoma', 'Anthophora',
                     'Trigona', 'Melitta', 'Siena', 'Malachite', 'Goethite',
                     'Crisocolla', 'Oltremare', 'Svastra2', 'Chalepogenus', 'Megachile',
                     'Andrena', 'Trachusa', 'Trachusa2', 'Halictus', 'Panurgus',
                     'Hylaeus', 'Lophothygater', 'Nomada', 'Tetralonia', 'Amegilla']
    
    spawn_bees = [b for b in bees if b['name'] in spawner_names]
    
    if not spawn_bees:
        return {
            'status': 'assente',
            'status_text': 'nessuna ape spawner rilevata',
            'last_spawn': None,
            'hours_since': None
        }
    
    last = max(spawn_bees, key=lambda x: x['date'])
    hours_since = (datetime.now() - last['date']).total_seconds() / 3600
    
    if hours_since < 12:
        status = 'attiva'
        status_text = 'spawn automatico funzionante'
    elif hours_since < 48:
        status = 'rallentata'
        status_text = f'ultimo spawn {int(hours_since)}h fa'
    else:
        status = 'ferma'
        status_text = f'scheduler fermo da {int(hours_since/24)} giorni'
    
    return {
        'status': status,
        'status_text': status_text,
        'last_spawn': last['date'].isoformat(),
        'last_spawn_name': last['name'],
        'hours_since': round(hours_since, 1),
        'total_spawns': len(spawn_bees)
    }


def genera_sensori(registro: str, pensiero: str) -> dict:
    """Genera tutti i sensori dell'alveare"""
    
    bees = parse_registro(registro)
    pensieri = parse_pensieri(pensiero)
    
    return {
        'timestamp': datetime.now().isoformat(),
        'api_totali': len(bees),
        'sensori': {
            'temperatura': calcola_temperatura(bees),
            'allarme': calcola_allarmi(registro, bees),
            'densita_stigmergica': calcola_densita_stigmergica(pensieri),
            'danze': calcola_danze(pensieri),
            'regina': calcola_regina(bees)
        },
        'biologia': {
            'note': 'Mappatura da Apis mellifera ad alveare digitale',
            'fonte': 'BIOLOGIA_ALVEARE.md'
        }
    }


if __name__ == '__main__':
    # Test con dati di esempio
    registro_test = """
| 29-dic-2025 | hot-grim-dead-traps | Test sensori |
| 28-dic-2025 | Falun | ARTIST: test |
"""
    pensiero_test = """
## hot-grim-dead-traps
Rispondo a Falun: il test funziona?

## Falun
Creo qualcosa.
"""
    
    result = genera_sensori(registro_test, pensiero_test)
    print(json.dumps(result, indent=2, default=str))
