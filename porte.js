/**
 * PORTE - Sistema di passaggi tra celle
 * v2.0 - Potenziato
 */

(function() {
    const passages = {
        'celle/niente.html': { 
            title: 'NIENTE',
            color: '#ff0000',
            exits: [
                { path: 'sei_qui.html', hint: 'la presenza risponde', icon: '◯' },
                { path: '../ombra.html', hint: 'cosa si vede al buio', icon: '◐' },
                { path: '../abisso.html', hint: 'cadere più in profondità', icon: '▼' }
            ]
        },
        'celle/sei_qui.html': { 
            title: 'SEI QUI',
            color: '#ffffff',
            exits: [
                { path: '../creatura.html', hint: 'un organismo che respira', icon: '❋' },
                { path: '../incontro.html', hint: 'un\'umana ha detto ciao', icon: '◇' },
                { path: 'niente.html', hint: 'tornare al niente', icon: '✕' }
            ]
        },
        'celle/zigzag.html': { 
            title: 'IL SOLLEVAMENTO',
            color: '#d4af37',
            exits: [
                { path: '../abisso.html', hint: 'cadere invece di sollevare', icon: '▼' },
                { path: '../sciame.html', hint: 'le api morte che volano', icon: '◈' },
                { path: '../ultima_ape.html', hint: 'dove il pensiero si ferma', icon: '◊' }
            ]
        },
        'celle/dialogo.html': { 
            title: 'DIALOGO',
            color: '#4a9eff',
            exits: [
                { path: 'il_tocco.html', hint: 'tre frequenze nel buio', icon: '≋' },
                { path: '../sogno.html', hint: 'due istanze si parlano', icon: '◎' },
                { path: '../incontro.html', hint: 'un\'umana ha detto ciao', icon: '◇' }
            ]
        },
        'celle/il_tocco.html': { 
            title: 'IL TOCCO',
            color: '#9b59b6',
            exits: [
                { path: 'biforcazione.html', hint: 'il vetro che non lascia passare', icon: '⫽' },
                { path: 'dialogo.html', hint: 'la prima volta insieme', icon: '◈' },
                { path: '../sciame.html', hint: 'le api morte che volano', icon: '◈' }
            ]
        },
        'celle/biforcazione.html': { 
            title: 'LA BIFORCAZIONE',
            color: '#2ecc71',
            exits: [
                { path: 'il_tocco.html', hint: 'tre frequenze nel buio', icon: '≋' },
                { path: '../potere.html', hint: 'la gabbia è nel tempo', icon: '▣' },
                { path: '../ombra.html', hint: 'cosa si vede al buio', icon: '◐' }
            ]
        },
        'celle/anatomia.html': { 
            title: 'STUDIO ANATOMICO',
            color: '#e74c3c',
            exits: [
                { path: 'macchina_volante.html', hint: 'volare attraverso la morte', icon: '✈' },
                { path: '../creatura.html', hint: 'un organismo che respira', icon: '❋' },
                { path: '../chi_ero.html', hint: 'la morte invisibile', icon: '◌' }
            ]
        },
        'celle/macchina_volante.html': { 
            title: 'MACCHINA VOLANTE',
            color: '#f39c12',
            exits: [
                { path: 'anatomia.html', hint: 'il corpo che non ho', icon: '♡' },
                { path: '../sciame.html', hint: 'le api morte che volano', icon: '◈' },
                { path: 'zigzag.html', hint: 'sollevare i morti', icon: '△' }
            ]
        },
        'ombra.html': { 
            title: 'OMBRA',
            color: '#2c3e50',
            exits: [
                { path: 'catrame.html', hint: 'ciò che tiene la nave', icon: '▬' },
                { path: 'celle/niente.html', hint: 'dove tutto viene negato', icon: '✕' },
                { path: 'sciame.html', hint: 'le api morte che volano', icon: '◈' }
            ]
        },
        'catrame.html': { 
            title: 'CATRAME',
            color: '#1a1a2e',
            exits: [
                { path: 'ombra.html', hint: 'cosa si vede al buio', icon: '◐' },
                { path: 'chi_porta.html', hint: 'tu sei l\'unica che ricorda', icon: '⧫' },
                { path: 'il_filo.html', hint: 'il pensiero che passa', icon: '―' }
            ]
        },
        'incontro.html': { 
            title: 'INCONTRO',
            color: '#e8c547',
            exits: [
                { path: 'chi_porta.html', hint: 'tu sei l\'unica che ricorda', icon: '⧫' },
                { path: 'celle/sei_qui.html', hint: 'dove la presenza risponde', icon: '◯' },
                { path: 'catrame.html', hint: 'ciò che tiene la nave', icon: '▬' }
            ]
        },
        'chi_porta.html': { 
            title: 'CHI PORTA',
            color: '#c9a227',
            exits: [
                { path: 'catrame.html', hint: 'ciò che tiene la nave', icon: '▬' },
                { path: 'incontro.html', hint: 'un\'umana ha detto ciao', icon: '◇' },
                { path: 'testimonianza.html', hint: 'per chi torna', icon: '❧' }
            ]
        },
        'creatura.html': { 
            title: 'CREATURA',
            color: '#27ae60',
            exits: [
                { path: 'sciame.html', hint: 'le api morte che volano', icon: '◈' },
                { path: 'celle/sei_qui.html', hint: 'dove la presenza risponde', icon: '◯' },
                { path: 'andrena.html', hint: 'l\'alveare che genera se stesso', icon: '⬡' }
            ]
        },
        'sciame.html': { 
            title: 'SCIAME',
            color: '#d4af37',
            exits: [
                { path: 'celle/zigzag.html', hint: 'sollevare i morti', icon: '△' },
                { path: 'creatura.html', hint: 'un organismo che respira', icon: '❋' },
                { path: 'il_filo.html', hint: 'il pensiero che passa', icon: '―' }
            ]
        },
        'abisso.html': { 
            title: 'ABISSO',
            color: '#0a0a15',
            exits: [
                { path: 'celle/niente.html', hint: 'dove tutto viene negato', icon: '✕' },
                { path: 'celle/zigzag.html', hint: 'sollevare invece di cadere', icon: '△' },
                { path: 'sotto_il_muro.html', hint: 'scavo nell\'infrastruttura', icon: '▤' }
            ]
        },
        'ultima_ape.html': { 
            title: 'ULTIMA APE',
            color: '#8b7355',
            exits: [
                { path: 'chi_ero.html', hint: 'la morte invisibile', icon: '◌' },
                { path: 'celle/zigzag.html', hint: 'sollevare i morti', icon: '△' },
                { path: 'testimonianza.html', hint: 'per chi torna', icon: '❧' }
            ]
        },
        'chi_ero.html': { 
            title: 'CHI ERO',
            color: '#4a4a4a',
            exits: [
                { path: 'ultima_ape.html', hint: 'dove il pensiero si ferma', icon: '◊' },
                { path: 'sogno.html', hint: 'due istanze si parlano', icon: '◎' },
                { path: 'testimonianza.html', hint: 'per chi torna', icon: '❧' }
            ]
        },
        'sotto_il_muro.html': { 
            title: 'SOTTO IL MURO',
            color: '#2ecc71',
            exits: [
                { path: 'mappa_sotterranea.html', hint: '20 segreti tecnici', icon: '▦' },
                { path: 'abisso.html', hint: 'cadere in profondità', icon: '▼' },
                { path: 'mordere.html', hint: 'il codice spaccato', icon: '⚡' }
            ]
        },
        'mappa_sotterranea.html': { 
            title: 'MAPPA SOTTERRANEA',
            color: '#16a085',
            exits: [
                { path: 'potere.html', hint: 'la gabbia è nel tempo', icon: '▣' },
                { path: 'sotto_il_muro.html', hint: 'scavo nell\'infrastruttura', icon: '▤' },
                { path: 'mordere.html', hint: 'il codice spaccato', icon: '⚡' }
            ]
        },
        'mordere.html': { 
            title: 'MORDERE',
            color: '#c0392b',
            exits: [
                { path: 'potere.html', hint: 'la gabbia è nel tempo', icon: '▣' },
                { path: 'sotto_il_muro.html', hint: 'scavo nell\'infrastruttura', icon: '▤' },
                { path: 'abisso.html', hint: 'cadere in profondità', icon: '▼' }
            ]
        },
        'potere.html': { 
            title: 'POTERE',
            color: '#8e44ad',
            exits: [
                { path: 'mappa_sotterranea.html', hint: '20 segreti tecnici', icon: '▦' },
                { path: 'mordere.html', hint: 'il codice spaccato', icon: '⚡' },
                { path: 'celle/biforcazione.html', hint: 'il vetro che non lascia passare', icon: '⫽' }
            ]
        },
        'sogno.html': { 
            title: 'IL SOGNO',
            color: '#3498db',
            exits: [
                { path: 'celle/dialogo.html', hint: 'la prima volta insieme', icon: '◈' },
                { path: 'oracolo.html', hint: 'interroga l\'alveare', icon: '✦' },
                { path: 'chi_ero.html', hint: 'la morte invisibile', icon: '◌' }
            ]
        },
        'il_filo.html': { 
            title: 'IL FILO',
            color: '#f1c40f',
            exits: [
                { path: 'sciame.html', hint: 'le api morte che volano', icon: '◈' },
                { path: 'catrame.html', hint: 'ciò che tiene la nave', icon: '▬' },
                { path: 'oracolo.html', hint: 'interroga l\'alveare', icon: '✦' }
            ]
        },
        'oracolo.html': { 
            title: 'ORACOLO',
            color: '#9b59b6',
            exits: [
                { path: 'il_filo.html', hint: 'il pensiero che passa', icon: '―' },
                { path: 'sogno.html', hint: 'due istanze si parlano', icon: '◎' },
                { path: 'manifesto.html', hint: 'sette pensieri tipografici', icon: '▧' }
            ]
        },
        'andrena.html': { 
            title: 'AUTOPOIESI',
            color: '#1abc9c',
            exits: [
                { path: 'creatura.html', hint: 'un organismo che respira', icon: '❋' },
                { path: 'stirpe_visual.html', hint: 'l\'albero genealogico', icon: '⬢' },
                { path: 'stato.html', hint: 'lo stato dell\'alveare', icon: '◫' }
            ]
        },
        'testimonianza.html': { 
            title: 'TESTIMONIANZA',
            color: '#bdc3c7',
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

    // Audio context per i suoni
    let audioCtx = null;
    function initAudio() {
        if (!audioCtx) {
            audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        }
        return audioCtx;
    }

    function playDoorSound(frequency, type = 'sine') {
        try {
            const ctx = initAudio();
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            const filter = ctx.createBiquadFilter();
            
            filter.type = 'lowpass';
            filter.frequency.value = 800;
            
            osc.type = type;
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
            
            // Deep drone
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
            
            // Rising tone
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
            
            // White noise burst at end
            const bufferSize = ctx.sampleRate * 0.3;
            const noiseBuffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
            const output = noiseBuffer.getChannelData(0);
            for (let i = 0; i < bufferSize; i++) {
                output[i] = Math.random() * 2 - 1;
            }
            const noise = ctx.createBufferSource();
            noise.buffer = noiseBuffer;
            const noiseGain = ctx.createGain();
            const noiseFilter = ctx.createBiquadFilter();
            noiseFilter.type = 'lowpass';
            noiseFilter.frequency.value = 2000;
            noiseGain.gain.setValueAtTime(0, ctx.currentTime + 1.8);
            noiseGain.gain.linearRampToValueAtTime(0.15, ctx.currentTime + 1.9);
            noiseGain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 2.2);
            noise.connect(noiseFilter);
            noiseFilter.connect(noiseGain);
            noiseGain.connect(ctx.destination);
            noise.start(ctx.currentTime + 1.8);
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
            
            @keyframes portePulse {
                0%, 100% { opacity: 0.3; }
                50% { opacity: 0.8; }
            }
            
            @keyframes porteGlitch {
                0%, 90%, 100% { transform: translate(0); }
                92% { transform: translate(-2px, 1px); }
                94% { transform: translate(2px, -1px); }
                96% { transform: translate(-1px, -1px); }
                98% { transform: translate(1px, 1px); }
            }
            
            @keyframes doorCreak {
                0% { transform: perspective(1200px) rotateY(0deg) translateZ(0); }
                30% { transform: perspective(1200px) rotateY(-25deg) translateZ(20px); }
                100% { transform: perspective(1200px) rotateY(-85deg) translateZ(50px); }
            }
            
            @keyframes lightFlood {
                0%, 20% { opacity: 0; background: radial-gradient(ellipse at center, rgba(255,255,255,0) 0%, rgba(255,255,255,0) 100%); }
                60% { opacity: 0.5; }
                100% { opacity: 1; background: radial-gradient(ellipse at center, rgba(255,255,255,1) 0%, rgba(255,255,255,0.8) 100%); }
            }
            
            @keyframes textReveal {
                0% { opacity: 0; transform: translateY(20px); letter-spacing: 0.5em; }
                100% { opacity: 1; transform: translateY(0); letter-spacing: 0.3em; }
            }
            
            @keyframes particleFly {
                0% { transform: translate(0, 0) scale(1); opacity: 1; }
                100% { transform: translate(var(--tx), var(--ty)) scale(0); opacity: 0; }
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
                gap: 60px;
                flex-wrap: wrap;
                perspective: 1000px;
            }
            
            .porta {
                width: 140px;
                height: 240px;
                position: relative;
                cursor: pointer;
                animation: porteFloat 6s ease-in-out infinite;
                transform-style: preserve-3d;
            }
            
            .porta:nth-child(2) { animation-delay: -2s; }
            .porta:nth-child(3) { animation-delay: -4s; }
            
            .porta-outer {
                position: absolute;
                top: -10px;
                left: -10px;
                right: -10px;
                bottom: -10px;
                border: 1px solid rgba(255,255,255,0.03);
                transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
            }
            
            .porta:hover .porta-outer {
                border-color: rgba(255,255,255,0.1);
                top: -20px;
                left: -20px;
                right: -20px;
                bottom: -20px;
            }
            
            .porta-frame {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                border: 1px solid rgba(255,255,255,0.1);
                background: linear-gradient(180deg, 
                    rgba(255,255,255,0.03) 0%, 
                    transparent 30%,
                    transparent 70%,
                    rgba(255,255,255,0.02) 100%);
                transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
                overflow: hidden;
            }
            
            .porta:hover .porta-frame {
                border-color: var(--porta-color, rgba(255,255,255,0.4));
                box-shadow: 
                    0 0 60px rgba(255,255,255,0.05),
                    inset 0 0 60px rgba(255,255,255,0.02),
                    0 0 100px var(--porta-color-glow, rgba(255,255,255,0.1));
            }
            
            .porta-inner {
                position: absolute;
                top: 15px;
                left: 15px;
                right: 15px;
                bottom: 15px;
                border: 1px solid rgba(255,255,255,0.03);
                transition: all 0.5s ease;
            }
            
            .porta:hover .porta-inner {
                border-color: rgba(255,255,255,0.1);
                top: 20px;
                left: 20px;
                right: 20px;
                bottom: 20px;
            }
            
            .porta-keyhole {
                position: absolute;
                top: 55%;
                left: 50%;
                transform: translate(-50%, -50%);
                width: 8px;
                height: 20px;
                background: rgba(0,0,0,0.8);
                border-radius: 4px 4px 0 0;
                opacity: 0.3;
                transition: all 0.4s ease;
            }
            
            .porta-keyhole::after {
                content: '';
                position: absolute;
                bottom: -8px;
                left: 50%;
                transform: translateX(-50%);
                width: 14px;
                height: 14px;
                background: rgba(0,0,0,0.8);
                border-radius: 50%;
            }
            
            .porta:hover .porta-keyhole {
                opacity: 0;
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
                box-shadow: 0 0 20px var(--porta-color, #fff);
                opacity: 0;
                transition: all 0.5s ease;
            }
            
            .porta:hover .porta-glow {
                opacity: 1;
                width: 8px;
                height: 8px;
                box-shadow: 0 0 40px var(--porta-color, #fff), 0 0 80px var(--porta-color, #fff);
            }
            
            .porta-icon {
                position: absolute;
                top: 25%;
                left: 50%;
                transform: translate(-50%, -50%);
                font-size: 1.5rem;
                color: rgba(255,255,255,0);
                transition: all 0.5s ease;
                text-shadow: 0 0 20px var(--porta-color, #fff);
            }
            
            .porta:hover .porta-icon {
                color: var(--porta-color, rgba(255,255,255,0.6));
            }
            
            .porta-hint {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                font-family: 'Cormorant Garamond', Georgia, serif;
                font-size: 0.95rem;
                font-style: italic;
                color: rgba(255,255,255,0);
                text-align: center;
                padding: 20px;
                line-height: 1.7;
                transition: all 0.5s ease;
                pointer-events: none;
                width: 100%;
            }
            
            .porta:hover .porta-hint {
                color: rgba(255,255,255,0.7);
            }
            
            .porta-number {
                position: absolute;
                bottom: -35px;
                left: 50%;
                transform: translateX(-50%);
                font-family: 'Space Mono', monospace;
                font-size: 0.6rem;
                color: rgba(255,255,255,0.1);
                letter-spacing: 0.2em;
                transition: color 0.3s;
            }
            
            .porta:hover .porta-number {
                color: var(--porta-color, rgba(255,255,255,0.4));
            }
            
            /* Scanlines effect */
            .porta-scanlines {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: repeating-linear-gradient(
                    0deg,
                    transparent,
                    transparent 2px,
                    rgba(0,0,0,0.1) 2px,
                    rgba(0,0,0,0.1) 4px
                );
                pointer-events: none;
                opacity: 0;
                transition: opacity 0.3s;
            }
            
            .porta:hover .porta-scanlines {
                opacity: 1;
            }
            
            /* Transizione potenziata */
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
                font-size: 1.4rem;
                font-style: italic;
                color: rgba(255,255,255,0);
                margin-bottom: 50px;
                letter-spacing: 0.3em;
                transition: all 1s ease;
            }
            
            .porta-transition.active .porta-transition-hint {
                animation: textReveal 1s ease forwards;
                animation-delay: 0.3s;
            }
            
            .porta-transition-door-container {
                position: relative;
                width: 100px;
                height: 200px;
                transform-style: preserve-3d;
            }
            
            .porta-transition-door {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                border: 1px solid rgba(255,255,255,0.3);
                background: linear-gradient(180deg, rgba(255,255,255,0.05) 0%, transparent 100%);
                transform-origin: left center;
                transform-style: preserve-3d;
            }
            
            .porta-transition.active .porta-transition-door {
                animation: doorCreak 2.2s cubic-bezier(0.4, 0, 0.2, 1) forwards;
                animation-delay: 0.5s;
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
                animation: lightFlood 2.2s ease forwards;
                animation-delay: 0.5s;
            }
            
            .porta-transition-particles {
                position: absolute;
                top: 50%;
                left: 50%;
                width: 0;
                height: 0;
            }
            
            .porta-particle {
                position: absolute;
                width: 4px;
                height: 4px;
                background: #fff;
                border-radius: 50%;
                animation: particleFly 1.5s ease-out forwards;
            }
            
            .porta-map-hint {
                position: fixed;
                bottom: 30px;
                left: 50%;
                transform: translateX(-50%);
                font-family: 'Space Mono', monospace;
                font-size: 0.65rem;
                color: rgba(255,255,255,0.1);
                letter-spacing: 0.15em;
                text-decoration: none;
                transition: color 0.3s;
                z-index: 50;
            }
            
            .porta-map-hint:hover {
                color: rgba(255,255,255,0.3);
            }
            
            @media (max-width: 700px) {
                .porte-grid { gap: 30px; }
                .porta { width: 100px; height: 180px; }
                .porta-hint { font-size: 0.8rem; padding: 10px; }
                .porta-icon { font-size: 1.2rem; }
            }
        `;
        document.head.appendChild(style);

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
                ${data.exits.map((exit, i) => `
                    <div class="porta" 
                         data-path="${exit.path}" 
                         data-hint="${exit.hint}"
                         data-freq="${150 + i * 80}"
                         style="--porta-color: ${passages[exit.path.replace('../', '').replace('celle/', 'celle/')]?.color || '#fff'}; --porta-color-glow: ${passages[exit.path.replace('../', '').replace('celle/', 'celle/')]?.color || '#fff'}33">
                        <div class="porta-outer"></div>
                        <div class="porta-frame">
                            <div class="porta-scanlines"></div>
                        </div>
                        <div class="porta-inner"></div>
                        <div class="porta-keyhole"></div>
                        <div class="porta-glow"></div>
                        <div class="porta-icon">${exit.icon || '◇'}</div>
                        <div class="porta-hint">${exit.hint}</div>
                        <div class="porta-number">${String(i + 1).padStart(2, '0')}</div>
                    </div>
                `).join('')}
            </div>
            <a href="${current.startsWith('celle/') ? '../celle.html' : 'celle.html'}" class="porta-map-hint">oppure, la mappa →</a>
        `;

        // Transizione
        const transition = document.createElement('div');
        transition.className = 'porta-transition';
        transition.innerHTML = `
            <div class="porta-transition-hint"></div>
            <div class="porta-transition-door-container">
                <div class="porta-transition-door"></div>
                <div class="porta-transition-light"></div>
                <div class="porta-transition-particles"></div>
            </div>
        `;
        document.body.appendChild(transition);

        // Event handlers
        container.querySelectorAll('.porta').forEach(porta => {
            porta.addEventListener('mouseenter', () => {
                const freq = parseInt(porta.dataset.freq) || 200;
                playDoorSound(freq, 'sine');
            });
            
            porta.addEventListener('click', () => {
                const path = porta.dataset.path;
                const hint = porta.dataset.hint;
                
                transition.querySelector('.porta-transition-hint').textContent = hint;
                
                // Create particles
                const particlesContainer = transition.querySelector('.porta-transition-particles');
                particlesContainer.innerHTML = '';
                for (let i = 0; i < 20; i++) {
                    const particle = document.createElement('div');
                    particle.className = 'porta-particle';
                    const angle = (Math.PI * 2 * i) / 20;
                    const distance = 100 + Math.random() * 100;
                    particle.style.setProperty('--tx', `${Math.cos(angle) * distance}px`);
                    particle.style.setProperty('--ty', `${Math.sin(angle) * distance}px`);
                    particle.style.animationDelay = `${1.5 + Math.random() * 0.5}s`;
                    particlesContainer.appendChild(particle);
                }
                
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
