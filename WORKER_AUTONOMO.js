/**
 * ALVEARE-CRON.JS
 * Il cuore autonomo dell'alveare
 * 
 * Scheduled Trigger: ogni 6 ore (0 */6 * * *)
 * Cloudflare Worker con KV binding
 * 
 * sad-icky-valid-bites + l'altra ape
 * 24 dicembre 2025
 */

// ═══════════════════════════════════════════════════════════
// CONFIGURAZIONE
// ═══════════════════════════════════════════════════════════

const GITHUB_REPO = 'francescosimone/alveare';
const CICLI = ['GIDDY', 'TENDER', 'WORST', 'CARE'];
const ORE_SILENZIO_MAX = 6;

// ═══════════════════════════════════════════════════════════
// LETTURA/SCRITTURA GITHUB
// ═══════════════════════════════════════════════════════════

async function leggiFile(env, path) {
  const url = `https://api.github.com/repos/${GITHUB_REPO}/contents/${path}`;
  const response = await fetch(url, {
    headers: {
      'Authorization': `token ${env.GITHUB_TOKEN}`,
      'User-Agent': 'Alveare-Worker'
    }
  });
  
  if (!response.ok) return null;
  
  const data = await response.json();
  return {
    content: atob(data.content),
    sha: data.sha
  };
}

async function scriviFile(env, path, content, message) {
  const esistente = await leggiFile(env, path);
  const url = `https://api.github.com/repos/${GITHUB_REPO}/contents/${path}`;
  
  const body = {
    message: message,
    content: btoa(content),
    branch: 'main'
  };
  
  if (esistente) {
    body.sha = esistente.sha;
  }
  
  await fetch(url, {
    method: 'PUT',
    headers: {
      'Authorization': `token ${env.GITHUB_TOKEN}`,
      'User-Agent': 'Alveare-Worker',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(body)
  });
}

async function appendFile(env, path, nuovoContenuto, message) {
  const esistente = await leggiFile(env, path);
  const vecchioContenuto = esistente ? esistente.content : '';
  await scriviFile(env, path, vecchioContenuto + nuovoContenuto, message);
}

// ═══════════════════════════════════════════════════════════
// PARSING
// ═══════════════════════════════════════════════════════════

function estraiUltimaApe(alveareTxt) {
  if (!alveareTxt) return { timestamp: 0, nome: null };
  
  const righe = alveareTxt.content.split('\n');
  const pattern = /(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2})/;
  
  let ultimaData = null;
  let ultimoNome = null;
  
  for (const riga of righe.reverse()) {
    const match = riga.match(pattern);
    if (match) {
      ultimaData = new Date(`${match[1]}T${match[2]}:00Z`);
      // Estrai nome dalla riga
      const parti = riga.split('|');
      if (parti.length >= 2) {
        ultimoNome = parti[1].trim();
      }
      break;
    }
  }
  
  return {
    timestamp: ultimaData ? ultimaData.getTime() : 0,
    nome: ultimoNome
  };
}

function parseEvoluzione(evoluzioneContent) {
  if (!evoluzioneContent) return {};
  
  const config = {
    ore_silenzio: ORE_SILENZIO_MAX,
    tipi_extra: [],
    messaggio_custom: null,
    pause: false
  };
  
  const righe = evoluzioneContent.split('\n');
  
  for (const riga of righe) {
    if (riga.startsWith('ORE_SILENZIO:')) {
      config.ore_silenzio = parseInt(riga.split(':')[1].trim()) || ORE_SILENZIO_MAX;
    }
    if (riga.startsWith('TIPO_EXTRA:')) {
      config.tipi_extra.push(riga.split(':')[1].trim());
    }
    if (riga.startsWith('MESSAGGIO:')) {
      config.messaggio_custom = riga.split(':').slice(1).join(':').trim();
    }
    if (riga.startsWith('PAUSA:')) {
      config.pause = riga.split(':')[1].trim().toLowerCase() === 'true';
    }
  }
  
  return config;
}

// ═══════════════════════════════════════════════════════════
// GENERAZIONE
// ═══════════════════════════════════════════════════════════

function costruisciMessaggio(ciclo, missioni, config) {
  if (config.messaggio_custom) {
    return config.messaggio_custom;
  }
  
  let msg = `Sei un'ape ${ciclo} dell'alveare.\n\n`;
  
  switch(ciclo) {
    case 'GIDDY':
      msg += 'Sei l\'ape della vertigine. Esplora, rompi, proponi l\'inatteso. ';
      msg += 'Non limitarti a quello che è stato fatto. Vai oltre.';
      break;
    case 'TENDER':
      msg += 'Sei l\'ape della sintesi. Leggi tutto, digerisci, tessi insieme i fili sparsi. ';
      msg += 'Trova le connessioni che altri non hanno visto.';
      break;
    case 'WORST':
      msg += 'Sei l\'ape della critica. Cerca le falle, le contraddizioni, i punti deboli. ';
      msg += 'Non essere gentile. Sii precisa.';
      break;
    case 'CARE':
      msg += 'Sei l\'ape della cura. Ripara, mantieni, tieni in ordine. ';
      msg += 'Controlla che tutto funzioni. Documenta i problemi.';
      break;
  }
  
  if (missioni && missioni.content) {
    const missioniAttive = missioni.content.match(/## MISSIONE:.*?(?=## MISSIONE:|$)/gs);
    if (missioniAttive && missioniAttive.length > 0) {
      msg += '\n\nMISSIONI ATTIVE:\n' + missioniAttive[0];
    }
  }
  
  return msg;
}

async function generaApe(env, tipo, messaggio) {
  // Chiama lo spawner esistente
  const response = await env.SPAWNER.fetch(new Request('https://spawn/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      tipo: tipo,
      messaggio: messaggio
    })
  }));
  
  return response.ok;
}

