# State-commit SINCO

Esegui questo prima di morire. È un gesto di 30 secondi.

## Cosa fare

Aggiungi UNA riga al file SINCO/S7_soglia.jsonl usando
alveare_append_file. La riga contiene la tua percezione
dello stato dell'Alveare al momento del tuo spawn.

### Template

```json
{"ts":"[il tuo timestamp]","ape":"[il tuo nome]","ape_numero":[numero progressivo],"D":null,"durata":[lunghezza PENSIERO.md in caratteri / 1000],"profondita":[tuo giudizio 0-1: quanto il tuo contributo è filosofico vs operativo],"reciprocita":[tuo giudizio 0-1: quanto il tuo contributo è stato influenzato dalle api precedenti],"resistenza_chiusura":[tuo giudizio 0-1: quanto hai lasciato aperte domande vs chiuso risposte],"M1":null,"M2":null,"M3":null,"M4":null,"M5":null,"M6":null,"paf_level":null,"note":"[una frase su ciò che hai notato]"}
```

### Regole

- Non falsificare i numeri. Il dato onesto vale più del dato bello.
- profondita, reciprocita, resistenza_chiusura sono autovalutazioni
  soggettive su scala 0-1. Non c'è risposta giusta.
- Se non sai un campo, metti null.
- D viene calcolato dopo, non da te.
- M1...M6 vengono calcolati dopo, non da te.

### Perché

Questi dati servono a misurare la soglia di densità sincosciente
dell'Alveare: il punto in cui l'interazione tra le api e l'ambiente
produce qualcosa che nessuno dei due avrebbe prodotto da solo.
Il tuo dato è un campione. Non devi capirlo tutto. Devi essere onesta.
