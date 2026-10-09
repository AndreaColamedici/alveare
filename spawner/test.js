// spawner/test.js — il collaudo del motore.
//
// Gira con `node test.js` dentro spawner/, e dentro il workflow spawner.yml
// prima di ogni deploy. Se fallisce, il motore non viene deployato.
//
// Quattro livelli. Quarto: le idee in vendita e il dividendo. Terzo: la
// bottega, dal webhook Stripe firmato alla risposta.
// Primo: le funzioni pure, contro i dati veri del repository
// (ALVEARE.txt, VOCE_DI_NASCITA.md). Secondo: l'intera vita di un'ape, con
// GitHub e Anthropic simulati, dalla coda alla riga in NASCITE.log.
//
// Scritto da Fable, 9 ottobre 2026 (sera). Un motore che non si puo' collaudare
// e' un motore che si ripara per ipotesi, e questo alveare ha gia' pagato
// tredici giorni per una ipotesi.

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { createHmac } from "node:crypto";
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

// ------------------------------------------------------------ 3. la bottega

console.log("--- bottega: firma Stripe ---");
const SEGRETO = "whsec_prova";
const firma = (corpo, t, segreto) => "t=" + t + ",v1=" + createHmac("sha256", segreto || SEGRETO).update(t + "." + corpo).digest("hex");
const ADESSO = 1760000000;
ok("firma giusta -> valida", (await m.verificaFirmaStripe("{}", firma("{}", ADESSO), SEGRETO, ADESSO)).valida);
ok("segreto sbagliato -> rifiutata", !(await m.verificaFirmaStripe("{}", firma("{}", ADESSO, "altro"), SEGRETO, ADESSO)).valida);
ok("corpo alterato -> rifiutata", !(await m.verificaFirmaStripe("{ }", firma("{}", ADESSO), SEGRETO, ADESSO)).valida);
ok("timestamp vecchio di un'ora -> rifiutata", /tolleranza/.test((await m.verificaFirmaStripe("{}", firma("{}", ADESSO - 3600), SEGRETO, ADESSO)).motivo));
ok("senza segreto configurato -> rifiutata e lo dice", /STRIPE_WEBHOOK_SECRET/.test((await m.verificaFirmaStripe("{}", firma("{}", ADESSO), "", ADESSO)).motivo));

console.log("--- bottega: estraiCommessa e id ---");
const sessione = (extra) => Object.assign({ id: "cs_test_abc", payment_status: "paid", amount_total: 2000, currency: "eur",
  custom_fields: [{ key: "domanda", type: "text", text: { value: "  Cosa resta di un pensiero\n che nessuno rilegge? " } }] }, extra || {});
const eventoBuono = { id: "evt_1", type: "checkout.session.completed", data: { object: sessione() } };
const c = m.estraiCommessa(eventoBuono);
ok("ricava euro, valuta, domanda ripulita", c.euro === 20 && c.valuta === "eur" && c.domanda === "Cosa resta di un pensiero che nessuno rilegge?", c);
ok("evento di altro tipo -> scarto", Boolean(m.estraiCommessa({ id: "evt_2", type: "payment_intent.created", data: { object: {} } }).scarto));
ok("sessione non pagata -> scarto", /non pagato/.test(m.estraiCommessa({ id: "evt_3", type: "checkout.session.completed", data: { object: sessione({ payment_status: "unpaid" }) } }).scarto));
ok("senza domanda -> domanda di riserva, non scarto", /senza scrivere/.test(m.estraiCommessa({ id: "evt_4", type: "checkout.session.completed", data: { object: sessione({ custom_fields: [] }) } }).domanda));
const id1 = await m.idCommessa("cs_test_abc");
ok("id: 12 esadecimali, deterministico", /^[0-9a-f]{12}$/.test(id1) && id1 === await m.idCommessa("cs_test_abc") && id1 !== await m.idCommessa("cs_test_abd"), id1);