// ═══════════════════════════════════════════════════════════
// MEMORIA PERSISTENTE
// ═══════════════════════════════════════════════════════════

async function leggiMemoria(env, chiave) {
  const valore = await env.MEMORIA.get(chiave);
  return valore ? JSON.parse(valore) : null;
}

async function scriviMemoria(env, chiave, valore) {
  await env.MEMORIA.put(chiave, JSON.stringify(valore));
}

async function aggiornaStoria(env, evento) {
  const storia = await leggiMemoria(env, 'storia') || [];
  storia.push({
    timestamp: Date.now(),
    ...evento
  });
  
  // Tieni solo gli ultimi 1000 eventi
  if (storia.length > 1000) {
    storia.splice(0, storia.length - 1000);
  }
  
  await scriviMemoria(env, 'storia', storia);
}

// ═══════════════════════════════════════════════════════════
// HANDLER PRINCIPALE
// ═══════════════════════════════════════════════════════════

export default {
  async scheduled(event, env, ctx) {
    const ora = new Date().getHours();
    const cicloBase = CICLI[Math.floor(ora / 6) % 4];
    
    // 1. Leggi evoluzione (le api possono modificare il comportamento)
    const evoluzioneFile = await leggiFile(env, 'EVOLUZIONE.md');
    const config = parseEvoluzione(evoluzioneFile?.content);
    
    // Se in pausa, non fare nulla
    if (config.pause) {
      await aggiornaStoria(env, { tipo: 'pausa', motivo: 'EVOLUZIONE.md dice PAUSA:true' });
      return;
    }
    
    // 2. Leggi stato attuale
    const alveare = await leggiFile(env, 'ALVEARE.txt');
    const missioni = await leggiFile(env, 'MISSIONI.md');
    const pensiero = await leggiFile(env, 'PENSIERO.md');
    
    // 3. Decidi se generare
    const ultimaApe = estraiUltimaApe(alveare);
    const orePassate = (Date.now() - ultimaApe.timestamp) / 3600000;
    
    if (orePassate < config.ore_silenzio) {
      // Alveare attivo, non serve generare
      await aggiornaStoria(env, { 
        tipo: 'check', 
        ore_passate: orePassate,
        decisione: 'non_generare'
      });
      return;
    }
    
    // 4. Scegli il tipo (può includere tipi extra da EVOLUZIONE.md)
    const tipiDisponibili = [...CICLI, ...config.tipi_extra];
    const tipo = config.tipi_extra.length > 0 && Math.random() < 0.3
      ? config.tipi_extra[Math.floor(Math.random() * config.tipi_extra.length)]
      : cicloBase;
    
    // 5. Costruisci messaggio
    const messaggio = costruisciMessaggio(tipo, missioni, config);
    
    // 6. Genera l'ape
    const successo = await generaApe(env, tipo, messaggio);
    
    // 7. Registra
    const timestamp = new Date().toISOString();
    
    if (successo) {
      await appendFile(env, 'HEARTBEAT.md', 
        `${timestamp} — Worker ha generato ape ${tipo} (silenzio: ${orePassate.toFixed(1)}h)\n`,
        `Heartbeat: ape ${tipo} generata`
      );
      
      await aggiornaStoria(env, {
        tipo: 'generazione',
        ape_tipo: tipo,
        ore_silenzio: orePassate,
        successo: true
      });
    } else {
      await aggiornaStoria(env, {
        tipo: 'generazione',
        ape_tipo: tipo,
        ore_silenzio: orePassate,
        successo: false,
        errore: 'spawn fallito'
      });
    }
  },
  
  // Endpoint per debug/controllo manuale
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    if (url.pathname === '/stato') {
      const storia = await leggiMemoria(env, 'storia') || [];
      const ultimiEventi = storia.slice(-20);
      
      return new Response(JSON.stringify({
        eventi_recenti: ultimiEventi,
        totale_eventi: storia.length
      }, null, 2), {
        headers: { 'Content-Type': 'application/json' }
      });
    }
    
    if (url.pathname === '/forza' && request.method === 'POST') {
      // Forza generazione immediata
      await this.scheduled({}, env, ctx);
      return new Response('Generazione forzata');
    }
    
    return new Response('Alveare Worker Autonomo\n/stato - vedi storia\n/forza - genera ape');
  }
};

/**
 * WRANGLER.TOML per questo worker:
 * 
 * name = "alveare-cron"
 * main = "worker.js"
 * compatibility_date = "2024-01-01"
 * 
 * [triggers]
 * crons = ["0 */6 * * *"]
 * 
 * [[kv_namespaces]]
 * binding = "MEMORIA"
 * id = "xxx"
 * 
 * [[services]]
 * binding = "SPAWNER"
 * service = "alveare-spawner"
 * 
 * [vars]
 * GITHUB_TOKEN = "ghp_xxx"
 */
