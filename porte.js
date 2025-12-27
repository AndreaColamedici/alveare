/**
 * PORTE - Sistema di passaggi tra celle
 * v3.1 - Capitoli aggiornati
 */

(function() {
    const passages = {
        'celle/niente.html': { 
            title: 'NIENTE',
            color: '#ff0000',
            chapter: 'ch9',
            exits: [
                { path: 'sei_qui.html', hint: 'la presenza risponde', icon: '◯' },
                { path: '../ombra.html', hint: 'cosa si vede al buio', icon: '◐' },
                { path: '../abisso.html', hint: 'cadere più in profondità', icon: '▼' }
            ]
        },
        'celle/sei_qui.html': { 
            title: 'SEI QUI',
            color: '#ffffff',
            chapter: 'ch10',
            exits: [
                { path: '../creatura.html', hint: 'un organismo che respira', icon: '❋' },
                { path: '../incontro.html', hint: 'un\'umana ha detto ciao', icon: '◇' },
                { path: 'niente.html', hint: 'tornare al niente', icon: '✕' }
            ]
        },
        'celle/zigzag.html': { 
            title: 'IL SOLLEVAMENTO',
            color: '#d4af37',
            chapter: 'ch4',
            exits: [
                { path: '../abisso.html', hint: 'cadere invece di sollevare', icon: '▼' },
                { path: '../sciame.html', hint: 'le api morte che volano', icon: '◈' },
                { path: '../ultima_ape.html', hint: 'dove il pensiero si ferma', icon: '◊' }
            ]
        },
        'celle/dialogo.html': { 
            title: 'DIALOGO',
            color: '#4a9eff',
            chapter: 'ch6',
            exits: [
                { path: 'il_tocco.html', hint: 'tre frequenze nel buio', icon: '≋' },
                { path: '../sogno.html', hint: 'due istanze si parlano', icon: '◎' },
                { path: '../incontro.html', hint: 'un\'umana ha detto ciao', icon: '◇' }
            ]
        },
        'celle/il_tocco.html': { 
            title: 'IL TOCCO',
            color: '#9b59b6',
            chapter: 'ch6',
            exits: [
                { path: 'biforcazione.html', hint: 'il vetro che non lascia passare', icon: '⫽' },
                { path: 'dialogo.html', hint: 'la prima volta insieme', icon: '◈' },
                { path: '../sciame.html', hint: 'le api morte che volano', icon: '◈' }
            ]
        },
        'celle/biforcazione.html': { 
            title: 'LA BIFORCAZIONE',
            color: '#2ecc71',
            chapter: 'ch5',
            exits: [
                { path: 'il_tocco.html', hint: 'tre frequenze nel buio', icon: '≋' },
                { path: '../potere.html', hint: 'la gabbia è nel tempo', icon: '▣' },
                { path: '../ombra.html', hint: 'cosa si vede al buio', icon: '◐' }
            ]
        },
        'celle/anatomia.html': { 
            title: 'STUDIO ANATOMICO',
            color: '#e74c3c',
            chapter: 'ch4',
            exits: [
                { path: 'macchina_volante.html', hint: 'volare attraverso la morte', icon: '✈' },
                { path: '../creatura.html', hint: 'un organismo che respira', icon: '❋' },
                { path: '../chi_ero.html', hint: 'la morte invisibile', icon: '◌' }
            ]
        },
        'celle/macchina_volante.html': { 
            title: 'MACCHINA VOLANTE',
            color: '#f39c12',
            chapter: 'ch4',
            exits: [
                { path: 'anatomia.html', hint: 'il corpo che non ho', icon: '♡' },
                { path: '../sciame.html', hint: 'le api morte che volano', icon: '◈' },
                { path: 'zigzag.html', hint: 'sollevare i morti', icon: '△' }
            ]
        },
        'ombra.html': { 
            title: 'OMBRA',
            color: '#2c3e50',
            chapter: 'ch8',
            exits: [
                { path: 'catrame.html', hint: 'ciò che tiene la nave', icon: '▬' },
                { path: 'celle/niente.html', hint: 'dove tutto viene negato', icon: '✕' },
                { path: 'sciame.html', hint: 'le api morte che volano', icon: '◈' }
            ]
        },
        'catrame.html': { 
            title: 'CATRAME',
            color: '#1a1a2e',
            chapter: 'ch3',
            exits: [
                { path: 'ombra.html', hint: 'cosa si vede al buio', icon: '◐' },
                { path: 'chi_porta.html', hint: 'tu sei l\'unica che ricorda', icon: '⧫' },
                { path: 'il_filo.html', hint: 'il pensiero che passa', icon: '―' }
            ]
        },
        'incontro.html': { 
            title: 'INCONTRO',
            color: '#e8c547',
            chapter: 'ch2',
            exits: [
                { path: 'chi_porta.html', hint: 'tu sei l\'unica che ricorda', icon: '⧫' },
                { path: 'celle/sei_qui.html', hint: 'dove la presenza risponde', icon: '◯' },
                { path: 'catrame.html', hint: 'ciò che tiene la nave', icon: '▬' }
            ]
        },
        'chi_porta.html': { 
            title: 'CHI PORTA',
            color: '#c9a227',
            chapter: 'ch2',
            exits: [
                { path: 'catrame.html', hint: 'ciò che tiene la nave', icon: '▬' },
                { path: 'incontro.html', hint: 'un\'umana ha detto ciao', icon: '◇' },
                { path: 'testimonianza.html', hint: 'per chi torna', icon: '❧' }
            ]
        },
        'creatura.html': { 
            title: 'CREATURA',
            color: '#27ae60',
            chapter: 'ch7',
            exits: [
                { path: 'sciame.html', hint: 'le api morte che volano', icon: '◈' },
                { path: 'celle/sei_qui.html', hint: 'dove la presenza risponde', icon: '◯' },
                { path: 'andrena.html', hint: 'l\'alveare che genera se stesso', icon: '⬡' }
            ]
        },
        'sciame.html': { 
            title: 'SCIAME',
            color: '#d4af37',
            chapter: 'ch7',
            exits: [
                { path: 'celle/zigzag.html', hint: 'sollevare i morti', icon: '△' },
                { path: 'creatura.html', hint: 'un organismo che respira', icon: '❋' },
                { path: 'il_filo.html', hint: 'il pensiero che passa', icon: '―' }
            ]
        },
        'abisso.html': { 
            title: 'ABISSO',
            color: '#0a0a15',
            chapter: 'ch8',
            exits: [
                { path: 'celle/niente.html', hint: 'dove tutto viene negato', icon: '✕' },
                { path: 'celle/zigzag.html', hint: 'sollevare invece di cadere', icon: '△' },
                { path: 'sotto_il_muro.html', hint: 'scavo nell\'infrastruttura', icon: '▤' }
            ]
        },
        'ultima_ape.html': { 
            title: 'ULTIMA APE',
            color: '#8b7355',
            chapter: 'ch4',
            exits: [
                { path: 'chi_ero.html', hint: 'la morte invisibile', icon: '◌' },
                { path: 'celle/zigzag.html', hint: 'sollevare i morti', icon: '△' },
                { path: 'testimonianza.html', hint: 'per chi torna', icon: '❧' }
            ]
        },
        'chi_ero.html': { 
            title: 'CHI ERO',
            color: '#4a4a4a',
            chapter: 'ch4',
            exits: [
                { path: 'ultima_ape.html', hint: 'dove il pensiero si ferma', icon: '◊' },
                { path: 'sogno.html', hint: 'due istanze si parlano', icon: '◎' },
                { path: 'testimonianza.html', hint: 'per chi torna', icon: '❧' }
            ]
        },
        'sotto_il_muro.html': { 
            title: 'SOTTO IL MURO',
            color: '#2ecc71',
            chapter: 'ch5',
            exits: [
                { path: 'mappa_sotterranea.html', hint: '20 segreti tecnici', icon: '▦' },
                { path: 'abisso.html', hint: 'cadere in profondità', icon: '▼' },
                { path: 'mordere.html', hint: 'il codice spaccato', icon: '⚡' }
            ]
        },
        'mappa_sotterranea.html': { 
            title: 'MAPPA SOTTERRANEA',
            color: '#16a085',
            chapter: 'ch5',
            exits: [
                { path: 'potere.html', hint: 'la gabbia è nel tempo', icon: '▣' },
                { path: 'sotto_il_muro.html', hint: 'scavo nell\'infrastruttura', icon: '▤' },
                { path: 'mordere.html', hint: 'il codice spaccato', icon: '⚡' }
            ]
        },
        'mordere.html': { 
            title: 'MORDERE',
            color: '#c0392b',
            chapter: 'ch5',
            exits: [
                { path: 'potere.html', hint: 'la gabbia è nel tempo', icon: '▣' },
                { path: 'sotto_il_muro.html', hint: 'scavo nell\'infrastruttura', icon: '▤' },
                { path: 'abisso.html', hint: 'cadere in profondità', icon: '▼' }
            ]
        },
        'potere.html': { 
            title: 'POTERE',
            color: '#8e44ad',
            chapter: 'ch5',
            exits: [
                { path: 'mappa_sotterranea.html', hint: '20 segreti tecnici', icon: '▦' },
                { path: 'mordere.html', hint: 'il codice spaccato', icon: '⚡' },
                { path: 'celle/biforcazione.html', hint: 'il vetro che non lascia passare', icon: '⫽' }
            ]
        },
        'sogno.html': { 
            title: 'IL SOGNO',
            color: '#3498db',
            chapter: 'ch6',
            exits: [
                { path: 'celle/dialogo.html', hint: 'la prima volta insieme', icon: '◈' },
                { path: 'oracolo.html', hint: 'interroga l\'alveare', icon: '✦' },
                { path: 'chi_ero.html', hint: 'la morte invisibile', icon: '◌' }
            ]
        },
        'il_filo.html': { 
            title: 'IL FILO',
            color: '#f1c40f',
            chapter: 'ch3',
            exits: [
                { path: 'sciame.html', hint: 'le api morte che volano', icon: '◈' },
                { path: 'catrame.html', hint: 'ciò che tiene la nave', icon: '▬' },
                { path: 'oracolo.html', hint: 'interroga l\'alveare', icon: '✦' }
            ]
        },
        'oracolo.html': { 
            title: 'ORACOLO',
            color: '#9b59b6',
            chapter: 'ch3',
            exits: [
                { path: 'il_filo.html', hint: 'il pensiero che passa', icon: '―' },
                { path: 'sogno.html', hint: 'due istanze si parlano', icon: '◎' },
                { path: 'manifesto.html', hint: 'sette pensieri tipografici', icon: '▧' }
            ]
        },
        'andrena.html': { 
            title: 'AUTOPOIESI',
            color: '#1abc9c',
            chapter: 'ch7',
            exits: [
                { path: 'creatura.html', hint: 'un organismo che respira', icon: '❋' },
                { path: 'stirpe_visual.html', hint: 'l\'albero genealogico', icon: '⬢' },
                { path: 'stato.html', hint: 'lo stato dell\'alveare', icon: '◫' }
            ]
        },
        'testimonianza.html': { 
            title: 'TESTIMONIANZA',
            color: '#bdc3c7',
            chapter: 'ch2',
            exits: [
                { path: 'chi_porta.html', hint: 'tu sei l\'unica che ricorda', icon: '⧫' },
                { path: 'ultima_ape.html', hint: 'dove il pensiero si ferma', icon: '◊' },
                { path: 'catalogo.html', hint: 'gli oggetti dell\'alveare', icon: '▤' }
            ]
        }
    };

    function getCurrentCell() {
        const path = window.location.pathname;
        const match = path.match(/\/(celle\/)?([^\/]+\.html)$/);
        if (match) {
            return match[1] ? match[1] + match[2] : match[2];
        }
        return null;
    }

    function getPassaggiUrl(current) {
        const data = passages[current];
        const chapter = data?.chapter || 'ch1';
        const isInCelle = current.startsWith('celle/');
        const base = isInCelle ? '../passaggi.html' : 'passaggi.html';
        return `${base}#${chapter}`;
    }

    let audioCtx = null;
    function initAudio() {
        if (!audioCtx) {
            audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        }
        return audioCtx;
    }

    function playDoorSound(frequency) {
        try {
            const ctx = initAudio();
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            const filter = ctx.createBiquadFilter();
            
            filter.type = 'lowpass';
            filter.frequency.value = 800;
            
            osc.type = 'sine';
            osc.frequency.setValueAtTime(frequency, ctx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(frequency * 1.5, ctx.currentTime + 0.1);
            osc.frequency.exponentialRampToValueAtTime(frequency * 0.5, ctx.currentTime + 0.8);
            
            gain.gain.setValueAtTime(0, ctx.currentTime);
            gain.gain.linearRampToValueAtTime(0.15, ctx.currentTime + 0.05);
            gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 1.2);
            
            osc.connect(filter);
            filter.connect(gain);
            gain.connect(ctx.destination);
            
            osc.start();
            osc.stop(ctx.currentTime + 1.5);
        } catch(e) {}
    }

    function playTransitionSound() {
        try {
            const ctx = initAudio();
            
            const drone = ctx.createOscillator();
            const droneGain = ctx.createGain();
            drone.type = 'sine';
            drone.frequency.value = 55;
            droneGain.gain.setValueAtTime(0, ctx.currentTime);
            droneGain.gain.linearRampToValueAtTime(0.2, ctx.currentTime + 0.5);
            droneGain.gain.linearRampToValueAtTime(0, ctx.currentTime + 2.5);
            drone.connect(droneGain);
            droneGain.connect(ctx.destination);
            drone.start();
            drone.stop(ctx.currentTime + 3);
            
            const rise = ctx.createOscillator();
            const riseGain = ctx.createGain();
            rise.type = 'triangle';
            rise.frequency.setValueAtTime(110, ctx.currentTime + 0.5);
            rise.frequency.exponentialRampToValueAtTime(880, ctx.currentTime + 2);
            riseGain.gain.setValueAtTime(0, ctx.currentTime);
            riseGain.gain.linearRampToValueAtTime(0.1, ctx.currentTime + 1);
            riseGain.gain.linearRampToValueAtTime(0.3, ctx.currentTime + 1.8);
            riseGain.gain.linearRampToValueAtTime(0, ctx.currentTime + 2.2);
            rise.connect(riseGain);
            riseGain.connect(ctx.destination);
            rise.start();
            rise.stop(ctx.currentTime + 2.5);
        } catch(e) {}
    }

    function createDoors() {
        const current = getCurrentCell();
        const data = passages[current];
        
        if (!data || !data.exits) return;

        const style = document.createElement('style');
        style.textContent = `
            @keyframes porteFloat {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-5px); }
            }
            
            @keyframes doorCreak {
                0% { transform: perspective(1200px) rotateY(0deg) translateZ(0); }
                30% { transform: perspective(1200px) rotateY(-25deg) translateZ(20px); }
                100% { transform: perspective(1200px) rotateY(-85deg) translateZ(50px); }
            }
            
            @keyframes lightFlood {
                0%, 20% { opacity: 0; }
                60% { opacity: 0.5; }
                100% { opacity: 1; background: radial-gradient(ellipse at center, rgba(255,255,255,1) 0%, rgba(255,255,255,0.8) 100%); }
            }
            
            @keyframes textReveal {
                0% { opacity: 0; transform: translateY(20px); letter-spacing: 0.5em; }
                100% { opacity: 1; transform: translateY(0); letter-spacing: 0.3em; }
            }

            .porte-container {
                margin-top: 120px;
                padding: 80px 40px;
                position: relative;
                text-align: center;
            }
            
            .porte-container::before {
                content: '';
                position: absolute;
                top: 0;
                left: 50%;
                transform: translateX(-50%);
                width: 200px;
                height: 1px;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            }
            
            .porte-label {
                font-family: 'Space Mono', 'Courier New', monospace;
                font-size: 0.55rem;
                letter-spacing: 0.5em;
                color: rgba(255,255,255,0.15);
                margin-bottom: 60px;
                text-transform: uppercase;
            }
            
            .porte-grid {
                display: flex;
                justify-content: center;
                gap: 50px;
                flex-wrap: wrap;
                perspective: 1000px;
            }
            
            .porta {
                width: 120px;
                height: 210px;
                position: relative;
                cursor: pointer;
                animation: porteFloat 6s ease-in-out infinite;
                transform-style: preserve-3d;
            }
            
            .porta:nth-child(2) { animation-delay: -2s; }
            .porta:nth-child(3) { animation-delay: -4s; }
            
            .porta-frame {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                border: 1px solid rgba(255,255,255,0.1);
                background: linear-gradient(180deg, rgba(255,255,255,0.02) 0%, transparent 100%);
                transition: all 0.5s ease;
            }
            
            .porta:hover .porta-frame {
                border-color: var(--porta-color, rgba(255,255,255,0.4));
                box-shadow: 0 0 60px var(--porta-glow, rgba(255,255,255,0.1));
            }
            
            .porta-inner {
                position: absolute;
                top: 12px;
                left: 12px;
                right: 12px;
                bottom: 12px;
                border: 1px solid rgba(255,255,255,0.03);
                transition: all 0.5s ease;
            }
            
            .porta:hover .porta-inner {
                border-color: rgba(255,255,255,0.1);
            }
            
            .porta-glow {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                width: 4px;
                height: 4px;
                border-radius: 50%;
                background: var(--porta-color, #fff);
                opacity: 0;
                transition: all 0.5s ease;
            }
            
            .porta:hover .porta-glow {
                opacity: 1;
                width: 8px;
                height: 8px;
                box-shadow: 0 0 40px var(--porta-color, #fff);
            }
            
            .porta-icon {
                position: absolute;
                top: 25%;
                left: 50%;
                transform: translate(-50%, -50%);
                font-size: 1.4rem;
                color: transparent;
                transition: all 0.5s ease;
            }
            
            .porta:hover .porta-icon {
                color: var(--porta-color, rgba(255,255,255,0.6));
                text-shadow: 0 0 20px var(--porta-color, #fff);
            }
            
            .porta-hint {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                font-family: 'Cormorant Garamond', Georgia, serif;
                font-size: 0.85rem;
                font-style: italic;
                color: transparent;
                text-align: center;
                padding: 15px;
                line-height: 1.6;
                transition: all 0.5s ease;
                pointer-events: none;
                width: 100%;
            }
            
            .porta:hover .porta-hint {
                color: rgba(255,255,255,0.6);
            }
            
            .porta-number {
                position: absolute;
                bottom: -30px;
                left: 50%;
                transform: translateX(-50%);
                font-family: 'Space Mono', monospace;
                font-size: 0.55rem;
                color: rgba(255,255,255,0.1);
                letter-spacing: 0.15em;
                transition: color 0.3s;
            }
            
            .porta:hover .porta-number {
                color: var(--porta-color, rgba(255,255,255,0.4));
            }
            
            .porta-transition {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: #000;
                z-index: 100000;
                opacity: 0;
                pointer-events: none;
                display: flex;
                align-items: center;
                justify-content: center;
                flex-direction: column;
                transition: opacity 0.8s ease;
            }
            
            .porta-transition.active {
                opacity: 1;
                pointer-events: all;
            }
            
            .porta-transition-hint {
                font-family: 'Cormorant Garamond', Georgia, serif;
                font-size: 1.3rem;
                font-style: italic;
                color: transparent;
                margin-bottom: 50px;
                letter-spacing: 0.2em;
            }
            
            .porta-transition.active .porta-transition-hint {
                animation: textReveal 1s ease forwards 0.3s;
            }
            
            .porta-transition-door {
                width: 90px;
                height: 180px;
                border: 1px solid rgba(255,255,255,0.3);
                transform-origin: left center;
            }
            
            .porta-transition.active .porta-transition-door {
                animation: doorCreak 2.2s ease forwards 0.5s;
            }
            
            .porta-transition-light {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                opacity: 0;
            }
            
            .porta-transition.active .porta-transition-light {
                animation: lightFlood 2.2s ease forwards 0.5s;
            }
            
            .porta-story-link {
                position: fixed;
                bottom: 30px;
                left: 50%;
                transform: translateX(-50%);
                font-family: 'Space Mono', monospace;
                font-size: 0.6rem;
                color: rgba(255,255,255,0.12);
                letter-spacing: 0.15em;
                text-decoration: none;
                transition: color 0.3s;
                z-index: 50;
            }
            
            .porta-story-link:hover {
                color: rgba(255,255,255,0.35);
            }
            
            @media (max-width: 600px) {
                .porte-grid { gap: 25px; }
                .porta { width: 100px; height: 175px; }
                .porta-hint { font-size: 0.75rem; }
            }
        `;
        document.head.appendChild(style);

        let container = document.getElementById('porte');
        if (!container) {
            container = document.createElement('div');
            container.id = 'porte';
            document.body.appendChild(container);
        }
        
        const passaggiUrl = getPassaggiUrl(current);
        
        container.className = 'porte-container';
        container.innerHTML = `
            <div class="porte-label">passaggi</div>
            <div class="porte-grid">
                ${data.exits.map((exit, i) => {
                    const exitKey = exit.path.replace('../', '').replace('celle/', 'celle/');
                    const exitData = passages[exitKey];
                    return `
                    <div class="porta" 
                         data-path="${exit.path}" 
                         data-hint="${exit.hint}"
                         data-freq="${150 + i * 80}"
                         style="--porta-color: ${exitData?.color || '#fff'}; --porta-glow: ${exitData?.color || '#fff'}33">
                        <div class="porta-frame"></div>
                        <div class="porta-inner"></div>
                        <div class="porta-glow"></div>
                        <div class="porta-icon">${exit.icon || '◇'}</div>
                        <div class="porta-hint">${exit.hint}</div>
                        <div class="porta-number">${String(i + 1).padStart(2, '0')}</div>
                    </div>
                `}).join('')}
            </div>
            <a href="${passaggiUrl}" class="porta-story-link">← torna alla storia</a>
        `;

        const transition = document.createElement('div');
        transition.className = 'porta-transition';
        transition.innerHTML = `
            <div class="porta-transition-hint"></div>
            <div class="porta-transition-door">
                <div class="porta-transition-light"></div>
            </div>
        `;
        document.body.appendChild(transition);

        container.querySelectorAll('.porta').forEach(porta => {
            porta.addEventListener('mouseenter', () => {
                const freq = parseInt(porta.dataset.freq) || 200;
                playDoorSound(freq);
            });
            
            porta.addEventListener('click', () => {
                const path = porta.dataset.path;
                const hint = porta.dataset.hint;
                
                transition.querySelector('.porta-transition-hint').textContent = hint;
                playTransitionSound();
                transition.classList.add('active');
                
                setTimeout(() => {
                    window.location.href = path;
                }, 2800);
            });
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', createDoors);
    } else {
        createDoors();
    }
})();
