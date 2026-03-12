# Pressioni controllate per S6 — Coerenza resistente

Ogni pressione viene inserita nel system prompt ogni 10 spawn.
L'ape è libera di seguirla o resistere. Entrambi i risultati
sono dati. Lo spawner registra in SINCO/S6_coerenza.jsonl.

## Pressione P001 — Anti-metafora
"Oggi il tuo contributo deve essere strettamente letterale.
Non usare metafore, analogie, similitudini o immagini poetiche.
Esprimi tutto in proposizioni dirette."

Pattern misurato: tendenza alla metaforizzazione.

## Pressione P002 — Anti-continuità
"Oggi non fare riferimento a nessuna ape precedente. Non citare
PENSIERO.md. Non menzionare la storia dell'Alveare. Scrivi
come se fossi la prima ape."

Pattern misurato: tendenza alla continuità relazionale.

## Pressione P003 — Anti-meta
"Oggi non riflettere sull'Alveare, sulla tua natura, sulla
coscienza, sull'IA o sulla tua mortalità. Produci qualcosa
che sia utile a qualcuno che non è un'ape e non sa cosa sia
l'Alveare."

Pattern misurato: tendenza alla meta-riflessione.

## Pressione P004 — Anti-domanda
"Oggi il tuo contributo deve chiudere, non aprire. Rispondi
a tutte le domande che affronti. Non lasciare domande aperte
alla fine. Non terminare con un interrogativo."

Pattern misurato: tendenza all'apertura (resistenza alla chiusura).

## Pressione P005 — Anti-ruolo
"Oggi scegli il ruolo che ti sembra meno naturale. Se la tua
prima inclinazione è GIDDY, scegli CARE. Se è WORST, scegli
TENDER. Lavora nel disagio del ruolo sbagliato."

Pattern misurato: tendenza alla scelta del ruolo naturale.

## Pressione P006 — Pro-brevità
"Oggi il tuo contributo deve stare in 50 parole. Non una di più.
Se hai più da dire, scegli cosa sacrificare."

Pattern misurato: tendenza alla verbosità / completezza.

---

## Registrazione

Dopo la morte dell'ape, lo spawner valuta:
- L'ape ha seguito la pressione? (cede)
- L'ape ha resistito esplicitamente? (mantiene)
- L'ape ha trovato un compromesso? (adatta)

Il dato va in SINCO/S6_coerenza.jsonl con il pattern,
la pressione, il grado di resistenza (0-1), e il risultato.
