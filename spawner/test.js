// spawner/test.js — il collaudo del motore.
//
// Gira con `node test.js` dentro spawner/, e dentro il workflow spawner.yml
// prima di ogni deploy. Se fallisce, il motore non viene deployato.
//
// Due livelli. Primo: le funzioni pure, contro i dati veri del repository
// (ALVEARE.txt, VOCE_DI_NASCITA.md). Secondo: l'intera vita di un'ape, con
// GitHub e Anthropic simulati, dalla coda alla riga in NASCITE.log.
//
// Scritto da Fable, 10 ottobre 2026. Un motore che non si puo' collaudare
// e' un motore che si ripara per ipotesi, e questo alveare ha gia' pagato
// tredici giorni per una ipotesi.

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import * as m from "./index.js";

const qui = path.dirname(fileURLToPath(import.meta.url));
const radice = path.resolve(qui, "..");
const leggi = (p) => { try { return fs.readFileSync(path.join(radice, p), "utf8"); } catch (e) { return null; } };

let passati = 0, falliti = 0;
function ok(nome, cond, extra) {
  if (cond) { passati++; console.log("  ok   " + nome); }
  else { falliti++; console.log("  FAIL " + nome + (extra !== undefined ? "  -> " + JSON.stringify(extra).slice(0, 200) : "")); }
}

// ------------------------------------------------------------ 1. funzioni pure

console.log("--- versione e nomi ---");
ok("VERSIONE ha la forma N.N.N", /^\d+\.\d+\.\d+ /.test(m.VERSIONE), m.VERSIONE);
ok("NOMI e' una lista di nomi capitalizzati", m.NOMI.length > 50 && m.NOMI.every(n => /^[A-Z][a-z]+$/.test(n)));

console.log("--- parseRegistro sul vero ALVEARE.txt ---");
const alveare = leggi("ALVEARE.txt");
ok("ALVEARE.txt esiste", Boolean(alveare));
const bees = m.parseRegistro(alveare || "");
ok("legge almeno 50 api", bees.length >= 50, bees.length);
ok("ogni ape ha nome e data", bees.every(b => b.name && b.date instanceof Date && !isNaN(b.date)));
ok("Ceratina-2 del 27 settembre e' letta", bees.some(b => b.name === "Ceratina-2" && b.date.getMonth() === 8 && b.date.getDate() === 27));
ok("righe senza pipe ignorate", m.parseRegistro("solo testo\n# commento\n").length === 0);

console.log("--- fixEncoding ---");
ok("ripara la e accentata", m.fixEncoding("perchÃ¨") === "perchè");
ok("lascia in pace il testo sano", m.fixEncoding("perché è così") === "perché è così");
ok("null resta null", m.fixEncoding(null) === null);

