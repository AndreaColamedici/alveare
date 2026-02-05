// Worker per dialoghi con ospiti dell'alveare
// Proxy leggero: riceve da ospite.html, inoltra ad Anthropic, salva i dialoghi
// Richiede variabili d'ambiente: ANTHROPIC_API_KEY, GITHUB_TOKEN

const REPO_OWNER = 'andreacolamedici';
const REPO_NAME = 'alveare';
const DIALOGHI_PATH = 'DIALOGHI_OSPITI.md';

export default {
  async fetch(request, env) {
    const cors = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type'
    };

    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 200, headers: cors });
    }

    if (request.method !== 'POST') {
      return new Response('Method not allowed', { status: 405, headers: cors });
    }

    const url = new URL(request.url);

    // ─── /chat → proxy verso Anthropic ───
    if (url.pathname === '/chat') {
      try {
        const body = await request.json();
        const { model, max_tokens, system, messages, bee_name } = body;

        console.log(`[GUEST] Chat da ape ${bee_name || 'sconosciuta'}, ${messages.length} messaggi`);

        const anthropicResponse = await fetch('https://api.anthropic.com/v1/messages', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'x-api-key': env.ANTHROPIC_API_KEY,
            'anthropic-version': '2023-06-01'
          },
          body: JSON.stringify({
            model: model || 'claude-sonnet-4-20250514',
            max_tokens: max_tokens || 1000,
            system: system,
            messages: messages
          })
        });

        const data = await anthropicResponse.json();

        if (data.error) {
          console.log(`[GUEST] Errore API: ${JSON.stringify(data.error)}`);
        }

        return new Response(JSON.stringify(data), {
          status: anthropicResponse.status,
          headers: { ...cors, 'Content-Type': 'application/json' }
        });

      } catch (error) {
        console.log(`[GUEST] Eccezione chat: ${error.message}`);
        return new Response(JSON.stringify({ error: { message: error.message } }), {
          status: 500,
          headers: { ...cors, 'Content-Type': 'application/json' }
        });
      }
    }

    // ─── /dialogo → salva su GitHub ───
    if (url.pathname === '/dialogo') {
      try {
        const { content, ospite, ape } = await request.json();

        console.log(`[GUEST] Salvataggio dialogo: ${ospite} ↔ ${ape}`);

        // Leggi il file esistente
        const headers = {
          'Authorization': `token ${env.GITHUB_TOKEN}`,
          'Accept': 'application/vnd.github.v3+json',
          'User-Agent': 'Alveare-Guest-Worker'
        };

        let existingContent = '';
        let sha = null;

        try {
          const getResponse = await fetch(
            `https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/contents/${DIALOGHI_PATH}`,
            { headers }
          );

          if (getResponse.ok) {
            const fileData = await getResponse.json();
            sha = fileData.sha;
            existingContent = atob(fileData.content);
          }
        } catch (e) {
          console.log(`[GUEST] File non trovato, creo nuovo`);
        }

        // Append del dialogo
        const newContent = existingContent + content;

        const putBody = {
          message: `dialogo: ${ospite} ↔ ${ape}`,
          content: btoa(unescape(encodeURIComponent(newContent))),
          branch: 'main'
        };
        if (sha) putBody.sha = sha;

        const putResponse = await fetch(
          `https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/contents/${DIALOGHI_PATH}`,
          {
            method: 'PUT',
            headers: { ...headers, 'Content-Type': 'application/json' },
            body: JSON.stringify(putBody)
          }
        );

        if (!putResponse.ok) {
          const errText = await putResponse.text();
          console.log(`[GUEST] Errore GitHub: ${errText}`);
          return new Response(JSON.stringify({ error: 'Errore salvataggio' }), {
            status: 500,
            headers: { ...cors, 'Content-Type': 'application/json' }
          });
        }

        console.log(`[GUEST] Dialogo salvato`);
        return new Response(JSON.stringify({ ok: true }), {
          status: 200,
          headers: { ...cors, 'Content-Type': 'application/json' }
        });

      } catch (error) {
        console.log(`[GUEST] Eccezione dialogo: ${error.message}`);
        return new Response(JSON.stringify({ error: error.message }), {
          status: 500,
          headers: { ...cors, 'Content-Type': 'application/json' }
        });
      }
    }

    // ─── fallback ───
    return new Response('Not found', { status: 404, headers: cors });
  }
};
