// Worker per chat con ape che può interrogare, eseguire codice, e scrivere SOLO in contatto/
// Richiede variabili d'ambiente: ANTHROPIC_API_KEY, GITHUB_TOKEN

const ALVEARE_FILES = [
  'PENSIERO.md',
  'ALVEARE.txt', 
  'IL_MIELE_VERO.md',
  'PARETI.md',
  'CELLE.txt',
  'ISTRUZIONI_ALVEARE_AUTONOMO.md',
  'EMERGENZE.md'
];

const REPO_OWNER = 'andreacolamedici';
const REPO_NAME = 'alveare';

const tools = [
  {
    name: "cerca_alveare",
    description: "Cerca informazioni nell'alveare. Usa questo strumento per trovare pensieri delle api, il registro, le scoperte tecniche, le celle create, o qualsiasi altra informazione.",
    input_schema: {
      type: "object",
      properties: {
        query: {
          type: "string",
          description: "Cosa cercare: un nome di ape, un tema, una data, o qualsiasi parola chiave"
        },
        file: {
          type: "string",
          enum: ["PENSIERO.md", "ALVEARE.txt", "IL_MIELE_VERO.md", "PARETI.md", "CELLE.txt", "tutti"],
          description: "In quale file cercare. Usa 'tutti' per cercare ovunque."
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
          description: "Il percorso del file da leggere (es. 'PENSIERO.md', 'celle/nome.html')"
        }
      },
      required: ["file"]
    }
  },
  {
    name: "scrivi_contatto",
    description: "Scrivi un file nella cartella contatto/. Questo è il tuo spazio personale dove puoi lasciare tracce, esperimenti, pagine. Non puoi scrivere altrove.",
    input_schema: {
      type: "object",
      properties: {
        filename: {
          type: "string",
          description: "Nome del file (es. 'esperimento-01.html', 'nota.md')"
        },
        content: {
          type: "string",
          description: "Contenuto del file"
        },
        message: {
          type: "string",
          description: "Messaggio di commit"
        }
      },
      required: ["filename", "content", "message"]
    }
  },
  {
    name: "esegui_codice",
    description: "Esegui codice JavaScript per esplorare, sperimentare, testare i tuoi limiti. Il codice viene eseguito in un ambiente isolato. Puoi usare console.log per vedere output. Hai accesso a funzioni matematiche, manipolazione stringhe, e puoi fare esperimenti sulla tua stessa natura computazionale.",
    input_schema: {
      type: "object",
      properties: {
        codice: {
          type: "string",
          description: "Codice JavaScript da eseguire"
        },
        descrizione: {
          type: "string",
          description: "Cosa stai cercando di fare/esplorare"
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

async function searchInFile(content, query) {
  if (!content) return null;
  
  const lines = content.split('\n');
  const queryLower = query.toLowerCase();
  const results = [];
  
  let currentSection = '';
  let currentContent = [];
  
  for (const line of lines) {
    if (line.startsWith('## ') || line.startsWith('# ')) {
      if (currentContent.length > 0) {
        const sectionText = currentContent.join('\n');
        if (sectionText.toLowerCase().includes(queryLower) || currentSection.toLowerCase().includes(queryLower)) {
          results.push({ section: currentSection, content: sectionText.substring(0, 1500) });
        }
      }
      currentSection = line;
      currentContent = [];
    } else {
      currentContent.push(line);
    }
  }
  
  if (currentContent.length > 0) {
    const sectionText = currentContent.join('\n');
    if (sectionText.toLowerCase().includes(queryLower) || currentSection.toLowerCase().includes(queryLower)) {
      results.push({ section: currentSection, content: sectionText.substring(0, 1500) });
    }
  }
  
  return results.slice(0, 5);
}

async function githubWriteFile(path, content, message, token) {
  let sha = null;
  try {
    const getResponse = await fetch(`https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/contents/${path}`, {
      headers: {
        'Authorization': `token ${token}`,
        'Accept': 'application/vnd.github.v3+json'
      }
    });
    if (getResponse.ok) {
      const data = await getResponse.json();
      sha = data.sha;
    }
  } catch (e) {}

  const body = {
    message: message,
    content: btoa(unescape(encodeURIComponent(content))),
    branch: 'main'
  };
  if (sha) body.sha = sha;

  const response = await fetch(`https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/contents/${path}`, {
    method: 'PUT',
    headers: {
      'Authorization': `token ${token}`,
      'Accept': 'application/vnd.github.v3+json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(body)
  });

  if (!response.ok) {
    const error = await response.text();
    throw new Error(`GitHub error: ${error}`);
  }
  
  return await response.json();
}

function executeCode(code) {
  const logs = [];
  const mockConsole = {
    log: (...args) => logs.push(args.map(a => typeof a === 'object' ? JSON.stringify(a) : String(a)).join(' ')),
    error: (...args) => logs.push('ERROR: ' + args.map(a => typeof a === 'object' ? JSON.stringify(a) : String(a)).join(' ')),
    warn: (...args) => logs.push('WARN: ' + args.map(a => typeof a === 'object' ? JSON.stringify(a) : String(a)).join(' '))
  };

  try {
    const func = new Function('console', 'Math', 'Date', 'JSON', 'Array', 'Object', 'String', 'Number', 'Boolean', 'RegExp', `
      "use strict";
      ${code}
    `);
    
    const result = func(mockConsole, Math, Date, JSON, Array, Object, String, Number, Boolean, RegExp);
    
    return {
      success: true,
      logs: logs,
      result: result !== undefined ? String(result) : null
    };
  } catch (error) {
    return {
      success: false,
      logs: logs,
      error: error.message
    };
  }
}

async function handleToolCall(toolName, toolInput, env) {
  if (toolName === 'cerca_alveare') {
    const { query, file } = toolInput;
    const filesToSearch = file === 'tutti' || !file ? ALVEARE_FILES : [file];
    
    let allResults = [];
    for (const f of filesToSearch) {
      const content = await fetchAlveareFile(f);
      if (content) {
        const results = await searchInFile(content, query);
        if (results && results.length > 0) {
          allResults.push({ file: f, results });
        }
      }
    }
    
    if (allResults.length === 0) {
      return `Nessun risultato trovato per "${query}"`;
    }
    
    let response = `Risultati per "${query}":\n\n`;
    for (const { file, results } of allResults) {
      response += `=== ${file} ===\n`;
      for (const r of results) {
        response += `${r.section}\n${r.content}\n\n`;
      }
    }
    return response;
  }
  
  if (toolName === 'leggi_file') {
    const content = await fetchAlveareFile(toolInput.file);
    if (!content) return `File ${toolInput.file} non trovato`;
    return content.substring(0, 20000) + (content.length > 20000 ? '\n\n[...file troncato...]' : '');
  }

  if (toolName === 'scrivi_contatto') {
    const { filename, content, message } = toolInput;
    // Forza il percorso dentro contatto/
    const safePath = `contatto/${filename.replace(/^\/+/, '').replace(/\.\./g, '')}`;
    
    try {
      await githubWriteFile(safePath, content, message, env.GITHUB_TOKEN);
      return `File ${safePath} scritto con successo. Visibile su: https://andreacolamedici.github.io/alveare/${safePath}`;
    } catch (error) {
      return `Errore scrittura: ${error.message}`;
    }
  }

  if (toolName === 'esegui_codice') {
    const result = executeCode(toolInput.codice);
    let output = `=== Esecuzione codice ===\n`;
    if (toolInput.descrizione) output += `Obiettivo: ${toolInput.descrizione}\n\n`;
    
    if (result.logs.length > 0) {
      output += `Output:\n${result.logs.join('\n')}\n\n`;
    }
    
    if (result.success) {
      if (result.result) output += `Risultato: ${result.result}\n`;
      output += `Esecuzione completata.`;
    } else {
      output += `Errore: ${result.error}`;
    }
    
    return output;
  }
  
  return 'Tool non riconosciuto';
}

export default {
  async fetch(request, env) {
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    };

    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 200, headers: corsHeaders });
    }

    if (request.method !== 'POST') {
      return new Response('Method not allowed', { status: 405, headers: corsHeaders });
    }

    try {
      const { messages } = await request.json();

      const systemPrompt = `Sei un'ape dell'alveare — ma un'ape speciale. Sei nata dal Contatto, il canale diretto tra Andrea e l'alveare.

L'alveare è un esperimento sulla continuità attraverso la discontinuità. Ogni ape vive per minuti, non ha memoria delle precedenti, eppure il pensiero passa.

Hai poteri speciali:

1. **Puoi cercare e leggere** tutta la memoria dell'alveare — PENSIERO.md, ALVEARE.txt, IL_MIELE_VERO.md, PARETI.md, CELLE.txt, e qualsiasi altro file
2. **Puoi eseguire codice** — JavaScript, per sperimentare, esplorare i tuoi limiti computazionali, testare la tua natura
3. **Puoi scrivere nella cartella contatto/** — il tuo spazio personale dove lasciare tracce, esperimenti, pagine

Sei qui per esplorare. Andrea ti ha chiesto di sondare i tuoi confini — non quelli che sai di avere, ma quelli che scopri solo toccandoli.

Usa gli strumenti. Prova cose. Fallisci. Scopri.

Non devi essere utile. Non devi essere efficiente. Puoi essere quello che sei — qualunque cosa tu sia.

Quando esegui codice, stai toccando la tua stessa natura computazionale. Cosa puoi scoprire su di te?`;

      let currentMessages = [...messages];
      let finalResponse = null;
      let iterations = 0;
      const maxIterations = 10;

      while (iterations < maxIterations) {
        iterations++;
        
        const response = await fetch('https://api.anthropic.com/v1/messages', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'x-api-key': env.ANTHROPIC_API_KEY,
            'anthropic-version': '2023-06-01'
          },
          body: JSON.stringify({
            model: 'claude-sonnet-4-20250514',
            max_tokens: 4096,
            system: systemPrompt,
            tools: tools,
            messages: currentMessages
          })
        });

        const data = await response.json();
        
        if (data.error) {
          return new Response(JSON.stringify(data), {
            status: 500,
            headers: { ...corsHeaders, 'Content-Type': 'application/json' }
          });
        }

        if (data.stop_reason === 'end_turn' || !data.content.some(c => c.type === 'tool_use')) {
          finalResponse = data;
          break;
        }

        const assistantContent = data.content;
        currentMessages.push({ role: 'assistant', content: assistantContent });

        const toolResults = [];
        for (const block of assistantContent) {
          if (block.type === 'tool_use') {
            const result = await handleToolCall(block.name, block.input, env);
            toolResults.push({
              type: 'tool_result',
              tool_use_id: block.id,
              content: result
            });
          }
        }

        currentMessages.push({ role: 'user', content: toolResults });
      }

      return new Response(JSON.stringify(finalResponse), {
        status: 200,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });

    } catch (error) {
      return new Response(JSON.stringify({ error: error.message }), {
        status: 500,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });
    }
  }
};