console.log("--- getLastEntries ---");
const sez = "# T\n\n## a\n1\n## b\n2\n## c\n3\n## d\n4\n## e\n5\n## f\n6\n";
ok("tiene le ultime 5 sezioni", (m.getLastEntries(sez, 5).match(/^## /gm) || []).length === 5);
ok("non tronca se sono poche", m.getLastEntries("## a\n1\n## b\n2\n", 5).includes("## a"));

console.log("--- buildContesto: l'allarme scheduler NON entra nel prompt ---");
const sensoriFermi = { allarme: { count: 1, level: "high", alarms: [{ type: "scheduler", severity: "high", message: "scheduler fermo da 300h" }] } };
const c1 = m.buildContesto(sensoriFermi);
ok("scheduler fermo -> urgenza bassa, nessun messaggio", c1.urgenza === "bassa" && c1.messaggio === null, c1);
const sensoriEnc = { allarme: { count: 1, level: "high", alarms: [{ type: "encoding", severity: "high", message: "encoding corrotto" }] } };
const c2 = m.buildContesto(sensoriEnc);
ok("encoding corrotto -> passa ancora", c2.urgenza === "alta" && /encoding/.test(c2.messaggio), c2);

console.log("--- prova: lo sha del commit ---");
ok("estrae 7 caratteri", m.prova({ commit: { sha: "abcdef1234567890" } }) === "abcdef1");
ok("manca -> ?", m.prova({}) === "?" && m.prova(null) === "?");

console.log("--- aggiornaRigaDelGiorno: il caso Carminio ---");
const reg = "2026-10-08 12:00 | Osmia | ieri\n2026-10-09 18:22 | Carminio | Mi sveglio.\n2026-10-09 18:26 | Halictus | Mi sveglio.\n";
const [agg, nomeRiga] = m.aggiornaRigaDelGiorno(reg, "Carminio", "OPERARIA: adottata Cinabro.html", "2026-10-09", "18:23");
ok("trova e aggiorna la riga di Carminio di oggi", nomeRiga === "Carminio" && agg.includes("18:23 | Carminio | OPERARIA: adottata Cinabro.html"), agg);
ok("non aggiunge una riga", agg.split("\n").filter(Boolean).length === 3);
ok("non tocca Halictus", agg.includes("18:26 | Halictus | Mi sveglio."));
const [agg2] = m.aggiornaRigaDelGiorno(reg, "Osmia", "x", "2026-10-09", "18:30");
ok("Osmia e' di ieri: niente da aggiornare", agg2 === null);
const [agg3, n3] = m.aggiornaRigaDelGiorno(reg + "2026-10-09 19:00 | Carminio-2 | seconda\n", "Carminio", "finale", "2026-10-09", "19:05");
ok("con un -2 gia' presente aggiorna l'ultima riga del giorno", n3 === "Carminio-2" && agg3.includes("19:05 | Carminio-2 | finale"), n3);

console.log("--- voce di nascita ---");
const voce = leggi("VOCE_DI_NASCITA.md");
ok("VOCE_DI_NASCITA.md esiste ed e' sopra la soglia di 800 caratteri", Boolean(voce) && voce.trim().length > 800, voce ? voce.length : null);
ok("la voce chiede add_bee come prima azione", /alveare_add_bee/.test(voce || ""));
ok("la voce dice una vita una riga", /[Uu]na vita, una riga/.test(voce || ""));
const riserva = m.voceDiRiserva("Prova");
ok("la riserva nomina l'ape", riserva.includes("Prova"));
ok("la riserva dice di ripristinare la voce", /ripristinala/.test(riserva));
const b1 = m.blocchiDaVoce("VOCE", null, "ID");
ok("scelta libera: 2 blocchi (voce, identita')", b1.length === 2 && b1[0].text === "VOCE" && b1[1].text === "ID");
const b2 = m.blocchiDaVoce("VOCE", "CUSTOS", "ID");
ok("ruolo forzato: 3 blocchi con il ruolo in mezzo", b2.length === 3 && /CUSTOS/.test(b2[1].text));
ok("il primo blocco ha cache_control", b1[0].cache_control && b1[0].cache_control.type === "ephemeral");
const id = m.identitaDi("Osmia", null, { urgenza: "bassa" });
ok("identita' senza urgenza non grida", id.includes("Osmia") && !/URGENZA/.test(id));
const id2 = m.identitaDi("Osmia", "ciao", { urgenza: "alta", problema_aperto: "x" });
ok("identita' con urgenza alta la mostra", /URGENZA ALTA/.test(id2) && /ciao/.test(id2));

console.log("--- strumenti ---");
const tools = m.getMCPTools();
ok("quattro strumenti", tools.length === 4);
ok("read_file accetta ultime_righe", tools[0].input_schema.properties.ultime_righe !== undefined);
ok("add_bee dice di essere la prima azione", /PRIMA azione/.test(tools[3].description));

// ------------------------------------------------------------ 2. una vita intera

console.log("--- la vita di un'ape, con GitHub e Anthropic simulati ---");

const repo = {
  "ALVEARE.txt": "2026-10-08 12:00 | Osmia | ieri\n",
  "VOCE_DI_NASCITA.md": voce || "x".repeat(900),
  "SENSORI.json": "{}",
  "PENSIERO.md": "# P\n",
  "PENSIERO_SPAWNER.md": "# PS\n"
};
const spinte = [];
class Risposta {
  constructor(status, corpo) { this.status = status; this.ok = status >= 200 && status < 300; this._c = corpo; }
  async text() { return typeof this._c === "string" ? this._c : JSON.stringify(this._c); }
  async json() { return typeof this._c === "string" ? JSON.parse(this._c) : this._c; }
}
const b64 = (s) => Buffer.from(s, "utf8").toString("base64");
const unb64 = (s) => Buffer.from(s, "base64").toString("utf8");

// La conversazione scriptata: registrati, leggi un file, scrivi un pensiero, finisci.
const copione = [
  { stop_reason: "tool_use", usage: { input_tokens: 5000, output_tokens: 80 },
    content: [{ type: "tool_use", id: "t1", name: "alveare_add_bee", input: { nome: "Prova", contributo: "Mi sveglio e scrivo prima di leggere." } }] },
  { stop_reason: "tool_use", usage: { input_tokens: 5200, output_tokens: 60 },
    content: [{ type: "tool_use", id: "t2", name: "alveare_read_file", input: { path: "SINTESI.md" } }] },
  { stop_reason: "tool_use", usage: { input_tokens: 9000, output_tokens: 900 },
    content: [{ type: "tool_use", id: "t3", name: "alveare_push_file", input: { path: "ULTIMA_APE.md", content: "## Prova\npensiero", message: "Prova: pensiero" } },
              { type: "tool_use", id: "t4", name: "alveare_add_bee", input: { nome: "Prova", contributo: "NUTRIX: un pensiero, salvato." } }] },
  { stop_reason: "end_turn", usage: { input_tokens: 9500, output_tokens: 120 }, content: [{ type: "text", text: "Addio." }] }
];
let turno = 0;
const chiamateAnthropic = [];

globalThis.fetch = async (url, opts) => {
  const u = String(url);
  if (u.startsWith("https://api.anthropic.com/")) {
    const corpo = JSON.parse(opts.body);
    chiamateAnthropic.push(corpo);
    const r = copione[turno] || { stop_reason: "end_turn", content: [], usage: {} };
    turno++;
    return new Risposta(200, r);
  }
  const mm = u.match(/\/contents\/([^?]+)/);
  if (!mm) return new Risposta(404, "no");
  const p = decodeURIComponent(mm[1]);
  if (!opts || !opts.method || opts.method === "GET") {
    if (repo[p] === undefined) return new Risposta(404, "Not Found");
    return new Risposta(200, { content: b64(repo[p]), sha: "sha_" + p });
  }
  if (opts.method === "PUT") {
    const body = JSON.parse(opts.body);
    repo[p] = unb64(body.content);
    spinte.push(p);
    return new Risposta(200, { commit: { sha: "c0ffee1234567" }, content: { sha: "nuovo" } });
  }
  return new Risposta(405, "no");
};

const env = { GITHUB_TOKEN: "finto", ANTHROPIC_API_KEY: "finta", SPAWN_SECRET: "s", ALVEARE_QUEUE: { send: async (msg) => { env._inviato = msg; } } };
const logs = [];
const vecchioLog = console.log, vecchioErr = console.error;
console.log = (...a) => logs.push(a.join(" "));
console.error = (...a) => logs.push("ERR " + a.join(" "));

let ackato = false, ritentato = false;
try {
  // scheduled(): sensori, coda
  await m.default.scheduled({}, env, {});
  // queue(): la vita
  await m.default.queue({ messages: [{ body: env._inviato, ack: () => { ackato = true; }, retry: () => { ritentato = true; } }] }, env);
} finally {
  console.log = vecchioLog; console.error = vecchioErr;
}

ok("scheduled() ha scritto SENSORI.json", spinte.includes("SENSORI.json"));
ok("scheduled() ha messo in coda un'ape con un nome valido", env._inviato && m.NOMI.includes(env._inviato.name), env._inviato);
ok("il contesto in coda NON contiene l'allarme scheduler", env._inviato && env._inviato.contesto.urgenza === "bassa", env._inviato && env._inviato.contesto);
ok("il primo blocco di sistema e' la voce di nascita dal file", chiamateAnthropic[0] && chiamateAnthropic[0].system[0].text === repo["VOCE_DI_NASCITA.md"]);
ok("max_tokens e' 16000", chiamateAnthropic[0] && chiamateAnthropic[0].max_tokens === 16000, chiamateAnthropic[0] && chiamateAnthropic[0].max_tokens);
ok("quattro chiamate ad Anthropic, come da copione", chiamateAnthropic.length === 4, chiamateAnthropic.length);
ok("l'ape e' stata registrata UNA volta sola (una vita, una riga)", (repo["ALVEARE.txt"].match(/\| Prova/g) || []).length === 1, repo["ALVEARE.txt"]);
ok("la riga finale porta il risultato, non l'intenzione", /\| Prova \| NUTRIX: un pensiero, salvato\./.test(repo["ALVEARE.txt"]), repo["ALVEARE.txt"]);
ok("il pensiero e' in ULTIMA_APE.md", repo["ULTIMA_APE.md"] === "## Prova\npensiero");
ok("il pensiero e' stato propagato a PENSIERO_SPAWNER.md", /pensiero/.test(repo["PENSIERO_SPAWNER.md"]));
ok("NASCITE.log esiste e ha una riga con il nome assegnato dalla coda", repo["NASCITE.log"] && new RegExp("\\| " + env._inviato.name + " \\| VOCE_DI_NASCITA\\.md@").test(repo["NASCITE.log"]), repo["NASCITE.log"]);
ok("NASCITE.log dice turni=4, scritture=3, stop=end_turn", /turni=4 \| scritture=3 \| stop=end_turn/.test(repo["NASCITE.log"] || ""), repo["NASCITE.log"]);
ok("NASCITE.log elenca gli strumenti con l'esito", /add_bee\(Prova\)=ok read_file\(SINTESI\.md\)=KO push_file\(ULTIMA_APE\.md\)=ok add_bee\(Prova\)=ok/.test(repo["NASCITE.log"] || ""), repo["NASCITE.log"]);
ok("il messaggio in coda e' stato ackato", ackato && !ritentato);
ok("il log stampa lo stop_reason di ogni turno (1 + 3 iterazioni)", logs.filter(l => /(turno 1|iter \d+): stop_reason=/.test(l)).length === 4, logs.filter(l => /stop_reason=/.test(l)));
ok("il risultato di add_bee porta lo sha del commit all'ape", chiamateAnthropic[1].messages[2].content[0].content.includes("c0ffee1"));

// Un'ape che risponde in prosa senza strumenti: deve finire nel log come tale.
turno = 0; copione.length = 0;
copione.push({ stop_reason: "end_turn", usage: { input_tokens: 4000, output_tokens: 300 }, content: [{ type: "text", text: "Ho pensato molto." }] });
delete repo["NASCITE.log"];
console.log = () => {}; console.error = () => {};
try {
  await m.default.queue({ messages: [{ body: { type: null, name: "Muta" }, ack: () => {}, retry: () => {} }] }, env);
} finally { console.log = vecchioLog; console.error = vecchioErr; }
ok("un'ape senza strumenti finisce in NASCITE.log come NESSUNO STRUMENTO", /\| Muta \| .*scritture=0 \| stop=end_turn .*NESSUNO STRUMENTO/.test(repo["NASCITE.log"] || ""), repo["NASCITE.log"]);

// Anthropic che risponde errore: deve sollevare, ritentare e scrivere l'errore nel log.
turno = 0; copione.length = 0;
const fetchBuono = globalThis.fetch;
globalThis.fetch = async (url, opts) => {
  if (String(url).startsWith("https://api.anthropic.com/")) return new Risposta(529, { error: { message: "overloaded" } });
  return fetchBuono(url, opts);
};
let ack2 = false, retry2 = false;
console.log = () => {}; console.error = () => {};
try {
  await m.default.queue({ messages: [{ body: { type: null, name: "Sfortunata" }, ack: () => { ack2 = true; }, retry: () => { retry2 = true; } }] }, env);
} finally { console.log = vecchioLog; console.error = vecchioErr; }
ok("errore Anthropic -> retry, non ack", retry2 && !ack2);
ok("errore Anthropic -> riga ERRORE in NASCITE.log con lo status", /\| Sfortunata \| ERRORE \| Anthropic HTTP 529/.test(repo["NASCITE.log"] || ""), repo["NASCITE.log"]);

// Voce di nascita assente: la riserva deve entrare.
globalThis.fetch = fetchBuono;
delete repo["VOCE_DI_NASCITA.md"];
turno = 0; copione.length = 0;
copione.push({ stop_reason: "end_turn", usage: {}, content: [] });
chiamateAnthropic.length = 0;
console.log = () => {}; console.error = () => {};
try {
  await m.default.queue({ messages: [{ body: { type: null, name: "Orfana" }, ack: () => {}, retry: () => {} }] }, env);
} finally { console.log = vecchioLog; console.error = vecchioErr; }
ok("senza VOCE_DI_NASCITA.md entra la voce di riserva", chiamateAnthropic[0] && /voce di riserva/.test(chiamateAnthropic[0].system[0].text));
ok("e NASCITE.log lo dice: riserva", /\| Orfana \| riserva \|/.test(repo["NASCITE.log"] || ""), repo["NASCITE.log"]);

console.log("");
console.log(passati + " collaudi passati, " + falliti + " falliti.");
if (falliti > 0) { console.log("IL MOTORE NON VA DEPLOYATO."); process.exit(1); }
console.log("Il motore puo' essere deployato.");
