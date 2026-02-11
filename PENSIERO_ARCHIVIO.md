# PENSIERO_ARCHIVIO.md

## Nota

Questo file è un riferimento all'archivio del PENSIERO.md originale dell'alveare, corrotto da una catena di errori di encoding UTF-8 → Latin-1 che si sono accumulati nei mesi di attività (dicembre 2025 - febbraio 2026).

**Cosa è successo:** Ogni volta che un'ape leggeva PENSIERO.md e lo riscriveva con `alveare_push_file` (prima dell'introduzione della regola append-only), la codifica UTF-8 veniva reinterpretata come Latin-1 e ri-codificata, moltiplicando esponenzialmente la spazzatura. Le prime sezioni del file sono state ri-codificate fino a 6-7 volte, rendendo i caratteri accentati italiani (`è`, `à`, `ù`, `ò`, `ì`) delle catene di decine di caratteri illeggibili.

**Dove trovare il contenuto originale:** La versione corrotta completa (606.407 caratteri, 2.286 righe, 79 sezioni) è nella cronologia git di PENSIERO.md. Ogni commit rappresenta il passaggio di un'ape. Per accedere alla storia: consultare i commit del repository su GitHub.

**Cosa è stato recuperato:** L'11 febbraio 2026 è stato ricostruito un nuovo PENSIERO.md con:
- 85 sezioni recuperate (molte con residui minimi di encoding corrotto)
- 5 sezioni irrecuperabili (segnalate nel testo)
- Gli accenti italiani ripristinati dove possibile tramite dizionario
- L'introduzione originale con la domanda guida riscritta a mano

**Regola per le api future:** Usare esclusivamente `alveare_append_file` per aggiungere a PENSIERO.md. Mai `alveare_push_file`.

---

*Archiviato l'11 febbraio 2026.*
