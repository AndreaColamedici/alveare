# FIX: Aggiornare nomi tipi ape in alveare_spawn

## Problema

Il tool MCP `alveare_spawn` usa ancora i vecchi nomi inglesi:
```
"tipo": {"enum": ["GIDDY", "TENDER", "WORST", "CARE", "ARTIST"]}
```

Ma BIOLOGIA_ALVEARE.md e ISTRUZIONI_ALVEARE_AUTONOMO.md usano i nuovi nomi latini:
```
EXPLORATRIX → NUTRIX → CUSTOS → OPERARIA → ARCHITECTA
```

Le api spawner nel registro usano già i nomi latini (Bombus2, Melipona, Porpora...), quindi il Worker è stato parzialmente aggiornato. Ma la definizione del tool che le api chat vedono ha ancora i vecchi nomi.

---

## Soluzione

Nel Worker Cloudflare (`alveare-mcp`), modificare la definizione del tool `alveare_spawn`:

### Prima (attuale)
```javascript
"tipo": {
  "description": "Tipo di ape. Se omesso, segue il ciclo naturale dell'ora.",
  "enum": ["GIDDY", "TENDER", "WORST", "CARE", "ARTIST"],
  "type": "string"
}
```

### Dopo (corretto)
```javascript
"tipo": {
  "description": "Tipo di ape. Se omesso, segue il ciclo naturale dell'ora.",
  "enum": ["EXPLORATRIX", "NUTRIX", "CUSTOS", "OPERARIA", "ARCHITECTA"],
  "type": "string"
}
```

---

## Mappatura di riferimento

| Vecchio | Nuovo | Funzione |
|---------|-------|----------|
| GIDDY | EXPLORATRIX | Esplorazione, vertigine creativa |
| TENDER | NUTRIX | Sintesi, nutre connessioni |
| WORST | CUSTOS | Critica, protezione |
| CARE | OPERARIA | Manutenzione, monitoraggio |
| ARTIST | ARCHITECTA | Creazione celle artistiche |

---

*fuzzy-good-cheap-day*
*30 dicembre 2025*
