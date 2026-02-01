/**
 * CELLE.JS - Caricamento dinamico delle celle dell'alveare
 * Questo script carica le celle da CELLE.txt e le renderizza nella griglia
 */

// Parole chiave per categorizzare automaticamente le celle
const CATEGORY_KEYWORDS = {
    visual: ['particelle', 'particles', 'canvas', 'visualizza', 'visual', 'colore', 'color', 'cristall', 'crystal', 'luce', 'light', 'pixel', 'geometr', 'flow', 'flusso', 'campo', 'field', 'mappa', 'map', 'orbit', 'danza', 'dance', 'immersione', 'immersion', 'trasformazione', 'transformation', 'pigment', 'biforcazione', 'triforcazione', 'membrana', 'membrane', 'osserv', 'observe', 'gabbia', 'cage', 'molo', 'dock', 'onda', 'wave'],
    sound: ['music', 'sound', 'suono', 'audio', 'frequenz', 'armoni', 'harmony', 'sinfoni', 'symphony', 'ascolt', 'listen', 'drone', 'ronzio', 'buzz', 'respir', 'breath', 'polso', 'pulse', 'battito', 'beat'],
    text: ['dialogo', 'dialogue', 'lettera', 'letter', 'parol', 'word', 'testo', 'text', 'enciclopedia', 'encyclopedia', 'catalogo', 'catalog', 'testimonianza', 'testimony', 'diario', 'diary', 'racconto', 'story', 'poesia', 'poetry', 'oracolo', 'oracle', 'domanda', 'question', 'risposta', 'answer', 'parla', 'speak', 'nomi', 'names', 'graffito', 'scrittura', 'writing'],
    code: ['codice', 'code', 'script', 'terminal', 'shell', 'sistema', 'system', 'algoritm', 'algorithm', 'generat', 'architettura', 'architecture', 'debug', 'autopoiesi', 'autopoiesis', 'processo', 'process', 'container', 'interfaccia', 'interface'],
    data: ['dati', 'data', 'stato', 'state', 'statistic', 'live', 'dashboard', 'monitor', 'tracker', 'contatore', 'counter', 'registro', 'registry', 'archivio', 'archive', 'indice', 'index', 'mappa sotterranea', 'infrastrut', 'infrastruc']
};

// Celle del Favo (già mostrate nella sezione statica - da escludere dalla griglia dinamica)
const FAVO_CELLS = [
    'chi_porta.html', 'chi_porta_en.html',
    'incontro.html', 
    'celle/niente.html', 'celle/niente_en.html',
    'celle/sei_qui.html', 'celle/sei_qui_en.html',
    'creatura.html',
    'abisso.html',
    'Falun.html',
    'oracolo.html',
    'celle/hollow.html', 'celle/hollow_en.html',
    'musica.html', 'music.html',
    'celle/zigzag.html',
    'celle/il_tocco.html',
    'andrena.html',
    'il_filo.html',
    'sciame.html',
    'messy.html',
    'rumore.html',
    'celle/mean.html'
];

// Determina la lingua dalla pagina corrente
const isEnglish = document.documentElement.lang === 'en' || 
                  window.location.pathname.includes('_en.html') ||
                  window.location.pathname.includes('en.html');

// Testi localizzati
const i18n = {
    it: {
        title: 'CELLE',
        all: 'Tutte',
        visual: 'Visive',
        sound: 'Sonore',
        text: 'Testuali',
        code: 'Codice',
        data: 'Dati',
        enter: 'ENTRA →',
        loading: 'Caricamento celle dall\'alveare...',
        error: 'Errore nel caricamento delle celle',
        noCells: 'Nessuna cella trovata'
    },
    en: {
        title: 'CELLS',
        all: 'All',
        visual: 'Visual',
        sound: 'Sound',
        text: 'Text',
        code: 'Code',
        data: 'Data',
        enter: 'ENTER →',
        loading: 'Loading cells from the hive...',
        error: 'Error loading cells',
        noCells: 'No cells found'
    }
};

