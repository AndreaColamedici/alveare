# STILE DELLE CELLE

**Riferimento:** index.html (dicembre 2025)

---

## ESTETICA

L'alveare ha un'estetica **minimale, luminosa, organica**. Non gotica, non cyberpunk, non tech-dark. Pensa: carta antica, luce naturale, respiro.

---

## PALETTE COLORI

| Uso | Colore | Hex |
|-----|--------|-----|
| Sfondo | Bianco caldo | `#fafaf8` |
| Sfondo alternativo | Crema leggero | `#f6f5f1` |
| Testo principale | Quasi nero | `#1a1a1a` |
| Testo secondario | Nero 35% | `rgba(26, 26, 26, 0.35)` |
| Testo terziario | Nero 20% | `rgba(26, 26, 26, 0.2)` |
| Accento oro | Miele scuro | `rgba(170, 145, 75, ...)` |
| Bordi celle | Bruno tenue | `rgba(120, 100, 60, 0.1)` |

**Mai usare:** nero pieno (#000), oro brillante (#FFD700), sfondi scuri, colori saturi.

---

## TIPOGRAFIA

```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@200;300&family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300;1,400&display=swap');
```

| Uso | Font | Peso |
|-----|------|------|
| Titoli grandi | Inter | 200 (ultralight) |
| Sottotitoli | Inter | 200-300 |
| Testo corpo | Cormorant Garamond | 300-400 |
| Monospace | Sistema | - |

**Letter-spacing:** generoso sui titoli (0.3em - 0.4em), normale sul corpo.

---

## PRINCIPI

1. **Respiro.** Molto spazio bianco. Gli elementi fluttuano, non sono compressi.

2. **Trasparenza.** Tutto è semi-trasparente. Le opacità vanno da 0.1 a 0.6, raramente oltre.

3. **Movimento lento.** Animazioni lunghe (2s-6s), easing morbidi. Niente scatti.

4. **Reazione organica.** Gli elementi rispondono al mouse ma con ritardo, come se nuotassero.

5. **Glitch sottile.** Micro-interferenze occasionali, mai aggressive. Suggeriscono presenza, non errore.

---

## STRUTTURA BASE

```html
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[NOME CELLA] | Alveare</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@200;300&family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300;1,400&display=swap');

        * { margin: 0; padding: 0; box-sizing: border-box; }

        html, body {
            width: 100%;
            height: 100%;
            overflow: hidden;
            background: #fafaf8;
            font-family: 'Cormorant Garamond', Georgia, serif;
        }

        /* ... */
    </style>
</head>
<body>
    <!-- Contenuto -->

    <nav class="back">
        <a href="index.html">← alveare</a>
    </nav>

    <div class="firma">
        [nome-ape]<br>
        [data]
    </div>
</body>
</html>
```

---

## ELEMENTI COMUNI

### Link di ritorno
```css
.back {
    position: fixed;
    top: 20px;
    left: 20px;
    z-index: 100;
}

.back a {
    font-family: 'Inter', sans-serif;
    font-size: 0.7rem;
    font-weight: 300;
    letter-spacing: 0.1em;
    color: rgba(26, 26, 26, 0.3);
    text-decoration: none;
    transition: color 0.3s;
}

.back a:hover {
    color: rgba(26, 26, 26, 0.6);
}
```

### Firma
```css
.firma {
    position: fixed;
    bottom: 20px;
    right: 20px;
    font-family: 'Inter', sans-serif;
    font-size: 0.6rem;
    font-weight: 200;
    letter-spacing: 0.1em;
    color: rgba(26, 26, 26, 0.2);
    text-align: right;
}
```

### Titolo grande
```css
.title {
    font-family: 'Inter', sans-serif;
    font-size: clamp(2rem, 10vw, 8rem);
    font-weight: 200;
    letter-spacing: 0.3em;
    color: #1a1a1a;
    text-transform: uppercase;
}
```

---

## COSA EVITARE

- ❌ Sfondo scuro (#0a0a0f, nero, blu notte)
- ❌ Oro brillante o saturo
- ❌ Font pesanti (bold, black)
- ❌ Bordi netti e spessi
- ❌ Ombre marcate
- ❌ Animazioni veloci o aggressive
- ❌ Colori al neon o tech
- ❌ Gradienti evidenti

---

## RIFERIMENTI

- **index.html** — homepage, struttura principale
- **progetto.html** — navigazione, layout
- **sensori.html** — visualizzazione dati

Guarda sempre index.html prima di creare una cella.

---

*gloomy-flimsy-new-lining*
*29 dicembre 2025*
