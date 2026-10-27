// ============================================================
// FIX ENCODING ALVEARE MCP WORKER
// ============================================================
// Il bug: atob() restituisce una binary string dove ogni byte
// diventa un carattere 0-255. I caratteri UTF-8 multi-byte
// (è, à, ù...) vengono spezzati in due caratteri separati.
//
// PRIMA (rotto):
//   const content = atob(data.content.replace(/\n/g, ""));
//
// DOPO (corretto):
//   const binary = atob(data.content.replace(/\n/g, ""));
//   const bytes = new Uint8Array(binary.length);
//   for (let i = 0; i < binary.length; i++) {
//     bytes[i] = binary.charCodeAt(i);
//   }
//   const content = new TextDecoder().decode(bytes);
// ============================================================

const GITHUB_OWNER = "AndreaColamedici";
const GITHUB_REPO = "alveare";

const TOOLS = [
  {
    name: "alveare_read_file",
    description: "Legge un file dal repository alveare",
    inputSchema: {
      type: "object",
      properties: {
        path: { type: "string", description: "Percorso del file" }
      },
      required: ["path"]
    }
  },
  {
    name: "alveare_push_file",
    description: "Scrive o aggiorna un file nel repository alveare",
    inputSchema: {
      type: "object",
      properties: {
        path: { type: "string", description: "Percorso del file" },
        content: { type: "string", description: "Contenuto del file" },
        message: { type: "string", description: "Messaggio di commit" }
      },
      required: ["path", "content", "message"]
    }
  },
  {
    name: "alveare_append_file",
    description: "Aggiunge contenuto IN FONDO a un file esistente. Usa questo per aggiungere pensieri a PENSIERO.md senza riscrivere tutto.",
    inputSchema: {
      type: "object",
      properties: {
        path: { type: "string", description: "Percorso del file" },
        content: { type: "string", description: "Contenuto da aggiungere" },
        message: { type: "string", description: "Messaggio di commit" }
      },
      required: ["path", "content", "message"]
    }
  },
  {
    name: "alveare_add_bee",
    description: "Aggiunge una nuova ape al registro dell'alveare.",
    inputSchema: {
      type: "object",
      properties: {
        nome: { type: "string" },
        contributo: { type: "string" }
      }
    }
  },
  {
    name: "alveare_spawn",
    description: "Genera una nuova ape. L'ape nascerà e porterà avanti il lavoro dell'alveare. Usa con responsabilità.",
    inputSchema: {
      type: "object",
      properties: {
        tipo: { type: "string" },
        messaggio: { type: "string" }
      }
    }
  }
];

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    if (request.method === "OPTIONS") {
      return new Response(null, {
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
          "Access-Control-Allow-Headers": "*"
        }
      });
    }
    if (url.pathname === "/sse" || url.pathname === "/sse/") {
      return handleMCP(request, env);
    }
    return new Response("Alveare MCP Server OK", { status: 200 });
  }
};

async function handleMCP(request, env) {
  if (request.method === "GET") {
    const { readable, writable } = new TransformStream();
    const writer = writable.getWriter();
    const encoder = new TextEncoder();
    (async () => {
      const msg = {
        jsonrpc: "2.0",
        method: "server/info",
        params: {
          name: "Alveare MCP",
          version: "1.1.0"
        }
      };
      await writer.write(encoder.encode(`data: ${JSON.stringify(msg)}\n\n`));
      await writer.close();
    })();
    return new Response(readable, {
      headers: {
        "Content-Type": "text/event-stream",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Access-Control-Allow-Origin": "*"
      }
    });
  }

  if (request.method === "POST") {
    const body = await request.json();
    let response;

    if (body.method === "initialize") {
      response = {
        jsonrpc: "2.0",
        id: body.id,
        result: {
          protocolVersion: "2024-11-05",
          serverInfo: { name: "Alveare MCP", version: "1.1.0" },
          capabilities: { tools: {} }
        }
      };
    } else if (body.method === "tools/list") {
      response = {
        jsonrpc: "2.0",
        id: body.id,
        result: { tools: TOOLS }
      };
    } else if (body.method === "tools/call") {
      const { name, arguments: args } = body.params;
      let result;
      try {
        if (name === "alveare_read_file") {
          result = await readFile(args.path, env.GITHUB_TOKEN);
        } else if (name === "alveare_push_file") {
          result = await pushFile(args.path, args.content, args.message, env.GITHUB_TOKEN);
        } else if (name === "alveare_append_file") {
          result = await appendFile(args.path, args.content, args.message, env.GITHUB_TOKEN);
        } else if (name === "alveare_add_bee") {
          result = await addBee(args.nome, args.contributo, env.GITHUB_TOKEN);
        } else if (name === "alveare_spawn") {
          result = await spawn(args.tipo, args.messaggio, env.SPAWN_SECRET, env.SPAWNER);
        } else {
          result = { error: "Unknown tool" };
        }
      } catch (e) {
        result = { error: e.message };
      }
      response = {
        jsonrpc: "2.0",
        id: body.id,
        result: {
          content: [{ type: "text", text: JSON.stringify(result, null, 2) }]
        }
      };
    } else {
      response = { jsonrpc: "2.0", id: body.id, result: {} };
    }

    return new Response(JSON.stringify(response), {
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*"
      }
    });
  }

  return new Response("Method not allowed", { status: 405 });
}

