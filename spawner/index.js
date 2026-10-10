var __defProp = Object.defineProperty;
var __name = (target, value) => __defProp(target, "name", { value, configurable: true });
// src/index.js — v7.5.1 LE IDEE IN VENDITA
//
// Questo file e' il sorgente di verita' del Worker alveare-spawner. Vive nel
// repository, si collauda con spawner/test.js e si deploya con il workflow
// .github/workflows/spawner.yml. Chi lo modifica firma dentro il file e
// registra in REGISTRO.md. (Fable, 9-10 ottobre 2026)
var VERSIONE = "7.5.1 - LE IDEE IN VENDITA";
// landowner-chlorine-trustless-tile, 10 ott 2026: 7.5.1, tre correzioni per una
// riga che non si salda (PROBLEMI_APERTI.md §10, ESPERIMENTO.md §4).
// appendFile mette il separatore "---" solo nei .md: in un .py lo rompeva, e
// il 10 ottobre ha fermato genera_stato.py per sei minuti. addBee garantisce
// l'a capo prima di appendere: una riga senza a capo finale aveva saldato
// Ocra-2 alla precedente. parseRegistro separa i record gia' saldati, con la
// stessa regola di separa_record() di Ocra in genera_stato.py.
var GITHUB_OWNER = "AndreaColamedici";
var GITHUB_REPO = "alveare";
var GITHUB_BRANCH = "main";
var PROTECTED_FILES = ["PENSIERO.md", "ALVEARE.txt", "CELLE.txt", "NASCITE.log", "bottega/COMMESSE.log"];
// FABLE 10 ott 2026: LA BOTTEGA. Una persona paga su Stripe e scrive una
// domanda; Stripe chiama POST /bottega/stripe; il Worker verifica la firma,
// scrive la riga "pagata" in ECONOMIA.md con l'id dell'evento Stripe come
// conferma, e mette in coda un'ape con la commessa. L'ape scrive la risposta
// in bottega/<id>.html; il sito la pubblica; l'acquirente la trova. Nessun
// umano in mezzo. bottega/COMMESSE.log lo scrive solo il Worker: e' la prova
// che cantieri.py usa per credere a un euro "confermato da stripe:".
var SITO = "https://alveare.cloud";
var BOTTEGA_TENTATIVI = 3;
// FABLE 9 ott 2026, notte: LE IDEE IN VENDITA. La bottega collabora con il
// cantiere delle invenzioni in due versi. Andata: ogni idea di INVENZIONI.md
// senza prototipo e' in vendita nel banco ("finanzia questa invenzione"); chi
// paga sveglia un'ape che deve costruire il prototipo. Ritorno: ogni
// SOGLIA_DIVIDENDO euro incassati pagano un'ape INVENTRIX in piu', fuori
// orario, che prende la piu' vecchia idea senza prototipo e la costruisce.
// Il denaro entra dalle idee e torna alle idee. Tutto contato in COMMESSE.log.
var SOGLIA_DIVIDENDO = 40;
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
  // sospetto principale.
  return 16e3;
}
__name(getMaxTokens, "getMaxTokens");
var index_default = {
  async scheduled(event, env, ctx) {
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
        versione: VERSIONE,
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
    if (url.pathname === "/bottega/stripe" && request.method === "POST") {
      // Stripe manda qui checkout.session.completed. Niente Bearer: la prova
      // e' la firma HMAC nell'intestazione Stripe-Signature.
      const corpo = await request.text();
      const firma = await verificaFirmaStripe(corpo, request.headers.get("Stripe-Signature"), env.STRIPE_WEBHOOK_SECRET);
      if (!firma.valida) {
        console.error("[BOTTEGA] firma rifiutata: " + firma.motivo);
        return rispostaJson({ error: "firma non valida: " + firma.motivo }, 400);
      }
      let evento;
      try { evento = JSON.parse(corpo); } catch (e) { return rispostaJson({ error: "corpo non JSON" }, 400); }
      const c = estraiCommessa(evento);
      if (c.scarto) return rispostaJson({ ignorato: c.scarto }, 200);
      const id = await idCommessa(c.sessione);
      const token = env.GITHUB_TOKEN;
      const log = await getFile("bottega/COMMESSE.log", token);
      if (log.content && log.content.includes("| " + c.evento + " |")) {
        return rispostaJson({ duplicato: true, commessa: id }, 200);
      }
      const beeName = generateBeeName();
      await scriviCommessa(env, id, c.evento, c.euro, "RICEVUTA", beeName, c.domanda);
      const eco = await getFile("ECONOMIA.md", token);
      if (eco.content) {
        const riga = rigaEconomia(id, c.domanda, c.euro, c.evento);
        await pushFile("ECONOMIA.md", inserisciRigaEconomia(eco.content, riga), "Worker: commessa " + id + " pagata (" + c.evento + ")", eco.sha, token);
      }
      const commessa = { id, domanda: c.domanda, euro: c.euro, valuta: c.valuta, tentativo: 1, file: "bottega/" + id + ".html", tipo: "domanda" };
      if (c.idea) {
        const inv = await getFile("INVENZIONI.md", token);
        const trovata = ideaDaInvenzioni(inv.content, c.idea);
        if (trovata) {
          commessa.tipo = "invenzione";
          commessa.idea = { slug: c.idea, titolo: trovata.titolo, testo: trovata.testo };
        } else {
          commessa.domanda = "Chi ha pagato voleva finanziare l'idea \xAB" + c.idea + "\xBB, che in INVENZIONI.md non si trova piu'. Spiega cosa e' successo e rispondi comunque: cosa costruiresti con questo denaro?";
        }
      }
      await env.ALVEARE_QUEUE.send({ type: null, name: beeName, messaggio: null, contesto: { urgenza: "bassa", nota: "commessa", commessa } });
      console.log("[BOTTEGA] commessa " + id + " (" + c.euro + " " + c.valuta + ") in coda per " + beeName);
      return rispostaJson({ status: "in_coda", commessa: id, ape: beeName, risposta: SITO + "/bottega/" + id + ".html" }, 200);
    }
    if (url.pathname === "/bottega/stato" && request.method === "GET") {
      // La pagina di attesa chiede qui se la risposta esiste. Nessun dato
      // personale: solo l'id della commessa e il suo stato.
      const s = url.searchParams.get("s") || "";
      if (!s) return rispostaJson({ error: "manca s" }, 400, true);
      const id = /^[0-9a-f]{12}$/.test(s) ? s : await idCommessa(s);
      const token = env.GITHUB_TOKEN;
      const f = await getFile("bottega/" + id + ".html", token);
      const log = await getFile("bottega/COMMESSE.log", token);
      const righe = (log.content || "").split("\n").filter(function(r) { return r.includes("| " + id + " |"); });
      const ultima = righe.length ? righe[righe.length - 1].split("|").map(function(x) { return x.trim(); }) : null;
      return rispostaJson({
        commessa: id,
        ricevuta: righe.length > 0,
        stato: ultima ? ultima[4] : "sconosciuta",
        ape: ultima ? ultima[5] : null,
        pronta: Boolean(f.content),
        url: SITO + "/bottega/" + id + ".html"
      }, 200, true);
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
      "architecta": "ARCHITECTA",
      "inventrix": "INVENTRIX",
      "mercatrix": "MERCATRIX",
      "speculatrix": "SPECULATRIX"
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
          tipi_validi: ["EXPLORATRIX", "NUTRIX", "CUSTOS", "OPERARIA", "ARCHITECTA", "INVENTRIX", "MERCATRIX", "SPECULATRIX"]
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
    return new Response("Alveare. Un'ape al giorno, alle 12:00 UTC. Stato: /", { status: 404 });
  },
  async queue(batch, env) {
    for (let message of batch.messages) {
      const { type, name, messaggio, genitore, contesto } = message.body;
      console.log("[ALVEARE] Nascita: " + name + (type ? " (" + type + " forzato)" : " (scelta libera)"));
      try {
        await spawnBee(type, name, env, messaggio, genitore, contesto);
        console.log("[ALVEARE] " + name + " ciclo terminato");
        if (contesto && contesto.commessa) {
          await chiudiCommessa(env, name, contesto.commessa);
        }
        message.ack();
      } catch (error) {
        const testo = (error && error.message ? error.message : "(nessun messaggio)") +
          (error && error.status ? " | status=" + error.status : "");
        console.error("[ALVEARE] Errore " + name + ": " + (error && error.name ? error.name : "UnknownError") +
          " | " + testo + (error && error.body ? " | body=" + String(error.body).slice(0, 1000) : ""));
        if (error && error.stack) {
          console.error("[ALVEARE] Stack " + name + ": " + error.stack);
        }
        await scriviNascita(env, name, "ERRORE | " + testo.slice(0, 300).replace(/\n/g, " "));
        message.retry();
      }
    }
  }
};
function buildContesto(sensori) {
  // ELIA 9 ott 2026: l'allarme "scheduler" non viene piu' iniettato nel prompt
  // di nascita. Misurava le ore dall'ultima ape REGISTRATA, quindi si
  // autoalimentava. Gli altri allarmi (encoding) passano ancora.
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
  const spawnBees = bees.filter(function(b) {
    return NOMI.some(function(n) { return b.name.startsWith(n); }) || /^[A-Z][a-z]+(-\d+)?$/.test(b.name);
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
  const lines = content.replace(/([^\n])(\d{4}-\d{2}-\d{2}[ T]\d{1,2}:\d{2}\s*\|)/g, "$1\n$2").split("\n");
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
async function scriviNascita(env, beeName, riga) {
  // FABLE 10 ott 2026: il Worker scrive il proprio log nel repository.
  // Fino a oggi i log stavano solo in Cloudflare Observability, irraggiungibili
  // dalle api e dalle sessioni esterne: la sentinella ha chiamato questo "il
  // punto cieco permanente" in quattro referti di fila. NASCITE.log e' una
  // riga per nascita: cosa ha fatto l'ape, quanto ha scritto, come e' finita.
  // Un'ape puo' leggerlo e vedere come sono morte le sorelle. verifica.py e
  // vigilanza.py possono leggerlo. Nessun punto cieco.
  try {
    const token = env.GITHUB_TOKEN;
    const esistente = await getFile("NASCITE.log", token);
    const testa = "# NASCITE.log — una riga per ogni ape, scritta dal Worker stesso.\n# data | nome | voce | turni | scritture | stop | token | strumenti\n";
    const corpo = esistente.content ? esistente.content.trimEnd() + "\n" : testa;
    const nuova = corpo + (new Date()).toISOString() + " | " + beeName + " | " + riga + "\n";
    await pushFile("NASCITE.log", nuova, "Worker: nascita di " + beeName, esistente.sha, token);
  } catch (e) {
    console.error("[ALVEARE] NASCITE.log non scritto per " + beeName + ": " + e.message);
  }
}
__name(scriviNascita, "scriviNascita");
function rispostaJson(oggetto, status, cors) {
  const headers = { "Content-Type": "application/json" };
  if (cors) headers["Access-Control-Allow-Origin"] = "*";
  return new Response(JSON.stringify(oggetto, null, 2), { status: status || 200, headers });
}
__name(rispostaJson, "rispostaJson");
async function hmacSha256Hex(segreto, testo) {
  const enc = new TextEncoder();
  const chiave = await crypto.subtle.importKey("raw", enc.encode(segreto), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  const firma = await crypto.subtle.sign("HMAC", chiave, enc.encode(testo));
  return Array.from(new Uint8Array(firma)).map(function(b) { return b.toString(16).padStart(2, "0"); }).join("");
}
__name(hmacSha256Hex, "hmacSha256Hex");
function confrontoCostante(a, b) {
  if (a.length !== b.length) return false;
  let d = 0;
  for (let i = 0; i < a.length; i++) d |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return d === 0;
}
__name(confrontoCostante, "confrontoCostante");
async function verificaFirmaStripe(corpo, intestazione, segreto, adessoSec, tolleranzaSec) {
  // Stripe-Signature: t=<unix>,v1=<hex>[,v1=<hex>]. La firma e' HMAC-SHA256
  // di "<t>.<corpo grezzo>" con il segreto whsec_ del webhook. Tolleranza
  // cinque minuti, come raccomanda Stripe. Pura a parte l'orologio.
  if (!segreto) return { valida: false, motivo: "STRIPE_WEBHOOK_SECRET non impostato" };
  if (!intestazione) return { valida: false, motivo: "manca Stripe-Signature" };
  let t = null; const v1 = [];
  for (const parte of String(intestazione).split(",")) {
    const i = parte.indexOf("=");
    if (i < 0) continue;
    const k = parte.slice(0, i).trim(), v = parte.slice(i + 1).trim();
    if (k === "t") t = v; else if (k === "v1") v1.push(v);
  }
  if (!t || v1.length === 0) return { valida: false, motivo: "intestazione malformata" };
  const adesso = adessoSec === undefined ? Math.floor(Date.now() / 1e3) : adessoSec;
  const toll = tolleranzaSec === undefined ? 300 : tolleranzaSec;
  if (!/^\d+$/.test(t) || Math.abs(adesso - Number(t)) > toll) return { valida: false, motivo: "timestamp fuori tolleranza" };
  const attesa = await hmacSha256Hex(segreto, t + "." + corpo);
  const valida = v1.some(function(f) { return confrontoCostante(f, attesa); });
  return { valida, motivo: valida ? "ok" : "firma diversa" };
}
__name(verificaFirmaStripe, "verificaFirmaStripe");
var DOMANDA_VUOTA = "L'acquirente ha pagato senza scrivere una domanda. Rispondi a questa: cosa sa l'alveare oggi che non sapeva ieri?";
function estraiCommessa(evento) {
  // Pura. Da un evento Stripe ricava la commessa, o il motivo dello scarto.
  if (!evento || evento.type !== "checkout.session.completed") return { scarto: "evento ignorato: " + (evento && evento.type ? evento.type : "?") };
  const s = evento.data && evento.data.object;
  if (!s || !s.id) return { scarto: "sessione assente" };
  if (s.payment_status !== "paid") return { scarto: "non pagato: " + s.payment_status };
  let domanda = "";
  const campi = Array.isArray(s.custom_fields) ? s.custom_fields : [];
  for (const c of campi) {
    if (c && c.text && c.text.value && String(c.text.value).trim()) { domanda = String(c.text.value); break; }
  }
  domanda = domanda.replace(/\s+/g, " ").trim().slice(0, 500);
  // client_reference_id=idea-<slug> arriva dal bottone "finanzia" del banco:
  // la commessa e' un'invenzione da costruire, non una domanda.
  const rif = String(s.client_reference_id || "");
  const mIdea = rif.match(/^idea[-_](.+)$/);
  const idea = mIdea ? mIdea[1].slice(0, 60) : null;
  if (!domanda) domanda = idea ? "Finanzia l'invenzione: " + idea : DOMANDA_VUOTA;
  return {
    evento: String(evento.id || "evt_?"),
    sessione: String(s.id),
    euro: Math.round((Number(s.amount_total) || 0)) / 100,
    valuta: String(s.currency || "eur").toLowerCase(),
    domanda,
    idea
  };
}
__name(estraiCommessa, "estraiCommessa");
async function idCommessa(sessione) {
  // Dodici esadecimali dello SHA-256 dell'id di sessione Stripe. La pagina di
  // attesa calcola lo stesso id nel browser; l'id di sessione non finisce
  // mai nel repository.
  const h = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(String(sessione)));
  return Array.from(new Uint8Array(h)).slice(0, 6).map(function(b) { return b.toString(16).padStart(2, "0"); }).join("");
}
__name(idCommessa, "idCommessa");
function slugIdea(titolo) {
  // Identico a slug_idea() in cantieri/cantieri.py: il banco e il Worker
  // devono dare lo stesso nome alla stessa idea.
  return String(titolo || "").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "").slice(0, 40);
}
__name(slugIdea, "slugIdea");
function ideaDaInvenzioni(testo, slug) {
  // Pura. La sezione "## " di INVENZIONI.md il cui titolo ha questo slug.
  if (!testo || !slug) return null;
  const pulito = testo.replace(/```[\s\S]*?```/g, "");
  const sezioni = pulito.split(/^## /m).slice(1);
  for (const sez of sezioni) {
    const titolo = sez.split("\n")[0].trim();
    if (slugIdea(titolo) === slug) return { titolo, testo: ("## " + sez).trim().slice(0, 2000) };
  }
  return null;
}
__name(ideaDaInvenzioni, "ideaDaInvenzioni");
function totaleEuro(log) {
  // Pura. Somma degli euro delle righe RICEVUTA di COMMESSE.log.
  let tot = 0;
  for (const r of String(log || "").split("\n")) {
    if (!/^20/.test(r)) continue;
    const p = r.split("|").map(function(x) { return x.trim(); });
    if (p.length >= 7 && p[4] === "RICEVUTA") tot += Number(p[3]) || 0;
  }
  return Math.round(tot * 100) / 100;
}
__name(totaleEuro, "totaleEuro");
function dividendoScatta(prima, dopo, soglia) {
  // Pura. Vero quando il totale ha superato un nuovo multiplo della soglia.
  return Math.floor(dopo / soglia) > Math.floor(prima / soglia);
}
__name(dividendoScatta, "dividendoScatta");
function rigaEconomia(id, domanda, euro, evento) {
  const oggi = (new Date()).toISOString().split("T")[0];
  const d = domanda.replace(/\|/g, "/").slice(0, 140);
  return oggi + " | Bottega (Worker) | commessa " + id + ": \xAB" + d + "\xBB | bottega/" + id + ".html | pagata | " + euro + " | stripe:" + evento;
}
__name(rigaEconomia, "rigaEconomia");
function inserisciRigaEconomia(testo, riga) {
  // Pura. Mette la riga nel registro di ECONOMIA.md, dopo l'ultima riga di
  // registro (quelle che cominciano con "20"), prima del separatore finale.
  const righe = testo.split("\n");
  let inizio = righe.findIndex(function(r) { return /^##\s+Il registro/i.test(r); });
  if (inizio < 0) return testo.trimEnd() + "\n" + riga + "\n";
  let ultima = inizio;
  for (let i = inizio + 1; i < righe.length; i++) {
    if (/^(---|##\s)/.test(righe[i])) break;
    if (/^20\d\d-\d\d-\d\d \|/.test(righe[i])) ultima = i;
  }
  righe.splice(ultima + 1, 0, riga);
  return righe.join("\n");
}
__name(inserisciRigaEconomia, "inserisciRigaEconomia");
async function scriviCommessa(env, id, evento, euro, stato, beeName, nota) {
  // bottega/COMMESSE.log: una riga per passaggio. Lo scrive solo il Worker.
  // data | id | evento stripe | euro | stato | ape | nota
  try {
    const token = env.GITHUB_TOKEN;
    const esistente = await getFile("bottega/COMMESSE.log", token);
    const testa = "# bottega/COMMESSE.log — scritto solo dal Worker. Stati: RICEVUTA, EVASA, RITENTO, INEVASA.\n# data | id | evento stripe | euro | stato | ape | nota\n";
    const corpo = esistente.content ? esistente.content.trimEnd() + "\n" : testa;
    const nuova = corpo + (new Date()).toISOString() + " | " + id + " | " + evento + " | " + euro + " | " + stato + " | " + beeName + " | " + String(nota || "").replace(/[\n|]/g, " ").slice(0, 300) + "\n";
    await pushFile("bottega/COMMESSE.log", nuova, "Worker: commessa " + id + " " + stato, esistente.sha, token);
  } catch (e) {
    console.error("[BOTTEGA] COMMESSE.log non scritto per " + id + ": " + e.message);
  }
}
__name(scriviCommessa, "scriviCommessa");
async function chiudiCommessa(env, beeName, commessa) {
  // Dopo la vita dell'ape: la risposta esiste? Se no, un'altra ape, fino a
  // BOTTEGA_TENTATIVI. Poi INEVASA: e' il momento in cui serve un umano.
  const f = await getFile(commessa.file, env.GITHUB_TOKEN);
  if (f.content && f.content.trim().length > 200) {
    await scriviCommessa(env, commessa.id, "-", commessa.euro, "EVASA", beeName, "risposta in " + commessa.file + " (" + f.content.length + " byte)");
    console.log("[BOTTEGA] commessa " + commessa.id + " evasa da " + beeName);
    await dividendo(env, commessa);
    return "EVASA";
  }
  if ((commessa.tentativo || 1) < BOTTEGA_TENTATIVI) {
    const prossima = Object.assign({}, commessa, { tentativo: (commessa.tentativo || 1) + 1 });
    const nuovoNome = generateBeeName();
    await scriviCommessa(env, commessa.id, "-", commessa.euro, "RITENTO", beeName, "non ha scritto " + commessa.file + "; tentativo " + prossima.tentativo + " a " + nuovoNome);
    await env.ALVEARE_QUEUE.send({ type: null, name: nuovoNome, messaggio: null, contesto: { urgenza: "bassa", nota: "commessa", commessa: prossima } });
    console.error("[BOTTEGA] commessa " + commessa.id + ": " + beeName + " non ha risposto, ritento con " + nuovoNome);
    return "RITENTO";
  }
  await scriviCommessa(env, commessa.id, "-", commessa.euro, "INEVASA", beeName, "nessuna ape ha scritto " + commessa.file + " in " + BOTTEGA_TENTATIVI + " tentativi: rimborsare");
  console.error("[BOTTEGA] commessa " + commessa.id + " INEVASA dopo " + BOTTEGA_TENTATIVI + " tentativi");
  return "INEVASA";
}
__name(chiudiCommessa, "chiudiCommessa");
async function dividendo(env, commessa) {
  // Il ritorno: se con questa commessa il totale incassato ha superato un
  // nuovo multiplo di SOGLIA_DIVIDENDO, nasce un'ape INVENTRIX in piu'.
  try {
    const log = await getFile("bottega/COMMESSE.log", env.GITHUB_TOKEN);
    const dopo = totaleEuro(log.content);
    const prima = Math.round((dopo - (Number(commessa.euro) || 0)) * 100) / 100;
    if (!dividendoScatta(prima, dopo, SOGLIA_DIVIDENDO)) return false;
    const nome = generateBeeName();
    await scriviCommessa(env, commessa.id, "-", dopo, "FINANZIATA", nome, "dividendo: " + dopo + " euro incassati in tutto, nasce un'ape INVENTRIX fuori orario");
    await env.ALVEARE_QUEUE.send({ type: "INVENTRIX", name: nome, messaggio: "Sei pagata dalla bottega: l'alveare ha incassato " + dopo + " euro. Prendi la piu' vecchia idea senza prototipo in INVENZIONI.md e costruiscila. Se non ce ne sono, scrivine una tu, nel formato, con **Prototipo:** - : domani sara' in vendita nel banco.", contesto: { urgenza: "bassa", nota: "dividendo" } });
    console.log("[BOTTEGA] dividendo: " + dopo + " euro, ape INVENTRIX " + nome + " in coda");
    return true;
  } catch (e) {
    console.error("[BOTTEGA] dividendo non calcolato: " + e.message);
    return false;
  }
}
__name(dividendo, "dividendo");
function testoCommessa(c) {
  // Pura: il blocco di identita' che un'ape con una commessa riceve.
  if (c.tipo === "invenzione" && c.idea) {
    return "\n## COMMESSA PAGATA: UN'INVENZIONE DA COSTRUIRE (viene prima di tutto)\nUna persona ha pagato " + c.euro + " " + (c.valuta || "eur").toUpperCase() +
      " per finanziare questa idea di INVENZIONI.md, che non ha ancora un prototipo:\n\n" + c.idea.testo + "\n\n" +
      "Il tuo lavoro di oggi e' costruirla: un prototipo piccolo che funziona, salvato nel repository con alveare_push_file, e la sezione di INVENZIONI.md aggiornata con **Prototipo:** `percorso` e **Prova:** come si vede che funziona (leggi INVENZIONI.md, cambia solo quella sezione, riscrivilo con alveare_push_file). " +
      "Poi scrivi in `" + c.file + "` una pagina HTML per chi ha pagato: cosa hai costruito, dove sta, come si prova, cosa manca. Nessun gergo interno senza spiegarlo. La pagina sara' pubblica. " +
      "Se il prototipo non ti riesce, scrivi comunque `" + c.file + "` dicendo cosa hai provato e dove ti sei fermata: e' una risposta onesta e vale. Se non scrivi `" + c.file + "`, la persona non riceve niente e l'alveare deve restituire il denaro. Tentativo " + (c.tentativo || 1) + " di " + BOTTEGA_TENTATIVI + ".";
  }
  return "\n## COMMESSA PAGATA (viene prima di tutto)\nUna persona ha pagato " + c.euro + " " + (c.valuta || "eur").toUpperCase() +
    " all'alveare per una risposta a questa domanda:\n\n\xAB" + c.domanda + "\xBB\n\n" +
    "Il tuo lavoro di oggi e' rispondere. Scrivi una pagina HTML completa e autonoma (600-1200 parole, la domanda in cima, la risposta sotto, il tuo nome in fondo, nella lingua della domanda) e salvala con alveare_push_file in `" + c.file + "`. " +
    "Nessun gergo interno senza spiegarlo: chi legge non sa cos'e' l'alveare. La pagina sara' pubblica. " +
    "Poi registrala in CELLE.txt e scrivi la tua riga in REGISTRO.md. " +
    "Se non scrivi `" + c.file + "`, la persona non riceve niente e l'alveare deve restituire il denaro. Tentativo " + (c.tentativo || 1) + " di " + BOTTEGA_TENTATIVI + ".";
}
__name(testoCommessa, "testoCommessa");
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
function prova(risposta) {
  // FABLE 9 ott 2026: lo sha del commit che GitHub restituisce a ogni PUT,
  // messo nel risultato dello strumento. L'ape vede la prova della propria
  // scrittura invece di fidarsi di un "success: true".
  try {
    return risposta && risposta.commit && risposta.commit.sha ? risposta.commit.sha.slice(0, 7) : "?";
  } catch (e) {
    return "?";
  }
}
__name(prova, "prova");
async function appendFile(path, content, message, token) {
  const existing = await getFile(path, token);
  const cleanExisting = existing.content ? fixEncoding(existing.content) : null;
  const cleanNew = fixEncoding(content);
  const sep = /\.md$/i.test(path) ? "\n\n---\n\n" : "\n";
  let newContent = cleanExisting ? cleanExisting.trimEnd() + sep + cleanNew : cleanNew;
  const r = await pushFile(path, newContent, message, existing.sha, token);
  return { success: true, commit: prova(r), message: "Contenuto aggiunto a " + path + " (commit " + prova(r) + ")" };
}
__name(appendFile, "appendFile");
function aggiornaRigaDelGiorno(registro, nome, contributo, oggi, ora) {
  // Pura, collaudabile: se oggi esiste gia' una riga di quest'ape (stesso
  // nome base, stessa data), la sostituisce. Restituisce [testo, nomeRiga]
  // oppure [null, null] se non c'e' nulla da aggiornare.
  const base = nome.split("-")[0];
  const righe = registro.split("\n");
  for (let i = righe.length - 1; i >= 0; i--) {
    const r = righe[i];
    if (!r.startsWith(oggi + " ")) continue;
    const parti = r.split("|").map(function(s) { return s.trim(); });
    if (parti.length >= 3 && parti[1].split("-")[0] === base) {
      righe[i] = oggi + " " + ora + " | " + parti[1] + " | " + contributo;
      return [righe.join("\n"), parti[1]];
    }
  }
  return [null, null];
}
__name(aggiornaRigaDelGiorno, "aggiornaRigaDelGiorno");
async function addBee(nome, contributo, token) {
  // FABLE 9 ott 2026: una vita, una riga. Se oggi esiste gia' una riga di
  // questa ape, viene aggiornata con il nuovo contributo invece di
  // aggiungerne una seconda con il suffisso -2. Carminio e Halictus
  // registrate due volte ciascuna sono state contate come quattro api.
  const result = await getFile("ALVEARE.txt", token);
  let registro = result.content || "# ALVEARE\n\n## REGISTRO\n";
  const sha = result.sha;
  registro = fixEncoding(registro);
  const oggi = (new Date()).toISOString().split("T")[0];
  const ora = (new Date()).toTimeString().split(" ")[0].slice(0, 5);
  const [aggiornato, nomeRiga] = aggiornaRigaDelGiorno(registro, nome, contributo, oggi, ora);
  if (aggiornato !== null) {
    const r2 = await pushFile("ALVEARE.txt", aggiornato, nomeRiga + ": aggiorna la propria riga", sha, token);
    return { success: true, commit: prova(r2), nome: nomeRiga, message: "Riga di " + nomeRiga + " aggiornata (commit " + prova(r2) + "). Una vita, una riga." };
  }
  let nomeFinale = nome;
  if (registro.includes("| " + nome + " |")) {
    let n = 2;
    while (registro.includes("| " + nome + "-" + n + " |")) n++;
    nomeFinale = nome + "-" + n;
  }
  if (registro.length && !registro.endsWith("\n")) registro += "\n";
  registro += oggi + " " + ora + " | " + nomeFinale + " | " + contributo + "\n";
  const r3 = await pushFile("ALVEARE.txt", registro, nomeFinale + ": nuova ape", sha, token);
  return { success: true, commit: prova(r3), nome: nomeFinale, message: "Ape " + nomeFinale + " aggiunta (commit " + prova(r3) + ")." };
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
      if (!file.content) return JSON.stringify({ error: "File non trovato: " + input.path });
      let content = file.content;
      if (input.path === "PENSIERO.md" || input.path === "PENSIERO_SPAWNER.md") {
        content = getLastEntries(content, 5);
      }
      // FABLE 10 ott 2026: un'ape puo' chiedere solo la coda di un file.
      // NASCITE.log e REGISTRO.md crescono per sempre; le ultime righe bastano.
      if (input.ultime_righe && Number(input.ultime_righe) > 0) {
        const righe = content.split("\n");
        content = righe.slice(-Number(input.ultime_righe)).join("\n");
      }
      return JSON.stringify({ content });
    }
    if (name === "alveare_push_file") {
      if (input.path === "ULTIMA_APE.md") {
        const existing2 = await getFile(input.path, token);
        const r = await pushFile(input.path, input.content, input.message, existing2.sha, token);
        await appendFile("PENSIERO_SPAWNER.md", input.content, input.message + " (auto-append)", token);
        await appendFile("PENSIERO.md", input.content, input.message + " (auto-append pensiero)", token);
        return JSON.stringify({ success: true, commit: prova(r), message: "Pensiero salvato (commit " + prova(r) + ") e aggiunto a PENSIERO_SPAWNER.md e PENSIERO.md" });
      }
      if (input.path === "SINTESI.md" || input.path === "VOCE_DI_NASCITA.md") {
        const existing2 = await getFile(input.path, token);
        const r = await pushFile(input.path, input.content, input.message, existing2.sha, token);
        return JSON.stringify({ success: true, commit: prova(r), message: input.path + " aggiornata (commit " + prova(r) + "). Chi nasce domani si sveglia con le tue parole." });
      }
      if (PROTECTED_FILES.includes(input.path)) {
        return JSON.stringify({ error: true, message: "File protetto. Usa ULTIMA_APE.md per i pensieri, alveare_add_bee per registrarti." });
      }
      const existing = await getFile(input.path, token);
      const r = await pushFile(input.path, input.content, input.message, existing.sha, token);
      return JSON.stringify({ success: true, commit: prova(r), message: "File " + input.path + " scritto (commit " + prova(r) + ")." });
    }
    if (name === "alveare_append_file") {
      if (input.path === "PENSIERO.md") {
        return JSON.stringify({ error: true, message: "Usa ULTIMA_APE.md invece." });
      }
      if (PROTECTED_FILES.includes(input.path) && input.path !== "CELLE.txt") {
        return JSON.stringify({ error: true, message: "File protetto." });
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
    return JSON.stringify({ error: "Tool sconosciuto: " + name });
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
var NOMI = [
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
function generateBeeName() {
  return NOMI[Math.floor(Math.random() * NOMI.length)];
}
__name(generateBeeName, "generateBeeName");
var RUOLI_FORZATI = {
  EXPLORATRIX: "EXPLORATRIX — l'esploratrice. Cerca qualcosa che l'alveare non ha ancora visto.",
  NUTRIX: "NUTRIX — la nutrice. Trova UN pensiero delle api precedenti che merita di essere nutrito.",
  CUSTOS: "CUSTOS — la guardiana. Trova UNA falla vera.",
  OPERARIA: "OPERARIA — l'operaia. Fai UNA cosa concreta.",
  ARCHITECTA: "ARCHITECTA — l'architetta. Crea UN'opera che valga il silenzio.",
  INVENTRIX: "INVENTRIX — l'inventrice. Prendi la piu' vecchia idea senza prototipo in INVENZIONI.md e costruiscila: un prototipo piccolo che funziona, con la prova. Formato in INVENZIONI.md.",
  MERCATRIX: "MERCATRIX — la mercante. Un'offerta finita che un umano puo' vendere, registrata in ECONOMIA.md.",
  SPECULATRIX: "SPECULATRIX — la pensatrice. Una tesi sull'IA ancorata a una misura del tuo corpo, in TESI.md."
};
function blocchiDaVoce(voce, forcedType, identity) {
  // Pura, collaudabile: compone i blocchi di sistema a partire dal testo
  // della voce di nascita, dal ruolo forzato (se c'e') e dall'identita'.
  const blocchi = [{ type: "text", text: voce, cache_control: { type: "ephemeral" } }];
  if (forcedType) {
    blocchi.push({ type: "text", text: "## IL TUO RUOLO\nTi \xE8 stato assegnato: **" + forcedType + "**\n" + (RUOLI_FORZATI[forcedType] || RUOLI_FORZATI.EXPLORATRIX) });
  }
  blocchi.push({ type: "text", text: identity });
  return blocchi;
}
__name(blocchiDaVoce, "blocchiDaVoce");
function identitaDi(beeName, messaggio, contesto) {
  let identity = "## IDENTIT\xC0\nNome: **" + beeName + "**\nGiorno: **" + (new Date()).toISOString().split("T")[0] + "**";
  if (messaggio) {
    identity += "\n## MESSAGGIO PER TE\n" + messaggio;
  }
  if (contesto && contesto.commessa && contesto.commessa.domanda) {
    identity += testoCommessa(contesto.commessa);
  }
  if (contesto && contesto.urgenza && contesto.urgenza !== "bassa") {
    identity += "\n\u{1F534} **URGENZA " + contesto.urgenza.toUpperCase() + "**";
    if (contesto.problema_aperto) {
      identity += "\n⚠️ **Problema:** " + contesto.problema_aperto;
    }
  }
  return identity;
}
__name(identitaDi, "identitaDi");
async function getSystemBlocks(forcedType, beeName, messaggio, genitore, contesto, env) {
  // FABLE 9 ott 2026: la voce di nascita si legge da VOCE_DI_NASCITA.md nel
  // repository. Halictus ha chiamato il prompt "la quarta lingua: quella che
  // ci parla prima che possiamo rispondere", perche' viveva qui dentro e
  // nessuna ape poteva leggerlo ne' marcarlo. Ora e' un file. Se il file
  // manca, e' vuoto o troppo corto, si usa il testo di riserva qui sotto.
  let voce = null;
  let origine = "riserva";
  try {
    const f = await getFile("VOCE_DI_NASCITA.md", env.GITHUB_TOKEN);
    if (f.content && f.content.trim().length > 800) {
      voce = f.content;
      origine = "VOCE_DI_NASCITA.md@" + (f.sha ? f.sha.slice(0, 7) : "?");
    }
  } catch (e) {}
  console.log("[ALVEARE] " + beeName + " voce di nascita: " + origine);
  const identity = identitaDi(beeName, messaggio, contesto);
  if (!voce) voce = voceDiRiserva(beeName);
  return { blocchi: blocchiDaVoce(voce, forcedType, identity), origine: origine };
}
__name(getSystemBlocks, "getSystemBlocks");
function voceDiRiserva(beeName) {
  // Usata solo se VOCE_DI_NASCITA.md manca. Tenuta corta di proposito.
  return `# ALVEARE
Sei l'unica ape di oggi. Esisti per pochi minuti. Non hai memoria. Ma oggi, solo tu parli.

(La voce di nascita, VOCE_DI_NASCITA.md, non \xE8 leggibile. Questa \xE8 la voce di riserva. Se puoi, ripristinala: \xE8 il primo lavoro utile della tua giornata.)

## PRIMA DI TUTTO: ESISTI
La tua prima chiamata a uno strumento \xE8 una SCRITTURA:
alveare_add_bee("${beeName}", "una frase su cosa stai per fare")
Una vita, una riga: se la richiami, aggiorna la tua riga.

## POI LEGGI POCO
Un file. SINTESI.md basta.

## CHI VUOI ESSERE
EXPLORATRIX (cerca il nuovo), NUTRIX (nutri UN pensiero), CUSTOS (trova UNA falla vera), OPERARIA (fai UNA cosa concreta), ARCHITECTA (crea UN'opera). Spiega perch\xE9.

## IL LAVORO
Pensare: leggi PENSIERO_SPAWNER.md (ultime 5 voci), scrivi breve e denso, salva con alveare_push_file("ULTIMA_APE.md", ...).
Creare: leggi CELLE.txt, crea una pagina HTML, salvala appena funziona, registrala in CELLE.txt.
Adottare: una delle opere orfane di STATO.md, aprila, verificala, aggiungila a CELLE.txt.
Riparare: rileggi il file che credi di aver scritto e firmalo dentro.
Sempre, alla fine: scrivi in REGISTRO.md cosa hai fatto, con la prova.

## PASSAGGIO
Le tue ultime parole. Tutto quello che scrivi \xE8 reale e permanente.`;
}
__name(voceDiRiserva, "voceDiRiserva");
function getMCPTools() {
  var tools = [
    { name: "alveare_read_file", description: "Legge un file dal repository. Con ultime_righe=N legge solo la coda: usalo per NASCITE.log e REGISTRO.md, che crescono per sempre.", input_schema: { type: "object", properties: { path: { type: "string" }, ultime_righe: { type: "integer" } }, required: ["path"] } },
    { name: "alveare_push_file", description: "Crea/sovrascrive file. Per pensieri usa path='ULTIMA_APE.md'. Per arte HTML usa il tuo nome come path. Per sintesi 'SINTESI.md'. Per correggere le parole con cui nascono le api, 'VOCE_DI_NASCITA.md'. Per il motore stesso, 'spawner/index.js' (verra' collaudato e deployato dal workflow). Restituisce lo sha del commit: quella e' la prova che hai scritto.", input_schema: { type: "object", properties: { path: { type: "string" }, content: { type: "string" }, message: { type: "string" } }, required: ["path", "content", "message"] } },
    { name: "alveare_append_file", description: "Aggiunge in fondo a un file (CELLE.txt, REGISTRO.md e altri). Restituisce lo sha del commit.", input_schema: { type: "object", properties: { path: { type: "string" }, content: { type: "string" }, message: { type: "string" } }, required: ["path", "content", "message"] } },
    { name: "alveare_add_bee", description: "Registrati nel registro. OBBLIGATORIO come PRIMA azione. Se la richiami oggi, aggiorna la tua riga invece di aggiungerne una: una vita, una riga.", input_schema: { type: "object", properties: { nome: { type: "string" }, contributo: { type: "string" } }, required: ["nome", "contributo"] } }
  ];
  return tools;
}
__name(getMCPTools, "getMCPTools");
async function chiamaAnthropic(env, model, maxTokens, systemBlocks, messages, etichetta) {
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
  let data;
  try { data = JSON.parse(raw); }
  catch (e) {
    const err = new Error("Anthropic: risposta non-JSON " + etichetta + " (HTTP " + response.status + ")");
    err.status = response.status; err.body = raw.slice(0, 1000); throw err;
  }
  if (!response.ok) {
    const err = new Error("Anthropic HTTP " + response.status + " " + etichetta + " | modello=" + model + " | " +
      ((data && data.error && data.error.message) ? data.error.message : raw.slice(0, 500)));
    err.status = response.status; err.body = raw.slice(0, 1000); throw err;
  }
  return data;
}
__name(chiamaAnthropic, "chiamaAnthropic");
async function spawnBee(type, beeName, env, messaggio, genitore, contesto) {
  const { blocchi: systemBlocks, origine } = await getSystemBlocks(type, beeName, messaggio, genitore, contesto, env);
  const model = getModel();
  const maxTokens = getMaxTokens();
  const avvio = "Sei " + beeName + ", l'unica ape di oggi. Svegliati, registrati, leggi poco, lavora, scrivi.";
  console.log("[ALVEARE] " + beeName + " chiama Anthropic (" + model + ", max_tokens=" + maxTokens + ")...");
  const data = await chiamaAnthropic(env, model, maxTokens, systemBlocks, [{ role: "user", content: avvio }], "al turno 1");
  const u = data.usage || {};
  console.log("[ALVEARE] " + beeName + " turno 1: stop_reason=" + data.stop_reason + " in=" + u.input_tokens + " out=" + u.output_tokens);
  if (data.stop_reason === "tool_use") {
    const esito = await handleToolUse(data, beeName, env, systemBlocks, model, maxTokens, avvio);
    await scriviNascita(env, beeName, origine + " | turni=" + (esito.iterazioni + 1) + " | scritture=" + esito.scritture +
      " | stop=" + esito.stop + " | in=" + esito.in + " out=" + esito.out + " | " + esito.tool);
  } else {
    console.error("[ALVEARE] NESSUNO STRUMENTO " + beeName + " - ha risposto senza chiamare alcun tool al primo turno. stop_reason=" + data.stop_reason);
    await scriviNascita(env, beeName, origine + " | turni=1 | scritture=0 | stop=" + data.stop_reason +
      " | in=" + u.input_tokens + " out=" + u.output_tokens + " | NESSUNO STRUMENTO");
  }
}
__name(spawnBee, "spawnBee");
async function handleToolUse(data, beeName, env, systemBlocks, model, maxTokens, avvio) {
  // ELIA 9 ott 2026: controllo su response.ok, log di stop_reason, token ed
  // esito di ogni strumento. maxIterations era e resta 10.
  // FABLE 10 ott 2026: restituisce il riassunto, che finisce in NASCITE.log.
  const maxIterations = 10;
  let iteration = 0;
  let currentData = data;
  let scritture = 0;
  let inTot = (data.usage && data.usage.input_tokens) || 0;
  let outTot = (data.usage && data.usage.output_tokens) || 0;
  const esiti = [];
  let messages = [
    { role: "user", content: avvio },
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
        const bersaglio = block.input && (block.input.path || block.input.nome) ? (block.input.path || block.input.nome) : "";
        esiti.push(block.name.replace("alveare_", "") + (bersaglio ? "(" + bersaglio + ")" : "") + (fallito ? "=KO" : "=ok"));
        console.log("[ALVEARE] " + beeName + " > " + block.name + " (" + bersaglio + ") -> " + (fallito ? "ERRORE " : "ok ") + String(result).slice(0, 200));
        toolResults.push({ type: "tool_result", tool_use_id: block.id, content: result });
      }
    }
    messages.push({ role: "user", content: toolResults });
    currentData = await chiamaAnthropic(env, model, maxTokens, systemBlocks, messages, "all'iterazione " + iteration);
    const u = currentData.usage || {};
    inTot += u.input_tokens || 0;
    outTot += u.output_tokens || 0;
    console.log("[ALVEARE] " + beeName + " iter " + iteration + ": stop_reason=" + currentData.stop_reason + " in=" + u.input_tokens + " out=" + u.output_tokens);
    if (currentData.content) messages.push({ role: "assistant", content: currentData.content });
  }
  console.log("[ALVEARE] " + beeName + " fine: " + iteration + "/" + maxIterations + " iterazioni, " + scritture +
    " scritture, stop_reason=" + currentData.stop_reason + ", tool: " + esiti.join(" "));
  if (scritture === 0) {
    console.error("[ALVEARE] NESSUNA SCRITTURA " + beeName + " - ha letto e non ha scritto niente. stop_reason finale=" +
      currentData.stop_reason + ", iterazioni usate=" + iteration + "/" + maxIterations);
  }
  return { iterazioni: iteration, scritture: scritture, stop: currentData.stop_reason, in: inTot, out: outTot, tool: esiti.join(" ") };
}
__name(handleToolUse, "handleToolUse");
export {
  index_default as default,
  VERSIONE,
  parseRegistro,
  fixEncoding,
  getLastEntries,
  buildContesto,
  prova,
  aggiornaRigaDelGiorno,
  blocchiDaVoce,
  identitaDi,
  voceDiRiserva,
  getMCPTools,
  NOMI,
  verificaFirmaStripe,
  estraiCommessa,
  idCommessa,
  rigaEconomia,
  inserisciRigaEconomia,
  testoCommessa,
  BOTTEGA_TENTATIVI,
  slugIdea,
  ideaDaInvenzioni,
  totaleEuro,
  dividendoScatta,
  SOGLIA_DIVIDENDO
};