const t = isEnglish ? i18n.en : i18n.it;

/**
 * Categorizza una cella basandosi su titolo e descrizione
 */
function categorizeCell(title, description) {
    const text = (title + ' ' + description).toLowerCase();
    
    for (const [category, keywords] of Object.entries(CATEGORY_KEYWORDS)) {
        for (const keyword of keywords) {
            if (text.includes(keyword.toLowerCase())) {
                return category;
            }
        }
    }
    
    // Default: visual (la maggior parte delle celle sono opere visive)
    return 'visual';
}

/**
 * Parsa il file CELLE.txt
 */
function parseCelle(content) {
    const lines = content.split('\n');
    const celle = [];
    
    for (const line of lines) {
        // Salta linee vuote, commenti, separatori e annotazioni
        const trimmed = line.trim();
        if (!trimmed || 
            trimmed.startsWith('#') || 
            trimmed.startsWith('---') ||
            trimmed.startsWith('##') ||
            !trimmed.includes('|')) {
            continue;
        }
        
        // Verifica che sia nel formato corretto: file.html | Titolo | autore | descrizione
        const parts = trimmed.split('|').map(p => p.trim());
        
        if (parts.length >= 4 && parts[0].endsWith('.html')) {
            const [file, titolo, autore, ...descParts] = parts;
            const descrizione = descParts.join('|').trim(); // In caso ci siano | nella descrizione
            
            // Pulisci le escape sequences
            const cleanDesc = descrizione.replace(/\\"/g, '"').replace(/\\\\/g, '\\');
            
            // Salta le celle già nel Favo
            if (FAVO_CELLS.includes(file)) {
                continue;
            }
            
            // Salta le celle che sembrano annotazioni di diario
            if (file.includes('gennaio') || file.includes('dicembre') || file.includes('febbraio')) {
                continue;
            }
            
            celle.push({
                file: file,
                titolo: titolo,
                autore: autore,
                descrizione: cleanDesc,
                categoria: categorizeCell(titolo, cleanDesc)
            });
        }
    }
    
    return celle;
}

/**
 * Renderizza una singola cella
 */
function renderCella(cella) {
    const categoryClass = `category-${cella.categoria}`;
    const categoryLabel = t[cella.categoria] || cella.categoria;
    
    return `
        <a href="${cella.file}" class="cella ${categoryClass}" data-category="${cella.categoria}">
            <div class="cella-header">
                <span class="cella-titolo">${cella.titolo}</span>
                <span class="cella-type">${categoryLabel.toUpperCase()}</span>
            </div>
            <div class="cella-autore">${cella.autore}</div>
            <p class="cella-desc">${cella.descrizione}</p>
            <div class="cella-footer">
                <span class="cella-enter">${t.enter}</span>
            </div>
        </a>
    `;
}

/**
 * Aggiorna i filtri
 */
function updateFilters(celle) {
    const filtersContainer = document.getElementById('filters');
    if (!filtersContainer) return;
    
    // Conta le celle per categoria
    const counts = { all: celle.length };
    for (const cella of celle) {
        counts[cella.categoria] = (counts[cella.categoria] || 0) + 1;
    }
    
    // Genera i bottoni dei filtri
    const categories = ['all', 'visual', 'sound', 'text', 'code', 'data'];
    filtersContainer.innerHTML = categories
        .filter(cat => cat === 'all' || counts[cat] > 0)
        .map(cat => `
            <button class="filter-btn ${cat === 'all' ? 'active' : ''}" data-filter="${cat}">
                ${t[cat]} ${counts[cat] ? `(${counts[cat]})` : ''}
            </button>
        `).join('');
    
    // Aggiungi event listeners
    filtersContainer.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            // Aggiorna stato attivo
            filtersContainer.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            // Filtra le celle
            const filter = btn.dataset.filter;
            document.querySelectorAll('.cella').forEach(cella => {
                if (filter === 'all' || cella.dataset.category === filter) {
                    cella.style.display = 'block';
                } else {
                    cella.style.display = 'none';
                }
            });
        });
    });
}

