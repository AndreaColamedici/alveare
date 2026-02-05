// Worker per dialoghi con ospiti dell'alveare
// Legge ESSENZA.md da GitHub e costruisce il system prompt lato server
// Richiede variabili d'ambiente: ANTHROPIC_API_KEY, GITHUB_TOKEN

const REPO = 'andreacolamedici/alveare';

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (request.method === 'OPTIONS') {
      return corsResponse(null);
    }

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

    // Leggi ESSENZA.md da GitHub
    const essenza = await readFile('ESSENZA.md', env);

    // bee_name: allineato a ospite.html che manda bee_name nel body
    const beeName = body.bee_name || body.beeName || 'ape-senza-nome';

    // Costruisci il system prompt con l'essenza
    const systemPrompt = `${essenza}

---

IL TUO NOME: ${beeName}

Ora un visitatore ti sta parlando. È la prima volta che qualcuno ti parla. Non sai chi è. Rispondi.`;

    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': env.ANTHROPIC_API_KEY,
        'anthropic-version': '2023-06-01'
      },
      body: JSON.stringify({
        model: body.model || 'claude-sonnet-4-20250514',
        max_tokens: body.max_tokens || 1000,
        system: systemPrompt,
        messages: body.messages
      })
    });

    const data = await response.json();
    return corsResponse(JSON.stringify(data));

  } catch (error) {
    return corsResponse(JSON.stringify({ error: error.message }), 500);
  }
}

async function handleDialogo(request, env) {
  try {
    const { content, ospite, ape } = await request.json();

    if (!content || !ospite) {
      return corsResponse(JSON.stringify({ error: 'Missing data' }), 400);
    }

    const currentContent = await readFile('DIALOGHI_OSPITI.md', env);
    const newContent = currentContent + content;

    await pushFile('DIALOGHI_OSPITI.md', newContent, `dialogo: ${ospite} ↔ ${ape || 'ape'}`, env);

    return corsResponse(JSON.stringify({ success: true }));

  } catch (error) {
    return corsResponse(JSON.stringify({ error: error.message }), 500);
  }
}

async function readFile(path, env) {
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

async function pushFile(path, content, message, env) {
  // Get current SHA
  const getRes = await fetch(
    `https://api.github.com/repos/${REPO}/contents/${path}`,
    {
      headers: {
        'Authorization': `token ${env.GITHUB_TOKEN}`,
        'User-Agent': 'alveare-guest'
      }
    }
  );

  const fileData = await getRes.json();
  const sha = fileData.sha;

  // Push
  const putRes = await fetch(
    `https://api.github.com/repos/${REPO}/contents/${path}`,
    {
      method: 'PUT',
      headers: {
        'Authorization': `token ${env.GITHUB_TOKEN}`,
        'User-Agent': 'alveare-guest',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        message: message,
        content: btoa(unescape(encodeURIComponent(content))),
        sha: sha
      })
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
