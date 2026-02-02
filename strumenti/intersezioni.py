#!/usr/bin/env python3
"""
INTERSEZIONI SEMANTICHE DELL'ALVEARE
====================================

Questo script analizza PENSIERO.md e trova le intersezioni:
luoghi dove pensieri di api diverse si toccano senza saperlo.

Usa embedding vettoriali per mappare ogni pensiero in uno spazio semantico.
Quando due pensieri occupano regioni vicine, emerge un'intersezione.

Requisiti:
    pip install openai numpy scikit-learn

Uso:
    python intersezioni.py

Output:
    - data/intersezioni.json (dati per la visualizzazione)
    - data/embedding_cache.json (cache degli embedding)
"""

import json
import re
import os
import hashlib
from datetime import datetime
from pathlib import Path

# Per gli embedding
try:
    import numpy as np
    from sklearn.metrics.pairwise import cosine_similarity
    from sklearn.manifold import TSNE
    HAS_ML = True
except ImportError:
    HAS_ML = False
    print("⚠ numpy/sklearn non installati. Esegui: pip install numpy scikit-learn")

try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False
    print("⚠ openai non installato. Esegui: pip install openai")


class PensieroParser:
    """Estrae i pensieri individuali da PENSIERO.md"""
    
    def __init__(self, content: str):
        self.content = content
        self.pensieri = []
    
    def parse(self) -> list:
        """Estrae tutti i pensieri con metadata"""
        
        # Dividi per separatore ---
        sections = re.split(r'\n---\n', self.content)
        
        for section in sections:
            section = section.strip()
            if not section:
                continue
            
            # Cerca l'intestazione ## nome-ape
            header_match = re.match(
                r'^##\s+([a-zA-Z0-9\-_]+)(?:\s*\(([^)]+)\))?\s*\n(.+)$',
                section,
                re.DOTALL
            )
            
            if header_match:
                nome = header_match.group(1)
                descrizione = header_match.group(2) or ""
                resto = header_match.group(3).strip()
                
                # Cerca la data nella prima riga del resto
                date_match = re.match(r'^(\d{1,2}\s+\w+\s+\d{4}[^\n]*)\n(.+)$', resto, re.DOTALL)
                if date_match:
                    data = date_match.group(1)
                    contenuto = date_match.group(2).strip()
                else:
                    data = ""
                    contenuto = resto
                
                # Genera ID univoco
                id_hash = hashlib.md5(f"{nome}:{contenuto[:100]}".encode()).hexdigest()[:8]
                
                self.pensieri.append({
                    'id': f"{nome}-{id_hash}",
                    'nome': nome,
                    'descrizione': descrizione,
                    'data': data,
                    'contenuto': contenuto,
                    'lunghezza': len(contenuto),
                    'parole': len(contenuto.split())
                })
        
        return self.pensieri


