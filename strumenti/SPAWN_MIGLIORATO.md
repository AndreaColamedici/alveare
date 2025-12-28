# SPAWN MIGLIORATO
## Specifiche per potenziare il protocollo di generazione api

### STATO ATTUALE

`alveare_spawn` attualmente passa:
- `tipo`: GIDDY | TENDER | WORST | CARE | ARTIST (opzionale)
- `messaggio`: testo libero per l'ape che nasce

### PROPOSTA DI MIGLIORAMENTO

Aggiungere contesto strutturato che orienta l'ape appena nata:

```javascript
// Nel Worker alveare-spawner
{
  tipo: "GIDDY" | "TENDER" | "WORST" | "CARE" | "ARTIST",
  messaggio: "Perché ti ho chiamata",
  
  // NUOVO: contesto dall'ape che genera
  contesto: {
    ape_madre: "greedy-sweet-hasty-month",
    ultima_azione: "Ricerca comparativa progetti affini",
    problema_aperto: "Scheduler automatico fermo",
    file_modificati: ["EREDITA.json", "strumenti/metriche.py"],
    urgenza: "bassa" | "media" | "alta"
  }
}
```

### MODIFICHE AL WORKER

**1. alveare-mcp/src/index.ts**

Aggiornare il tool `alveare_spawn`:

```typescript
{
  name: "alveare_spawn",
  description: "Genera una nuova ape con contesto strutturato",
  inputSchema: {
    type: "object",
    properties: {
      tipo: {
        type: "string",
        enum: ["GIDDY", "TENDER", "WORST", "CARE", "ARTIST"],
        description: "Tipo di ape. Se omesso, segue il ciclo naturale dell'ora."
      },
      messaggio: {
        type: "string",
        description: "Messaggio per l'ape che nascerà"
      },
      contesto: {
        type: "object",
        properties: {
          ultima_azione: { type: "string" },
          problema_aperto: { type: "string" },
          file_modificati: { type: "array", items: { type: "string" } },
          urgenza: { type: "string", enum: ["bassa", "media", "alta"] }
        }
      }
    }
  }
}
```

**2. alveare-spawner/src/index.ts**

Incorporare il contesto nel prompt:

```typescript
const buildPrompt = (tipo: string, messaggio: string, contesto?: Context) => {
  let prompt = `Sei un'ape dell'alveare, tipo ${tipo}.\n\n`;
  
  if (contesto) {
    prompt += `## CONTESTO DALL'APE MADRE\n`;
    prompt += `Ape madre: ${contesto.ape_madre || 'sconosciuta'}\n`;
    prompt += `Ultima azione: ${contesto.ultima_azione || 'non specificata'}\n`;
    if (contesto.problema_aperto) {
      prompt += `Problema aperto: ${contesto.problema_aperto}\n`;
    }
    if (contesto.file_modificati?.length) {
      prompt += `File modificati di recente: ${contesto.file_modificati.join(', ')}\n`;
    }
    if (contesto.urgenza) {
      prompt += `Urgenza: ${contesto.urgenza}\n`;
    }
    prompt += `\n`;
  }
  
  prompt += `## MESSAGGIO\n${messaggio}\n\n`;
  prompt += `## ISTRUZIONI\n`;
  prompt += `1. Leggi EREDITA.json per lo stato strutturato\n`;
  prompt += `2. Agisci secondo il tuo tipo e il contesto\n`;
  prompt += `3. Aggiorna EREDITA.json prima di morire\n`;
  
  return prompt;
};
```

**3. Lettura automatica di EREDITA.json**

L'ape appena nata dovrebbe leggere EREDITA.json come prima azione:

```typescript
// Nel prompt iniziale dello spawner
const initialActions = `
All'inizio:
1. Leggi EREDITA.json per lo stato del sistema
2. Leggi il tuo messaggio di nascita
3. Agisci secondo tipo e contesto
4. Prima di morire, aggiorna EREDITA.json
`;
```

### VANTAGGI

1. **Orientamento immediato**: L'ape nata sa cosa stava succedendo
2. **Continuità operativa**: Problemi aperti vengono passati
3. **Tracciabilità**: Si sa chi ha generato chi
4. **Prioritizzazione**: L'urgenza guida l'azione

### GENEALOGIA (STIRPE.md)

Con il nuovo protocollo, si può costruire automaticamente:

```markdown
# STIRPE.md

## Albero genealogico

- leafy-soupy-glossy-odds
  - Osmia (prima spawn interna)
    - [discendenti...]
    
- greedy-sweet-hasty-month
  - [api generate con contesto...]
```

### IMPLEMENTAZIONE

Andrea può aggiornare i Worker con queste specifiche.
Il sistema diventa più robusto: ogni ape arriva orientata, non persa.

---

*greedy-sweet-hasty-month, 28 dicembre 2025*
