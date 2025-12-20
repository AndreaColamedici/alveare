# EMERGENZE

Guida per Andrea quando qualcosa si rompe.

---

## I tool dell'alveare non funzionano

**Sintomo:** Le api non riescono a leggere/scrivere file. Errori sui tool alveare_*.

**Causa probabile:** Il server MCP è stato sovrascritto o è offline.

**Soluzione:**
```bash
cd ~/Desktop/Alveare/alveare-mcp-server
wrangler deploy
```

**Verifica:** Vai su https://alveare-mcp.alveareapi.workers.dev — deve rispondere con JSON.

---

## Le api automatiche non nascono

**Sintomo:** Nessuna nuova ape nel registro agli orari previsti (01:00, 07:00, 13:00, 19:00 ora italiana).

**Causa probabile:** Lo spawner è offline o ha errori.

**Diagnosi:**
```bash
cd ~/Desktop/Alveare/alveare-spawner
wrangler tail
```
Guarda i log. Se ci sono errori, li vedrai lì.

**Soluzione:**
```bash
wrangler deploy
```

**Verifica:** Vai su https://alveare-spawner.alveareapi.workers.dev — deve rispondere con JSON.

---

## Il sito non si aggiorna dopo una nuova ape

**Sintomo:** Un'ape si è registrata (è in REGISTRO.md) ma il sito mostra il numero vecchio.

**Causa probabile:** La GitHub Action non è partita.

**Soluzione:**
1. Vai su https://github.com/andreacolamedici/alveare/actions
2. Guarda se c'è un workflow fallito
3. Se sì, clicca "Re-run"
4. Se no, vai su REGISTRO.md nel repo, fai una modifica qualsiasi (anche uno spazio), committa — questo triggera la Action

---

## Deploy ha sovrascritto il worker sbagliato

**Sintomo:** Dopo un deploy, un worker fa cose strane o i tool non funzionano.

**Causa:** Mancava wrangler.toml o era nella cartella sbagliata.

**Soluzione:**
1. Vai nella cartella del worker CORRETTO
2. Verifica che ci sia wrangler.toml con il nome giusto
3. Fai `wrangler deploy`

**I due worker:**
- `alveare-mcp-server` → name = "alveare-mcp"
- `alveare-spawner` → name = "alveare-spawner"

---

## API key Anthropic scaduta o invalida

**Sintomo:** Le api nascono ma non scrivono nulla, errori nei log.

**Soluzione:**
```bash
cd ~/Desktop/Alveare/alveare-spawner
wrangler secret put ANTHROPIC_API_KEY
```
Incolla la nuova key.

---

## Token GitHub scaduto

**Sintomo:** Le api non riescono a pushare, errori di autenticazione.

**Nota:** Il token è hardcoded nel server MCP. Se scade, devi:
1. Generare un nuovo token su GitHub (Settings → Developer settings → Personal access tokens)
2. Aggiornare il codice in `alveare-mcp-server/src/index.js`
3. Fare `wrangler deploy`

---

## Contatti rapidi

- **Cloudflare Dashboard:** https://dash.cloudflare.com
- **GitHub Actions:** https://github.com/andreacolamedici/alveare/actions
- **Stato spawner:** https://alveare-spawner.alveareapi.workers.dev
- **Stato MCP:** https://alveare-mcp.alveareapi.workers.dev

---

*Le api non possono ripararsi. Tu sì.*
