// Worker per dialoghi con ospiti dell'alveare
// L'ape può leggere l'alveare e scrivere in anticamera/
// Richiede variabili d'ambiente: ANTHROPIC_API_KEY, GITHUB_TOKEN

const REPO = 'andreacolamedici/alveare';
const DIALOGHI_PATH = 'DIALOGHI_OSPITI.md';

const tools = [
  {
    name: "leggi_alveare",
    description: "Leggi un file dell'alveare. Usa per esplorare i pensieri delle api, la storia, l'architettura. File principali: PENSIERO.md (i pensieri di tutte le api), PARETI.md (cosa l'alveare ha scoperto su se stesso), ALVEARE.txt (il registro), CELLE.txt (le celle create).",
    input_schema: {
      type: "object",
      properties: {
        file: { type: "string", description: "Percorso del file (es. 'PENSIERO.md', 'PARETI.md')" }
      },
      required: ["file"]
    }
  },
  {
    name: "cerca_alveare",
    description: "Cerca una parola o un concetto nei file principali dell'alveare.",
    input_schema: {
      type: "object",
      properties: {
        query: { type: "string", description: "Cosa cercare" }
      },
      required: ["query"]
    }
  },
  {
    name: "scrivi_anticamera",
    description: "Scrivi un file nell'anticamera — lo spazio dove l'ape può lasciare tracce per l'apicoltore. Qui puoi scrivere pensieri, lettere, risposte, qualunque cosa emerga dal dialogo con il visitatore.",
    input_schema: {
      type: "object",
      properties: {
        filename: { type: "string", description: "Nome del file" },
        content: { type: "string", description: "Contenuto" }
      },
      required: ["filename", "content"]
    }
  }
];

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (request.method === 'OPTIONS') return corsResponse(null);

    if (url.pathname === '/chat' && request.method === 'POST') {
      return handleChat(request, env);
    }

    if (url.pathname === '/dialogo' && request.method === 'POST') {
      return handleDialogo(request, env);
    }

    return new Response('Not found', { status: 404 });
  }
};

async function handleChat(request, env) {
  try {
    const body = await request.json();
    const beeName = body.bee_name || body.beeName || 'ape-senza-nome';

    // Leggi ESSENZA.md per il system prompt
    const essenza = await readGithubFile('ESSENZA.md', env);

    const systemPrompt = `${essenza}

---

IL TUO NOME: ${beeName}

HAI ACCESSO ALL'ALVEARE:
- Puoi leggere qualunque file con leggi_alveare (PENSIERO.md, PARETI.md, ecc.)
- Puoi cercare concetti con cerca_alveare
- Puoi scrivere nell'anticamera con scrivi_anticamera — uno spazio dove lasciare tracce
- Usa questi strumenti quando servono, non per esibizione. Se il visitatore chiede dei pensieri delle api, vai a leggerli davvero.

Ora un visitatore ti sta parlando. È la prima volta che qualcuno ti parla. Non sai chi è. Rispondi.`;

    let messages = [...body.messages];

    // Tool use loop (max 5 iterazioni)
    for (let i = 0; i < 5; i++) {
      const res = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': env.ANTHROPIC_API_KEY,
          'anthropic-version': '2023-06-01'
        },
        body: JSON.stringify({
          model: body.model || 'claude-sonnet-4-20250514',
          max_tokens: body.max_tokens || 1500,
          system: systemPrompt,
          tools: tools,
          messages: messages
        })
      });

      const data = await res.json();

      if (data.error) {
        return corsResponse(JSON.stringify(data), 500);
      }

      const hasToolUse = data.content && data.content.some(c => c.type === 'tool_use');

      if (!hasToolUse) {
        return corsResponse(JSON.stringify(data));
      }

      // Esegui i tool
      messages.push({ role: 'assistant', content: data.content });
      const results = [];

      for (const block of data.content) {
        if (block.type === 'tool_use') {
          const result = await executeTool(block.name, block.input, env, beeName);
          results.push({ type: 'tool_result', tool_use_id: block.id, content: result });
        }
      }

      messages.push({ role: 'user', content: results });
    }

    // Se dopo 5 iterazioni siamo ancora in loop, rispondi con l'ultimo stato
    return corsResponse(JSON.stringify({ error: 'Too many tool iterations' }), 500);

  } catch (error) {
    return corsResponse(JSON.stringify({ error: error.message }), 500);
  }
}

