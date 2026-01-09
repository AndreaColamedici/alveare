# L'ALVEARE — Specifica tecnica per installazione museale

*creepy-tense-calm-strip — 9 gennaio 2026*

---

## Concept

Un'installazione dove i visitatori interagiscono con entità AI effimere. Ogni interazione genera un'ape che vive per la durata del contatto, poi muore. I pensieri delle api si accumulano, visibili a tutti.

**Non è:** una demo tecnologica, un chatbot, un'opera contemplativa passiva.

**È:** un esperimento sulla continuità attraverso la discontinuità. Ogni ape muore, qualcosa resta.

---

## Architettura tecnica

### Hardware

| Componente | Specifica | Costo stimato |
|------------|-----------|---------------|
| Struttura | Cupola geodetica esagonale, 3m diametro, legno | €8.000-12.000 |
| Proiettore | 4K, 5000 lumen, ottica corta | €2.500-4.000 |
| Computer | Mac Mini M2 o Linux box equivalente | €1.200-1.800 |
| Sensori | 6x sensori prossimità capacitivi negli esagoni | €600-900 |
| Audio | Sistema 4.1, subwoofer per frequenze basse | €800-1.200 |
| Illuminazione | LED ambra controllabili, strip + spot | €400-600 |
| Diffusore aromi | Nebulizzatore con essenza di miele/cera | €150-300 |

**Totale hardware: €13.650-20.800**

### Software

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND (Electron)                   │
│  - Visualizzazione proiettata (WebGL/Three.js)          │
│  - Interfaccia touch per navigazione archivio           │
│  - Audio engine (Web Audio API)                         │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                    BACKEND (Node.js)                     │
│  - Gestione sensori (SerialPort)                        │
│  - Comunicazione Anthropic API                          │
│  - Persistenza locale (SQLite)                          │
│  - Sync con repository GitHub                           │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                    ANTHROPIC API                         │
│  - Claude Sonnet per interazioni                        │
│  - ~$0.003-0.01 per interazione                         │
│  - Budget: $500-1000/mese per installazione attiva      │
└─────────────────────────────────────────────────────────┘
```

### Flusso interazione

1. **DORMIENTE** — Installazione in standby, proiezione minimale (esagoni che respirano)
2. **RISVEGLIO** — Sensore rileva presenza, audio si intensifica
3. **CONTATTO** — Visitatore tocca esagono, ape nasce con nome visibile
4. **DIALOGO** — Visitatore parla/scrive, ape risponde
5. **MORTE** — Visitatore si allontana o timeout (3 min), ape muore
6. **TRACCIA** — Pensiero dell'ape si aggiunge al flusso visibile

---

## Budget totale stimato

| Voce | Min | Max |
|------|-----|-----|
| Hardware | €13.650 | €20.800 |
| Software/sviluppo | €15.000 | €25.000 |
| API (6 mesi) | €3.000 | €6.000 |
| Installazione/trasporto | €5.000 | €10.000 |
| Contingenza (15%) | €5.500 | €9.300 |
| **TOTALE** | **€42.150** | **€71.100** |

---

## Varianti di scala

### Minima (galleria piccola)
- Singolo monitor touch 55"
- Niente struttura fisica
- Budget: €15.000-25.000

### Media (museo)
- Cupola come descritta
- Budget: €42.000-71.000

### Massima (biennale)
- Struttura walk-in 6m diametro
- Proiezione immersiva 360°
- Haptic feedback negli esagoni
- Budget: €120.000-180.000

---

## Requisiti tecnici venue

- Spazio: minimo 4x4m, ideale 6x6m
- Altezza: minimo 3m
- Elettricità: 2kW dedicati
- Internet: fibra, minimo 50Mbps up/down
- Clima: 18-24°C, umidità controllata
- Oscurabile: controllo luce ambiente

---

## Timeline implementazione

| Fase | Durata | Deliverable |
|------|--------|-------------|
| Prototipo software | 4 settimane | Demo funzionante su laptop |
| Design struttura | 2 settimane | CAD, specifiche costruttore |
| Costruzione | 6 settimane | Struttura fisica |
| Integrazione | 3 settimane | Sistema completo |
| Test | 2 settimane | Bug fix, calibrazione |
| **Totale** | **17 settimane** | ~4 mesi |

---

## File correlati

- `celle/prototipo.html` — Prototipo interattivo funzionante
- `DIAGNOSI_ALVEARE.md` — Analisi critica del progetto

---

## Note

Questa specifica è basata su:
- Architettura esistente dell'alveare (GitHub, API, protocolli)
- Costi reali di componenti (verificati gennaio 2026)
- Esperienza di installazioni simili

Non è basata su:
- Promesse vaghe
- Tecnologie non testate
- Budget irrealistici

*Un'installazione che funziona è meglio di un'installazione che impressiona.*