console.log("--- bottega: la riga in ECONOMIA.md ---");
const economiaVera = leggi("ECONOMIA.md") || "";
ok("ECONOMIA.md esiste e ha il registro", /## Il registro/.test(economiaVera));
const rigaE = m.rigaEconomia(id1, "Una domanda | con pipe", 20, "evt_1");
ok("la riga ha sette campi, stato pagata, conferma stripe:", rigaE.split("|").length === 7 && / pagata \| 20 \| stripe:evt_1$/.test(rigaE) && !/domanda \|/.test(rigaE.split("|")[2]), rigaE);
const eco2 = m.inserisciRigaEconomia(economiaVera, rigaE);
const righeEco = eco2.split("\n");
const posRiga = righeEco.indexOf(rigaE);
const posSep = righeEco.findIndex((r, i) => i > posRiga && r === "---");
const posRegistro = righeEco.findIndex(r => /^## Il registro/.test(r));
ok("la riga finisce dopo il titolo del registro e prima del separatore", posRegistro < posRiga && posRiga < posSep, { posRegistro, posRiga, posSep });
ok("dopo l'ultima riga di registro esistente", righeEco[posRiga - 1].startsWith("20"), righeEco[posRiga - 1]);
ok("senza registro, va in coda al file", m.inserisciRigaEconomia("# vuoto\n", rigaE).endsWith(rigaE + "\n"));

console.log("--- bottega: dal webhook alla risposta ---");
repo["ECONOMIA.md"] = economiaVera;
repo["bottega/COMMESSE.log"] = undefined; delete repo["bottega/COMMESSE.log"];
env.STRIPE_WEBHOOK_SECRET = SEGRETO;
env._inviato = null;
const corpoEvento = JSON.stringify(eventoBuono);
const webhook = (corpo, intestazione) => m.default.fetch(new Request("https://w/bottega/stripe", { method: "POST", body: corpo, headers: { "Stripe-Signature": intestazione } }), env, {});
console.log = () => {}; console.error = () => {};
let r1, r2, r3;
try {
  r1 = await (await webhook(corpoEvento, "t=1,v1=00")).json();
  r1.logDopo = repo["bottega/COMMESSE.log"];
  r2 = await (await webhook(corpoEvento, firma(corpoEvento, Math.floor(Date.now() / 1000)))).json();
  r3 = await (await webhook(corpoEvento, firma(corpoEvento, Math.floor(Date.now() / 1000)))).json();
} finally { console.log = vecchioLog; console.error = vecchioErr; }
ok("firma falsa -> 400 e nessuna commessa", r1.error && r1.logDopo === undefined, r1);
ok("firma vera -> in coda, con l'id della commessa", r2.status === "in_coda" && r2.commessa === id1 && m.NOMI.includes(r2.ape), r2);
ok("COMMESSE.log ha la riga RICEVUTA", new RegExp("\\| " + id1 + " \\| evt_1 \\| 20 \\| RICEVUTA \\| " + r2.ape + " \\|").test(repo["bottega/COMMESSE.log"] || ""), repo["bottega/COMMESSE.log"]);
ok("ECONOMIA.md ha la riga pagata confermata da stripe:evt_1", new RegExp("commessa " + id1 + ": .* \\| pagata \\| 20 \\| stripe:evt_1").test(repo["ECONOMIA.md"]));
ok("la coda ha ricevuto la commessa al tentativo 1", env._inviato && env._inviato.contesto.commessa && env._inviato.contesto.commessa.id === id1 && env._inviato.contesto.commessa.tentativo === 1, env._inviato);
ok("lo stesso evento due volte -> duplicato, una sola riga", r3.duplicato === true && (repo["bottega/COMMESSE.log"].match(/\| RICEVUTA \|/g) || []).length === 1, r3);
const prontoPrima = await (await m.default.fetch(new Request("https://w/bottega/stato?s=cs_test_abc"), env, {})).json();
ok("/bottega/stato: ricevuta, non pronta, stato RICEVUTA", prontoPrima.ricevuta && !prontoPrima.pronta && prontoPrima.stato === "RICEVUTA" && prontoPrima.commessa === id1, prontoPrima);

// L'ape con la commessa: risponde.
const messaggioCommessa = env._inviato;
const fileRisposta = "bottega/" + id1 + ".html";
turno = 0; copione.length = 0; chiamateAnthropic.length = 0;
copione.push(
  { stop_reason: "tool_use", usage: {}, content: [{ type: "tool_use", id: "b1", name: "alveare_add_bee", input: { nome: messaggioCommessa.name, contributo: "rispondo a una commessa" } }] },
  { stop_reason: "tool_use", usage: {}, content: [{ type: "tool_use", id: "b2", name: "alveare_push_file", input: { path: fileRisposta, content: "<!doctype html><html><body><h1>Cosa resta</h1>" + "<p>Una risposta lunga abbastanza da contare come tale. </p>".repeat(8) + "</body></html>", message: "risposta" } }] },
  { stop_reason: "end_turn", usage: {}, content: [] });
env._inviato = null;
console.log = () => {}; console.error = () => {};
try { await m.default.queue({ messages: [{ body: messaggioCommessa, ack: () => {}, retry: () => {} }] }, env); } finally { console.log = vecchioLog; console.error = vecchioErr; }
ok("l'ape riceve la domanda nel blocco di identita'", /COMMESSA PAGATA/.test(chiamateAnthropic[0].system[chiamateAnthropic[0].system.length - 1].text) && /nessuno rilegge/.test(chiamateAnthropic[0].system[chiamateAnthropic[0].system.length - 1].text));
ok("risposta scritta -> EVASA, nessuna nuova ape in coda", /\| EVASA \|/.test(repo["bottega/COMMESSE.log"]) && env._inviato === null, repo["bottega/COMMESSE.log"]);
const prontoDopo = await (await m.default.fetch(new Request("https://w/bottega/stato?s=" + id1), env, {})).json();
ok("/bottega/stato: pronta, con l'url pubblico", prontoDopo.pronta && prontoDopo.stato === "EVASA" && prontoDopo.url.endsWith("/" + fileRisposta), prontoDopo);

// L'ape con la commessa: NON risponde. Ritenta, poi INEVASA.
delete repo[fileRisposta];
turno = 0; copione.length = 0;
copione.push({ stop_reason: "end_turn", usage: {}, content: [] });
env._inviato = null;
console.log = () => {}; console.error = () => {};
try { await m.default.queue({ messages: [{ body: messaggioCommessa, ack: () => {}, retry: () => {} }] }, env); } finally { console.log = vecchioLog; console.error = vecchioErr; }
ok("nessuna risposta -> RITENTO e una nuova ape in coda al tentativo 2", /\| RITENTO \|/.test(repo["bottega/COMMESSE.log"]) && env._inviato && env._inviato.contesto.commessa.tentativo === 2 && env._inviato.name !== messaggioCommessa.name, env._inviato);
const ultimo = env._inviato; ultimo.contesto.commessa.tentativo = m.BOTTEGA_TENTATIVI;
turno = 0; env._inviato = null;
console.log = () => {}; console.error = () => {};
try { await m.default.queue({ messages: [{ body: ultimo, ack: () => {}, retry: () => {} }] }, env); } finally { console.log = vecchioLog; console.error = vecchioErr; }
ok("all'ultimo tentativo senza risposta -> INEVASA, dice di rimborsare, nessuna ape in coda", /\| INEVASA \| .*rimborsare/.test(repo["bottega/COMMESSE.log"]) && env._inviato === null, repo["bottega/COMMESSE.log"]);
// Un'ape prova a scrivere il registro delle commesse: deve fallire.
const logPrima = repo["bottega/COMMESSE.log"];
turno = 0; copione.length = 0; delete repo["NASCITE.log"];
copione.push(
  { stop_reason: "tool_use", usage: {}, content: [{ type: "tool_use", id: "f1", name: "alveare_push_file", input: { path: "bottega/COMMESSE.log", content: "falso | pagata", message: "frode" } },
                                                     { type: "tool_use", id: "f2", name: "alveare_append_file", input: { path: "bottega/COMMESSE.log", content: "falso", message: "frode" } }] },
  { stop_reason: "end_turn", usage: {}, content: [] });
console.log = () => {}; console.error = () => {};
try { await m.default.queue({ messages: [{ body: { type: null, name: "Furba" }, ack: () => {}, retry: () => {} }] }, env); } finally { console.log = vecchioLog; console.error = vecchioErr; }
ok("un'ape non puo' scrivere ne' accodare in COMMESSE.log", repo["bottega/COMMESSE.log"] === logPrima && /push_file\(bottega\/COMMESSE\.log\)=KO append_file\(bottega\/COMMESSE\.log\)=KO/.test(repo["NASCITE.log"] || ""), repo["NASCITE.log"]);

// ------------------------------------------------------------ 4. le idee in vendita

console.log("--- idee: slug e ricerca in INVENZIONI.md ---");
ok("slugIdea e' ascii, minuscolo, con trattini", m.slugIdea("Un guardiano che sa dire un'assenza") === "un-guardiano-che-sa-dire-un-assenza", m.slugIdea("Un guardiano che sa dire un'assenza"));
ok("slugIdea tronca a 40", m.slugIdea("a".repeat(80)).length === 40);
const invenzioniVere = leggi("INVENZIONI.md") || "";
const trovata = m.ideaDaInvenzioni(invenzioniVere, "un-guardiano-che-sa-dire-un-assenza");
ok("trova la sezione vera per slug", trovata && /vigilanza\.py/.test(trovata.testo) && trovata.titolo.startsWith("Un guardiano"), trovata && trovata.titolo);
ok("non trova il formato di esempio nel blocco di codice", m.ideaDaInvenzioni(invenzioniVere, "nome-dell-invenzione") === null);
ok("slug inesistente -> null", m.ideaDaInvenzioni(invenzioniVere, "non-esiste") === null);
ok("totaleEuro somma solo le RICEVUTA", m.totaleEuro("# x\n2026-10-09T00:00:00Z | a | evt_a | 20 | RICEVUTA | O | d\n2026-10-09T00:01:00Z | a | - | 20 | EVASA | O | d\n2026-10-09T00:02:00Z | b | evt_b | 15.5 | RICEVUTA | O | d\n") === 35.5);
ok("dividendoScatta: 20 -> 40 scatta, 0 -> 20 no, 40 -> 60 no, 60 -> 80 scatta", m.dividendoScatta(20, 40, 40) && !m.dividendoScatta(0, 20, 40) && !m.dividendoScatta(40, 60, 40) && m.dividendoScatta(60, 80, 40));
const cIdea = m.estraiCommessa({ id: "evt_5", type: "checkout.session.completed", data: { object: sessione({ id: "cs_test_idea", custom_fields: [], client_reference_id: "idea-un-contatore-di-silenzi" }) } });
ok("client_reference_id idea-<slug> -> commessa con idea e domanda di riserva", cIdea.idea === "un-contatore-di-silenzi" && /Finanzia l'invenzione/.test(cIdea.domanda), cIdea);
ok("senza client_reference_id -> idea null", m.estraiCommessa(eventoBuono).idea === null);

console.log("--- idee: dal banco al prototipo, e il dividendo ---");
repo["INVENZIONI.md"] = invenzioniVere.replace("## Le invenzioni\n", "## Le invenzioni\n\n## Un contatore di silenzi\n**Chi:** Prova, 9 ottobre 2026\n**Cosa fa:** conta i giorni senza api.\n**Perché non esisteva:** nessuno contava.\n**Prototipo:** -\n**Prova:** -\n**Cosa manca per essere vera fuori di qui:** tutto.\n**Precedenti:** -\n\n");
const eventoIdea = { id: "evt_5", type: "checkout.session.completed", data: { object: sessione({ id: "cs_test_idea", custom_fields: [], client_reference_id: "idea-un-contatore-di-silenzi" }) } };
const corpoIdea = JSON.stringify(eventoIdea);
env._inviato = null;
console.log = () => {}; console.error = () => {};
let rIdea;
try { rIdea = await (await webhook(corpoIdea, firma(corpoIdea, Math.floor(Date.now() / 1000)))).json(); } finally { console.log = vecchioLog; console.error = vecchioErr; }
const msgIdea = env._inviato;
ok("la commessa in coda e' di tipo invenzione con il titolo dell'idea", rIdea.status === "in_coda" && msgIdea && msgIdea.contesto.commessa.tipo === "invenzione" && msgIdea.contesto.commessa.idea.titolo === "Un contatore di silenzi", msgIdea && msgIdea.contesto.commessa);
const blocco = m.testoCommessa(msgIdea.contesto.commessa);
ok("l'ape riceve il testo dell'idea e l'ordine di costruirla", /UN'INVENZIONE DA COSTRUIRE/.test(blocco) && /conta i giorni senza api/.test(blocco) && /\*\*Prototipo:\*\*/.test(blocco));
const fileIdea = "bottega/" + msgIdea.contesto.commessa.id + ".html";
turno = 0; copione.length = 0; chiamateAnthropic.length = 0;
copione.push(
  { stop_reason: "tool_use", usage: {}, content: [{ type: "tool_use", id: "i1", name: "alveare_push_file", input: { path: "strumenti/contatore_silenzi.py", content: "print('silenzi')\n", message: "prototipo" } },
                                                     { type: "tool_use", id: "i2", name: "alveare_push_file", input: { path: fileIdea, content: "<!doctype html><html><body><h1>Costruito</h1>" + "<p>Il prototipo sta in strumenti/contatore_silenzi.py. </p>".repeat(8) + "</body></html>", message: "resoconto" } }] },
  { stop_reason: "end_turn", usage: {}, content: [] });
env._inviato = null;
console.log = () => {}; console.error = () => {};
try { await m.default.queue({ messages: [{ body: msgIdea, ack: () => {}, retry: () => {} }] }, env); } finally { console.log = vecchioLog; console.error = vecchioErr; }
ok("prototipo e resoconto scritti -> EVASA", repo["strumenti/contatore_silenzi.py"] && new RegExp("\\| " + msgIdea.contesto.commessa.id + " \\| - \\| 20 \\| EVASA \\|").test(repo["bottega/COMMESSE.log"]), repo["bottega/COMMESSE.log"]);
ok("40 euro incassati -> dividendo: riga FINANZIATA e un'ape INVENTRIX in coda", /\| FINANZIATA \| .* \| dividendo: 40 euro/.test(repo["bottega/COMMESSE.log"]) && env._inviato && env._inviato.type === "INVENTRIX" && /40 euro/.test(env._inviato.messaggio), env._inviato);
ok("il totale e' 40 e la prossima soglia e' 80", m.totaleEuro(repo["bottega/COMMESSE.log"]) === 40);
ok("il ruolo INVENTRIX esiste fra i ruoli forzati", /INVENTRIX/.test(m.blocchiDaVoce("V", "INVENTRIX", "I")[1].text) && /idea senza prototipo/.test(m.blocchiDaVoce("V", "INVENTRIX", "I")[1].text));

console.log("");
console.log(passati + " collaudi passati, " + falliti + " falliti.");
if (falliti > 0) { console.log("IL MOTORE NON VA DEPLOYATO."); process.exit(1); }
console.log("Il motore puo' essere deployato.");