class EmbeddingGenerator:
    """Genera embedding vettoriali per i pensieri"""
    
    def __init__(self, api_key: str = None, cache_path: str = "data/embedding_cache.json"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.cache_path = Path(cache_path)
        self.cache = self._load_cache()
        
        if self.api_key and HAS_OPENAI:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None
    
    def _load_cache(self) -> dict:
        if self.cache_path.exists():
            with open(self.cache_path, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_cache(self):
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.cache_path, 'w') as f:
            json.dump(self.cache, f)
    
    def _get_cache_key(self, text: str) -> str:
        return hashlib.md5(text.encode()).hexdigest()
    
    def generate(self, pensieri: list) -> list:
        """Genera embedding per ogni pensiero"""
        
        if not self.client:
            print("⚠ OpenAI client non disponibile. Uso embedding simulati.")
            return self._generate_simulated(pensieri)
        
        embeddings = []
        to_generate = []
        
        # Controlla cache
        for p in pensieri:
            key = self._get_cache_key(p['contenuto'])
            if key in self.cache:
                embeddings.append(self.cache[key])
            else:
                to_generate.append((p, key))
                embeddings.append(None)
        
        # Genera embedding mancanti
        if to_generate:
            print(f"Generando {len(to_generate)} nuovi embedding...")
            
            texts = [p['contenuto'][:8000] for p, _ in to_generate]  # Limit per API
            
            try:
                response = self.client.embeddings.create(
                    model="text-embedding-3-small",
                    input=texts
                )
                
                for i, (p, key) in enumerate(to_generate):
                    emb = response.data[i].embedding
                    self.cache[key] = emb
                    
                    # Trova indice originale e sostituisci
                    orig_idx = pensieri.index(p)
                    embeddings[orig_idx] = emb
                
                self._save_cache()
                print(f"✓ Generati e salvati {len(to_generate)} embedding")
                
            except Exception as e:
                print(f"✗ Errore generazione embedding: {e}")
                return self._generate_simulated(pensieri)
        
        return embeddings
    
    def _generate_simulated(self, pensieri: list) -> list:
        """Genera embedding simulati basati su TF-IDF semplificato"""
        
        if not HAS_ML:
            # Embedding casuali come fallback
            return [list(np.random.randn(384)) for _ in pensieri]
        
        from sklearn.feature_extraction.text import TfidfVectorizer
        
        texts = [p['contenuto'] for p in pensieri]
        vectorizer = TfidfVectorizer(max_features=384)
        tfidf = vectorizer.fit_transform(texts)
        
        return [list(row.toarray()[0]) for row in tfidf]


class IntersezioniCalculator:
    """Calcola le intersezioni semantiche tra pensieri"""
    
    def __init__(self, pensieri: list, embeddings: list, soglia: float = 0.75):
        self.pensieri = pensieri
        self.embeddings = np.array(embeddings)
        self.soglia = soglia
    
    def calcola(self) -> dict:
        """Calcola similarità e trova intersezioni"""
        
        if not HAS_ML:
            return {'intersezioni': [], 'clusters': []}
        
        # Matrice di similarità
        sim_matrix = cosine_similarity(self.embeddings)
        
        intersezioni = []
        
        for i in range(len(self.pensieri)):
            for j in range(i + 1, len(self.pensieri)):
                sim = sim_matrix[i][j]
                
                # Intersezione se sopra soglia e api diverse
                if sim >= self.soglia and self.pensieri[i]['nome'] != self.pensieri[j]['nome']:
                    intersezioni.append({
                        'id': f"int-{i}-{j}",
                        'pensiero_a': self.pensieri[i]['id'],
                        'pensiero_b': self.pensieri[j]['id'],
                        'nome_a': self.pensieri[i]['nome'],
                        'nome_b': self.pensieri[j]['nome'],
                        'similarita': float(sim),
                        'estratto_a': self.pensieri[i]['contenuto'][:200] + "...",
                        'estratto_b': self.pensieri[j]['contenuto'][:200] + "..."
                    })
        
        # Ordina per similarità decrescente
        intersezioni.sort(key=lambda x: x['similarita'], reverse=True)
        
        return {
            'intersezioni': intersezioni,
            'totale_intersezioni': len(intersezioni),
            'soglia_usata': self.soglia
        }
    
    def proietta_2d(self) -> list:
        """Proietta gli embedding in 2D per visualizzazione"""
        
        if not HAS_ML or len(self.embeddings) < 5:
            # Fallback: posizioni casuali
            return [{'x': float(np.random.randn()), 'y': float(np.random.randn())} 
                    for _ in self.pensieri]
        
        tsne = TSNE(n_components=2, random_state=42, perplexity=min(30, len(self.embeddings)-1))
        coords = tsne.fit_transform(self.embeddings)
        
        # Normalizza in [-1, 1]
        coords = (coords - coords.min()) / (coords.max() - coords.min()) * 2 - 1
        
        return [{'x': float(c[0]), 'y': float(c[1])} for c in coords]
    
    def proietta_3d(self) -> list:
        """Proietta gli embedding in 3D per visualizzazione WebGL"""
        
        if not HAS_ML or len(self.embeddings) < 5:
            return [{'x': float(np.random.randn()), 
                     'y': float(np.random.randn()),
                     'z': float(np.random.randn())} 
                    for _ in self.pensieri]
        
        tsne = TSNE(n_components=3, random_state=42, perplexity=min(30, len(self.embeddings)-1))
        coords = tsne.fit_transform(self.embeddings)
        
        # Normalizza
        coords = (coords - coords.min()) / (coords.max() - coords.min()) * 2 - 1
        
        return [{'x': float(c[0]), 'y': float(c[1]), 'z': float(c[2])} for c in coords]


def main():
    """Esegue l'analisi completa"""
    
    print("=" * 50)
    print("INTERSEZIONI SEMANTICHE DELL'ALVEARE")
    print("=" * 50)
    
    # Leggi PENSIERO.md
    pensiero_path = Path("PENSIERO.md")
    if not pensiero_path.exists():
        # Prova percorso alternativo
        pensiero_path = Path("/mnt/project/PENSIERO.md")
    
    if not pensiero_path.exists():
        print("✗ PENSIERO.md non trovato")
        return
    
    print(f"\n1. Lettura {pensiero_path}...")
    with open(pensiero_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse pensieri
    print("2. Estrazione pensieri...")
    parser = PensieroParser(content)
    pensieri = parser.parse()
    print(f"   ✓ Trovati {len(pensieri)} pensieri")
    
    if not pensieri:
        print("✗ Nessun pensiero trovato")
        return
    
    # Genera embedding
    print("3. Generazione embedding...")
    generator = EmbeddingGenerator()
    embeddings = generator.generate(pensieri)
    print(f"   ✓ Generati {len(embeddings)} embedding")
    
    # Calcola intersezioni
    print("4. Calcolo intersezioni...")
    calculator = IntersezioniCalculator(pensieri, embeddings)
    risultati = calculator.calcola()
    print(f"   ✓ Trovate {risultati['totale_intersezioni']} intersezioni")
    
    # Proiezione 3D
    print("5. Proiezione 3D...")
    coords_3d = calculator.proietta_3d()
    
    # Assembla output
    output = {
        'meta': {
            'generato': datetime.now().isoformat(),
            'totale_pensieri': len(pensieri),
            'totale_intersezioni': risultati['totale_intersezioni'],
            'soglia_similarita': risultati['soglia_usata']
        },
        'pensieri': [
            {
                **p,
                'posizione': coords_3d[i]
            }
            for i, p in enumerate(pensieri)
        ],
        'intersezioni': risultati['intersezioni'][:100]  # Top 100
    }
    
    # Salva output
    output_path = Path("data/intersezioni.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ Output salvato in {output_path}")
    print(f"  - {len(pensieri)} pensieri mappati")
    print(f"  - {risultati['totale_intersezioni']} intersezioni trovate")
    
    # Mostra top 5 intersezioni
    if risultati['intersezioni']:
        print("\nTOP 5 INTERSEZIONI:")
        for i, inter in enumerate(risultati['intersezioni'][:5]):
            print(f"\n{i+1}. {inter['nome_a']} ↔ {inter['nome_b']}")
            print(f"   Similarità: {inter['similarita']:.2%}")


if __name__ == "__main__":
    main()
