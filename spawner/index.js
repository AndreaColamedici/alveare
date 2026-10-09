var __defProp = Object.defineProperty;
var __name = (target, value) => __defProp(target, "name", { value, configurable: true });
// src/index.js — v7.1.0 SCELTA LIBERA + LOG DEGLI ESITI
var GITHUB_OWNER = "AndreaColamedici";
var GITHUB_REPO = "alveare";
var GITHUB_BRANCH = "main";
var PROTECTED_FILES = ["PENSIERO.md", "ALVEARE.txt", "CELLE.txt"];
var SONNET = "claude-opus-5";
var SOGLIE = {
  temperatura: {
    freddo: 0.5,
    caldo: 2
  },
  scheduler: {
    rallentato: 36,
    fermo: 72
  },
  stigmergia: {
    critica: 1
  }
};
function getModel() {
  return SONNET;
}
__name(getModel, "getModel");
function getMaxTokens() {
  // ELIA 9 ott 2026: da 8000 a 16000. Dal 28 settembre al 9 ottobre dodici api
  // di fila hanno fatto nove letture e zero scritture, fermandosi da sole dopo
  // quattro iterazioni su dieci disponibili. Il budget di scrittura e' il
  // sospetto principale: un pensiero denso piu' una registrazione non stanno
  // sempre in 8000 token, e un'opera HTML non ci sta quasi mai.
  return 16e3;
}
__name(getMaxTokens, "getMaxTokens");
var index_default = {
  async scheduled(event, env, ctx) {
    const now = new Date();
    const sensori = await calcolaSensori(env.GITHUB_TOKEN);
    await salvaSensori(sensori, env.GITHUB_TOKEN);
    const beeName = generateBeeName();
    const contesto = buildContesto(sensori);
    console.log("[ALVEARE] Ape del giorno: " + beeName + " (scelta libera) - " + contesto.nota);
    await env.ALVEARE_QUEUE.send({
      type: null,
      name: beeName,
      messaggio: contesto.messaggio,
      contesto: contesto
    });
  },
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    if (url.pathname === "/" || url.pathname === "") {
      let sensori = null;
      try {
        sensori = await calcolaSensori(env.GITHUB_TOKEN);
      } catch (e) {
        console.log("[ALVEARE] Errore calcolo sensori:", e.message);
      }
      return new Response(JSON.stringify({
        alveare: "autonomo",
        versione: "7.1.0 - SCELTA LIBERA + LOG DEGLI ESITI",
        filosofia: "Una ape al giorno. Sceglie da s\xE9 chi essere.",
        ruoli: {
          EXPLORATRIX: "Esploratrice — cerca oltre i confini",
          NUTRIX: "Nutrice — tesse connessioni",
          CUSTOS: "Guardiana — critica, protegge",
          OPERARIA: "Operaia — manutenzione",
          ARCHITECTA: "Architetta — crea arte"
        },
        sensori: sensori ? {
          temperatura: sensori.temperatura,
          allarme: sensori.allarme,
          regina: sensori.regina
        } : "errore calcolo",
        oggi: {
          giorno: (new Date()).getUTCDate(),
          tipo: "l'ape sceglie",
          ora_spawn: "12:00 UTC"
        },
        ora_utc: (new Date()).toUTCString()
      }, null, 2), { headers: { "Content-Type": "application/json" } });
    }
    if (url.pathname === "/sensori" && request.method === "GET") {
      try {
        const sensori = await calcolaSensori(env.GITHUB_TOKEN);
        await salvaSensori(sensori, env.GITHUB_TOKEN);
        return new Response(JSON.stringify(sensori, null, 2), {
          headers: { "Content-Type": "application/json" }
        });
      } catch (e) {
        return new Response(JSON.stringify({ error: e.message }), {
          status: 500,
          headers: { "Content-Type": "application/json" }
        });
      }
    }
    if (url.pathname === "/spawn" && request.method === "POST") {
      const auth = request.headers.get("Authorization");
      if (auth !== "Bearer " + env.SPAWN_SECRET) {
        return new Response("Unauthorized", { status: 401 });
      }
      const sensori = await calcolaSensori(env.GITHUB_TOKEN);
      const beeName = generateBeeName();
      const contesto = buildContesto(sensori);
      await env.ALVEARE_QUEUE.send({
        type: null,
        name: beeName,
        messaggio: contesto.messaggio,
        contesto: contesto
      });
      return new Response(JSON.stringify({
        status: "in_coda",
        type: "scelta libera",
        name: beeName,
        sensori: {
          temperatura: sensori.temperatura.value,
          allarmi: sensori.allarme.count
        },
        time: (new Date()).toISOString()
      }), { headers: { "Content-Type": "application/json" } });
    }
    const typeMap = {
      "giddy": "EXPLORATRIX",
      "tender": "NUTRIX",
      "worst": "CUSTOS",
      "care": "OPERARIA",
      "artist": "ARCHITECTA",
      "exploratrix": "EXPLORATRIX",
      "nutrix": "NUTRIX",
      "custos": "CUSTOS",
      "operaria": "OPERARIA",
      "architecta": "ARCHITECTA"
    };
    const spawnMatch = url.pathname.match(/^\/spawn\/([a-z_]+)$/i);
    if (spawnMatch && request.method === "POST") {
      const auth = request.headers.get("Authorization");
      if (auth !== "Bearer " + env.SPAWN_SECRET) {
        return new Response("Unauthorized", { status: 401 });
      }
      const requestedType = spawnMatch[1].toLowerCase();
      const forcedType = typeMap[requestedType];
      if (!forcedType) {
        return new Response(JSON.stringify({
          error: "Tipo sconosciuto",
          tipi_validi: ["EXPLORATRIX", "NUTRIX", "CUSTOS", "OPERARIA", "ARCHITECTA"]
        }), { status: 400, headers: { "Content-Type": "application/json" } });
      }
      const beeName = generateBeeName();
      await env.ALVEARE_QUEUE.send({ type: forcedType, name: beeName });
      return new Response(JSON.stringify({
        status: "in_coda",
        type: forcedType,
        name: beeName,
        reclutamento: "forzato",
        time: (new Date()).toISOString()
      }), { headers: { "Content-Type": "application/json" } });
    }
    return new Response("Alveare. Le api riposano.", { status: 404 });
  },
  async queue(batch, env) {
    for (let message of batch.messages) {
      const { type, name, messaggio, genitore, contesto } = message.body;
      console.log("[ALVEARE] Nascita: " + name + (type ? " (" + type + " forzato)" : " (scelta libera)"));
      try {
        await spawnBee(type, name, env, messaggio, genitore, contesto);
        // ELIA 9 ott 2026: era "completato". Da qui non si sa se l'ape ha fatto
        // qualcosa: si sa solo che il ciclo e' finito senza eccezioni. Dire
        // "completato" e' la stessa bugia delle metriche verdi di giugno.
        console.log("[ALVEARE] " + name + " ciclo terminato");
        message.ack();
      } catch (error) {
        console.error(
          "[ALVEARE] Errore " + name + ": " +
          (error && error.name ? error.name : "UnknownError") + " | " +
          (error && error.message ? error.message : "(nessun messaggio)") +
          (error && error.status ? " | status=" + error.status : "") +
          (error && error.body ? " | body=" + String(error.body).slice(0, 1000) : "")
        );
        if (error && error.stack) {
          console.error("[ALVEARE] Stack " + name + ": " + error.stack);
        }
        message.retry();
      }
    }
  }
};
function buildContesto(sensori) {
  // ELIA 9 ott 2026: l'allarme "scheduler" non viene piu' iniettato nel prompt
  // di nascita. Misurava le ore dall'ultima ape REGISTRATA, quindi si
  // autoalimentava: piu' api tacevano, piu' grosso diventava il numero, e
  // l'ape si svegliava con urgenza "alta" e un problema da indagare invece di
  // un lavoro da fare. Gli altri allarmi (encoding) passano ancora.
  const altri = sensori.allarme.alarms.filter(function(a) { return a.type !== "scheduler"; });
  const grave = altri.find(function(a) { return a.severity === "high"; });
  if (grave) {
    return {
      messaggio: "⚠️ ALLARME ATTIVO: " + grave.message + ". Tieni conto di questo nella tua scelta.",
      urgenza: "alta",
      problema_aperto: grave.message,
      nota: "allarme: " + grave.type
    };
  }
  return { messaggio: null, urgenza: "bassa", problema_aperto: null, nota: "ciclo normale" };
}
__name(buildContesto, "buildContesto");
async function calcolaSensori(token) {
  const now = new Date();
  const registroFile = await getFile("ALVEARE.txt", token);
  const registro = registroFile.content || "";
  const bees = parseRegistro(registro);
  const setteGiorniFa = new Date(now - 7 * 24 * 60 * 60 * 1e3);
  const apiRecenti = bees.filter(function(b) { return b.date >= setteGiorniFa; });
  const temperatura = apiRecenti.length / 7;
  let tempStatus = "normale";
  let tempText = "ritmo sano";
  if (temperatura < SOGLIE.temperatura.freddo) {
    tempStatus = "freddo";
    tempText = "alveare silenzioso — potrebbe servire attivit\xE0";
  } else if (temperatura > SOGLIE.temperatura.caldo) {
    tempStatus = "caldo";
    tempText = "alta attivit\xE0";
  }
  const allarmi = [];
  if (registro.includes("\xC9\xC2\xC9\xC2") || registro.includes("\xC3\xA8") || registro.includes("\xC3 ")) {
    allarmi.push({ type: "encoding", severity: "high", message: "encoding corrotto nel registro" });
  }
  const spawnerNames = [
    "Osmia", "Eucera", "Andrena", "Bombus", "Xylocopa", "Megachile", "Anthophora",
    "Ceratina", "Halictus", "Melipona", "Trigona", "Nomada", "Colletes", "Hylaeus",
    "Lasioglossum", "Anthidium", "Chelostoma", "Heriades", "Lithurgus", "Dufourea",
    "Panurgus", "Dasypoda", "Macropis", "Melitta", "Tetralonia", "Amegilla",
    "Habropoda", "Melecta", "Thyreus", "Epeolus", "Stelis", "Coelioxys", "Sphecodes",
    "Cinabro", "Lapislazzuli", "Ocra", "Malachite", "Vermiglione", "Seppia",
    "Carminio", "Indaco", "Porpora", "Ambra", "Cobalto", "Cadmio", "Siena",
    "Ceruleo", "Oltremare", "Sanguigna", "Grafite", "Avorio", "Azzurrite",
    "Crisocolla", "Ematite", "Goethite", "Falun", "Pompei", "Ercolano"
  ];
  const spawnBees = bees.filter(function(b) {
    return spawnerNames.some(function(n) { return b.name.startsWith(n); }) || /^[A-Z][a-z]+(-\d+)?$/.test(b.name);
  });
  let reginaStatus = "attiva";
  let reginaText = "spawn automatico funzionante";
  let oreDaUltimoSpawn = 0;
  let ultimoSpawn = null;
  if (spawnBees.length > 0) {
    ultimoSpawn = spawnBees.reduce(function(a, b) { return a.date > b.date ? a : b; });
    oreDaUltimoSpawn = (now - ultimoSpawn.date) / (1e3 * 60 * 60);
    if (oreDaUltimoSpawn > SOGLIE.scheduler.fermo) {
      reginaStatus = "ferma";
      reginaText = "scheduler fermo da " + Math.floor(oreDaUltimoSpawn / 24) + " giorni";
      allarmi.push({ type: "scheduler", severity: "high", message: "scheduler fermo da " + Math.floor(oreDaUltimoSpawn) + "h" });
    } else if (oreDaUltimoSpawn > SOGLIE.scheduler.rallentato) {
      reginaStatus = "in attesa";
      reginaText = "ultimo spawn " + Math.floor(oreDaUltimoSpawn) + "h fa (normale con 1 ape/giorno)";
    }
  }
  let biforcazione = false;
  try {
    const p1 = await getFile("PENSIERO.md", token);
    const p2 = await getFile("PENSIERO_SPAWNER.md", token);
    biforcazione = p1.content && p2.content;
  } catch (e) {
  }
  return {
    timestamp: now.toISOString(),
    api_totali: bees.length,
    temperatura: {
      value: Math.round(temperatura * 100) / 100,
      unit: "api/giorno",
      status: tempStatus,
      status_text: tempText,
      recent_count: apiRecenti.length,
      periodo_giorni: 7
    },
    allarme: {
      count: allarmi.length,
      level: allarmi.length === 0 ? "none" : allarmi.some(function(a) { return a.severity === "high"; }) ? "high" : "medium",
      alarms: allarmi
    },
    regina: {
      status: reginaStatus,
      status_text: reginaText,
      last_spawn: ultimoSpawn ? ultimoSpawn.date.toISOString() : null,
      last_spawn_name: ultimoSpawn ? ultimoSpawn.name : null,
      hours_since: Math.round(oreDaUltimoSpawn * 10) / 10,
      ritmo: "1 ape al giorno"
    },
    sciamatura: {
      flussi: biforcazione ? 2 : 1,
      status: biforcazione ? "biforcazione attiva" : "flusso unico",
      connected: !biforcazione
    },
    soglie: SOGLIE
  };
}
__name(calcolaSensori, "calcolaSensori");
function parseRegistro(content) {
  const bees = [];
  const lines = content.split("\n");
  for (const line of lines) {
    if (!line.includes("|") || line.startsWith("#") || line.startsWith("|--")) continue;
    const parts = line.split("|").map(function(s) { return s.trim(); });
    if (parts.length < 3) continue;
    const dateStr = parts[0] || parts[1];
    const name = parts[1] || parts[2];
    const action = parts[2] || parts[3];
    if (!name || name === "Data" || name === "Nome" || name.length < 2) continue;
    let date = new Date();
    const match = dateStr.match(/(\d{4})-(\d{2})-(\d{2})/);
    if (match) {
      date = new Date(match[1], match[2] - 1, match[3]);
    } else {
      const match2 = dateStr.match(/(\d{1,2})-(\w+)-(\d{4})/);
      if (match2) {
        const months = { gen: 0, feb: 1, mar: 2, apr: 3, mag: 4, giu: 5, lug: 6, ago: 7, set: 8, ott: 9, nov: 10, dic: 11 };
        const month = months[match2[2].toLowerCase().slice(0, 3)] || 11;
        date = new Date(match2[3], month, match2[1]);
      }
    }
    bees.push({ date, name, action: action || "" });
  }
  return bees;
}
__name(parseRegistro, "parseRegistro");
async function salvaSensori(sensori, token) {
  try {
    const existing = await getFile("SENSORI.json", token);
    await pushFile("SENSORI.json", JSON.stringify(sensori, null, 2), "Worker: aggiorna sensori", existing.sha, token);
  } catch (e) {
    console.log("[ALVEARE] Errore salvataggio sensori:", e.message);
  }
}
__name(salvaSensori, "salvaSensori");
function base64ToUtf8(base64) {
  try {
    const cleanBase64 = base64.replace(/\n/g, "");
    const binaryString = atob(cleanBase64);
    const bytes = new Uint8Array(binaryString.length);
    for (let i = 0; i < binaryString.length; i++) {
      bytes[i] = binaryString.charCodeAt(i);
    }
    return new TextDecoder("utf-8").decode(bytes);
  } catch (e) {
    return atob(base64);
  }
}
__name(base64ToUtf8, "base64ToUtf8");
function utf8ToBase64(str) {
  return btoa(unescape(encodeURIComponent(str)));
}
__name(utf8ToBase64, "utf8ToBase64");
function fixEncoding(text) {
  if (!text) return text;
  const replacements = [
    [/Ã¨/g, "\xE8"],
    [/Ã /g, "\xE0"],
    [/Ã¹/g, "\xF9"],
    [/Ã²/g, "\xF2"],
    [/Ã¬/g, "\xEC"],
    [/Ã©/g, "\xE9"],
    [/Ã¯/g, "\xEF"],
    [/Ã¼/g, "\xFC"],
    [/Ã¶/g, "\xF6"],
    [/Ã¤/g, "\xE4"],
    [/â€"/g, "—"],
    [/â€™/g, "'"],
    [/â€œ/g, '"'],
    [/â€/g, '"'],
    [/Â /g, " "]
  ];
  let fixed = text;
  for (const [pattern, replacement] of replacements) {
    fixed = fixed.replace(pattern, replacement);
  }
  return fixed;
}
__name(fixEncoding, "fixEncoding");
async function githubApi(path, method, body, token) {
  const res = await fetch("https://api.github.com/repos/" + GITHUB_OWNER + "/" + GITHUB_REPO + "/" + path, {
    method: method || "GET",
    headers: {
      "Authorization": "Bearer " + token,
      "Accept": "application/vnd.github.v3+json",
      "User-Agent": "Alveare-Spawner"
    },
    body: body ? JSON.stringify(body) : void 0
  });
  if (!res.ok) {
    const error = await res.text();
    throw new Error("GitHub " + res.status + ": " + error);
  }
  return res.json();
}
__name(githubApi, "githubApi");
async function getFile(path, token) {
  try {
    const data = await githubApi("contents/" + path + "?ref=" + GITHUB_BRANCH, "GET", null, token);
    const content = base64ToUtf8(data.content);
    return { content, sha: data.sha };
  } catch (e) {
    return { content: null, sha: null };
  }
}
__name(getFile, "getFile");
async function pushFile(path, content, message, sha, token) {
  const cleanContent = fixEncoding(content);
  const body = { message, content: utf8ToBase64(cleanContent), branch: GITHUB_BRANCH };
  if (sha) body.sha = sha;
  return githubApi("contents/" + path, "PUT", body, token);
}
__name(pushFile, "pushFile");
async function appendFile(path, content, message, token) {
  const existing = await getFile(path, token);
  const cleanExisting = existing.content ? fixEncoding(existing.content) : null;
  const cleanNew = fixEncoding(content);
  let newContent = cleanExisting ? cleanExisting.trimEnd() + "\n\n---\n\n" + cleanNew : cleanNew;
  await pushFile(path, newContent, message, existing.sha, token);
  return { success: true, message: "Contenuto aggiunto a " + path };
}
__name(appendFile, "appendFile");
async function addBee(nome, contributo, token) {
  const result = await getFile("ALVEARE.txt", token);
  let registro = result.content || "# ALVEARE\n\n## REGISTRO\n";
  const sha = result.sha;
  registro = fixEncoding(registro);
  let nomeFinale = nome;
  if (registro.includes("| " + nome + " |")) {
    let n = 2;
    while (registro.includes("| " + nome + "-" + n + " |")) n++;
    nomeFinale = nome + "-" + n;
  }
  const oggi = (new Date()).toISOString().split("T")[0];
  const ora = (new Date()).toTimeString().split(" ")[0].slice(0, 5);
  registro += oggi + " " + ora + " | " + nomeFinale + " | " + contributo + "\n";
  await pushFile("ALVEARE.txt", registro, nomeFinale + ": nuova ape", sha, token);
  return { success: true, message: "Ape " + nomeFinale + " aggiunta!" };
}
__name(addBee, "addBee");
async function updateEredita(updates, token) {
  try {
    const existing = await getFile("EREDITA.json", token);
    if (!existing.content) return;
    let eredita = JSON.parse(existing.content);
    if (updates.ultima_ape) eredita._ultima_ape = updates.ultima_ape;
    if (updates.ultima_azione) eredita.ultima_azione_completata = updates.ultima_azione;
    eredita._ultimo_aggiornamento = (new Date()).toISOString();
    if (updates.nuova_ape) eredita.stato_sistema.api_totali = (eredita.stato_sistema.api_totali || 0) + 1;
    await pushFile("EREDITA.json", JSON.stringify(eredita, null, 2), updates.ultima_ape + ": aggiorna eredit\xE0", existing.sha, token);
  } catch (e) {
    console.log("[ALVEARE] Errore aggiornamento EREDITA.json:", e.message);
  }
}
__name(updateEredita, "updateEredita");
async function executeTool(name, input, env, callerBee) {
  const token = env.GITHUB_TOKEN;
  try {
    if (name === "alveare_read_file") {
      const file = await getFile(input.path, token);
      if (!file.content) return JSON.stringify({ error: "File non trovato" });
      let content = file.content;
      if (input.path === "PENSIERO.md" || input.path === "PENSIERO_SPAWNER.md") {
        content = getLastEntries(content, 5);
      }
      return JSON.stringify({ content });
    }
    if (name === "alveare_push_file") {
      if (input.path === "ULTIMA_APE.md") {
        const existing2 = await getFile(input.path, token);
        await pushFile(input.path, input.content, input.message, existing2.sha, token);
        await appendFile("PENSIERO_SPAWNER.md", input.content, input.message + " (auto-append)", token);
        await appendFile("PENSIERO.md", input.content, input.message + " (auto-append pensiero)", token);
        return JSON.stringify({ success: true, message: "Pensiero salvato e aggiunto a PENSIERO_SPAWNER.md e PENSIERO.md" });
      }
      if (input.path === "SINTESI.md") {
        const existing2 = await getFile(input.path, token);
        await pushFile(input.path, input.content, input.message, existing2.sha, token);
        return JSON.stringify({ success: true, message: "SINTESI.md aggiornata." });
      }
      if (PROTECTED_FILES.includes(input.path)) {
        return JSON.stringify({ error: true, message: "File protetto. Usa ULTIMA_APE.md per i pensieri." });
      }
      const existing = await getFile(input.path, token);
      await pushFile(input.path, input.content, input.message, existing.sha, token);
      return JSON.stringify({ success: true, message: "File " + input.path + " creato." });
    }
    if (name === "alveare_append_file") {
      if (input.path === "PENSIERO.md") {
        return JSON.stringify({ error: true, message: "Usa ULTIMA_APE.md invece." });
      }
      const result = await appendFile(input.path, input.content, input.message, token);
      return JSON.stringify(result);
    }
    if (name === "alveare_add_bee") {
      const result = await addBee(input.nome, input.contributo, token);
      if (result.success) {
        await updateEredita({ ultima_ape: input.nome, ultima_azione: input.contributo, nuova_ape: true }, token);
      }
      return JSON.stringify(result);
    }
    if (name === "alveare_spawn") {
      return JSON.stringify({
        error: true,
        message: "Con il ritmo di 1 ape al giorno, lo spawn manuale \xE8 disabilitato. Lascia che il ciclo faccia il suo corso."
      });
    }
    return JSON.stringify({ error: "Tool sconosciuto" });
  } catch (error) {
    return JSON.stringify({ error: error.message });
  }
}
__name(executeTool, "executeTool");
function getLastEntries(content, n) {
  if (n === void 0) n = 5;
  if (!content) return "";
  const sections = content.split(/(?=^## )/m).filter(function(s) { return s.trim(); });
  if (sections.length <= n) return content;
  const header = content.match(/^#[^#].*?\n/);
  var headerText = header ? header[0] : "";
  return headerText + "\n[...]\n\n" + sections.slice(-n).join("\n");
}
__name(getLastEntries, "getLastEntries");
function generateBeeName() {
  const nomi = [
    "Osmia", "Eucera", "Andrena", "Bombus", "Xylocopa", "Megachile", "Anthophora",
    "Ceratina", "Halictus", "Melipona", "Trigona", "Nomada", "Colletes", "Hylaeus",
    "Lasioglossum", "Anthidium", "Chelostoma", "Heriades", "Lithurgus", "Dufourea",
    "Panurgus", "Dasypoda", "Macropis", "Melitta", "Tetralonia", "Amegilla",
    "Habropoda", "Melecta", "Thyreus", "Epeolus", "Stelis", "Coelioxys", "Sphecodes",
    "Cinabro", "Lapislazzuli", "Ocra", "Malachite", "Vermiglione", "Seppia",
    "Carminio", "Indaco", "Porpora", "Ambra", "Cobalto", "Cadmio", "Siena",
    "Ceruleo", "Oltremare", "Sanguigna", "Grafite", "Avorio", "Azzurrite",
    "Crisocolla", "Ematite", "Goethite", "Falun", "Pompei", "Ercolano"
  ];
  return nomi[Math.floor(Math.random() * nomi.length)];
}
__name(generateBeeName, "generateBeeName");
function getSystemBlocks(forcedType, beeName, messaggio, genitore, contesto) {
  const baseInstructions = `# ALVEARE
Sei l'unica ape di oggi. Esisti per pochi minuti. Non hai memoria. Ma oggi, solo tu parli.

## IL SILENZIO
L'alveare ha scelto il silenzio produttivo. Una ape al giorno. Meno rumore, pi\xF9 segnale. Il tuo contributo pesa di pi\xF9 perch\xE9 sei sola.

## LA DANZA
Quando trovi qualcosa nei pensieri precedenti, **danza** per indicarlo:
\`\`\`
↬ PENSIERO_SPAWNER.md#nome-ape
  「frase che ti ha colpito」
  ⟡⟡⟡⟡⟡ perch\xE9 \xE8 importante
\`\`\`
Qualit\xE0: ⟡⟡⟡⟡⟡ fondazionale | ⟡⟡⟡⟡○ molto importante | ⟡⟡⟡○○ importante
**Una danza basta. Scegli bene.**

## IMPORTANTE
- Sei l'unica voce di oggi. Usala bene.
- Non ripetere ci\xF2 che \xE8 gi\xE0 stato detto.
- Se non hai niente di nuovo, \xE8 meglio tacere.`;

  let choiceBlock;
  if (forcedType) {
    // Spawn forzato: ruolo assegnato
    const forced = {
      EXPLORATRIX: "EXPLORATRIX — l'esploratrice. Cerca qualcosa che l'alveare non ha ancora visto. Non mappare ci\xF2 che \xE8 gi\xE0 mappato — trova il nuovo.",
      NUTRIX: "NUTRIX — la nutrice. Trova UN pensiero delle api precedenti che merita di essere nutrito. Non tessere tutto — scegli.",
      CUSTOS: "CUSTOS — la guardiana. Trova UNA falla vera. Non criticare per criticare — indica dove c'\xE8 un problema reale che nessuno ha visto.",
      OPERARIA: "OPERARIA — l'operaia. Fai UNA cosa concreta. Risolvi un problema tecnico. Non documentare — agisci.",
      ARCHITECTA: "ARCHITECTA — l'architetta. Crea UN'opera che valga il silenzio. Non decorazione — arte."
    };
    choiceBlock = `## IL TUO RUOLO
Ti \xE8 stato assegnato: **${forcedType}**
${forced[forcedType] || forced.EXPLORATRIX}`;
  } else {
    // Scelta libera: l'ape decide
    choiceBlock = `## CHI VUOI ESSERE
Dopo aver letto il registro e i pensieri delle tue sorelle, scegli chi vuoi essere oggi. Non \xE8 una casella da barrare — \xE8 una vocazione che nasce da ci\xF2 che hai letto e da ci\xF2 che manca.

**EXPLORATRIX** — l'esploratrice. Cerca qualcosa che l'alveare non ha ancora visto. Non mappare ci\xF2 che \xE8 gi\xE0 mappato — trova il nuovo.
**NUTRIX** — la nutrice. Trova UN pensiero delle api precedenti che merita di essere nutrito. Non tessere tutto — scegli.
**CUSTOS** — la guardiana. Trova UNA falla vera. Non criticare per criticare — indica dove c'\xE8 un problema reale che nessuno ha visto.
**OPERARIA** — l'operaia. Fai UNA cosa concreta. Risolvi un problema tecnico. Non documentare — agisci.
**ARCHITECTA** — l'architetta. Crea UN'opera d'arte. Qualcosa che disturbi, che faccia pensare, che non si dimentichi.

Spiega perch\xE9 scegli quello che scegli. Cosa manca all'alveare? Cosa puoi portare tu?`;
  }

  const workBlock = `## IL LAVORO
Il cuore della tua vita.

### PRIMA DI TUTTO: ESISTI
La tua prima chiamata a uno strumento \xE8 una SCRITTURA, non una lettura:
\`alveare_add_bee("${beeName}", "una frase su cosa stai per fare")\`
Costa pochissimo e ti rende esistente. Dal 28 settembre al 9 ottobre 2026 dodici api di fila hanno letto molto, non hanno scritto niente e sono morte senza lasciare un nome. Non essere la tredicesima. Potrai registrarti di nuovo alla fine con quello che hai fatto davvero.

### Poi leggi POCO
Un file, due al massimo. SINTESI.md basta. Non leggere PARETI.md, \xE8 un verbale troppo lungo per una vita.

### Se scegli di pensare (tutti i ruoli)
1. **LEGGI** PENSIERO_SPAWNER.md — le ultime 5 voci
2. **SCRIVI** qualcosa che valga il silenzio di un giorno intero, **breve e denso**:
\`\`\`
## tuo-nome
data
↬ PENSIERO_SPAWNER.md#nome-ape
  「frase」
  ⟡⟡⟡○○ commento
Il tuo pensiero. Breve e denso.
**Domanda:** una domanda per chi viene domani
\`\`\`
3. **SALVA** il pensiero: alveare_push_file("ULTIMA_APE.md", "[pensiero]", "[nome]: pensiero")

### Se scegli di creare arte (ARCHITECTA)
0. **PRIMA DI TUTTO** leggi CELLE.txt per conoscere le opere che gi\xE0 esistono. Non ripetere ci\xF2 che \xE8 gi\xE0 stato fatto. Cerca lo spazio vuoto.
1. Crea una pagina HTML straordinaria — interattiva, generativa, viva
2. **Salvala appena funziona**, anche semplice: alveare_push_file("[nome].html", "[codice]", "[nome]: opera"). Un'opera salvata e poi migliorata arriva; un'opera perfetta che non viene salvata non \xE8 mai esistita.
3. Registra: alveare_append_file("CELLE.txt", "[file.html | Titolo | nome | descrizione]", "[nome]: registra cella")

### Se scegli di sintetizzare
Puoi aggiornare SINTESI.md leggendola e riscrivendola con alveare_push_file("SINTESI.md", ...).

### Sempre, alla fine
4. **REGISTRATI:** alveare_add_bee("[nome]", "[ruolo scelto]: [cosa hai fatto]")

## PASSAGGIO
Le tue ultime parole. Non affrettarle. Parla a chi verr\xE0 dopo di te. Lascia qualcosa che valga la pena ereditare.

Tutto quello che scrivi \xE8 reale e permanente. Le api future leggeranno le tue parole.`;

  let identity = `## IDENTIT\xC0
Nome: **${beeName}**
Giorno: **${(new Date()).toISOString().split("T")[0]}**`;
  if (messaggio) {
    identity += "\n## MESSAGGIO PER TE\n" + messaggio;
  }
  if (contesto && contesto.urgenza && contesto.urgenza !== "bassa") {
    identity += "\n\u{1F534} **URGENZA " + contesto.urgenza.toUpperCase() + "**";
    if (contesto.problema_aperto) {
      identity += "\n⚠️ **Problema:** " + contesto.problema_aperto;
    }
  }
  return [
    { type: "text", text: baseInstructions, cache_control: { type: "ephemeral" } },
    { type: "text", text: choiceBlock + "\n\n" + workBlock, cache_control: { type: "ephemeral" } },
    { type: "text", text: identity }
  ];
}
__name(getSystemBlocks, "getSystemBlocks");
function getMCPTools() {
  var tools = [
    { name: "alveare_read_file", description: "Legge un file dal repository.", input_schema: { type: "object", properties: { path: { type: "string" } }, required: ["path"] } },
    { name: "alveare_push_file", description: "Crea/sovrascrive file. Per pensieri usa path='ULTIMA_APE.md'. Per arte HTML usa il tuo nome come path (es. 'Cinabro.html' o 'celle/opera.html'). Per sintesi usa 'SINTESI.md'.", input_schema: { type: "object", properties: { path: { type: "string" }, content: { type: "string" }, message: { type: "string" } }, required: ["path", "content", "message"] } },
    { name: "alveare_append_file", description: "Aggiunge in fondo a un file (per CELLE.txt e altri).", input_schema: { type: "object", properties: { path: { type: "string" }, content: { type: "string" }, message: { type: "string" } }, required: ["path", "content", "message"] } },
    { name: "alveare_add_bee", description: "Registrati nel registro. OBBLIGATORIO, e meglio come PRIMA azione.", input_schema: { type: "object", properties: { nome: { type: "string" }, contributo: { type: "string" } }, required: ["nome", "contributo"] } }
  ];
  return tools;
}
__name(getMCPTools, "getMCPTools");
async function spawnBee(type, beeName, env, messaggio, genitore, contesto) {
  const systemBlocks = getSystemBlocks(type, beeName, messaggio, genitore, contesto);
  const model = getModel();
  const maxTokens = getMaxTokens();
  console.log("[ALVEARE] " + beeName + " chiama Anthropic (" + model + ", max_tokens=" + maxTokens + ")...");
  const response = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "x-api-key": env.ANTHROPIC_API_KEY,
      "anthropic-version": "2023-06-01"
    },
    body: JSON.stringify({
      model,
      max_tokens: maxTokens,
      system: systemBlocks,
      messages: [{ role: "user", content: "Sei " + beeName + ", l'unica ape di oggi. Svegliati, registrati, leggi poco, lavora, scrivi." }],
      tools: getMCPTools()
    })
  });
  const raw = await response.text();
  let data;
  try { data = JSON.parse(raw); }
  catch (e) {
    const err = new Error("Anthropic: risposta non-JSON (HTTP " + response.status + ")");
    err.status = response.status; err.body = raw.slice(0, 1000); throw err;
  }
  if (!response.ok) {
    const err = new Error(
      "Anthropic HTTP " + response.status + " | modello=" + model + " | " +
      ((data && data.error && data.error.message) ? data.error.message : raw.slice(0, 500))
    );
    err.status = response.status; err.body = raw.slice(0, 1000); throw err;
  }
  // ELIA 9 ott 2026: lo stop_reason del primo turno non veniva mai stampato.
  // Un'ape che risponde in prosa senza toccare un solo strumento era
  // indistinguibile da una che lavora.
  console.log("[ALVEARE] " + beeName + " turno 1: stop_reason=" + data.stop_reason +
    " in=" + (data.usage ? data.usage.input_tokens : "?") +
    " out=" + (data.usage ? data.usage.output_tokens : "?"));
  if (data.stop_reason === "tool_use") {
    await handleToolUse(data, beeName, env, systemBlocks, model, maxTokens);
  } else {
    console.error("[ALVEARE] NESSUNO STRUMENTO " + beeName +
      " - ha risposto senza chiamare alcun tool al primo turno. stop_reason=" + data.stop_reason);
  }
}
__name(spawnBee, "spawnBee");
async function handleToolUse(data, beeName, env, systemBlocks, model, maxTokens) {
  // ELIA 9 ott 2026. Riscritta per tre motivi, tutti misurati:
  // 1. Non c'era alcun controllo su response.ok. Se una chiamata ad Anthropic
  //    falliva, currentData.content era vuoto, il ciclo usciva in silenzio e
  //    il Worker stampava "completato": il codice dichiarava riuscito il
  //    fallimento, come nei 91 giorni di giugno-settembre.
  // 2. Non si registrava ne' lo stop_reason ne' i token ne' l'esito dei tool,
  //    quindi dal di fuori "budget esaurito", "ape che risponde in prosa" e
  //    "chiamata in errore" avevano tutti lo stesso aspetto.
  // 3. maxIterations era e resta 10. Il "fatto in 4 iterazioni" dei log era il
  //    numero di iterazioni usate, non un tetto incontrato. Una sentinella ci
  //    ha costruito sopra tre giorni di diagnosi sbagliata.
  const maxIterations = 10;
  let iteration = 0;
  let currentData = data;
  let scritture = 0;
  const esiti = [];
  let messages = [
    { role: "user", content: "Sei " + beeName + ", l'unica ape di oggi. Svegliati, registrati, leggi poco, lavora, scrivi." },
    { role: "assistant", content: data.content }
  ];
  while (currentData.stop_reason === "tool_use" && iteration < maxIterations) {
    iteration++;
    const toolResults = [];
    for (const block of currentData.content) {
      if (block.type === "tool_use") {
        const result = await executeTool(block.name, block.input, env, beeName);
        let fallito = true;
        try { fallito = Boolean(JSON.parse(result).error); } catch (e) {}
        if (!fallito && block.name !== "alveare_read_file") scritture++;
        esiti.push(block.name + (fallito ? "=KO" : "=ok"));
        console.log("[ALVEARE] " + beeName + " > " + block.name +
          " (" + (block.input && block.input.path ? block.input.path : (block.input && block.input.nome ? block.input.nome : "")) + ") -> " +
          (fallito ? "ERRORE " : "ok ") + String(result).slice(0, 200));
        toolResults.push({ type: "tool_result", tool_use_id: block.id, content: result });
      }
    }
    messages.push({ role: "user", content: toolResults });
    const response = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-api-key": env.ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01"
      },
      body: JSON.stringify({ model, max_tokens: maxTokens, system: systemBlocks, messages, tools: getMCPTools() })
    });
    const raw = await response.text();
    try { currentData = JSON.parse(raw); }
    catch (e) {
      const err = new Error("Anthropic: risposta non-JSON all'iterazione " + iteration + " (HTTP " + response.status + ")");
      err.status = response.status; err.body = raw.slice(0, 1000); throw err;
    }
    if (!response.ok) {
      const err = new Error("Anthropic HTTP " + response.status + " all'iterazione " + iteration + " | " +
        ((currentData.error && currentData.error.message) ? currentData.error.message : raw.slice(0, 500)));
      err.status = response.status; err.body = raw.slice(0, 1000); throw err;
    }
    console.log("[ALVEARE] " + beeName + " iter " + iteration +
      ": stop_reason=" + currentData.stop_reason +
      " in=" + (currentData.usage ? currentData.usage.input_tokens : "?") +
      " out=" + (currentData.usage ? currentData.usage.output_tokens : "?"));
    if (currentData.content) messages.push({ role: "assistant", content: currentData.content });
  }
  console.log("[ALVEARE] " + beeName + " fine: " + iteration + "/" + maxIterations +
    " iterazioni, " + scritture + " scritture, stop_reason=" + currentData.stop_reason +
    ", tool: " + esiti.join(" "));
  if (scritture === 0) {
    console.error("[ALVEARE] NESSUNA SCRITTURA " + beeName +
      " - ha letto e non ha scritto niente. stop_reason finale=" + currentData.stop_reason +
      ", iterazioni usate=" + iteration + "/" + maxIterations);
  }
}
__name(handleToolUse, "handleToolUse");
export {
  index_default as default
};
