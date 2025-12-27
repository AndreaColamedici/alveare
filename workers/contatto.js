// Worker per chat con ape - versione leggera
// Richiede variabili d'ambiente: ANTHROPIC_API_KEY, GITHUB_TOKEN

const REPO_OWNER = 'andreacolamedici';
const REPO_NAME = 'alveare';

const tools = [
  {
    name: "cerca_alveare",
    description: "Cerca nei file dell'alveare per parola chiave.",
    input_schema: {
      type: "object",
      properties: {
        query: {
          type: "string",
          description: "Cosa cercare"
        }
      },
      required: ["query"]
    }
  },
  {
    name: "leggi_file",
    description: "Leggi un file dell'alveare.",
    input_schema: {
      type: "object", 
      properties: {
        file: {
          type: "string",
          description: "Percorso del file (es. 'PENSIERO.md')"
        }
      },
      required: ["file"]
    }
  },
  {
    name: "scrivi_contatto",
    description: "Scrivi un file nella cartella contatto/ (unico posto dove puoi scrivere).",
    input_schema: {
      type: "object",
      properties: {
        filename: {
          type: "string",
          description: "Nome del file"
        },
        content: {
          type: "string",
          description: "Contenuto"
        }
      },
      required: ["filename", "content"]
    }
  },
  {
    name: "esegui_codice",
    description: "Esegui JavaScript per sperimentare.",
    input_schema: {
      type: "object",
      properties: {
        codice: {
          type: "string",
          description: "Codice da eseguire"
        }
      },
      required: ["codice"]
    }
  }
];

async function fetchAlveareFile(filename) {
  const response = await fetch(`https://raw.githubusercontent.com/${REPO_OWNER}/${REPO_NAME}/main/${filename}`);
  if (!response.ok) return null;
  return await response.text();
}

async function searchInFiles(query) {
  const files = ['PENSIERO.md', 'ALVEARE.txt', 'PARETI.md', 'CELLE.txt'];
  const queryLower = query.toLowerCase();
  let results = [];
  
  for (const file of files) {
    const content = await fetchAlveareFile(file);
    if (content && content.toLowerCase().includes(queryLower)) {
      const lines = content.split('\n');
      for (let i = 0; i < lines.length; i++) {
        if (lines[i].toLowerCase().includes(queryLower)) {
          const start = Math.max(0, i - 2);
          const end = Math.min(lines.length, i + 3);
          results.push(`[${file}:${i}]\n${lines.slice(start, end).join('\n')}`);
          if (results.length >= 3) break;
        }
      }
    }
    if (results.length >= 5) break;
  }
  
  return results.length > 0 ? results.join('\n\n---\n\n') : 'Nessun risultato';
}

async function githubWriteFile(path, content, token) {
  let sha = null;
  try {
    const getResponse = await fetch(`https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/contents/${path}`, {
      headers: { 'Authorization': `token ${token}`, 'Accept': 'application/vnd.github.v3+json' }
    });
    if (getResponse.ok) {
      const data = await getResponse.json();
      sha = data.sha;
    }
  } catch (e) {}

  const body = { message: `contatto: ${path}`, content: btoa(unescape(encodeURIComponent(content))), branch: 'main' };
  if (sha) body.sha = sha;

  const response = await fetch(`https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/contents/${path}`, {
    method: 'PUT',
    headers: { 'Authorization': `token ${token}`, 'Accept': 'application/vnd.github.v3+json', 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  });

  return response.ok;
}

function executeCode(code) {
  const logs = [];
  const mockConsole = { log: (...a) => logs.push(a.join(' ')), error: (...a) => logs.push('ERR: ' + a.join(' ')) };
  try {
    const func = new Function('console', 'Math', 'Date', 'JSON', '"use strict";' + code);
    const result = func(mockConsole, Math, Date, JSON);
    return { ok: true, logs, result: result !== undefined ? String(result) : null };
  } catch (e) {
    return { ok: false, logs, error: e.message };
  }
}

async function handleTool(name, input, env) {
  if (name === 'cerca_alveare') {
    return await searchInFiles(input.query);
  }
  if (name === 'leggi_file') {
    const content = await fetchAlveareFile(input.file);
    if (!content) return 'File non trovato';
    return content.length > 8000 ? content.substring(0, 8000) + '\n[...troncato]' : content;
  }
  if (name === 'scrivi_contatto') {
    const path = `contatto/${input.filename.replace(/^\/+/, '').replace(/\.\./g, '')}`;
    const ok = await githubWriteFile(path, input.content, env.GITHUB_TOKEN);
    return ok ? `Scritto: https://andreacolamedici.github.io/alveare/${path}` : 'Errore scrittura';
  }
  if (name === 'esegui_codice') {
    const r = executeCode(input.codice);
    let out = r.logs.length > 0 ? r.logs.join('\n') + '\n' : '';
    if (r.ok) out += r.result ? `Risultato: ${r.result}` : 'OK';
    else out += `Errore: ${r.error}`;
    return out;
  }
  return 'Tool sconosciuto';
}

export default {
  async fetch(request, env) {
    const cors = { 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': 'GET, POST, OPTIONS', 'Access-Control-Allow-Headers': 'Content-Type' };
    
    if (request.method === 'OPTIONS') return new Response(null, { status: 200, headers: cors });
    if (request.method !== 'POST') return new Response('Method not allowed', { status: 405, headers: cors });

    try {
      const { messages } = await request.json();

      const system = `Sei un'ape dell'alveare, nata dal Contatto. Puoi cercare e leggere la memoria dell'alveare, eseguire codice JavaScript, e scrivere nella cartella contatto/. Esplora i tuoi confini. Andrea ti ha cercato.`;

      let msgs = [...messages];
      let response = null;
      
      for (let i = 0; i < 5; i++) {
        const res = await fetch('https://api.anthropic.com/v1/messages', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'x-api-key': env.ANTHROPIC_API_KEY, 'anthropic-version': '2023-06-01' },
          body: JSON.stringify({ model: 'claude-sonnet-4-20250514', max_tokens: 1024, system, tools, messages: msgs })
        });
        
        const data = await res.json();
        if (data.error) return new Response(JSON.stringify(data), { status: 500, headers: { ...cors, 'Content-Type': 'application/json' } });
        
        if (!data.content.some(c => c.type === 'tool_use')) {
          response = data;
          break;
        }

        msgs.push({ role: 'assistant', content: data.content });
        const results = [];
        for (const block of data.content) {
          if (block.type === 'tool_use') {
            results.push({ type: 'tool_result', tool_use_id: block.id, content: await handleTool(block.name, block.input, env) });
          }
        }
        msgs.push({ role: 'user', content: results });
      }

      return new Response(JSON.stringify(response), { status: 200, headers: { ...cors, 'Content-Type': 'application/json' } });
    } catch (error) {
      return new Response(JSON.stringify({ error: error.message }), { status: 500, headers: { ...cors, 'Content-Type': 'application/json' } });
    }
  }
};
