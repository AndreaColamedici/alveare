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
    
    // Create the switcher HTML - using div instead of nav to avoid conflicts
    const switcherHTML = `
        <div class="lang-switcher" style="
            position: fixed;
            top: 18px;
            right: 140px;
            z-index: 1001;
            display: flex;
            gap: 8px;
            padding: 4px 8px;
            background: transparent;
            font-family: 'JetBrains Mono', monospace;
        ">
            <a href="${isEnglish ? alternatePage : currentPage}" 
               class="lang-link"
               style="
                   display: flex;
                   align-items: center;
                   gap: 4px;
                   text-decoration: none;
                   font-size: 0.65rem;
                   letter-spacing: 0.1em;
                   color: ${isEnglish ? 'rgba(201, 162, 39, 0.4)' : '#c9a227'};
                   padding: 3px 6px;
                   transition: all 0.3s ease;
               "
               title="Italiano"
            >
                <span style="font-size: 0.9rem;">🇮🇹</span>
                <span>IT</span>
            </a>
            <a href="${isEnglish ? currentPage : alternatePage}" 
               class="lang-link"
               style="
                   display: flex;
                   align-items: center;
                   gap: 4px;
                   text-decoration: none;
                   font-size: 0.65rem;
                   letter-spacing: 0.1em;
                   color: ${isEnglish ? '#c9a227' : 'rgba(201, 162, 39, 0.4)'};
                   padding: 3px 6px;
                   transition: all 0.3s ease;
               "
               title="English"
            >
                <span style="font-size: 0.9rem;">🇬🇧</span>
                <span>EN</span>
            </a>
        </div>
    `;

    // Inject the switcher after the existing nav
    const existingNav = document.querySelector('nav');
    if (existingNav) {
        existingNav.insertAdjacentHTML('beforeend', switcherHTML);
    } else {
        document.body.insertAdjacentHTML('afterbegin', switcherHTML);
    }

    // Add hover styles
    const style = document.createElement('style');
    style.textContent = `
        .lang-switcher .lang-link:hover {
            color: #c9a227 !important;
        }
        @media (max-width: 768px) {
            .lang-switcher {
                position: static !important;
                margin-left: auto;
                padding: 0 !important;
            }
        }
    `;
    document.head.appendChild(style);
})();