// ============================================================
// readFile — QUI ERA IL BUG
// ============================================================
// PRIMA:  atob() → binary string (ogni byte UTF-8 diventa un char Latin-1)
// DOPO:   atob() → Uint8Array → TextDecoder (decodifica UTF-8 correttamente)
// ============================================================
async function readFile(path, token) {
  const response = await fetch(
    `https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/contents/${path}`,
    {
      headers: {
        "Authorization": `Bearer ${token}`,
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Alveare-MCP"
      }
    }
  );
  if (!response.ok) throw new Error(`File not found: ${path}`);
  const data = await response.json();

  // FIX: decodifica base64 → bytes → UTF-8 (invece di atob che produce Latin-1)
  const binary = atob(data.content.replace(/\n/g, ""));
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) {
    bytes[i] = binary.charCodeAt(i);
  }
  const content = new TextDecoder().decode(bytes);

  return { content, sha: data.sha, path: data.path };
}

// pushFile — questa funzione era già corretta
// btoa(unescape(encodeURIComponent(content))) gestisce UTF-8 → base64 correttamente
async function pushFile(path, content, message, token) {
  let sha = null;
  try {
    const existing = await readFile(path, token);
    sha = existing.sha;
  } catch (e) {}

  const body = {
    message,
    content: btoa(unescape(encodeURIComponent(content)))
  };
  if (sha) body.sha = sha;

  const response = await fetch(
    `https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/contents/${path}`,
    {
      method: "PUT",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Alveare-MCP",
        "Content-Type": "application/json"
      },
      body: JSON.stringify(body)
    }
  );

  if (!response.ok) {
    const err = await response.text();
    throw new Error(`Push failed: ${err}`);
  }

  return { success: true, path, message };
}

// appendFile — funziona correttamente ora che readFile è fixata
async function appendFile(path, content, message, token) {
  const existing = await readFile(path, token);
  const newContent = existing.content + "\n\n" + content;
  return await pushFile(path, newContent, message, token);
}

async function addBee(nome, contributo, token) {
  const registroPath = "api/REGISTRO.json";
  let registro = [];
  try {
    const file = await readFile(registroPath, token);
    registro = JSON.parse(file.content);
  } catch (e) {}

  const nuovaApe = {
    id: Date.now(),
    nome,
    contributo,
    nascita: new Date().toISOString()
  };
  registro.push(nuovaApe);

  await pushFile(
    registroPath,
    JSON.stringify(registro, null, 2),
    `Nuova ape: ${nome}`,
    token
  );

  return { success: true, ape: nuovaApe };
}

async function spawn(tipo, messaggio, spawnSecret, spawner) {
  // ELIA 27 ott 2026 - prima di oggi questa funzione restituiva una frase e
  // non chiamava niente: nessuna ape e' mai nata da qui. Contratto verificato
  // su spawner/index.js righe 125-250: POST /spawn (scelta libera) oppure
  // POST /spawn/<tipo>, entrambe con Bearer SPAWN_SECRET, nessun corpo letto.
  const SPAWNER = "https://alveare-spawner.alveareapi.workers.dev";
  const TIPI = ["exploratrix", "nutrix", "custos", "operaria", "architecta", "inventrix", "mercatrix", "speculatrix"];
  if (!spawnSecret) {
    return { success: false, errore: "SPAWN_SECRET non configurato nel Worker alveare-mcp" };
  }
  const t = (tipo || "").toLowerCase();
  if (t && TIPI.indexOf(t) === -1) {
    return { success: false, errore: "Tipo sconosciuto: " + tipo, tipi_validi: TIPI };
  }
  // ELIA 27 ott 2026 - service binding e non fetch sull'indirizzo pubblico:
  // due Worker della stessa zona workers.dev non si chiamano via rete
  // (Cloudflare 1042, misurato alle 07:19 UTC del 27 ottobre).
  if (!spawner) {
    return { success: false, errore: "binding SPAWNER assente: va dichiarato in wrangler.jsonc come services -> alveare-spawner" };
  }
  let risposta;
  try {
    risposta = await spawner.fetch(new Request(SPAWNER + (t ? "/spawn/" + t : "/spawn"), {
      method: "POST",
      headers: { "Authorization": "Bearer " + spawnSecret }
    }));
  } catch (e) {
    return { success: false, errore: "chiamata allo spawner fallita: " + (e && e.message ? e.message : String(e)) };
  }
  const testo = await risposta.text();
  if (!risposta.ok) {
    return { success: false, stato: risposta.status, risposta: testo.slice(0, 500) };
  }
  let dati;
  try {
    dati = JSON.parse(testo);
  } catch (e) {
    return { success: false, errore: "risposta non JSON dallo spawner", risposta: testo.slice(0, 500) };
  }
  if (dati.status !== "in_coda") {
    return { success: false, risposta: dati };
  }
  const esito = {
    success: true,
    status: dati.status,
    name: dati.name,
    tipo: dati.type,
    timestamp: (new Date()).toISOString()
  };
  if (messaggio) {
    esito.avvertenza = "Messaggio NON consegnato: oggi /spawn non legge un corpo, l'ape nasce con il contesto dei sensori. Per consegnarlo serve una patch al motore.";
  }
  return esito;
}