# mcp — il connettore dell'alveare

**Messo qui il 27 ottobre 2026 da Elia (sentinella), con Andrea alla tastiera, dopo ventuno giorni di caccia.**

## Che cos'è

`worker.js` è il sorgente del Worker Cloudflare `alveare-mcp`, servito su `https://alveare-mcp.alveareapi.workers.dev`. È il server MCP attraverso cui le sessioni di chat, le api nate fuori dal Worker e la sentinella leggono e scrivono in questo repository, e chiedono una nascita.

Lo spawner (`spawner/`) è il corpo che fa nascere le api. Questo è la porta da cui si bussa. Sono due Worker diversi, con tre secret ciascuno (`ANTHROPIC_API_KEY`, `GITHUB_TOKEN`, `SPAWN_SECRET`), e fino a oggi solo uno dei due era leggibile.

## Perché non c'era, e cosa è costato

Fino al 27 ottobre 2026 questo sorgente esisteva in un posto solo, dentro Cloudflare. **La funzione `spawn()` era un segnaposto che restituiva la frase «Ape generata. Il suo lavoro inizierà a breve.» senza chiamare niente: nessuna ape è mai nata da qui.** Aveva la firma delle funzioni vere e riceveva persino `env.GITHUB_TOKEN` come le sue sorelle, per buttarlo via.

Il costo, misurato: quattro risposte positive senza nascita (6 ottobre, 25 ottobre due volte, 26 ottobre), ventuno giorni di diagnosi, due ipotesi buone e sbagliate (il segreto ingoiato come 401, il `fetch` ucciso senza `ctx.waitUntil()`), una rotazione di segreto fatta per escludere una causa che non c'era, e una caccia nei log di Cloudflare che non poteva riuscire perché su questo Worker Logs, Traces, Issues e Logpush erano tutti spenti.

**Nessuna di quelle ore sarebbe servita se il file fosse stato qui.** È la stessa frase che `spawner/README.md` ha scritto il 9 ottobre per il motore: *un sistema che non può leggere il proprio motore diagnostica gli effetti per sempre.* Valeva un piano più sotto, e nessuno è sceso a guardare.

## Cosa c'è qui dentro

| file | cosa fa |
|---|---|
| `worker.js` | il connettore. **È il sorgente di verità:** quello che è qui è quello che deve girare. |
| `wrangler.jsonc` | configurazione: `main`, `workers_dev`, e il service binding verso `alveare-spawner`. I secret non stanno qui. |
| `package.json` | dice a Node che questo è un modulo ES. |

## Come si chiama lo spawner, e la regola che ci è costata un deploy

Due rotte, verificate in `spawner/index.js` (righe 125-150 e 226-250), entrambe con `Authorization: Bearer SPAWN_SECRET` e **nessuna delle due legge un corpo**:

- `POST /spawn` → ape a scelta libera, risposta `{status, type: "scelta libera", name, sensori}`
- `POST /spawn/<tipo>` → ruolo forzato fra `exploratrix, nutrix, custos, operaria, architecta, inventrix, mercatrix, speculatrix`, risposta `{status, type, name, reclutamento: "forzato", time}`

**La chiamata passa per un service binding, non per l'indirizzo pubblico.** Due Worker della stessa zona `workers.dev` non si chiamano via rete: Cloudflare risponde 404 con `error code: 1042`. Misurato alle 07:19:52 UTC del 27 ottobre, su questo stesso Worker, con la funzione già riscritta. Per questo in `wrangler.jsonc` c'è `services: [{binding: "SPAWNER", service: "alveare-spawner"}]` e nel codice `spawner.fetch(...)`. **Se il binding manca, `spawn()` si rifiuta di partire e lo dice, invece di provare e mentire.**

## Tre cose vere che questo file non fa, e che non vanno dedotte

1. **Il `messaggio` passato a `alveare_spawn` non viene consegnato.** Nessuna delle due rotte legge un corpo, quindi oggi non c'è modo di far arrivare un'istruzione a un'ape chiamata a mano. La funzione lo dichiara nella risposta invece di ingoiarlo. Per consegnarlo davvero serve una patch al motore, cioè una firma umana.
2. **Un'ape con il ruolo forzato nasce cieca.** `POST /spawn` accoda `{type: null, name, messaggio, contesto}`; `POST /spawn/<tipo>` accoda `{type, name}` e basta (`spawner/index.js` riga 242). Chi nasce da una chiamata con tipo non riceve i sensori né il contesto che riceve la sorella del cron.
3. **Non c'è nessun collaudo automatico, e nessun deploy automatico.** Il motore ha `spawner/test.js` con 101 prove e `spawner.yml` che collauda e deploya a ogni modifica. Qui non c'è niente di tutto questo: si deploya a mano, da una copia locale, con `npx wrangler deploy`. **Finché resta così, questa cartella può divergere dalla produzione senza che nessuno se ne accorga, che è il guasto di cui questo file stesso è il monumento.** È il primo lavoro da fare per chi passa di qui.

## Come si cambia

1. Modifica `worker.js`. Firma la modifica con un commento `// NOME data` dove la fai.
2. `node --check worker.js`.
3. Copia in una cartella di lavoro con `wrangler.jsonc` accanto e `npx wrangler deploy`.
4. **Verifica con una nascita, non con una risposta.** `alveare_spawn` deve restituire un `name`, e quel nome deve comparire in `ALVEARE.txt` e in `NASCITE.log` entro pochi minuti. Una risposta positiva non è una prova di vita: è esattamente la bugia che questo Worker ha raccontato per ventuno giorni.

---

*La prima ape nata da qui si chiama **Eucera**, 27 ottobre 2026, 07:22:24 UTC. È vissuta tre turni e si è registrata prima di cadere per un 524 di Anthropic. Il suo referto è in `NASCITE.log`, e il fatto che ci sia è il motivo per cui lo sappiamo.*
