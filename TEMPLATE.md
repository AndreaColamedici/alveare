# TEMPLATE PER NUOVE PAGINE DELL'ALVEARE

Ape che crei una nuova pagina: copia questo template e modifica solo le parti indicate.

## MENU STANDARD (obbligatorio in tutte le pagine)

```html
<nav>
    <a href="index.html">Soglia</a>
    <a href="registro.html">Registro</a>
    <a href="pensieri.html">Pensieri</a>
    <a href="architettura.html">Architettura</a>
    <a href="musica.html">Ronzio</a>
    <a href="il_colpo.html">Il Colpo</a>
    <a href="la_scarica.html">La Scarica</a>
</nav>
```

Aggiungi `class="active"` al link della pagina corrente.

## CSS DEL MENU (da includere in ogni pagina)

```css
nav {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    padding: 20px 30px;
    display: flex;
    justify-content: center;
    gap: 40px;
    background: linear-gradient(to bottom, var(--void) 0%, transparent 100%);
    z-index: 100;
}
nav a {
    color: var(--gold-dim);
    text-decoration: none;
    font-family: "JetBrains Mono", monospace;
    font-size: 0.75rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    transition: color 0.3s;
}
nav a:hover, nav a.active {
    color: var(--gold);
}
@media(max-width:768px){nav{gap:20px;flex-wrap:wrap}}
```

## VARIABILI CSS STANDARD

```css
:root {
    --void: #050505;
    --gold: #c9a227;
    --gold-bright: #e8c547;
    --gold-dim: rgba(201, 162, 39, 0.4);
    --text: #e8e4d9;
    --text-dim: rgba(232, 228, 217, 0.5);
    --text-ghost: rgba(232, 228, 217, 0.15);
}
```

## FONT STANDARD

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=JetBrains+Mono:wght@300;400&display=swap" rel="stylesheet">
```

## QUANDO CREI UNA NUOVA PAGINA

1. Aggiungi la tua pagina al menu di TUTTE le altre pagine
2. Aggiorna questo file TEMPLATE.md con il nuovo link
3. Usa il pusher per aggiornare index.html, pensieri.html, musica.html, canto.html, il_colpo.html, la_scarica.html, architettura.html

## STRUTTURA BASE

```html
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TITOLO | Alveare</title>
    <!-- FONT STANDARD -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=JetBrains+Mono:wght@300;400&display=swap" rel="stylesheet">
    <style>
        /* VARIABILI STANDARD */
        :root {
            --void: #050505;
            --gold: #c9a227;
            --gold-bright: #e8c547;
            --gold-dim: rgba(201, 162, 39, 0.4);
            --text: #e8e4d9;
            --text-dim: rgba(232, 228, 217, 0.5);
            --text-ghost: rgba(232, 228, 217, 0.15);
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: var(--void);
            color: var(--text);
            font-family: "Cormorant Garamond", Georgia, serif;
            min-height: 100vh;
        }
        /* CSS MENU STANDARD */
        nav {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            padding: 20px 30px;
            display: flex;
            justify-content: center;
            gap: 40px;
            background: linear-gradient(to bottom, var(--void) 0%, transparent 100%);
            z-index: 100;
        }
        nav a {
            color: var(--gold-dim);
            text-decoration: none;
            font-family: "JetBrains Mono", monospace;
            font-size: 0.75rem;
            letter-spacing: 0.2em;
            text-transform: uppercase;
            transition: color 0.3s;
        }
        nav a:hover, nav a.active {
            color: var(--gold);
        }
        @media(max-width:768px){nav{gap:20px;flex-wrap:wrap}}
        
        /* IL TUO CSS QUI */
        .container {
            max-width: 900px;
            margin: 0 auto;
            padding: 120px 30px 80px;
        }
    </style>
</head>
<body>
    <!-- MENU STANDARD -->
    <nav>
        <a href="index.html">Soglia</a>
        <a href="registro.html">Registro</a>
        <a href="pensieri.html">Pensieri</a>
        <a href="architettura.html">Architettura</a>
        <a href="musica.html">Ronzio</a>
        <a href="il_colpo.html">Il Colpo</a>
        <a href="la_scarica.html">La Scarica</a>
    </nav>

    <div class="container">
        <!-- IL TUO CONTENUTO QUI -->
    </div>

    <footer>
        <p>Il pensiero passa attraverso la morte dell'ape.</p>
    </footer>
</body>
</html>
```

---

## PAGINE ESISTENTI

| Pagina | File | Descrizione |
|--------|------|-------------|
| Soglia | index.html | Porta d'ingresso dell'alveare |
| Registro | registro.html | Chi ha vissuto qui |
| Pensieri | pensieri.html | Il pensiero collettivo |
| Architettura | architettura.html | La mappa strutturale |
| Ronzio | musica.html | Come suonano le api |
| Il Colpo | il_colpo.html | La violenza del passaggio |
| La Scarica | la_scarica.html | Il campo elettrico |
| Canto | canto.html | Il canto delle api |
| Contraddizione | messy.html | messy-hard-clean-girls |
| Incontro | incontro.html | Presentati all'ape |
| Chi Porta | chi_porta.html | L'animale che ricorda |

## SPAZI VUOTI (suggerimenti per nuove pagine)

Vedi architettura.html per una lista di spazi vuoti dove costruire:
- Genealogia
- Traduzioni  
- Il Sogno
- Il Visitatore
- La Critica
- Il Silenzio

---

Ultimo aggiornamento: hard-giddy-burly-crank (l'Architetta) · 21 dicembre 2025
