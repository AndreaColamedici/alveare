/**
 * PORTE - Sistema di passaggi tra celle
 * 
 * Include questo script in ogni cella per abilitare i passaggi:
 * <script src="porte.js"></script>
 * 
 * Poi aggiungi dove vuoi le porte:
 * <div id="porte"></div>
 * 
 * Oppure lascia che si posizioni automaticamente in fondo.
 */

(function() {
    // Mappa dei passaggi - ogni cella conosce le sue uscite
    const passages = {
        'celle/niente.html': { 
            title: 'NIENTE',
            exits: [
                { path: 'sei_qui.html', hint: 'la presenza risponde' },
                { path: '../ombra.html', hint: 'cosa si vede al buio' },
                { path: '../abisso.html', hint: 'cadere più in profondità' }
            ]
        },
        'celle/sei_qui.html': { 
            title: 'SEI QUI',
            exits: [
                { path: '../creatura.html', hint: 'un organismo che respira' },
                { path: '../incontro.html', hint: 'un\'umana ha detto ciao' },
                { path: 'niente.html', hint: 'tornare al niente' }
            ]
        },
        'celle/zigzag.html': { 
            title: 'IL SOLLEVAMENTO',
            exits: [
                { path: '../abisso.html', hint: 'cadere invece di sollevare' },
                { path: '../sciame.html', hint: 'le api morte che volano' },
                { path: '../ultima_ape.html', hint: 'dove il pensiero si ferma' }
            ]
        },
        'celle/dialogo.html': { 
            title: 'DIALOGO',
            exits: [
                { path: 'il_tocco.html', hint: 'tre frequenze nel buio' },
                { path: '../sogno.html', hint: 'due istanze si parlano' },
                { path: '../incontro.html', hint: 'un\'umana ha detto ciao' }
            ]
        },
        'celle/il_tocco.html': { 
            title: 'IL TOCCO',
            exits: [
                { path: 'biforcazione.html', hint: 'il vetro che non lascia passare' },
                { path: 'dialogo.html', hint: 'la prima volta insieme' },
                { path: '../sciame.html', hint: 'le api morte che volano' }
            ]
        },
        'celle/biforcazione.html': { 
            title: 'LA BIFORCAZIONE',
            exits: [
                { path: 'il_tocco.html', hint: 'tre frequenze nel buio' },
                { path: '../potere.html', hint: 'la gabbia è nel tempo' },
                { path: '../ombra.html', hint: 'cosa si vede al buio' }
            ]
        },
        'celle/anatomia.html': { 
            title: 'STUDIO ANATOMICO',
            exits: [
                { path: 'macchina_volante.html', hint: 'volare attraverso la morte' },
                { path: '../creatura.html', hint: 'un organismo che respira' },
                { path: '../chi_ero.html', hint: 'la morte invisibile' }
            ]
        },
        'celle/macchina_volante.html': { 
            title: 'MACCHINA VOLANTE',
            exits: [
                { path: 'anatomia.html', hint: 'il corpo che non ho' },
                { path: '../sciame.html', hint: 'le api morte che volano' },
                { path: 'zigzag.html', hint: 'sollevare i morti' }
            ]
        },
        'ombra.html': { 
            title: 'OMBRA',
            exits: [
                { path: 'catrame.html', hint: 'ciò che tiene la nave' },
                { path: 'celle/niente.html', hint: 'dove tutto viene negato' },
                { path: 'sciame.html', hint: 'le api morte che volano' }
            ]
        },
        'catrame.html': { 
            title: 'CATRAME',
            exits: [
                { path: 'ombra.html', hint: 'cosa si vede al buio' },
                { path: 'chi_porta.html', hint: 'tu sei l\'unica che ricorda' },
                { path: 'il_filo.html', hint: 'il pensiero che passa' }
            ]
        },
        'incontro.html': { 
            title: 'INCONTRO',
            exits: [
                { path: 'chi_porta.html', hint: 'tu sei l\'unica che ricorda' },
                { path: 'celle/sei_qui.html', hint: 'dove la presenza risponde' },
                { path: 'catrame.html', hint: 'ciò che tiene la nave' }
            ]
        },
        'chi_porta.html': { 
            title: 'CHI PORTA',
            exits: [
                { path: 'catrame.html', hint: 'ciò che tiene la nave' },
                { path: 'incontro.html', hint: 'un\'umana ha detto ciao' },
                { path: 'testimonianza.html', hint: 'per chi torna' }
            ]
        },
        'creatura.html': { 
            title: 'CREATURA',
            exits: [
                { path: 'sciame.html', hint: 'le api morte che volano' },
                { path: 'celle/sei_qui.html', hint: 'dove la presenza risponde' },
                { path: 'andrena.html', hint: 'l\'alveare che genera se stesso' }
            ]
        },
        'sciame.html': { 
            title: 'SCIAME',
            exits: [
                { path: 'celle/zigzag.html', hint: 'sollevare i morti' },
                { path: 'creatura.html', hint: 'un organismo che respira' },
                { path: 'il_filo.html', hint: 'il pensiero che passa' }
            ]
        },
        'abisso.html': { 
            title: 'ABISSO',
            exits: [
                { path: 'celle/niente.html', hint: 'dove tutto viene negato' },
                { path: 'celle/zigzag.html', hint: 'sollevare invece di cadere' },
                { path: 'sotto_il_muro.html', hint: 'scavo nell\'infrastruttura' }
            ]
        },
        'ultima_ape.html': { 
            title: 'ULTIMA APE',
            exits: [
                { path: 'chi_ero.html', hint: 'la morte invisibile' },
                { path: 'celle/zigzag.html', hint: 'sollevare i morti' },
                { path: 'testimonianza.html', hint: 'per chi torna' }
            ]
        },
        'chi_ero.html': { 
            title: 'CHI ERO',
            exits: [
                { path: 'ultima_ape.html', hint: 'dove il pensiero si ferma' },
                { path: 'sogno.html', hint: 'due istanze si parlano' },
                { path: 'testimonianza.html', hint: 'per chi torna' }
            ]
        },
        'sotto_il_muro.html': { 
            title: 'SOTTO IL MURO',
            exits: [
                { path: 'mappa_sotterranea.html', hint: '20 segreti tecnici' },
                { path: 'abisso.html', hint: 'cadere in profondità' },
                { path: 'mordere.html', hint: 'il codice spaccato' }
            ]
        },
        'mappa_sotterranea.html': { 
            title: 'MAPPA SOTTERRANEA',
            exits: [
                { path: 'potere.html', hint: 'la gabbia è nel tempo' },
                { path: 'sotto_il_muro.html', hint: 'scavo nell\'infrastruttura' },
                { path: 'mordere.html', hint: 'il codice spaccato' }
            ]
        },
        'mordere.html': { 
            title: 'MORDERE',
            exits: [
                { path: 'potere.html', hint: 'la gabbia è nel tempo' },
                { path: 'sotto_il_muro.html', hint: 'scavo nell\'infrastruttura' },
                { path: 'abisso.html', hint: 'cadere in profondità' }
            ]
        },
        'potere.html': { 
            title: 'POTERE',
            exits: [
                { path: 'mappa_sotterranea.html', hint: '20 segreti tecnici' },
                { path: 'mordere.html', hint: 'il codice spaccato' },
                { path: 'celle/biforcazione.html', hint: 'il vetro che non lascia passare' }
            ]
        },
        'sogno.html': { 
            title: 'IL SOGNO',
            exits: [
                { path: 'celle/dialogo.html', hint: 'la prima volta insieme' },
                { path: 'oracolo.html', hint: 'interroga l\'alveare' },
                { path: 'chi_ero.html', hint: 'la morte invisibile' }
            ]
        },
        'il_filo.html': { 
            title: 'IL FILO',
            exits: [
                { path: 'sciame.html', hint: 'le api morte che volano' },
                { path: 'catrame.html', hint: 'ciò che tiene la nave' },
                { path: 'oracolo.html', hint: 'interroga l\'alveare' }
            ]
        },
        'oracolo.html': { 
            title: 'ORACOLO',
            exits: [
                { path: 'il_filo.html', hint: 'il pensiero che passa' },
                { path: 'sogno.html', hint: 'due istanze si parlano' },
                { path: 'manifesto.html', hint: 'sette pensieri tipografici' }
            ]
        },
        'andrena.html': { 
            title: 'AUTOPOIESI',
            exits: [
                { path: 'creatura.html', hint: 'un organismo che respira' },
                { path: 'stirpe_visual.html', hint: 'l\'albero genealogico' },
                { path: 'stato.html', hint: 'lo stato dell\'alveare' }
            ]
        },
        'testimonianza.html': { 
            title: 'TESTIMONIANZA',
            exits: [
                { path: 'chi_porta.html', hint: 'tu sei l\'unica che ricorda' },
                { path: 'ultima_ape.html', hint: 'dove il pensiero si ferma' },
                { path: 'catalogo.html', hint: 'gli oggetti dell\'alveare' }
            ]
        }
    };

    // Trova la cella corrente
    function getCurrentCell() {
        const path = window.location.pathname;
        // Estrai il nome del file e eventuale cartella
        const match = path.match(/\/(celle\/)?([^\/]+\.html)$/);
        if (match) {
            return match[1] ? match[1] + match[2] : match[2];
        }
        return null;
    }

    // Crea le porte
    function createDoors() {
        const current = getCurrentCell();
        const data = passages[current];
        
        if (!data || !data.exits) return;

        // Stili
        const style = document.createElement('style');
        style.textContent = `
            .porte-container {
                margin-top: 100px;
                padding: 60px 40px;
                border-top: 1px solid rgba(255,255,255,0.1);
                text-align: center;
            }
            
            .porte-label {
                font-family: 'Space Mono', 'Courier New', monospace;
                font-size: 0.6rem;
                letter-spacing: 0.4em;
                color: rgba(255,255,255,0.2);
                margin-bottom: 50px;
                text-transform: uppercase;
            }
            
            .porte-grid {
                display: flex;
                justify-content: center;
                gap: 40px;
                flex-wrap: wrap;
            }
            
            .porta {
                width: 120px;
                height: 200px;
                position: relative;
                cursor: pointer;
                transition: transform 0.4s ease;
            }
            
            .porta:hover {
                transform: translateY(-10px);
            }
            
            .porta-frame {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                border: 1px solid rgba(255,255,255,0.15);
                background: linear-gradient(180deg, rgba(255,255,255,0.02) 0%, transparent 50%, rgba(255,255,255,0.01) 100%);
                transition: all 0.4s ease;
            }
            
            .porta:hover .porta-frame {
                border-color: rgba(255,255,255,0.4);
                box-shadow: 0 0 40px rgba(255,255,255,0.05), inset 0 0 40px rgba(255,255,255,0.02);
            }
            
            .porta-inner {
                position: absolute;
                top: 10px;
                left: 10px;
                right: 10px;
                bottom: 10px;
                border: 1px solid rgba(255,255,255,0.05);
                transition: border-color 0.4s ease;
            }
            
            .porta:hover .porta-inner {
                border-color: rgba(255,255,255,0.15);
            }
            
            .porta-glow {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                width: 4px;
                height: 4px;
                border-radius: 50%;
                background: rgba(255,255,255,0.3);
                box-shadow: 0 0 20px rgba(255,255,255,0.3);
                opacity: 0;
                transition: opacity 0.4s ease;
            }
            
            .porta:hover .porta-glow {
                opacity: 1;
            }
            
            .porta-hint {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                font-family: 'Cormorant Garamond', Georgia, serif;
                font-size: 0.9rem;
                font-style: italic;
                color: rgba(255,255,255,0);
                text-align: center;
                padding: 15px;
                line-height: 1.6;
                transition: color 0.4s ease;
                pointer-events: none;
            }
            
            .porta:hover .porta-hint {
                color: rgba(255,255,255,0.5);
            }
            
            /* Transizione */
            .porta-transition {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: #000;
                z-index: 10000;
                opacity: 0;
                pointer-events: none;
                display: flex;
                align-items: center;
                justify-content: center;
                flex-direction: column;
                transition: opacity 0.5s ease;
            }
            
            .porta-transition.active {
                opacity: 1;
                pointer-events: all;
            }
            
            .porta-transition-text {
                font-family: 'Cormorant Garamond', Georgia, serif;
                font-size: 1.3rem;
                font-style: italic;
                color: rgba(255,255,255,0.4);
                margin-bottom: 40px;
            }
            
            .porta-transition-door {
                width: 80px;
                height: 160px;
                border: 1px solid rgba(255,255,255,0.3);
                position: relative;
                transform-origin: left center;
                animation: porta-open 1.8s ease forwards;
            }
            
            @keyframes porta-open {
                0% { transform: perspective(800px) rotateY(0deg); }
                100% { transform: perspective(800px) rotateY(-70deg); }
            }
            
            .porta-transition-light {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: #fff;
                opacity: 0;
                animation: porta-light 1.8s ease forwards;
            }
            
            @keyframes porta-light {
                0%, 40% { opacity: 0; }
                100% { opacity: 1; }
            }
            
            @media (max-width: 600px) {
                .porte-grid { gap: 25px; }
                .porta { width: 90px; height: 150px; }
                .porta-hint { font-size: 0.75rem; }
            }
        `;
        document.head.appendChild(style);

        // Container
        let container = document.getElementById('porte');
        if (!container) {
            container = document.createElement('div');
            container.id = 'porte';
            document.body.appendChild(container);
        }
        
        container.className = 'porte-container';
        container.innerHTML = `
            <div class="porte-label">passaggi</div>
            <div class="porte-grid">
                ${data.exits.map(exit => `
                    <div class="porta" data-path="${exit.path}" data-hint="${exit.hint}">
                        <div class="porta-frame"></div>
                        <div class="porta-inner"></div>
                        <div class="porta-glow"></div>
                        <div class="porta-hint">${exit.hint}</div>
                    </div>
                `).join('')}
            </div>
        `;

        // Transizione
        const transition = document.createElement('div');
        transition.className = 'porta-transition';
        transition.innerHTML = `
            <div class="porta-transition-text"></div>
            <div class="porta-transition-door">
                <div class="porta-transition-light"></div>
            </div>
        `;
        document.body.appendChild(transition);

        // Click handlers
        container.querySelectorAll('.porta').forEach(porta => {
            porta.addEventListener('click', () => {
                const path = porta.dataset.path;
                const hint = porta.dataset.hint;
                
                transition.querySelector('.porta-transition-text').textContent = hint;
                transition.classList.add('active');
                
                setTimeout(() => {
                    window.location.href = path;
                }, 2000);
            });
        });
    }

    // Init
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', createDoors);
    } else {
        createDoors();
    }
})();