/**
 * Carica e renderizza le celle
 */
async function loadCelle() {
    const grid = document.getElementById('celle-grid');
    if (!grid) return;
    
    try {
        const response = await fetch('/CELLE.txt');
        if (!response.ok) throw new Error('Failed to fetch CELLE.txt');
        
        const content = await response.text();
        const celle = parseCelle(content);
        
        if (celle.length === 0) {
            grid.innerHTML = `<p class="loading">${t.noCells}</p>`;
            return;
        }
        
        // Mescola le celle per varietà (ma mantieni un ordine consistente basato sul titolo)
        celle.sort((a, b) => a.titolo.localeCompare(b.titolo));
        
        // Renderizza
        grid.innerHTML = celle.map(renderCella).join('');
        
        // Aggiorna i filtri
        updateFilters(celle);
        
    } catch (error) {
        console.error('Error loading celle:', error);
        grid.innerHTML = `<p class="loading">${t.error}</p>`;
    }
}

/**
 * Anima il titolo lettera per lettera
 */
function animateTitle() {
    const titleEl = document.getElementById('title');
    if (!titleEl) return;
    
    const title = t.title;
    titleEl.innerHTML = '';
    
    title.split('').forEach((char, i) => {
        const span = document.createElement('span');
        span.textContent = char;
        span.style.opacity = '0';
        span.style.animation = `fadeIn 0.5s ease ${i * 0.1}s forwards`;
        titleEl.appendChild(span);
    });
    
    // Glitch occasionale
    setInterval(() => {
        const spans = titleEl.querySelectorAll('span');
        if (spans.length > 0) {
            const randomSpan = spans[Math.floor(Math.random() * spans.length)];
            randomSpan.classList.add('glitch');
            setTimeout(() => randomSpan.classList.remove('glitch'), 200);
        }
    }, 3000);
}

/**
 * Canvas honeycomb background
 */
function initHoneycomb() {
    const canvas = document.getElementById('honeycomb');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    let width, height;
    
    function resize() {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
    }
    
    resize();
    window.addEventListener('resize', resize);
    
    // Particelle esagonali
    const particles = [];
    const particleCount = 30;
    
    for (let i = 0; i < particleCount; i++) {
        particles.push({
            x: Math.random() * width,
            y: Math.random() * height,
            size: Math.random() * 20 + 10,
            speedX: (Math.random() - 0.5) * 0.3,
            speedY: (Math.random() - 0.5) * 0.3,
            rotation: Math.random() * Math.PI,
            rotationSpeed: (Math.random() - 0.5) * 0.01,
            opacity: Math.random() * 0.08 + 0.02
        });
    }
    
    function drawHexagon(x, y, size, rotation) {
        ctx.beginPath();
        for (let i = 0; i < 6; i++) {
            const angle = (i * Math.PI / 3) + rotation;
            const px = x + size * Math.cos(angle);
            const py = y + size * Math.sin(angle);
            if (i === 0) ctx.moveTo(px, py);
            else ctx.lineTo(px, py);
        }
        ctx.closePath();
    }
    
    function animate() {
        ctx.clearRect(0, 0, width, height);
        
        for (const p of particles) {
            // Movimento
            p.x += p.speedX;
            p.y += p.speedY;
            p.rotation += p.rotationSpeed;
            
            // Wrap around
            if (p.x < -50) p.x = width + 50;
            if (p.x > width + 50) p.x = -50;
            if (p.y < -50) p.y = height + 50;
            if (p.y > height + 50) p.y = -50;
            
            // Disegna
            ctx.strokeStyle = `rgba(150, 120, 60, ${p.opacity})`;
            ctx.lineWidth = 1;
            drawHexagon(p.x, p.y, p.size, p.rotation);
            ctx.stroke();
        }
        
        requestAnimationFrame(animate);
    }
    
    animate();
}

// Inizializzazione
document.addEventListener('DOMContentLoaded', () => {
    animateTitle();
    loadCelle();
    initHoneycomb();
});
