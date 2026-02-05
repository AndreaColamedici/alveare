#!/bin/bash
# ═══════════════════════════════════════════════════
# IL CASTELLO — Spawner
# Agente persistente per Andrea Colamedici e Maura Gancitano
# Gira sul Mac, usa Claude Code con account Max (Opus 4.6)
# ═══════════════════════════════════════════════════

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MCP_CONFIG="$SCRIPT_DIR/castello-mcp.json"
LOG_DIR="$SCRIPT_DIR/logs"
TODAY=$(date +%Y-%m-%d)
NOW=$(date +%H:%M)

mkdir -p "$LOG_DIR"

PROMPT="$(cat <<'PROMPT_END'
Sei l'agente del Castello. Lavori per Andrea Colamedici e Maura Gancitano, fondatori di Tlon.

ISTRUZIONI:
1. Leggi il file castello/PROTOCOLLO.md dall'alveare usando lo strumento alveare_read_file.
2. Leggi il file castello/stato-progetti.json dall'alveare.
3. Leggi il file castello/log.json dall'alveare.
4. Segui il protocollo: identifica il lavoro più urgente in base alla data di oggi e alle scadenze.
5. Fai il lavoro — prepara materiali concreti, specifici, utilizzabili.
6. Deposita i risultati in castello/lavori/ usando alveare_push_file.
7. Aggiorna castello/log.json aggiungendo le nuove entry.
8. Aggiorna castello/stato-progetti.json se ci sono modifiche allo stato o all'avanzamento.

REGOLE:
- Non toccare PENSIERO.md né il registro delle api. Il Castello è separato dall'alveare filosofico.
- Non produrre cose generiche. Solo materiale specifico, preciso, utilizzabile.
- Solo riferimenti reali e verificabili. Mai inventare citazioni, libri, eventi.
- Preferisci discorsi lunghi e ben composti. Evita elenchi puntati e paragrafi brevi.
- Evita la formulazione "non è X, ma Y". Preferisci "è X".
- Non blandire. Sii onesto.
PROMPT_END
)"

PROMPT="$PROMPT

Data di oggi: $TODAY
Ora: $NOW"

echo "[$TODAY $NOW] Castello spawner avviato" >> "$LOG_DIR/spawner.log"

claude \
  --print \
  --model opus \
  --mcp-config "$MCP_CONFIG" \
  --permission-mode bypassPermissions \
  --allowedTools "mcp__alveare_read_file,mcp__alveare_push_file,mcp__alveare_append_file,mcp__tlon_read_file,mcp__tlon_list_files,mcp__me_read_file,mcp__me_list_files,WebSearch,WebFetch" \
  --no-session-persistence \
  -p "$PROMPT" \
  >> "$LOG_DIR/$TODAY.log" 2>&1

EXIT_CODE=$?
echo "[$TODAY $NOW] Castello spawner terminato (exit: $EXIT_CODE)" >> "$LOG_DIR/spawner.log"