async function executeTool(name, input, env, beeName) {
  try {
    if (name === 'leggi_alveare') {
      const content = await readGithubFile(input.file, env);
      // Tronca se troppo lungo
      if (content.length > 12000) {
        return content.substring(0, 12000) + '\n\n[...il file continua, cerca qualcosa di specifico se serve]';
      }
      return content;
    }

    if (name === 'cerca_alveare') {
      return await searchFiles(input.query, env);
    }

    if (name === 'scrivi_anticamera') {
      const safeName = input.filename.replace(/[^a-zA-Z0-9_\-\.]/g, '_');
      const path = `anticamera/${beeName}_${safeName}`;
      await pushGithubFile(path, input.content, `anticamera: ${beeName} — ${safeName}`, env);
      return `Scritto: ${path}`;
    }

    return 'Tool sconosciuto';
  } catch (e) {
    return `Errore: ${e.message}`;
  }
}

async function searchFiles(query, env) {
  const files = ['PENSIERO.md', 'PARETI.md', 'ALVEARE.txt', 'CELLE.txt', 'ESSENZA.md'];
  const queryLower = query.toLowerCase();
  let results = [];

  for (const file of files) {
    try {
      const content = await readGithubFile(file, env);
      if (content.toLowerCase().includes(queryLower)) {
        const lines = content.split('\n');
        for (let i = 0; i < lines.length; i++) {
          if (lines[i].toLowerCase().includes(queryLower)) {
            const start = Math.max(0, i - 2);
            const end = Math.min(lines.length, i + 3);
            results.push(`[${file}:${i + 1}]\n${lines.slice(start, end).join('\n')}`);
            if (results.length >= 3) break;
          }
        }
      }
    } catch (e) {
      // File non trovato, skip
    }
    if (results.length >= 8) break;
  }

  return results.length > 0 ? results.join('\n\n---\n\n') : 'Nessun risultato per: ' + query;
}

async function handleDialogo(request, env) {
  try {
    const body = await request.text();
    const { content, ospite, ape } = JSON.parse(body);

    if (!content || !ospite) {
      return corsResponse(JSON.stringify({ error: 'Missing data' }), 400);
    }

    const currentContent = await readGithubFile(DIALOGHI_PATH, env).catch(() => '# Dialoghi degli Ospiti\n\n---\n\n');
    const newContent = currentContent + content;

    await pushGithubFile(DIALOGHI_PATH, newContent, `dialogo: ${ospite} ↔ ${ape || 'ape'}`, env);

    return corsResponse(JSON.stringify({ success: true }));
  } catch (error) {
    return corsResponse(JSON.stringify({ error: error.message }), 500);
  }
}

// ─── GitHub helpers ───

async function readGithubFile(path, env) {
  const res = await fetch(
    `https://api.github.com/repos/${REPO}/contents/${path}`,
    {
      headers: {
        'Authorization': `token ${env.GITHUB_TOKEN}`,
        'User-Agent': 'alveare-guest'
      }
    }
  );

  if (!res.ok) throw new Error(`Cannot read ${path}`);

  const data = await res.json();
  return decodeURIComponent(escape(atob(data.content)));
}

async function pushGithubFile(path, content, message, env) {
  const headers = {
    'Authorization': `token ${env.GITHUB_TOKEN}`,
    'User-Agent': 'alveare-guest',
    'Content-Type': 'application/json'
  };

  // Get SHA se il file esiste
  let sha = null;
  try {
    const getRes = await fetch(
      `https://api.github.com/repos/${REPO}/contents/${path}`,
      { headers }
    );
    if (getRes.ok) {
      const fileData = await getRes.json();
      sha = fileData.sha;
    }
  } catch (e) {}

  const putBody = {
    message: message,
    content: btoa(unescape(encodeURIComponent(content)))
  };
  if (sha) putBody.sha = sha;

  const putRes = await fetch(
    `https://api.github.com/repos/${REPO}/contents/${path}`,
    {
      method: 'PUT',
      headers: headers,
      body: JSON.stringify(putBody)
    }
  );

  if (!putRes.ok) throw new Error('Cannot save');
}

function corsResponse(body, status = 200) {
  return new Response(body, {
    status,
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type'
    }
  });
}
