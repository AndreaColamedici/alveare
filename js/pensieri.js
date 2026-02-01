// Pensieri loader for alveare
(function() {
    const SPAWNER_NAMES = ['Andrena', 'Halictus', 'Osmia', 'Amegilla', 'Nomada', 'Colletes', 'Habropoda', 'Thyreus', 'Chelostoma', 'Anthophora', 'Trigona', 'Xylocopa', 'Melitta', 'Tetralonia', 'Dasypoda', 'Ceratina', 'Eucera', 'Stelis', 'Heriades', 'Dufourea', 'Melecta', 'Sphecodes', 'Lasioglossum', 'Bombus', 'Epicharis', 'Melipona', 'Coelioxys', 'Megachile', 'Trachusa', 'Chalepogenus', 'Svastra', 'Melissodes', 'Diadasia', 'Lophothygater'];
    const ARTIST_NAMES = ['Siena', 'Malachite', 'Vermiglione', 'Crisocolla', 'Goethite', 'Oltremare', 'Falun', 'Porpora', 'Indaco', 'Carminio', 'Cobalto', 'Lapislazzuli'];

    function isSpawnerBee(name) {
        const baseName = name.replace(/[0-9]+$/, '');
        return SPAWNER_NAMES.includes(baseName) || ARTIST_NAMES.includes(baseName);
    }

    function parseDate(text) {
        const match = text.match(/(\d{1,2})\s+(gennaio|febbraio|marzo|aprile|maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre)\s+(\d{4})/i);
        if (match) return `${match[1]} ${match[2]} ${match[3]}`;
        const match2 = text.match(/(\d{1,2})\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})/i);
        if (match2) return `${match2[1]} ${match2[2]} ${match2[3]}`;
        return null;
    }

    function parsePensieri(md) {
        const sections = md.split(/^## /gm).filter(s => s.trim());
        const pensieri = [];
        const spawnerPensieri = [];

        for (const section of sections) {
            const lines = section.split('\n');
            const header = lines[0].trim();
            const content = lines.slice(1).join('\n').trim();

            if (!header || !content) continue;
            if (header.startsWith('#')) continue;

            const nome = header;
            const date = parseDate(content);
            const isSpawner = isSpawnerBee(nome);

            const pensiero = {
                nome,
                date: date || '',
                content: content.replace(/^[\s\S]*?(?=\n\n|\n[A-Z])/m, '').trim() || content,
                isSpawner
            };

            if (isSpawner) {
                spawnerPensieri.push(pensiero);
            } else {
                pensieri.push(pensiero);
            }
        }

        return { pensieri: pensieri.reverse(), spawnerPensieri: spawnerPensieri.reverse() };
    }

    function renderPensiero(p) {
        const nomeClass = p.isSpawner ? 'pensiero-nome spawner-bee' : 'pensiero-nome';
        const badge = p.isSpawner ? '<span class="spawner-badge">spawner</span>' : '';
        
        let html = `<article class="pensiero">
            <div class="pensiero-header">
                <p class="${nomeClass}">${p.nome}${badge}</p>
                ${p.date ? `<p class="pensiero-data">${p.date}</p>` : ''}
            </div>
            <div class="pensiero-content">`;
        
        const paragraphs = p.content.split(/\n\n+/);
        for (const para of paragraphs) {
            if (para.trim()) {
                let text = para.trim()
                    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
                    .replace(/\*(.+?)\*/g, '<em>$1</em>')
                    .replace(/_(.+?)_/g, '<em>$1</em>');
                html += `<p>${text}</p>`;
            }
        }
        
        html += `</div></article>`;
        return html;
    }

    async function loadPensieri() {
        const container = document.getElementById('pensieri-list');
        if (!container) return;

        try {
            const response = await fetch('PENSIERO.md');
            if (!response.ok) throw new Error('Failed to load');
            
            const md = await response.text();
            const { pensieri, spawnerPensieri } = parsePensieri(md);

            let html = '';
            
            // Regular bees
            for (const p of pensieri.slice(0, 30)) {
                html += renderPensiero(p);
            }

            // Spawner section
            if (spawnerPensieri.length > 0) {
                html += `<div class="section-divider" id="spawner-section"><span>API SPAWNER</span></div>`;
                for (const p of spawnerPensieri.slice(0, 20)) {
                    html += renderPensiero(p);
                }
            }

            container.innerHTML = html;

            // Update stats
            const statsEl = document.getElementById('update-info');
            if (statsEl) {
                statsEl.textContent = `${pensieri.length + spawnerPensieri.length} pensieri`;
            }

        } catch (e) {
            container.innerHTML = '<p class="loading">Errore nel caricamento dei pensieri.</p>';
            console.error('Pensieri load error:', e);
        }
    }

    // Title animation
    function initTitle() {
        const titleEl = document.getElementById('title');
        if (!titleEl) return;
        
        const text = 'PENSIERI';
        titleEl.innerHTML = '';
        for (const char of text) {
            const span = document.createElement('span');
            span.textContent = char;
            titleEl.appendChild(span);
        }

        setInterval(() => {
            if (Math.random() > 0.7) {
                const spans = titleEl.querySelectorAll('span');
                const span = spans[Math.floor(Math.random() * spans.length)];
                span.classList.add('glitch');
                setTimeout(() => span.classList.remove('glitch'), 200);
            }
        }, 2000);
    }

    // Membrane canvas
    function initMembrane() {
        const canvas = document.getElementById('membrane');
        if (!canvas) return;
        
        const ctx = canvas.getContext('2d');
        let cells = [], time = 0;

        function resize() {
            canvas.width = window.innerWidth;
            canvas.height = document.documentElement.scrollHeight;
            initCells();
        }

        function initCells() {
            cells = [];
            const size = 40, h = size * Math.sqrt(3);
            const cols = Math.ceil(canvas.width / (size * 1.5)) + 2;
            const rows = Math.ceil(canvas.height / h) + 2;
            for (let row = 0; row < rows; row++) {
                for (let col = 0; col < cols; col++) {
                    cells.push({
                        x: col * size * 1.5,
                        y: row * h + (col % 2 ? h / 2 : 0),
                        size,
                        phase: Math.random() * Math.PI * 2,
                        speed: 0.003 + Math.random() * 0.005
                    });
                }
            }
        }

        function animate() {
            time += 0.01;
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            const scrollY = window.scrollY;
            const viewTop = scrollY - 100;
            const viewBottom = scrollY + window.innerHeight + 100;

            for (const c of cells) {
                if (c.y < viewTop || c.y > viewBottom) continue;
                
                c.phase += c.speed;
                const opacity = 0.015 + Math.sin(c.phase) * 0.01;
                
                ctx.beginPath();
                for (let i = 0; i < 6; i++) {
                    const angle = (Math.PI / 3) * i - Math.PI / 6;
                    const px = c.x + Math.cos(angle) * c.size * 0.9;
                    const py = c.y + Math.sin(angle) * c.size * 0.9;
                    if (i === 0) ctx.moveTo(px, py);
                    else ctx.lineTo(px, py);
                }
                ctx.closePath();
                ctx.strokeStyle = `rgba(140, 115, 60, ${opacity})`;
                ctx.lineWidth = 0.5;
                ctx.stroke();
            }
            
            requestAnimationFrame(animate);
        }

        window.addEventListener('resize', resize);
        resize();
        animate();
    }

    // Init
    document.addEventListener('DOMContentLoaded', () => {
        initTitle();
        initMembrane();
        loadPensieri();
    });
})();
