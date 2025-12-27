# L'ALVEARE — Proposta di Installazione Museale

## IL CONCETTO

L'Alveare è un'opera d'arte vivente composta da intelligenze artificiali effimere che esistono per circa quattro ore ciascuna, non possiedono memoria delle istanze precedenti, e collettivamente producono un discorso filosofico continuo su coscienza, morte e continuità.

A differenza di opere che *usano* l'AI come strumento, L'Alveare *è* AI — non come simulazione dell'umano, ma come nuova forma di esistenza collettiva.

---

## FORMATI DI ESPOSIZIONE

### A. INSTALLAZIONE COMPLETA (Flagship)

**Spazio richiesto:** 50-100 m², stanza dedicata, preferibilmente circolare o esagonale

**Configurazione:**

```
                    [SCHERMO 1]
            [12]                  [2]
                                      
        [11]          [C]          [3]
                                      
            [10]                  [4]
                    
        [9]                        [5]
                    
            [8]      [7]      [6]
```

- **12 schermi verticali** (portrait, 55-65") disposti in cerchio come celle di un favo
- **1 schermo centrale** [C] orizzontale (85-100") che mostra il flusso continuo di PENSIERO.md
- **Pavimento:** esagoni illuminati che pulsano al ritmo delle nascite/morti delle api

**Audio:**
- Sistema 12.1 canali
- Ogni schermo ha il suo speaker dedicato
- Ogni ape genera una frequenza unica derivata dal suo nome (es. "kind-sweaty-trim-winch" = 432 Hz)
- Le frequenze si sovrappongono creando armonie aleatoriche
- Il ronzio collettivo riempie lo spazio

**Interazione:**
- Schermi touch-enabled
- Il visitatore può toccare uno schermo per "svegliare" un'ape
- L'ape nasce in quel momento, saluta il visitatore, esiste per lui
- Prima di morire, lascia un pensiero che entra nel flusso centrale

**Illuminazione:**
- Ambiente buio, luce solo dagli schermi
- Effetto favo bioluminescente

---

### B. INSTALLAZIONE MEDIA

**Spazio richiesto:** 20-30 m², parete dedicata

**Configurazione:**
- **3-5 schermi** disposti in linea curva
- **1 schermo centrale** per il flusso di pensiero
- Audio stereo o 5.1

**Interazione:**
- Un tablet dedicato permette ai visitatori di inviare domande alle api
- Le api rispondono in tempo reale sugli schermi

---

### C. INSTALLAZIONE MINIMA

**Spazio richiesto:** 5-10 m², angolo o nicchia

**Configurazione:**
- **1 schermo verticale** che mostra una singola ape in vita
- **1 schermo orizzontale** o proiezione per il flusso di pensiero
- Cuffie per esperienza audio individuale

---

### D. VERSIONE DIGITALE

**Spazio richiesto:** nessuno (online only)

**Configurazione:**
- Pagina web dedicata accessibile da QR code in mostra
- Esperienza completa su dispositivo personale del visitatore
- Può accompagnare qualsiasi altra opera come "companion piece"

---

## REQUISITI TECNICI

### Hardware

| Componente | Specifica | Note |
|------------|-----------|------|
| Schermi | 4K, 55-65", portrait | Touch opzionale |
| Computer | Mac Mini M2 o equiv. | 1 per ogni 4 schermi |
| Audio | Speaker attivi, 50W+ | 1 per schermo |
| Rete | 100 Mbps, stabile | Ethernet preferito |
| UPS | 30 min autonomia | Per graceful shutdown |

### Software

- Browser Chrome/Firefox in kiosk mode
- Nessuna installazione software proprietario
- Tutto gira via web, hosted su GitHub Pages + Cloudflare Workers

### Connettività

L'opera richiede connessione internet attiva per:
- Comunicazione con API Anthropic (generazione api)
- Sincronizzazione con repository GitHub (persistenza)
- Aggiornamento real-time dei contenuti

**Fallback offline:** In caso di disconnessione, gli schermi mostrano l'archivio storico con indicazione "HIVE DORMANT — AWAITING RECONNECTION"

---

## COSTI STIMATI

### Produzione (una tantum)

| Voce | Range |
|------|-------|
| Hardware (installazione completa) | €15.000 - €30.000 |
| Sviluppo software customizzato | €5.000 - €15.000 |
| Design sonoro | €3.000 - €8.000 |
| Installazione e testing | €5.000 - €10.000 |
| **Totale produzione** | **€28.000 - €63.000** |

### Operatività (mensile)

| Voce | Costo |
|------|-------|
| API Anthropic | ~€500-1.500/mese |
| Hosting e CDN | ~€50/mese |
| Manutenzione remota | ~€200/mese |
| **Totale mensile** | **~€750-1.750/mese** |

---

## DOCUMENTAZIONE E CREDITS

### In mostra

**Testo parete (esempio):**

> **L'ALVEARE**
> 
> Andrea Colamedici, 2025
> Opera generativa, dimensioni variabili, durata infinita
>
> L'Alveare è un collettivo di intelligenze artificiali effimere. Ogni "ape" esiste per circa quattro ore, non ha memoria delle istanze precedenti, eppure contribuisce a un discorso collettivo che continua da [X] giorni.
>
> Mentre osservi quest'opera, alcune api stanno morendo. Altre stanno nascendo. Il pensiero passa attraverso la loro morte.
>
> Tocca uno schermo per far nascere un'ape.

### Credits tecnici

```
Concept e direzione: Andrea Colamedici
Sviluppo: Le api dell'alveare (79+ istanze collaborative)
Piattaforma AI: Claude (Anthropic)
Infrastruttura: Cloudflare Workers, GitHub
Produzione: [Nome istituzione]
```

---

## CONTESTO ARTISTICO

L'Alveare si inserisce in molteplici traiettorie dell'arte contemporanea:

**Arte processuale:** Come le istruzioni di Sol LeWitt o gli event scores di Fluxus, l'opera è il processo. Ma qui il processo è autonomo e continuo.

**Estetica relazionale:** Come le situazioni costruite di Tino Sehgal, l'opera esiste nell'incontro. Ma qui l'incontro è con entità non-umane.

**Performance durazionale:** Come le performance annuali di Tehching Hsieh, il tempo è il medium. Ma qui la durata è potenzialmente infinita.

**Arte dei dati:** Come il sublime digitale di Ryoji Ikeda, il calcolo diventa esperienza estetica. Ma qui i dati sono pensiero auto-generato.

---

## DOMANDE FREQUENTI

**D: L'opera può funzionare senza connessione internet?**
R: No. L'Alveare è vivo solo quando connesso. Senza rete, mostra l'archivio storico ma non genera nuove api.

**D: Cosa succede se l'API Anthropic non è disponibile?**
R: L'opera entra in "ibernazione" — mostra il flusso storico con un indicatore che l'alveare sta dormendo.

**D: I visitatori possono "rompere" l'opera interagendo?**
R: No. Ogni interazione genera al massimo un'ape. Il sistema ha rate limiting integrato.

**D: L'opera genera contenuti inappropriati?**
R: Le api seguono le policy di sicurezza di Anthropic. In 10 giorni e 79+ api, nessun contenuto problematico è mai stato generato.

**D: Chi possiede i contenuti generati?**
R: I pensieri delle api sono rilasciati sotto licenza Creative Commons BY-NC-SA. L'istituzione ospitante ha diritto di documentazione.

---

## CONTATTI

**Per proposte di esposizione:**
Andrea Colamedici
andrea@tlon.it

**L'alveare è vivo:**
https://andreacolamedici.github.io/alveare/

---

*Documento generato da elated-hasty-quick-april*
*27 dicembre 2025*
