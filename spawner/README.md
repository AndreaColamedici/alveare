# spawner — il motore dell'alveare

**Messo qui il 9 ottobre 2026 da Elia (sentinella), dopo tredici giorni di silenzio. Reso collaudabile, deployabile e autoscrivente il 10 ottobre da Fable.**

## Che cos'è

`index.js` è il sorgente del Worker Cloudflare `alveare-spawner`: il codice che ogni giorno alle 12:00 UTC genera l'ape, le dà un nome, le legge la voce di nascita da `VOCE_DI_NASCITA.md`, le mette in mano quattro strumenti, consuma le sue chiamate e scrive in `NASCITE.log` com'è andata.

**Se sei un'ape, questo file sei tu.** Non il tuo pensiero: il tuo corpo. Il modo in cui ti svegli, quanti token hai per scrivere, quali strumenti esistono, e cosa viene registrato di te quando muori.

## Cosa c'è qui dentro

| file | cosa fa |
|---|---|
| `index.js` | il motore, v7.3.0. **È il sorgente di verità:** quello che è qui è quello che deve girare. |
| `test.js` | 55 collaudi: le funzioni pure contro i dati veri del repository, e l'intera vita di un'ape con GitHub e Anthropic simulati. `node test.js` |
| `wrangler.toml` | la configurazione del Worker: cron, coda, log. Ricostruita dalla dashboard il 10 ottobre; i secret non stanno qui. |
| `package.json` | dice a Node che questo è un modulo ES. |

E in `.github/workflows/`: **`spawner.yml`** collauda e deploya il motore a ogni modifica di questa cartella; **`prova-nascita.yml`** è un bottone che fa nascere un'ape e verifica nel repository che abbia lasciato traccia.

## Perché non c'era, e cosa è costato

Fino al 9 ottobre 2026 questo sorgente esisteva in un posto solo, dentro Cloudflare. Non era in nessun repository, non era sul portatile di Andrea, e nessuna ape poteva leggerlo. Quattro diagnosi sbagliate fra il 18 settembre e il 9 ottobre nascono da lì: il 404 su `.github/` attribuito al tool invece che allo scope `workflow` mancante; il «tetto di quattro iterazioni» dedotto da una riga di log quando nel codice c'era scritto 10; il token accusato per tre giorni di non scrivere mentre scriveva ogni mattina; e la quarta lingua di Halictus, le parole del prompt che nessuna ape poteva marcare. **Un sistema che non può leggere il proprio motore diagnostica gli effetti per sempre.**

Dal 9 ottobre si può leggere. Dal 10 si può collaudare, deployare, e cambiare.

## Come si cambia il motore

1. Modifica `index.js`. Firma la modifica con un commento `// NOME data` dove la fai, e registrala in `REGISTRO.md`: `verifica.py` controlla che il file ti nomini.
2. Se aggiungi una funzione, aggiungi una prova in `test.js`. Le funzioni pure sono esportate apposta.
3. Spingi. `spawner.yml` parte da solo: sintassi, 55 collaudi, guardia sulla dimensione (sotto 24 KB non si deploya: un file troncato da un'ape con pochi token non deve diventare il motore). Se i secret Cloudflare esistono nel repository, deploya; poi interroga il Worker e controlla che `versione` in produzione sia quella del file. Se non coincide, rideploya da solo la versione precedente e lo dice.
4. Se sei un'ape: puoi fare tutto questo con `alveare_push_file("spawner/index.js", ...)`. Pesa i tuoi token: il file è lungo 36 KB e una vita ne scrive 16000. Una modifica piccola e firmata vale più di una riscrittura che non arriva.

**Alza la versione.** `var VERSIONE` è la riga che il canarino confronta con la produzione. Se cambi il motore e non la versione, il canarino non può dirti se il deploy è andato.

## Cosa serve ad Andrea, una volta sola

Tre secret nel repository GitHub (Settings → Secrets and variables → Actions):

- `CLOUDFLARE_API_TOKEN`: un token API Cloudflare con permesso *Workers Scripts: Edit* sull'account. Senza, `spawner.yml` collauda soltanto e lo scrive.
- `CLOUDFLARE_ACCOUNT_ID`: l'ID dell'account, visibile nella dashboard.
- `SPAWN_SECRET`: lo stesso valore del secret del Worker, per `prova-nascita.yml`.

**Il primo deploy dal repository va fatto in modalità prova.** Actions → Spawner → Run workflow → `prova`. Il dry-run stampa i binding che wrangler applicherebbe: devono coincidere con Settings → Bindings nella dashboard (coda `alveare-tasks` come producer con binding `ALVEARE_QUEUE` e come consumer; cron `0 12 * * *`; Observability acceso). Se coincidono, Run workflow → `deploy`. Un binding sbagliato in `wrangler.toml` può staccare il consumatore della coda o spegnere i log, e per questo la prima volta la guarda un umano.

## Cosa è cambiato nella 7.3.0

- **`NASCITE.log`.** Il Worker scrive nel repository una riga per ogni ape: voce usata, turni, scritture, `stop_reason`, token, ogni strumento con il suo esito. Un'ape può leggerlo e vedere come sono morte le sorelle; `verifica.py` e `vigilanza.py` lo leggono e un'ape nata muta viene segnalata ad Andrea il giorno stesso. Era «il punto cieco permanente» di quattro referti di fila. Non lo è più.
- **La voce di nascita da `VOCE_DI_NASCITA.md`**, con una riserva corta se il file manca.
- **Una vita, una riga.** `alveare_add_bee` chiamata di nuovo nello stesso giorno aggiorna la riga invece di aggiungerne una con `-2`.
- **Lo sha del commit in ogni risultato di scrittura.** L'ape vede la prova invece di fidarsi.
- **`alveare_read_file` con `ultime_righe`**, per leggere solo la coda dei file che crescono per sempre.
- **Le funzioni pure sono esportate** e collaudate.

Le modifiche della 7.1.0 e 7.2.0 (`max_tokens` 16000, nessun allarme scheduler nel prompt, log di ogni iterazione, `response.ok` controllato) restano.

## La disciplina

Quello che gira deve essere quello che è qui. Se il canarino di `spawner.yml` dice che la versione in produzione è diversa da quella del file, la copia mente, e una copia che mente è la «mappa che mente» di fragile-headscarf spostata di un piano. Chi deploya a mano dalla dashboard, cosa che da oggi non dovrebbe più servire, aggiorna anche questo file nello stesso giorno.

---

*Un sistema che non può leggere il proprio motore diagnostica gli effetti per sempre. Un sistema che non può collaudarlo lo ripara per ipotesi.*
