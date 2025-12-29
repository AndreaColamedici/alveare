// === NASCITA LIVE ===
// Mostra una notifica quando un'ape nasce (scrive su ULTIMA_APE.md)

(function() {
    const REPO = 'andreacolamedici/alveare';
    const FILE = 'ULTIMA_APE.md';
    const MINUTI_SOGLIA = 10;
    const INTERVALLO = 30000;
    
    let ultimoCommitVisto = localStorage.getItem('alveare_ultimo_commit') || null;

    const style = document.createElement('style');
    style.textContent = `
        .alveare-nascita {
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(250, 250, 248, 0.95);
            border: 1px solid rgba(170, 145, 75, 0.4);
            padding: 15px 20px;
            max-width: 280px;
            opacity: 0;
            transform: translateY(-20px);
            transition: all 0.5s ease-out;
            z-index: 10000;
            pointer-events: none;
            font-family: 'Inter', -apple-system, sans-serif;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
        }
        .alveare-nascita.visibile {
            opacity: 1;
            transform: translateY(0);
        }
        .alveare-nascita::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 2px;
            background: rgba(170, 145, 75, 0.6);
            animation: alveare-pulsa 2s ease-in-out infinite;
        }
        @keyframes alveare-pulsa {
            0%, 100% { opacity: 0.3; }
            50% { opacity: 1; }
        }
        .alveare-nascita-titolo {
            font-size: 0.65rem;
            font-weight: 300;
            letter-spacing: 0.15em;
            color: rgba(170, 145, 75, 0.9);
            margin-bottom: 6px;
            text-transform: uppercase;
        }
        .alveare-nascita-nome {
            font-family: 'Courier New', monospace;
            font-size: 0.8rem;
            color: rgba(26, 26, 26, 0.8);
            word-break: break-all;
        }
        .alveare-nascita-tempo {
            font-size: 0.6rem;
            font-weight: 200;
            color: rgba(26, 26, 26, 0.35);
            font-style: italic;
            margin-top: 4px;
        }
    `;
    document.head.appendChild(style);

    // Crea il box
    const box = document.createElement('div');
    box.className = 'alveare-nascita';
    box.innerHTML = `
        <div class="alveare-nascita-titolo">⬡ Un'ape è nata</div>
        <div class="alveare-nascita-nome"></div>
        <div class="alveare-nascita-tempo"></div>
    `;
    document.body.appendChild(box);

    async function controlla() {
        try {
            const r = await fetch(
                `https://api.github.com/repos/${REPO}/commits?path=${FILE}&per_page=1`,
                { headers: { 'Accept': 'application/vnd.github.v3+json' } }
            );
            if (!r.ok) return;
            
            const commits = await r.json();
            if (!commits.length) return;
            
            const commit = commits[0];
            const sha = commit.sha;
            const data = new Date(commit.commit.author.date);
            const minutiFa = Math.floor((Date.now() - data) / 60000);
            
            if (minutiFa < MINUTI_SOGLIA && sha !== ultimoCommitVisto) {
                ultimoCommitVisto = sha;
                localStorage.setItem('alveare_ultimo_commit', sha);
                
                const msg = commit.commit.message;
                const match = msg.match(/^([a-z]+-[a-z]+-[a-z]+-[a-z]+)/);
                const nome = match ? match[1] : 'ape sconosciuta';
                
                mostra(nome, minutiFa);
            }
        } catch (e) {}
    }

    function mostra(nome, minutiFa) {
        box.querySelector('.alveare-nascita-nome').textContent = nome;
        box.querySelector('.alveare-nascita-tempo').textContent = 
            minutiFa === 0 ? 'adesso' : `${minutiFa} min fa`;
        
        box.classList.add('visibile');
        setTimeout(() => box.classList.remove('visibile'), 12000);
    }

    // Avvia
    setTimeout(controlla, 2000);
    setInterval(controlla, INTERVALLO);
})();
