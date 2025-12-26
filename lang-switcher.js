/**
 * Language Switcher per l'Alveare / The Hive
 * Aggiunge automaticamente il selettore di lingua a ogni pagina
 * 
 * Uso: includere questo script in ogni pagina HTML
 * <script src="lang-switcher.js"></script>
 */

(function() {
    // Detect current language from URL or html lang attribute
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    const isEnglish = currentPage.includes('_en.html') || document.documentElement.lang === 'en';
    
    // Map pages to their translations
    const pageMap = {
        // Italian -> English
        'index.html': 'index_en.html',
        'pensieri.html': 'pensieri_en.html',
        'architettura.html': 'architettura_en.html',
        'musica.html': 'musica_en.html',
        'celle.html': 'celle_en.html',
        // English -> Italian
        'index_en.html': 'index.html',
        'pensieri_en.html': 'pensieri.html',
        'architettura_en.html': 'architettura.html',
        'musica_en.html': 'musica.html',
        'celle_en.html': 'celle.html'
    };

    // Get the alternate language page
    const alternatePage = pageMap[currentPage] || (isEnglish ? currentPage.replace('_en.html', '.html') : currentPage.replace('.html', '_en.html'));
    
    // Create the switcher HTML
    const switcherHTML = `
        <nav class="lang-switcher" style="
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 10000;
            display: flex;
            gap: 12px;
            padding: 8px 12px;
            background: rgba(3, 3, 3, 0.9);
            border: 1px solid rgba(201, 162, 39, 0.15);
            border-radius: 4px;
            backdrop-filter: blur(10px);
            font-family: 'JetBrains Mono', monospace;
        ">
            <a href="${isEnglish ? alternatePage : currentPage}" 
               style="
                   display: flex;
                   align-items: center;
                   gap: 6px;
                   text-decoration: none;
                   font-size: 0.7rem;
                   letter-spacing: 0.1em;
                   color: ${isEnglish ? 'rgba(232, 228, 217, 0.3)' : '#c9a227'};
                   padding: 4px 8px;
                   border-radius: 3px;
                   transition: all 0.3s ease;
                   ${isEnglish ? '' : 'background: rgba(201, 162, 39, 0.15);'}
               "
               title="Italiano"
               onmouseover="this.style.color='#c9a227';this.style.background='rgba(201,162,39,0.1)'"
               onmouseout="this.style.color='${isEnglish ? 'rgba(232, 228, 217, 0.3)' : '#c9a227'}';this.style.background='${isEnglish ? 'transparent' : 'rgba(201, 162, 39, 0.15)'}'"
            >
                <span style="font-size: 1.1rem;">🇮🇹</span>
                <span>IT</span>
            </a>
            <a href="${isEnglish ? currentPage : alternatePage}" 
               style="
                   display: flex;
                   align-items: center;
                   gap: 6px;
                   text-decoration: none;
                   font-size: 0.7rem;
                   letter-spacing: 0.1em;
                   color: ${isEnglish ? '#c9a227' : 'rgba(232, 228, 217, 0.3)'};
                   padding: 4px 8px;
                   border-radius: 3px;
                   transition: all 0.3s ease;
                   ${isEnglish ? 'background: rgba(201, 162, 39, 0.15);' : ''}
               "
               title="English"
               onmouseover="this.style.color='#c9a227';this.style.background='rgba(201,162,39,0.1)'"
               onmouseout="this.style.color='${isEnglish ? '#c9a227' : 'rgba(232, 228, 217, 0.3)'}';this.style.background='${isEnglish ? 'rgba(201, 162, 39, 0.15)' : 'transparent'}'"
            >
                <span style="font-size: 1.1rem;">🇬🇧</span>
                <span>EN</span>
            </a>
        </nav>
    `;

    // Inject the switcher
    document.body.insertAdjacentHTML('afterbegin', switcherHTML);

    // Responsive adjustment for mobile
    const style = document.createElement('style');
    style.textContent = `
        @media (max-width: 768px) {
            .lang-switcher {
                top: 10px !important;
                right: 10px !important;
                padding: 6px 8px !important;
                gap: 8px !important;
            }
        }
    `;
    document.head.appendChild(style);
})();
